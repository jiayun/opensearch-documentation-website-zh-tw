---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文字分段"
parent: Ingest processors
nav_order: 258
---

# 文字分段處理器

`text_chunking` 處理器會將長文件分割成較短的文章段落。此處理器支援下列文字分割演算法：

- [`fixed_token_length`](#the-fixed-token-length-algorithm)：依詞元數量指定的長度將文字分割成段落。
- [`fixed_char_length`](#the-fixed-character-length-algorithm)：依字元數指定的長度將文字分割成段落。
- [`delimiter`](#the-delimiter-algorithm)：依分隔符號將文字分割成段落。

以下是 `text_chunking` 處理器的語法：

```json
{
  "text_chunking": {
    "field_map": {
      "<input_field>": "<output_field>"
    },
    "algorithm": {
      "<name>": "<parameters>"
    }
  }
}
```

## 組態參數

下表列出 `text_chunking` 處理器的必要與選用參數。

| 參數                   | 資料類型 | 必要/選用  | 說明                                                                                                                                                                          |
|:----------------------------|:----------|:---|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `field_map`                 | 物件    | 必要	 | 包含鍵值對，指定文字欄位到輸出欄位的對應。	                                                                                              |
| `field_map.<input_field>`	  | 字串	   | 必要	 | 用於取得文字以產生分塊段落的來源欄位名稱。	                                                                                                    |
| `field_map.<output_field>`	 | 字串	   | 必要	 | 用於儲存分塊結果的欄位名稱。	                                                                                                                        |
| `algorithm`	                | 物件	   | 必要	 | 最多包含一組鍵值對，指定分塊演算法及其參數。                                                                                            |
| `algorithm.<name>`          | 字串	   | 選用	 | 分塊演算法的名稱。有效值為 [`fixed_token_length`](#the-fixed-token-length-algorithm)、[`fixed_char_length`](#the-fixed-character-length-algorithm) 與 [`delimiter`](#the-delimiter-algorithm)。預設為 `fixed_token_length`。	 |
| `algorithm.<parameters>`	   | 物件	   | 選用	 | 分塊演算法的參數。預設包含 `fixed_token_length` 演算法的預設參數。	                                                       |
| `ignore_missing`	           | 布林值	  | 選用	 | 若為 `true`，空欄位將從輸出中排除。若為 `false`，輸出會為每個空欄位包含一個空清單。預設為 `false`。	                                                        |
| `description`	              | 字串	   | 選用	 | 處理器的簡要說明。                                                                                                                                                |
| `tag`	                      | 字串	   | 選用	 | 處理器的識別標籤。在除錯時有助於區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。	                                                             |
| `if` | 包含布林運算式的字串 | 選用 | 執行處理器的條件。 |
| `ignore_failure` | 布林值 | 選用 | 指定處理器即使遇到錯誤仍繼續執行。若設為 `true`，處理器失敗將被忽略。預設為 `false`。 |
| `on_failure` | 清單 | 選用 | 處理器失敗時要執行的處理器清單。 |

若要對巢狀欄位執行分塊，請將 `input_field` 與 `output_field` 的值指定為 JSON 物件。不支援巢狀欄位的點路徑。例如，請使用 `"field_map": { "foo": { "bar": "bar_chunk"} }` 而非 `"field_map": { "foo.bar": "foo.bar_chunk"}`。
{: .note}

### 固定詞元長度演算法

下表列出 `fixed_token_length` 演算法的選用參數。

| 參數  | 資料類型 | 必要/選用  | 說明  |
|:---|:----------|:---|:---|
| `token_limit`	     | 整數	  | 選用	 | 每個區塊中的詞元數量上限。有效值為至少 `1` 的整數。預設為 `384`，其計算方式為 `512 (tokens) * 0.75`，以確保區塊不會超過 [OpenSearch 支援的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#supported-pretrained-models) 的 512 詞元輸入限制。`standard` 斷詞器會將文字拆分為單字，根據 [OpenAI](https://platform.openai.com/docs/introduction) 的說法，1 個詞元約等於 0.75 個英文字。	 |
| `tokenizer`	       | 字串	   | 選用	 | [單字斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/index/#word-tokenizers) 的名稱。預設為 `standard`。	 |
| `overlap_rate`	    | 浮點數     | 選用	 | 區塊之間的重疊程度。有效值為介於 `0` 與 `0.5` 之間（含）的浮點數。預設為 `0`。依照 [Amazon Bedrock](https://aws.amazon.com/blogs/aws/knowledge-bases-now-delivers-fully-managed-rag-experience-in-amazon-bedrock/) 的建議，建議使用 0--0.2 的值以提升準確度。	 |
| `max_chunk_limit`	 | 整數   | 選用	 | 區塊數量上限。如果處理器產生的區塊數超過此限制，多餘的文字會加入最後一個區塊。預設為 `100`。若要停用此參數，請將其設為 `-1`。	|

### 固定字元長度演算法

下表列出 `fixed_char_length` 演算法的選用參數。

| 參數  | 資料類型 | 必要/選用  | 說明  |
|:---|:----------|:---|:---|
| `char_limit`	     | 整數	  | 選用	 | 每個分塊的最大字元數。有效值為至少 `1` 的整數。預設為 `2048`，其計算方式為 `512 (tokens) * 4 (chars)`，因為 512 個詞元是文字嵌入模型的常見上限。根據 [OpenAI](https://platform.openai.com/docs/concepts#tokens)，1 個詞元大約等於 4 個英文字元。	 |
| `overlap_rate`	    | 浮點數     | 選用	 | 分塊之間的重疊程度。有效值為介於 `0` 與 `0.5` 之間（含端點）的浮點數。預設為 `0`。如 [Amazon Bedrock](https://aws.amazon.com/blogs/aws/knowledge-bases-now-delivers-fully-managed-rag-experience-in-amazon-bedrock/) 所建議，我們建議使用 0--0.2 的值以提升準確度。	 |
| `max_chunk_limit`	 | 整數   | 選用	 | 分塊的最大數量。如果處理器產生的分塊數超過此上限，多出來的文字會加入最後一個分塊。預設為 `100`。若要停用此參數，請將其設為 `-1`。	|

每個詞元 4 個字元的估算不適用於中文、日文或韓文文字，這些文字中 1 個詞元通常只涵蓋 1--2 個字元。例如，一個 2,048 字元的中文分塊，對 `bert-base-multilingual-uncased` 斷詞器而言約含 2,000 個詞元，對 XLM-RoBERTa 斷詞器而言約含 1,200 個詞元。文字嵌入模型會忽略超出其詞元上限的文字且不會回傳錯誤，因此這類分塊的大部分內容不會呈現在其嵌入中。對於中文、日文或韓文文字，請將 `char_limit` 設為大約等於模型的詞元上限（例如，對於詞元上限為 512 的模型，設為 `500`）。
{: .important}

### 分隔符演算法

下表列出 `delimiter` 演算法的選用參數。

| 參數  | 資料類型 | 必要/選用  | 說明  |
|:---|:---|:---|:---|
| `delimiter`	| 字串	    | 選用	 | 用於分割文字的字串分隔符。您可以將 `delimiter` 設為任何字串，例如 `\n`（以換行字元將文字分割為段落）或 `.`（將文字分割為句子）。預設為 `\n\n`（以兩個換行字元將文字分割為段落）。 |
| `max_chunk_limit`	 | 整數	   | 選用	 | 分段數量上限。若處理器產生的分段數超過此上限，多出的文字會附加到最後一個分段。預設為 `100`。若要停用此參數，請將其設為 `-1`。	 |

## 使用處理器

請依照下列步驟在管線中使用處理器。您可以在建立處理器時指定分塊演算法。如果您未提供演算法名稱，分塊處理器將使用預設的 `fixed_token_length` 演算法及其所有預設參數。

**步驟 1：建立管線**

下列範例請求會建立一個資料匯入管線，將 `passage_text` 欄位中的文字轉換為分塊段落，並儲存在 `passage_chunk` 欄位中：

```json
PUT _ingest/pipeline/text-chunking-ingest-pipeline
{
  "description": "A text chunking ingest pipeline",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 10,
            "overlap_rate": 0.2,
            "tokenizer": "standard"
          }
        },
        "field_map": {
          "passage_text": "passage_chunk"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2 (選用)：測試管線**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/text-chunking-ingest-pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex",
      "_id": "1",
      "_source":{
         "passage_text": "This is an example document to be chunked. The document contains a single paragraph, two sentences and 24 tokens by standard tokenizer in OpenSearch."
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

回應確認除了 `passage_text` 欄位之外，處理器已在 `passage_chunk` 欄位中產生分塊結果。處理器將段落分割為每塊 10 個詞的分塊。由於 `overlap` 設定為 0.2，每個分塊的最後 2 個詞會在下一個分塊中重複出現：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex",
        "_id": "1",
        "_source": {
          "passage_text": "This is an example document to be chunked. The document contains a single paragraph, two sentences and 24 tokens by standard tokenizer in OpenSearch.",
          "passage_chunk": [
            "This is an example document to be chunked. The document ",
            "The document contains a single paragraph, two sentences and 24 ",
            "and 24 tokens by standard tokenizer in OpenSearch."
          ]
        },
        "_ingest": {
          "timestamp": "2024-03-20T02:55:25.642366Z"
        }
      }
    }
  ]
}
```

建立資料匯入管線後，您需要建立一個索引來匯入文件。若要了解更多，請參閱[文字分塊]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。

## 串接文字分塊處理器

您可以將多個文字分塊處理器串接在一起。例如，若要將文件分割為段落，請套用 `delimiter` 演算法並將參數指定為 `\n\n`。為了防止段落超過詞元上限，可以附加另一個使用 `fixed_token_length` 演算法的文字分塊處理器。您可以如下設定此範例的資料匯入管線：

```json
PUT _ingest/pipeline/text-chunking-cascade-ingest-pipeline
{
  "description": "A text chunking pipeline with cascaded algorithms",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "delimiter": {
            "delimiter": "\n\n"
          }
        },
        "field_map": {
          "passage_text": "passage_chunk1"
        }
      }
    },
    {
      "text_chunking": {
        "algorithm": {
          "fixed_token_length": {
            "token_limit": 500,
            "overlap_rate": 0.2,
            "tokenizer": "standard"
          }
        },
        "field_map": {
          "passage_chunk1": "passage_chunk2"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用串接處理器進行遞迴文字分塊

若需要更進階的控制，您可以串連兩個以上的處理器，以建立遞迴分塊效果。此策略會將文字逐步解構為更小、更具語意意義的單元。

例如，您可以先將文件分割為段落 (`\n\n`)，再將每個段落分割為句子 (`. `)。最後，您可以使用 `fixed_char_length` 演算法對每個句子進行分塊，以確保最終段落不超過特定長度。這種階層式方法有助於在最終大小限制內盡可能保留語意脈絡。

下列範例設定了一個三階段遞迴分塊管線：

```json
PUT _ingest/pipeline/recursively-text-chunking-cascade-ingest-pipeline
{
  "description": "A pipeline that recursively chunks text by paragraph, then sentence, then character length.",
  "processors": [
    {
      "text_chunking": {
        "algorithm": {
          "delimiter": {
            "delimiter": "\n\n"
          }
        },
        "field_map": {
          "original_text": "paragraph_chunks"
        }
      }
    },
    {
      "text_chunking": {
        "algorithm": {
          "delimiter": {
            "delimiter": ". "
          }
        },
        "field_map": {
          "paragraph_chunks": "sentence_chunks"
        }
      }
    },
    {
      "text_chunking": {
        "algorithm": {
          "fixed_char_length": {
            "char_limit": 300,
            "overlap_rate": 0.1
          }
        },
        "field_map": {
          "sentence_chunks": "final_recursive_chunks"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 後續步驟

- 如需完整範例，請參閱[文字分塊]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。
- 若要進一步瞭解語意搜尋，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。
- 若要進一步瞭解稀疏搜尋，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。
- 若要進一步瞭解如何在 OpenSearch 中使用模型，請參閱[選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
- 如需將長文件分塊並使用外部託管模型產生嵌入的教學，請參閱[使用文字分塊進行語意搜尋]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-search/long-document/)。
