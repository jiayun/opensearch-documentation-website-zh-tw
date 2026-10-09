---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Search Relevance Stats API
nav_order: 65
parent: Compare Search Results
grand_parent: Optimizing search quality
has_children: false
---

# Search Relevance Stats API
2.7 版引進
{: .label .label-purple }

Search Relevance Stats API 提供 [Search Relevance 外掛程式](https://github.com/opensearch-project/dashboards-search-relevance)作業的相關資訊。Search Relevance 外掛程式會處理 [Compare Search Results]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/) Dashboards 工具所送出的作業。

Search Relevance Stats API 會擷取收到請求當下那一分鐘區間的統計資料。舉例來說，若在 23:59:59.004 收到請求，則會收集 23:58:00.000--23:58:59.999 時間區間的統計資料。

如要變更收集統計資料的預設時間區間，請在 `opensearch_dashboards.yml` 檔案中將 `searchRelevanceDashboards.metrics.metricInterval` 設定更新為新的時間區間（以毫秒為單位）。`opensearch_dashboards.yml` 檔案位於 OpenSearch Dashboards 安裝目錄的 `config` 資料夾中。舉例來說，下列設定會將區間設為一秒：

```yml
searchRelevanceDashboards.metrics.metricInterval: 1000 
```

#### 範例請求

您可以在下列格式中提供 Search Relevance Stats API 的 URL 位址來存取該 API：

```
<opensearch-dashboards-endpoint-address>/api/relevancy/stats
```

若 OpenSearch 組態檔中指定了連接埠號，OpenSearch Dashboards 端點位址可能會包含該連接埠號。具體的 URL 格式取決於 OpenSearch 部署類型及其所在的網路環境。
{: .note}

您可以用兩種方式查詢端點：
  
  - 在瀏覽器中存取端點位址 (例如 `http://localhost:5601/api/relevancy/stats`)

  - 在終端機中使用 `curl` 命令：
    ```bash
    curl -X GET http://localhost:5601/api/relevancy/stats
    ```
    {% include copy.html %}

#### 範例回應

以下是前述請求的回應：

```json
{
  "data": {
    "search_relevance": {
      "fetch_index": {
        "200": {
          "response_time_total": 28.79286289215088,
          "count": 1
        }
      },
      "single_search": {
        "200": {
          "response_time_total": 29.817723274230957,
          "count": 1
        }
      },
      "comparison_search": {
        "200": {
          "response_time_total": 13.265346050262451,
          "count": 2
        }
      }
    }
  },
  "overall": {
    "response_time_avg": 17.968983054161072,
    "requests_per_second": 0.06666666666666667
  },
  "counts_by_component": {
    "search_relevance": 4
  },
  "counts_by_status_code": {
    "200": 4
  }
}
```

## 回應本文欄位

下表列出所有回應欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- | 
| [`data.search_relevance`](#the-datasearch_relevance-object) | 物件 | 與 Search Relevance 作業相關的統計資料。 |
| `overall` | 物件 | 所有作業的平均統計資料。 |
| `overall.response_time_avg` | Double | 所有作業的平均回應時間（以毫秒為單位）。 |
| `overall.requests_per_second` | Double | 所有作業平均每秒的請求數。 |
| `counts_by_component` | 物件 | `data` 物件之所有子物件的所有 `count` 值總和。 |
| `counts_by_component.search_relevance` | `search_relevance` 物件中所有作業的回應總數。 |
| `counts_by_status_code` | 物件 | 包含所有 Search Relevance 作業的回應碼及其計數清單。 |

### `data.search_relevance` 物件

`data.search_relevance` 物件包含下表所述的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `comparison_search` | 物件 | 與比較搜尋作業相關的統計資料。比較搜尋作業是指在 Compare Search Results 工具中同時輸入 Query 1 和 Query 2 時，用來比較兩個查詢的請求。 |
| `single_search` | 物件 | 與單一搜尋作業相關的統計資料。單一搜尋作業是指在 Compare Search Results 工具中僅輸入 Query 1 或 Query 2（而非兩者）時，用來執行單一查詢的請求。 |
| `fetch_index` | 物件 | 與擷取比較搜尋或單一搜尋之索引相關的作業統計資料。 |

`comparison_search`、`single_search` 和 `fetch_index` 物件各包含一份 HTTP 回應碼清單。下表列出每個回應碼的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `response_time_total` | Double | 有此 HTTP 回應碼之回應的回應時間總和（以毫秒為單位）。 |
| `count` | 整數 | 有此 HTTP 回應碼的回應總數。  |
