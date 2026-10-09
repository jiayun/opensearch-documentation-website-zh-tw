---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分割"
nav_order: 140
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 分割搜尋處理器
於 2.17 版推出
{: .label .label-purple }

`split` 處理器會根據指定的分隔符號，將字串欄位分割成子字串陣列。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`field` | 字串 | 包含要分割之字串的欄位。必要。
`separator` | 字串 | 用來分割字串的分隔符號。請指定單一分隔字元或規則運算式模式。必要。
`preserve_trailing` | 布林值 | 若設為 `true`，則保留結果陣列中尾端的空欄位（例如 `''`）。若設為 `false`，則會從結果陣列中移除尾端的空欄位。預設為 `false`。 
`target_field` | 字串 | 儲存子字串陣列的欄位。若未指定，則會就地更新該欄位。 
`tag` | 字串 | 處理器的識別碼。 
`description` | 字串 | 處理器的說明。 
`ignore_failure` | 布林值 | 若為 `true`，則 OpenSearch [忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中的其餘處理器。選用。預設為 `false`。

## 範例 

下列範例示範如何使用含有 `split` 處理器的搜尋管線。

### 設定

建立名為 `my_index` 的索引，並將包含 `message` 欄位的文件編製索引：

```json
POST /my_index/_doc/1
{
  "message": "ingest, search, visualize, and analyze data",
  "visibility": "public"
}
```
{% include copy-curl.html %}

### 建立搜尋管線 

下列請求會建立含有 `split` 回應處理器的搜尋管線，該處理器會分割 `message` 欄位，並將結果儲存在 `split_message` 欄位中：

```json
PUT /_search/pipeline/my_pipeline
{
  "response_processors": [
    {
      "split": {
        "field": "message",
        "separator": ", ",
        "target_field": "split_message"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

在沒有搜尋管線的情況下搜尋 `my_index` 中的文件：

```json
GET /my_index/_search
```
{% include copy-curl.html %}

回應包含 `message` 欄位：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}
```json
{
  "took": 3,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "message": "ingest, search, visualize, and analyze data",
          "visibility": "public"
        }
      }
    ]
  }
}
```
</details>

若要使用管線搜尋，請在 `search_pipeline` 查詢參數中指定管線名稱：

```json
GET /my_index/_search?search_pipeline=my_pipeline
```
{% include copy-curl.html %}

`message` 欄位會遭到分割，並將結果儲存在 `split_message` 欄位中：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 6,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "visibility": "public",
          "message": "ingest, search, visualize, and analyze data",
          "split_message": [
            "ingest",
            "search",
            "visualize",
            "and analyze data"
          ]
        }
      }
    ]
  }
}
```
</details>

您也可以使用 `fields` 選項來搜尋文件中的特定欄位：

```json
POST /my_index/_search?pretty&search_pipeline=my_pipeline
{
    "fields": ["visibility", "message"]
}
``` 
{% include copy-curl.html %}

在回應中，`message` 欄位會遭到分割，並將結果儲存在 `split_message` 欄位中：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 7,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "my_index",
        "_id": "1",
        "_score": 1,
        "_source": {
          "visibility": "public",
          "message": "ingest, search, visualize, and analyze data",
          "split_message": [
            "ingest",
            "search",
            "visualize",
            "and analyze data"
          ]
        },
        "fields": {
          "visibility": [
            "public"
          ],
          "message": [
            "ingest, search, visualize, and analyze data"
          ],
          "split_message": [
            "ingest",
            "search",
            "visualize",
            "and analyze data"
          ]
        }
      }
    ]
  }
}
```
</details>