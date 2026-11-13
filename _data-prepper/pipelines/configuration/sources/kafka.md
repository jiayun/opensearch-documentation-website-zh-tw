---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Kafka
parent: Sources
grand_parent: Pipelines
nav_order: 40
---

# Kafka 來源

您可以在 OpenSearch Data Prepper 中使用 Apache Kafka 來源 (`kafka`)，從一或多個 Kafka [主題](https://kafka.apache.org/intro#intro_concepts_and_terms) 讀取記錄。這些記錄包含您的 Data Prepper 管線可以匯入的事件。`kafka` 來源使用 Kafka 的 [Consumer API](https://kafka.apache.org/documentation/#consumerapi) 從 Kafka broker 取用訊息，然後建立 Data Prepper 事件，供 Data Prepper 管線進一步處理。

## 用法

下列範例顯示 Data Prepper 管線中的 `kafka` 來源：

```yaml
kafka-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - 127.0.0.1:9092
      topics:
        - name: Topic1
          group_id: groupID1
        - name: Topic2
          group_id: groupID1
  sink:
    - stdout: {}
```

## 組態

請搭配 `kafka` 來源使用下列組態選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`bootstrap_servers` | 是，當未使用 Amazon Managed Streaming for Apache Kafka (Amazon MSK) 作為叢集時。 | IP 位址 | 初始連線至 Kafka 叢集時使用的主機或連接埠。您可以使用每個 broker 的 IP 位址或連接埠號碼，設定多個 Kafka broker。使用 [Amazon MSK](https://aws.amazon.com/msk/) 作為 Kafka 叢集時，系統會使用組態中提供的 MSK Amazon Resource Name (ARN)，從 MSK 取得啟動伺服器 (bootstrap server) 資訊。
`topics` | 是 | JSON 陣列 | Data Prepper `kafka` 來源用來讀取訊息的 Kafka 主題。您最多可以設定 10 個主題。如需 `topics` 組態選項的詳細資訊，請參閱[主題](#topics)。
`schema` | 否 | JSON 物件 | 結構描述註冊表 (schema registry) 組態。如需詳細資訊，請參閱[結構描述](#schema)。
`authentication` | 否 | JSON 物件 | 為管線與 Kafka 設定驗證選項。如需詳細資訊，請參閱[驗證](#authentication)。
`encryption` | 否 | JSON 物件 | 加密組態。如需詳細資訊，請參閱[加密](#encryption)。
`aws` | 否 | JSON 物件 | AWS 組態。如需詳細資訊，請參閱 [aws](#aws)。
`acknowledgments` | 否 | 布林值 | 若為 `true`，則啟用 `kafka` 來源，使其在 OpenSearch 接收器收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/#end-to-end-acknowledgments)。預設為 `false`。
`acknowledgments_timeout` | 否 | 持續時間 | 等待從 Kafka 讀取之記錄的端對端確認的最長時間。僅在 `acknowledgments` 為 `true` 時適用。若記錄未在此時間內獲得確認，則不會提交其位移 (offset)。根據預設，確認實際上永遠不會逾時。
`acknowledgments_expiry_reset` | 否 | 布林值 | 若為 `true`，在所有事件獲得確認之前即已過期的確認集合會被視為否定確認，因此來源會將受影響的分割區倒回 (seek) 至最後提交的位移，並重新讀取這些記錄。若為 `false`，則會忽略已過期的確認集合。僅在 `acknowledgments` 為 `true` 時適用。預設為 `false`。
`client_dns_lookup` | 是，當使用 DNS 別名時。 | 字串 | 設定 Kafka 的 `client.dns.lookup` 選項。預設為 `default`。

### 主題

請在 `topics` 陣列中，為每個主題使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 每個 Kafka 主題的名稱。
`group_id` | 是 | 字串 | 設定 Kafka 的 `group.id` 選項。
`client_id` | 否 | 字串 | 為主題的取用者設定 Kafka 的 `client.id` 選項。長度必須介於 1 到 255 個字元之間。
`workers` | 否 | 整數 | 與每個主題相關聯的多執行緒取用者數量。預設值為 `2`。最大值為 `200`。
`serde_format` | 否 | 字串 | 指出主題中訊息的序列化與還原序列化格式。預設值為 `plaintext`。
`auto_commit` | 否 | 布林值 | 若為 `false`，取用者的位移不會在背景中定期認可至 Kafka。預設值為 `false`。
`commit_interval` | 否 | 持續時間 | 當 `auto_commit` 設為 `true` 時，透過 Kafka 的 `auto.commit.interval.ms` 選項，設定取用者位移自動認可至 Kafka 的頻率。預設值為 `5s`。
`session_timeout` | 否 | 持續時間 | 使用 Kafka 的群組管理功能時，來源偵測用戶端故障的時間長度；群組管理功能可用於平衡資料串流。預設值為 `45s`。
`auto_offset_reset` | 否 | 字串 | 透過 Kafka 的 `auto.offset.reset` 選項，自動將位移重設為較早的位移或最新的位移。預設值為 `earliest`。
`thread_waiting_time` | 否 | 持續時間 | 執行緒等待前一個執行緒完成其工作並通知下一個執行緒的時間長度。Kafka 取用者 API 的輪詢逾時值會設為此設定的一半。預設值為 `5s`。
`max_partition_fetch_bytes` | 否 | 字串 | 透過 Kafka 的 `max.partition.fetch.bytes` 設定，設定從每個分割區傳回的資料量上限。預設值為 `1mb`。
`heart_beat_interval` | 否 | 持續時間 | 透過 Kafka 的 `heartbeat.interval.ms` 設定，在使用 Kafka 的群組管理功能時，傳送至取用者協調器的兩次活動訊號之間的預期時間長度。預設值為 `5s`。
`fetch_max_wait` | 否 | 整數 | 透過 Kafka 的 `fetch.max.wait.ms` 設定，在資料不足以滿足 `fetch_min_bytes` 要求時，伺服器封鎖擷取請求的最長時間（以毫秒為單位）。預設值為 `500`。
`fetch_max_bytes` | 否 | 字串 | 透過 Kafka 的 `fetch.max.bytes` 設定，伺服器針對擷取請求傳回的資料量上限。最大值為 `50mb`。預設值為 `50mb`。
`fetch_min_bytes` | 否 | 字串 | 透過 Kafka 的 `fetch.min.bytes` 設定，伺服器在擷取請求期間傳回的資料量下限。預設值為 `1b`。
`retry_backoff` | 否 | 持續時間 | 重試對指定主題分割區的失敗請求之前所等待的時間長度。預設值為 `10s`。
`reconnect_backoff` | 否 | 持續時間 | 透過 Kafka 的 `reconnect.backoff.ms` 設定，嘗試重新連線至代理程式 (broker) 之前所等待的時間長度。預設值為 `10s`。
`connections_max_idle` | 否 | 持續時間 | 透過 Kafka 的 `connections.max.idle.ms` 設定，經過此時間長度後，取用者會關閉閒置連線。最小值為 `1s`。預設值為 `540s`。
`metadata_max_age` | 否 | 持續時間 | 透過 Kafka 的 `metadata.max.age.ms` 設定，經過此時間長度後，取用者會重新整理中繼資料。取用者會在重新整理中繼資料時偵測新的分割區。預設值為 `300s`。
`max_poll_interval` | 否 | 持續時間 | 透過 Kafka 的 `max.poll.interval.ms` 選項，在使用群組管理時，兩次呼叫 `poll()` 之間的最大延遲。預設值為 `300s`。
`consumer_max_poll_records` | 否 | 整數 | 透過 Kafka 的 `max.poll.records` 設定，單次 `poll()` 呼叫所傳回的記錄數量上限。預設值為 `500`。
`isolation_level` | 否 | 字串 | 透過 Kafka 的 `isolation.level` 設定，控制取用者如何讀取以交易方式寫入的訊息。有效值為 `read_uncommitted`（傳回所有訊息）以及 `read_committed`（僅傳回已認可交易中的訊息）。預設值為 `read_uncommitted`。
`key_mode` | 否 | 字串 | 指出應如何處理 Kafka 訊息的索引鍵欄位。預設設定為 `include_as_field`，會將索引鍵包含在 `kafka_key` 事件中。`include_as_metadata` 設定會將索引鍵包含在事件的中繼資料中。`discard` 設定會捨棄索引鍵。

### 結構描述

`schema` 組態具有下列選項。

選項 | 類型 | 必要 | 說明
:--- | :--- | :--- | :---
`type` | 字串 | 是 | 根據您的登錄檔設定結構描述類型。有效值為 `aws_glue`（AWS Glue 結構描述登錄檔）及 `confluent`（Confluent 結構描述登錄檔）。使用 `aws_glue` 登錄檔時，請設定所有 [AWS](#aws) 組態選項。
`override_endpoint` | 布林值 | 否 | 當 `true` 且 `type` 為 `aws_glue` 時，`kafka` 來源會使用 `registry_url` 作為 AWS Glue 結構描述登錄檔端點。預設值為 `false`。
`basic_auth_credentials_source` | 字串 | 否 | 結構描述登錄檔認證資訊的來源。提供 `api_key/api_secret` 時，請使用 `USER_INFO`。其他有效值為 `URL` 及 `SASL_INHERIT`。預設值通常與底層用戶端一致。

只有在使用 `confluent` 登錄檔時，才需要下列組態選項。

選項 | 類型 | 說明
:--- | :--- | :---
`registry_url` | 字串 | 結構描述登錄檔的基礎 URL（例如 `http://schema-registry:8081` 或 `https://sr.example.com`）。
`version` | 整數 | 每個主體（subject）所使用的結構描述版本。若未指定，則使用最新版本。
`api_key` | 字串 | 結構描述登錄檔的 API 金鑰。
`api_secret` | 字串 | 結構描述登錄檔的 API 密鑰。

下列範例設定結構描述登錄檔：

```yaml
schema:
  type: confluent
  registry_url: "http://schema-registry:8081"
  api_key: "<optional if using basic/key auth>"
  api_secret: "<optional if using basic/key auth>"
```
{% include copy.html %}

#### 透過 TLS 連線至結構描述註冊服務

Kafka 來源透過 `https` 連線至結構描述註冊服務時，會使用 JVM 信任存放區 (truststore)。如果結構描述註冊服務是由自訂 CA 簽署，請將該 CA 新增至 Data Prepper JVM 信任存放區，或使用環境變數提供自訂信任存放區。

您可以使用下列命令，以您的 CA 憑證建置信任存放區：

```bash
keytool -importcert -noprompt -alias sr-ca -file sr-ca.pem -keystore /usr/share/data-prepper/certs/sr.truststore.jks -storepass changeit
```
{% include copy.html %}

下列命令使用 `JAVA_TOOL_OPTIONS` 設定 Data Prepper：

```yaml
JAVA_TOOL_OPTIONS=-Djavax.net.ssl.trustStore=/usr/share/data-prepper/certs/sr.truststore.jks -Djavax.net.ssl.trustStorePassword=changeit
```
{% include copy.html %}

您可以使用下列方法在 `docker-compose.yaml` 中設定 Data Prepper：

```yaml
environment:
  - JAVA_TOOL_OPTIONS=-Djavax.net.ssl.trustStore=/usr/share/data-prepper/certs/sr.truststore.jks -Djavax.net.ssl.trustStorePassword=changeit
volumes:
  - ./certs:/usr/share/data-prepper/certs:ro
```
{% include copy.html %}

### 驗證

`authentication` 區段用於設定 SASL：

```yaml
authentication:
  sasl:
    plaintext:
      username: alice
      password: secret
```
{% include copy.html %}

| 選項 | 類型 | 說明 |
|:---|:---|:---|
| `sasl` | 物件 | SASL 組態。 |

#### SASL

設定 SASL 驗證時，請使用下列其中一個選項。

選項 | 類型 | 說明
:--- | :--- | :---
`plaintext` | JSON 物件 | 純文字驗證組態。為了回溯相容性，也支援別名 `plain`。如需更多資訊，請參閱 [SASL 純文字](#sasl-plaintext)。
`scram` | JSON 物件 | Salted Challenge Response Authentication Mechanism (SCRAM) 驗證組態。如需更多資訊，請參閱 [SASL SCRAM](#sasl-scram)。
`aws_msk_iam` | 字串 | Amazon MSK AWS Identity and Access Management (IAM) 組態。若設為 `role`，則會使用 `aws` 組態中設定的 `sts_role_arn`。預設值為 `default`。
`azure_federated` | JSON 物件 | 使用聯合至 Microsoft Entra ID 的 AWS 認證資訊，向 Azure Event Hubs 的 Kafka 端點進行驗證的組態。如需更多資訊，請參閱 [SASL Azure 聯合驗證](#sasl-azure-federated)。

##### SASL 純文字

使用 [SASL.plain](https://kafka.apache.org/10/javadoc/org/apache/kafka/common/security/auth/SecurityProtocol.html) 通訊協定時，下列選項為必要選項。

| 選項 | 類型 | 說明 |
|:---|:---|:---|
| `username` | 字串 | SASL/PLAIN 使用者名稱。 |
| `password` | 字串 | SASL/PLAIN 密碼。 |

##### SASL SCRAM

使用 SCRAM 驗證時，必須提供下列選項。

| 選項 | 類型 | 說明 |
|:---|:---|:---|
| `username` | 字串 | SCRAM 使用者名稱。 |
| `password` | 字串 | SCRAM 密碼。 |
| `mechanism` | 字串 | 要使用的 SCRAM 機制，例如 `SCRAM-SHA-256` 或 `SCRAM-SHA-512`。此值會傳遞至 Kafka 的 `sasl.mechanism` 設定。 |

##### SASL Azure 聯合驗證

`azure_federated` 選項可將來源連線至 Azure Event Hubs 命名空間的 Kafka 端點，而不需在管線中儲存 Azure 用戶端密碼。來源會使用 [`aws`](#aws) 組態中的認證資訊，向 AWS STS 請求 Web 身分識別權杖，接著在 Microsoft Entra ID 權杖端點將此權杖交換為存取權杖，並使用該存取權杖進行 SASL/OAUTHBEARER 驗證。來源會快取存取權杖，並在其到期前請求新的存取權杖。

若要使用此選項，請在您的 AWS 帳戶中啟用輸出身分識別聯合，允許 AWS 認證資訊呼叫 `sts:GetWebIdentityToken`，並在 Microsoft Entra 應用程式中新增信任 AWS 權杖的聯合身分識別認證資訊。來源會使用 `aws.region` 中設定的區域；若已設定 `aws.sts_role_arn`，來源會先擔任該角色，再請求權杖。此連線一律使用 `SASL_SSL` 安全性通訊協定。

使用 `azure_federated` 時，下列選項為必要選項。

| 選項 | 類型 | 說明 |
|:---|:---|:---|
| `client_id` | 字串 | Microsoft Entra 應用程式的應用程式（用戶端）ID。 |
| `token_endpoint` | 字串 | Microsoft Entra ID OAuth 2.0 權杖端點，例如 `https://login.microsoftonline.com/<tenant-id>/oauth2/v2.0/token`。 |
| `scope` | 字串 | 所請求存取權杖的範圍。若為 Azure Event Hubs，請使用 `https://<namespace>.servicebus.windows.net/.default`。 |

下列範例設定 `azure_federated` 驗證：

```yaml
kafka-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - my-namespace.servicebus.windows.net:9093
      topics:
        - name: my-event-hub
          group_id: data-prepper-group
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
  sink:
    - stdout: {}
```
{% include copy.html %}

### 加密

設定 SSL 加密時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`type` | 否 | 字串 | 加密類型。使用 `none` 可停用加密。預設為 `ssl`。
`certificate` | 否 | 字串 | SSL 憑證內容。請使用此選項或 `trust_store_file_path` 其中之一，不可同時使用。
`trust_store_file_path` | 否 | 字串 | 包含 SSL 憑證的信任存放區檔案路徑。請使用此選項或 `certificate` 其中之一，不可同時使用。
`trust_store_password` | 否 | 字串 | 信任存放區檔案的密碼。
`insecure` | 否 | 布林值 | 用於關閉 SSL 憑證驗證的布林值旗標。若設定為 `true`，則會關閉憑證授權單位 (CA) 憑證驗證，並傳送不安全的 HTTP 請求。預設為 `false`。

使用下列組態啟用 SSL 加密：

```yaml
encryption:
  type: ssl
  # With public CA: no extra config needed.
  # With private CA: trust using JVM truststore.
```
{% include copy.html %}

### AWS

為 `aws` 服務設定驗證時，請使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`region` | 否 | 字串 | 用於認證資訊的 AWS 區域。預設依照[標準 SDK 行為來判斷區域](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 向 Amazon Simple Queue Service (Amazon SQS) 和 Amazon Simple Storage Service (Amazon S3) 發出請求時，要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，此時會使用[標準 SDK 的認證資訊行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`msk` | 否 | JSON 物件 | [MSK](#msk) 組態設定。
`sts_header_overrides` | 否 | 對應 | 要加入 AWS STS `AssumeRole` 請求的標頭對應。您最多可以指定 5 個標頭。

#### MSK

請在 `msk` 物件中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`arn` | 是 | 字串 | 要使用的 [MSK ARN](https://docs.aws.amazon.com/msk/1.0/apireference/configurations-arn.html)。
`broker_connection_type` | 否 | 字串 | 要搭配 MSK 代理伺服器 (broker) 使用的連接器類型。有效值為 `public`、`single_vpc` 和 `multi_vpc`。預設為 `single_vpc`。

## 組態範例

本節示範不同的管線組態選項。

### 基本 Kafka 來源

下列範例管線會使用多個取用者工作程序，從單一純文字 Kafka 主題讀取 JSON 訊息、加以剖析，並將其編製索引至 OpenSearch：

```yaml
kafka-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - localhost:9092
      topics:
        - name: my-topic
          group_id: data-prepper-group
          workers: 4
  processor:
    - parse_json:
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        username: admin
        password: "<custom-admin-password>"
        index: kafka-data
```
{% include copy.html %}

### 使用 SSL 加密的 Kafka 來源

下列範例管線會透過 TLS 連線至 Kafka 訊息代理，從安全主題取用訊息，並將結果寫入 OpenSearch：

```yaml
kafka-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - kafka-broker.example.com:9093
      topics:
        - name: secure-topic
          group_id: secure-group
      encryption:
        type: ssl
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        username: admin
        password: "<custom-admin-password>"
        index: secure-kafka-data
```
{% include copy.html %}

### 使用 SASL PLAIN 驗證的 Kafka 來源

下列範例管線會透過 TLS 使用 SASL/PLAIN 通訊協定向 Kafka 進行驗證，從主題取用訊息，並將其編製索引至 OpenSearch：

```yaml
kafka-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - kafka-broker.example.com:9094
      topics:
        - name: authenticated-topic
          group_id: auth-group
      encryption:
        type: ssl
      authentication:
        sasl:
          plaintext:
            username: kafka-user
            password: kafka-password
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        username: admin
        password: "<custom-admin-password>"
        index: authenticated-kafka-data
```
{% include copy.html %}

### 搭配 AWS Glue 結構描述登錄檔的 Amazon MSK

下列範例設定 Amazon MSK 搭配 AWS Glue 結構描述登錄檔：使用 AWS 設定從 MSK 叢集取用訊息，使用 AWS Glue 結構描述登錄檔將承載還原序列化，將時間戳記正規化，並寫入 Amazon OpenSearch 網域：

```yaml
msk-pipeline:
  source:
    kafka:
      acknowledgments: true
      topics:
        - name: my-msk-topic
          group_id: msk-consumer-group
          auto_offset_reset: earliest
      aws:
        region: us-east-1
        sts_role_arn: arn:aws:iam::123456789012:role/data-prepper-role
        msk:
          arn: arn:aws:kafka:us-east-1:123456789012:cluster/my-cluster-name/uuid
      schema:
        type: aws_glue
  processor:
    - date:
        match:
          - key: timestamp
            patterns: ["epoch_milli"]
        destination: "@timestamp"
  sink:
    - opensearch:
        hosts: ["https://search-my-domain.us-east-1.opensearch.amazonaws.com"]
        aws:
          region: us-east-1
          sts_role_arn: arn:aws:iam::123456789012:role/opensearch-role
        index: msk-data
        index_type: custom
```
{% include copy.html %}

### 搭配 schema registry 的 Confluent Kafka

下列範例設定搭配 schema registry 的 Confluent Kafka，使用 SASL 與 Confluent schema registry 認證資訊，透過 TLS 連線至 Confluent Cloud、解碼酬載，並將其編製索引至 OpenSearch：

```yaml
confluent-pipeline:
  source:
    kafka:
      bootstrap_servers:
        - pkc-xxxxx.us-east-1.aws.confluent.cloud:9092
      topics:
        - name: confluent-topic
          group_id: confluent-group
          auto_offset_reset: earliest
      encryption:
        type: ssl
      authentication:
        sasl:
          plaintext:
            username: confluent-api-key
            password: confluent-api-secret
      schema:
        type: confluent
        registry_url: https://psrc-xxxxx.us-east-1.aws.confluent.cloud
        api_key: "{% raw %}${{aws_secrets:schema-secret:schema_registry_api_key}}{% endraw %}"
        api_secret: "{% raw %}${{aws_secrets:schema-secret:schema_registry_api_secret}}{% endraw %}"
        basic_auth_credentials_source: USER_INFO
  sink:
    - opensearch:
        hosts: ["https://localhost:9200"]
        username: admin
        password: "<custom-admin-password>"
        index_type: custom
        index: confluent-data
```
{% include copy.html %}

