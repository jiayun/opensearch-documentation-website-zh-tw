---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將記錄資料匯入 OpenSearch"
parent: Getting started
nav_order: 30
---

# 將記錄資料匯入 OpenSearch

在本教學中，您將在 Docker 中執行 Data Prepper 與 OpenSearch，將原始 Apache 存取記錄傳送至 Data Prepper，並在 OpenSearch 中搜尋剖析後的記錄資料。您建立的管線會執行下列工作：

1. 透過 HTTP 接收記錄行。
1. 將每一行記錄剖析為個別欄位，例如用戶端 IP 位址、請求路徑與回應碼。
1. 將記錄時間戳記轉換為日期，並將回應碼與大小轉換為整數。
1. 將每個事件寫入 OpenSearch 索引，並列印至 Data Prepper 記錄檔。

此管線會剖析 Apache 通用記錄格式的記錄行，例如下列內容：

```text
10.0.0.7 - - [19/Oct/2026:10:16:03 +0000] "GET /checkout HTTP/1.1" 500 98
```

每一行包含用戶端 IP 位址、兩個身分欄位（空白時為 `-`）、時間戳記、請求（方法、路徑與 HTTP 版本）、回應碼，以及以位元組為單位的回應大小。

當您啟動容器時，Docker Compose 會下載 Data Prepper 與 OpenSearch 映像，因此您不需要先安裝 Data Prepper。

## 先決條件

