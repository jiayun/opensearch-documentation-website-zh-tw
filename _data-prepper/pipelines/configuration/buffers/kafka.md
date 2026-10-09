---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: kafka
parent: Buffers
grand_parent: Pipelines
nav_order: 80
---

# Kafka 緩衝區

`kafka` 緩衝區會將資料緩衝至 Apache Kafka 主題 (topic) 中。資料在傳輸期間會透過 Kafka 主題保存。

以下範例說明如何在 HTTP 管線中執行 Kafka 緩衝區。
此範例會連線至在本機執行的 Kafka 叢集。

```yaml
kafka-buffer-pipeline:
  source:
    http:
  buffer:
    kafka:
      bootstrap_servers: ["localhost:9092"]
      encryption:
        type: none
      topics:
        - name: my-buffer-topic
          group_id: data-prepper
          create_topic: true
  processor:
    - grok:
        match:
          message: [ "%{COMMONAPACHELOG}" ]
  sink:
    - stdout:
```

## 組態選項

請搭配 `kafka` 緩衝區使用下列組態選項。


選項 | 必要 | 類型 | 說明
--- | --- | --- | ---
`authentication` | 否 | [驗證](#authentication) | 設定管線與 Kafka 兩者的驗證選項。如需詳細資訊，請參閱[驗證](#authentication)。
`aws` | 否 | [AWS](#aws) | AWS 組態。如需詳細資訊，請參閱 [`aws`](#aws)。
`bootstrap_servers` | 是 | 字串清單 | 與 Kafka 叢集進行初始連線時所用的主機與連接埠。您可以使用每個 broker 的 IP 位址或連接埠號碼來設定多個 Kafka broker。使用 [Amazon Managed Streaming for Apache Kafka (Amazon MSK)](https://aws.amazon.com/msk/) 作為 Kafka 叢集時，系統會使用組態中提供的 Amazon Resource Name (ARN)，從 Amazon MSK 取得 bootstrap server 資訊。
`encryption` | 否 | [加密](#encryption) | 傳輸中加密的加密組態。如需詳細資訊，請參閱[加密](#encryption)。
`producer_properties` | 否 | [Producer 屬性](#producer_properties) | 可設定的 Kafka producer 屬性清單。 
`topics` | 是 | 清單 | 緩衝區要使用的[主題](#topic)清單。每個緩衝區必須提供一個主題。


<!-- vale off -->
### topic
<!-- vale on -->

`topic` 選項用於設定單一 Kafka 主題，並指示 `kafka` 緩衝區如何使用該主題。


選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | Kafka 主題的名稱。
`group_id` | 是 | 字串 | 設定 Kafka 的 `group.id` 選項。
`workers` | 否 | 整數 | 與每個主題相關聯的多執行緒取用者 (consumer) 數量。預設值為 `2`。最大值為 `200`。
`encryption_key` | 否 | 字串 | 進階加密標準 (AES) 加密金鑰，用於在資料傳送至 Kafka 之前，於 OpenSearch Data Prepper 內加密與解密資料。此值必須為純文字，或使用 AWS Key Management Service (AWS KMS) 加密。
`kms` | 否 | AWS KMS 金鑰 | 設定後，會使用 AWS KMS 金鑰加密資料。如需詳細資訊，請參閱 [`kms`](#kms)。
`auto_commit` | 否 | 布林值 | 若為 `false`，取用者位移 (offset) 不會在背景中定期提交至 Kafka。預設值為 `false`。
`commit_interval` | 否 | 整數 | 當 `auto_commit` 設為 `true` 時，透過 Kafka 的 `auto.commit.interval.ms` 選項設定取用者位移自動提交至 Kafka 的頻率 (以秒為單位)。預設值為 `5s`。
`session_timeout` | 否 | 整數 | 使用 Kafka 的群組管理功能時，來源偵測用戶端故障的時間長度。群組管理功能可用於平衡資料串流。預設值為 `45s`。
`auto_offset_reset` | 否 | 字串 | 透過 Kafka 的 `auto.offset.reset` 選項，自動將位移重設為最早或最新的位移。預設值為 `earliest`。
`thread_waiting_time` | 否 | 整數 | 執行緒等待前一個執行緒完成其工作並通知下一個執行緒的時間長度。Kafka 取用者 API 的輪詢 (poll) 逾時值會設為此設定的一半。預設值為 `5s`。
`max_partition_fetch_bytes` | 否 | 整數 | 透過 Kafka 的 `max.partition.fetch.bytes` 設定，設定每個分割區 (partition) 傳回資料的上限 (以 MB 為單位)。預設值為 `1mb`。
`heart_beat_interval` | 否 | 整數 | 透過 Kafka 的 `heartbeat.interval.ms` 設定使用 Kafka 的群組管理功能時，傳送至取用者協調器 (consumer coordinator) 的心跳之間的預期間隔時間。預設值為 `5s`。
`fetch_max_wait` | 否 | 整數 | 透過 Kafka 的 `fetch.max.wait.ms` 設定，在沒有足夠資料滿足 `fetch_min_bytes` 要求時，伺服器封鎖擷取 (fetch) 請求的最長時間。預設值為 `500ms`。
`fetch_max_bytes` | 否 | 整數 | 透過 Kafka 的 `fetch.max.bytes` 設定，broker 可接受的記錄大小上限。預設值為 `50mb`。
`fetch_min_bytes` | 否 | 整數 | 透過 Kafka 的 `retry.backoff.ms` 設定，伺服器在擷取請求期間傳回的最小資料量。預設值為 `1b`。
`retry_backoff` | 否 | 整數 | 重試對指定主題分割區失敗的請求之前，所需等待的時間長度。預設值為 `10s`。
`max_poll_interval` | 否 | 整數 | 透過 Kafka 的 `max.poll.interval.ms` 選項使用群組管理時，兩次呼叫 `poll()` 之間的最長延遲時間。預設值為 `300s`。
`consumer_max_poll_records` | 否 | 整數 | 透過 Kafka 的 `max.poll.records` 設定，單次 `poll()` 呼叫所傳回的記錄數量上限。預設值為 `500`。
`max_message_bytes` | 否 | 整數 | 訊息大小上限 (以位元組為單位)。預設值為 1 MB。


<!-- vale off -->
### kms
<!-- vale on -->

使用 AWS KMS 時，AWS KMS 金鑰可以解密 `encryption_key`，使其不必以純文字儲存。若要搭配 `kafka` 緩衝區設定 AWS KMS，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`key_id` | 是 | 字串 | AWS KMS 金鑰的 ID。可以是完整的金鑰 ARN 或金鑰別名。
`region` | 否 | 字串 | AWS KMS 金鑰所在的 AWS 區域。
`sts_role_arn` | 否 | 字串 | 用於存取 AWS KMS 金鑰的 AWS Security Token Service (AWS STS) 角色 ARN。
`encryption_context` | 否 | Map | 若有提供，傳送至主題的訊息會將此 Map 納入作為 AWS KMS 加密內容 (encryption context)。


### 驗證

`authentication` 物件內必須包含下列選項。

選項 | 類型 | 說明
:--- | :--- | :---
`sasl` | JSON 物件 | 簡單驗證與安全層 (SASL) 驗證組態。


### SASL

設定 SASL 驗證時，請使用下列其中一個選項。

選項 | 類型 | 說明
:--- | :--- | :---
`plaintext` | JSON 物件 | [PLAINTEXT](#sasl-plaintext) 驗證組態。
`aws_msk_iam` | 字串 | Amazon MSK AWS Identity and Access Management (IAM) 組態。若設為 `role`，則會使用 `aws` 組態中設定的 `sts_role_arn`。預設值為 `default`。

#### SASL PLAINTEXT

使用 [SASL PLAINTEXT](https://kafka.apache.org/10/javadoc/org/apache/kafka/common/security/auth/SecurityProtocol.html) 通訊協定時，必須提供下列選項。

選項 | 類型 | 說明
:--- | :--- | :---
`username` | 字串 | PLAINTEXT 驗證的使用者名稱。
`password` | 字串 | PLAINTEXT 驗證的密碼。

#### 加密

設定 SSL 加密時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`type` | 否 | 字串 | 加密類型。使用 `none` 可停用加密。預設值為 `ssl`。
`insecure` | 否 | 布林值 | 用於關閉 SSL 憑證驗證的布林值旗標。若設為 `true`，則會關閉憑證授權單位 (CA) 憑證驗證，並傳送不安全的 HTTP 請求。預設值為 `false`。

<!-- vale off -->
#### producer_properties
<!-- vale on -->

請使用下列組態選項來設定 Kafka producer。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`max_request_size` | 否 | 整數 | producer 傳送至 Kafka 的請求大小上限。預設值為 1 MB。


<!-- vale off -->
#### aws
<!-- vale on -->

為 `aws` 服務設定驗證時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於憑證的 AWS 區域。預設採用[標準 SDK 判斷區域的行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon Simple Queue Service (Amazon SQS) 與 Amazon Simple Storage Service (Amazon S3) 發出請求時所擔任的 AWS STS 角色。預設值為 `null`，此時會使用[標準 SDK 憑證行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`msk` | 否 | JSON 物件 | [Amazon MSK](#msk) 組態設定。

<!-- vale off -->
#### msk
<!-- vale on -->

請在 `msk` 物件內使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`arn` | 是 | 字串 | 要使用的 [Amazon MSK ARN](https://docs.aws.amazon.com/msk/1.0/apireference/configurations-arn.html)。
`broker_connection_type` 否 | 字串 | 與 Amazon MSK broker 搭配使用的連接器類型，可為 `public`、`single_vpc` 或 `multi_vpc`。預設值為 `single_vpc`。
