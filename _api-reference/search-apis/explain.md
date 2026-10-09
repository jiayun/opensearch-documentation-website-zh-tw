---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Explain
parent: Search APIs
nav_order: 40
redirect_from:
 - /opensearch/rest-api/explain/
 - /api-reference/explain/
---

# Explain API
**於 1.0 版推出**
{: .label .label-purple }

Explain API 會傳回詳細資訊，說明特定文件為何符合或不符合某個查詢。此 API 可協助您了解 OpenSearch 如何計算每個搜尋結果的相關性分數 (`_score`)，是偵錯搜尋相關性問題及最佳化查詢的必備工具。

OpenSearch 使用稱為 [Okapi BM25](https://en.wikipedia.org/wiki/Okapi_BM25) 的機率排名架構來計算相關性分數。Okapi BM25 是以 Apache Lucene 所使用的原始 [詞頻/反向文件頻率 (TF/IDF)](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/package-summary.html#scoring) 架構為基礎。

使用 Explain API 在資源和時間方面都所費不貲。對於正式環境叢集，我們建議僅在疑難排解時酌量使用。
{: .warning }

## 限制

Explain API 不支援 `search_pipeline` 參數。傳送帶有內嵌或具名搜尋管線的請求會導致 `parsing_exception` 錯誤。這適用於所有查詢類型。

若要將搜尋管線處理器與 `explain` 搭配使用，請為 [Search API]({{site.url}}{{site.baseurl}}/api-reference/search/) 提供 `explain=true` 查詢參數。如需將 `explain` 與混合查詢搭配使用的詳細資訊，請參閱[混合搜尋說明]({{site.url}}{{site.baseurl}}/vector-search/ai-search/hybrid-search/explain/)。

<!-- spec_insert_start
api: explain
component: endpoints
-->
## 端點
```json
GET  /{index}/_explain/{id}
POST /{index}/_explain/{id}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `id` | **必要** | 字串 | 文件 ID。 |
| `index` | **必要** | 字串 | 要搜尋的索引。只能指定單一索引名稱。 |

## 查詢參數

您必須指定索引和文件 ID。所有其他參數均為選用。

參數 | 類型 | 說明 | 必要
:--- | :--- | :--- | :---
`analyzer` | 字串 | 用於 `q` 查詢字串的分析器。僅在使用了 `q` 時有效。 | 否
`analyze_wildcard` | 布林值 | 是否分析 `q` 字串中的萬用字元查詢和前綴查詢。僅在使用 `q` 時有效。預設為 `false`。 | 否
`default_operator` | 字串 | `q` 查詢字串的預設布林運算子 (`AND` 或 `OR`)。僅在使用了 `q` 時有效。預設為 `OR`。  | 否
`df` | 字串 | 若 `q` 字串中未指定欄位，則為要搜尋的預設欄位。僅在使用了 `q` 時有效。 | 否
`lenient` | 布林值 | 指定 OpenSearch 是否應忽略格式相關的查詢失敗 (例如，對文字欄位查詢整數)。預設為 `false`。 | 否
`preference` | 字串 | 指定要從哪個分片擷取結果的偏好設定。可用的選項為 `_local` (指示作業從本機配置的副本分片擷取結果)，以及指派給特定副本分片的自訂字串值。根據預設，OpenSearch 會對隨機分片執行說明作業。 | 否
`q` | 字串 | 使用 [Lucene 語法]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/#query-string-syntax) 的查詢字串。使用時，您可以使用 `analyzer`、`analyze_wildcard`、`default_operator`、`df` 及 `stored_fields` 參數來設定查詢行為。 | 否
`stored_fields` | 字串 | 要傳回的已儲存欄位清單，以逗號分隔。若省略，則僅傳回 `_source`。 | 否
`routing` | 字串 | 用於將作業路由至特定分片的值。 | 否
`_source` | 字串 | 是否在回應本文中包含 `_source` 欄位。有效值為 `true` (包含完整的 `_source`)、`false` (排除 `_source`)，或要在查詢回應中包含的來源欄位清單 (以逗號分隔)。根據預設，若未指定，Explain API 回應中不會傳回 `_source` 欄位。 | 否
`_source_excludes` | 字串 | 要在查詢回應中排除的來源欄位清單，以逗號分隔。 | 否
`_source_includes` | 字串 | 要在查詢回應中包含的來源欄位清單，以逗號分隔。 | 否

## 請求本文欄位

請求本文包含要對指定文件說明的查詢。下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`query` | 物件 | 要對文件執行的查詢。使用與 [Search API]({{site.url}}{{site.baseurl}}/api-reference/search/) 相同的查詢語法。如需查詢類型的詳細資訊，請參閱 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/)。

## 範例：說明 match 查詢

下列範例說明 `products` 索引中的文件 `1` 為何符合在 `name` 欄位中搜尋詞彙 "computer" 的查詢：

<!-- spec_insert_start
component: example_code
rest: POST /products/_explain/1
body: |
{
  "query": {
    "match": {
      "name": "computer"
    }
  }
}
-->
{% capture step1_rest %}
POST /products/_explain/1
{
  "query": {
    "match": {
      "name": "computer"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.explain(
  id = "1",
  index = "products",
  body =   {
    "query": {
      "match": {
        "name": "computer"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

Explain API 會傳回回應，其中包含文件是否符合查詢，以及分數計算的詳細分解。說明包含 BM25 評分公式的組成部分：詞頻 (`tf`)、反向文件頻率 (`idf`) 及欄位長度正規化：

<details markdown="block">
  <summary>
    說明 match 查詢的回應
  </summary>
  {: .text-delta}

```json
{
  "_index": "products",
  "_id": "1",
  "matched": true,
  "explanation": {
    "value": 0.31506687,
    "description": "weight(name:computer in 0) [PerFieldSimilarity], result of:",
    "details": [
      {
        "value": 0.31506687,
        "description": "score(freq=1.0), computed as boost * idf * tf from:",
        "details": [
          {
            "value": 0.6931472,
            "description": "idf, computed as log(1 + (N - n + 0.5) / (n + 0.5)) from:",
            "details": [
              {
                "value": 2,
                "description": "n, number of documents containing term",
                "details": []
              },
              {
                "value": 4,
                "description": "N, total number of documents with field",
                "details": []
              }
            ]
          },
          {
            "value": 0.45454544,
            "description": "tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl)) from:",
            "details": [
              {
                "value": 1.0,
                "description": "freq, occurrences of term within document",
                "details": []
              },
              {
                "value": 1.2,
                "description": "k1, term saturation parameter",
                "details": []
              },
              {
                "value": 0.75,
                "description": "b, length normalization parameter",
                "details": []
              },
              {
                "value": 2.0,
                "description": "dl, length of field",
                "details": []
              },
              {
                "value": 2.0,
                "description": "avgdl, average length of field",
                "details": []
              }
            ]
          }
        ]
      }
    ]
  }
}
```

</details>

## 範例：使用查詢字串參數

您可以使用 `q` 參數，以 Lucene 查詢字串語法指定查詢，而不需提供請求本文。以下範例說明文件 `1` 為何符合查詢字串 "name:laptop"：

<!-- spec_insert_start
component: example_code
rest: GET /products/_explain/1?q=name:laptop
-->
{% capture step1_rest %}
GET /products/_explain/1?q=name:laptop
{% endcapture %}

{% capture step1_python %}


response = client.explain(
  id = "1",
  index = "products",
  params = { "q": "name:laptop" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 回應本文欄位

回應包含文件是否符合查詢，以及相關性分數如何計算的詳細資訊。下表列出回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`_index` | 字串 | 包含該文件的索引名稱。
`_id` | 字串 | 文件 ID。
`matched` | 布林值 | 文件是否符合查詢。若為 `true`，表示文件符合並具有相關性分數。若為 `false`，表示文件不符合查詢。
`explanation` | 物件 | 分數計算的說明。包含下列巢狀欄位：`value` (計算出的分數或分數元件)、`description` (供人閱讀的計算說明)，以及 `details` (巢狀計算的子說明陣列)。
`explanation.value` | 浮點數 | 分數計算的數值結果。對頂層說明而言，這是最終的相關性分數。對巢狀說明而言，這代表中間計算值。
`explanation.description` | 字串 | 所執行計算的描述。對 BM25 評分而言，這通常描述評分公式的組成部分，例如詞彙頻率 (`tf`)、反向文件頻率 (`idf`) 以及正規化因子。
`explanation.details` | 物件陣列 | 巢狀說明物件的陣列，將分數計算分解為各個組成部分。每個 detail 物件的結構與說明物件相同 (包含 `value`、`description` 和 `details` 欄位)。
`get` | 物件 | 文件中繼資料與來源資料。僅在使用 `_source` 或 `stored_fields` 參數時才會包含。包含 `_seq_no`、`_primary_term`、`found` 和 `_source` 等欄位。
`get._source` | 物件 | 文件的原始 JSON 內容。僅在指定 `_source` 參數時才會包含。

## BM25 評分元件

說明細節包含下列 BM25 評分元件。

欄位 | 說明
:--- | :---
`idf` | 反向文件頻率 (IDF)。衡量詞彙在索引中所有文件之間的稀有或常見程度。計算公式為 `log(1 + (N - n + 0.5) / (n + 0.5))`，其中 `N` 是具有該欄位的文件總數，`n` 是包含該詞彙的文件數。越稀有的詞彙 IDF 值越高，對相關性分數的貢獻也越大。
`tf` | 詞彙頻率 (TF)。衡量詞彙在文件欄位中出現的頻率。計算公式為 `freq / (freq + k1 * (1 - b + b * dl / avgdl))`，其中 `freq` 是詞彙出現的次數，`k1` 是詞彙飽和參數 (預設 1.2)，`b` 是長度正規化參數 (預設 0.75)，`dl` 是欄位長度，`avgdl` 是所有文件的平均欄位長度。越常出現的詞彙對相關性分數的貢獻越大，但效益會遞減。
`k1` | 詞彙飽和參數。控制分數隨詞彙頻率增加而上升的速度。預設值為 1.2。較低的值會使分數更快飽和，較高的值則讓詞彙頻率對分數有更大的影響。
`b` | 長度正規化參數。控制欄位長度對分數的影響程度。預設值為 0.75。值為 0 時停用長度正規化，值為 1 時完全依欄位長度正規化。包含符合詞彙的較短欄位通常會獲得較高分數。
`dl` | 文件欄位長度。此特定文件在該欄位中的詞元數量。
`avgdl` | 平均文件欄位長度。索引中所有文件在該欄位中的平均詞元數量。
`boost` | 查詢 boost 值。套用至分數的乘數。未在查詢中明確指定時，預設 boost 為 1.0。

最終的相關性分數是將這些元件相乘計算而得：`score = boost * idf * tf`。這些值會在新增或更新文件時於編製索引階段計算並儲存，且可能因分片層級的統計資料而有些微不精確。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:data/read/explain`。