安裝 [Docker](https://docs.docker.com/get-docker/)，包括 [Docker Compose](https://docs.docker.com/compose/)。容器會使用連接埠 `9200`（OpenSearch）與 `2021`（Data Prepper），因此請確認這些連接埠未被使用。

如果您使用 Linux，請增加 OpenSearch 可用的記憶體對應數量上限。如需詳細資訊，請參閱[重要設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#important-settings)。

## 步驟 1：定義管線

為本教學建立一個目錄（例如 `data-prepper-tutorial`）。在此目錄中，建立名為 `pipelines.yaml` 的檔案，其中包含下列管線組態。將 `<custom-admin-password>` 取代為符合[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)的密碼。您也會在下一個步驟中將此密碼用於 OpenSearch：

```yaml
log-pipeline:
  source:
    http:
      ssl: false
  processor:
    - grok:
        match:
          message: ['%{COMMONAPACHELOG}']
    - date:
        match:
          - key: timestamp
            patterns: ["dd/MMM/yyyy:HH:mm:ss Z"]
        destination: "@timestamp"
    - convert_type:
        keys: ["response", "bytes"]
        type: integer
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: "<custom-admin-password>"
        index: web-logs
        flush_timeout: -1
    - stdout:
```
{% include copy.html %}

此檔案定義名為 `log-pipeline` 的單一管線，其中包含下列元件：

- `source`：[`http`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/http/) 來源會在 `/log/ingest` 路徑的連接埠 `2021` 上接收事件。`ssl: false` 設定會接受純 HTTP 請求，僅適用於本機測試。
- `processor`：Data Prepper 會依列出的順序執行處理器：
  - [`grok`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/grok/) 處理器會將 `message` 欄位與內建的 `COMMONAPACHELOG` 模式進行比對，並為記錄行的每個部分新增欄位，例如 `clientip`、`verb`、`request`、`response`、`bytes` 與 `timestamp`。
  - [`date`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/date/) 處理器會剖析 `timestamp` 欄位，並以 ISO 8601 格式將結果寫入 `@timestamp` 欄位，以便 OpenSearch 將其對應為日期。
  - [`convert_type`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/convert-entry-type/) 處理器會將 `response` 與 `bytes` 欄位從字串轉換為整數，以便您對其執行範圍查詢。
- `sink`：每個事件都會傳送至這兩個接收端：
  - [`opensearch`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/) 接收端會將事件寫入 `web-logs` 索引。`opensearch` 主機名稱會參照您將在下一個步驟中定義的 OpenSearch 容器。`insecure: true` 設定會略過憑證驗證，因為 OpenSearch 容器使用示範憑證。依預設，接收端在將事件寫入 OpenSearch 之前，最多會等待 60 秒來批次處理事件。將 `flush_timeout` 設為 `-1` 後，事件一經處理就會立即寫入，讓您能立即看到結果。
  - [`stdout`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/stdout/) 接收端會將每個已處理的事件列印至 Data Prepper 記錄檔，以便您檢查。

## 步驟 2：建立 Docker Compose 檔案

在同一個目錄中，建立名為 `.env` 的檔案，其中包含下列內容。將 `<custom-admin-password>` 取代為您在 `pipelines.yaml` 中使用的密碼：

```bash
OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
```
{% include copy.html %}

Docker Compose 會自動讀取 `.env` 檔案，並將密碼傳遞給 OpenSearch。如果密碼不符合需求，OpenSearch 就不會啟動。

建立名為 `docker-compose.yml` 的檔案，其中包含下列組態：

```yaml
services:
  opensearch:
    image: opensearchproject/opensearch:latest
    container_name: opensearch
    environment:
      - discovery.type=single-node
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD}
    ports:
      - 9200:9200
  data-prepper:
    image: opensearchproject/data-prepper:latest
    container_name: data-prepper
    volumes:
      - ./pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml
    ports:
      - 2021:2021
    depends_on:
      - opensearch
```
{% include copy.html %}

此檔案定義兩個容器：

- `opensearch`：已啟用安全性的單一節點 OpenSearch 叢集，可於 `https://localhost:9200` 使用。
- `data-prepper`：Data Prepper 執行個體。Data Prepper 會載入 `/usr/share/data-prepper/pipelines/` 目錄中的每個管線組態檔，因此 `volumes` 設定會將您的 `pipelines.yaml` 檔案掛載至該目錄。連接埠 `2021` 已發布，以便您從自己的機器將資料傳送至 `http` 來源。

您的目錄現在包含下列檔案：

```text
data-prepper-tutorial/
├── .env
├── docker-compose.yml
└── pipelines.yaml
```

## 步驟 3：啟動容器

從 `data-prepper-tutorial` 目錄中，在背景啟動容器：

```bash
docker compose up -d
```
{% include copy.html %}

追蹤 Data Prepper 記錄檔：

```bash
docker compose logs -f data-prepper
```
{% include copy.html %}

OpenSearch 啟動期間，Data Prepper 會記錄 `Failed to initialize OpenSearch sink, retrying` 警告。這些警告是預期中的。Data Prepper 會重試直到 OpenSearch 可用為止，這通常需要不到一分鐘。當管線就緒時，記錄檔會包含下列內容：

```text
data-prepper  | ... INFO  org.opensearch.dataprepper.plugins.source.loghttp.HTTPSource - Started http source on port 2021...
data-prepper  | ... INFO  org.opensearch.dataprepper.plugins.sink.opensearch.OpenSearchSink - Initialized OpenSearch sink
```

讓記錄檔繼續執行，並為下一個步驟開啟新的終端機視窗。

## 步驟 4：將記錄資料傳送至 Data Prepper

`http` 來源接受一個 JSON 陣列，其中每個物件會成為一個事件。傳送三行 Apache 存取記錄，每行放在 `message` 欄位中：

```bash
curl -X POST http://localhost:2021/log/ingest \
  -H "Content-Type: application/json" \
  -d '[
    {"message": "192.168.1.10 - - [19/Oct/2026:10:15:32 +0000] \"GET /products/123 HTTP/1.1\" 200 5120"},
    {"message": "192.168.1.25 - - [19/Oct/2026:10:15:47 +0000] \"POST /cart HTTP/1.1\" 201 342"},
    {"message": "10.0.0.7 - - [19/Oct/2026:10:16:03 +0000] \"GET /checkout HTTP/1.1\" 500 98"}
  ]'
```
{% include copy.html %}

Data Prepper 會回應 `200 OK`。

## 步驟 5：檢視處理後的事件

返回包含 Data Prepper 記錄檔的終端機。`stdout` 接收端會將每個處理後的事件列印在單一行上。例如，以下事件（為方便閱讀而格式化）是由第三行記錄所建立：

```json
{
  "message": "10.0.0.7 - - [19/Oct/2026:10:16:03 +0000] \"GET /checkout HTTP/1.1\" 500 98",
  "request": "/checkout",
  "auth": "-",
  "ident": "-",
  "response": 500,
  "bytes": 98,
  "clientip": "10.0.0.7",
  "verb": "GET",
  "httpversion": "1.1",
  "timestamp": "19/Oct/2026:10:16:03 +0000",
  "@timestamp": "2026-10-19T10:16:03.000Z"
}
```

將此事件與您傳送的記錄行比較：

- `message` 欄位包含原始記錄行。
- `grok` 處理器新增了 `clientip`、`ident`、`auth`、`timestamp`、`verb`、`request`、`httpversion`、`response` 與 `bytes` 欄位。
- `date` 處理器新增了 `@timestamp` 欄位。
- `convert_type` 處理器將 `response` 與 `bytes` 轉換為整數，因此它們顯示時沒有引號。

## 步驟 6：在 OpenSearch 中搜尋資料

`opensearch` 接收端已將相同的事件寫入 `web-logs` 索引。搜尋傳回錯誤的請求，也就是包含 `400` 以上回應碼的請求：

```bash
curl -X GET "https://localhost:9200/web-logs/_search?pretty" -ku admin:<custom-admin-password> \
  -H "Content-Type: application/json" \
  -d '{
    "query": {
      "range": {
        "response": {
          "gte": 400
        }
      }
    }
  }'
```
{% include copy.html %}

`-k` 選項會略過憑證驗證，因為 OpenSearch 使用示範憑證。回應包含傳回 `500` 回應碼之請求的事件：

```json
{
  "took" : 41,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "web-logs",
        "_id" : "QJmSVKEBVverMSge8P0k",
        "_score" : 1.0,
        "_source":{"message":"10.0.0.7 - - [19/Oct/2026:10:16:03 +0000] \"GET /checkout HTTP/1.1\" 500 98","request":"/checkout","auth":"-","ident":"-","response":500,"bytes":98,"clientip":"10.0.0.7","verb":"GET","httpversion":"1.1","timestamp":"19/Oct/2026:10:16:03 +0000","@timestamp":"2026-10-19T10:16:03.000Z"}
      }
    ]
  }
}
```

範圍查詢之所以有效，是因為 `convert_type` 處理器在事件到達 OpenSearch 之前，已將 `response` 轉換為整數。

## 步驟 7：修改管線

Data Prepper 只會在啟動時讀取管線組態檔，因此變更管線後必須重新啟動 Data Prepper。

`timestamp` 欄位與 `@timestamp` 欄位重複。若要移除它，請在 `pipelines.yaml` 的 `processor` 清單結尾新增 [`delete_entries`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/delete-entries/) 處理器：

```yaml
  processor:
    - grok:
        match:
          message: ['%{COMMONAPACHELOG}']
    - date:
        match:
          - key: timestamp
            patterns: ["dd/MMM/yyyy:HH:mm:ss Z"]
        destination: "@timestamp"
    - convert_type:
        keys: ["response", "bytes"]
        type: integer
    - delete_entries:
        with_keys: ["timestamp"]
```
{% include copy.html %}

重新啟動 Data Prepper：

```bash
docker compose restart data-prepper
```
{% include copy.html %}

等待 Data Prepper 記錄檔包含新的 `Started http source on port 2021` 行，然後傳送另一行記錄：

```bash
curl -X POST http://localhost:2021/log/ingest \
  -H "Content-Type: application/json" \
  -d '[
    {"message": "10.0.0.7 - - [19/Oct/2026:10:20:11 +0000] \"GET /checkout HTTP/1.1\" 503 64"}
  ]'
```
{% include copy.html %}

Data Prepper 記錄檔中的新事件不再包含 `timestamp` 欄位：

```json
{
  "message": "10.0.0.7 - - [19/Oct/2026:10:20:11 +0000] \"GET /checkout HTTP/1.1\" 503 64",
  "request": "/checkout",
  "auth": "-",
  "ident": "-",
  "response": 503,
  "bytes": 64,
  "clientip": "10.0.0.7",
  "verb": "GET",
  "httpversion": "1.1",
  "@timestamp": "2026-10-19T10:20:11.000Z"
}
```

在變更之前已編製索引的事件不會被修改。

## 步驟 8：清理

若要停止並移除容器，請從 `data-prepper-tutorial` 目錄執行以下命令：

```bash
docker compose down
```
{% include copy.html %}

這些容器不使用磁碟區，因此移除它們會刪除 `web-logs` 索引。

## 後續步驟

- 若要了解管線結構、條件路由與其他管線選項，請參閱[管線]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines/)。
- 若要尋找可在管線中使用的來源、處理器與接收端，請參閱[來源]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sources/sources/)、[處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/processors/)與[接收端]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/sinks/)。有些處理器頁面包含將資料傳送至 `localhost:2021` 並寫入 `https://opensearch:9200` 的完整範例。您可以在本教學的環境中執行這些範例，方法是將範例管線複製到 `pipelines.yaml`，將 `<custom-admin-password>` 取代為 `.env` 檔案中的管理員密碼，然後重新啟動 Data Prepper。
- 若要設定 Data Prepper 伺服器，包括其連接埠、TLS 與驗證，請參閱[設定 OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/managing-data-prepper/configuring-data-prepper/)。
- 若要針對常見使用情境設定 Data Prepper，請參閱[記錄分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/log-analytics/)與[追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)。
- 若要從記錄收集器而非 `curl` 傳送記錄，請參閱 Data Prepper 儲存庫中 [Fluent Bit](https://github.com/opensearch-project/data-prepper/tree/main/examples/log-ingestion)、[Fluentd](https://github.com/opensearch-project/data-prepper/tree/main/examples/log-ingestion-fluentd)、[Kubernetes](https://github.com/opensearch-project/data-prepper/tree/main/examples/log-ingestion-k8s) 與 [Amazon ECS FireLens](https://github.com/opensearch-project/data-prepper/tree/main/examples/log-ingestion-ecs-firelens) 的範例。
