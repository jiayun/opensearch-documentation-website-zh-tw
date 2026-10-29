---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料匯入管線"
nav_order: 5
nav_exclude: true
has_toc: true
permalink: /ingest-pipelines/
redirect_from:
   - /api-reference/ingest-apis/ingest-pipelines/
   - /ingest-pipelines/index/
---

# 資料匯入管線

_資料匯入管線_ (ingest pipeline) 是一連串的[處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)，會在文件匯入索引時套用到文件上。每個處理器執行特定的工作，例如篩選、轉換或充實資料。處理器依照列出的順序執行，且每個處理器會接收前一個處理器的輸出。在所有處理器執行完畢後，修改過的文件就會出現在您的索引中。

例如，類似 `203.0.113.24 GET /cart/checkout 200` 這樣的網頁伺服器記錄檔資料列會以單一字串的形式送達。管線可以將它拆分為獨立的 `client_ip`、`method`、`path` 和 `status` 欄位，讓您能夠對每個欄位進行搜尋、篩選和彙總。本頁的[範例](#example-parsing-web-server-logs)會建立這個管線。

## 資料匯入管線與 Data Prepper 的比較

資料匯入管線在 OpenSearch 叢集的節點上執行，並在每份文件編製索引時進行處理。[Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 則以獨立服務的形式在叢集外部執行，並將處理後的資料傳送至 OpenSearch。

若您需要對個別文件進行輕量轉換，例如解析欄位，或使用在 OpenSearch 中註冊的模型產生向量嵌入，請使用資料匯入管線。若您需要處理大量資料、來自多個來源的資料，或跨多份文件的處理（例如彙總事件），請使用 Data Prepper。將處理作業移至 Data Prepper 也能減輕叢集的處理負載。

## 必要條件 

以下是使用資料匯入管線的必要條件：

- 至少一個具有 `ingest` 角色的節點。預設情況下，每個節點都具有此角色，因此無需任何設定。
- 如果已啟用 OpenSearch Security 外掛程式，您必須具備管理資料匯入管線的權限，例如透過 `cluster_manage_pipelines` 動作群組。如需更多資訊，請參閱[資料匯入 API]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/#required-permissions)。

在生產環境中，您可以透過在 `node.roles` 設定中僅將 `ingest` 角色指派給特定節點，讓這些節點專門處理匯入作業。如需更多資訊，請參閱[叢集形成]({{site.url}}{{site.baseurl}}/tuning-your-cluster/creating-a-cluster/)。
{: .tip}

## 定義管線

若要定義管線，請在 `processors` 陣列中依執行順序列出要執行的處理器。您也可以選擇在 `description` 欄位中描述該管線。

每個處理器都是一個物件，其鍵為處理器類型，其值則包含該處理器的參數。下列管線定義包含兩個處理器。`lowercase` 處理器會將 `category` 欄位轉為小寫，接著 `set` 處理器會新增一個值為 `true` 的 `in_stock` 欄位：

```json
{
  "description": "Normalizes product data",
  "processors": [
    {
      "lowercase": {
        "field": "category"
      }
    },
    {
      "set": {
        "field": "in_stock",
        "value": true
      }
    }
  ]
}
```

每種處理器類型都有各自的參數。各處理器的參數請參閱[資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)。

管線定義也可以包含下列選用欄位：

- `version`：版本號碼，可用來追蹤管線的變更。如需詳細資訊，請參閱[管線版本控制]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#pipeline-versioning)。
- `on_failure`：當管線中的處理器失敗且未自行處理該失敗時，要執行的處理器。如需詳細資訊，請參閱[在管線層級處理失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/#handling-failures-at-the-pipeline-level)。

## 範例：剖析 Web 伺服器記錄檔

下列範例會建立一個管線，將 Web 伺服器記錄檔的每一行剖析成獨立的欄位，接著測試該管線，然後使用它為文件編製索引。

建立一個名為 `parse-web-logs` 的管線。`dissect` 處理器會將 `message` 欄位拆分為四個欄位，`convert` 處理器會將 `status` 轉換為整數，而 `remove` 處理器則會刪除原始的 `message` 欄位。在 `dissect` 模式中，每個 `%{name}` 會擷取到下一個空格之前的文字，並將它儲存在以該名稱命名的欄位中：

```json
PUT _ingest/pipeline/parse-web-logs
{
  "description": "Parses web server log lines",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{client_ip} %{method} %{path} %{status}"
      }
    },
    {
      "convert": {
        "field": "status",
        "type": "integer"
      }
    },
    {
      "remove": {
        "field": "message"
      }
    }
  ]
}
```
{% include copy-curl.html %}

在不編製索引的情況下，對範例文件測試該管線：

```json
POST _ingest/pipeline/parse-web-logs/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "203.0.113.24 GET /cart/checkout 200"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會顯示文件若編製索引時會呈現的樣子。`message` 欄位已消失，記錄檔行被拆分為四個欄位，而 `status` 現在是數字 `200` 而不是字串：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "path": "/cart/checkout",
          "client_ip": "203.0.113.24",
          "method": "GET",
          "status": 200
        },
        "_ingest": {
          "timestamp": "2026-10-14T21:15:18.025620512Z"
        }
      }
    }
  ]
}
```

### 將管線套用至文件

若要使用管線處理文件，請在索引請求的 `pipeline` 查詢參數中指定管線 ID。[Index Document]({{site.url}}{{site.baseurl}}/api-reference/document-apis/index-document/)、[Bulk]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/) 與 [Update by Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) API 皆支援此參數。對於 [Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) API，請在 `dest.pipeline` 請求本文欄位中指定管線。

下列請求使用 `parse-web-logs` 管線為文件編製索引：

```json
PUT web-logs/_doc/1?pipeline=parse-web-logs
{
  "message": "203.0.113.24 GET /cart/checkout 200"
}
```
{% include copy-curl.html %}

若要驗證結果，請擷取該文件：

```json
GET web-logs/_doc/1
```
{% include copy-curl.html %}

儲存的文件包含解析後的欄位：

```json
{
  "_index": "web-logs",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "path": "/cart/checkout",
    "method": "GET",
    "client_ip": "203.0.113.24",
    "status": 200
  }
}
```

您也可以使用下列索引設定，設定對索引中每份文件自動執行的管線：

- `index.default_pipeline`：當索引請求未指定 `pipeline` 參數時執行的管線。若要對某個請求略過預設管線，請將 `pipeline` 設為 `_none`。
- `index.final_pipeline`：在請求管線或預設管線之後執行的管線。最終管線一律會執行，即使請求將 `pipeline` 設為 `_none` 亦然。請使用最終管線來處理每份文件都必須接受的作業，例如新增匯入時間戳記，無論請求指定的是哪個管線。最終管線無法變更文件的目標索引；若它變更了 `_index`，該文件將會失敗。

若要試用最終管線設定，請先建立一個名為 `add-ingest-time` 的管線，記錄每份文件的匯入時間。{% raw %}`{{_ingest.timestamp}}`{% endraw %} 範本會插入 OpenSearch 接收文件的時間。如需範本與中繼資料的詳細資訊，請參閱[存取管線中的資料]({{site.url}}{{site.baseurl}}/ingest-pipelines/accessing-data/)：

```json
PUT _ingest/pipeline/add-ingest-time
{
  "processors": [
    {
      "set": {
        "field": "ingested_at",
        "value": "{% raw %}{{_ingest.timestamp}}{% endraw %}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

下列請求建立一個名為 `web-logs-v2` 的索引，該索引預設執行 `parse-web-logs` 管線，並對每份文件執行 `add-ingest-time` 管線：

```json
PUT web-logs-v2
{
  "settings": {
    "index.default_pipeline": "parse-web-logs",
    "index.final_pipeline": "add-ingest-time"
  }
}
```
{% include copy-curl.html %}

如需這些設定的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。

## 資料匯入管線的常見用途

下表列出常見工作及其對應的處理器。完整清單請參閱[資料匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)。

工作 | 處理器
:--- | :---
剖析記錄檔行及其他非結構化文字並轉換為欄位 | [`grok`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/grok/), [`dissect`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/dissect/), [`kv`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/kv/), [`csv`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/csv/)
新增、重新命名、複製或移除欄位 | [`set`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/set/), [`rename`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/rename/), [`copy`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/copy/), [`remove`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/remove/)
轉換資料類型與格式 | [`convert`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/convert/), [`date`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/date/), [`json`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/json/), [`bytes`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/bytes/)
產生用於語意搜尋的向量嵌入 | [`text_embedding`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-embedding/), [`sparse_encoding`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/), [`text_image_embedding`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-image-embedding/)
根據 IP 位址新增地理資訊 | [`ip2geo`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ip2geo/)
捨棄文件或將其路由至其他索引 | [`drop`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/drop/), [`date_index_name`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/date-index-name/), [`set`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/set/)（作用於 `_index` 欄位）
套用自訂邏輯 | [`script`]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/script/)

## 儲存管線

OpenSearch 會將管線定義儲存在叢集狀態中。當您在 `include_global_state` 設為 `true` 的情況下建立快照時，快照會包含這些管線定義。如需更多資訊，請參閱[全域叢集狀態]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#global-cluster-state)。

## 資料匯入管線 API

OpenSearch 支援下列資料匯入管線 API：

- [建立管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/)
- [測試管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/simulate-ingest/)
- [擷取管線的相關資訊]({{site.url}}{{site.baseurl}}/ingest-pipelines/get-ingest/)
- [刪除管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/delete-ingest/)

## 相關文件

- [在 OpenSearch 中使用匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)
- [在管線中存取文件欄位與中繼資料]({{site.url}}{{site.baseurl}}/ingest-pipelines/accessing-data/)
- [有條件地執行處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/conditional-execution/)
- [處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)
