# AWS Lambda EC2 and RDS Shutdown

このプロジェクトは、AWSのLambda関数を使用して、タグ `[shutdown:true]` が付与されたAuroraデータベースを毎日日本時間の20時に停止するためのCloudFormationテンプレートとPythonコードを提供します。

## 構成

- `template.yaml`
  - CloudFormationテンプレート。Lambda機能、IAMロール、CloudWatchイベントルールを定義し、スケジュールに基づいてLambdaを定期実行します。
- `rds_stop.py`
  - タグ `[shutdown:true]` が付与されたAuroraデータベースの停止を行うLambda関数のPythonコード。

## 必須要件

- AWSアカウント
- AWS CLI
- Python
- boto3ライブラリ（AWS SDK for Python）

## デプロイ手順

1. aws cloudformation package \
  --template-file template.yaml \
  --s3-bucket cf-templates-1jcq9sx4g1nyh-ap-northeast-1 \
  --output-template-file packaged-template.yaml
2. テンプレートを展開する
aws cloudformation deploy --stack-name Autostop-RDS-stack --template-file packaged-template.yaml --capabilities CAPABILITY_NAMED_IAM
