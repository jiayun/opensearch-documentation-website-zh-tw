---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分析 Jaeger 追蹤資料"
parent: Trace analytics
nav_order: 55
redirect_from:
  - /observability-plugin/trace/trace-analytics-jaeger/
---

# 分析 Jaeger 追蹤資料

於 2.5 版推出
{: .label .label-purple }

如果您使用 OpenSearch 作為 [Jaeger](https://www.jaegertracing.io/) 的儲存後端，您可以使用 OpenSearch Dashboards 中的追蹤分析來分析 Jaeger 追蹤資料。追蹤分析會顯示您的服務與作業的錯誤率和延遲。您可以篩選追蹤，並檢查個別追蹤的跨度，以找出服務問題。

追蹤分析支援兩種資料來源。選取 **Data Prepper** 以分析 OpenSearch Data Prepper 匯入至 OpenSearch 的追蹤資料。選取 **Jaeger** 以分析 Jaeger 儲存在 OpenSearch 中的追蹤資料。

## Jaeger 索引

Jaeger 和 Data Prepper 會將追蹤資料儲存在不同的索引中。Data Prepper 會寫入名為 `otel-v1-apm-span-*` 和 `otel-v1-apm-service-map*` 的索引。Jaeger 會寫入名為 `jaeger-span-*` 和 `jaeger-service-*` 的索引。根據預設，Jaeger 每天會建立新的跨度索引和新的服務索引。

## 錯誤資料需求

追蹤分析會使用 `tag.error` 欄位來識別包含錯誤的跨度。Jaeger v2 一律會將 `error` 標籤儲存為跨度文件中的欄位，因此不需要額外的組態即可取得錯誤資料。

較舊的 Jaeger 收集器預設會將標籤儲存在巢狀陣列中。如果您使用其中一種收集器，請將 `ES_TAGS_AS_FIELDS_ALL` 環境變數設為 `true`。否則，追蹤分析中將無法取得錯誤資料。

## 設定 OpenSearch 以使用 Jaeger 資料

下列範例使用 Docker Compose 執行單一節點 OpenSearch 叢集、OpenSearch Dashboards、Jaeger 以及 Jaeger HotROD 範例應用程式。HotROD 會使用 OpenTelemetry Protocol (OTLP) 將追蹤資料傳送至 Jaeger，而 Jaeger 會將資料儲存在 OpenSearch 中。

### 步驟 1：設定管理員密碼

OpenSearch 需要為 `admin` 使用者設定自訂密碼。在空目錄中，建立名為 `.env` 的檔案，其中包含下列這一行，並將 `<custom-admin-password>` 取代為高強度密碼：

```bash
OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
```
{% include copy.html %}

Docker Compose 會讀取此檔案，並將密碼傳遞給 OpenSearch 和 Jaeger。如需詳細資訊，請參閱[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)。

### 步驟 2：設定 Jaeger

在同一個目錄中，建立名為 `jaeger-config.yaml` 的檔案，其中包含下列組態。此組態會設定 Jaeger 接收 OTLP 資料並將其儲存在 OpenSearch 中：

```yaml
service:
  extensions: [jaeger_storage, jaeger_query]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger_storage_exporter]

extensions:
  jaeger_query:
    storage:
      traces: opensearch_storage

  jaeger_storage:
    backends:
      opensearch_storage:
        opensearch:
          server_urls:
            - https://opensearch:9200
          tls:
            insecure_skip_verify: true # The demo security configuration uses self-signed certificates
          auth:
            basic:
              username: admin
              password: ${env:OPENSEARCH_PASSWORD}

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
  jaeger_storage_exporter:
    trace_storage: opensearch_storage
```
{% include copy.html %}

### 步驟 3：建立 Docker Compose 檔案

在同一個目錄中，建立名為 `docker-compose.yml` 的檔案，其中包含下列組態：

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
    healthcheck: # Jaeger starts only after the cluster is available
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

  jaeger:
    image: jaegertracing/jaeger:latest
    command: ["--config", "/etc/jaeger/config.yaml"]
    environment:
      - OPENSEARCH_PASSWORD=${OPENSEARCH_INITIAL_ADMIN_PASSWORD}
    volumes:
      - ./jaeger-config.yaml:/etc/jaeger/config.yaml:ro
    ports:
      - "16686:16686" # Jaeger UI
      - "4317:4317" # OTLP over gRPC
      - "4318:4318" # OTLP over HTTP
    networks:
      - opensearch-net
    depends_on:
      opensearch:
        condition: service_healthy

  hotrod:
    image: jaegertracing/example-hotrod:latest
    command: ["all"]
    environment:
      - OTEL_EXPORTER_OTLP_ENDPOINT=http://jaeger:4318
    ports:
      - "8080:8080"
    networks:
      - opensearch-net
    depends_on:
      - jaeger

volumes:
  opensearch-data:

networks:
  opensearch-net:
```
{% include copy.html %}

### 步驟 4：啟動容器

若要啟動容器，請執行下列命令：

```bash
docker compose up -d
```
{% include copy.html %}

Jaeger 和 HotROD 會在 OpenSearch 叢集回報 `green` 或 `yellow` 健康狀態後啟動，這可能需要一分鐘或更久。

若要停止容器並刪除其資料，請執行下列命令：

```bash
docker compose down -v
```
{% include copy.html %}

### 步驟 5：產生範例資料

若要開啟 HotROD 範例應用程式，請前往 [http://localhost:8080](http://localhost:8080)。每次您選取客戶時，HotROD 就會產生一個追蹤。部分追蹤包含錯誤，因此追蹤分析中的錯誤檢視會顯示資料。

![HotROD 範例應用程式]({{site.url}}{{site.baseurl}}/images/trace-analytics/sample-app.png)

若要確認 Jaeger 已將追蹤資料儲存在 OpenSearch 中，請列出 Jaeger 索引：

```bash
curl -sk -u admin:<custom-admin-password> "https://localhost:9200/_cat/indices/jaeger-*?v"
```
{% include copy.html %}

回應會包含當天的 `jaeger-span-*` 索引和 `jaeger-service-*` 索引。

### 步驟 6：在 OpenSearch Dashboards 中檢視追蹤資料

前往 [http://localhost:5601](http://localhost:5601)，並以您在步驟 1 中設定的密碼登入 `admin` 使用者。在頂端功能表中，前往 **Observability** > **Traces**。

## 選取資料來源

若要分析 Jaeger 資料，請從 **Trace analytics** 頁面頂端的資料來源選取器中選取 **Jaeger**。

![選取 Jaeger 作為追蹤分析資料來源]({{site.url}}{{site.baseurl}}/images/trace-analytics/select-data.png)

追蹤分析只會顯示所選時間範圍的資料。預設時間範圍是過去 5 分鐘。如果沒有出現任何追蹤，請在範例應用程式中產生新資料，或選取更長的時間範圍。

## 追蹤

**Traces** 頁面會列出所選時間範圍內的追蹤。對於每個追蹤，清單會顯示追蹤 ID、延遲、追蹤是否包含錯誤，以及上次更新的時間。

![Jaeger 追蹤清單]({{site.url}}{{site.baseurl}}/images/trace-analytics/service-trace-data.png)

### 錯誤率

若要檢視錯誤資料，請展開追蹤清單下方的 **Service and Operations**，然後選取 **Errors**。圖表會顯示一段時間內的追蹤錯誤率。**Top 5 Service and Operation Errors** 表格會列出錯誤率最高的服務與作業組合。

![一段時間內的追蹤錯誤率]({{site.url}}{{site.baseurl}}/images/trace-analytics/error-rate.png)

### 請求率

若要檢視輸送量，請選取 **Request rate**。圖表會顯示一段時間內的追蹤數量。**Top 5 Service and Operation Latency** 表格會列出延遲最高的服務與作業組合。

![一段時間內的追蹤以及延遲最高的作業]({{site.url}}{{site.baseurl}}/images/trace-analytics/throughput.png)

在任一表格中，選取服務和作業名稱，即可依該服務和作業篩選追蹤清單。

### 追蹤詳細資料

若要檢視追蹤的詳細資料，請選取其追蹤 ID。追蹤詳細資料頁面會以時間軸、清單或樹狀結構顯示每個服務花費的時間以及追蹤的跨度。**Payload** 區段會以 JSON 格式顯示跨度文件。

![Jaeger 追蹤詳細資料]({{site.url}}{{site.baseurl}}/images/trace-analytics/trace-details.png)

## 服務

若要檢視每個服務的平均持續時間、錯誤率、請求率和追蹤數量，請選取 **Services**。

![Jaeger 服務清單]({{site.url}}{{site.baseurl}}/images/trace-analytics/services-jaeger.png)
