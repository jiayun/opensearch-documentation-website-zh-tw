---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄檔匯入"
nav_order: 10
redirect_from:
  - /observability-plugin/log-analytics/
---

# 記錄檔匯入

記錄檔匯入提供一種方式，可將非結構化的記錄資料轉換為結構化資料並匯入 OpenSearch。結構化的記錄資料可在搜尋事件記錄時，依據資料格式進行更佳的查詢與篩選。

## 開始使用記錄檔匯入

OpenSearch 記錄檔匯入由三個元件組成：[Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/)、[OpenSearch]({{site.url}}{{site.baseurl}}/quickstart/) 與 [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/index/)。Data Prepper 儲存庫包含數個[範例應用程式](https://github.com/opensearch-project/data-prepper/tree/main/examples)，您可以用來入門。

### 資料的基本流程

![從分散式應用程式到 OpenSearch 的記錄資料流程圖]({{site.url}}{{site.baseurl}}/images/la.png)

1. 記錄檔匯入依賴您在應用程式的環境中加入記錄收集機制，以收集並傳送記錄資料。

   （在下列[範例](#example)中，使用 [Fluent Bit](https://docs.fluentbit.io/manual/) 作為記錄收集器，從檔案收集記錄資料並傳送至 Data Prepper）。

2. [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 接收記錄資料，將資料轉換為結構化格式，並在 OpenSearch 叢集上編製索引。

3. 之後即可透過 OpenSearch 搜尋查詢或 OpenSearch Dashboards 的 **Discover** 頁面來探索資料。

### 範例

此範例模擬將記錄項目寫入記錄檔，再由 Data Prepper 處理並儲存至 OpenSearch。

此範例位於 [Data Prepper 儲存庫](https://github.com/opensearch-project/data-prepper)的 `examples/log-ingestion/` 目錄中，包含下列檔案。

| 檔案 | 說明 |
|:---|:---|
| `docker-compose.yaml` | 定義 [Fluent Bit](https://docs.fluentbit.io/manual/)（`fluent-bit`）、單一節點 OpenSearch 叢集（`opensearch`）與 OpenSearch Dashboards（`dashboards`）容器。 |
| `docker-compose-dataprepper.yaml` | 定義 Data Prepper（`data-prepper`）容器。 |
| `fluent-bit.conf` | 設定 Fluent Bit 讀取 `test.log`，並將每一行新內容傳送至 Data Prepper。 |
| `log_pipeline.yaml` | 定義 Data Prepper 管線，使用 `COMMONAPACHELOG` grok 模式解析每一行記錄，並寫入 `apache_logs` 索引。 |
| `test.log` | Fluent Bit 讀取的記錄檔。 |

此範例在 `docker-compose.yaml` 與 `log_pipeline.yaml` 中都將 OpenSearch `admin` 密碼設為 `Developer@123`。若要使用不同的密碼，請在啟動容器前於這兩個檔案中修改。

若要執行此範例，請依照下列步驟操作：

1. 複製 Data Prepper 儲存庫並前往範例目錄：

   ```bash
   git clone https://github.com/opensearch-project/data-prepper.git
   cd data-prepper/examples/log-ingestion
   ```
   {% include copy.html %}

1. 使用單一命令啟動兩個 Docker Compose 檔案中的容器：

   ```bash
   docker compose -f docker-compose.yaml -f docker-compose-dataprepper.yaml up -d
   ```
   {% include copy.html %}

   兩個檔案必須在同一個命令中指定，讓全部四個容器加入同一個 Docker 網路。若分開啟動，Fluent Bit 將無法連線至 Data Prepper，Data Prepper 也無法連線至 OpenSearch，因此不會有任何資料被編製索引。

1. 等待 Data Prepper 準備好接收資料。重複執行下列命令，直到輸出包含類似 `Started http source on port 2021` 的一行為止：

   ```bash
   docker logs data-prepper 2>&1 | grep "Started http source"
   ```
   {% include copy.html %}

   Data Prepper 只有在連線至 OpenSearch 之後才會啟動管線，這可能需要一分鐘或更久。若在 Data Prepper 準備好之前寫入記錄資料，Fluent Bit 可能會在傳送失敗後捨棄該資料。

1. 在 `test.log` 附加一行記錄：

   ```bash
   echo '63.173.168.120 - - [04/Nov/2021:15:07:25 -0500] "GET /search/tag/list HTTP/1.0" 200 5003' >> test.log
   ```
   {% include copy.html %}

   Fluent Bit 會收集該行記錄並傳送至 Data Prepper。若要確認已送達，請執行 `docker logs fluent-bit`。輸出會包含類似以下的一行：

   ```
   [2026/10/06 15:29:12.026] [ info] [output:http:http.0] data-prepper:2021, HTTP status=200
   200 OK
   ```

1. Data Prepper 會解析該行記錄並寫入 `apache_logs` 索引，如 `log_pipeline.yaml` 中所定義。Data Prepper 以批次方式將文件傳送至 OpenSearch，因此文件可能需要一分鐘或更久才會出現。若要檢視該文件，請執行下列命令：

   ```bash
   curl -X GET -u 'admin:Developer@123' -k 'https://localhost:9200/apache_logs/_search?pretty&size=1'
   ```
   {% include copy.html %}

   回應會包含解析後的記錄資料：

   ```json
   {
     "took" : 18,
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
           "_index" : "apache_logs",
           "_id" : "zQHWEaEBgXJEccxmMBZy",
           "_score" : 1.0,
           "_source" : {
             "date" : 1.791300551511732E9,
             "log" : "63.173.168.120 - - [04/Nov/2021:15:07:25 -0500] \"GET /search/tag/list HTTP/1.0\" 200 5003",
             "request" : "/search/tag/list",
             "auth" : "-",
             "ident" : "-",
             "response" : "200",
             "bytes" : "5003",
             "clientip" : "63.173.168.120",
             "verb" : "GET",
             "httpversion" : "1.0",
             "timestamp" : "04/Nov/2021:15:07:25 -0500"
           }
         }
       ]
     }
   }
   ```

1. 若要在 OpenSearch Dashboards 中檢視資料，請前往 [http://localhost:5601](http://localhost:5601) 並以 `admin` 使用者身分登入。為 `apache_logs` 索引建立索引模式，然後在 **Discover** 頁面選取該索引模式。此索引不包含 `date` 類型的欄位，因此建立索引模式時請不指定時間欄位。如需更多資訊，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。

若要停止容器並刪除其資料，請執行下列命令：

```bash
docker compose -f docker-compose.yaml -f docker-compose-dataprepper.yaml down -v
```
{% include copy.html %}
