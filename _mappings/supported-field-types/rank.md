---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Rank 欄位類型"
nav_order: 25
has_children: false
parent: Specialized search field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/rank/
  - /opensearch/supported-field-types/rank/
  - /field-types/rank/
---

# Rank 欄位類型
**於 1.0 版推出**
{: .label .label-purple }

下表列出 OpenSearch 支援的所有 rank 欄位類型。

欄位資料類型 | 說明
:--- | :---  
[`rank_feature`](#rank-feature) | 提升或降低文件的相關性分數。 
[`rank_features`](#rank-features) | 提升或降低文件的相關性分數。適用於特徵清單稀疏的情況。 

Rank feature 與 rank features 欄位只能使用 [rank feature 查詢](#rank-feature-query)來查詢。它們不支援彙總或排序。
{: .note }

## Rank feature

Rank feature 欄位類型會使用正的 [float]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 值，在 `rank_feature` 查詢中提升或降低文件的相關性分數。根據預設，此值會提升相關性分數。若要降低相關性分數，請將選用的 `positive_score_impact` 參數設為 false。

### 範例

建立含有 rank feature 欄位的對應：

```json
PUT chessplayers
{
  "mappings": {
    "properties": {
      "name" : {
        "type" : "text"
      },
      "rating": {
        "type": "rank_feature" 
      },
      "age": {
        "type": "rank_feature",
        "positive_score_impact": false 
      }
    }
  }
}
```
{% include copy-curl.html %}

將三份文件編製索引，其中一個 rank_feature 欄位會提升分數 (`rating`)，另一個 rank_feature 欄位則會降低分數 (`age`)：

```json
PUT testindex1/_doc/1
{
  "name" : "John Doe",
  "rating" : 2554,
  "age" : 75
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "name" : "Kwaku Mensah",
  "rating" : 2067,
  "age": 10
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/3
{
  "name" : "Nikki Wolf",
  "rating" : 1864,
  "age" : 22
}
```
{% include copy-curl.html %}

## Rank feature 查詢

使用 rank feature 查詢，您可以依評分、依年齡，或同時依評分與年齡為玩家排名。若依評分為玩家排名，評分較高的玩家會有較高的相關性分數。若依年齡為玩家排名，較年輕的玩家會有較高的相關性分數。

使用 rank feature 查詢，依年齡與評分搜尋玩家：

```json
GET chessplayers/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "rank_feature": {
            "field": "rating"
          }
        },
        {
          "rank_feature": {
            "field": "age"
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

同時依年齡與評分排名時，較年輕的玩家以及排名較高的玩家分數較好：

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
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 1.2093145,
    "hits" : [
      {
        "_index" : "chessplayers",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.2093145,
        "_source" : {
          "name" : "Kwaku Mensah",
          "rating" : 1967,
          "age" : 10
        }
      },
      {
        "_index" : "chessplayers",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0150313,
        "_source" : {
          "name" : "Nikki Wolf",
          "rating" : 1864,
          "age" : 22
        }
      },
      {
        "_index" : "chessplayers",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.8098284,
        "_source" : {
          "name" : "John Doe",
          "rating" : 2554,
          "age" : 75
        }
      }
    ]
  }
}
```

## Rank features

Rank features 欄位類型與 rank feature 欄位類型類似，但更適合稀疏的特徵清單。Rank features 欄位可將數值特徵向量編製索引，之後用於在 `rank_feature` 查詢中提升或降低文件的相關性分數。 

### 範例

建立含有 rank features 欄位的對應：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "correlations": {
        "type": "rank_features" 
      }
    }
  }
}
```
{% include copy-curl.html %}

若要將含有 rank features 欄位的文件編製索引，請使用以字串為鍵、以正 float 值為值的 hashmap：

```json
PUT testindex1/_doc/1
{
  "correlations": { 
    "young kids" : 1,
    "older kids" : 15,
    "teens" : 25.9
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/2
{
  "correlations": {
    "teens": 10,
    "adults": 95.7
  }
}
```
{% include copy-curl.html %}

使用 rank feature 查詢來查詢文件：

```json
GET testindex1/_search
{
  "query": {
    "rank_feature": {
      "field": "correlations.teens"
    }
  }
}
```
{% include copy-curl.html %}

回應會依相關性分數排名：

```json
{
  "took" : 123,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.6258503,
    "hits" : [
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.6258503,
        "_source" : {
          "correlations" : {
            "young kids" : 1,
            "older kids" : 15,
            "teens" : 25.9
          }
        }
      },
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 0.39263803,
        "_source" : {
          "correlations" : {
            "teens" : 10,
            "adults" : 95.7
          }
        }
      }
    ]
  }
}
```

Rank feature 與 rank features 欄位使用最高的九個有效位元來計算精確度，導致約 0.4% 的相對誤差。值的儲存相對精確度為 2<sup>−8</sup> = 0.00390625。
{: .note }
