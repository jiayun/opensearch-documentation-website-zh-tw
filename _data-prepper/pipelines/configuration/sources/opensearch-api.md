---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: OpenSearch API
parent: Sources
grand_parent: Pipelines
nav_order: 55
---

# OpenSearch API 來源

`opensearch_api` 來源接受與 [OpenSearch Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 相容的 HTTP 請求。標準 OpenSearch 用戶端（例如 [Apache Flink OpenSearch Connector](https://nightlies.apache.org/flink/flink-docs-stable/docs/connectors/datastream/opensearch/)、Logstash 及 [`opensearch-py`]({{site.url}}{{site.baseurl}}/clients/python-low-level/)）可透過此來源將資料傳送至 Data Prepper。

與 OpenSearch Bulk API 不同，此來源以非同步方式寫入。事件會先緩衝以供下游處理，而非直接寫入 OpenSearch。使用 `zero` 緩衝區時，事件會直接傳遞至接收器。無論緩衝區類型為何，回應皆為合成的，並不反映 OpenSearch 的實際索引結果。

## 使用方式

`opensearch_api` 來源支援下列端點：

```json
POST /{path}/_bulk
POST /{path}/{index}/_bulk
```

## 組態

下表列出 `opensearch_api` 來源的組態選項。

| 參數 | 類型 | 必要 | 預設 | 說明 |
|-----------|------|----------|---------|-------------|
| `port` | 整數 | 否 | `9200` | 來源接聽的連接埠。必須介於 0--65535。 |
| `path` | 字串 | 否 | `/` | 端點的 URI 路徑。必須以 `/` 開頭。支援 `${pipelineName}` 預留位置。 |
| `request_timeout` | 整數 | 否 | `10000` | 請求逾時，單位為毫秒。 |
| `thread_count` | 整數 | 否 | `200` | 排程執行緒集區中的執行緒數目。 |
| `max_connection_count` | 整數 | 否 | `500` | 開啟連線數上限。 |
| `max_pending_requests` | 整數 | 否 | `1024` | 工作佇列中的工作數上限。 |
| `health_check_service` | 布林值 | 否 | `false` | 在設定的連接埠上啟用 `/health` 端點。 |
| `unauthenticated_health_check` | 布林值 | 否 | `false` | 若為 `true`，健康狀態端點不需要驗證。 |
| `compression` | 字串 | 否 | `none` | 套用至請求承載的壓縮。有效值為 `none` 與 `gzip`。 |
| `authentication` | 物件 | 否 | 未驗證 | 驗證組態。請參閱[驗證](#authentication)。 |
| `ssl` | 布林值 | 否 | `false` | 啟用 TLS/SSL。 |
| `ssl_certificate_file` | 字串 | 視情況而定 | — | SSL 憑證檔案的路徑。若 `ssl` 為 `true` 且 `use_acm_certificate_for_ssl` 為 `false`，則為必要。支援 Amazon Simple Storage Service (Amazon S3) 路徑 (`s3://bucket/path`)。 |
| `ssl_key_file` | 字串 | 視情況而定 | — | SSL 金鑰檔案的路徑（已解密）。若 `ssl` 為 `true` 且 `use_acm_certificate_for_ssl` 為 `false`，則為必要。支援 Amazon S3 路徑。 |
| `use_acm_certificate_for_ssl` | 布林值 | 否 | `false` | 若為 `true`，則使用 AWS Certificate Manager (ACM) 取得 TLS 憑證。 |
| `acm_certificate_arn` | 字串 | 視情況而定 | — | ACM 憑證的 Amazon Resource Name (ARN)。若 `use_acm_certificate_for_ssl` 為 `true`，則為必要。 |
| `acm_private_key_password` | 字串 | 否 | 隨機 | 用於解密 ACM 私密金鑰的密碼。 |
| `acm_certificate_timeout_millis` | 整數 | 否 | `120000` | 擷取 ACM 憑證的逾時，單位為毫秒。 |
| `aws_region` | 字串 | 視情況而定 | — | 用於存取 ACM 或 Amazon S3 憑證的 AWS 區域。 |

## 驗證

根據預設，此來源在沒有驗證的情況下執行。若要在組態中明確表示，請使用 `unauthenticated` 索引鍵：

```yaml
source:
  opensearch_api:
    authentication:
      unauthenticated:
```
{% include copy.html %}

### HTTP 基本驗證

下列範例使用使用者名稱與密碼設定 HTTP 基本驗證：

```yaml
source:
  opensearch_api:
    authentication:
      http_basic:
        username: my-user
        password: my_s3cr3t
```
{% include copy.html %}

### 自訂驗證

若要提供自訂驗證，請建立實作 [`ArmeriaHttpAuthenticationProvider`](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-plugins/armeria-common/src/main/java/org/opensearch/dataprepper/armeria/authentication/ArmeriaHttpAuthenticationProvider.java) 介面的外掛程式。

## 事件中繼資料屬性

對於大量請求中的每個動作，來源會建立具有下列中繼資料屬性的 Data Prepper 事件。

| 屬性 | 說明 | 範例 |
|-----------|-------------|---------|
| `opensearch_action` | 大量動作類型 | `index`、`create`、`update`、`delete` |
| `opensearch_index` | 目標索引名稱 | `my-index` |
| `opensearch_id` | 文件 ID（若有提供） | `doc-123` |
| `opensearch_routing` | 路由值（若有提供） | `user-456` |
| `opensearch_pipeline` | 資料匯入管線（若有提供） | `my-pipeline` |

您可以使用 `getMetadata` 方法或 `${metadata_key}` 語法，在處理器與接收器中參照這些屬性。

## 回應格式

成功時，來源會傳回含有空 `items` 陣列的 JSON 回應：

```json
{
  "took": 5,
  "errors": false,
  "items": []
}
```

下表列出回應欄位。

| 欄位 | 說明 |
|-------|-------------|
| `took` | 實際處理時間，從收到請求到完成緩衝區寫入為止，單位為毫秒。 |
| `errors` | 指出是否發生任何錯誤。當所有資料都成功寫入緩衝區時，一律為 `false`。 |
| `items` | 一律為空陣列。由於 Data Prepper 會緩衝文件以供下游處理，而非直接編製索引，因此請求時無法取得個別項目的結果。 |

## 回應狀態碼

下表列出可能的回應狀態碼。

| 狀態 | 說明 |
|--------|-------------|
| `200` | 請求資料已成功寫入緩衝區。 |
| `400` | 請求資料格式錯誤或使用不支援的格式。 |
| `408` | 請求寫入緩衝區時逾時。 |
| `413` | 請求承載超過設定的緩衝區容量。 |
| `429` | 來源已達容量上限；請求遭拒。 |

## 緩衝區相容性

`opensearch_api` 來源可搭配下列緩衝區類型使用。

| 緩衝區 | 支援 | 備註 |
|--------|-----------|-------|
| [`bounded_blocking`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/bounded-blocking/) | 是 | 預設。事件會儲存在記憶體內封鎖佇列中。 |
| [`kafka`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/buffers/kafka/) | 是 | 需要 Data Prepper 2.x。事件會序列化至 Apache Kafka，並在取用端重建。 |
| `zero` | 是 | 事件會直接傳遞至接收器，不進行緩衝。 |

## 指標

`opensearch_api` 來源會發出下列指標。

### 計數器

下表列出計數器指標。

| 指標 | 說明 |
|--------|-------------|
| `requestsReceived` | 端點收到的請求總數。 |
| `successRequests` | 成功處理的請求總數 (200)。 |
| `badRequests` | 格式無效的請求總數 (400)。 |
| `requestTimeouts` | 逾時的請求總數 (408)。 |
| `requestsTooLarge` | 超過緩衝區容量的請求總數 (413)。 |
| `requestsRejected` | 因容量已滿而遭拒的請求總數 (429)。 |
| `internalServerError` | 發生內部錯誤的請求總數 (500)。 |

### 計時器

下表列出計時器指標。

| 指標 | 說明 |
|--------|-------------|
| `requestProcessDuration` | 請求處理延遲，單位為秒。 |

### 分佈摘要

下表列出分佈摘要指標。

| 指標 | 說明 |
|--------|-------------|
| `payloadSize` | 傳入請求承載大小的分佈，單位為位元組。 |

## 範例

下列範例示範 `opensearch_api` 來源的常見組態。

### 搭配 OpenSearch 接收器的基本管線

下列範例設定一個管線，用於接收大量請求，並使用中繼資料屬性將事件寫入 OpenSearch 接收器：

```yaml
opensearch-pipeline:
  source:
    opensearch_api:
      port: 9202
      path: "/opensearch"
  sink:
    - opensearch:
        hosts: ["https://opensearch-node:9200"]
        index: "${getMetadata(\"opensearch_index\")}"
        document_id: "${getMetadata(\"opensearch_id\")}"
        routing: "${getMetadata(\"opensearch_routing\")}"
        action: "${getMetadata(\"opensearch_action\")}"
```
{% include copy.html %}

### 已啟用 SSL

下列範例使用 HTTP 基本驗證啟用 SSL：

```yaml
opensearch-pipeline:
  source:
    opensearch_api:
      port: 9202
      ssl: true
      ssl_certificate_file: "/certs/server.crt"
      ssl_key_file: "/certs/server.key"
      authentication:
        http_basic:
          username: admin
          password: admin
  sink:
    - opensearch:
        hosts: ["https://opensearch-node:9200"]
        index: "${getMetadata(\"opensearch_index\")}"
        action: "${getMetadata(\"opensearch_action\")}"
```
{% include copy.html %}

### 使用 cURL 傳送資料

下列範例使用 cURL 將大量請求傳送至 `opensearch_api` 來源：

```bash
curl -XPOST "http://localhost:9202/opensearch/_bulk" \
  -H "Content-Type: application/json" \
  -d '{"index":{"_index":"movies","_id":"1"}}
{"title":"Rush","year":2013}
{"delete":{"_index":"movies","_id":"2"}}
'
```
{% include copy.html %}

<!-- vale off -->
### 使用 opensearch-py 傳送資料
<!-- vale on -->

下列範例使用 `opensearch-py` 用戶端傳送大量請求：

```python
from opensearchpy import OpenSearch

client = OpenSearch(
    hosts=[{"host": "localhost", "port": 9202}],
    use_ssl=False,
    url_prefix="/opensearch"
)

client.bulk(body=[
    {"index": {"_index": "movies", "_id": "1"}},
    {"title": "Rush", "year": 2013},
])
```
{% include copy.html %}
