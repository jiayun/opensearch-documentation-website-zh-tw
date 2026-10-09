---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Text
nav_order: 15
has_children: false
parent: String field types
grand_parent: Supported field types
redirect_from:
  - /opensearch/supported-field-types/text/
  - /field-types/supported-field-types/text/
  - /field-types/text/
---

# Text 欄位類型
**於 1.0 版推出**
{: .label .label-purple }

`text` 欄位類型包含經過分析的字串。它用於全文搜尋，因為它允許部分比對。搜尋多個詞彙時，可以只比對其中部分而非全部。視分析器而定，結果可以不區分大小寫、進行詞幹化、移除停用詞、套用同義詞等等。


如果您需要使用某個欄位進行精確值搜尋，請改將它對應為 [`keyword`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/)。
{: .note }

[`match_only_text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/match-only-text/) 欄位是 `text` 欄位的空間最佳化版本。如果您不需要查詢片語或使用位置查詢，請將欄位對應為 `match_only_text` 而不是 `text`。位置查詢是指詞彙在片語中的位置很重要的查詢，例如 interval 或 span 查詢。
{: .note}

## 範例

建立一個包含 text 欄位的對應：

```json
PUT movies
{
  "mappings" : {
    "properties" : {
      "title" : {
        "type" :  "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出 text 欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :---
`analyzer` | 此欄位要使用的分析器。預設情況下，會在編製索引時和搜尋時使用。若要在搜尋時覆寫，請設定 `search_analyzer` 參數。預設為 `standard` 分析器，它使用基於文法的斷詞，並以 [Unicode Text Segmentation](https://unicode.org/reports/tr29/) 演算法為基礎。
`boost` | 一個浮點數值，指定此欄位對相關性分數的權重。高於 1.0 的值會提高該欄位的相關性；介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。可動態更新。
`eager_global_ordinals` | 指定是否應在重新整理時立即載入全域序數。如果此欄位經常用於彙總，應將此參數設為 `true`。預設為 `false`。可動態更新。
`fielddata` | 一個布林值，指定是否要存取此欄位經過分析的詞元，以用於排序、彙總和指令碼。預設為 `false`。可動態更新。
`fielddata_frequency_filter` | 一個 JSON 物件，指定只將文件頻率介於 `min` 與 `max` 值之間（以絕對數字或百分比提供）的已分析詞元載入記憶體。頻率是按分段計算。參數：`min`、`max`、`min_segment_size`。預設載入所有已分析的詞元。可動態更新。
`fields` | 若要以多種方式為同一字串編製索引（例如同時作為 keyword 和 text），請提供 fields 參數。您可以指定一個版本的欄位用於搜尋，另一個版本用於排序和彙總。
`index` | 一個布林值，指定此欄位是否應可搜尋。預設為 `true`。
`index_options` | 指定要儲存在索引中供搜尋與突顯使用的資訊。有效值：`docs`（僅文件編號）、`freqs`（文件編號與詞彙頻率）、`positions`（文件編號、詞彙頻率與詞彙位置）、`offsets`（文件編號、詞彙頻率、詞彙位置以及起始與結束字元偏移量）。預設為 `positions`。
`index_phrases` | 一個布林值，指定是否單獨為 2-gram 編製索引。2-gram 是此欄位字串中兩個連續詞彙的組合。可加快無 slop 的精確片語查詢，但會使索引變大。在未移除停用詞時效果最佳。預設為 `false`。
`index_prefixes` | 一個 JSON 物件，指定單獨為詞彙前綴編製索引。前綴的字元數介於 `min_chars` 與 `max_chars` 之間（含端點）。可加快前綴搜尋，但會使索引變大。選用參數：`min_chars`、`max_chars`。預設 `min_chars` 為 2，`max_chars` 為 5。
`meta` | 接受此欄位的中繼資料。
`norms` | 一個布林值，指定計算相關性分數時是否應使用欄位長度。預設為 `true`。
`position_increment_gap` | text 欄位經過分析後會被指派位置。如果某個欄位包含字串陣列，而這些位置是連續的，可能會導致跨不同陣列元素的比對。為避免這種情況，會在連續的陣列元素之間插入一個人為間隔。您可以透過指定整數 `position_increment_gap` 來變更此間隔。注意：如果 `slop` 大於 `position_element_gap`，可能會發生跨不同陣列元素的比對。預設為 100。可動態更新。
`similarity` | 用於計算相關性分數的排名演算法。預設為 `BM25`。
[`term_vector`](#term-vector-parameter) | 一個布林值，指定是否應儲存此欄位的詞彙向量。預設為 `no`。

## 詞彙向量參數

詞彙向量是在分析期間產生的。它包含：
- 詞彙清單。
- 每個詞彙的序數位置。
- 搜尋字串在欄位內的起始與結束字元偏移量。
- 承載資料（如果有的話）。每個詞彙都可以有與該詞彙位置相關聯的自訂二進位資料。

`term_vector` 欄位包含一個接受下列參數的 JSON 物件：

參數 | 儲存的值
:--- | :---
`no` | 無。這是預設值。
`yes` | 欄位中的詞彙。
`with_offsets` | 詞彙與字元偏移量。
`with_positions_offsets` | 詞彙、位置與字元偏移量。
`with_positions_offsets_payloads` | 詞彙、位置、字元偏移量與承載資料。
`with_positions` | 詞彙與位置。
`with_positions_payloads` | 詞彙、位置與承載資料。

儲存位置對鄰近查詢很有用。儲存字元偏移量對突顯很有用。
{: .tip }

### 詞彙向量參數範例

建立一個包含 text 欄位的對應，該欄位在詞彙向量中儲存字元偏移量：

```json
PUT testindex
{
  "mappings" : {
    "properties" : {
      "dob" : {
        "type" :  "text",
        "term_vector": "with_positions_offsets"
      }
    }
  }
}
```
{% include copy-curl.html %}

為一個包含 text 欄位的文件編製索引：

```json
PUT testindex/_doc/1
{
    "dob" : "The patient's date of birth."
}
```
{% include copy-curl.html %}

查詢「date of birth」並在原始欄位中將它突顯：

```json
GET testindex/_search
{
  "query": {
    "match": {
      "dob": "date of birth"
    }
  },
  "highlight": {
    "fields": {
      "dob": {} 
    }
  }
}
```
{% include copy-curl.html %}

「date of birth」這幾個字會在回應中被突顯：

```json
{
  "took" : 854,
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
    "max_score" : 0.8630463,
    "hits" : [
      {
        "_index" : "testindex",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.8630463,
        "_source" : {
          "text" : "The patient's date of birth."
        },
        "highlight" : {
          "text" : [
            "The patient's <em>date</em> <em>of</em> <em>birth</em>."
          ]
        }
      }
    ]
  }
}
```
