---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "固定分數"
parent: Compound queries
nav_order: 40
redirect_from:
  - /query-dsl/query-dsl/compound/constant-score/
---

# 固定分數查詢

如果您需要傳回包含特定詞彙的文件，而不考慮該詞彙出現的次數，可以使用 `constant_score` 查詢。`constant_score` 查詢會包裝篩選查詢，並將結果中所有文件的相關性分數設為 `boost` 參數的值。因此，所有傳回的文件都具有相同的相關性分數，且不考慮詞頻／反向文件頻率（TF/IDF）。篩選查詢不會計算相關性分數。此外，OpenSearch 會快取經常使用的篩選查詢，以提升效能。 

## 範例

使用下列查詢，傳回 `shakespeare` 索引中包含「Hamlet」一詞的文件：

```json
GET shakespeare/_search
{
  "query": {
    "constant_score": {
      "filter": {
        "match": {
          "text_entry": "Hamlet"
        }
      },
      "boost": 1.2
    }
  }
}
```
{% include copy-curl.html %}

結果中所有文件的相關性分數都設為 1.2：

<details open markdown="block">
<summary>
    回應
</summary>
{: .text-delta }

```json
{
  "took": 8,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 96,
      "relation": "eq"
    },
    "max_score": 1.2,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "32535",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32536,
          "play_name": "Hamlet",
          "speech_number": 48,
          "line_number": "1.1.97",
          "speaker": "HORATIO",
          "text_entry": "Dared to the combat; in which our valiant Hamlet--"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32546",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32547,
          "play_name": "Hamlet",
          "speech_number": 48,
          "line_number": "1.1.108",
          "speaker": "HORATIO",
          "text_entry": "His fell to Hamlet. Now, sir, young Fortinbras,"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32625",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32626,
          "play_name": "Hamlet",
          "speech_number": 59,
          "line_number": "1.1.184",
          "speaker": "HORATIO",
          "text_entry": "Unto young Hamlet; for, upon my life,"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32633",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32634,
          "play_name": "Hamlet",
          "speech_number": 60,
          "line_number": "",
          "speaker": "MARCELLUS",
          "text_entry": "Enter KING CLAUDIUS, QUEEN GERTRUDE, HAMLET,  POLONIUS, LAERTES, VOLTIMAND, CORNELIUS, Lords, and Attendants"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32634",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32635,
          "play_name": "Hamlet",
          "speech_number": 1,
          "line_number": "1.2.1",
          "speaker": "KING CLAUDIUS",
          "text_entry": "Though yet of Hamlet our dear brothers death"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32699",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32700,
          "play_name": "Hamlet",
          "speech_number": 8,
          "line_number": "1.2.65",
          "speaker": "KING CLAUDIUS",
          "text_entry": "But now, my cousin Hamlet, and my son,--"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32703",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32704,
          "play_name": "Hamlet",
          "speech_number": 12,
          "line_number": "1.2.69",
          "speaker": "QUEEN GERTRUDE",
          "text_entry": "Good Hamlet, cast thy nighted colour off,"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32723",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32724,
          "play_name": "Hamlet",
          "speech_number": 16,
          "line_number": "1.2.89",
          "speaker": "KING CLAUDIUS",
          "text_entry": "Tis sweet and commendable in your nature, Hamlet,"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32754",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32755,
          "play_name": "Hamlet",
          "speech_number": 17,
          "line_number": "1.2.120",
          "speaker": "QUEEN GERTRUDE",
          "text_entry": "Let not thy mother lose her prayers, Hamlet:"
        }
      },
      {
        "_index": "shakespeare",
        "_id": "32759",
        "_score": 1.2,
        "_source": {
          "type": "line",
          "line_id": 32760,
          "play_name": "Hamlet",
          "speech_number": 19,
          "line_number": "1.2.125",
          "speaker": "KING CLAUDIUS",
          "text_entry": "This gentle and unforced accord of Hamlet"
        }
      }
    ]
  }
}
```
</details>

## 參數

下表列出 `constant_score ` 查詢支援的所有最上層參數。

參數 | 說明
:--- | :---
`filter` | 文件必須符合此篩選查詢，才會在結果中傳回。必要。
`boost` | 指派給所有傳回文件作為相關性分數的浮點數值。選用。預設為 1.0。