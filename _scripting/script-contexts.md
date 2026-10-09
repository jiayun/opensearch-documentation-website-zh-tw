---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼情境"
nav_order: 45
---

# 指令碼情境

指令碼會在_指令碼情境_中執行。情境會決定指令碼可接收的變數、必須傳回的值，以及允許使用的語言。在某個情境中有效的指令碼，在另一個情境中通常無效，這也是為什麼可做為 script field 使用的指令碼，在移入 update 之後可能會失敗。

情境是其他數項功能定義時所依據的單位。編譯限制與快取會依情境分別追蹤，`script.allowed_contexts` 會依情境限制指令碼功能，而儲存的指令碼在您儲存時，可針對具名情境進行編譯。

## 列出叢集中的情境

已安裝的外掛程式會註冊自己的情境，因此最權威的清單就是您的叢集所回報的清單。若要列出叢集中的所有情境，請使用 [Get Script Contexts API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-contexts/)：

```json
GET _script_context
```
{% include copy-curl.html %}

每個項目都會列出一個情境名稱及其方法。`execute` 方法會提供指令碼的傳回類型，以及傳遞給它的任何引數，而每個 `get` 方法則對應到指令碼可讀取的變數：

```json
{
  "contexts": [
    {
      "name": "aggregation_selector",
      "methods": [
        {
          "name": "execute",
          "return_type": "boolean",
          "params": []
        },
        {
          "name": "getParams",
          "return_type": "java.util.Map",
          "params": []
        }
      ]
    }
  ]
}
```

回應內容很長，因為它涵蓋了每個情境。若只要列出情境名稱，請使用 `filter_path` 查詢參數：

```json
GET _script_context?filter_path=contexts.name
```
{% include copy-curl.html %}

## 依工作分類的情境

以下各節依工作將情境分組。`params` 變數在所有情境中皆可使用，因此未列於各說明中。

### 搜尋與評分

下表列出搜尋期間執行的情境。

情境 | 傳回 | 變數 | 用於
:--- | :--- | :--- | :---
`score` | `double` | `doc`, `_score`, `explanation` | [`script_score` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script-score/) 與 `function_score` 指令碼評分。
`filter` | `boolean` | `doc` | [`script` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script/)。
`field` | `Object` | `doc` | [指令碼欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields)。
`derived_field` | `void` | `doc`, `emit()` | [衍生欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/)。
`number_sort` | `double` | `doc`, `_score` | 數值[以指令碼為基礎的排序]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/)。
`string_sort` | `String` | `doc`, `_score` | 字串以指令碼為基礎的排序。
`terms_set` | `Number` | `doc` | `terms_set` 查詢的 `minimum_should_match_script`。
`similarity` | `double` | `weight`, `query`, `field`, `term`, `doc` | 指令碼化的相似度模組。
`similarity_weight` | `double` | `query`, `field`, `term` | 指令碼化相似度的權重計算。
`interval` | `boolean` | `interval` | `intervals` 查詢的 `script` 篩選條件。
`search` | `void` | `ctx` | 搜尋請求的前置處理。

`score` 情境除了傳回分數之外，也會提供 `_score`，因此指令碼可以根據查詢所計算出的相關性進一步處理。請參閱[存取相關性分數]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/#accessing-the-relevance-score)。

### 彙總

下表列出彙總情境。

情境 | 傳回 | 變數 | 用於
:--- | :--- | :--- | :---
`aggs` | `Object` | `doc`, `_score`, `value` | 指標或桶彙總的 `script`。
`aggs_init` | `void` | `state` | [指令碼化指標彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/scripted-metric/) 的 `init_script`。
`aggs_map` | `void` | `doc`, `_score`, `state` | 指令碼化指標彙總的 `map_script`。
`aggs_combine` | `Object` | `state` | 指令碼化指標彙總的 `combine_script`。
`aggs_reduce` | `Object` | `states` | 指令碼化指標彙總的 `reduce_script`。
`bucket_aggregation` | `Number` | 無 | [桶指令碼]({{site.url}}{{site.baseurl}}/aggregations/pipeline/bucket-script/) 管線彙總。
`aggregation_selector` | `boolean` | 無 | 桶選取器管線彙總。
`moving-function` | `double` | `params`, `values` | `moving_fn` 管線彙總的 `script`。
`script_heuristic` | `double` | `params` | `significant_terms` 彙總的 `script_heuristic`。

這四個指令碼化指標情境會依序執行，並透過 `state` 溝通；`aggs_init` 會建立它，`aggs_map` 會依文件填入它，`aggs_combine` 會依分片縮減它，而 `aggs_reduce` 則會以清單 `states` 的形式接收它。

### 匯入與更新

下表列出文件被編製索引或更新時所執行的情境。

