---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "限制"
nav_order: 99
redirect_from:
  - /search-plugins/sql/limitation/
---

# SQL 與 PPL 限制

SQL 外掛程式有下列限制。

## 不支援對運算式進行彙總

您只能對欄位套用彙總。彙總無法接受運算式作為參數。例如，不支援 `avg(log(age))`。

## FROM 子句中的子查詢

`FROM` 子句中的子查詢，格式為：`SELECT outer FROM (SELECT inner)`，僅在查詢合併為單一查詢時才支援。例如，支援下列查詢：

```sql
SELECT t.f, t.d
FROM (
    SELECT FlightNum as f, DestCountry as d
    FROM opensearch_dashboards_sample_data_flights
    WHERE OriginCountry = 'US') t
```
{% include copy.html %}


但若外部查詢含有 `GROUP BY` 或 `ORDER BY`，則不支援。

## JOIN 查詢

由於 OpenSearch 原生不支援關聯式操作，`JOIN` 查詢僅以盡力而為的方式支援。

### JOIN 不支援對聯結結果進行彙總

`JOIN` 查詢不支援對聯結結果進行彙總。

例如，不支援 `SELECT depo.name, avg(empo.age) FROM empo JOIN depo WHERE empo.id = depo.id GROUP BY depo.name`。

### 效能

`JOIN` 查詢容易進行耗費資源的索引掃描操作。

`JOIN` 查詢在處理超過 500 萬筆相符記錄的結果集時，可能會遇到效能問題。
若要改善 `JOIN` 效能，請先篩選資料以減少聯結的記錄數。例如，將聯結限制在特定的索引鍵值範圍：

```sql
SELECT l.key, l.spanId, r.spanId
  FROM logs_left AS l
  JOIN logs_right AS r
  ON l.key = r.key
  WHERE l.key >= 17491637400000
    AND l.key < 17491637500000
    AND r.key >= 17491637400000
    AND r.key < 17491637500000
  LIMIT 10
```
{% include copy.html %}


根據預設，`JOIN` 查詢會在 60 秒後自動終止，以避免過度耗用資源。您可以使用查詢中的提示來調整此逾時期間。例如，若要設定 5 分鐘 (300 秒) 的逾時，請使用下列程式碼：

```sql
SELECT /*! JOIN_TIME_OUT(300) */ left.a, right.b FROM left JOIN right ON left.id = right.id;
```
{% include copy.html %}


當[查詢外部資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/query-data-source/)時，這些效能限制不適用。

## 分頁僅支援基本查詢

分頁查詢可讓您取得分頁回應。

目前分頁僅支援基本查詢。例如，下列查詢會傳回含有游標 ID 的資料。

```json
POST _plugins/_sql/
{
  "fetch_size" : 5,
  "query" : "SELECT OriginCountry, DestCountry FROM opensearch_dashboards_sample_data_flights ORDER BY OriginCountry ASC"
}
```
{% include copy-curl.html %}

以 JDBC 格式傳回且含有游標 ID 的回應。

```json
{
  "schema": [
    {
      "name": "OriginCountry",
      "type": "keyword"
    },
    {
      "name": "DestCountry",
      "type": "keyword"
    }
  ],
  "cursor": "d:eyJhIjp7fSwicyI6IkRYRjFaWEo1UVc1a1JtVjBZMmdCQUFBQUFBQUFCSllXVTJKVU4yeExiWEJSUkhsNFVrdDVXVEZSYkVKSmR3PT0iLCJjIjpbeyJuYW1lIjoiT3JpZ2luQ291bnRyeSIsInR5cGUiOiJrZXl3b3JkIn0seyJuYW1lIjoiRGVzdENvdW50cnkiLCJ0eXBlIjoia2V5d29yZCJ9XSwiZiI6MSwiaSI6ImtpYmFuYV9zYW1wbGVfZGF0YV9mbGlnaHRzIiwibCI6MTMwNTh9",
  "total": 13059,
  "datarows": [[
    "AE",
    "CN"
  ]],
  "size": 1,
  "status": 200
}
```

含有 `aggregation` 與 `join` 的查詢目前不支援分頁。

## 查詢處理引擎

在 OpenSearch 3.0.0 之前，SQL 外掛程式使用兩個查詢處理引擎：`V1` 與 `V2`。兩個引擎都支援大部分功能，但只有 `V2` 處於積極開發中。當您執行查詢時，外掛程式會先嘗試使用 `V2` 引擎執行，若執行失敗則退回使用 `V1`。若某個查詢在 `V2` 中受支援但在 `V1` 中不受支援，該查詢會失敗並傳回錯誤回應。

