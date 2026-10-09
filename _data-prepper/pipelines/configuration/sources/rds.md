---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: RDS
parent: Sources
grand_parent: Pipelines
nav_order: 95
---

# RDS 來源

`rds` 來源可在 [Amazon Relational Database Service (Amazon RDS)](https://aws.amazon.com/rds/) 和 [Amazon Aurora](https://aws.amazon.com/aurora/) 資料庫上啟用變更資料擷取（CDC）。它可使用資料庫複寫記錄檔接收資料庫事件，例如 `INSERT`、`UPDATE` 或 `DELETE`，並支援透過將 RDS 資料匯出至 Amazon Simple Storage Service (Amazon S3) 進行初始載入。

此來源支援下列資料庫引擎：
- Aurora MySQL 和 Aurora PostgreSQL
- RDS MySQL 和 RDS PostgreSQL

此來源提供兩種匯入選項，用於從 Aurora/RDS 匯入資料：

1. 匯出：從 Aurora/RDS 完整匯出初始資料至 S3，以初始載入 Aurora/RDS 資料庫的目前狀態。
2. 串流：從資料庫複寫記錄檔（MySQL `binlog` 或 PostgreSQL WAL）串流傳輸事件。 

## 使用方式

下列管線範例指定了 `rds` 來源。它會從 Aurora MySQL 叢集匯入資料：

```yaml
version: "2"
rds-pipeline:
  source:
    rds:
      db_identifier: "my-rds-instance"
      engine: "aurora-mysql"
      database: "mydb"
      authentication:
        username: "myuser"
        password: "mypassword"
      s3_bucket: "my-export-bucket"
      s3_region: "us-west-2"
      s3_prefix: "rds-exports"
      export:
        kms_key_id: "arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012"
        export_role_arn: "arn:aws:iam::123456789012:role/rds-export-role"
      stream: true
      aws:
        region: "us-west-2"
        sts_role_arn: "arn:aws:iam::123456789012:role/my-pipeline-role"
```

## 組態選項

下列表格說明 `rds` 來源的組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`db_identifier` | 是 | 字串 | RDS 執行個體或 Aurora 叢集的識別碼。
`cluster` | 否 | 布林值 | `db_identifier` 是指叢集（`true`）還是執行個體（`false`）。預設為 `false`。對於 Aurora 引擎，此選項一律為 `true`。
`engine` | 是 | 字串 | 資料庫引擎類型。必須是 `mysql`、`postgresql`、`aurora-mysql` 或 `aurora-postgresql` 其中之一。
`database` | 是 | 字串 | 要連線的資料庫名稱。
`tables` | 否 | 物件 | 用於指定要包含或排除哪些資料表的組態。如需詳細資訊，請參閱 [tables](#tables)。
`authentication` | 是 | 物件 | 資料庫驗證憑證。如需詳細資訊，請參閱 [authentication](#authentication)。
`aws` | 是 | 物件 | AWS 組態。如需詳細資訊，請參閱 [`aws`](#aws)。
`acknowledgments` | 否 | 布林值 | 設為 `true` 時，允許來源在 OpenSearch 接收端收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。預設為 `true`。
`s3_data_file_acknowledgment_timeout` | 否 | 時間長度 | 搭配確認機制使用時，從 RDS 匯出讀取的資料到期前所經過的時間。預設為 30 分鐘。
`stream_acknowledgment_timeout` | 否 | 時間長度 | 搭配確認機制使用時，從資料庫串流讀取的資料到期前所經過的時間。預設為 10 分鐘。
`s3_bucket` | 是 | 字串 | 用於儲存 RDS 匯出資料的 S3 儲存貯體名稱。
`s3_prefix` | 否 | 字串 | 匯出儲存貯體中 S3 物件的前綴。
`s3_region` | 否 | 字串 | S3 儲存貯體的 AWS 區域。若未指定，則使用與 [`aws`](#aws) 組態中指定的相同區域。
`partition_count` | 否 | 整數 | S3 緩衝區中的資料夾分割區數量。必須介於 1 到 1,000 之間。預設為 100。
`export` | 否 | 物件 | RDS 匯出作業的組態。如需詳細資訊，請參閱 [export](#export-options)。
`stream` | 否 | 布林值 | 是否啟用資料庫變更事件的串流傳輸。預設為 `false`。
`tls` | 否 | 物件 | 資料庫連線的 TLS 組態。如需詳細資訊，請參閱 [`tls`](#tls-options)。
`disable_s3_read_for_leader` | 否 | 布林值 | 是否停用領導節點的 S3 讀取作業。預設為 `false`。

<!-- vale off -->
### aws
<!-- vale on -->

在 AWS 組態中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 憑證使用的 AWS 區域。預設採用[判定區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon RDS 和 Amazon S3 發出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，這會使用[處理憑證的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_external_id` | 否 | 字串 | 擔任 STS 角色時使用的外部 ID。長度必須介於 2 到 1,224 個字元之間。
`sts_header_overrides` | 否 | 對應表 | AWS Identity and Access Management (IAM) 角色為來源外掛程式採用的標頭覆寫對應表。最多 5 個標頭。

<!-- vale off -->
### authentication
<!-- vale on -->

使用下列選項進行資料庫驗證。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`username` | 是 | 字串 | 用於驗證的資料庫使用者名稱。
`password` | 是 | 字串 | 用於驗證的資料庫密碼。

<!-- vale off -->
### tables
<!-- vale on -->

使用下列選項指定資料擷取要包含哪些資料表。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`include` | 否 | 清單 | 資料擷取要包含的資料表名稱清單。最多 1,000 個資料表。若有指定，則只會處理這些資料表。
`exclude` | 否 | 清單 | 資料擷取要排除的資料表名稱清單。最多 1,000 個資料表。即使這些資料表符合包含模式，也會予以忽略。

<!-- vale off -->
### 匯出選項
<!-- vale on -->

下列選項可讓您自訂 RDS 匯出功能。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`kms_key_id` | 是 | 字串 | 用於加密匯出資料的 AWS Key Management Service (AWS KMS) 金鑰 ID 或 Amazon Resource Name (ARN)。
`export_role_arn` | 是 | 字串 | RDS 為執行匯出作業而擔任的 IAM 角色之 ARN。

<!-- vale off -->
### TLS 選項
<!-- vale on -->

下列選項可讓您設定資料庫連線的 TLS。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`insecure` | 否 | 布林值 | 是否停用資料庫連線的 TLS 加密。預設為 `false`（已啟用 TLS）。

## 提供的中繼資料屬性

下列中繼資料會新增至 `rds` 來源處理的每個事件。您可使用[運算式語法的 `getMetadata` 函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-metadata/)存取這些中繼資料屬性。

* `primary_key`: 資料庫記錄的主索引鍵。對於具有複合主索引鍵的資料表，各值會以 `|` 分隔符號串接。
* `event_timestamp`: 資料庫變更發生時的時間戳記，以紀元毫秒表示。對於匯出事件，這代表匯出時間。對於串流事件，這代表交易認可時間。
* `document_version`: 從事件時間戳記產生的長整數，用作文件版本。 
* `opensearch_action`: 用於將事件傳送至 OpenSearch 的大量操作，例如 `index` 或 `delete`。
* `change_event_type`: 串流事件類型。可以是 `insert`、`update` 或 `delete`。
* `table_name`: 事件來源資料庫資料表的名稱。
* `schema_name`: 事件來源結構描述的名稱。對於 MySQL，`schema_name` 與 `database_name` 相同。
* `database_name`: 事件來源資料庫的名稱。
* `ingestion_type`: 指出事件來自匯出或串流。有效值為 `EXPORT` 和 `STREAM`。
* `s3_partition_key`: 事件會在處理前儲存在 S3 暫存用儲存貯體中。此中繼資料指出事件在處理前儲存於 S3 儲存貯體中的位置。

## 權限

以下是將 RDS 作為來源執行時所需的權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "allowReadingFromS3Buckets",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:GetBucketLocation",
        "s3:ListBucket",
        "s3:PutObject"
      ],
      "Resource": [
        "arn:aws:s3:::s3_bucket",
        "arn:aws:s3:::s3_bucket/*"
      ]
    },
    {
      "Sid": "AllowDescribeInstances",
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBInstances"
      ],
      "Resource": [
        "arn:aws:rds:region:account-id:db:*"
      ]
    },
    {
      "Sid": "AllowDescribeClusters",
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBClusters"
      ],
      "Resource": [
        "arn:aws:rds:region:account-id:cluster:*"
      ]
    },
    {
      "Sid": "AllowSnapshots",
      "Effect": "Allow",
      "Action": [
        "rds:DescribeDBClusterSnapshots",
        "rds:CreateDBClusterSnapshot",
        "rds:DescribeDBSnapshots",
        "rds:CreateDBSnapshot",
        "rds:AddTagsToResource"
      ],
      "Resource": [
        "arn:aws:rds:region:account-id:cluster:*",
        "arn:aws:rds:region:account-id:cluster-snapshot:*",
        "arn:aws:rds:region:account-id:db:*",
        "arn:aws:rds:region:account-id:snapshot:*"
      ]
    },
    {
      "Sid": "AllowExport",
      "Effect": "Allow",
      "Action": [
        "rds:StartExportTask"
      ],
      "Resource": [
        "arn:aws:rds:region:account-id:cluster:*",
        "arn:aws:rds:region:account-id:cluster-snapshot:*",
        "arn:aws:rds:region:account-id:snapshot:*"
      ]
    },
    {
      "Sid": "AllowDescribeExports",
      "Effect": "Allow",
      "Action": [
        "rds:DescribeExportTasks"
      ],
      "Resource": "*"
    },
    {
      "Sid": "AllowAccessToKmsForExport",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:Encrypt",
        "kms:DescribeKey",
        "kms:RetireGrant",
        "kms:CreateGrant",
        "kms:ReEncrypt*",
        "kms:GenerateDataKey*"
      ],
      "Resource": [
        "arn:aws:kms:region:account-id:key/export-key-id"
      ]
      },
    {
      "Sid": "AllowPassingExportRole",
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": [
        "arn:aws:iam::account-id:role/export-role"
      ]
    }
  ]
}
```

## 指標

`rds` 來源包含下列指標：

* `exportJobSuccess`：已成功的 RDS 匯出任務數。
* `exportJobFailure`：已失敗的 RDS 匯出任務數。
* `exportS3ObjectsTotal`：在 S3 中找到的匯出資料檔案總數。
* `exportS3ObjectsProcessed`：已從 S3 成功處理的匯出資料檔案總數。
* `exportS3ObjectsErrors`：從 S3 處理失敗的匯出資料檔案總數。
* `exportRecordsTotal`：在匯出中找到的記錄總數。
* `exportRecordsProcessed`：已成功處理的匯出記錄總數。
* `exportRecordsProcessingErrors`：匯出記錄處理錯誤數。
* `changeEventsProcessed`：從資料庫串流處理的變更事件數。
* `changeEventsProcessingErrors`：來自資料庫串流的變更事件處理錯誤數。
* `bytesReceived`：來源接收的位元組總數。
* `bytesProcessed`：來源處理的位元組總數。
* `positiveAcknowledgementSets`：串流處理中正面確認的確認集數。
* `negativeAcknowledgementSets`：串流處理中負面確認的確認集數。
* `checkpointCount`：串流處理中的檢查點總數。
* `noDataExtendLeaseCount`：在自上次檢查點後未處理新資料的分割區上延長租約的次數。
* `giveupPartitionCount`：放棄分割區的次數。
* `replicationLogEntryProcessingTime`：處理複寫記錄事件所花費的時間。
* `replicationLogEntryProcessingErrors`：處理失敗的複寫記錄事件數。
