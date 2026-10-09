---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: AWS Lambda
parent: Processors
grand_parent: Pipelines
nav_order: 40
---

# AWS Lambda 處理器

[AWS Lambda](https://aws.amazon.com/lambda/) 整合可讓您在 OpenSearch Data Prepper 管線中使用無伺服器運算功能，實現彈性的事件處理與資料路由。

## 組態

`aws_lambda` 處理器可讓您在 Data Prepper 管線中呼叫 AWS Lambda 函式以處理事件。它可依據您的使用案例，支援同步與非同步呼叫。

## 組態欄位

您可以使用下列組態選項來設定此處理器。

欄位 | 類型 | 必要 | 說明
-------------------- | ------- | -------- | ---------------------------------------------------------------------------- 
`function_name` | 字串 | 必要 | 要呼叫的 AWS Lambda 函式名稱。長度必須為 3--500 個字元。
`aws.region` | 字串 | 必要 | Lambda 函式所在的 AWS 區域。
`aws.sts_role_arn` | 字串 | 選用 | 呼叫 Lambda 函式前要擔任之角色的 Amazon 資源名稱（ARN）。長度必須為 20--2048 個字元。
`aws.sts_external_id` | 字串 | 選用 | 用於 STS 角色擔任的外部 ID。長度必須為 2--1224 個字元。
`aws.sts_header_overrides` | 對應表 | 選用 | STS 標頭覆寫。最多支援 5 個標頭。
`client.max_retries` | 整數 | 選用 | 呼叫失敗時的最大重試次數。預設為 `3`。
`client.api_call_timeout` | 持續時間 | 選用 | API 呼叫逾時。預設為 `60s`。
`client.api_call_attempt_timeout` | 持續時間 | 選用 | 個別 API 呼叫嘗試的逾時。若未指定，則使用 AWS SDK 預設值。
`client.connection_timeout` | 持續時間 | 選用 | SDK 連線逾時。預設為 `60s`。
`client.read_timeout` | 持續時間 | 選用 | SDK 等待從已建立連線讀取資料的時間。若未指定，則使用 AWS SDK 預設值。
`client.max_concurrency` | 整數 | 選用 | 用戶端上的最大並行執行緒數。預設為 `200`。
`client.base_delay` | 持續時間 | 選用 | 指數退避的基本延遲。預設為 `100ms`。
`client.max_backoff` | 持續時間 | 選用 | 指數退避的最大退避時間。預設為 `20s`。
`client.retryable_status_codes` | 清單 | 選用 | Lambda 呼叫傳回時會觸發重試的 HTTP 狀態碼清單，例如 `[500, 502, 503, 504]`。預設為空清單（僅使用標準 AWS SDK 重試條件）。請用於可安全重試暫時性伺服器端錯誤的冪等函式。
`batch` | 物件 | 選用 | Lambda 呼叫的批次設定。包含 `key_name`（預設值：`"events"`），以及含有 `event_count`（預設值：`100`）、`maximum_size`（預設值：`"5mb"`）和 `event_collect_timeout`（預設值：`10s`）的 `threshold` 物件。如需詳細資訊，請參閱[批次處理](#batch-processing)。
`lambda_when` | 字串 | 選用 | 決定何時呼叫 Lambda 處理器的條件運算式。
`response_codec` | 物件 | 選用 | 用於剖析 Lambda 回應的轉碼器組態。預設為 `json`。
`tags_on_failure` | 清單 | 選用 | 當 Lambda 函式失敗或遇到例外狀況時，要新增至事件的標籤清單。
`response_events_match` | 布林值 | 選用 | 指定 Data Prepper 如何解譯及處理 Lambda 函式回應。預設為 `false`。
`response_mode` | 字串 | 選用 | 回應處理模式，可為 `replace` 或 `merge`。預設為 `replace`。
`keys` | 清單 | 選用 | 要傳送至 Lambda 函式的索引鍵。
`cache` | 物件 | 選用 | 快取組態。僅在 `response_mode` 為 `merge` 且已指定 `keys` 時有效。
`cache.ttl` | 長整數 | 選用 | 快取存留時間。
`cache.max_size` | 長整數 | 選用 | 快取大小上限。必須介於 1048576 與 10485760 之間。
`circuit_breaker_retries` | 整數 | 選用 | 繼續執行前斷路器檢查的最大次數。預設為 `0`。
`circuit_breaker_wait_interval` | 長整數 | 選用 | 斷路器檢查之間的間隔時間（以毫秒為單位）。預設為 `1000ms`。

以下是組態範例：

```yaml
processors:
  - aws_lambda:
      function_name: my-lambda-function
      response_events_match: false
      response_mode: replace
      aws:
        region: us-east-1
        sts_role_arn: arn:aws:iam::123456789012:role/my-lambda-role
      client:
        max_retries: 3
        api_call_timeout: PT60S
        api_call_attempt_timeout: PT30S  # Optional: per-attempt timeout
        connection_timeout: PT60S
        read_timeout: PT15M              # Optional: for long-running Lambda functions
        max_concurrency: 200
        base_delay: "PT0.1S"
        max_backoff: "PT20S"
        retryable_status_codes: [500, 502, 503, 504]  # Optional: retry these Lambda invocation status codes
      batch:
        key_name: events
        threshold:
          event_count: 100
          maximum_size: 5mb
          event_collect_timeout: PT10S
      lambda_when: "/some_key == null"
      keys: ["key1", "key2"]
      cache:
        ttl: 3600
        max_size: 5242880
      circuit_breaker_retries: 0
      circuit_breaker_wait_interval: 1000
      tags_on_failure: ["lambda_failed"]
```
{% include copy.html %}

## 逾時組態

`aws_lambda` 處理器依循 AWS SDK 最佳實務，支援多層逾時設定：

- `api_call_timeout`：整個 API 呼叫（包含所有重試）的總時間。
- `api_call_attempt_timeout`：每次個別嘗試的時間限制。
- `read_timeout`：從已建立連線等待資料的時間。

對於執行時間超過 60 秒的 Lambda 函式，請將 `api_call_timeout` 與 `read_timeout` 都設定為適當的值。`api_call_attempt_timeout` 會強制執行每次嘗試的逾時，讓緩慢的請求能快速失敗，同時保留整體的重試行為。

## 使用方式

此處理器支援下列呼叫類型：

- `request-response`：處理器會等待 Lambda 函式完成後再繼續執行。
- `event`：以非同步方式觸發函式，不等待回應。

### 批次處理

`aws_lambda` 處理器在呼叫 Lambda 函式時會將事件分批處理。`batch` 組態可讓您設定大量呼叫的閾值。

`batch` 組態的結構如下：

- `key_name`：在傳送至 Lambda 的承載中，用來將事件分組的索引鍵（預設值：`"events"`）。
- `threshold`：包含批次閾值設定的物件：
  - `event_count`：每個批次的最大事件數（預設值：`100`）。
  - `maximum_size`：批次大小上限（預設值：`5mb`）。
  - `event_collect_timeout`：傳送批次前收集事件的最長等待時間（預設值：`10s`）。必須介於 1 秒與 3600 秒之間。

**重要**：`event_collect_timeout` 參數必須指定在 `batch.threshold` 底下，而非直接指定在 `batch` 底下。

### 回應處理

此處理器支援兩種回應模式：
- `replace`：Lambda 回應取代原始事件資料（預設）
- `merge`：Lambda 回應與原始事件資料合併

### 快取

當 `response_mode` 設定為 `merge` 且指定了 `keys` 時，處理器可以快取 Lambda 回應，以提升重複請求的效能。

### 斷路器

處理器包含斷路器功能，可從容處理記憶體壓力情況。

### 失敗時加上標籤

當 Lambda 處理失敗或發生例外狀況時，可以使用 `tags_on_failure` 組態為事件套用自訂標籤。

## 行為

設定為批次處理時，`aws_lambda` 處理器會將多個事件分組為單一請求。此分組由批次閾值決定，可依據事件數量、大小限制或逾時時間。接著處理器會將整個批次作為單一承載傳送至 Lambda 函式。

## Lambda 回應處理

`response_events_match` 設定定義了 Data Prepper 如何處理傳送至 Lambda 的批次事件與所收到回應之間的關係：

- `true`：Lambda 傳回一個 JSON 陣列，其中包含每個批次事件的結果。Data Prepper 會將此陣列對應回其相應的原始事件，確保批次中的每個事件都取得陣列中對應的回應部分。
- `false`：Lambda 針對整個批次傳回一或多個事件。回應事件與原始事件沒有關聯。原始事件的中繼資料不會保留在回應事件中。例如，當 `response_events_match` 設定為 `true` 時，Lambda 函式預期會傳回與原始請求數量相同的回應事件數，並維持原始順序。

## Lambda 函式實作

當 Data Prepper 呼叫您的 Lambda 函式時，會傳送一個 JSON 物件，其中事件分組在設定的 `key_name` 之下（預設：`"events"`）。

### 輸入格式

您的 Lambda 函式會收到以下輸入結構：

```json
{
  "events": [
    {"field1": "value1", "field2": "value2"},
    {"field1": "value3", "field2": "value4"}
  ]
}
```
{% include copy.html %}

索引鍵名稱（在此範例中為 `"events"`）可透過 `batch.key_name` 參數設定。

### 輸出格式

預期的輸出格式取決於 `response_events_match` 設定：

#### 當設定為 `response_events_match: false` 時（預設）

Lambda 可以傳回一或多個新事件。傳回的事件不需要與輸入數量相符。當設定為 `response_events_match: false` 時，`aws_lambda` 處理器會捨棄所有輸入事件，僅輸出 Lambda 函式傳回的事件，以取代輸入資料而非與其合併：

```python
def lambda_handler(event, context):
    # Process all input events and return new events
    return [
        {"result": "processed_data_1"},
        {"result": "processed_data_2"}
    ]
```
{% include copy.html %}

#### 當設定為 `response_events_match: true` 時

以下函式會在每個事件中將 `status` 索引鍵設定為靜態值 `processed`：

```python
def lambda_handler(event, context):
    input_events = event.get('events', [])
    output = []

    # Process each event and maintain order
    for input_event in input_events:
        processed_event = input_event.copy()
        processed_event["status"] = "processed"
        # Transform data as needed
        for key, value in input_event.items():
            if isinstance(value, str):
                processed_event[key] = value.upper()
        output.append(processed_event)

    # Must return same count as input
    return output
```
{% include copy.html %}

<!-- vale off -->
### Lambda 函式範例
<!-- vale on -->

以下 Lambda 函式會將所有字串欄位轉換為大寫：

```python
def lambda_handler(event, context):
    # Get events from the configured key_name (default: "events")
    input_events = event.get('events', [])
    output_events = []

    for input_event in input_events:
        # Add transformation marker
        input_event["_transformed_"] = True

        # Transform string fields to uppercase
        for key, value in input_event.items():
            if isinstance(value, str):
                input_event[key] = value.upper()

        output_events.append(input_event)

    return output_events
```
{% include copy.html %}

## 限制

請注意以下限制：

- 承載限制：6 MB 承載上限
- 回應編碼器：僅支援 JSON 編碼器

## 整合測試

此外掛程式的整合測試與主要 Data Prepper 建置程序分開執行。請使用以下 Gradle 命令執行這些測試：

```bash
./gradlew :data-prepper-plugins:aws-lambda:integrationTest -Dtests.processor.lambda.region="us-east-1" -Dtests.processor.lambda.functionName="lambda_test_function"  -Dtests.processor.lambda.sts_role_arn="arn:aws:iam::123456789012:role/dataprepper-role
```
{% include copy.html %}
