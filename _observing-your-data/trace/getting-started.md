---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
parent: Trace analytics
grand_parent: Classic observability apps
nav_order: 1
redirect_from:
  - /observability-plugin/trace/get-started/
  - /monitoring-plugins/trace/get-started/
---

# 追蹤分析入門

追蹤分析使用 [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 將追蹤資料匯入 OpenSearch，並使用 [OpenSearch Dashboards 中的追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/ta-dashboards/) 進行視覺化。在本教學中，您將執行一個會產生追蹤資料的範例應用程式、將追蹤資料傳送至 OpenSearch，並在 OpenSearch Dashboards 中檢視。

如果您已使用 Jaeger 並以 OpenSearch 作為其儲存後端，請改參閱 [分析 Jaeger 追蹤資料]({{site.url}}{{site.baseurl}}/observing-your-data/trace/trace-analytics-jaeger/)。

## 資料的基本流程

下圖說明追蹤資料如何從應用程式流向 OpenSearch。

![從分散式應用程式到 OpenSearch 的資料流程圖]({{site.url}}{{site.baseurl}}/images/ta.svg)

1. 您在應用程式中加入檢測，以產生追蹤資料。[OpenTelemetry 文件](https://opentelemetry.io/docs/)包含許多程式語言的範例應用程式，包括 Java、Python、Go 和 JavaScript。
1. [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)使用 OpenTelemetry Protocol (OTLP) 從應用程式接收追蹤資料，並將其傳送至 Data Prepper。
1. Data Prepper 處理追蹤資料，將 span 寫入 `otel-v1-apm-span-*` 索引，並將服務關聯寫入 `otel-v1-apm-service-map` 索引。
1. OpenSearch Dashboards 中的追蹤分析會以圖表和表格顯示資料，呈現服務相依性、延遲、錯誤率和輸送量。

## 執行 Jaeger HotROD 範例

下列範例使用 Docker Compose 執行單一節點的 OpenSearch 叢集、OpenSearch Dashboards、Data Prepper、OpenTelemetry Collector，以及 [Jaeger HotROD](https://github.com/jaegertracing/jaeger/tree/main/examples/hotrod) 範例應用程式，此應用程式模擬由數個微服務組成的共乘服務。

### 步驟 1：設定管理員密碼

OpenSearch 要求為 `admin` 使用者設定自訂密碼。請在空目錄中建立一個名為 `.env` 的檔案，內容為下列一行，並將 `<custom-admin-password>` 替換為強式密碼：

```bash
OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
```
{% include copy.html %}

Docker Compose 會讀取此檔案，並將密碼傳遞給 OpenSearch。如需更多資訊，請參閱 [管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)。

### 步驟 2：設定 OpenTelemetry Collector

在同一個目錄中，建立名為 `otel-collector-config.yaml` 的檔案，內容包含下列組態。Collector 會從 HotROD 接收 OTLP 資料，並將追蹤傳送至 Data Prepper：

```yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:

exporters:
  otlp_grpc/data-prepper:
    endpoint: data-prepper:21890
    tls:
      insecure: true

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlp_grpc/data-prepper]
```
{% include copy.html %}

### 步驟 3：設定 Data Prepper 管線

在同一個目錄中，建立一個名為 `pipelines.yaml` 的檔案，內容包含以下組態，並將兩處 `<custom-admin-password>` 替換為您在步驟 1 中設定的密碼。`entry-pipeline` 會接收追蹤資料並將其傳遞給兩條管線：`raw-trace-pipeline` 將 span 寫入 OpenSearch，`service-map-pipeline` 則寫入服務之間的關聯。如需更多資訊，請參閱 [追蹤分析]({{site.url}}{{site.baseurl}}/data-prepper/common-use-cases/trace-analytics/)。

```yaml
entry-pipeline:
  source:
    otel_trace_source:
      ssl: false
  sink:
    - pipeline:
        name: raw-trace-pipeline
    - pipeline:
        name: service-map-pipeline

raw-trace-pipeline:
  source:
    pipeline:
      name: entry-pipeline
  processor:
    - otel_traces:
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true # The demo security configuration uses self-signed certificates
        username: admin
        password: <custom-admin-password>
        index_type: trace-analytics-raw

service-map-pipeline:
  source:
    pipeline:
      name: entry-pipeline
  processor:
    - service_map:
  sink:
    - opensearch:
        hosts: ["https://opensearch:9200"]
        insecure: true
        username: admin
        password: <custom-admin-password>
        index_type: trace-analytics-service-map
```
{% include copy.html %}

### 步驟 4：建立 Docker Compose 檔案

在同一目錄中，建立名為 `docker-compose.yml` 的檔案，並在其中加入下列組態：

```yaml
services:
  opensearch:
    image: opensearchproject/opensearch:latest
    environment:
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
      - OPENSEARCH_INITIAL_ADMIN_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD}
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - opensearch-data:/usr/share/opensearch/data
    ports:
      - "9200:9200"
    healthcheck: # Data Prepper starts only after the cluster is available
      test: ["CMD-SHELL", "curl -sk -u admin:$$OPENSEARCH_INITIAL_ADMIN_PASSWORD https://localhost:9200/_cluster/health | grep -qE '\"status\":\"(green|yellow)\"'"]
      interval: 10s
      timeout: 5s
      retries: 30
    networks:
      - opensearch-net

  opensearch-dashboards:
    image: opensearchproject/opensearch-dashboards:latest
    ports:
      - "5601:5601"
    environment:
      OPENSEARCH_HOSTS: '["https://opensearch:9200"]'
    networks:
      - opensearch-net
    depends_on:
      - opensearch

  data-prepper:
    image: opensearchproject/data-prepper:latest
    volumes:
      - ./pipelines.yaml:/usr/share/data-prepper/pipelines/pipelines.yaml:ro
    networks:
      - opensearch-net
    depends_on:
      opensearch:
        condition: service_healthy

  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otelcol/config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otelcol/config.yaml:ro
    networks:
      - opensearch-net
    depends_on:
      - data-prepper

  hotrod:
    image: jaegertracing/example-hotrod:latest
    command: ["all"]
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4318
    ports:
      - "8080:8080"
    networks:
      - opensearch-net
    depends_on:
      - otel-collector

volumes:
  opensearch-data:

networks:
  opensearch-net:
```
{% include copy.html %}

### 步驟 5：啟動容器

若要啟動容器，請執行以下命令：

```bash
docker compose up -d
```
{% include copy.html %}

Data Prepper 會在 OpenSearch 叢集回報 `green` 或 `yellow` 健康狀態後啟動，這可能需要一分鐘或更久。若要確認 Data Prepper 已準備好接收追蹤資料，請重複執行以下命令，直到輸出包含類似 `Started otel_trace_source on port 21890` 的一行為止：

```bash
docker compose logs data-prepper | grep "Started otel_trace_source"
```
{% include copy.html %}

### 步驟 6：產生追蹤資料

若要開啟 HotROD 範例應用程式，請前往 [http://localhost:8080](http://localhost:8080)。每次您選取客戶時，HotROD 會透過其服務傳送請求並產生追蹤。部分請求會刻意失敗，以便追蹤分析中的錯誤檢視能顯示資料。

請選取數個客戶。Data Prepper 會在收到完整追蹤後寫入 span，因此資料最多可能需要三分鐘才會出現。若要確認 OpenSearch 含有追蹤資料，請執行下列命令：

```bash
curl -sk -u admin:<custom-admin-password> "https://localhost:9200/_cat/indices/otel-v1-apm-*?v"
```
{% include copy.html %}

回應會列出 `otel-v1-apm-span-000001` 與 `otel-v1-apm-service-map` 索引。`docs.count` 欄位會顯示每個索引的非零文件數。

### 步驟 7：在 OpenSearch Dashboards 中檢視追蹤資料

前往 [http://localhost:5601](http://localhost:5601) 並以 `admin` 使用者身分登入，密碼使用您在步驟 1 設定的密碼。在頂端選單中，前往 **Observability** > **Traces**。請確認資料來源已選取 **Data Prepper**。

**Traces** 頁面會列出來自 HotROD 的跨度與追蹤，**Services** 頁面則會顯示每個服務以及服務之間的依賴關係圖。如果您沒有看到任何資料，請使用時間選擇器選取包含您產生追蹤資料之時間的時間範圍。如需更多資訊，請參閱 [OpenSearch Dashboards 中的追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/ta-dashboards/)。

### 步驟 8：清理

若要停止容器並刪除其資料，請執行下列命令：

```bash
docker compose down -v
```
{% include copy.html %}
