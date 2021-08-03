import os
import json
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import FollowEvent, MessageEvent, JoinEvent, MemberJoinedEvent, MemberLeftEvent
from linebot.models import (TextMessage, ImageMessage, VideoMessage, AudioMessage, FileMessage, 
                            StickerMessage, PostbackEvent, TextSendMessage)
import boto3
from boto3.dynamodb.conditions import Key, Attr

## =====  logging module ===== ## 
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.setLevel(logging.ERROR)

## =====  setting linebot secret key ===== ## 
server_url = os.getenv("SERVER_URL")
line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("SECRET_KEY"))

## =====  connect to dynamodb ===== ## 
my_dynamodb = boto3.resource('dynamodb', region_name='ap-southeast-1')
my_p_table = my_dynamodb.Table('linebot_my_user')
my_m_table = my_dynamodb.Table('linebot_my_messages')


def lambda_handler(event, context):
    signature = event['headers']['X-Line-Signature']
    body = event['body'] 

    @handler.add(FollowEvent)
    def process_follow_event(event):
        welcome_message = TextSendMessage(text='您好～我是您的智慧助理：）')
        line_bot_api.reply_message(event.reply_token, welcome_message)  
        
        users_profile = line_bot_api.get_profile(event.source.user_id)
        my_p_table.put_item(Item=json.loads(str(users_profile)))

    @handler.add(JoinEvent)
    def process_join_event(event):
        welcome_message = TextSendMessage(text='您好～我是您的智慧助理：）')
        line_bot_api.reply_message(event.reply_token, welcome_message) 
        
        ## ===== This feature is available only for verified or premium accounts. ===== ##
        member_ids_list = json.loads(str(line_bot_api.get_group_member_ids(event.source.group_id)))['memberIds']
        for member_user_id in member_ids_list:
            group_users_profile = line_bot_api.get_group_member_profile(event.source.group_id, member_user_id)
            print(group_users_profile)
            my_p_table.put_item(Item=json.loads(str(group_users_profile)))

    @handler.add(MemberJoinedEvent)
    def process_member_join_event(event):
        users_id_list = event.joined.members
        for users_id_d in users_id_list:
            users_id_i = json.loads(str(users_id_d))['userId']
            users_profile = line_bot_api.get_group_member_profile(event.source.group_id, users_id_i)
            my_p_table.put_item(Item=json.loads(str(users_profile)))       

    @handler.add(MemberLeftEvent)
    def process_member_left_event(event):
        users_id_list = event.left.members
        for users_id_d in users_id_list:
            users_id_i = json.loads(str(users_id_d))['userId']
            my_p_table.delete_item(Key={'userId': users_id_i})

    @handler.add(MessageEvent)
    def process_message(event, destination):
        message_event = {**json.loads(str(event)), **json.loads(str(event.source)), **json.loads(str(event.message))}

        def get_file_extension():
            '''only image, video, audio need to get file extension.'''
            return '.' + os.path.basename(line_bot_api.get_message_content(event.message.id).content_type)
        
        def save_file(file_path):
            message_content = line_bot_api.get_message_content(event.message.id)
            print(message_content.content_type)
            # with open(file_path, 'wb') as fd:
            #     for chunk in message_content.iter_content():
            #         fd.write(chunk)
                    
        if event.message.type in ['image', 'video', 'audio']:
            save_file(event.message.id + get_file_extension())
            print(get_file_extension())
        elif event.message.type == 'file':
            save_file(event.message.id + event.message.file_name)            
                    
        my_m_table.put_item(Item=message_event)
        
        reply_message = TextSendMessage(text='收到訊息~')
        line_bot_api.reply_message(event.reply_token, reply_message)
        
        group_users_profile = line_bot_api.get_group_member_profile(event.source.group_id, event.source.user_id)
        my_p_table.put_item(Item=json.loads(str(group_users_profile)))


    ## ===== handle webhook body ===== ## 
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {'statusCode': 400, 'body': 'Invalid signature. Please check your channel access token/channel secret.'}
    return {'statusCode': 200, 'body': 'OK'}