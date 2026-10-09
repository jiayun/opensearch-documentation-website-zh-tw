---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新命名欄位"
nav_order: 100
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 重新命名欄位處理器
於 2.8 版推出
{: .label .label-purple }

`rename_field` 搜尋回應處理器會攔截搜尋回應並重新命名指定的欄位。當您的索引與應用程式對同一欄位使用不同名稱時，這非常有用。例如，如果您在索引中重新命名某個欄位，`rename_field` 處理器可以在將回應傳送至您的應用程式之前，把新名稱改回舊名稱。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`field` | 字串 | 要重新命名的欄位。必要。
`target_field` | 字串 | 新的欄位名稱。必要。
`tag` | 字串 | 處理器的識別碼。
`description` | 字串 | 處理器的描述。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中其餘的處理器。選用。預設為 `false`。

## 範例

下列範例示範如何使用含有 `rename_field` 處理器的搜尋管線。

### 設定

建立一個名為 `my_index` 的索引，並為含有欄位 `message` 的文件編製索引：

```json
POST /my_index/_doc/1
{
  "message": "This is a public message", 
  "visibility":"public"
}
```
{% include copy-curl.html %}

### 建立搜尋管線

下列請求會建立一個搜尋管線，其中包含一個將欄位 `message` 重新命名為 `notification` 的 `rename_field` 回應處理器：

```json
PUT /_search/pipeline/my_pipeline
{
  "response_processors": [
    {
      "rename_field": {
        "field": "message",
        "target_field": "notification"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

在不使用搜尋管線的情況下搜尋 `my_index` 中的文件：

```json
GET /my_index/_search
```
{% include copy-curl.html %}

回應包含欄位 `message`：

<details open markdown="block">
<summary>
    回應
</summary>
{: .text-delta}
```json
{
  "took" : 1,
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
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "message" : "This is a public message",
          "visibility" : "public"
        }
      }
    ]
  }
}
```
</details>

若要使用管線進行搜尋，請在 `search_pipeline` 查詢參數中指定管線名稱：

```json
GET /my_index/_search?search_pipeline=my_pipeline
```
{% include copy-curl.html %}

欄位 `message` 已重新命名為 `notification`：

<details open markdown="block">
<summary>
    回應
</summary>
{: .text-delta}
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
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "visibility" : "public",
          "notification" : "This is a public message"
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
    "fields":["visibility", "message"]
}
``` 
{% include copy-curl.html %}

在回應中，欄位 `message` 已重新命名為 `notification`：

<details open markdown="block">
<summary>
    回應
</summary>
{: .text-delta}
```json
{
  "took" : 4,
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
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "visibility" : "public",
          "notification" : "This is a public message"
        },
        "fields" : {
          "visibility" : [
            "public"
          ],
          "notification" : [
            "This is a public message"
          ]
        }
      }
    ]
  }
}

```
</details>