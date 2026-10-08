---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞元圖"
nav_order: 150
---

# 詞元圖

詞元圖顯示文字分析期間詞元之間的關係，特別是在處理多字同義詞或複合詞時。詞元圖有助於確保查詢比對與片語擴充的準確性。

每個詞元都會被指派下列中繼資料：

- `position` – 詞元在文字中的位置

- `positionLength` – 詞元跨越的位置數（用於多字表達式）

詞元圖使用這些資訊建立詞元關係的圖形結構，供後續剖析查詢時使用。具備圖形感知能力的詞元篩選器，例如 [`synonym_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym-graph/) 和 [`word_delimiter_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/word-delimiter-graph/)，可讓您更準確地比對片語。

下圖說明使用 [`synonym_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym-graph/) 時 `position` 與 `positionLength` 之間的關係。「NYC」詞元的 `position` 被指派為 `0`，`positionLength` 被指派為 `3`。

![詞元圖]({{site.url}}{{site.baseurl}}/images/nyc-token-graph.png){: width="700" }

## 在編製索引與查詢期間使用詞元圖

在編製索引時，`positionLength` 會被忽略，且不會使用詞元圖。

在執行查詢期間，多種查詢類型都可以運用詞元圖，其中最常用的如下：

- [`match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/)
- [`match_phrase`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)

## 範例：同義詞與同義詞圖的比較

若要進一步了解具備圖形感知能力的詞元篩選器與標準詞元篩選器之間的差異，您可以依照下列步驟比較 [`synonym`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym/) 詞元篩選器與 [`synonym_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym-graph/) 詞元篩選器：

1. 建立使用 [`synonym`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym/) 詞元篩選器（不具圖形感知能力）的索引：

    ```json
    PUT /synonym_index
    {
      "settings": {
        "analysis": {
          "filter": {
            "my_synonyms": {
              "type": "synonym",
              "synonyms": ["ssd => solid state drive"]
            }
          },
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": ["lowercase", "my_synonyms"]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "content": {
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

2. 建立使用 [`synonym_graph`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/synonym-graph/) 詞元篩選器（具圖形感知能力）的索引：

    ```json
    PUT /synonym_graph_index
    {
      "settings": {
        "analysis": {
          "filter": {
            "my_synonyms": {
              "type": "synonym_graph",
              "synonyms": ["ssd => solid state drive"]
            }
          },
          "analyzer": {
            "my_analyzer": {
              "tokenizer": "standard",
              "filter": ["lowercase", "my_synonyms"]
            }
          }
        }
      },
      "mappings": {
        "properties": {
          "content": {
            "type": "text",
            "analyzer": "my_analyzer"
          }
        }
      }
    }
    ```
    {% include copy-curl.html %}

3. 在每個索引中建立相同的文件：

    ```json
    PUT /synonym_index/_doc/1
    { "content": "ssd is critical" }
    ```
    {% include copy-curl.html %}
    
    ```json
    PUT /synonym_graph_index/_doc/1
    { "content": "ssd is critical" }
    ```
    {% include copy-curl.html %}

4. 搜尋不具圖形感知能力的索引：

    ```json
    POST /synonym_index/_search
    {
      "query": {
        "match_phrase": {
          "content": "solid state drive is critical"
        }
      }
    }
    ```
    {% include copy-curl.html %}
  
    回應中沒有任何命中結果：
    
    ```json
    {
      "took": 13,
      "timed_out": false,
      "_shards": {
        "total": 1,
        "successful": 1,
        "skipped": 0,
        "failed": 0
      },
      "hits": {
        "total": {
          "value": 0,
          "relation": "eq"
        },
        "max_score": null,
        "hits": []
      }
    }
    ```

5. 搜尋具圖形感知能力的索引：

    ```json
    POST /synonym_graph_index/_search
    {
      "query": {
        "match_phrase": {
          "content": "solid state drive is critical"
        }
      }
    }
    ```
    {% include copy-curl.html %}
    
    回應中包含一筆命中結果：
    
    ```json
    {
      "took": 9,
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
        "max_score": 1.4384103,
        "hits": [
          {
            "_index": "synonym_graph_index",
            "_id": "1",
            "_score": 1.4384103,
            "_source": {
              "content": "ssd is critical"
            }
          }
        ]
      }
    }
    ```

使用具圖形感知能力的詞元篩選器時會產生命中結果，這是因為在執行 [`match_phrase`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/) 查詢期間，會使用詞元圖產生額外的子查詢。下圖說明由具圖形感知能力的詞元篩選器所建立的詞元圖。

![詞元圖]({{site.url}}{{site.baseurl}}/images/ssd-token-graph.png){: width="700" }