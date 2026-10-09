---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新排序"
nav_order: 110
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 重新排序處理器
於 2.12 版推出
{: .label .label-purple }

`rerank` 搜尋回應處理器會攔截搜尋結果並重新排序。此處理器會根據文件的新分數來排序搜尋結果中的文件。

OpenSearch 支援下列重新排序類型。

類型 | 說明 | 最早可用版本
:--- | :--- | :---
[`ml_opensearch`](#the-ml_opensearch-rerank-type) | 套用 OpenSearch 提供的交叉編碼器模型。 | 2.12
[`by_field`](#the-by_field-rerank-type) | 根據使用者提供的欄位套用重新排序。 | 2.18

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`rerank_type` | 物件 | 必要 | 用於文件重新排序的重新排序類型。有效值為 `ml-opensearch` 和 `by_field`。
`context` | 物件 |  `ml_opensearch` 重新排序類型為必要。`by_field` 重新排序類型為選用，且不會影響結果。 | 為 `rerank` 處理器提供在查詢時重新排序所需的資訊。
`tag` | 字串 | 選用 | 處理器的識別碼。
`description` | 字串 | 選用 | 處理器的說明。
`ignore_failure` | 布林值 | 選用 | 若為 `true`，OpenSearch [會忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中的其餘處理器。預設為 `false`。

<!-- vale off -->
## ml_opensearch 重新排序類型
<!-- vale on -->
於 2.12 版推出
{: .label .label-purple }

若要使用交叉編碼器模型重新排序結果，請指定 `ml_opensearch` 重新排序類型。

### 先決條件

使用 `ml_opensearch` 重新排序類型之前，您必須設定交叉編碼器模型。如需使用 OpenSearch 所提供模型的相關資訊，請參閱[交叉編碼器模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#cross-encoder-models)。如需使用自訂模型的相關資訊，請參閱[自訂本機模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/)。

`ml_opensearch` 重新排序類型支援下列欄位。所有欄位皆為必要。

欄位  | 資料類型 | 說明
:--- | :---  | :--- 
`ml_opensearch.model_id` | 字串 | 用於重新排序的交叉編碼器模型 ID。如需詳細資訊，請參閱[使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/using-ml-models/)。
`context.document_fields` | 陣列 | 文件欄位陣列，指定要從哪些欄位擷取提供給交叉編碼器模型的上下文。

### 範例

下列範例示範如何使用含有 `rerank` 處理器的搜尋管線，該處理器使用 `ml_opensearch` 重新排序類型實作。如需完整範例，請參閱[使用交叉編碼器模型重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-cross-encoder/)。

### 建立搜尋管線

下列請求會建立含有 `rerank` 回應處理器的搜尋管線：

```json
PUT /_search/pipeline/rerank_pipeline
{
  "response_processors": [
    {
      "rerank": {
        "ml_opensearch": {
          "model_id": "gnDIbI0BfUsSoeNT_jAw"
        },
        "context": {
          "document_fields": [ "title", "text_representation"]
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

將 OpenSearch 查詢與包含大型語言模型（LLM）查詢上下文的 `ext` 物件合併。提供將用於重新排序結果的 `query_text`：

```json
POST /_search?search_pipeline=rerank_pipeline
{
  "query": {
    "match": {
      "text_representation": "Where is Albuquerque?"
    }
  },
  "ext": {
    "rerank": {
      "query_context": {
        "query_text": "Where is Albuquerque?"
      }
    }
  }
}
```
{% include copy-curl.html %}

您可以提供包含重新排序所用文字之欄位的完整路徑，以取代 `query_text`。例如，若您在 `text_representation` 物件中指定子欄位 `query`，請在 `query_text_path` 參數中指定其路徑：

```json
POST /_search?search_pipeline=rerank_pipeline
{
  "query": {
    "match": {
      "text_representation": {
        "query": "Where is Albuquerque?"
      }
    }
  },
  "ext": {
    "rerank": {
      "query_context": {
        "query_text_path": "query.match.text_representation.query"
      }
    }
  }
}
```
{% include copy-curl.html %}

`query_context` 物件包含下列欄位。您必須提供 `query_text` 或 `query_text_path` 其中之一，但不能同時提供兩者。

欄位名稱 | 必要/選用 | 說明
:--- | :--- | :---  
`query_text` | `query_text` 或 `query_text_path` 必須擇一提供。 | 您要用來重新排序搜尋結果之問題的自然語言文字。
`query_text_path` | `query_text` 或 `query_text_path` 必須擇一提供。 | 您要用來重新排序搜尋結果之問題文字的完整 JSON 路徑。路徑中允許的字元數上限為 `1000`。


<!-- vale off -->
## by_field 重新排序類型
<!-- vale on -->
於 2.18 版推出
{: .label .label-purple }

若要依文件欄位重新排序結果，請指定 `by_field` 重新排序類型。

`by_field` 物件支援下列欄位。

欄位  | 資料類型 | 必要/選用 | 說明
:--- | :---  | :--- | :--- 
`target_field` | 字串 | 必要 |  指定欄位名稱，或包含要用於重新排序之分數的欄位點路徑。
`remove_target_field` | 布林值 | 選用 | 若為 `true`，回應不會包含用於執行重新排序的 `target_field`。預設為 `false`。
`keep_previous_score` | 布林值 | 選用 | 若為 `true`，回應會包含一個欄位，其中含有重新排序前計算的分數。欄位名稱由 `previous_score_field` 指定。這在偵錯時可能很有用。預設為 `false`。
`previous_score_field` | 字串 | 選用 | 當 `keep_previous_score` 為 `true` 時，用來儲存重新排序前計算之分數的欄位名稱。預設為 `previous_score`。僅在 `keep_previous_score` 為 `true` 時使用。

若您的索引已定義 `previous_score` 文件欄位，請將 `previous_score_field` 設為不同的名稱（例如 `original_query_score`），以避免覆寫搜尋結果中現有的欄位值。
{: .note}


### 範例

下列範例示範如何使用含有 `rerank` 處理器的搜尋管線，該處理器使用 `by_field` 重新排序類型實作。如需完整範例，請參閱[依文件欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field/)。

### 建立搜尋管線

下列請求會建立含有 `by_field` 重新排序類型回應處理器的搜尋管線，該處理器會依 `reviews.stars` 欄位排序文件，並指定傳回原始文件分數：

```json
PUT /_search/pipeline/rerank_byfield_pipeline
{
  "response_processors": [
    {
      "rerank": {
        "by_field": {
          "target_field": "reviews.stars",
          "keep_previous_score" : true
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

若要將搜尋管線套用至查詢，請在查詢參數中提供搜尋管線名稱：

```json
POST /book-index/_search?search_pipeline=rerank_byfield_pipeline
{
  "query": {
     "match_all": {}
  }
}
```
{% include copy-curl.html %}

## 後續步驟

- 進一步了解[重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)。
- 參閱[使用交叉編碼器模型重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-cross-encoder/)的完整範例。
- 參閱[依文件欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field/)的完整範例。
- 參閱[使用外部託管的交叉編碼器模型依欄位重新排序]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/rerank-by-field-cross-encoder/)的完整範例。