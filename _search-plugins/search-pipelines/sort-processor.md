---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "排序"
nav_order: 130
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 排序搜尋處理器
於 2.16 版推出
{: .label .label-purple }

`sort` 處理器會以遞增或遞減順序排序項目陣列。數值陣列會以數值方式排序，而字串或混合陣列（字串與數字）則會以字典順序排序。若輸入不是陣列，處理器會擲回錯誤。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`field`  | 字串 | 要排序的欄位。必須是陣列。必要。
`order`  | 字串 | 要套用的排序順序。接受 `asc`（遞增）或 `desc`（遞減）。預設為 `asc`。
`target_field` | 字串 | 儲存已排序陣列的欄位名稱。若未指定，則已排序的陣列會儲存在與原始陣列相同的欄位中（`field` 變數）。 
`tag` | 字串 | 處理器的識別碼。 
`description` | 字串 | 處理器的描述。 
`ignore_failure` | 布林值 | 若為 `true`，則 OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中其餘的處理器。選用。預設為 `false`。

## 範例 

下列範例示範如何使用包含 `sort` 處理器的搜尋管線。

### 設定

建立名為 `my_index` 的索引，並將一份含有 `message` 欄位的文件編製索引；該欄位包含字串陣列：

```json
POST /my_index/_doc/1
{
  "message": ["one", "two", "three", "four"], 
  "visibility": "public"
}
```
{% include copy-curl.html %}

### 建立搜尋管線 

建立包含 `sort` 回應處理器的搜尋管線，該處理器會排序 `message` 欄位，並將排序後的結果儲存在 `sorted_message` 欄位中：

```json
PUT /_search/pipeline/my_pipeline
{
  "response_processors": [
    {
      "sort": {
        "field": "message",
        "target_field": "sorted_message"
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
  "took": 1,
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
          "message": [
            "one",
            "two",
            "three",
            "four"
          ],
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

`sorted_message` 欄位包含 `message` 欄位中依字母順序排序的字串：

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
          "visibility": "public",
          "sorted_message": [
            "four",
            "one",
            "three",
            "two"
          ],
          "message": [
            "one",
            "two",
            "three",
            "four"
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

在回應中，`message` 欄位會被排序，結果會儲存在 `sorted_message` 欄位中：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 2,
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
          "sorted_message": [
            "four",
            "one",
            "three",
            "two"
          ],
          "message": [
            "one",
            "two",
            "three",
            "four"
          ]
        },
        "fields": {
          "visibility": [
            "public"
          ],
          "sorted_message": [
            "four",
            "one",
            "three",
            "two"
          ],
          "message": [
            "one",
            "two",
            "three",
            "four"
          ]
        }
      }
    ]
  }
}
```
</details>