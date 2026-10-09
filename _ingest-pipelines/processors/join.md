---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Join
parent: Ingest processors
nav_order: 160
---

# Join 處理器

`join` 處理器會將陣列的元素串接成單一字串值，並在每個元素之間使用指定的分隔符。如果提供的輸入不是陣列，則會擲回例外。

以下是 `join` 處理器的語法：

```json
{
  "join": {
    "field": "field_name",
    "separator": "separator_string"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `join` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 要套用 join 運算子的欄位名稱。必須是陣列。
`separator` | 必要 | 串接欄位值時使用的字串分隔符。若未指定，則值會在沒有分隔符的情況下直接串接。
`target_field` | 選用 | 要指派清理後值的欄位。若未指定，則會就地更新該欄位。
`description` | 選用 | 處理器用途或組態的描述。
`if` | 選用 | 指定要有條件地執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器的失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理處理器的失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 選用 | 處理器的識別碼。對偵錯與指標很有用。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `example-join-pipeline` 的管線，使用 `join` 處理器串接 `uri` 欄位的所有值，並以指定的分隔符 `/` 分隔：

```json
PUT _ingest/pipeline/example-join-pipeline  
{  
  "description": "Example pipeline using the join processor",  
  "processors": [  
    {  
      "join": {  
        "field": "uri",  
        "separator": "/"  
      }  
    }  
  ]  
}  
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/example-join-pipeline/_simulate  
{  
  "docs": [  
    {  
      "_source": {  
        "uri": [  
          "app",  
          "home",  
          "overview"  
        ]  
      }  
    }  
  ]  
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線如預期運作：

```json
{  
  "docs": [  
    {  
      "doc": {  
        "_index": "_index",  
        "_id": "_id",  
        "_source": {  
          "uri": "app/home/overview"  
        },  
        "_ingest": {  
          "timestamp": "2024-05-24T02:16:01.00659117Z"  
        }  
      }  
    }  
  ]  
}  
```
{% include copy-curl.html %}

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
POST testindex1/_doc/1?pipeline=example-join-pipeline  
{  
  "uri": [  
    "app",  
    "home",  
    "overview"  
  ]  
} 
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
