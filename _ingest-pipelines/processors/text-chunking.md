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

| 參數                   | 資料類型 | 必要／選用  | 說明                                                                                                                                                                          |
|:----------------------------|:----------|:---|:-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `field_map`                 | 物件    | 必要	 | 包含鍵值對，用於指定文字欄位到輸出欄位的對應。	                                                                                              |
| `field_map.<input_field>`	  | 字串	   | 必要	 | 從中取得文字以產生分段段落的欄位名稱。	                                                                                                    |
| `field_map.<output_field>`	 | 字串	   | 必要	 | 儲存分段結果的欄位名稱。	                                                                                                                        |
| `algorithm`	                | 物件	   | 必要	 | 包含最多一個鍵值對，用於指定分段演算法與參數。                                                                                            |
| `algorithm.<name>`          | 字串	   | 選用	 | 分段演算法的名稱。有效值為 [`fixed_token_length`](#the-fixed-token-length-algorithm)、[`fixed_char_length`](#the-fixed-character-length-algorithm) 及 [`delimiter`](#the-delimiter-algorithm)。預設為 `fixed_token_length`。	 |
| `algorithm.<parameters>`	   | 物件	   | 選用	 | 分段演算法的參數。依預設，包含 `fixed_token_length` 演算法的預設參數。	                                                       |
| `ignore_missing`	           | 布林值	  | 選用	 | 若為 `true`，空欄位會從輸出中排除。若為 `false`，輸出會為每個空欄位包含空清單。預設為 `false`。	                                                        |
| `description`	              | 字串	   | 選用	 | 處理器的簡短描述。                                                                                                                                                |
| `tag`	                      | 字串	   | 選用	 | 處理器的識別標籤。在偵錯時可用來區分同類型的處理器。	                                                             |

若要對巢狀欄位執行分段，請將 `input_field` 與 `output_field` 值指定為 JSON 物件。不支援巢狀欄位的點路徑。例如，請使用 `"field_map": { "foo": { "bar": "bar_chunk"} }` 而非 `"field_map": { "foo.bar": "foo.bar_chunk"}`。
{: .note}

### 固定詞元長度演算法

下表列出 `fixed_token_length` 演算法的選用參數。

| 參數  | 資料類型 | 必要／選用  | 說明  |
|:---|:----------|:---|:---|
| `token_limit`	     | 整數	  | 選用	 | 分段演算法的詞元上限。有效值為至少 `1` 的整數。預設為 `384`。	                                                  |
| `tokenizer`	       | 字串	   | 選用	 | [單字斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/index/#word-tokenizers) 名稱。預設為 `standard`。	 |
| `overlap_rate`	    | 浮點數     | 選用	 | 詞元演算法中的重疊程度。有效值為介於 `0` 與 `0.5` 之間（含）的浮點數。預設為 `0`。	                                              |
| `max_chunk_limit`	 | 整數   | 選用	 | 分段演算法的分段上限。預設為 `100`。若要停用此參數，請將其設為 `-1`。	|

`token_limit` 的預設值計算方式為 `512 (tokens) * 0.75 = 384`，使輸出段落不會超過下游文字嵌入模型的詞元上限限制。對於 [OpenSearch 支援的預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/#supported-pretrained-models)，例如 `msmarco-distilbert-base-tas-b` 與 `opensearch-neural-sparse-encoding-v1`，輸入詞元上限為 `512`。`standard` 斷詞器會將文字斷詞為詞。根據 [OpenAI](https://platform.openai.com/docs/introduction)，1 個詞元約等於 0.75 個英文單字。
{: .note}

您可以將 `overlap_rate` 設為 0--0.5 範圍（含）內的小數百分比值。如 [Amazon Bedrock](https://aws.amazon.com/blogs/aws/knowledge-bases-now-delivers-fully-managed-rag-experience-in-amazon-bedrock/) 所建議，我們建議將此參數設為 0–0.2 以提升準確度。
{: .note}

`max_chunk_limit` 參數會限制分段段落的數量。若處理器產生的段落數超過上限，多出的文字會加入最後一個分段。
{: .note}

### 固定字元長度演算法

下表列出 `fixed_char_length` 演算法的選用參數。

| 參數  | 資料類型 | 必要／選用  | 說明  |
|:---|:----------|:---|:---|
| `char_limit`	     | 整數	  | 選用	 | 分段演算法的字元上限。有效值為至少 `1` 的整數。預設為 `2048`。	                                                  |
| `overlap_rate`	    | 浮點數     | 選用	 | 詞元演算法中的重疊程度。有效值為介於 `0` 與 `0.5` 之間（含）的浮點數。預設為 `0`。	                                              |
| `max_chunk_limit`	 | 整數   | 選用	 | 分段演算法的分段上限。預設為 `100`。若要停用此參數，請將其設為 `-1`。	|

`char_limit` 的預設值計算方式為 `512 (tokens) * 4 (chars) = 2048`，因為 512 個詞元是文字嵌入模型的常見上限。根據 [OpenAI](https://platform.openai.com/docs/concepts#tokens)，1 個詞元約等於 4 個英文字元。
{: .note}

您可以將 `overlap_rate` 設為 0--0.5 範圍（含）內的小數百分比值。如 [Amazon Bedrock](https://aws.amazon.com/blogs/aws/knowledge-bases-now-delivers-fully-managed-rag-experience-in-amazon-bedrock/) 所建議，我們建議將此參數設為 0–0.2 以提升準確度。
{: .note}

`max_chunk_limit` 參數會限制分段段落的數量。若處理器產生的段落數超過上限，多出的文字會加入最後一個分段。
{: .note}

### 分隔符演算法

下表列出 `delimiter` 演算法的選用參數。

| 參數  | 資料類型 | 必要／選用  | 說明  |
|:---|:---|:---|:---|
| `delimiter`	| 字串	    | 選用	 | 用於分割文字的字串分隔符。您可以將 `delimiter` 設定為任何字串，例如 `\n`（以換行將文字分割為段落）或 `.`（以句點將文字分割成句子）。預設為 `\n\n`（以兩個換行字元將文字分割為段落）。 |
| `max_chunk_limit`	 | 整數	   | 選用	 | 分段演算法的分段上限。預設為 `100`。若要停用此參數，請將其設定為 `-1`。	 |

`max_chunk_limit` 參數限制分段段落的數量。如果處理器產生的段落數量超過上限，多出的文字會加入最後一個分段。
{: .note}

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

回應確認除了 `passage_text` 欄位之外，處理器已在 `passage_chunk` 欄位中產生分段結果。處理器將段落分割為 10 個詞的分段。由於 `overlap` 設定為 0.2，每個分段的最後 2 個詞會在下一個分段中重複出現：

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

建立資料匯入管線後，您需要建立一個索引來匯入文件。若要了解更多，請參閱 [文字分段]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。

## 級聯文字分塊處理器

您可以將多個文字分塊處理器串連在一起。例如，若要將文件分割為段落，請套用 `delimiter` 演算法並將參數指定為 `\n\n`。為了防止段落超過詞元上限，可以附加另一個使用 `fixed_token_length` 演算法的文字分塊處理器。您可以如下設定此範例的資料匯入管線：

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

### 使用級聯處理器的遞迴文字分塊

若需要更進階的控制，您可以串連兩個以上的處理器，以建立遞迴分塊效果。此策略會將文字逐步解構為更小、更具語意意義的單元。

例如，您可以先將文件分割為段落 (`\n\n`)，再將每個段落分割為句子 (`. `)。最後，您可以使用 `fixed_char_length` 演算法對每個句子進行分塊，以確保最終段落不超過特定長度。這種階層式方法有助於在最終大小限制內盡可能保留語意上下文。

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

- 如需完整範例，請參閱 [文字分段]({{site.url}}{{site.baseurl}}/search-plugins/text-chunking/)。
- 若要了解更多關於語意搜尋的資訊，請參閱 [語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。
- 若要了解更多關於稀疏搜尋的資訊，請參閱 [神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。
- 若要了解更多關於在 OpenSearch 中使用模型的資訊，請參閱 [選擇模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/#choosing-a-model)。
