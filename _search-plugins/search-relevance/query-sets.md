---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢集"
nav_order: 3
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 查詢集

查詢集 (query set) 是一組查詢的集合。這些查詢用於搜尋相關性評估的實驗。Search Relevance Workbench 提供多種抽樣技術，可從符合 [User Behavior Insights (UBI)]({{site.url}}{{site.baseurl}}/search-plugins/ubi/schemas/) 規格的真實使用者資料建立查詢集。
此外，Search Relevance Workbench 也允許您匯入查詢集。

## 建立查詢集

如果您使用 UBI 規格追蹤使用者行為，可以從多種抽樣方法中選擇，根據儲存在 `ubi_queries` 索引中的真實使用者查詢建立查詢集。若要從名稱不同的索引抽樣，請使用 `ubiQueriesIndex` 參數。

Search Relevance Workbench 支援三種抽樣方法：
* Random：從所有查詢中隨機抽樣。
* [Probability-Proportional-to-Size Sampling](https://opensourceconnections.com/blog/2022/10/13/how-to-succeed-with-explicit-relevance-evaluation-using-probability-proportional-to-size-sampling/)：以頻率加權方式從所有查詢中抽樣，以取得具代表性的樣本。
* Top N：取最常出現的前 N 個查詢。

### 端點

```json
POST _plugins/_search_relevance/query_sets
```

### 請求本文欄位

下表列出可用的輸入參數。

欄位 | 資料類型 |  描述
:---  | :--- | :---
`name` | 字串 | 查詢集的名稱。最大長度為 50 個字元。
`description` | 字串 | 查詢集的簡短描述。最大長度為 250 個字元。
`sampling` | 字串 | 定義要使用的抽樣器。有效值為 `pptss`（機率與大小成比例的抽樣）、`random`、`topn`（最常出現的查詢）與 `manual`。
`querySetSize` | 整數 | 查詢集中的目標查詢數量。視 `ubi_queries` 中唯一查詢的數量而定，產生的查詢集可能包含較少的查詢。必須為正整數。
`ubiQueriesIndex` | 字串 | 選用的索引名稱，該索引包含要抽樣的 UBI 查詢。預設為 `ubi_queries`。當您的 UBI 查詢儲存在名稱不同的索引時，請指定此參數。

### 範例請求：使用 Top N 抽樣器抽樣 20 個查詢

```json
POST _plugins/_search_relevance/query_sets
{
  "name": "Top 20",
  "description": "Top 20 most frequent queries sourced from user searches.",
  "sampling": "topn",
  "querySetSize": 20
}
```

### 範例請求：手動上傳查詢集

```json
PUT _plugins/_search_relevance/query_sets
{
   	"name": "TVs",
   	"description": "TV queries",
   	"sampling": "manual",
   	"querySetQueries": [
      {
        "queryText": "tv"
      },
      {
        "queryText": "led tv"
      }
    ]
}
```

## 查詢集格式

Search Relevance Workbench 支援兩種查詢集格式，各自適用於不同的使用情境。兩種格式都是使用者查詢的集合，差別在於是否包含預期答案。

* **基本查詢集**：僅包含使用者查詢的清單，不含其他資訊。適用於不需要特定答案的一般相關性測試。

* **含參考答案的查詢集**：使用者查詢的清單，其中每個查詢都與其預期答案配對。此格式特別適合評估設計為提供特定答案的應用程式，例如問答系統。

### 欄位

所有查詢集都由一或多個項目組成。每個項目都是一個 JSON 物件，包含下列欄位。

| 欄位 | 資料類型 | 描述 |
| :--- | :--- | :--- |
| `queryText` | 字串 | 使用者查詢字串。必要。 |
| `referenceAnswer` | 字串 | 使用者查詢的預期或正確答案。此欄位用於產生判斷 (judgment)，尤其是搭配大型語言模型 (LLM) 時。選用。 |
| 自訂欄位 | 字串 | `queryText` 與 `referenceAnswer` 以外的任何欄位都會以自訂欄位的形式儲存在項目中。您可以在搜尋組態中，以自訂欄位的名稱作為 [Mustache 模板變數]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/#using-mustache-templates) 來參照它。選用。 |

### 基本查詢集範例

基本查詢集的每個項目只包含 `queryText` 欄位。適用於沒有單一「正確」答案的一般相關性測試。

#### 不含參考答案的查詢集範例

```json
{"queryText": "t towels kitchen"}
{"queryText": "table top bandsaw for metal"}
{"queryText": "tan strappy heels for women"}
{"queryText": "tank top plus size women"}
{"queryText": "tape and mudding tools"}
```

### 含參考答案的查詢集範例

在此格式中，每個項目都將 `queryText` 與 `referenceAnswer` 配對。用於評估會傳回特定答案的應用程式，例如聊天機器人或問答系統。

#### 含參考答案的查詢集範例

```json
{"queryText": "What is the capital of France?", "referenceAnswer": "Paris"}
{"queryText": "Who wrote 'Romeo and Juliet'?", "referenceAnswer": "William Shakespeare"}
{"queryText": "What is the chemical symbol for water?", "referenceAnswer": "H2O"}
{"queryText": "What is the highest mountain in the world?", "referenceAnswer": "Mount Everest"}
{"queryText": "When was the first iPhone released?", "referenceAnswer": "June 29, 2007"}
```

`referenceAnswer` 欄位在使用 [LLM 產生判斷]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/) 時特別有用。LLM 可以將參考答案作為基準事實，與擷取的搜尋結果比較，從而準確評分回應的相關性。

