---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "計數"
parent: Search APIs
nav_order: 35
redirect_from:
 - /opensearch/rest-api/count/
 - /api-reference/count/
---

# Count API
**於 1.0 版引入**
{: .label .label-purple }

Count API 會傳回符合查詢的文件數量。您可以使用此 API 取得索引、資料串流或叢集的文件數量。常見的使用案例包括：

- 取得索引或資料串流中的文件總數，而不擷取實際文件。
- 計算符合特定條件的文件數量，以驗證資料是否已正確編製索引。
- 追蹤不同時間區間的文件數量，以監控資料隨時間的成長情形。
- 在執行耗費資源的搜尋作業之前，先取得符合條件的文件數量，以驗證查詢結果。

當您只需要文件數量時，Count API 比使用搭配 `size: 0` 的 Search API 更有效率，因為它專門針對計數作業進行最佳化。為了提升效能，OpenSearch 會將計數查詢分散到所有分片上平行執行。每個分片會使用其中一個可用副本來處理請求，因此可隨著副本數量增加而水平擴充。

或者，您可以使用 [CAT Indices API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-indices/) 或 [CAT Count API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-count/) 取得每個索引或資料串流中的文件數量。
{: .note }

<!-- spec_insert_start
api: count
component: endpoints
-->
## 端點
```json
GET  /_count
POST /_count
GET  /{index}/_count
POST /{index}/_count
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: count
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 清單或字串 | 要搜尋的資料串流、索引和別名清單，以逗號分隔。支援萬用字元（`*`）。若要搜尋所有資料串流和索引，請省略此參數，或使用 `*` 或 `_all`。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: count
component: query_parameters
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 值僅以不存在或已關閉的索引為目標時，請求會傳回錯誤。即使請求也以其他開啟的索引為目標，此行為仍適用。 | N/A |
| `analyze_wildcard` | 布林值 | 若為 `true`，則會分析萬用字元和前綴查詢。只有在指定 `q` 查詢字串參數時，才能使用此參數。 | `false` |
| `analyzer` | 字串 | 用於查詢字串的分析器。只有在指定 `q` 查詢字串參數時，才能使用此參數。 | N/A |
| `default_operator` | 字串 | 查詢字串查詢的預設運算子：`AND` 或 `OR`。只有在指定 `q` 查詢字串參數時，才能使用此參數。<br> 有效值為：`and`、`AND`、`or` 和 `OR`。 | N/A |
| `df` | 字串 | 當查詢字串中未提供欄位前綴時，作為預設使用的欄位。只有在指定 `q` 查詢字串參數時，才能使用此參數。 | N/A |
| `expand_wildcards` | 清單或字串 | 指定萬用字元運算式可符合的索引類型。支援以逗號分隔的值。<br> 有效值為：<br> - `all`：符合任何索引，包括隱藏索引。<br> - `closed`：符合已關閉的非隱藏索引。<br> - `hidden`：符合隱藏索引。必須與 `open`、`closed` 或兩者搭配使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：符合開啟的非隱藏索引。 | N/A |
| `ignore_throttled` | 布林值 | 若為 `true`，則會忽略已凍結的具體索引、展開後的索引或透過別名指定的索引。 | N/A |
| `ignore_unavailable` | 布林值 | 若為 `false`，當請求以不存在或已關閉的索引為目標時，會傳回錯誤。 | N/A |
| `lenient` | 布林值 | 若為 `true`，則會忽略查詢字串中因格式造成的查詢失敗（例如向數值欄位提供文字）。 | N/A |
| `min_score` | 浮點數 | 設定文件必須具有的最低 `_score` 值，才會納入結果。 | N/A |
| `preference` | 字串 | 指定應執行作業的節點或分片。預設為隨機選取。 | `random` |
| `q` | 字串 | 使用 Lucene 查詢字串語法的查詢。 | N/A |
| `routing` | 清單或字串 | 用於將作業路由至特定分片的自訂值。 | N/A |
| `terminate_after` | 整數 | 每個分片要收集的文件數量上限。如果查詢達到此限制，OpenSearch 會提前終止查詢。OpenSearch 會先收集文件，再進行排序。 | N/A |

<!-- spec_insert_end -->

## 請求本文欄位

請求本文為選用。您可以使用 Query DSL 定義查詢，並透過請求本文限制結果。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 用於篩選文件的查詢。如果未指定，則會使用 `match_all` 查詢來計算目標中的所有文件。如需 OpenSearch 查詢的詳細資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。

## 範例：計算叢集中的所有文件

下列範例請求會傳回整個叢集中所有文件的總數：

<!-- spec_insert_start
component: example_code
rest: GET /_count
-->
{% capture step1_rest %}
GET /_count
{% endcapture %}

{% capture step1_python %}


response = client.count(
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：計算多個索引中的所有文件

下列範例請求會傳回 `movies` 和 `tv_shows` 索引中所有文件的總數：

<!-- spec_insert_start
component: example_code
rest: GET /movies,tv_shows/_count
-->
{% capture step1_rest %}
GET /movies,tv_shows/_count
{% endcapture %}

{% capture step1_python %}


response = client.count(
  index = "movies,tv_shows",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：計算符合查詢的文件

下列範例請求會計算 `movies` 索引中 `genre` 欄位為 `drama` 的文件數量：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_count
body: |
{
  "query": {
    "term": {
      "genre": "drama"
    }
  }
}
-->
{% capture step1_rest %}
POST /movies/_count
{
  "query": {
    "term": {
      "genre": "drama"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.count(
  index = "movies",
  body =   {
    "query": {
      "term": {
        "genre": "drama"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用查詢字串計算文件

下列範例請求會使用 `q` 查詢參數，計算 `genre` 欄位為 `drama` 的文件數量：

<!-- spec_insert_start
component: example_code
rest: GET /movies/_count?q=genre:drama
-->
{% capture step1_rest %}
GET /movies/_count?q=genre:drama
{% endcapture %}

{% capture step1_python %}


response = client.count(
  index = "movies",
  params = { "q": "genre:drama" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：提前終止文件計數

下列範例請求會使用 `terminate_after` 參數，在找到三份符合條件的文件後停止計數：

<!-- spec_insert_start
component: example_code
rest: POST /movies/_count?terminate_after=3
body: |
{
  "query": {
    "match_all": {}
  }
}
-->
{% capture step1_rest %}
POST /movies/_count?terminate_after=3
{
  "query": {
    "match_all": {}
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.count(
  index = "movies",
  params = { "terminate_after": "3" },
  body =   {
    "query": {
      "match_all": {}
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

下列範例回應顯示文件數量和分片資訊：

```json
{
  "count" : 7,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  }
}
```

使用 `terminate_after` 參數時，回應會包含 `terminated_early` 欄位：

```json
{
  "terminated_early" : true,
  "count" : 7,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  }
}
```

## 回應本文欄位

Count API 回應包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`count` | 整數 | 符合查詢的文件總數。如果未提供查詢，則代表指定目標中的所有文件。
`_shards` | 物件 | 包含參與計數作業的分片資訊。
`_shards.total` | 整數 | 計數作業所查詢的分片總數。
`_shards.successful` | 整數 | 成功執行計數作業的分片數量。
`_shards.skipped` | 整數 | 計數作業期間略過的分片數量。如果分片不包含任何符合查詢的文件，則可能會略過該分片。
`_shards.failed` | 整數 | 未能執行計數作業的分片數量。如果此值大於 0，請檢查您的叢集健康狀態和分片配置。
`terminated_early` | 布林值 | 僅在使用 `terminate_after` 查詢參數時出現。當值為 `true` 時，表示計數作業在所有符合條件的文件計數完成之前就已終止。

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:data/read/search`。
