---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指標分析"
nav_order: 50
---

# 指標分析
於 2.4 版推出
{: .label .label-purple }

隨著 OpenSearch 2.4 的發布，您現在可以使用 **Metrics** 工具，匯入並視覺化直接儲存在 OpenSearch 中的指標資料。這讓您能夠運用相關工具，跨記錄檔、追蹤及指標分析與關聯資料。

在推出此功能之前，您只能匯入並視覺化受監控環境中的記錄檔與追蹤。透過 **Metrics** 工具，您現在可以更精細地觀察數位資產、更深入了解基礎架構的健康狀態，並為根本原因分析提供更充分的依據。

**Metrics** 工具除了提供聯合視覺化功能之外，還支援以下項目：

 - 包含 [OpenTelemetry (OTel) 相容指標索引](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability/metrics) 且具有 OTel 型訊號的 OpenSearch 叢集。如需 OTel 的概觀，請參閱[什麼是 OpenTelemetry？](https://opentelemetry.io/docs/what-is-opentelemetry/)。
 - 包含連線至 Prometheus 伺服器之 [Prometheus 資料來源](https://github.com/opensearch-project/sql/blob/main/docs/dev/datasource-prometheus.md) 的 OpenSearch 叢集。 

下圖顯示從 Prometheus 擷取指標並將其顯示在視覺化儀表板上的流程。

![Prometheus 資料來源]({{site.url}}{{site.baseurl}}/images/metrics/prom-metrics.png){: width="700" }

下圖顯示一個可觀測性儀表板，此儀表板使用 OTel 查詢將 OpenSearch 索引中的指標資料視覺化。

![OTel 資料來源]({{site.url}}{{site.baseurl}}/images/metrics/otel-metrics.png){: width="700" }

---

## 設定 Prometheus 將指標資料傳送至 OpenSearch

您必須先使用 [SQL 外掛程式](https://github.com/opensearch-project/sql) 建立從 [Prometheus](https://prometheus.io/) 到 OpenSearch 的連線。接著，您可以使用 `_datasources` API 端點設定與 Prometheus 的連線。 

以下範例顯示一個不使用任何驗證來設定 Prometheus 資料來源的請求：

```json
POST _plugins/_query/_datasources 
{
    "name" : "my_prometheus",
    "connector": "prometheus",
    "properties" : {
        "prometheus.uri" : "http://localhost:9090"
    }
}
```
{% include copy-curl.html %}

以下範例顯示如何使用 AWS Signature Version 4 驗證來設定 Prometheus 資料來源：

```json
POST _plugins/_query/_datasources
{
    "name" : "my_prometheus",
    "connector": "prometheus",
    "properties" : {
        "prometheus.uri" : "http://localhost:8080",
        "prometheus.auth.type" : "awssigv4",
        "prometheus.auth.region" : "us-east-1",
        "prometheus.auth.access_key" : "<access_key>",
        "prometheus.auth.secret_key" : "<secret_key>"
    }
}
```
{% include copy-curl.html %}

設定連線之後，您可以前往 **Observability** > **Metrics** 頁面，在 OpenSearch Dashboards 中檢視 Prometheus 指標，如下圖所示。

![顯示在儀表板上的 Prometheus 指標]({{site.url}}{{site.baseurl}}/images/metrics/metrics1.png){: width="700" }

### 開發人員資源

請參閱以下開發人員資源，取得範例程式碼、文章、教學及 API 參考資料：

* [資料來源設定](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/datasources.md)，包含資料來源 API 的驗證與授權相關資訊。
* [Prometheus 連接器](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/connectors/prometheus_connector.md)，包含組態資訊。
* [Simple Schema for Observability](https://github.com/opensearch-project/opensearch-catalog/tree/main/docs/schema/observability)，包含 OTel 結構描述與資料匯入管線的相關資訊。
* [OTel Metrics Source](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/otel-metrics-source)，包含 Data Prepper 指標管線與匯入的相關資訊。

---

## 在 OpenSearch 示範環境中試用 OpenTelemetry Metrics 

OpenSearch [`opentelemetry-demo` 儲存庫](https://github.com/opensearch-project/opentelemetry-demo) 提供了實際示範，說明如何透過 OpenTelemetry 的 **OpenTelemetry Metrics** 收集、處理及視覺化指標資料，並使用 OpenSearch Dashboards 中的 **Metrics** 工具。

### 在 OpenSearch 中視覺化 OTel 指標

若要在 OpenSearch 中視覺化 OTel 指標資料，請依照下列步驟操作： 

1. 安裝 [`opentelemetry-demo` 儲存庫](https://github.com/opensearch-project/opentelemetry-demo)。如需相關說明，請參閱[快速入門](https://github.com/opensearch-project/opentelemetry-demo/blob/main/README.md#quick-start)。
2. 收集 OTel 訊號，包括指標訊號。如需相關說明，請參閱 [OTel Collector](https://opentelemetry.io/docs/collector/) 指南。  
3. 設定 OTel 管線以發出指標訊號。如需相關說明，請參閱 [OTel Collector Pipeline](https://github.com/opensearch-project/opentelemetry-demo/tree/main/src/otel-collector) 指南。

#### YAML 組態檔案範例

```yaml
    service:
      extensions: [basicauth/client]
      pipelines:
        traces:
          receivers: [otlp]
          processors: [batch]
          exporters: [otlp, debug, spanmetrics, otlp/traces, opensearch/traces]
        metrics:
          receivers: [otlp, spanmetrics]
          processors: [filter/ottl, transform, batch]
          exporters: [otlphttp/prometheus, otlp/metrics, debug]
        logs:
          receivers: [otlp]
          processors: [batch]
          exporters: [otlp/logs,  opensearch/logs, debug]
```
{% include copy.html %}
    
4. 設定 [Data Prepper 管線](https://github.com/opensearch-project/opentelemetry-demo/blob/main/src/dataprepper/README.md)，將收集到的指標訊號發送至 OpenSearch 指標索引。

#### YAML 組態檔案範例

```yaml
    otel-metrics-pipeline:
      workers: 8
      delay: 3000
      source:
        otel_metrics_source:
          health_check_service: true
          ssl: false
      buffer:
        bounded_blocking:
          buffer_size: 1024 # max number of records the buffer accepts
          batch_size: 1024 # max number of records the buffer drains after each read
      processor:
        - otel_metrics:
            calculate_histogram_buckets: true
            calculate_exponential_histogram_buckets: true
            exponential_histogram_max_allowed_scale: 10
            flatten_attributes: false
      sink:
        - opensearch:
            hosts: ["https://opensearch-node1:9200"]
            username: "admin"
            password: "my_%New%_passW0rd!@#"
            insecure: true
            index_type: custom
            template_file: "templates/ss4o_metrics.json"
            index: ss4o_metrics-otel-%{yyyy.MM.dd}
            bulk_size: 4
```
{% include copy.html %}

5. 將指標資料匯入 OpenSearch。示範開始產生資料後，指標訊號將會新增至支援 OpenTelemetry Metrics 結構描述格式的 OpenSearch 索引中。
6. 在 **Metrics** 頁面上，從 **Data sources** 下拉式選單中選擇 `Otel-Index`，並從 **OTel index** 下拉式選單中選擇 `Simple Schema for Observability Index`。隨即會顯示視覺化，如下圖所示。

![OTel 指標儀表板]({{site.url}}{{site.baseurl}}/images/metrics/otel-metrics.png){: width="700" }

---

## 在遠端叢集中視覺化指標
於 2.14 版推出
{: .label .label-purple }

您可以使用 **Metrics** 工具檢視來自遠端 OpenSearch 叢集的指標。選取右上方工具列上的資料庫圖示，並從 **DATA SOURCES** 下拉式選單中選擇叢集，如下圖所示。您可以從本機叢集切換至遠端叢集。

![使用 Metrics 分析工具切換叢集]({{site.url}}{{site.baseurl}}/images/metrics/remote-cluster-selection.png){: width="700" }

您也可以將來自其他來源的指標視覺化與本機指標視覺化並列檢視。從 **DATA SOURCES** 下拉式選單中選擇遠端指標視覺化，即可將其新增至儀表板上已顯示的視覺化群組中。下圖顯示一個儀表板範例。

![指標儀表板]({{site.url}}{{site.baseurl}}/images/metrics/otel-metrics-remote-cluster-selection.png){: width="700" }

若要了解資料來源的多叢集支援，請參閱[讓 OpenSearch Dashboards 支援多個 OpenSearch 叢集](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/1388)。

## 根據自訂指標建立視覺化

您可以使用 OpenSearch 叢集收集的指標資料（包括 Prometheus 指標與自訂指標）建立視覺化。

若要建立這些視覺化，請依照下列步驟操作：

1. 從 OpenSearch Dashboards 主選單前往 **Observability** > **Metrics** > **Available Metrics**。
2. 選擇要新增至視覺化的指標，然後選取 **Save**。
3. 當系統提示您選擇 **Custom operational dashboards/application** 時，請選擇其中一個列出的選項。您可以在 **Metric Name** 欄位中編輯預先定義的名稱值。
4. 選取 **Save** 以儲存視覺化。下圖顯示一個視覺化範例。

![包含視覺化的指標分析儀表板]({{site.url}}{{site.baseurl}}/images/metrics/metrics2.png){: width="700" }

## 為 Prometheus 指標定義 PPL 查詢

您可以定義 [Piped Processing Language (PPL)]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) 查詢，與 Prometheus 收集的指標互動。以下是 Prometheus 指標的 PPL 查詢範例：

```
source = my_prometheus.prometheus_http_requests_total | stats avg(@value) by span(@timestamp,15s), handler, code
```
{% include copy.html %}

### 根據 PPL 查詢建立自訂視覺化

若要根據 PPL 查詢建立自訂視覺化，請依照下列步驟操作：

1. 在 **Logs** 頁面上，選取 > **Event Explorer**。
2. 在 **Explorer** 頁面上，輸入您的 PPL 查詢並選取 **Run**，然後選取 **Save**。
3. 當系統提示您選擇 **Custom Operational Dashboards/Application** 時，請選取其中一個列出的選項。您也可以選擇在 **Metric Name** 欄位中編輯預先定義的名稱值，並可選擇將視覺化儲存為指標。
4. 選取 **Save** 以儲存您的自訂視覺化。 

只有包含時間序列視覺化以及統計資料或時間範圍 (span) 資訊的查詢，才能儲存為指標，如下圖所示。

![將查詢儲存為指標]({{site.url}}{{site.baseurl}}/images/metrics/metrics3.png){: width="700" }
