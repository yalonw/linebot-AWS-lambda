###### Date: 2020.09

# LineBot + AWS Lambda
### 開發目標
- 利用 LineBot 自動儲存所有 Line 對話訊息，以及儲存使用者資訊，
  並佈署至 AWS Lambda & DynamoDB
- Use AWS Lambda to build a serverless service backend for LINEBot server,
  and then store user messages in DynamoDB

### 開發環境
- 雲服務 Cloud Service : AWS ( Amazon Web Services )
- 伺服器 Server : [AWS Lambda](https://aws.amazon.com/tw/lambda/)
- 資料庫 Database : [Amazon DynamoDB](https://aws.amazon.com/tw/dynamodb/)
- 儲存空間 Storage : [Amazon Simple Storage Service ( Amazon S3 )](https://aws.amazon.com/tw/s3)
- 其他輔助功能：Layers、API Gateway、IAM

### 程式碼
> 此版本並無儲存多媒體檔案（如照片、影片、音檔、文件等），故無使用 Amazon S3
- Lambda Function source code ： (╭☞ ･ω･)╭☞ [傳送門](./auto-record/lambda_function.py)

### 參考資料
- [Serverless Service Backend with AWS Lambda, API Gateway, DynamoDB](https://aws.amazon.com/getting-started/hands-on/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/module-3/?nc1=h_ls)
- [DynamoDB | Create, Read, Update, and Delete an Item with Python](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.03.html)

