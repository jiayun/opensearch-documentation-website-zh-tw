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
`bootstrap_servers` | 是，當未使用 Amazon Managed Streaming for Apache Kafka (Amazon MSK) 作為叢集時。 | IP 位址 | 與 Kafka 叢集建立初始連線的主機或連接埠。您可以透過每個 broker 的 IP 位址或連接埠號碼來設定多個 Kafka broker。當使用 [Amazon MSK](https://aws.amazon.com/msk/) 作為您的 Kafka 叢集時，bootstrap 伺服器資訊會透過組態中提供的 MSK Amazon Resource Name (ARN) 從 MSK 取得。
`topics` | 是 | JSON 陣列 | Data Prepper `kafka` 來源用來讀取訊息的 Kafka 主題。您最多可以設定 10 個主題。如需 `topics` 組態選項的詳細資訊，請參閱[主題](#topics)。
`schema` | 否 | JSON 物件 | 結構描述註冊服務組態。如需詳細資訊，請參閱[結構描述](#schema)。
`authentication` | 否 | JSON 物件 | 設定管線與 Kafka 兩者的驗證選項。如需詳細資訊，請參閱[驗證](#authentication)。
`encryption` | 否 | JSON 物件 | 加密組態。如需詳細資訊，請參閱[加密](#encryption)。
`aws` | 否 | JSON 物件 | AWS 組態。如需詳細資訊，請參閱 [aws](#aws)。
`acknowledgments` | 否 | 布林值 | 若為 `true`，則啟用 `kafka` 來源，在 OpenSearch 接收器接收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/#end-to-end-acknowledgments)。預設為 `false`。
`client_dns_lookup` | 是，當使用 DNS 別名時。 | 字串 | 設定 Kafka 的 `client.dns.lookup` 選項。預設為 `default`。

### 主題

請在 `topics` 陣列中對每個主題使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 每個 Kafka 主題的名稱。
`group_id` | 是 | 字串 | 設定 Kafka 的 `group.id` 選項。
`workers` | 否 | 整數 | 與每個主題相關聯的多執行緒消費者數量。預設為 `2`。最大值為 `200`。
`serde_format` | 否 | 字串 | 指示主題中訊息的序列化與反序列化格式。預設為 `plaintext`。
`auto_commit` | 否 | 布林值 | 當為 `false` 時，消費者的偏移量將不會在背景定期提交至 Kafka。預設為 `false`。
`commit_interval` | 否 | 整數 | 當 `auto_commit` 設定為 `true` 時，設定透過 Kafka 的 `auto.commit.interval.ms` 選項將消費者偏移量自動提交至 Kafka 的頻率 (以秒為單位)。預設為 `5s`。
`session_timeout` | 否 | 整數 | 使用 Kafka 的群組管理功能 (可用於平衡資料串流) 時，來源偵測用戶端故障的時間長度。預設為 `45s`。
`auto_offset_reset` | 否 | 字串 | 透過 Kafka 的 `auto.offset.reset` 選項，自動將偏移量重設為較早或最新的偏移量。預設為 `earliest`。
`thread_waiting_time` | 否 | 整數 | 執行緒等待前一個執行緒完成其工作並向下一個執行緒發出訊號的時間長度。Kafka 消費者 API 的 poll 逾時值會設定為此設定值的一半。預設為 `5s`。
`max_partition_fetch_bytes` | 否 | 整數 | 透過 Kafka 的 `max.partition.fetch.bytes` 設定，設定從每個分割區傳回的最大資料量上限 (以 MB 為單位)。預設為 `1mb`。
`heart_beat_interval` | 否 | 整數 | 透過 Kafka 的 `heartbeat.interval.ms` 設定使用 Kafka 的群組管理機制時，對消費者協調器傳送心跳的預期間隔時間。預設為 `5s`。
`fetch_max_wait` | 否 | 整數 | 當資料不足以滿足 `fetch_min_bytes` 需求時，伺服器透過 Kafka 的 `fetch.max.wait.ms` 設定封鎖擷取請求的最長時間。預設為 `500ms`。
`fetch_max_bytes` | 否 | 整數 | broker 透過 Kafka 的 `fetch.max.bytes` 設定接受的最大記錄大小。預設為 `50mb`。
`fetch_min_bytes` | 否 | 整數 | 伺服器在擷取請求期間透過 Kafka 的 `retry.backoff.ms` 設定傳回的最小資料量。預設為 `1b`。
`retry_backoff` | 否 | 整數 | 重試對指定主題分割區之失敗請求前的等待時間。預設為 `10s`。
`max_poll_interval` | 否 | 整數 | 透過 Kafka 的 `max.poll.interval.ms` 選項使用群組管理時，兩次 `poll()` 呼叫之間的最大延遲。預設為 `300s`。
`consumer_max_poll_records` | 否 | 整數 | 透過 Kafka 的 `max.poll.records` 設定，單次 `poll()` 呼叫傳回的最大記錄數。預設為 `500`。
`key_mode` | 否 | 字串 | 指示應如何處理 Kafka 訊息的 key 欄位。預設設定為 `include_as_field`，會將 key 包含在 `kafka_key` 事件中。`include_as_metadata` 設定會將 key 包含在事件的中繼資料中。`discard` 設定則會捨棄 key。

### 結構描述

`schema` 組態具有下列選項。

選項 | 類型 | 必要 | 說明
:--- | :--- | :--- | :---
`type` | 字串 | 是 | 根據您的註冊服務設定結構描述類型。有效值為 `aws_glue` (AWS Glue 結構描述註冊服務) 與 `confluent` (Confluent 結構描述註冊服務)。使用 `aws_glue` 註冊服務時，請設定任何 [AWS](#aws) 組態選項。
`basic_auth_credentials_source` | 字串 | 否 | 結構描述註冊服務憑證的來源。提供 `api_key/api_secret` 時請使用 `USER_INFO`。其他有效值為 `URL` 與 `SASL_INHERIT`。預設值通常與底層用戶端一致。

下列組態選項僅在使用 `confluent` 註冊服務時才需要。

選項 | 類型 | 說明
:--- | :--- | :---
`registry_url` | 字串 | 結構描述註冊服務的基礎 URL (例如 `http://schema-registry:8081` 或 `https://sr.example.com`)。
`version` | 字串 | 每個主體要使用的結構描述版本。請使用整數或 `latest`。
`api_key` | 字串 | 結構描述註冊服務的 API 金鑰。
`api_secret` | 字串 | 結構描述註冊服務的 API 密鑰。

下列範例設定結構描述註冊服務：

```yaml
schema:
  type: confluent
  registry_url: "http://schema-registry:8081"
  api_key: "<optional if using basic/key auth>"
  api_secret: "<optional if using basic/key auth>"
  version: "latest"
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
`plaintext` | JSON 物件 | 純文字驗證組態。為了回溯相容性，也支援別名 `plain`。如需詳細資訊，請參閱 [SASL 純文字](#sasl-plaintext)。
`aws_msk_iam` | 字串 | Amazon MSK AWS Identity and Access Management (IAM) 組態。若設定為 `role`，則會使用 `aws` 組態中設定的 `sts_role_arm`。預設為 `default`。

##### SASL 純文字

使用 [SASL.plain](https://kafka.apache.org/10/javadoc/org/apache/kafka/common/security/auth/SecurityProtocol.html) 通訊協定時，下列選項為必要選項。

| 選項 | 類型 | 說明 |
|:---|:---|:---|
| `username` | 字串 | SASL/PLAIN 使用者名稱。 |
| `password` | 字串 | SASL/PLAIN 密碼。 |

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
`region` | 否 | 字串 | 用於認證資訊的 AWS 區域。預設依照[標準 SDK 行為決定區域](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。
`sts_role_arn` | 否 | 字串 | 向 Amazon Simple Queue Service (Amazon SQS) 和 Amazon Simple Storage Service (Amazon S3) 發出請求時所擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，此時將使用[標準 SDK 認證資訊行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。
`msk` | 否 | JSON 物件 | [MSK](#msk) 組態設定。

#### MSK

請在 `msk` 物件中使用下列選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`arn` | 是 | 字串 | 要使用的 [MSK ARN](https://docs.aws.amazon.com/msk/1.0/apireference/configurations-arn.html)。
`broker_connection_type` | 否 | 字串 | 與 MSK 訊息代理 (broker) 搭配使用的連接器類型。有效值為 `public`、`single_vpc` 和 `multip_vpc`。預設為 `single_vpc`。

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
        password: admin_password
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
        password: admin_password
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
        password: admin_password
        index: authenticated-kafka-data
```
{% include copy.html %}

### 搭配 AWS Glue 結構描述註冊服務的 Amazon MSK

下列範例會設定搭配 AWS Glue 結構描述註冊服務的 Amazon MSK：使用 AWS 設定從 MSK 叢集取用訊息，使用 AWS Glue 結構描述註冊服務將酬載反序列化，正規化時間戳記，並寫入 Amazon OpenSearch 網域：

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
        registry_name: my-glue-registry
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

### 搭配結構描述註冊服務的 Confluent Kafka

下列範例會設定搭配結構描述註冊服務的 Confluent Kafka，使用 SASL 與 Confluent 結構描述註冊服務憑證透過 TLS 連線至 Confluent Cloud，解碼酬載，並將其編製索引至 OpenSearch：

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
        password: admin_password
        index_type: custom
        index: confluent-data
```
{% include copy.html %}