從 OpenSearch 3.0.0 開始，SQL 外掛程式引進了新的查詢引擎 (`V3`)，其運用 Apache Calcite 進行查詢最佳化與執行。由於 `V3` 在 OpenSearch 3.0.0 中是實驗性功能，因此預設為停用。若要啟用這個新引擎，請將 `plugins.calcite.enabled` 設為 `true`。類似於 `V2` 退回至 `V1` 的邏輯，當您執行查詢時，外掛程式會先嘗試使用 `V3` 引擎執行，若執行失敗則退回使用 `V2`。如需 `V3` 的詳細資訊，請參閱 [PPL Engine V3](https://github.com/opensearch-project/sql/blob/main/docs/dev/intro-v3-engine.md)。

### V1 引擎限制

`V1` 查詢引擎是 OpenSearch 中原始的 SQL 處理引擎。雖然它已在很大程度上被較新的引擎取代，但了解其限制有助於解釋某些查詢行為，尤其是當查詢從 `V2` 退回至 `V1` 時。下列限制特別適用於 `V1` 引擎：

* 不支援沒有 `FROM` 子句的 select 常值運算式。例如，不支援 `SELECT 1`。
* `WHERE` 子句不支援運算式。例如，不支援 `SELECT FlightNum FROM opensearch_dashboards_sample_data_flights where (AvgTicketPrice + 100) <= 1000`。
* 大多數[相關性搜尋函式]({{site.url}}{{site.baseurl}}/search-plugins/sql/full-text/)僅在 `V2` 引擎中實作。

這類查詢會由 `V2` 引擎成功執行，除非它們含有 `V1` 專屬的函式。您很可能永遠不會遇到這些限制。

### V2 引擎限制

`V2` 查詢引擎可處理大多數現代 SQL 查詢模式。然而，它有一些限制可能會影響您的查詢開發，尤其是複雜的分析工作負載。了解這些限制有助於您設計出能與 OpenSearch 最佳搭配運作的查詢：

* [游標功能](#pagination-only-supports-basic-queries)僅由 `V1` 引擎支援。
  * 如需 `V2` 引擎中對 `cursor`/`pagination` 的支援，請追蹤 [GitHub issue #656](https://github.com/opensearch-project/sql/issues/656)。
* `json` 格式化輸出僅在 `V1` 引擎中受支援。 
* `V2` 引擎不會追蹤查詢執行時間，因此不會回報慢速查詢。
* `V2` 查詢引擎不僅在 OpenSearch 引擎中執行查詢，也支援複雜查詢的後處理。因此，`explain` 輸出不再是 OpenSearch 領域特定語言 (DSL)，而是也包含來自 `V2` 查詢引擎的查詢計畫資訊。
* `V2` 查詢引擎不支援彙總查詢，例如 `histogram`、`date_histogram`、`percentiles`、`topHits`、`stats`、`extended_stats`、`terms` 或 `range`。
* 不支援 JOIN 與子查詢。若要掌握 JOIN 與子查詢的最新開發進度，請追蹤 [GitHub issue #1441](https://github.com/opensearch-project/sql/issues/1441) 與 [GitHub issue #892](https://github.com/opensearch-project/sql/issues/892)。
* OpenSearch 原生不支援陣列資料類型，但隱含允許多重值欄位。SQL/PPL 外掛程式嚴格遵循索引對應中定義的資料類型語意。在剖析 OpenSearch 回應時，它預期資料符合宣告的類型，且不會將陣列中的所有資料都解譯。若啟用 [`plugins.query.field_type_tolerance`](https://github.com/opensearch-project/sql/blob/main/docs/user/admin/settings.rst#plugins-query-field-type-tolerance) 設定，SQL/PPL 外掛程式會以傳回純量資料類型的方式處理陣列資料集，允許基本查詢 (例如 `SELECT * FROM tbl WHERE condition`)。然而，在運算式或函式中使用多重值欄位會導致例外狀況。若停用或未設定此設定，則只會傳回陣列的第一個元素，保留預設行為。
* 不支援 `nested` 查詢的 PartiQL 語法。

### V3 引擎限制與限制條件

`V3` 查詢引擎使用 Apache Calcite 提供增強的查詢處理能力。作為 OpenSearch 3.0.0 中的實驗性功能，它有一些限制與行為差異，您在開發查詢時應留意。這些限制分為三類：新限制、不支援的功能，以及行為變更。

#### 限制

`V3` 引擎對 OpenSearch 中繼資料欄位引進了更嚴格的驗證。在操作會處理欄位名稱的命令時，請留意下列限制：

- `eval` 不允許您使用 [OpenSearch 中繼資料欄位]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/index/)作為欄位。
- `rename` 不允許重新命名為 [OpenSearch 中繼資料欄位]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/index/)。
- `as` 不允許您使用 [OpenSearch 中繼資料欄位]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/index/)作為別名。

### 不支援的功能

`V3` 引擎不支援先前引擎中可用的所有功能。對於下列功能，查詢會自動轉送至 `V2` 查詢引擎：

- `trendline`
- `show datasource`
- `describe`
- `top` 與 `rare`
- `fillnull`
- `patterns`
- `dedup` 搭配 `consecutive=true`
- 搜尋相關命令：
  - `AD`
  - `ML`
  - `Kmeans`
- 含有 `fetch_size` 參數的命令
- 含有中繼資料欄位的查詢，例如 `_id` 或 `_doc`
- JSON 相關函式：
  - `cast to json`
  - `json`
  - `json_valid`
- 搜尋相關函式：
  - `match`
  - `match_phrase`
  - `match_bool_prefix`
  - `match_phrase_prefix`
  - `simple_query_string`
  - `query_string`
  - `multi_match`

#### V2 與 V3 的比較

由於 `V3` 引擎在內部使用不同的實作，某些行為已與先前版本不同。`V3` 中的行為被視為正確，但與 `V2` 中的相同查詢相比，可能會產生不同的結果。下表列出這些差異。

項目 | `V2` | `V3`
:--- | :--- | :---
`timestampdiff` 的傳回類型 | `timestamp` | `int`
`regexp` 的傳回類型 | `int` | `boolean`
`count`、`dc`、`distinct_count` 的傳回類型 | `int` | `bigint`
`ceiling`、`floor`、`sign` 的傳回類型 | `int` | 與輸入相同的類型
對值 "Amber JOHnny" 執行 `like(firstname, 'Ambe_')` | `true` | `false`
對值 "Amber JOHnny" 執行 `like(firstname, 'Ambe*')` | `true` | `false`
`cast(firstname as boolean)` | `false` | `null`
啟用 `pushdown` 時多個 `null` 值的總和 | `0` | `null`
`percentile(null, 50)` | `0` | `null`
