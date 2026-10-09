---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Percolator
nav_order: 35
has_children: false
parent: Specialized search field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/percolator/
  - /opensearch/supported-field-types/percolator/
  - /field-types/percolator/
---

# Percolator 欄位類型
**於 1.0 版推出**
{: .label .label-purple }

`percolator` 欄位類型指定將此欄位視為查詢。任何 JSON 物件欄位都可以標記為 `percolator` 欄位。一般而言，文件會被編製索引，並對其執行搜尋。當您使用 `percolator` 欄位時，您儲存的是一項搜尋，而 `percolate` 查詢之後會將文件與該搜尋比對。如需詳細範例，請參閱 [Percolate 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/percolate/)。

## 範例

某位客戶正在搜尋價格為 $400 或以下的桌子，並想為此搜尋建立警示。

建立對應，將 percolator 欄位類型指派給 query 欄位：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "search": {
        "properties": {
          "query": { 
            "type": "percolator" 
          }
        }
      },
      "price": { 
        "type": "float" 
      },
      "item": { 
        "type": "text" 
      }
    }
  }
}
```
{% include copy-curl.html %}

將查詢編製索引：

```json
PUT testindex1/_doc/1
{
  "search": {
    "query": {
      "bool": {
        "filter": [
          { 
            "match": { 
              "item": { 
                "query": "table" 
              }
            }
          },
          { 
            "range": { 
              "price": { 
                "lte": 400.00 
              } 
            } 
          }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

查詢中參照的欄位必須已存在於對應中。
{: .note }

執行 percolate 查詢以搜尋相符的文件：

```json
GET testindex1/_search
{
  "query" : {
    "bool" : {
      "filter" : 
        {
          "percolate" : {
            "field" : "search.query",
            "document" : {
              "item" : "Mahogany table",
              "price": 399.99
            }
          }
        }
    }
  }
}
```
{% include copy-curl.html %}

回應包含最初編製索引的查詢：

```json
{
  "took" : 30,
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
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "search" : {
            "query" : {
              "bool" : {
                "filter" : [
                  {
                    "match" : {
                      "item" : {
                        "query" : "table"
                      }
                    }
                  },
                  {
                    "range" : {
                      "price" : {
                        "lte" : 400.0
                      }
                    }
                  }
                ]
              }
            }
          }
        },
        "fields" : {
          "_percolator_document_slot" : [
            0
          ]
        }
      }
    ]
  }
}
```