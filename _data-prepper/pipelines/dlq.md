---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "死信佇列"
parent: Pipelines
nav_order: 15
---

# 死信佇列

OpenSearch Data Prepper 管線支援死信佇列 (DLQ)，可將失敗的事件卸載，並使其可供分析。

自 Data Prepper 2.3 起，僅有 `s3` 來源支援 DLQ。

## 設定 DLQ 寫入器

若要為 `s3` 來源設定 DLQ 寫入器，請將以下內容新增至您的 `pipeline.yaml` 檔案：

```yaml
sink:
  - opensearch:
      hosts: ["https://opensearch:9200"]
      index: my-index
      username: admin
      password: admin-password
      insecure: true

      dlq:
        s3:
          bucket: my-dlq-bucket
          key_path_prefix: dlq-files/
          region: us-west-2
          sts_role_arn: arn:aws:iam::123456789012:role/dlq-role
          bucket_owner: 123456789012
```

產生的 DLQ 檔案會以 DLQ 物件的 JSON 陣列形式輸出。任何寫入 `s3` DLQ 的檔案都包含下列名稱模式：

```
dlq-v${version}-${pipelineName}-${pluginId}-${timestampIso8601}-${uniqueId}
```

名稱模式中的下列資訊會被取代：

- `version`：Data Prepper 版本。
- `pipelineName`：`pipelines.yaml` 中所指出的管線名稱。
- `pluginId`：與 DLQ 事件相關聯的外掛程式 ID。

## 組態

DLQ 支援下列組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`bucket` | 是 | 字串 | DLQ 將失敗記錄輸出至其中的儲存貯體名稱。
`key_path_prefix` | 否 | 字串 | Amazon Simple Storage Service (Amazon S3) 儲存貯體中使用的 `key_prefix`。預設為 `""`。支援時間值模式變數，例如 `/%{yyyy}/%{MM}/%{dd}`，包括 [Java DateTimeFormatter](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html) 中列出的任何變數。例如，使用 `/%{yyyy}/%{MM}/%{dd}` 模式時，您可以將 `key_prefix` 設為 `/2023/01/24`。
`region` | 否 | 字串 | S3 儲存貯體的 AWS 區域。預設為 `us-east-1`。
`sts_role_arn` | 否 | 字串 | DLQ 為了寫入 AWS S3 儲存貯體而擔任的 STS 角色。預設為 `null`，其使用標準 SDK 的憑證行為。若要使用此選項，S3 儲存貯體必須已設定 `s3:PutObject` 權限。
`bucket_owner` | 否 | 字串 | S3 儲存貯體擁有者的 AWS 帳戶 ID。設定後，Data Prepper 會將此值以 `expectedBucketOwner` 傳遞至 S3，若與實際的儲存貯體擁有者不符，S3 會拒絕寫入。預設為 `null`，其不會執行明確的儲存貯體擁有者檢查。

將 DLQ 與 OpenSearch 輸出端搭配使用時，您可以設定 [`max_retries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/#configure-max_retries) 選項，在輸出端達到重試次數上限後，將失敗的記錄傳送至 DLQ。

## 指標

DLQ 支援下列指標。

### 計數器

- `dlqS3RecordsSuccess`：衡量成功傳送至 S3 的記錄數。
- `dlqS3RecordsFailed`：衡量傳送至 S3 失敗的記錄數。
- `dlqS3RequestSuccess`：衡量成功的 S3 請求數。
- `dlqS3RequestFailed`：衡量失敗的 S3 請求數。

### 分佈摘要

- `dlqS3RequestSizeBytes`：衡量 S3 請求承載大小的分佈，以位元組為單位。

### 計時器

- `dlqS3RequestLatency`：衡量傳送每個 S3 請求時的延遲，包括重試。

## DLQ 物件

DLQ 支援下列 DLQ 物件：

- `pluginId`：傳送至 DLQ 的事件所源自的外掛程式 ID。
- `pluginName`：外掛程式的名稱。
- `failedData`：包含失敗物件及其選項的物件。此物件為每個外掛程式所獨有。
- `pipelineName`：事件失敗時所在的 Data Prepper 管線名稱。
- `timestamp`：失敗的時間戳記，格式為 `ISO8601`。
