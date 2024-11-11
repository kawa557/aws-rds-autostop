# AWS Lambda RDS Shutdown

このプロジェクトは、AWSのLambda関数を使用して、タグ `[shutdown:true]` が付与されたRDSを毎日指定の時間に停止するためのCloudFormationテンプレートとPythonコードです。

## 構成

- `template.yaml`
  - CloudFormationテンプレート。Lambda機能、IAMロール、イベントルールを定義し、スケジュールに基づいてLambdaを定期実行します。
  - ParametersのScheduleExpressionで指定したcron式に従ってRDSを停止します。
    - cronで指定する時間はUTCです。
    - 例えばJST20時を指定する場合は"cron(0 11 * * ? *)" となります。
- `rds_stop.py`
  - タグ `[shutdown:true]` が付与されたAuroraデータベースの停止を行うLambda関数のPythonコード。

## デプロイ手順

1. テンプレートファイルをパッケージ化する
```
aws cloudformation package \
  --template-file template.yaml \
  --s3-bucket ${artifacts保管用バケット名} \
  --output-template-file packaged-template.yaml
```
2. テンプレートを展開する ※日本時間20時に停止する場合
```
aws cloudformation deploy \
  --stack-name Autostop-RDS-stack \
  --template-file packaged-template.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides ScheduleExpression="cron(0 11 * * ? *)"
  ```