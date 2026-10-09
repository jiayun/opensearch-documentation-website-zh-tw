---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Regexp
parent: Term-level queries
nav_order: 100
---

# Regexp 查詢

使用 `regexp` 查詢來搜尋符合規則表達式的詞元。如需撰寫規則表達式的詳細資訊，請參閱[規則表達式語法]({{site.url}}{{site.baseurl}}/query-dsl/regex-syntax/)。

下列查詢會搜尋任何以大寫或小寫字母開頭，且後面接著 `amlet` 的詞元：

```json
GET shakespeare/_search
{
  "query": {
    "regexp": {
      "play_name": "[a-zA-Z]amlet"
    }
  }
}
```
{% include copy-curl.html %}

請注意下列重要考量：

- 規則表達式會套用至欄位中的詞元 (亦即 token)，而非整個欄位。
- 根據預設，規則表達式的長度上限為 1,000 個字元。若要變更長度上限，請更新 `index.max_regex_length` 設定。
- 規則表達式使用 Lucene 語法，這與較標準化的實作方式不同。請徹底測試，以確保您獲得預期的結果。如需深入了解，請參閱 [Lucene 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/index.html)。
- 若要提升 regexp 查詢效能，請避免使用沒有前置字元或後置字元的萬用字元模式，例如 `.*` 或 `.*?+`。
- `regexp` 查詢可能是成本高昂的操作，且需要將 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/#expensive-queries) 設定設為 `true`。在頻繁執行 `regexp` 查詢之前，請先測試其對叢集效能的影響，並檢視可能可達到類似結果的替代查詢。
- [wildcard 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/) 會建立專門設計來非常有效率地處理萬用字元和規則表達式查詢的索引。

## 比對詞元而非欄位值

`regexp` 查詢不會經過分析，但其搜尋的欄位可能會。當 `text` 欄位經過索引時，標準分析器會將其值分割成小寫詞元，而規則表達式必須符合其中一個詞元。因此，包含大寫字母或空格的模式對 `text` 欄位不會傳回任何結果。

若要試試看，請將文件編製索引至使用動態對應的索引。`title` 欄位會對應為 `text`，並具有 `title.keyword` 子欄位：

```json
PUT my-index/_doc/1?refresh=true
{
  "title": "Henry IV"
}
```
{% include copy-curl.html %}

`title` 欄位包含詞元 `henry` 和 `iv`，因此下列查詢不會傳回任何結果：

```json
GET my-index/_search
{
  "query": {
    "regexp": {
      "title": "Henry.*"
    }
  }
}
```
{% include copy-curl.html %}

若要符合原始欄位值（包括其大小寫和空格），請搜尋 `keyword` 子欄位：

```json
GET my-index/_search
{
  "query": {
    "regexp": {
      "title.keyword": "Henry I.*"
    }
  }
}
```
{% include copy-curl.html %}

<details markdown="block">
<summary>
    回應
</summary>
{: .text-delta}

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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "my-index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "title": "Henry IV"
        }
      }
    ]
  }
}
```
</details>

如果 `regexp` 查詢未傳回任何結果，也請檢查下列事項：

- 模式必須符合整個詞元。例如，`hen` 不符合詞元 `henry`，但 `hen.*` 符合。
- 不支援 `^` 和 `$` 錨點。例如，`^Henry.*` 在 `keyword` 欄位中不符合 `Henry IV`。如需詳細資訊，請參閱[不支援的功能]({{site.url}}{{site.baseurl}}/query-dsl/regex-syntax/#unsupported-features)。
- 根據預設，比對會區分大小寫。若要不論大小寫進行詞元比對，請將 `case_insensitive` 設為 `true`。例如，當 `case_insensitive` 為 `true` 時，`henry iv` 會在 `title.keyword` 欄位中符合 `Henry IV`。

## 參數

此查詢接受欄位名稱（`<field>`）作為最上層參數：

```json
GET _search
{
  "query": {
    "regexp": {
      "<field>": {
        "value": "[Ss]ample",
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `value` 之外，所有參數都是選用的。

參數 | 資料類型 | 說明
:--- | :--- | :---
`value` | 字串 | 用於比對 `<field>` 中所指定欄位之詞元的規則表達式。
`boost` | 浮點數 | 浮點數值，用於指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 和 1.0 之間的值會降低欄位的相關性。預設為 1.0。
`case_insensitive` | 布林值 | 若為 `true`，則允許規則表達式值與已編製索引的欄位值進行不區分大小寫的比對。預設為 `false`（大小寫區分由欄位的對應決定）。
`flags` | 字串 | 啟用 Lucene 規則表達式引擎的選用運算子。如需有效值，請參閱[選用運算子]({{site.url}}{{site.baseurl}}/query-dsl/regex-syntax/#optional-operators)。
`max_determinized_states` | 整數 | Lucene 會將規則表達式轉換為具有若干確定化狀態的自動機。此參數會指定查詢所需的自動機狀態數上限。請使用此參數來避免高資源耗用。若要執行複雜的規則表達式，您可能需要提高此參數的值。預設為 10,000。
`rewrite` | 字串 | 決定 OpenSearch 如何改寫及評分多詞元查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。預設為 `constant_score`。

如果將 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行 `regexp` 查詢。
{: .important}
