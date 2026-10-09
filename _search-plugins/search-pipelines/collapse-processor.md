---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "摺疊"
nav_order: 10
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 摺疊處理器
於 2.12 版推出
{: .label .label-purple }

`collapse` 回應處理器會捨棄與結果集中先前文件在特定欄位具有相同值的命中結果。
這類似於在搜尋請求中傳遞 `collapse` 參數，但回應處理器是在從所有分片擷取後才套用至
回應。`collapse` 回應處理器可與 `rescore` 搜尋
請求參數搭配使用，也可在重新排序回應處理器之後套用。

使用 `collapse` 回應處理器時，傳回的結果可能會少於 `size` 筆，因為命中結果會被捨棄，
而該集合的大小已小於或等於 `size`。若要提高傳回 `size` 筆命中結果的可能性，請使用
`oversample` 請求處理器和 `truncate_hits` 回應處理器，如[此範例]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/truncate-hits-processor/#oversample-collapse-and-truncate-hits)所示。

## 請求本文欄位

下表列出所有請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`field` | 字串 | 將從每個傳回的搜尋命中結果讀取其值的欄位。搜尋回應中只會傳回每個指定欄位值的第一筆命中結果。必要。
`context_prefix` | 字串 | 可用來從特定範圍讀取 `original_size` 變數，以避免衝突。選用。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)並繼續執行搜尋管線中的其餘處理器。選用。預設為 `false`。

## 範例

以下範例示範使用含有 `collapse` 處理器的搜尋管線。

### 設定

建立許多包含要用於摺疊之欄位的文件：

```json
POST /_bulk
{ "create":{"_index":"my_index","_id":1}}
{ "title" : "document 1", "color":"blue" }
{ "create":{"_index":"my_index","_id":2}}
{ "title" : "document 2", "color":"blue" }
{ "create":{"_index":"my_index","_id":3}}
{ "title" : "document 3", "color":"red" }
{ "create":{"_index":"my_index","_id":4}}
{ "title" : "document 4", "color":"red" }
{ "create":{"_index":"my_index","_id":5}}
{ "title" : "document 5", "color":"yellow" }
{ "create":{"_index":"my_index","_id":6}}
{ "title" : "document 6", "color":"yellow" }
{ "create":{"_index":"my_index","_id":7}}
{ "title" : "document 7", "color":"orange" }
{ "create":{"_index":"my_index","_id":8}}
{ "title" : "document 8", "color":"orange" }
{ "create":{"_index":"my_index","_id":9}}
{ "title" : "document 9", "color":"green" }
{ "create":{"_index":"my_index","_id":10}}
{ "title" : "document 10", "color":"green" }
``` 
{% include copy-curl.html %}

建立僅在 `color` 欄位上摺疊的管線：

```json
PUT /_search/pipeline/collapse_pipeline
{
  "response_processors": [
    {
      "collapse" : {
        "field": "color"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

在此範例中，您請求前三份文件，然後在 `color` 欄位上摺疊。由於前兩份文件具有相同的 `color`，因此第二份文件會被捨棄，
而請求會傳回第一份和第三份文件：

```json
POST /my_index/_search?search_pipeline=collapse_pipeline
{
  "size": 3
}
```
{% include copy-curl.html %}


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
      "value" : 10,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "title" : "document 1",
          "color" : "blue"
        }
      },
      {
        "_index" : "my_index",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "title" : "document 3",
          "color" : "red"
        }
      }
    ]
  },
  "profile" : {
    "shards" : [ ]
  }
}
```
</details>
