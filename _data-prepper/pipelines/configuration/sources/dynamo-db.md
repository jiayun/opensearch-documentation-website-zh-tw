---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: DynamoDB
parent: Sources
grand_parent: Pipelines
nav_order: 20
---

# DynamoDB 來源

`dynamodb` 來源可在 [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) 資料表上啟用異動資料擷取 (CDC)。它可以使用 DynamoDB 串流接收資料表事件，例如 `create`、`update` 或 `delete`，並支援使用[時間點復原 (PITR)](https://aws.amazon.com/dynamodb/pitr/) 的初始快照。

此來源包含兩個用於串流 DynamoDB 事件的匯入選項：

1. 使用 [PITR](https://aws.amazon.com/dynamodb/pitr/) 的_完整初始快照_會取得 DynamoDB 資料表目前狀態的初始快照。這需要在您的 DynamoDB 資料表上啟用 PITR Snapshots 與 DynamoDB 選項。
2.  從 DynamoDB 串流串流事件，而不進行完整初始快照。如果您已在管線中具備快照機制，這會很實用。這需要在 DynamoDB 資料表上啟用 DynamoDB 串流選項。

## 使用方式

下列範例管線將 DynamoDB 指定為來源。它會透過 PITR 快照，從名為 `table-a` 的 DynamoDB 資料表匯入資料。它也會指出 `start_position`，以告知管線如何讀取 DynamoDB 串流事件：

```yaml
version: "2"
cdc-pipeline:
  source:
    dynamodb:
      tables:
        - table_arn: "arn:aws:dynamodb:us-west-2:123456789012:table/table-a"
          export:
            s3_bucket: "test-bucket"
            s3_prefix: "myprefix"
          stream:
            start_position: "LATEST" # Read latest data from streams (Default)
            view_on_remove: NEW_IMAGE
      aws:
        region: "us-west-2"
        sts_role_arn: "arn:aws:iam::123456789012:role/my-iam-role"
```

## 組態選項

下列表格說明 `dynamodb` 來源的組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`aws` | 是 | AWS | AWS 組態。如需更多資訊，請參閱[`aws`](#aws)。
`acknowledgments` | 否 | 布林值  | 當 `true` 時，啟用 `s3` 來源，以便在 OpenSearch 接收器收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。
`shared_acknowledgement_timeout` | 否 | 持續時間 | 搭配確認使用時，從 DynamoDB 串流讀取的資料到期前所經過的時間量。預設為 10 分鐘。
`s3_data_file_acknowledgment_timeout` | 否 | 持續時間 | 搭配確認使用時，從 DynamoDB 匯出讀取的資料到期前所經過的時間量。預設為 5 分鐘。
`tables` | 是 | 清單 | DynamoDB 資料表的組態。如需更多資訊，請參閱[tables](#tables)。

<!-- vale off -->
### aws
<!-- vale on -->

在 AWS 組態中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於憑證的 AWS Region。預設為[決定 Region 的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon Simple Queue Service (Amazon SQS) 與 Amazon Simple Storage Service (Amazon S3) 的請求所要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，其將使用[憑證的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`aws_sts_header_overrides` | 否 | 對應表 | 接收器外掛程式擔任 AWS Identity and Access Management (IAM) 角色時使用的標頭覆寫對應。


<!-- vale off -->
### tables
<!-- vale on -->

搭配 `tables` 組態使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`table_arn` | 是 | 字串 | 來源 DynamoDB 資料表的 Amazon Resource Name (ARN)。
`export` | 否 | 匯出 | 決定如何匯出 DynamoDB 事件。如需更多資訊，請參閱[export](#export-options)。
`stream` | 否 | 串流 | 決定管線如何從 DynamoDB 資料表讀取資料。如需更多資訊，請參閱[stream](#stream-option)。

#### 匯出選項

下列選項可讓您自訂 DynamoDB 事件的匯出目的地。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`s3_bucket` | 是 | 字串 | 儲存匯出資料檔案的目的地儲存貯體。
`s3_prefix` | 否 | 字串 | S3 儲存貯體的自訂前置詞。
`s3_sse_kms_key_id` | 否 | 字串 |  用於加密匯出資料檔案的 AWS Key Management Service (AWS KMS) 金鑰。`key_id` 是 KMS 金鑰的 ARN，例如 `arn:aws:kms:us-west-2:123456789012:key/0a4bc22f-bb96-4ad4-80ca-63b12b3ec147`。
`s3_region` | 否 | 字串 | S3 儲存貯體的 Region。

#### 串流選項

下列選項可讓您自訂管線如何從 DynamoDB 資料表讀取事件。

選項 | 必要 | 類型   | 說明
:--- | :--- | :--- | :---
`start_position` | 否 | 字串 | 啟用 DynamoDB 串流選項時，來源開始讀取串流事件的位置。`LATEST` 會從最新的串流記錄開始讀取事件。 
`view_on_remove` | 否 | 列舉 | 用於 DynamoDB 串流中 REMOVE 事件的[串流記錄檢視](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)。必須是 `NEW_IMAGE` 或 `OLD_IMAGE`。預設為 `NEW_IMAGE`。如果使用 `OLD_IMAGE` 選項且找不到舊映像，來源會尋找 `NEW_IMAGE`。

## 公開的中繼資料屬性

下列中繼資料將新增至 `dynamodb` 來源所處理的每個事件。這些中繼資料屬性可使用[運算式語法 `getMetadata` 函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-metadata/)存取。

* `primary_key`：DynamoDB 項目的主索引鍵。對於僅包含分割區索引鍵的資料表，此值會提供分割區索引鍵。對於同時包含分割區索引鍵與排序索引鍵的資料表，`primary_key` 屬性將等於分割區索引鍵與排序索引鍵，並以 `|` 分隔，例如 `partition_key|sort_key`。
* `partition_key`：DynamoDB 項目的分割區索引鍵。
* `sort_key`：DynamoDB 項目的排序索引鍵。如果資料表不包含排序索引鍵，這會是 null。
* `dynamodb_timestamp`：DynamoDB 項目的時間戳記。對於匯出項目，這會是匯出時間；對於串流項目，這會是 DynamoDB 串流事件時間。接收器會使用此時間戳記，為 DynamoDB 串流事件發出 `EndtoEndLatency` 指標，以追蹤 DynamoDB 資料表中發生變更與該變更套用至接收器之間的延遲。
* `document_version`：使用 `dynamodb_timestamp` 調整同一秒內收到的串流項目在時間戳記相同時的排序判定。建議搭配 `opensearch` 接收器的 `document_version` 設定使用。
* `opensearch_action`：將 DynamoDB 事件動作對應至 OpenSearch 動作的預設值。對於匯出項目，此動作會是 `index`；對於串流事件，則會是 `INSERT` 或 `MODIFY`；而當 OpenSearch 動作為 `delete` 時，則為 `REMOVE` 串流事件。
* `dynamodb_event_name`：項目的確切事件類型。對於匯出項目會是 `null`，對於串流事件則會是 `INSERT`、`MODIFY` 或 `REMOVE`。
* `table_name`：事件來源的 DynamoDB 資料表名稱。
* `ttl_delete`：一個布林值，指出 `REMOVE` 事件是否由 DynamoDB Time-To-Live (TTL) 觸發。對於以 TTL 為基礎的刪除，`ttl_delete` 屬性為 `true`；對於所有其他事件則為 `false`。此中繼資料可搭配條件式路由或篩選使用，以不同於手動刪除的方式處理 TTL 刪除。


## 權限

下列是將 DynamoDB 作為來源執行所需的最低權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
      {
        "Sid": "allowDescribeTable",
        "Effect": "Allow",
        "Action": [
          "dynamodb:DescribeTable"
        ],
        "Resource": [
          "arn:aws:dynamodb:us-east-1:{account-id}:table/my-table"
        ]
      },
       {
            "Sid": "allowRunExportJob",
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeContinuousBackups",
                "dynamodb:ExportTableToPointInTime"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:{account-id}:table/my-table"
            ]
        },
        {
            "Sid": "allowCheckExportjob",
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeExport"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:{account-id}:table/my-table/export/*"
            ]
        },
        {
            "Sid": "allowReadFromStream",
            "Effect": "Allow",
            "Action": [
                "dynamodb:DescribeStream",
                "dynamodb:GetRecords",
                "dynamodb:GetShardIterator"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-east-1:{account-id}:table/my-table/stream/*"
            ]
        },
        {
            "Sid": "allowReadAndWriteToS3ForExport",
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:AbortMultipartUpload",
                "s3:PutObject",
                "s3:PutObjectAcl"
            ],
            "Resource": [
                "arn:aws:s3:::my-bucket/*"
            ]
        }
    ]
}
```

執行匯出時，不需要 `"Sid": "allowReadFromStream"` 區段。如果僅從 DynamoDB 串流讀取，則不需要 
`"Sid": "allowReadAndWriteToS3ForExport"`、`"Sid": "allowCheckExportjob"` 與 ` "Sid": "allowRunExportJob"` 區段。

## 限制

請注意下列限制：

* 每個 Data Prepper 執行個體最多可平行處理 150 個 DynamoDB 串流分片。為避免高延遲與資料遺失，請將 Data Prepper 執行個體數目設為開啟分片數上限除以 150（無條件進位至最接近的整數）。

## 指標

`dynamodb` 來源包含下列指標。

### 計數器

* `exportJobSuccess`：已成功提交的匯出工作數目。
* `exportJobFailure`：已失敗的匯出工作提交嘗試次數。
* `exportS3ObjectsTotal`：在 S3 中找到的匯出資料檔案總數。
* `exportS3ObjectsProcessed`：已從 S3 成功處理的匯出資料檔案總數。
* `exportRecordsTotal`：匯出中找到的記錄總數。
* `exportRecordsProcessed`：已成功處理的匯出記錄總數。
* `exportRecordsProcessingErrors`：匯出記錄處理錯誤數目。
* `changeEventsProcessed`：從 DynamoDB 串流處理的變更事件數目。
* `changeEventsProcessingErrors`：DynamoDB 串流變更事件的處理錯誤數目。
* `shardProgress`：正確讀取 DynamoDB 串流時遞增的分片進度。若此值在相當長的一段時間內為`0`，表示啟用串流的管線發生問題。

### 計量

`dynamodb` 來源包含下列計量：

* `totalOpenShards`：DynamoDB 串流中開啟的分片數目。開啟的分片是指未獲指派 `EndingSequenceNumber` 的分片。
* `activeShardsInProcessing`：Data Prepper 目前正在處理的分片數目。


