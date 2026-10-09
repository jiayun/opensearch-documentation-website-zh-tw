---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: DocumentDB
parent: Sources
grand_parent: Pipelines
nav_order: 10
---

# DocumentDB 來源

`documentdb` 來源會從 [Amazon DocumentDB](https://aws.amazon.com/documentdb/) 集合讀取文件。
它可以從匯出資料讀取歷史資料，並透過 Amazon DocumentDB 的[變更串流](https://docs.aws.amazon.com/documentdb/latest/developerguide/change_streams.html)持續取得最新資料。

`documentdb` 來源會從 Amazon DocumentDB 讀取資料，並將該資料放入 [Amazon Simple Storage Service (Amazon S3)](https://aws.amazon.com/s3/) 儲存貯體。
接著，其他 OpenSearch Data Prepper 工作節點會從 S3 儲存貯體讀取資料以進行處理。

## 用法
下列範例管線使用 `documentdb` 來源：

```yaml
version: "2"
documentdb-pipeline:
  source:
    documentdb:
      host: "docdb-mycluster.cluster-random.us-west-2.docdb.amazonaws.com"
      port: 27017
      authentication:
        {% raw %}username: ${{aws_secrets:secret:username}}
        password: ${{aws_secrets:secret:password}}{% endraw %}
      aws:
        sts_role_arn: "arn:aws:iam::123456789012:role/MyRole"
      s3_bucket: my-bucket
      s3_region: us-west-2
      collections:
        - collection: my-collection
          export: true
          stream: true
      acknowledgments: true
```
{% include copy.html %}

## 組態

您可以使用下列選項來設定 `documentdb` 來源。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`host` | 是 | 字串  | Amazon DocumentDB 叢集的主機名稱。
`port` | 否 | 整數 | Amazon DocumentDB 叢集的連接埠號碼。預設為 `27017`。
`trust_store_file_path` | 否 | 字串 | 包含 Amazon DocumentDB 叢集公開憑證之信任存放區檔案的路徑。
`trust_store_password` | 否 | 字串 | `trust_store_file_path` 所指定信任存放區的密碼。
`authentication` | 是 | 驗證 | 驗證組態。如需更多資訊，請參閱[驗證](#authentication)章節。
`collections` | 是 | 清單 | 集合組態的清單。必須指定且只能指定一個集合。如需更多資訊，請參閱[集合](#collection)章節。
`s3_bucket` | 是 | 字串  | 用於處理來自 Amazon DocumentDB 事件的 S3 儲存貯體。
`s3_prefix` | 否 | 字串  | 選用的 Amazon S3 金鑰前置詞。預設沒有金鑰前置詞。
`s3_region` | 否 | 字串  | S3 儲存貯體所在的 AWS 區域。
`aws` | 是 | AWS | AWS 組態。如需更多資訊，請參閱 [`aws`](#aws) 章節。
`id_key` | 否 | 字串  | 指定此選項時，Amazon DocumentDB 的 `_id` 欄位會設定為 `id_key` 所指定的金鑰名稱。當您需要比儲存至接收器的 `ObjectId` 字串所提供更多資訊時，可以使用此選項。預設情況下，`_id` 不會包含在事件中。
`direct_connection` | 否 | 布林值  | 當設定為 `true` 時，MongoDB 驅動程式會直接連線至指定的 Amazon DocumentDB 伺服器，而不會探索並連線至整個副本集。預設為 `true`。
`read_preference` | 否 | 字串  | 決定如何從 Amazon DocumentDB 讀取。如需更多資訊，請參閱[讀取偏好模式](https://www.mongodb.com/docs/v3.6/reference/read-preference/#read-preference-modes)。預設為 `primaryPreferred`。
`disable_s3_read_for_leader` | 否 | 布林值  | 當設定為 `true` 時，目前的領導者節點不會從 Amazon S3 讀取，而只會讀取串流。預設為 `false`。
`partition_acknowledgment_timeout` | 否 | 持續時間  | 設定節點持有分區的時間長度。預設為 `2h`。
`acknowledgments` | 否 | 布林值  | 設定為 `true` 時，會在事件傳送至接收器後於來源上啟用[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。
`insecure` | 否 | 布林值 | 停用 TLS。預設為 `false`。請勿在正式環境中使用此值。
`ssl_insecure_disable_verification` | 否 | 布林值 | 停用 TLS 主機名稱驗證。預設為 `false`。請勿在正式環境中啟用此旗標。請改用 `trust_store_file_path` 來驗證主機名稱。

### `authentication`

下列參數可讓您為 Amazon DocumentDB 叢集設定 `authentication`。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`username` | 是 | 字串 | 向 Amazon DocumentDB 叢集進行驗證時要使用的使用者名稱。支援自動重新整理。
`password` | 是 | 字串 | 向 Amazon DocumentDB 叢集進行驗證時要使用的密碼。支援自動重新整理。

### `collection`

下列參數可讓您設定 `collection` 以從 Amazon DocumentDB 叢集讀取。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`collection` | 是 | 字串 | 集合的名稱。
`export` | 否 | 布林值 | 是否包含匯出或完整載入。預設為 `true`。
`stream` | 否 | 布林值 | 是否啟用串流。預設為 `true`。
`partition_count` | 否 | 整數 | 定義要在 Amazon S3 中建立的分區數量。預設為 `100`。
`export_batch_size` | 否 | 整數 | 預設為 `10,000`。
`stream_batch_size` | 否 | 整數 | 預設為 `1,000`。

## `aws`

下列參數可讓您設定對 Amazon DocumentDB 的存取。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`sts_role_arn` | 否 | 字串 | 對 Amazon Simple Queue Service (Amazon SQS) 與 Amazon S3 發出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，其會使用[標準 SDK 憑證行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`aws_sts_header_overrides` | 否 | 對應 | 接收器外掛程式擔任 AWS Identity and Access Management (IAM) 角色時所使用標頭覆寫的對應。
`sts_external_id` | 否 | 字串 | Data Prepper 擔任 STS 角色時所使用的外部 STS ID。請參閱 [STS AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html) API 參考文件中的 `ExternalID`。
