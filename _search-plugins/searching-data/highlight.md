---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "醒目提示查詢相符項"
parent: Customizing search results
nav_order: 70
redirect_from:
  - /opensearch/search/highlight/
---

# 醒目提示查詢相符項

醒目提示會強調結果中的搜尋詞彙，讓您可以強調查詢相符項。

若要醒目提示搜尋詞彙，請在查詢區塊外新增 `highlight` 參數：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": "life"
    }
  },
  "size": 3,
  "highlight": {
    "fields": {
      "text_entry": {}
    }
  }
}
```

結果中的每份文件都包含一個 `highlight` 物件，顯示以 `em` 標籤包住的搜尋詞彙：

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 805,
      "relation" : "eq"
    },
    "max_score" : 7.450247,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "33765",
        "_score" : 7.450247,
        "_source" : {
          "type" : "line",
          "line_id" : 33766,
          "play_name" : "Hamlet",
          "speech_number" : 60,
          "line_number" : "2.2.233",
          "speaker" : "HAMLET",
          "text_entry" : "my life, except my life."
        },
        "highlight" : {
          "text_entry" : [
            "my <em>life</em>, except my <em>life</em>."
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "51877",
        "_score" : 6.873042,
        "_source" : {
          "type" : "line",
          "line_id" : 51878,
          "play_name" : "King Lear",
          "speech_number" : 18,
          "line_number" : "4.6.52",
          "speaker" : "EDGAR",
          "text_entry" : "The treasury of life, when life itself"
        },
        "highlight" : {
          "text_entry" : [
            "The treasury of <em>life</em>, when <em>life</em> itself"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "39245",
        "_score" : 6.6167283,
        "_source" : {
          "type" : "line",
          "line_id" : 39246,
          "play_name" : "Henry V",
          "speech_number" : 7,
          "line_number" : "4.7.31",
          "speaker" : "FLUELLEN",
          "text_entry" : "mark Alexanders life well, Harry of Monmouths life"
        },
        "highlight" : {
          "text_entry" : [
            "mark Alexanders <em>life</em> well, Harry of Monmouths <em>life</em>"
          ]
        }
      }
    ]
  }
}
```

醒目提示功能會作用於實際的欄位內容。OpenSearch 會從已儲存的欄位 (要將對應設為 `true` 的欄位) 擷取這些內容，或者，若該欄位未儲存，則從 `_source` 欄位擷取。您可以將 `force_source` 參數設為 `true`，強制從 `_source` 欄位擷取欄位內容。

即使搜尋本身使用同義詞或詞幹擷取，`highlight` 參數仍會醒目提示原始詞彙。
{: .note}

## 取得位移的方法

若要醒目提示搜尋詞彙，醒目提示器需要每個詞彙的起始與結束字元位移。位移會標示詞彙在原始文字中的位置。醒目提示器可以從下列來源取得位移：

- **倒排索引中的詞項紀錄 (Postings)**：將文件編製索引時，OpenSearch 會建立倒排搜尋索引&mdash;這是用來搜尋文件的核心資料結構。倒排索引中的詞項紀錄 (Postings) 代表倒排搜尋索引，並儲存每個分析後詞彙對應到其出現所在文件清單的對應。如果您在對應 [text 欄位]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/) 時將 `index_options` 參數設為 `offsets`，OpenSearch 會將每個詞彙的起始與結束字元位移新增至倒排索引。醒目提示期間，醒目提示器會直接在倒排索引中的詞項紀錄上重新執行原始查詢，以找出每個詞彙。因此，儲存位移可讓大型欄位的醒目提示更有效率，因為它不需要重新分析文字。儲存詞彙位移需要額外的磁碟空間，但使用的磁碟空間比儲存詞彙向量少。

- [**詞彙向量 (Term vectors)**]：如果您在對應 text 欄位時將 [`term_vector` 參數]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text#term-vector-parameter) 設為  `with_positions_offsets`，醒目提示器會使用 `term_vector` 來醒目提示該欄位。儲存詞彙向量需要最多的磁碟空間。不過，對於大於 1 MB 的欄位，以及前置詞或萬用字元等多詞彙查詢，它可讓醒目提示更快速，因為詞彙向量可存取每份文件的詞彙字典。

- **文字重新分析**：在沒有倒排索引中的詞項紀錄與詞彙向量的情況下，醒目提示器會重新分析文字以便醒目提示。對於每份需要醒目提示的文件與每個欄位，醒目提示器會建立一個小型記憶體內索引，並透過 Lucene 的查詢執行規劃器重新執行原始查詢，以存取目前文件的低階相符資訊。重新分析文字在大多數使用案例中運作良好。不過，對於大型欄位，此方法會耗用更多記憶體與時間。

## 醒目提示器類型

