---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Kinesis
parent: Sources
grand_parent: Pipelines
nav_order: 45
---

# Kinesis 來源

您可以使用 OpenSearch Data Prepper `kinesis` 來源，從一或多個 [Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/) 匯入記錄。

## 使用方式

下列範例管線將 Kinesis 指定為來源。此管線會從名為 `stream1` 和 `stream2` 的多個 Kinesis 資料串流匯入資料，並設定 `initial_position` 以指出讀取串流記錄的起始點：

```yaml
version: "2"
kinesis-pipeline:
  source:
    kinesis:
      streams:
        - stream_name: "stream1"
          initial_position: "LATEST"
        - stream_name: "stream2"
          initial_position: "LATEST"
      aws:
        region: "us-west-2"
        sts_role_arn: "arn:aws:iam::123456789012:role/my-iam-role"
```

## 組態選項

`kinesis` 來源支援下列組態選項。

選項 | 必要 | 類型     | 說明
:--- |:---------|:---------| :---
`aws` | 是      | AWS      | 指定 AWS 組態。請參閱 [`aws`](#aws)。
`acknowledgments` | 否       | 布林值  | 設為 `true` 時，可讓 `kinesis` 來源在 OpenSearch 接收器 (sink) 收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。預設為 `false`。
`streams` | 是      | 清單     | 設定 `kinesis` 來源用於讀取記錄的多個 Kinesis 資料串流清單。您最多可設定四個串流。請參閱[串流](#streams)。
`codec` | 是      | Codec    | 指定要套用的[編解碼器 (codec)](#codec)。
`buffer_timeout` | 否       | 持續時間 | 設定在逾時之前，允許將事件寫入 Data Prepper 緩衝區的時間長度。來源在指定時間內無法寫入緩衝區的任何事件都會遭到捨棄。預設為 `1s`。
`records_to_accumulate` | 否       | 整數  | 決定寫入緩衝區之前要累積的訊息數量。預設為 `100`。
`consumer_strategy` | 否       | 字串   | 選取用於匯入 Kinesis 資料串流的取用者策略。預設為 `fan-out`，但也可以使用 `polling`。如果啟用 `polling`，則需要額外的組態。
`polling` | 否       | polling   | 請參閱 [polling](#polling)。
`max_initialization_attempts` | 否 | 整數 | 來源停止重試之前，初始化 Kinesis 取用者的最大嘗試次數。預設為 `2147483647`。
`initialization_backoff_time` | 否 | 持續時間 | 每次嘗試初始化 Kinesis 取用者之間的等待時間。預設為 `1s`。

### 串流

您可以在 `streams` 陣列中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- |:---------| :--- | :---
`stream_name` | 否       | 字串 | 定義每個 Kinesis 資料串流的名稱。必須指定 `stream_name` 或 `stream_arn` 其中之一。
`stream_arn` | 否 | 字串 | Kinesis 資料串流的 Amazon Resource Name (ARN)。若同時指定 `stream_name` 與 `stream_arn`，則會使用 `stream_arn`。
`consumer_arn` | 否 | 字串 | 該串流要使用的增強型扇出 (enhanced fan-out) 消費者 ARN。僅在指定 `stream_arn` 且 `consumer_strategy` 為 `fan-out` 時適用。若未指定，來源會使用以管線名稱命名的串流消費者。
`initial_position` | 否       | 字串 | 設定 `initial_position`，以控制 `kinesis` 來源從何處開始讀取串流記錄。使用 `LATEST` 從最新的記錄開始讀取，使用 `EARLIEST` 從串流開頭讀取，或使用 `AT_TIMESTAMP` 從特定時間戳記開始讀取。預設為 `LATEST`。
`initial_timestamp`| 否       | 字串 | 指定開始讀取串流記錄的時間戳記。此值必須遵循 [ISO LocalDateTime](https://docs.oracle.com/javase/8/docs/api/java/time/format/DateTimeFormatter.html#ISO_LOCAL_DATE_TIME) 格式，並以 UTC 時區提供（例如 `2023-01-23T10:00:00`）。當 `initial_position` 設為 `AT_TIMESTAMP` 時，您必須指定 `initial_timestamp` 或 `range`。
`range` | 否  | 字串 | 指定從目前時間往前回溯多久，開始讀取 Kinesis 資料串流記錄。支援 ISO-8601 持續時間字串（例如 `PT20.345S` 或 `PT15M`），以及秒（`60s`）與毫秒（`1600ms`）的簡寫表示法。例如，`PT12H` 會從管線啟動前 12 小時的記錄開始讀取。當 `initial_position` 設為 `AT_TIMESTAMP` 時，您必須指定 `initial_timestamp` 或 `range`。

`checkpoint_interval` | 否       | 持續時間 | 設定 `checkpoint_interval`，以定期為 Kinesis 資料串流建立檢查點，避免重複處理記錄。預設為 `PT2M`。
`compression` | 否 | 字串  | 指定壓縮格式。若要解壓縮由 [CloudWatch Logs 訂閱篩選器](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SubscriptionFilters.html) 新增至 Kinesis 的記錄，請使用 `gzip` 壓縮格式。

<!-- vale off -->
## codec
<!-- vale on -->

`codec` 會決定 `kinesis` 來源如何剖析每個 Kinesis 串流記錄。為了提升效能並提高效率，您可以搭配特定處理器使用 [codec 組合]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/codec-processor-combinations/)。

<!-- vale off -->
### json codec
<!-- vale on -->

`json` codec 會將每一行剖析為 JSON 陣列中的單一 JSON 物件，然後為陣列中的每個物件建立 Data Prepper 事件。它可用於將巢狀 CloudWatch 事件剖析為個別記錄項目。
它也支援下列組態以搭配此 codec 使用。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`key_name` | 否 | 字串 | 要從中擷取 JSON 陣列並建立 Data Prepper 事件的輸入欄位名稱。
`include_keys` | 否 | List | 要擷取並新增為 Data Prepper 事件中其他欄位的輸入欄位清單。
`include_keys_metadata` | 否 | List | 要擷取並新增至 Data Prepper 事件中繼資料物件的輸入欄位清單。
`max_event_length` | 否 | 整數 | JSON codec 讀取之任何單一事件的大小上限。預設值為 20,000,000 個字元。


### `newline` codec

`newline` codec 會將每個 Kinesis 串流記錄剖析為單一記錄事件，非常適合處理單行記錄。它也能與 [`parse_json` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/parse-json/)搭配使用，以剖析每一行。

您可以使用下列選項來設定 `newline` codec。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`skip_lines` | 否 | 整數 | 設定建立事件前要略過的行數。您可以使用此組態略過常見的標題列。預設值為 `0`。
`header_destination` | 否 | 字串  | 定義要指派給串流事件標題行的索引鍵值。若指定此選項，則每個事件都會包含 `header_destination` 欄位。

### `otel_traces` codec

`otel_traces` codec 會將每個 Kinesis 資料串流記錄剖析為 OpenTelemetry 追蹤記錄，並為每個追蹤區段 (span) 記錄建立 Data Prepper 追蹤區段事件。

您可以使用下列選項來設定 `otel_traces` codec。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`format` | 否 | 字串 | 指定 OpenTelemetry 追蹤的格式。有效值為 `json` 和 `protobuf`。預設值為 `json`。
`otel_format` | 否 | 字串 | 指定解碼後追蹤區段的輸出格式。有效值為 `opensearch` 和 `otel`。預設值為 `opensearch`。
`length_prefixed_encoding` | 否 | 布林值 | 指定在 protobuf 格式中長度是否位於資料之前。預設值為 `false`。

<!-- vale off -->
### polling
<!-- vale on -->

當 `consumer_strategy` 設定為 `polling` 時，`kinesis` 來源會改用以輪詢為基礎的方式從 Kinesis 資料串流讀取記錄，而非預設的 `fan-out` 方式。

選項 | 必要 | 類型    | 說明
:--- | :--- |:--------| :---
`max_polling_records` | 否 | 整數 | 設定單次呼叫時從 Kinesis 擷取的記錄數量。預設值為 `10000`。
`idle_time_between_reads` | 否 | 持續時間  | 定義兩次呼叫之間的閒置時間長度。預設值為 `250ms`。

<!-- vale off -->
### aws
<!-- vale on -->

您可以在 `aws` 組態中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 設定用於認證資訊的 AWS 區域。預設採用[判斷區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 定義向 Amazon Kinesis Data Streams 與 Amazon DynamoDB 發出請求時所要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，此值會採用[認證資訊的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`sts_external_id` | 否 | 字串 | 定義擔任 STS 角色時所使用的外部 ID。長度必須介於 2 到 1,224 個字元之間。
`sts_header_overrides` | 否 | Map | 定義 AWS Identity and Access Management (IAM) 角色為來源外掛程式所擔任的標頭覆寫對應表。最多 5 個標頭。

## 公開的中繼資料屬性

`kinesis` 來源會將下列中繼資料新增至每個已處理的事件。您可以使用[運算式語法 `getMetadata` 函式]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/get-metadata/)存取中繼資料屬性。

- `stream_name`：包含取得事件來源的 Kinesis 資料串流名稱。

## 權限

若要以來源身分執行 `kinesis`，需要下列最低權限：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "kinesis:DescribeStream",
        "kinesis:DescribeStreamConsumer",
        "kinesis:DescribeStreamSummary",
        "kinesis:GetRecords",
        "kinesis:GetShardIterator",
        "kinesis:ListShards",
        "kinesis:ListStreams",
        "kinesis:ListStreamConsumers",
        "kinesis:RegisterStreamConsumer",
        "kinesis:SubscribeToShard"
      ],
      "Resource": [
        "arn:aws:kinesis:us-east-1:{account-id}:stream/stream1",
        "arn:aws:kinesis:us-east-1:{account-id}:stream/stream2"
      ]
    },
    {
      "Sid": "allowCreateTable",
      "Effect": "Allow",
      "Action": [
        "dynamodb:CreateTable",
        "dynamodb:PutItem",
        "dynamodb:DescribeTable",
        "dynamodb:DeleteItem",
        "dynamodb:GetItem",
        "dynamodb:Scan",
        "dynamodb:UpdateItem",
        "dynamodb:Query"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:{account-id}:table/kinesis-pipeline"
      ]
    }
  ]
}
```

`kinesis` 來源會使用 DynamoDB 資料表協調多個工作程序的資料匯入，因此您需要 DynamoDB 權限。

## 指標

`kinesis` 來源包含下列指標。

### 計數器

* `recordsProcessed`：計算已處理的串流記錄數。
* `recordProcessingErrors`：計算串流記錄處理錯誤數。
* `acknowledgementSetSuccesses`：計算已成功新增至接收器的已處理串流記錄數。
* `acknowledgementSetFailures`：計算新增至接收器失敗的已處理串流記錄數。
