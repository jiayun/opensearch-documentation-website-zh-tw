---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "S3 記錄檔"
parent: Common use cases
nav_order: 40
---

# S3 記錄檔

OpenSearch Data Prepper 可讓您從 [Amazon Simple Storage Service](https://aws.amazon.com/s3/) (Amazon S3) 載入記錄檔，包括傳統記錄檔、JSON 文件與 CSV 記錄檔。

## 架構

Data Prepper 可以使用 [Amazon Simple Queue Service (SQS)](https://aws.amazon.com/sqs/) (Amazon SQS) 佇列與 [Amazon S3 Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)，從 S3 儲存貯體讀取物件。

Data Prepper 會輪詢 Amazon SQS 佇列以取得 S3 事件通知。當 Data Prepper 收到 S3 物件已建立的通知時，就會讀取並剖析該 S3 物件。

下圖顯示相關元件的整體架構。

![S3 來源架構]({{site.url}}{{site.baseurl}}/images/data-prepper/s3-source/s3-architecture.jpg)

元件的資料流程如下：

1. 系統將記錄檔產生至 S3 儲存貯體。
2. S3 在 SQS 佇列中建立 S3 事件通知。
3. Data Prepper 輪詢 Amazon SQS 以取得訊息，然後接收一則訊息。
4. Data Prepper 從 S3 物件下載內容。
5. Data Prepper 將 S3 物件中的內容以文件形式傳送至 OpenSearch。

## 管線概觀

Data Prepper 支援使用 [`s3` 來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/)從 S3 讀取資料。

下圖顯示 Data Prepper 管線從 S3 讀取資料的概念示意。

![S3 來源架構]({{site.url}}{{site.baseurl}}/images/data-prepper/s3-source/s3-pipeline.jpg)

## 先決條件

在 Data Prepper 能夠從 S3 讀取記錄資料之前，您需要符合下列先決條件：

- 一個 S3 儲存貯體。
- 一個將記錄檔寫入 S3 的記錄產生器。確切的記錄產生器會依您的特定使用案例而異，但可能包括將記錄檔寫入 S3，或使用 Amazon CloudWatch 等服務。

## 入門

請使用下列步驟開始使用 Data Prepper 從 S3 載入記錄檔。

1. 為您的 S3 事件通知建立 [SQS 標準佇列](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/step-create-queue.html)。
2. 為 SQS 設定[儲存貯體通知](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html)。請使用 `s3:ObjectCreated:*` 事件類型。
3. 授予 Data Prepper [AWS Identity and Access Management (IAM)](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html) 權限，以存取 SQS 與 S3。
4. (建議) 建立 [SQS 死信佇列](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html) (DLQ)。
5. (建議) 設定 SQS 重新驅動政策，將失敗的訊息移至 DLQ。

### 為 Data Prepper 設定權限

若要檢視 S3 記錄檔，Data Prepper 需要存取 Amazon SQS 與 S3。請使用下列範例來設定權限：

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "s3-access",
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<YOUR-BUCKET>/*"
        },
        {
            "Sid": "sqs-access",
            "Effect": "Allow",
            "Action": [
                "sqs:DeleteMessage",
                "sqs:ReceiveMessage"
            ],
            "Resource": "arn:aws:sqs:<YOUR-REGION>:<123456789012>:<YOUR-SQS-QUEUE>"
        },
        {
            "Sid": "kms-access",
            "Effect": "Allow",
            "Action": "kms:Decrypt",
            "Resource": "arn:aws:kms:<YOUR-REGION>:<123456789012>:key/<YOUR-KMS-KEY>"
        }
    ]
}
```
{% include copy-curl.html %}

如果您的 S3 物件或 SQS 佇列未使用 KMS，您可以移除 `kms:Decrypt` 權限。

### SQS 死信佇列

下列兩種選項可用於處理 S3 物件處理錯誤：

- 使用 SQS 死信佇列 (DLQ) 追蹤失敗。這是建議的做法。
- 從 SQS 刪除訊息。您必須手動找出 S3 物件並修正錯誤。

下圖顯示搭配 DLQ 使用 SQS 時的系統架構。

![搭配 DLQ 的 S3 來源架構]({{site.url}}{{site.baseurl}}/images/data-prepper/s3-source/s3-architecture-dlq.jpg)

若要使用 SQS 死信佇列，請執行下列步驟：

1. 建立新的 SQS 標準佇列作為 DLQ。
2. 設定您的 SQS 重新驅動政策[以使用 DLQ](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-configure-dead-letter-queue.html)。建議將 **Maximum Receives** 設定設為較低的值，例如 2 或 3。
3. 設定 Data Prepper `s3` 來源，針對 `on_error` 使用 `retain_messages`。這是預設行為。

## 管線設計

建立一條從 S3 讀取記錄檔的管線，首先從 [`s3`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/) 來源外掛程式開始。請參考下列範例。

```yaml
s3-log-pipeline:
   source:
     s3:
       notification_type: sqs
       compression: gzip
       codec:
         newline:
       sqs:
         # Change this value to your SQS Queue URL
         queue_url: "arn:aws:sqs:<YOUR-REGION>:<123456789012>:<YOUR-SQS-QUEUE>"
         visibility_timeout: "2m"
```
{% include copy-curl.html %}

請根據您的使用案例設定下列選項：

* `queue_url`：這是 SQS 佇列 URL，對您的管線而言永遠是唯一的。
* `codec`：codec 決定如何剖析傳入的資料。
* `visibility_timeout`：請將此值設定為足夠大，讓 Data Prepper 能夠處理 10 個 S3 物件。不過，如果此值設定得太大，處理失敗的訊息在 Data Prepper 重試之前，至少會等待指定的時間。

每個選項的預設值適用於大多數使用案例。如需 S3 來源所有可用選項，請參閱 [`s3`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/s3/)。

```yaml
s3-log-pipeline:
   source:
     s3:
       notification_type: sqs
       compression: gzip
       codec:
         newline:
       sqs:
         # Change this value to your SQS Queue URL
         queue_url: "arn:aws:sqs:<YOUR-REGION>:<123456789012>:<YOUR-SQS-QUEUE>"
         visibility_timeout: "2m"
       aws:
         # Specify the correct region
         region: "<YOUR-REGION>"
         # This shows using an STS role, but you can also use your system's default permissions.
         sts_role_arn: "arn:aws:iam::<123456789012>:role/<DATA-PREPPER-ROLE>"
   processor:
     # You can configure a grok pattern to enrich your documents in OpenSearch.
     #- grok:
     #    match:
     #      message: [ "%{COMMONAPACHELOG}" ]
   sink:
     - opensearch:
         hosts: [ "https://localhost:9200" ]
         # Change to your credentials
         username: "admin"
         password: "admin"
         index: s3_logs
```
{% include copy-curl.html %}

## 多條 Data Prepper 管線

建議每條 Data Prepper 管線各使用一個 SQS 佇列。此外，您也可以讓同一叢集中的多個節點從同一個 SQS 佇列讀取資料，這不需要額外的 Data Prepper 組態。

如果您有多條管線，則必須為每條管線建立多個 SQS 佇列，即使這些管線使用同一個 S3 儲存貯體也一樣。

## Amazon SNS 扇出模式

為了應付 S3 產生的記錄檔規模，有些使用者需要多個 SQS 佇列來處理記錄檔。您可以使用 [Amazon Simple Notification Service](https://docs.aws.amazon.com/sns/latest/dg/welcome.html) (Amazon SNS)，將來自 S3 的事件通知路由至 SQS [扇出模式](https://docs.aws.amazon.com/sns/latest/dg/sns-common-scenarios.html)。使用 SNS 時，所有 S3 事件通知都會直接傳送至單一 SNS 主題，您可以在該主題訂閱多個 SQS 佇列。

為確保 Data Prepper 能夠直接剖析來自 SNS 主題的事件，請在 SNS 至 SQS 的訂閱上設定[原始訊息傳遞](https://docs.aws.amazon.com/sns/latest/dg/sns-large-payload-raw-message-delivery.html)。套用此選項不會影響訂閱該 SNS 主題的其他 SQS 佇列。

## 使用 Amazon S3 Select 篩選與擷取資料

如果管線使用 S3 來源，您可以在將 S3 物件內容匯入管線之前，使用 SQL 運算式對其執行篩選與運算。

`s3_select` 選項支援 [Parquet File Format](https://parquet.apache.org/docs/) 的物件。它也適用於以 gzip 或 BZIP2 壓縮的物件 (僅限 CSV 與 JSON 物件)，並支援使用 gzip 與 Snappy 為 Parquet File Format 進行資料行壓縮。

如需使用 Amazon S3 Select 的完整資訊，請參閱 [Filtering and retrieving data using Amazon S3 Select](https://docs.aws.amazon.com/AmazonS3/latest/userguide/selecting-content-from-objects.html) 與 [SQL reference for Amazon S3 Select](https://docs.aws.amazon.com/AmazonS3/latest/userguide/s3-select-sql-reference.html)。
{: .note}

下列範例管線會擷取以 Parquet File Format 編碼的 S3 物件中的所有資料：

```json
pipeline:
  source:
    s3:
      s3_select:
        expression: "select * from s3object s"  
        input_serialization: parquet
      notification_type: "sqs"
...
```
{% include copy-curl.html %}

下列範例管線只會擷取物件中的前 10,000 筆記錄：

```json
pipeline:
  source:
    s3:
      s3_select:
        expression: "select * from s3object s LIMIT 10000"
        input_serialization: parquet
      notification_type: "sqs"
...
```
{% include copy-curl.html %}

下列範例管線會從 `data_value` 位於指定範圍 200--500 內的 S3 物件擷取記錄：

```json
pipeline:
  source:
    s3:
      s3_select:
        expression: "select s.* from s3object s where s.data_value > 200 and s.data_value < 500 "
        input_serialization: parquet
      notification_type: "sqs"
...
```
{% include copy-curl.html %}
