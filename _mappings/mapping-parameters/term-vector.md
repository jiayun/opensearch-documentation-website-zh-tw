---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙向量"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/term-vector/
nav_order: 270
has_children: false
has_toc: false
---

# 詞彙向量對應參數

`term_vector` 對應參數控制是否在編製索引時為個別文字欄位儲存詞彙層級資訊。這些資訊包括詞彙頻率、位置與字元位移等詳細資料，可用於自訂評分與醒目顯示等進階功能。

預設情況下，`term_vector` 為停用狀態。啟用後，詞彙向量會被儲存，並可透過 `_termvectors` API 擷取。

啟用 `term_vector` 會增加索引大小。請只在需要詳細詞彙層級資料時才使用。
{: .important}

## 組態選項

`term_vector` 參數支援下列有效值：

- `no` (預設)：不儲存詞彙向量。
- `yes`：儲存詞彙頻率 (詞彙在特定文件中出現的次數) 與基本位置。
- `with_positions`：儲存詞彙位置，即詞彙在欄位中出現的順序。
- `with_offsets`：儲存字元位移，即詞彙在欄位文字中的確切起始與結束字元位置。
- `with_positions_offsets`：同時儲存位置與位移。
- `with_positions_payloads`：儲存詞彙位置以及酬載 (payload)，酬載是可在編製索引時附加至個別詞彙的選用自訂中繼資料 (例如標籤或數值)。酬載用於自訂評分或標記等進階情境，但需要特殊的分析器才能設定。
- `with_positions_offsets_payloads`：儲存所有詞彙向量資料。

## 在欄位上啟用 term_vector

下列請求會建立名為 `articles` 的索引，並將 `content` 欄位設定為儲存詞彙向量，包括位置與位移：

```json
PUT /articles
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "term_vector": "with_positions_offsets"
      }
    }
  }
}
```
{% include copy-curl.html %}


為範例文件編製索引：

```json
PUT /articles/_doc/1
{
  "content": "OpenSearch is an open-source search and analytics suite."
}
```
{% include copy-curl.html %}


使用 `_termvectors` API 擷取詞彙層級統計資料：

```json
POST /articles/_termvectors/1
{
  "fields": ["content"],
  "term_statistics": true,
  "positions": true,
  "offsets": true
}
```
{% include copy-curl.html %}

下列回應包含文件 ID `1` 中 `content` 欄位的詳細詞彙層級統計資料，例如詞彙頻率、文件頻率、詞元位置與字元位移：

```json
{
  "_index": "articles",
  "_id": "1",
  "_version": 1,
  "found": true,
  "took": 4,
  "term_vectors": {
    "content": {
      "field_statistics": {
        "sum_doc_freq": 9,
        "doc_count": 1,
        "sum_ttf": 9
      },
      "terms": {
        "an": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 2,
              "start_offset": 14,
              "end_offset": 16
            }
          ]
        },
        "analytics": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 7,
              "start_offset": 40,
              "end_offset": 49
            }
          ]
        },
        "and": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 6,
              "start_offset": 36,
              "end_offset": 39
            }
          ]
        },
        "is": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 1,
              "start_offset": 11,
              "end_offset": 13
            }
          ]
        },
        "open": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 3,
              "start_offset": 17,
              "end_offset": 21
            }
          ]
        },
        "opensearch": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 0,
              "start_offset": 0,
              "end_offset": 10
            }
          ]
        },
        "search": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 5,
              "start_offset": 29,
              "end_offset": 35
            }
          ]
        },
        "source": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 4,
              "start_offset": 22,
              "end_offset": 28
            }
          ]
        },
        "suite": {
          "doc_freq": 1,
          "ttf": 1,
          "term_freq": 1,
          "tokens": [
            {
              "position": 8,
              "start_offset": 50,
              "end_offset": 55
            }
          ]
        }
      }
    }
  }
}
```

## 使用詞彙向量進行醒目顯示

使用下列命令搜尋詞彙 "analytics"，並使用該欄位儲存的詞彙向量進行[醒目顯示]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)：

```json
POST /articles/_search
{
  "query": {
    "match": {
      "content": "analytics"
    }
  },
  "highlight": {
    "fields": {
      "content": {
        "type": "fvh"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列回應顯示一個相符的文件，其中在 `content` 欄位中找到詞彙 "analytics"。`highlight` 區段包含以 `<em>` 標籤包覆的相符詞彙，並使用該欄位儲存的詞彙向量來實現高效率且準確的醒目顯示：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.2876821,
    "hits": [
      {
        "_index": "articles",
        "_id": "1",
        "_score": 0.2876821,
        "_source": {
          "content": "OpenSearch is an open-source search and analytics suite."
        },
        "highlight": {
          "content": [
            "OpenSearch is an open-source search and <em>analytics</em> suite."
          ]
        }
      }
    ]
  }
}
```