OpenSearch 支援四種醒目提示器實作：`plain`、`unified`、`fvh` (Fast Vector Highlighter) 及 `semantic`。

下表列出每種醒目提示器取得位移的方法。

醒目提示器 | 取得位移的方法
:--- | :---
[`unified`](#the-unified-highlighter) | 若 `term_vector` 設為 `with_positions_offsets` 則使用詞彙向量，<br> 若 `index_options` 設為 `offsets` 則使用倒排索引，<br> 否則使用文字重新分析。
[`fvh`](#the-fvh-highlighter) | 詞彙向量。
[`plain`](#the-plain-highlighter) | 文字重新分析。
[`semantic`](#the-semantic-highlighter) | 模型推論。

### 設定醒目提示器類型

若要設定醒目提示器類型，請在 `type` 欄位中指定：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": "life"
    }
  },
  "highlight": {
    "fields": {
      "text_entry": { "type": "plain"}
    }
  }
}
```

### `unified` 醒目提示器

`unified` 醒目提示器以 Lucene Unified Highlighter 為基礎，是 OpenSearch 的預設醒目提示器。它會將文字分割為句子，並將這些句子視為個別文件，使用 BM25 演算法依相似度評分。`unified` 醒目提示器同時支援精確片語與多詞彙醒目提示，包括模糊、前置詞及正規表達式。如果您使用複雜查詢來醒目提示多份文件中的多個欄位，建議在 `postings` 或 `term_vector` 欄位上使用 `unified` 醒目提示器。

### `fvh` 醒目提示器

`fvh` 醒目提示器以 Lucene Fast Vector Highlighter 為基礎。若要使用此醒目提示器，您需要儲存帶有位置位移的詞彙向量，這會增加索引大小。`fvh` 醒目提示器可以將多個欄位的相符詞彙合併為一個結果。它也可以依相符項的位置指派權重；因此，醒目提示查詢時，若查詢對片語相符項的加權高於詞彙相符項，您就可以將片語相符項排序在詞彙相符項之前。此外，您可以設定 `fvh` 醒目提示器來選取所傳回文字片段的分界，也可以使用不同標籤醒目提示多個詞彙。

### `plain` 醒目提示器

`plain` 醒目提示器以標準 Lucene 醒目提示器為基礎。它要求要醒目提示的欄位必須個別儲存，或儲存在 `_source` 欄位中。`plain` 醒目提示器會模擬查詢比對邏輯，特別是詞彙重要性以及片語查詢中的位置。它適用於大多數使用情境，但對大型欄位可能較慢，因為它必須重新分析要醒目提示的文字。

### `semantic` 醒目提示器
**3.0 版新增**
{: .label .label-purple }

`semantic` 醒目提示器使用機器學習 (ML) 模型，根據查詢的語意，識別並醒目提示文字欄位中語意上最相關的句子或段落。這超越了其他醒目提示器所提供的傳統詞彙比對。它不依賴倒排索引中的詞項紀錄或詞彙向量的偏移量，而是使用已部署的 ML 模型（由 `model_id` 指定）對欄位內容執行推論。這種方式讓您即使在確切詞彙與查詢不符時，也能醒目提示語境上相關的文字。醒目提示作業以句子為單位執行。

`semantic` 醒目提示器支援兩種處理模式：

- **單一推論模式（預設）**：逐一處理每份文件，每份文件使用一次 ML 推論呼叫。支援本機模型與外部託管模型。
- [**批次推論模式**](#batch-inference-mode)：在單一次 ML 推論呼叫中處理所有文件，可大幅提升多文件結果的效能。 

對於正式環境，我們建議使用外部託管模型並啟用批次推論，以獲得最佳效能與擴充性。
{: .tip}

在使用 `semantic` 醒目提示器之前，您必須設定並部署句子醒目提示模型。有關在 OpenSearch 中使用 ML 模型的更多資訊，請參閱 [整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。有關 OpenSearch 提供的句子醒目提示模型，請參閱 [語意句子醒目提示模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#semantic-sentence-highlighting-models)。 
{: .note}

#### 基本用法（單一推論模式）

若要使用 `semantic` 醒目提示器，請在 `fields` 物件中將 `type` 設為 `semantic`，並在全域 `highlight.options` 物件中提供已部署的句子轉換器或問答模型的 `model_id`。下列範例使用 `neural` 查詢來尋找與「神經退化性疾病的治療方法」相關的文件，然後使用指定的 `sentence_model_id` 套用語意醒目提示：

```json
POST /neural-search-index/_search
{
  "_source": {
    "excludes": ["text_embedding"]
  },
  "query": {
    "neural": {
      "text_embedding": {
        "query_text": "treatments for neurodegenerative diseases",
        "model_id": "your-text-embedding-model-id",
        "k": 5
      }
    }
  },
  "highlight": {
    "fields": {
      "text": {
        "type": "semantic"
      }
    },
    "options": {
      "model_id": "your-sentence-model-id"
    }
  }
}
```
{% include copy-curl.html %}

回應會為每個命中包含一個 `highlight` 物件，透過 <em> 標籤強調語意上最相關的句子：

```json
{
  "took": 628,
  "timed_out": false,
  "_shards": { ... },
  "hits": {
    "total": { "value": 5, "relation": "eq" },
    "max_score": 0.4841726,
    "hits": [
      {
        "_index": "neural-search-index",
        "_id": "srL7G5YBmDiZSe-G2pDc",
        "_score": 0.4841726,
        "_source": {
          "text": "Alzheimer's disease is a progressive neurodegenerative disorder characterized by accumulation of amyloid-beta plaques and neurofibrillary tangles in the brain. Early symptoms include short-term memory impairment, followed by language difficulties, disorientation, and behavioral changes. While traditional treatments such as cholinesterase inhibitors and memantine provide modest symptomatic relief, they do not alter disease progression. Recent clinical trials investigating monoclonal antibodies targeting amyloid-beta, including aducanumab, lecanemab, and donanemab, have shown promise in reducing plaque burden and slowing cognitive decline. Early diagnosis using biomarkers such as cerebrospinal fluid analysis and PET imaging may facilitate timely intervention and improved outcomes."
        },
        "highlight": {
          "text": [
            "Alzheimer's disease is a progressive neurodegenerative disorder ... <em>Recent clinical trials investigating monoclonal antibodies targeting amyloid-beta, including aducanumab, lecanemab, and donanemab, have shown promise in reducing plaque burden and slowing cognitive decline.</em> Early diagnosis using biomarkers ..."
          ]
        }
      },
      // ... other hits with highlighted sentences ...
    ]
  }
}
```

如需逐步指引，請參閱 [語意醒目提示教學]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-highlighting-tutorial/)。

#### 批次推論模式
**3.3 版新增**
{: .label .label-purple }

若要在醒目提示多份文件時提升效能，請啟用批次推論模式。批次推論模式會在單一次 ML 模型推論呼叫中處理所有符合的文件，與單一推論模式（每份文件呼叫一次）相比，可降低延遲並提升輸送量。

批次推論模式需要具備批次處理能力的外部託管模型。本機模型不支援批次推論。有關外部託管模型的資訊，請參閱 [連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/)。
{: .note}

首先，設定叢集設定（一次性設定）：

```json
PUT _cluster/settings
{
  "persistent": {
    "search.pipeline.enabled_system_generated_factories": ["semantic-highlighter"]
  }
}
```
{% include copy-curl.html %}

接著在請求層級將 `ext.semantic_highlighting_batch` 設為 `true`。這會為請求中每個設定為 `type: semantic` 的醒目提示欄位啟用批次推論。

下列範例為頂層欄位啟用批次語意醒目提示：

```json
POST /neural-search-index/_search
{
  "_source": {
    "excludes": ["text_embedding"]
  },
  "query": {
    "neural": {
      "text_embedding": {
        "query_text": "treatments for neurodegenerative diseases",
        "model_id": "your-text-embedding-model-id",
        "k": 5
      }
    }
  },
  "highlight": {
    "fields": {
      "text": {
        "type": "semantic"
      }
    },
    "options": {
      "model_id": "your-remote-semantic-highlighting-model-id"
    }
  },
  "ext": {
    "semantic_highlighting_batch": true
  }
}
```
{% include copy-curl.html %}

下列範例為 `inner_hits` 內的欄位啟用批次語意醒目提示：

```json
POST /neural-search-index/_search
{
  "query": {
    "nested": {
      "path": "chunks",
      "query": {
        "match": { "chunks.text": "treatments for neurodegenerative diseases" }
      },
      "inner_hits": {
        "size": 5,
        "highlight": {
          "fields": {
            "chunks.text": { "type": "semantic" }
          },
          "options": {
            "model_id": "your-remote-semantic-highlighting-model-id"
          }
        }
      }
    }
  },
  "ext": {
    "semantic_highlighting_batch": true
  }
}
```
{% include copy-curl.html %}

批次推論提供的回應格式與單一推論相同。

## 醒目提示選項

下表說明您可以在全域或欄位層級指定的醒目提示選項。欄位層級設定會覆寫全域設定。

選項 | 說明
:--- | :---
`type` | 指定要使用的醒目提示器。有效值為 `unified`、`fvh`、`plain` 和 `semantic`。預設為 `unified`。
`fields` | 指定要搜尋醒目提示文字的欄位。支援萬用字元運算式。若使用萬用字元，則只會醒目提示 `text` 和 `keyword` 欄位。例如，您可以將 `fields` 設為 `my_field*`，以包含所有開頭為前置字元 `my_field` 的 `text` 和 `keyword` 欄位。 
`force_source` | 指定醒目提示的欄位值應取自 `_source` 欄位，而非取自已儲存的欄位值。預設為 `false`。
`require_field_match` | 指定是否只醒目提示包含搜尋查詢相符項目的欄位。預設為 `true`。若要醒目提示所有欄位，請將此選項設為 `false`。
`pre_tags` | 以字串陣列指定醒目提示文字的 HTML 起始標籤。
`post_tags` | 以字串陣列指定醒目提示文字的 HTML 結束標籤。
`tags_schema` | 若將此選項設為 `styled`，OpenSearch 會使用內建的標籤結構描述。在此結構描述中，`pre_tags` 為 `<em class="hlt1">`、`<em class="hlt2">`、`<em class="hlt3">`、`<em class="hlt4">`、`<em class="hlt5">`、`<em class="hlt6">`、`<em class="hlt7">`、`<em class="hlt8">`、`<em class="hlt9">` 和 `<em class="hlt10">`，而 `post_tags` 為 `</em>`。
`boundary_chars` | 所有邊界字元組合成一個字串。<br> 預設為 `".,!? \t\n"`。
`boundary_scanner` | 僅適用於 `unified` 和 `fvh` 醒目提示器。指定是否將醒目提示的片段分割為句子、單字或字元。有效值如下：<br>- `sentence`：依 [BreakIterator](https://docs.oracle.com/javase/8/docs/api/java/text/BreakIterator.html) 的定義，在句子邊界分割醒目提示的片段。您可以在 `boundary_scanner_locale` 選項中指定 BreakIterator 的地區設定。 <br>- `word`：依 [BreakIterator](https://docs.oracle.com/javase/8/docs/api/java/text/BreakIterator.html) 的定義，在單字邊界分割醒目提示的片段。您可以在 `boundary_scanner_locale` 選項中指定 BreakIterator 的地區設定。<br>- `chars`：在 `boundary_chars` 中列出的任何字元處分割醒目提示的片段。僅適用於 `fvh` 醒目提示器。 
`boundary_scanner_locale` | 為 `boundary_scanner` 提供 [地區設定](https://docs.oracle.com/javase/8/docs/api/java/util/Locale.html)。有效值為語言標籤（例如 `"en-US"`）。預設為 [Locale.ROOT](https://docs.oracle.com/javase/8/docs/api/java/util/Locale.html#ROOT)。
`boundary_max_scan` | 當 `fvh` 醒目提示器的 `boundary_scanner` 參數設為 `chars` 時，控制掃描邊界字元的距離。預設為 20。
`encoder` | 指定醒目提示的片段在傳回之前是否應進行 HTML 編碼。有效值為 `default`（不編碼）或 `html`（先逸出 HTML 文字，再插入醒目提示標籤）。例如，若欄位文字為 `<h3>Hamlet</h3>` 且 `encoder` 設為 `html`，則醒目提示的文字為 `"&lt;h3&gt;<em>Hamlet</em>&lt;&#x2F;h3&gt;"`。 
`fragmenter` | 指定如何將文字分割為醒目提示的片段。僅適用於 `plain` 醒目提示器。有效值如下：<br>- `span`（預設）：將文字分割為大小相同的片段，但盡量不在醒目提示詞彙之間分割文字。 <br>- `simple`：將文字分割為大小相同的片段。
`fragment_offset` | 指定您要開始醒目提示的字元位移。僅適用於 `fvh` 醒目提示器。
`fragment_size` | 醒目提示片段的大小，以字元數指定。若 `number_of_fragments` 設為 0，則忽略 `fragment_size`。預設為 100。
`number_of_fragments`| 傳回的片段數上限。若 `number_of_fragments` 設為 0，OpenSearch 會傳回整個欄位的醒目提示內容。預設為 5。
`order` | 醒目提示片段的排序順序。將 `order` 設為 `score`，以依相關性排序片段。每個醒目提示器使用不同的演算法來計算相關性分數。預設為 `none`。
`highlight_query` | 指定應醒目提示搜尋查詢以外之查詢的相符項目。當使用較快的查詢取得文件相符項目，並使用較慢的查詢（例如 `rescore_query`）來精簡結果時，`highlight_query` 選項很有用。我們建議將搜尋查詢納入 `highlight_query` 中。
`matched_fields` | 合併來自不同欄位的相符項目，以醒目提示單一欄位。此功能最常見的使用案例是醒目提示以不同方式分析並保留在多欄位中的文字。若使用 `fvh`，`matched_fields` 清單中的所有欄位都必須將其 `term_vector` 欄位設為 `with_positions_offsets`。合併相符項目的欄位是唯一載入的欄位，因此建議將其 `store` 選項設為 `yes`。僅適用於 `fvh` 和 `unified` 醒目提示器。
`no_match_size` | 指定若沒有相符的片段可醒目提示時，從欄位開頭算起要傳回的字元數。預設為 0。
`phrase_limit` | 文件中納入考量的相符片語數。限制 `fvh` 醒目提示器要分析的片語數，以避免耗用大量記憶體。若使用 `matched_fields`，`phrase_limit` 會指定每個相符欄位的片語數。`phrase_limit` 越高，查詢時間越長，記憶體耗用也越多。僅適用於 `fvh` 醒目提示器。預設為 256。
`max_analyzer_offset` | 指定醒目提示請求要分析的字元數上限。其餘文字將不會處理。若要醒目提示的文字超過此位移，則會傳回空的醒目提示。醒目提示請求要分析的字元數上限由 `index.highlight.max_analyzed_offset` 定義。達到此限制時，會傳回錯誤。請將 `max_analyzer_offset` 設為低於 `index.highlight.max_analyzed_offset` 的值，以避免發生錯誤。
`options` | 包含醒目提示器特定選項的全域物件。
`options.max_inference_batch_size` | 指定使用批次推論模式時，每個傳送至模型伺服器的推論請求要包含的文件數上限。若要處理的文件數超過此值，則會以此大小的批次反覆處理文件。預設為 `100`。僅適用於啟用批次推論模式時的 `semantic` 醒目提示器。
`options.model_id` | 要用於醒目提示的已部署 ML 模型 ID。`semantic` 醒目提示器為必要。啟用批次推論模式時，模型必須是具備批次處理能力的外部託管模型。請參閱[連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。

unified 醒目提示器的句子掃描器會將大於 `fragment_size` 的句子，在達到 `fragment_size` 後的第一個單字邊界處分割。若要傳回完整句子而不分割，請將 `fragment_size` 設為 0。
{: .note}

## 變更醒目提示標籤

請設計您的應用程式程式碼，以剖析 `highlight` 物件的結果，並對搜尋詞彙執行動作，例如變更其顏色或套用粗體或斜體格式。

若要變更預設的 `em` 標籤，請在 `pretag` 與 `posttag` 參數中指定新的標籤：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "play_name": "Henry IV"
    }
  },
  "size": 3,
  "highlight": {
    "pre_tags": [
      "<strong>"
    ],
    "post_tags": [
      "</strong>"
    ],
    "fields": {
      "play_name": {}
    }
  }
}
```

劇本名稱會在回應中以新標籤醒目提示：

```json
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3205,
      "relation" : "eq"
    },
    "max_score" : 3.548232,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "0",
        "_score" : 3.548232,
        "_source" : {
          "type" : "act",
          "line_id" : 1,
          "play_name" : "Henry IV",
          "speech_number" : "",
          "line_number" : "",
          "speaker" : "",
          "text_entry" : "ACT I"
        },
        "highlight" : {
          "play_name" : [
            "<strong>Henry IV</strong>"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "1",
        "_score" : 3.548232,
        "_source" : {
          "type" : "scene",
          "line_id" : 2,
          "play_name" : "Henry IV",
          "speech_number" : "",
          "line_number" : "",
          "speaker" : "",
          "text_entry" : "SCENE I. London. The palace."
        },
        "highlight" : {
          "play_name" : [
            "<strong>Henry IV</strong>"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "2",
        "_score" : 3.548232,
        "_source" : {
          "type" : "line",
          "line_id" : 3,
          "play_name" : "Henry IV",
          "speech_number" : "",
          "line_number" : "",
          "speaker" : "",
          "text_entry" : "Enter KING HENRY, LORD JOHN OF LANCASTER, the EARL of WESTMORELAND, SIR WALTER BLUNT, and others"
        },
        "highlight" : {
          "play_name" : [
            "<strong>Henry IV</strong>"
          ]
        }
      }
    ]
  }
}
```

## 指定醒目提示查詢

預設情況下，OpenSearch 僅會考慮搜尋查詢來進行醒目提示。如果您使用快速查詢取得文件符合結果，並使用較慢的查詢（例如 `rescore_query`）來精煉結果，則對精煉後的結果進行醒目提示會很有用。您可以透過新增 `highlight_query` 來達成：

```json
GET shakespeare/_search
{
  "query": {
    "match": {
      "text_entry": {
        "query": "thats my name"
      }
    }
  },
  "rescore": {
    "window_size": 20,
    "query": {
      "rescore_query": {
        "match_phrase": {
          "text_entry": {
            "query": "thats my name",
            "slop": 1
          }
        }
      },
      "rescore_query_weight": 5
    }
  },
  "_source": false,
  "highlight": {
    "order": "score",
    "fields": {
      "text_entry": {
        "highlight_query": {
          "bool": {
            "must": {
              "match": {
                "text_entry": {
                  "query": "thats my name"
                }
              }
            },
            "should": {
              "match_phrase": {
                "text_entry": {
                  "query": "that is my name",
                  "slop": 1,
                  "boost": 10.0
                }
              }
            },
            "minimum_should_match": 0
          }
        }
      }
    }
  }
}
```

## 合併不同欄位的符合結果以醒目提示單一欄位

您可以使用 `fvh` 醒目提示器，合併來自不同欄位的符合結果，以醒目提示單一欄位。此功能最常見的使用案例，是醒目提示以不同方式分析並儲存在多欄位（multi-fields）中的文字。`matched_fields` 清單中的所有欄位都必須將 `term_vector` 欄位設為 `with_positions_offsets`。合併符合結果的欄位是唯一載入的欄位，因此將其 `store` 選項設為 `yes` 會有所助益。

### 範例

為 `shakespeare` 索引建立對應，其中 `text_entry` 欄位使用 `standard` 分析器進行分析，並具有使用 `english` 分析器分析的 `english` 子欄位：

```json
PUT shakespeare
{
  "mappings" : {
    "properties" : {
      "text_entry" : {
        "type" :  "text",
        "term_vector": "with_positions_offsets",
        "fields": {
          "english": { 
            "type":     "text",
            "analyzer": "english",
            "term_vector": "with_positions_offsets"
          }
        }
      }
    }
  }
}
```

`standard` 分析器會將 `text_entry` 欄位拆分為個別單字。您可以使用 analyze API 操作來確認這一點：

```json
GET shakespeare/_analyze
{
  "text": "bragging of thine",
  "field": "text_entry"
}
```

回應包含以空白字元拆分的原始字串：

```json
{
  "tokens" : [
    {
      "token" : "bragging",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "of",
      "start_offset" : 9,
      "end_offset" : 11,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "thine",
      "start_offset" : 12,
      "end_offset" : 17,
      "type" : "<ALPHANUM>",
      "position" : 2
    }
  ]
}
```

`english` 分析器不僅會將字串拆分為單字，還會對詞元進行詞幹提取並移除停用詞。您可以使用 analyze API 操作搭配 `text_entry.english` 欄位來確認這一點：

```json
GET shakespeare/_analyze
{
  "text": "bragging of thine",
  "field": "text_entry.english"
}
```

回應包含經過詞幹提取的單字：

```json
{
  "tokens" : [
    {
      "token" : "brag",
      "start_offset" : 0,
      "end_offset" : 8,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "thine",
      "start_offset" : 12,
      "end_offset" : 17,
      "type" : "<ALPHANUM>",
      "position" : 2
    }
  ]
}
```

若要搜尋 `bragging` 一詞的所有形式，請使用下列查詢：

```json
GET shakespeare/_search
{
  "query": {
    "query_string": {
      "query": "text_entry.english:bragging",
      "fields": [
        "text_entry"
      ]
    }
  },
  "highlight": {
    "order": "score",
    "fields": {
      "text_entry": {
        "matched_fields": [
          "text_entry",
          "text_entry.english"
        ],
        "type": "fvh"
      }
    }
  }
}
```

回應會醒目提示 `text_entry` 欄位中 "bragging" 一詞的所有版本：

```json
{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 26,
      "relation" : "eq"
    },
    "max_score" : 10.153671,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "56666",
        "_score" : 10.153671,
        "_source" : {
          "type" : "line",
          "line_id" : 56667,
          "play_name" : "macbeth",
          "speech_number" : 34,
          "line_number" : "2.3.118",
          "speaker" : "MACBETH",
          "text_entry" : "Is left this vault to brag of."
        },
        "highlight" : {
          "text_entry" : [
            "Is left this vault to <em>brag</em> of."
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "71445",
        "_score" : 9.284528,
        "_source" : {
          "type" : "line",
          "line_id" : 71446,
          "play_name" : "Much Ado about nothing",
          "speech_number" : 18,
          "line_number" : "5.1.65",
          "speaker" : "LEONATO",
          "text_entry" : "As under privilege of age to brag"
        },
        "highlight" : {
          "text_entry" : [
            "As under privilege of age to <em>brag</em>"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "86782",
        "_score" : 9.284528,
        "_source" : {
          "type" : "line",
          "line_id" : 86783,
          "play_name" : "Romeo and Juliet",
          "speech_number" : 8,
          "line_number" : "2.6.31",
          "speaker" : "JULIET",
          "text_entry" : "Brags of his substance, not of ornament:"
        },
        "highlight" : {
          "text_entry" : [
            "<em>Brags</em> of his substance, not of ornament:"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "44531",
        "_score" : 8.552448,
        "_source" : {
          "type" : "line",
          "line_id" : 44532,
          "play_name" : "King John",
          "speech_number" : 15,
          "line_number" : "3.1.124",
          "speaker" : "CONSTANCE",
          "text_entry" : "A ramping fool, to brag and stamp and swear"
        },
        "highlight" : {
          "text_entry" : [
            "A ramping fool, to <em>brag</em> and stamp and swear"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "63208",
        "_score" : 8.552448,
        "_source" : {
          "type" : "line",
          "line_id" : 63209,
          "play_name" : "Merchant of Venice",
          "speech_number" : 11,
          "line_number" : "3.4.79",
          "speaker" : "PORTIA",
          "text_entry" : "A thousand raw tricks of these bragging Jacks,"
        },
        "highlight" : {
          "text_entry" : [
            "A thousand raw tricks of these <em>bragging</em> Jacks,"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "73026",
        "_score" : 8.552448,
        "_source" : {
          "type" : "line",
          "line_id" : 73027,
          "play_name" : "Othello",
          "speech_number" : 75,
          "line_number" : "2.1.242",
          "speaker" : "IAGO",
          "text_entry" : "but for bragging and telling her fantastical lies:"
        },
        "highlight" : {
          "text_entry" : [
            "but for <em>bragging</em> and telling her fantastical lies:"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "85974",
        "_score" : 8.552448,
        "_source" : {
          "type" : "line",
          "line_id" : 85975,
          "play_name" : "Romeo and Juliet",
          "speech_number" : 20,
          "line_number" : "1.5.70",
          "speaker" : "CAPULET",
          "text_entry" : "And, to say truth, Verona brags of him"
        },
        "highlight" : {
          "text_entry" : [
            "And, to say truth, Verona <em>brags</em> of him"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "96800",
        "_score" : 8.552448,
        "_source" : {
          "type" : "line",
          "line_id" : 96801,
          "play_name" : "Titus Andronicus",
          "speech_number" : 60,
          "line_number" : "1.1.311",
          "speaker" : "SATURNINUS",
          "text_entry" : "Agree these deeds with that proud brag of thine,"
        },
        "highlight" : {
          "text_entry" : [
            "Agree these deeds with that proud <em>brag</em> of thine,"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "18189",
        "_score" : 7.9273787,
        "_source" : {
          "type" : "line",
          "line_id" : 18190,
          "play_name" : "As you like it",
          "speech_number" : 12,
          "line_number" : "5.2.30",
          "speaker" : "ROSALIND",
          "text_entry" : "and Caesars thrasonical brag of I came, saw, and"
        },
        "highlight" : {
          "text_entry" : [
            "and Caesars thrasonical <em>brag</em> of I came, saw, and"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "32054",
        "_score" : 7.9273787,
        "_source" : {
          "type" : "line",
          "line_id" : 32055,
          "play_name" : "Cymbeline",
          "speech_number" : 52,
          "line_number" : "5.5.211",
          "speaker" : "IACHIMO",
          "text_entry" : "And then a mind put int, either our brags"
        },
        "highlight" : {
          "text_entry" : [
            "And then a mind put int, either our <em>brags</em>"
          ]
        }
      }
    ]
  }
}
```

若要讓「bragging」這個字的原始形式獲得較高的分數，您可以提升 `text_entry` 欄位的權重：

```json
GET shakespeare/_search
{
  "query": {
    "query_string": {
      "query": "bragging",
      "fields": [
        "text_entry^5",
        "text_entry.english"
      ]
    }
  },
  "highlight": {
    "order": "score",
    "fields": {
      "text_entry": {
        "matched_fields": [
          "text_entry",
          "text_entry.english"
        ],
        "type": "fvh"
      }
    }
  }
}
```

回應會先列出包含「bragging」這個字的文件：

```json
{
  "took" : 17,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 26,
      "relation" : "eq"
    },
    "max_score" : 49.746853,
    "hits" : [
      {
        "_index" : "shakespeare",
        "_id" : "45739",
        "_score" : 49.746853,
        "_source" : {
          "type" : "line",
          "line_id" : 45740,
          "play_name" : "King John",
          "speech_number" : 10,
          "line_number" : "5.1.51",
          "speaker" : "BASTARD",
          "text_entry" : "Of bragging horror: so shall inferior eyes,"
        },
        "highlight" : {
          "text_entry" : [
            "Of <em>bragging</em> horror: so shall inferior eyes,"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "63208",
        "_score" : 47.077244,
        "_source" : {
          "type" : "line",
          "line_id" : 63209,
          "play_name" : "Merchant of Venice",
          "speech_number" : 11,
          "line_number" : "3.4.79",
          "speaker" : "PORTIA",
          "text_entry" : "A thousand raw tricks of these bragging Jacks,"
        },
        "highlight" : {
          "text_entry" : [
            "A thousand raw tricks of these <em>bragging</em> Jacks,"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "68474",
        "_score" : 47.077244,
        "_source" : {
          "type" : "line",
          "line_id" : 68475,
          "play_name" : "A Midsummer nights dream",
          "speech_number" : 101,
          "line_number" : "3.2.427",
          "speaker" : "PUCK",
          "text_entry" : "Thou coward, art thou bragging to the stars,"
        },
        "highlight" : {
          "text_entry" : [
            "Thou coward, art thou <em>bragging</em> to the stars,"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "73026",
        "_score" : 47.077244,
        "_source" : {
          "type" : "line",
          "line_id" : 73027,
          "play_name" : "Othello",
          "speech_number" : 75,
          "line_number" : "2.1.242",
          "speaker" : "IAGO",
          "text_entry" : "but for bragging and telling her fantastical lies:"
        },
        "highlight" : {
          "text_entry" : [
            "but for <em>bragging</em> and telling her fantastical lies:"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "39816",
        "_score" : 44.679565,
        "_source" : {
          "type" : "line",
          "line_id" : 39817,
          "play_name" : "Henry V",
          "speech_number" : 28,
          "line_number" : "5.2.138",
          "speaker" : "KING HENRY V",
          "text_entry" : "armour on my back, under the correction of bragging"
        },
        "highlight" : {
          "text_entry" : [
            "armour on my back, under the correction of <em>bragging</em>"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "63200",
        "_score" : 44.679565,
        "_source" : {
          "type" : "line",
          "line_id" : 63201,
          "play_name" : "Merchant of Venice",
          "speech_number" : 11,
          "line_number" : "3.4.71",
          "speaker" : "PORTIA",
          "text_entry" : "Like a fine bragging youth, and tell quaint lies,"
        },
        "highlight" : {
          "text_entry" : [
            "Like a fine <em>bragging</em> youth, and tell quaint lies,"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "56666",
        "_score" : 10.153671,
        "_source" : {
          "type" : "line",
          "line_id" : 56667,
          "play_name" : "macbeth",
          "speech_number" : 34,
          "line_number" : "2.3.118",
          "speaker" : "MACBETH",
          "text_entry" : "Is left this vault to brag of."
        },
        "highlight" : {
          "text_entry" : [
            "Is left this vault to <em>brag</em> of."
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "71445",
        "_score" : 9.284528,
        "_source" : {
          "type" : "line",
          "line_id" : 71446,
          "play_name" : "Much Ado about nothing",
          "speech_number" : 18,
          "line_number" : "5.1.65",
          "speaker" : "LEONATO",
          "text_entry" : "As under privilege of age to brag"
        },
        "highlight" : {
          "text_entry" : [
            "As under privilege of age to <em>brag</em>"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "86782",
        "_score" : 9.284528,
        "_source" : {
          "type" : "line",
          "line_id" : 86783,
          "play_name" : "Romeo and Juliet",
          "speech_number" : 8,
          "line_number" : "2.6.31",
          "speaker" : "JULIET",
          "text_entry" : "Brags of his substance, not of ornament:"
        },
        "highlight" : {
          "text_entry" : [
            "<em>Brags</em> of his substance, not of ornament:"
          ]
        }
      },
      {
        "_index" : "shakespeare",
        "_id" : "44531",
        "_score" : 8.552448,
        "_source" : {
          "type" : "line",
          "line_id" : 44532,
          "play_name" : "King John",
          "speech_number" : 15,
          "line_number" : "3.1.124",
          "speaker" : "CONSTANCE",
          "text_entry" : "A ramping fool, to brag and stamp and swear"
        },
        "highlight" : {
          "text_entry" : [
            "A ramping fool, to <em>brag</em> and stamp and swear"
          ]
        }
      }
    ]
  }
}
```

## 查詢限制

請注意以下限制：

- 在擷取要突顯的詞彙時，突顯器不會反映查詢的布林邏輯。因此，對於某些複雜的布林查詢，例如巢狀布林查詢以及使用 `minimum_should_match` 的查詢，OpenSearch 可能會突顯與查詢比對結果不相符的詞彙。
- `fvh` 突顯器不支援 span 查詢。
- `semantic` 突顯器需要部署由 `highlight.options` 中 `model_id` 指定的 ML 模型。它不使用傳統的位移方法（postings 與 term vectors），而完全依賴模型推論。若要使用批次推論模式，您必須使用具備批次處理能力的外部託管模型。