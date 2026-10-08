---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分隔酬載"
parent: Token filters
nav_order: 90
---

# 分隔酬載詞元篩選器

`delimited_payload` 詞元篩選器用於在分析過程中剖析包含酬載 (payload) 的詞元。例如，字串 `red|1.5 fast|2.0 car|1.0` 會被剖析為詞元 `red`（酬載為 `1.5`）、`fast`（酬載為 `2.0`）以及 `car`（酬載為 `1.0`）。當您的詞元包含額外的關聯資料（例如權重、分數或其他數值），且您可以將這些資料用於評分或自訂查詢邏輯時，此篩選器特別實用。此篩選器可以處理不同類型的酬載，包括整數、浮點數和字串，並將酬載（額外的中繼資料）附加至詞元。

分析文字時，`delimited_payload` 詞元篩選器會剖析每個詞元、擷取酬載，並將其附加至詞元。之後可在查詢中使用此酬載來影響評分、提升權重 (boosting) 或其他自訂行為。

酬載會以 Base64 編碼字串的形式儲存。根據預設，查詢回應中不會隨詞元一起傳回酬載。若要傳回酬載，您必須設定其他參數。如需詳細資訊，請參閱[儲存酬載的範例]({{site.url}}{{site.baseurl}}/analyzers/token-filters/delimited-payload/#example-without-a-stored-payload)。

## 參數

`delimited_payload` 詞元篩選器有兩個參數。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`encoding` | 選用 | 字串 | 指定附加至詞元之酬載的資料類型。這會決定在分析和查詢期間如何解讀酬載資料。<br>有效值為：<br><br>- `float`：酬載會以 IEEE 754 格式解讀為 32 位元浮點數（例如 `car|2.5` 中的 `2.5`）。<br>- `identity`：酬載會解讀為字元序列（例如在 `user|admin` 中，`admin` 會解讀為字串）。<br>- `int`：酬載會解讀為 32 位元整數（例如 `priority|1` 中的 `1`）。<br> 預設為 `float`。
`delimiter` | 選用 | 字串 | 指定在輸入文字中分隔詞元與其酬載的字元。預設為管道字元（`|`）。

## 未儲存酬載的範例

下列範例請求會建立名為 `my_index` 的新索引，並設定使用 `delimited_payload` 篩選器的分析器：

```json
PUT /my_index
{
  "settings": {
    "analysis": {
      "filter": {
        "my_payload_filter": {
          "type": "delimited_payload",
          "delimiter": "|",
          "encoding": "float"
        }
      },
      "analyzer": {
        "my_analyzer": {
          "type": "custom",
          "tokenizer": "whitespace",
          "filter": ["my_payload_filter"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
POST /my_index/_analyze
{
  "analyzer": "my_analyzer",
  "text": "red|1.5 fast|2.0 car|1.0"
}
```
{% include copy-curl.html %}

回應中包含產生的詞元：

```json
{
  "tokens": [
    {
      "token": "red",
      "start_offset": 0,
      "end_offset": 7,
      "type": "word",
      "position": 0
    },
    {
      "token": "fast",
      "start_offset": 8,
      "end_offset": 16,
      "type": "word",
      "position": 1
    },
    {
      "token": "car",
      "start_offset": 17,
      "end_offset": 24,
      "type": "word",
      "position": 2
    }
  ]
}
```

## 儲存酬載的範例

若要設定在回應中傳回酬載，請建立會儲存詞項向量 (term vector) 的索引，並在索引對應中將 `term_vector` 設為 `with_positions_payloads` 或 `with_positions_offsets_payloads`。例如，下列索引已設定為儲存詞項向量：

```json
PUT /visible_payloads
{
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "term_vector": "with_positions_payloads",
        "analyzer": "custom_analyzer"
      }
    }
  },
  "settings": {
    "analysis": {
      "filter": {
        "my_payload_filter": {
          "type": "delimited_payload",
          "delimiter": "|",
          "encoding": "float"
        }
      },
      "analyzer": {
        "custom_analyzer": {
          "tokenizer": "whitespace",
          "filter": [ "my_payload_filter" ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

您可以使用下列請求將文件編製索引至此索引：

```json
PUT /visible_payloads/_doc/1
{
  "text": "red|1.5 fast|2.0 car|1.0"
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢查使用此分析器產生的詞元：

```json
GET /visible_payloads/_termvectors/1
{
  "fields": ["text"]
}
```
{% include copy-curl.html %}

回應中包含產生的詞元，其中含有酬載：

```json
{
  "_index": "visible_payloads",
  "_id": "1",
  "_version": 1,
  "found": true,
  "took": 3,
  "term_vectors": {
    "text": {
      "field_statistics": {
        "sum_doc_freq": 3,
        "doc_count": 1,
        "sum_ttf": 3
      },
      "terms": {
        "brown": {
          "term_freq": 1,
          "tokens": [
            {
              "position": 1,
              "start_offset": 10,
              "end_offset": 19,
              "payload": "QEAAAA=="
            }
          ]
        },
        "fox": {
          "term_freq": 1,
          "tokens": [
            {
              "position": 2,
              "start_offset": 20,
              "end_offset": 27,
              "payload": "P8AAAA=="
            }
          ]
        },
        "quick": {
          "term_freq": 1,
          "tokens": [
            {
              "position": 0,
              "start_offset": 0,
              "end_offset": 9,
              "payload": "QCAAAA=="
            }
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
