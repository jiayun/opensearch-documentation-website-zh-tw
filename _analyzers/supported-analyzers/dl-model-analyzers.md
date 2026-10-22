---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "DL 模型分析器"
parent: Analyzers
nav_order: 130
---

# DL 模型分析器

深度學習 (DL) 模型分析器專為搭配[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)而設計。它們實作與機器學習 (ML) 模型相同的斷詞規則，確保與神經稀疏搜尋相容。傳統的 OpenSearch 分析器使用標準的規則式斷詞（例如空白或單字邊界），而 DL 模型分析器則使用符合特定 ML 模型的斷詞規則（例如 BERT WordPiece 斷詞方案）。已編製索引的文件與搜尋查詢之間一致的斷詞，是神經稀疏搜尋正常運作的必要條件。

OpenSearch 支援下列 DL 模型分析器：

* [`bert-uncased`](#the-bert-uncased-analyzer)：以 [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) 模型斷詞器為基礎的分析器。
* [`mbert-uncased`](#the-mbert-uncased-analyzer)：以 [google-bert/bert-base-multilingual-uncased](https://huggingface.co/google-bert/bert-base-multilingual-uncased) 模型斷詞器為基礎的多語言分析器。

若要處理日文文字，請改用[`mbert-uncased` 分析器](#the-mbert-uncased-analyzer)：`bert-uncased` 詞彙表缺少許多假名字元，因此許多日文單字（例如 `パソコン`）會被斷詞為 `[UNK]`，而無法比對到任何文件。
{: .tip }

## 使用考量

使用 DL 模型分析器時，請留意下列考量事項：

* 這些分析器採用延遲載入。由於需要載入相依項目與相關資源，第一次呼叫這些分析器可能需要較長的時間。
* 這些斷詞器遵循與其對應模型斷詞器相同的規則。

## bert-uncased 分析器

`bert-uncased` 分析器以 [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) 模型為基礎，並依照 BERT WordPiece 斷詞機制對文字進行斷詞。此分析器特別適用於英文文字。

若要使用 `bert-uncased` 分析器分析文字，請在 `analyzer` 欄位中指定該分析器：

```json
POST /_analyze
{
  "analyzer": "bert-uncased",
  "text": "It's fun to contribute to OpenSearch!"
}
```
{% include copy-curl.html %}

## mbert-uncased 分析器

`mbert-uncased` 分析器以 [google-bert/bert-base-multilingual-uncased](https://huggingface.co/google-bert/bert-base-multilingual-uncased) 模型為基礎，支援多語言的斷詞處理，因此適合處理多語言內容的應用程式。

若要分析多語言文字，請在請求中指定 `mbert-uncased` 分析器：

```json
POST /_analyze
{
  "analyzer": "mbert-uncased",
  "text": "It's fun to contribute to OpenSearch!"
}
```
{% include copy-curl.html %}

### 半形與全形字元

與模型斷詞器相同，`mbert-uncased` 分析器不會正規化半形與全形形式。例如，半形 `ｶﾒﾗ` 會被斷詞為 `[UNK]`，因此不會與全形 `カメラ` 相符，而全形 `ＡＢＣ` 也不會與 `abc` 相符。此分析器也會移除日文濁音符號（dakuten 與 handakuten），因此 `パ` 與 `ハ` 會產生相同的詞元。

若要讓半形與全形形式相符，請對文件與查詢套用 Unicode 正規化形式相容合成（NFKC）。請在文件編碼前先進行正規化，例如在資料匯入管線中使用 `script` 處理器：

```json
PUT /_ingest/pipeline/nlp-ingest-pipeline-sparse
{
  "processors": [
    {
      "script": {
        "source": "ctx.passage_text = Normalizer.normalize(ctx.passage_text, Normalizer.Form.NFKC)"
      }
    },
    {
      "sparse_encoding": {
        "model_id": "<model_id>",
        "field_map": {
          "passage_text": "passage_embedding"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要正規化查詢，請建立自訂分析器，在 `mbert-uncased` 斷詞器之前套用 [ICU 正規化字元篩選器]({{site.url}}{{site.baseurl}}/analyzers/character-filters/icu-normalization/)。此字元篩選器需要 [`analysis-icu` 外掛程式]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/#installing-the-icu-plugin)：

```json
PUT /my-nlp-index
{
  "settings": {
    "default_pipeline": "nlp-ingest-pipeline-sparse",
    "analysis": {
      "char_filter": {
        "nfkc": {
          "type": "icu_normalizer",
          "name": "nfkc",
          "mode": "compose"
        }
      },
      "analyzer": {
        "mbert_nfkc": {
          "type": "custom",
          "char_filter": ["nfkc"],
          "tokenizer": "mbert-uncased"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "passage_text": {
        "type": "text"
      },
      "passage_embedding": {
        "type": "rank_features"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著在 `neural_sparse` 查詢中指定此自訂分析器：

```json
GET /my-nlp-index/_search
{
  "query": {
    "neural_sparse": {
      "passage_embedding": {
        "query_text": "ｶﾒﾗ",
        "analyzer": "mbert_nfkc"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例

如需在神經稀疏搜尋查詢中使用 DL 模型分析器的完整範例，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-with-pipelines/)。