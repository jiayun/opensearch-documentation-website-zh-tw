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
`acknowledgements_timeout` | 否 | 持續時間 | 等待從 Kafka 主題讀取之記錄的端對端確認的最長時間。如果記錄未在此時間內獲得確認，緩衝區會重設分割區並重新讀取記錄。根據預設，確認實際上永遠不會逾時。
`authentication` | 否 | [驗證](#authentication) | 設定管線與 Kafka 兩者的驗證選項。如需詳細資訊，請參閱[驗證](#authentication)。
`aws` | 否 | [AWS](#aws) | AWS 組態。如需詳細資訊，請參閱 [`aws`](#aws)。
`bootstrap_servers` | 是 | 字串清單 | 初次連線至 Kafka 叢集時使用的主機與連接埠。您可以使用各個 Kafka broker 的 IP 位址或連接埠號碼，設定多個 broker。使用 [Amazon Managed Streaming for Apache Kafka (Amazon MSK)](https://aws.amazon.com/msk/) 作為您的 Kafka 叢集時，系統會使用組態中提供的 Amazon Resource Name (ARN) 從 Amazon MSK 取得 bootstrap 伺服器資訊。
`bounded_batch_size` | 否 | 整數 | 每次讀取後從記憶體內緩衝區排出的記錄數量上限。Kafka 緩衝區會將主題中的記錄取用至此記憶體內緩衝區，再由處理器從中讀取記錄。預設值為 `250000`。
`bounded_buffer_size` | 否 | 整數 | 從 Kafka 主題取用記錄後，記憶體內緩衝區可接受的記錄數量上限。預設值為 `1000000`。
`custom_metric_prefix` | 否 | 字串 | 緩衝區指標的自訂前置詞。此前置詞會取代指標名稱中的外掛程式名稱。例如，將此選項設為 `mybuffer` 會產生 `mybufferRead_recordsConsumedRate` 之類的指標。如果未指定，則會使用外掛程式名稱 `kafka`。
`drain_timeout` | 否 | 持續時間 | 管線關閉時，等待緩衝區排空的最長時間。預設值為 `30s`。
`encryption` | 否 | [加密](#encryption) | 傳輸中加密的組態。如需詳細資訊，請參閱[加密](#encryption)。
`producer_properties` | 否 | [生產者屬性](#producer_properties) | 可設定的 Kafka 生產者屬性清單。 
`topics` | 是 | 清單 | 供緩衝區使用的[主題](#topic)清單。每個緩衝區必須提供一個主題。


<!-- vale off -->
### topic
<!-- vale on -->

`topic` 選項會設定單一 Kafka 主題，並告知 `kafka` 緩衝區如何使用該主題。


選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | Kafka 主題的名稱。
`group_id` | 是 | 字串 | 設定 Kafka 的 `group.id` 選項。
`client_id` | 否 | 字串 | 為緩衝區的消費者設定 Kafka 的 `client.id` 選項。長度必須介於 1 到 255 個字元之間。
`create_topic` | 否 | 布林值 | 若為 `true`，緩衝區會在管線啟動時建立主題。預設值為 `false`。
`number_of_partitions` | 否 | 整數 | 建立主題時要使用的分割區數量。僅在 `create_topic` 為 `true` 時適用。預設值為 `1`。
`replication_factor` | 否 | 整數 | 建立主題時要使用的複寫因子。僅在 `create_topic` 為 `true` 時適用。預設值為 `1`。
`workers` | 否 | 整數 | 與每個主題關聯的多執行緒消費者數量。預設值為 `2`。最大值為 `200`。
`encryption_key` | 否 | 字串 | 進階加密標準 (AES) 加密金鑰，用於在 OpenSearch Data Prepper 內將資料傳送至 Kafka 之前加密及解密資料。此值必須為純文字，或使用 AWS Key Management Service (AWS KMS) 加密。
`kms` | 否 | AWS KMS 金鑰 | 設定後，會使用 AWS KMS 金鑰加密資料。如需詳細資訊，請參閱 [`kms`](#kms)。
`encryption_id` | 否 | 字串 | 在 `data-prepper-config.yaml` 檔案的 `encryption` 擴充功能中定義之加密引擎的 ID。緩衝區會使用此加密引擎，在將資料傳送至 Kafka 之前加密及解密資料。請使用 `encryption_id` 或 `encryption_key` 其中之一，不可同時使用兩者。
`auto_commit` | 否 | 布林值 | 若為 `false`，消費者位移將不會在背景定期提交至 Kafka。預設值為 `false`。
`commit_interval` | 否 | 持續時間 | 當 `auto_commit` 設為 `true` 時，透過 Kafka 的 `auto.commit.interval.ms` 選項設定消費者位移自動提交至 Kafka 的頻率。預設值為 `5s`。
`session_timeout` | 否 | 持續時間 | 使用 Kafka 的群組管理功能（可用於平衡資料串流）時，來源偵測用戶端失敗的時間長度。預設值為 `45s`。
`auto_offset_reset` | 否 | 字串 | 透過 Kafka 的 `auto.offset.reset` 選項，自動將位移重設為最早或最新的位移。預設值為 `earliest`。
`thread_waiting_time` | 否 | 持續時間 | 執行緒等待前一個執行緒完成其工作並通知下一個執行緒的時間長度。Kafka 消費者 API 的輪詢逾時值會設為此設定值的一半。預設值為 `5s`。
`max_partition_fetch_bytes` | 否 | 字串 | 透過 Kafka 的 `max.partition.fetch.bytes` 設定，設定從每個分割區傳回的資料量上限。預設值為 `1mb`。
`heart_beat_interval` | 否 | 持續時間 | 透過 Kafka 的 `heartbeat.interval.ms` 設定，在使用 Kafka 的群組管理功能時，傳送至消費者協調器之心跳訊號之間的預期時間間隔。預設值為 `5s`。
`fetch_max_wait` | 否 | 持續時間 | 透過 Kafka 的 `fetch.max.wait.ms` 設定，當資料不足以滿足 `fetch_min_bytes` 要求時，伺服器阻擋擷取請求的最長時間。預設值為 `1000ms`。
`fetch_max_bytes` | 否 | 字串 | 透過 Kafka 的 `fetch.max.bytes` 設定，伺服器針對擷取請求傳回的資料量上限。最大值為 `50mb`。預設值為 `50mb`。
`fetch_min_bytes` | 否 | 字串 | 透過 Kafka 的 `fetch.min.bytes` 設定，伺服器在擷取請求期間傳回的資料量下限。預設值為 `2kb`。
`retry_backoff` | 否 | 持續時間 | 對指定主題分割區重試失敗請求之前要等待的時間長度。預設值為 `10s`。
`reconnect_backoff` | 否 | 持續時間 | 透過 Kafka 的 `reconnect.backoff.ms` 設定，嘗試重新連線至 broker 之前要等待的時間長度。預設值為 `10s`。
`connections_max_idle` | 否 | 持續時間 | 透過 Kafka 的 `connections.max.idle.ms` 設定，緩衝區的消費者在經過此時間長度後關閉閒置連線。若要為生產者設定此值，請使用 [`producer_properties`](#producer_properties) 中的 `connections_max_idle`。預設值為 `540s`。
`metadata_max_age` | 否 | 持續時間 | 透過 Kafka 的 `metadata.max.age.ms` 設定，緩衝區的消費者在經過此時間長度後重新整理中繼資料。若要為生產者設定此值，請使用 [`producer_properties`](#producer_properties) 中的 `metadata_max_age`。預設值為 `300s`。
`max_poll_interval` | 否 | 持續時間 | 透過 Kafka 的 `max.poll.interval.ms` 選項，在使用群組管理時，兩次叫用 `poll()` 之間的最大延遲。預設值為 `300s`。
`consumer_max_poll_records` | 否 | 整數 | 透過 Kafka 的 `max.poll.records` 設定，單次 `poll()` 呼叫傳回的記錄數量上限。預設值為 `500`。
`max_message_bytes` | 否 | 整數 | 訊息的大小上限（以位元組為單位）。預設值為 1 MB。


<!-- vale off -->
### kms
<!-- vale on -->

使用 AWS KMS 時，AWS KMS 金鑰可以解密 `encryption_key`，使其不必以純文字儲存。若要搭配 `kafka` 緩衝區設定 AWS KMS，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`key_id` | 是 | 字串 | AWS KMS 金鑰的 ID。可以是完整的金鑰 ARN 或金鑰別名。
`region` | 否 | 字串 | AWS KMS 金鑰所在的 AWS 區域。
`sts_role_arn` | 否 | 字串 | 用於存取 AWS KMS 金鑰的 AWS Security Token Service (AWS STS) 角色 ARN。
`encryption_context` | 否 | 對應表 | 若有提供，傳送至主題的訊息會將此對應表納入作為 AWS KMS 加密脈絡（encryption context）。


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
`scram` | JSON 物件 | [SCRAM](#sasl-scram) 驗證組態。
`aws_msk_iam` | 字串 | Amazon MSK AWS Identity and Access Management (IAM) 組態。若設定為 `role`，則會使用 `aws` 組態中設定的 `sts_role_arn`。預設值為 `default`。
`azure_federated` | JSON 物件 | 使用聯合至 Microsoft Entra ID 的 AWS 認證資訊，向 Azure Event Hubs 的 Kafka 端點進行驗證的組態。如需詳細資訊，請參閱 [SASL Azure 聯合驗證](#sasl-azure-federated)。

#### SASL PLAINTEXT

使用 [SASL PLAINTEXT](https://kafka.apache.org/10/javadoc/org/apache/kafka/common/security/auth/SecurityProtocol.html) 通訊協定時，必須提供下列選項。

選項 | 類型 | 說明
:--- | :--- | :---
`username` | 字串 | PLAINTEXT 驗證的使用者名稱。
`password` | 字串 | PLAINTEXT 驗證的密碼。

#### SASL SCRAM

使用加鹽挑戰回應驗證機制 (Salted Challenge Response Authentication Mechanism，SCRAM) 時，必須提供下列選項。

選項 | 類型 | 說明
:--- | :--- | :---
`username` | 字串 | 用於 SCRAM 驗證的使用者名稱。
`password` | 字串 | 用於 SCRAM 驗證的密碼。
`mechanism` | 字串 | 要使用的 SCRAM 機制，例如 `SCRAM-SHA-256` 或 `SCRAM-SHA-512`。此值會傳遞至 Kafka 的 `sasl.mechanism` 設定。

#### SASL Azure 同盟驗證

`azure_federated` 選項可將緩衝區連線至 Azure Event Hubs 命名空間的 Kafka 端點，而且不必在管線中儲存 Azure 用戶端密碼。緩衝區會使用 [`aws`](#aws) 組態中的認證資訊，向 AWS STS 請求 Web 身分識別權杖，接著在 Microsoft Entra ID 權杖端點將此權杖交換為存取權杖，再使用該存取權杖進行 SASL/OAUTHBEARER 驗證。緩衝區會快取存取權杖，並在權杖到期前請求新的權杖。

若要使用此選項，請在您的 AWS 帳戶中啟用輸出身分同盟、允許 AWS 認證資訊呼叫 `sts:GetWebIdentityToken`，並在 Microsoft Entra 應用程式中新增信任 AWS 權杖的同盟身分識別認證資訊。請在 `aws.region` 中設定 AWS 區域。若已設定 `aws.sts_role_arn`，緩衝區會先擔任該角色，再請求權杖。連線一律使用 `SASL_SSL` 安全性通訊協定。

使用 `azure_federated` 時，下列選項為必要選項。

選項 | 類型 | 說明
:--- | :--- | :---
`client_id` | 字串 | Microsoft Entra 應用程式的應用程式（用戶端）ID。
`token_endpoint` | 字串 | Microsoft Entra ID OAuth 2.0 權杖端點，例如 `https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token`。
`scope` | 字串 | 所請求存取權杖的範圍。若使用 Azure Event Hubs，請使用 `https://<namespace>.servicebus.windows.net/.default`。

下列範例設定 `azure_federated` 驗證：

```yaml
buffer:
  kafka:
    bootstrap_servers: ["my-namespace.servicebus.windows.net:9093"]
    topics:
      - name: my-buffer-event-hub
        group_id: data-prepper
    encryption:
      type: ssl
    authentication:
      sasl:
        azure_federated:
          client_id: <application-client-id>
          token_endpoint: https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token
          scope: https://my-namespace.servicebus.windows.net/.default
    aws:
      region: us-east-1
      sts_role_arn: arn:aws:iam::123456789012:role/event-hubs-federation
```
{% include copy.html %}

#### 加密

設定 SSL 加密時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`type` | 否 | 字串 | 加密類型。使用 `none` 可停用加密。預設為 `ssl`。
`certificate` | 否 | 字串 | SSL 憑證內容。請使用此選項或 `trust_store_file_path` 其中之一，不可同時使用。
`trust_store_file_path` | 否 | 字串 | 包含 SSL 憑證的信任儲存區（truststore）檔案路徑。請使用此選項或 `certificate` 其中之一，不可同時使用。
`trust_store_password` | 否 | 字串 | 信任儲存區檔案的密碼。
`insecure` | 否 | 布林值 | 用於關閉 SSL 憑證驗證的布林值旗標。若設為 `true`，將關閉憑證授權單位（CA）憑證驗證，並傳送不安全的 HTTP 請求。預設為 `false`。

<!-- vale off -->
#### producer_properties
<!-- vale on -->

使用下列組態選項來設定 Kafka 生產者（producer）。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`acks` | 否 | 字串 | 生產者在認定請求完成之前，需要從 broker 收到的確認數量，對應 Kafka 的 `acks` 設定。有效值為 `all`、`-1`、`0` 和 `1`。若未指定，則使用 Kafka 用戶端的預設值。
`batch_size` | 否 | 整數 | 傳送至同一分割區的一批記錄的大小上限（以位元組為單位），對應 Kafka 的 `batch.size` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`buffer_memory` | 否 | 字串 | 生產者可用於緩衝等待傳送至 Kafka 之記錄的記憶體總量，對應 Kafka 的 `buffer.memory` 設定。預設為 `50mb`。
`client_dns_lookup` | 否 | 字串 | 為生產者設定 Kafka 的 `client.dns.lookup` 選項。有效值為 `use_all_dns_ips` 和 `resolve_canonical_bootstrap_servers_only`。若未指定，則使用 Kafka 用戶端的預設值。
`client_id` | 否 | 字串 | 為生產者設定 Kafka 的 `client.id` 選項。若未指定，則使用 Kafka 用戶端的預設值。
`compression_type` | 否 | 字串 | 生產者所傳送資料的壓縮類型，對應 Kafka 的 `compression.type` 設定，例如 `gzip`、`snappy` 或 `zstd`。當主題使用靜態加密（`encryption_key`、`kms` 或 `encryption_id`）時，緩衝區會在加密資料之前自行壓縮資料，並關閉 Kafka 壓縮。若未指定，則使用 Kafka 用戶端的預設值。
`connections_max_idle` | 否 | 持續時間 | 閒置連線經過多久時間後關閉，對應 Kafka 的 `connections.max.idle.ms` 設定。預設為 `540s`。
`delivery_timeout` | 否 | 持續時間 | 回報傳送請求成功或失敗的最長時間（包含重試），對應 Kafka 的 `delivery.timeout.ms` 設定。預設為 `120s`。
`enable_idempotence` | 否 | 布林值 | 當設為 `true` 時，生產者會將每筆記錄恰好寫入主題一次，對應 Kafka 的 `enable.idempotence` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`interceptor_classes` | 否 | 清單 | Kafka 生產者攔截器的完整類別名稱清單，對應 Kafka 的 `interceptor.classes` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`linger_ms` | 否 | 整數 | 生產者在傳送批次之前等待其他記錄的時間（以毫秒為單位），對應 Kafka 的 `linger.ms` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`max_block` | 否 | 持續時間 | 傳送請求可被阻擋的最長時間，例如當生產者緩衝區已滿或無法取得中繼資料時，對應 Kafka 的 `max.block.ms` 設定。預設為 `60s`。
`max_in_flight_requests_per_connection` | 否 | 整數 | 生產者在單一連線上傳送的未確認請求數量上限，對應 Kafka 的 `max.in.flight.requests.per.connection` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`max_request_size` | 否 | 整數 | 生產者傳送至 Kafka 的請求大小上限（以位元組為單位）。當 `create_topic` 為 `true` 且此值大於預設值時，主題的 `max.message.bytes` 設定也會設為此值。預設為 `1048576`（1 MB）。
`metadata_max_age` | 否 | 持續時間 | 生產者經過多久時間後重新整理中繼資料，對應 Kafka 的 `metadata.max.age.ms` 設定。預設為 `300s`。
`metadata_max_idle` | 否 | 持續時間 | 生產者經過多久時間後捨棄閒置主題的快取中繼資料，對應 Kafka 的 `metadata.max.idle.ms` 設定。預設為 `300s`。
`metric_reporters` | 否 | 清單 | Kafka 指標報告器的完整類別名稱清單，對應 Kafka 的 `metric.reporters` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`metrics_num_samples` | 否 | 整數 | 為計算 Kafka 用戶端指標而保留的樣本數，對應 Kafka 的 `metrics.num.samples` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`metrics_recording_level` | 否 | 字串 | Kafka 用戶端指標的最高記錄層級，對應 Kafka 的 `metrics.recording.level` 設定。有效值為 `INFO`、`DEBUG` 和 `TRACE`。若未指定，則使用 Kafka 用戶端的預設值。
`metrics_sample_window` | 否 | 持續時間 | 計算 Kafka 用戶端指標樣本所用的時間區間，對應 Kafka 的 `metrics.sample.window.ms` 設定。預設為 `300s`。
`partitioner_adaptive_partitioning_enable` | 否 | 布林值 | 當設為 `true` 時，生產者會將更多記錄傳送至位於較快 broker 上的分割區，對應 Kafka 的 `partitioner.adaptive.partitioning.enable` 設定。預設為 `false`。
`partitioner_availability_timeout` | 否 | 持續時間 | 若 broker 在此時間長度內無法處理某個分割區的生產請求，分割器會將該分割區視為無法使用，對應 Kafka 的 `partitioner.availability.timeout.ms` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`partitioner_class` | 否 | 字串 | 決定每筆記錄所屬分割區之分割器的完整類別名稱，對應 Kafka 的 `partitioner.class` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`partitioner_ignore_keys` | 否 | 布林值 | 當設為 `true` 時，生產者在選擇分割區時會忽略記錄索引鍵，對應 Kafka 的 `partitioner.ignore.keys` 設定。若未指定，則使用 Kafka 用戶端的預設值。
`receive_buffer` | 否 | 字串 | TCP 接收緩衝區的大小，對應 Kafka 的 `receive.buffer.bytes` 設定。預設為 `50mb`。
`reconnect_backoff` | 否 | 持續時間 | 嘗試重新連線至 broker 之前等待的時間，對應 Kafka 的 `reconnect.backoff.ms` 設定。預設為 `50ms`。
`reconnect_backoff_max` | 否 | 持續時間 | 重複無法重新連線至 broker 時的最長等待時間，對應 Kafka 的 `reconnect.backoff.max.ms` 設定。預設為 `1s`。
`request_timeout` | 否 | 持續時間 | 生產者等待請求回應的最長時間，對應 Kafka 的 `request.timeout.ms` 設定。預設為 `30s`。
`retries` | 否 | 整數 | 生產者重試傳送因可重試錯誤而失敗之記錄的次數，對應 Kafka 的 `retries` 設定。預設為 `5`。
`retry_backoff` | 否 | 持續時間 | 重試失敗請求之前等待的時間，對應 Kafka 的 `retry.backoff.ms` 設定。預設為 `100ms`。
`send_buffer` | 否 | 字串 | TCP 傳送緩衝區的大小，對應 Kafka 的 `send.buffer.bytes` 設定。預設為 `50mb`。
`socket_connection_setup_timeout` | 否 | 持續時間 | 生產者等待建立通訊端連線的時間，對應 Kafka 的 `socket.connection.setup.timeout.ms` 設定。預設為 `10s`。
`socket_connection_setup_timeout_max` | 否 | 持續時間 | 重複連線失敗時，生產者等待建立通訊端連線的最長時間，對應 Kafka 的 `socket.connection.setup.timeout.max.ms` 設定。預設為 `30s`。


<!-- vale off -->
#### aws
<!-- vale on -->

為 `aws` 服務設定驗證時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於認證資訊的 AWS 區域。預設採用[判斷區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 對 Amazon Simple Queue Service（Amazon SQS）和 Amazon Simple Storage Service（Amazon S3）發出請求時所要擔任的 AWS STS 角色。預設為 `null`，此時會使用[認證資訊的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`msk` | 否 | JSON 物件 | [Amazon MSK](#msk) 組態設定。
`sts_header_overrides` | 否 | 對應表 | 要新增至 AWS STS `AssumeRole` 請求的標頭對應表。您最多可以指定 5 個標頭。

<!-- vale off -->
#### msk
<!-- vale on -->

請在 `msk` 物件中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`arn` | 是 | 字串 | 要使用的 [Amazon MSK ARN](https://docs.aws.amazon.com/msk/1.0/apireference/configurations-arn.html)。
`broker_connection_type` | 否 | 字串 | 與 Amazon MSK broker 搭配使用的連接器類型，可以是 `public`、`single_vpc` 或 `multi_vpc`。預設為 `single_vpc`。