情境 | 傳回 | 變數 | 用於
:--- | :--- | :--- | :---
`update` | `void` | `ctx` | [Update Document]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)、[Update By Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) 與 [Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) API。
`ingest` | `void` | `ctx` | [`script` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/script/)。
`processor_conditional` | `boolean` | `ctx` | 任何匯入處理器上的 `if` 條件。
`context_aware_grouping` | `String` | `ctx` | `context_aware_grouping` 對應的 `script`，會傳回文件所屬分段被選取時所用的分組索引鍵。
`analysis` | `boolean` | `token` | `condition` 詞元篩選器的 `condition`。

修改文件的情境會透過 `ctx` 公開文件資料。`doc` 變數無法使用，因此在更新中參照它的指令碼會編譯失敗。請參閱[更新指令碼]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/#update-scripts)。

### 範本與測試

下表列出其餘的通用情境。

情境 | 傳回 | 變數 | 用於
:--- | :--- | :--- | :---
`painless_test` | `Object` | 無 | [Execute Inline Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/exec-script/) 的預設情境。
`template` | `String` | 無 | 以 `mustache` 撰寫的[搜尋範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/)。

### 外掛程式情境

下表列出外掛程式所註冊的情境。唯有安裝對應的外掛程式時，這些情境才會出現。

情境 | 傳回 | 變數 | 註冊者
:--- | :--- | :--- | :---
`trigger` | `boolean` | `ctx` | Alerting，用於監視器觸發條件。
`ranklib` | `void` | 無 | Learning to Rank，用於 `ranklib` 模型。

## 各情境支援的語言

Painless 可在所有情境中執行。特殊用途語言則受到限制，因此使用這些語言的指令碼在其支援的情境之外會失敗。請使用 [Get Script Languages API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-language/) 查看您叢集的對應：

```json
GET _script_language
```
{% include copy-curl.html %}

下表摘要說明您可用來撰寫指令碼的語言。

語言 | 情境
:--- | :---
`painless` | 所有情境
`expression` | `score`, `field`, `filter`, `number_sort`, `aggs`, `bucket_aggregation`, `aggregation_selector`, `terms_set`
`mustache` | `template`
`knn` | `score`
`ranklib` | `ranklib`

`expression` 語言無法在 `update`、`ingest` 與 `string_sort` 中使用，因為它無法讀取 `_source`，也無法傳回字串。請參閱[限制]({{site.url}}{{site.baseurl}}/scripting/expressions/#limitations)。

## 為情境撰寫指令碼

讓指令碼符合情境，意味著提供正確的傳回值，並使用該情境所提供的變數。`derived_field` 情境同時說明了這兩點：它會傳回 `void`，並透過呼叫 `emit()` 來回報其值，而非直接傳回。

下列搜尋會定義一個衍生欄位，使用[測試設定]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#test-setup)中所建立的 `scripting-products` 索引，依價格級距為每個產品加上標籤：

```json
GET scripting-products/_search
{
  "_source": false,
  "derived": {
    "price_tier": {
      "type": "keyword",
      "script": { "source": "emit(doc['price'].value >= 200 ? 'premium' : 'standard')" }
    }
  },
  "query": { "match_all": {} },
  "sort": [{ "sku": "asc" }],
  "fields": ["price_tier"]
}
```
{% include copy-curl.html %}

每個結果都會帶有發出的值：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 5,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "3",
        "_score": null,
        "fields": {
          "price_tier": [
            "standard"
          ]
        },
        "sort": [
          "ACC-2001"
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": null,
        "fields": {
          "price_tier": [
            "premium"
          ]
        },
        "sort": [
          "AUD-1001"
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": null,
        "fields": {
          "price_tier": [
            "standard"
          ]
        },
        "sort": [
          "AUD-1002"
        ]
      },
      {
        "_index": "scripting-products",
        "_id": "4",
        "_score": null,
        "fields": {
          "price_tier": [
            "premium"
          ]
        },
        "sort": [
          "DSP-3001"
        ]
      }
    ]
  }
}
```
</details>

## 針對情境編譯已儲存的指令碼

在儲存指令碼時指定情境，可讓 OpenSearch 立即編譯它，因此對該情境無效的指令碼會在儲存請求時失敗，而不是在第一次使用它的搜尋時才失敗。請參閱[使用已儲存的指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#working-with-stored-scripts)。

## 依情境限制與設定

下列設定會依情境運作：

- `script.allowed_contexts` 會將叢集限制為一組具名情境，進而減少指令碼可執行的範圍。請參閱[限制允許的情境]({{site.url}}{{site.baseurl}}/scripting/script-security/#restricting-the-allowed-contexts)。
- `script.context.<context>.max_compilations_rate`、`.cache_max_size` 與 `.cache_expire` 可為單一情境設定編譯與快取，而不影響其他情境。請參閱[指令碼情境設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/script-and-resource-settings/#script-context-settings)。

## 相關文件

- [Painless 語言參考]({{site.url}}{{site.baseurl}}/scripting/painless-language/)
- [在指令碼中存取文件欄位]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/)
- [Get Script Contexts API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-contexts/)
