---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: AWS Lambda
parent: Sinks
grand_parent: Pipelines
nav_order: 10
---

# AWS Lambda 接收端

本頁面說明如何在 OpenSearch Data Prepper 中設定與使用 [AWS Lambda](https://aws.amazon.com/lambda/)，讓 Lambda 函式同時作為處理器與接收端。

## 組態

使用下列參數來設定 Lambda 接收端。

欄位             | 類型    | 必要 | 說明                                                                 
--------------------| ------- | -------- | ---------------------------------------------------------------------------- 
`function_name`     | 字串  | 是      | 要叫用的 AWS Lambda 函式名稱。                               
`invocation_type`   | 字串  | 否       | 指定叫用類型。預設為 `event`。             
`aws.region`        | 字串  | 是      | Lambda 函式所在的 AWS 區域。                         
`aws.sts_role_arn`  | 字串  | 否       | 在叫用 Lambda 函式前所要擔任之角色的 Amazon Resource Name (ARN)。               
`max_retries`       | 整數 | 否       | Lambda 叫用失敗時，接收端層級的最大重試次數。此設定控制 Data Prepper 的重試邏輯。預設為 `3`。
`client.max_retries` | 整數 | 否 | 個別 API 呼叫在 AWS SDK 用戶端層級的最大重試次數。此設定控制底層 SDK 針對網路或服務錯誤的重試機制。預設為 `3`。             
`client.api_call_timeout` | Duration | 否 | 整個 API 呼叫（包含所有重試）的總逾時時間。預設為 `60s`。
`client.api_call_attempt_timeout` | Duration | 否 | 每次個別重試嘗試的逾時時間。若未指定，則使用 AWS SDK 的預設值。
`client.connection_timeout` | Duration | 否 | SDK 連線逾時時間。預設為 `60s`。
`client.read_timeout` | Duration | 否 | SDK 從已建立的連線讀取資料時所等待的時間。若未指定，則使用 AWS SDK 的預設值。
`client.max_concurrency` | 整數 | 否 | 用戶端的最大並行執行緒數。預設為 `200`。
`client.base_delay`  | Duration | 否 | 指數退避的基礎延遲。預設為 `100ms`。
`client.max_backoff` | Duration | 否 | 指數退避的最大退避時間。預設為 `20s`。             
`batch`             | 物件  | 否       | Lambda 叫用的選用批次設定。包含 `key_name`（預設：`"events"`）以及具有 `event_count`（預設：`100`）、`maximum_size`（預設：`"5mb"`）和 `event_collect_timeout`（預設：`10s`）的 `threshold` 物件。
`lambda_when`       | 字串  | 否       | 決定何時叫用 Lambda 接收端的條件運算式。          
`dlq`               | 物件  | 否       | 失敗叫用的死信佇列 (DLQ) 組態。                

#### 組態範例

```yaml
sink:
  - aws_lambda:
      function_name: "my-lambda-sink"
      invocation_type: "event"
      aws:
        region: "us-west-2"
        sts_role_arn: "arn:aws:iam::123456789012:role/my-lambda-sink-role"
      max_retries: 5
      client:
        max_retries: 3
        api_call_timeout: PT60S
        api_call_attempt_timeout: PT30S  # Optional: per-attempt timeout
        connection_timeout: PT60S
        read_timeout: PT15M              # Optional: for long-running Lambda functions
        max_concurrency: 200
        base_delay: PT0.1S
        max_backoff: PT20S
      batch:
        key_name: "events"
        threshold:
          event_count: 50
          maximum_size: "3mb"
          event_collect_timeout: PT5S
      lambda_when: "event['type'] == 'log'"
      dlq:
        region: "us-east-1"
        sts_role_arn: "arn:aws:iam::123456789012:role/my-sqs-role"
        bucket: "<<your-dlq-bucket-name>>"
```
{% include copy.html %}

## 逾時組態

AWS Lambda 接收端遵循 AWS SDK 最佳實務，支援多層逾時：

- `api_call_timeout`：整個 API 呼叫（包含所有重試）的總時間。
- `api_call_attempt_timeout`：每次個別嘗試的時間限制。
- `read_timeout`：從已建立的連線等待資料的時間。

對於執行時間超過 60 秒的 Lambda 函式，請將 `api_call_timeout` 與 `read_timeout` 都設定為適當的值。

## 用法

叫用類型如下：

- `event`（預設）：以非同步方式執行函式，不等待回應。  
- `request-response`（僅限接收端）：以同步方式執行函式，但不會處理回應。
- `batch`：根據設定的門檻自動將事件分組。 
- `dlq`：支援在重試嘗試後針對失敗叫用使用 DLQ 組態。

Data Prepper 元件使用 AWS Identity and Access Management (IAM) 角色擔任機制 `aws.sts_role_arn`，以安全地叫用 Lambda 函式，並在事件處理期間遵守 Lambda 的並行限制。如需更多資訊，請參閱 [AWS Lambda 文件](https://docs.aws.amazon.com/lambda)。
{: .note}

## 開發人員指南

整合測試必須與 Data Prepper 主要建置分開執行。請使用下列命令執行：

```bash
./gradlew :data-prepper-plugins:aws-lambda:integrationTest -Dtests.sink.lambda.region="us-east-1" -Dtests.sink.lambda.functionName="lambda_test_function"  -Dtests.sink.lambda.sts_role_arn="arn:aws:iam::123456789012:role/dataprepper-role
```
{% include copy.html %}
