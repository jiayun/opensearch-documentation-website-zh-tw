---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄分析入門"
nav_order: 10
redirect_from:
  - /observability-plugin/log-analytics/
---

# 記錄分析入門

在本教學中，您將把 Apache 存取記錄檔傳送至 OpenSearch，使用 Piped Processing Language (PPL) 進行查詢，並將結果的視覺化加入儀表板。

本教學使用下列元件：

- [Fluent Bit](https://docs.fluentbit.io/manual/) 從檔案收集記錄列，並將它們傳送至 Data Prepper。
- [OpenSearch Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 將每個記錄列解析成欄位，並將結果寫入 OpenSearch 索引。
- [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/index/) 使用 [事件分析（Event analytics）]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/) 與 [作業面板（Operational panels）]({{site.url}}{{site.baseurl}}/observing-your-data/operational-panels/) 查詢並視覺化已編製索引的記錄。

下圖顯示記錄資料如何從應用程式流向 OpenSearch。

![從分散式應用程式到 OpenSearch 的記錄資料流程圖]({{site.url}}{{site.baseurl}}/images/la.png)

## 必要條件

若要執行本教學，您需要 [Docker](https://docs.docker.com/get-docker/) 與 [Git](https://git-scm.com/downloads)。本教學會在連接埠 9200 啟動 OpenSearch，並在連接埠 5601 啟動 OpenSearch Dashboards，因此請停止任何使用這些連接埠的其他 OpenSearch 叢集。

## 步驟 1：下載範例

範例位於 [Data Prepper 儲存庫](https://github.com/opensearch-project/data-prepper) 的 `examples/log-ingestion/` 目錄中，包含下列檔案。

| 檔案 | 說明 |
|:---|:---|
| `docker-compose.yaml` | 定義 Fluent Bit (`fluent-bit`)、單一節點 OpenSearch 叢集 (`opensearch`)，以及 OpenSearch Dashboards (`dashboards`) 容器。 |
| `docker-compose-dataprepper.yaml` | 定義 Data Prepper (`data-prepper`) 容器。 |
| `fluent-bit.conf` | 設定 Fluent Bit 讀取 `test.log`，並將每一個新的一列傳送至 Data Prepper。 |
| `log_pipeline.yaml` | 定義 Data Prepper 管線，使用 `COMMONAPACHELOG` grok 模式解析每個記錄列，並寫入 `apache_logs` 索引。 |
| `test.log` | Fluent Bit 讀取的記錄檔。 |

範例在 `docker-compose.yaml` 與 `log_pipeline.yaml` 中，將 OpenSearch `admin` 密碼設為 `Developer@123`。若要使用不同的密碼，請在啟動容器前於兩個檔案中變更它。

複製 Data Prepper 儲存庫並前往範例目錄：

```bash
git clone https://github.com/opensearch-project/data-prepper.git
cd data-prepper/examples/log-ingestion
```
{% include copy.html %}

## 步驟 2：為每個記錄事件加入時間戳記

作業面板（Operational panels）會依時間篩選每個視覺化，因此索引必須包含 `date` 類型的欄位。記錄列包含時間戳記，但 grok 模式會將它儲存為文字。若要加入 `date` 欄位，請在 `log_pipeline.yaml` 的 `processor` 清單中，於 `grok` 處理器之後加入 [`date` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/date/)。更新後的檔案包含下列管線：

```yaml
log-pipeline:
  source:
    http:
      ssl: false
  processor:
    - grok:
        match:
          log: [ "%{COMMONAPACHELOG}" ]
    - date:
        from_time_received: true
        destination: "@timestamp"
  sink:
    - opensearch:
        hosts: [ "https://opensearch:9200" ]
        insecure: true
        username: admin
        password: Developer@123
        index: apache_logs
```
{% include copy.html %}

`date` 處理器會將 `@timestamp` 欄位設為 Data Prepper 接收各事件的時間。使用接收時間可讓範例事件（其記錄列來自 2021 年）落在本教學所用 OpenSearch Dashboards 頁面的預設時間範圍內。

## 步驟 3：啟動容器

使用單一命令啟動兩個 Docker Compose 檔案中的容器：

```bash
docker compose -f docker-compose.yaml -f docker-compose-dataprepper.yaml up -d
```
{% include copy.html %}

兩個檔案必須在同一個命令中指定，讓所有四個容器加入同一個 Docker 網路。如果您分別啟動檔案，Fluent Bit 將無法連至 Data Prepper，Data Prepper 也無法連至 OpenSearch，導致沒有任何資料被編製索引。

請等待 Data Prepper 準備好接收資料。持續執行以下命令，直到輸出包含類似 `Started http source on port 2021` 的一列：

```bash
docker logs data-prepper 2>&1 | grep "Started http source"
```
{% include copy.html %}

Data Prepper 會在連接到 OpenSearch 之後才啟動管線，這可能需要一分鐘或更久的時間。如果您在 Data Prepper 準備好之前就寫入記錄資料，Fluent Bit 可能會在傳送失敗後捨棄資料。

## 步驟 4：傳送記錄資料

將下列記錄列附加至 `test.log`：

```bash
cat >> test.log <<'EOF'
63.173.168.120 - - [04/Nov/2021:15:07:25 -0500] "GET /search/tag/list HTTP/1.0" 200 5003
10.0.0.5 - - [04/Nov/2021:15:08:01 -0500] "GET /index.html HTTP/1.1" 200 1024
10.0.0.7 - - [04/Nov/2021:15:08:12 -0500] "POST /login HTTP/1.1" 401 512
10.0.0.9 - - [04/Nov/2021:15:09:44 -0500] "GET /missing HTTP/1.1" 404 210
10.0.0.5 - - [04/Nov/2021:15:10:02 -0500] "GET /cart HTTP/1.1" 500 98
EOF
```
{% include copy.html %}

Fluent Bit 會收集記錄列並將它們傳送至 Data Prepper。若要確認已傳送，請執行 `docker logs fluent-bit`。輸出會包含類似下面的一列：

```text
[2026/10/27 22:51:53.623] [ info] [output:http:http.0] data-prepper:2021, HTTP status=200
```

## 步驟 5：在 OpenSearch 中搜尋資料

Data Prepper 會解析每個記錄列，並依 `log_pipeline.yaml` 中的定義將它寫入 `apache_logs` 索引。Data Prepper 以批次方式將文件傳送至 OpenSearch，因此文件可能需要一分鐘或更久才會出現。若要查看第一份文件，請執行以下命令：

```bash
curl -X GET -u 'admin:Developer@123' -k 'https://localhost:9200/apache_logs/_search?pretty&size=1'
```
{% include copy.html %}

回應包含解析後的記錄資料，包括由 `date` 處理器加入的 `@timestamp` 欄位。`date` 欄位包含 Fluent Bit 讀取該列時的 epoch 秒數時間，由 Fluent Bit HTTP 輸出加入：

```json
{
  "took" : 6,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 5,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "apache_logs",
        "_id" : "B0Oif6EBGoQmkf_UZoQh",
        "_score" : 1.0,
        "_source" : {
          "date" : 1.793142650955058E9,
          "log" : "63.173.168.120 - - [04/Nov/2021:15:07:25 -0500] \"GET /search/tag/list HTTP/1.0\" 200 5003",
          "request" : "/search/tag/list",
          "auth" : "-",
          "ident" : "-",
          "response" : "200",
          "bytes" : "5003",
          "clientip" : "63.173.168.120",
          "verb" : "GET",
          "httpversion" : "1.0",
          "timestamp" : "04/Nov/2021:15:07:25 -0500",
          "@timestamp" : "2026-10-27T23:10:51.594Z"
        }
      }
    ]
  }
}
```

## 步驟 6：建立儀表板

前往 [http://localhost:5601](http://localhost:5601)，以 `admin` 使用者身分並使用密碼 `Developer@123` 登入。然後建立一個作業面板（operational panel）來容納您的視覺化：

1. 在頂端選單中，前往 **Observability** > **Dashboards**。
1. 選取 **Create Dashboard**。
1. 在 **Name** 中輸入 `Web traffic`，然後選取 **Create**。

## 步驟 7：查詢並視覺化記錄

使用事件分析（Event analytics）查詢記錄，並將視覺化儲存到儀表板：

1. 在頂端選單中，前往 **Observability** > **Logs**，然後選取 **Event Explorer**。
1. 在查詢編輯器中，輸入下列 PPL 查詢，它會統計每個 HTTP 方法的記錄事件數：

   ```sql
   source = apache_logs | stats count() by verb
   ```
{% include copy.html %}

1. 選取 **Run**。**Events** 標籤會列出結果。如果沒有出現結果，請使用時間選擇器選取包含您傳送記錄資料時間的時間範圍。
1. 選取 **Visualizations** 標籤。結果會以垂直長條圖顯示，每個 HTTP 方法一根長條。
1. 選取 **Save**。在 **Custom operational dashboards/application** 中選取 **Web traffic**。在 **Name** 中輸入 `Requests by method`，然後選取 **Save**。
1. 在頂端選單中，前往 **Observability** > **Dashboards**，然後選取 **Web traffic**。儀表板包含 **Requests by method** 視覺化。

## 步驟 8：清理

若要停止容器並刪除其資料，請執行以下命令：

```bash
docker compose -f docker-compose.yaml -f docker-compose-dataprepper.yaml down -v
```
{% include copy.html %}

## 後續步驟

- 若要了解記錄、追蹤與指標如何送達 OpenSearch，請參閱 [匯入可觀測性資料]({{site.url}}{{site.baseurl}}/observing-your-data/ingesting-observability-data/)。
- 若要進一步了解 PPL 查詢與視覺化，請參閱 [事件分析]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/)。
- 若要在可觀測性（Observability）工作區中探索記錄，請參閱 [記錄]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/discover-logs/)。
- 若要進一步了解 Data Prepper 管線，請參閱 [將記錄資料匯入 OpenSearch]({{site.url}}{{site.baseurl}}/data-prepper/getting-started/ingesting-log-data/)。