### 含自訂欄位的查詢集範例

除了 `queryText` 之外，每個項目還可以包含自訂欄位。您可以在[搜尋組態]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/#using-mustache-templates)中將這些欄位作為 Mustache 模板變數參照，讓同一個搜尋組態對每個查詢套用不同的篩選器或參數。

#### 含自訂欄位的查詢集範例

在下列範例中，每個項目都包含 `category` 自訂欄位。如果搜尋組態在其查詢中參照 `{{category}}`，就會依對應項目中的 `category` 值篩選每個查詢的結果：

```json
{"queryText": "phone", "category": "electronics"}
{"queryText": "steel", "category": "materials"}
{"queryText": "keyboard", "category": "electronics"}
```

## 管理查詢集

您可以使用下列 API 擷取或刪除查詢集。

### 擷取查詢集

此 API 會擷取可用的查詢集。

#### 端點

```json
GET _plugins/_search_relevance/query_sets
GET _plugins/_search_relevance/query_sets/{query_set_id}
```

#### 範例回應

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "search-relevance-queryset",
        "_id": "bb45c4c4-48ce-461b-acbc-f154c0a17ec9",
        "_score": null,
        "_source": {
          "id": "bb45c4c4-48ce-461b-acbc-f154c0a17ec9",
          "name": "TVs",
          "description": "Some TVs that people might want",
          "sampling": "manual",
          "timestamp": "2025-06-11T13:43:26.676Z",
          "querySetQueries": [
            {
              "queryText": "tv"
            },
            {
              "queryText": "led tv"
            }
          ]
        },
        "sort": [
          1749649406676
        ]
      }
    ]
  }
}
```

### 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 描述 |
| :--- | :--- | :--- |
| `query_set_id` | 字串 | 要擷取的查詢集 ID。留空時擷取所有查詢集。 |

### 刪除查詢集

您可以使用查詢集 ID 刪除查詢集。

#### 端點

```json
DELETE _plugins/_search_relevance/query_sets/{query_set_id}
```

#### 範例請求

```json
DELETE _plugins/_search_relevance/query_sets/bb45c4c4-48ce-461b-acbc-f154c0a17ec9
```

#### 範例回應

```json
{
  "_index": "search-relevance-queryset",
  "_id": "bb45c4c4-48ce-461b-acbc-f154c0a17ec9",
  "_version": 2,
  "result": "deleted",
  "forced_refresh": true,
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 17,
  "_primary_term": 1
}
```

### 搜尋查詢集

您可以使用 Query DSL 搜尋可用的查詢集。

#### 端點

```json
GET _plugins/_search_relevance/query_sets/_search
POST _plugins/_search_relevance/query_sets/_search
```

#### 範例請求

搜尋包含含有片語 `lamp without cord` 之查詢的查詢集：

```json
GET _plugins/_search_relevance/query_sets/_search
{
  "query": {
    "nested": {
      "path": "querySetQueries",
      "query": {
        "match_phrase": {
          "querySetQueries.queryText": "lamp without cord"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例回應

回應包含符合的查詢集，因為 `wall lamp without cord` 包含部分搜尋詞 `lamp without cord`：

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "search-relevance-queryset",
        "_id": "4622775e-9099-4375-af7f-f970dae25f09",
        "_score": 1,
        "_source": {
          "id": "4622775e-9099-4375-af7f-f970dae25f09",
          "name": "ESCI Queries",
          "description": "Queries from the ESCI ranking task",
          "sampling": "manual",
          "timestamp": "2026-01-20T12:49:35.940Z",
          "querySetQueries": [
            {
              "queryText": "tv"
            },
            {
              "queryText": "wall lamp without cord"
            }
          ]
        }
      }
    ]
  }
}
```
