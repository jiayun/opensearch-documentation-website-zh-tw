---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "死信佇列"
parent: Pipelines
nav_order: 15
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/dlq/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/dlq/
---

# 死信佇列

OpenSearch Data Prepper 管線支援死信佇列 (DLQ)，可用來卸載處理失敗的事件，並讓這些事件可供分析。

若要使用 DLQ，請在支援此功能的外掛程式中設定 `dlq` 設定，例如 `opensearch` 接收器 (sink)。

## 設定 DLQ 寫入器

若要為 `opensearch` 接收器 (sink) 設定 DLQ 寫入器，請將以下內容新增至您的 `pipeline.yaml` 檔案：

```yaml
sink:
  - opensearch:
      hosts: ["https://opensearch:9200"]
      index: my-index
      username: admin
      password: "<custom-admin-password>"
      insecure: true

      dlq:
        s3:
          bucket: my-dlq-bucket
          key_path_prefix: dlq-files/
          region: us-west-2
          sts_role_arn: arn:aws:iam::123456789012:role/dlq-role
          bucket_owner: 123456789012
```

根據預設，每個 DLQ 檔案都包含一個 JSON 物件，其中的 `dlqObjects` 陣列存放 DLQ 物件。當 `codec` 為 `ndjson` 時，每個 DLQ 檔案每行包含一個 DLQ 物件。寫入 `s3` DLQ 的任何檔案都採用以下名稱模式：

```
dlq-v${version}-${pipelineName}-${pluginId}-${timestampIso8601}-${uniqueId}.${extension}
```

名稱模式中的以下資訊會被取代：

- `version`：Data Prepper 版本。
- `pipelineName`：`pipelines.yaml` 中指定的管線名稱。
- `pluginId`：與 DLQ 事件相關聯的外掛程式 ID。
- `extension`：`codec` 選項的值，為 `json` 或 `ndjson`。

## 組態

DLQ 支援下列組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`bucket` | 是 | 字串 | DLQ 輸出失敗記錄的目的地儲存貯體名稱。
`key_path_prefix` | 否 | 字串 | 在 Amazon Simple Storage Service (Amazon S3) 儲存貯體中使用的 `key_prefix`。預設為 `""`。支援時間值模式變數，例如 `/%{yyyy}/%{MM}/%{dd}`，包括 [Java DateTimeFormatter](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html) 中列出的任何變數。例如，使用 `/%{yyyy}/%{MM}/%{dd}` 模式時，您可以將 `key_prefix` 設定為 `/2023/01/24`。
`region` | 否 | 字串 | S3 儲存貯體所在的 AWS 區域。預設為 `us-east-1`。
`sts_role_arn` | 否 | 字串 | DLQ 為了寫入 AWS S3 儲存貯體而擔任的 STS 角色。預設為 `null`，即採用標準 SDK 的認證資訊行為。若要使用此選項，S3 儲存貯體必須已設定 `s3:PutObject` 權限。
`sts_external_id` | 否 | 字串 | 擔任 STS 角色時使用的外部 ID。長度必須介於 2 到 1,224 個字元之間。
`sts_header_overrides` | 否 | Map | 要新增至 AWS STS `AssumeRole` 請求的標頭對應表。
`force_path_style` | 否 | 布林值 | 為 `true` 時，DLQ 會使用路徑樣式 URL（`https://s3.<region>.amazonaws.com/<bucket>/<key>`）而非虛擬主機樣式 URL 來定址 S3 儲存貯體。預設為 `false`。
`legacy_md5_checksum` | 否 | 布林值 | 為 `true` 時，DLQ 會在每個請求中傳送 `Content-MD5` 標頭，且僅在 S3 操作需要時才計算總和檢查碼。若 S3 相容儲存空間不支援較新的 AWS SDK 總和檢查碼演算法，請使用此設定。預設為 `false`。
`bucket_owner` | 否 | 字串 | S3 儲存貯體擁有者的 AWS 帳戶 ID。設定此選項後，Data Prepper 會將此值以 `expectedBucketOwner` 傳遞給 S3；若此值與實際的儲存貯體擁有者不符，S3 會拒絕寫入。預設為 `null`，即不執行明確的儲存貯體擁有者檢查。
`codec` | 否 | 字串 | DLQ 檔案的格式。有效值為 `json` 和 `ndjson`。為 `json` 時，每個檔案包含一個 JSON 物件，其中的 `dlqObjects` 陣列保存該批次中的所有 DLQ 物件。為 `ndjson` 時，每個檔案每行包含一個 DLQ 物件，並使用 `.ndjson` 副檔名。預設為 `json`。

將 DLQ 與 OpenSearch 接收器 (sink) 搭配使用時，您可以設定 [`max_retries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/#configure-max_retries) 選項，在接收器達到重試次數上限後，將失敗的記錄傳送至 DLQ。

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
