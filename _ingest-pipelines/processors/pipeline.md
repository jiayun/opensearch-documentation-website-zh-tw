---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管線"
parent: Ingest processors
nav_order: 220
---

# 管線處理器

`pipeline` 處理器可讓管線參考並包含另一個預先定義的管線。當您有一組需要在多個管線之間共用的常用處理器時，這會很有用。您不需要在每個管線中重新定義那些常用處理器，而是可以建立一個包含共用處理器的獨立基礎管線，然後使用管線處理器從其他管線參考該基礎管線。

以下是 `pipeline` 處理器的語法：

```json
{
  "pipeline": {
    "name": "general-pipeline"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `pipeline` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`name` | 必要	| 要執行之管線的名稱。
`description` | 選用 | 處理器用途或組態的說明。
`if` | 選用 | 指定以條件方式執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 選用 | 處理器的識別碼。適用於偵錯與指標。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `general-pipeline` 的一般管線，然後建立名為 `outer-pipeline` 的新管線，其會參考 `general-pipeline`：

```json
PUT _ingest/pipeline/general_pipeline  
{  
  "description": "a general pipeline",  
  "processors": [  
    {  
      "uppercase": {  
        "field": "protocol"  
      },  
      "remove": {  
        "field": "name"  
      }  
    }  
  ]  
}
```
{% include copy-curl.html %}

```json
PUT _ingest/pipeline/outer-pipeline  
{  
  "description": "an outer pipeline referencing the general pipeline",  
  "processors": [  
    {  
      "pipeline": {  
        "name": "general-pipeline"  
      }  
    }  
  ]  
}
```
{% include copy-curl.html %}

### 步驟 2 (選用)：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/outer-pipeline/_simulate
{  
  "docs": [  
    {  
      "_source": {  
        "protocol": "https",  
        "name":"test"  
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
          "protocol": "HTTPS"  
        },  
        "_ingest": {  
          "timestamp": "2024-05-24T02:43:43.700735801Z"  
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
POST testindex1/_doc/1?pipeline=outer-pipeline  
{  
  "protocol": "https",  
  "name": "test"  
}  
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引，將 `protocol` 欄位的值轉換為大寫，並從 `testindex1` 索引中的文件移除 name 欄位，如下列回應所示：

```json
{  
  "_index": "testindex1",  
  "_id": "1",  
  "_version": 2,  
  "result": "created",  
  "_shards": {  
    "total": 2,  
    "successful": 2,  
    "failed": 0  
  },  
  "_seq_no": 1,  
  "_primary_term": 1  
}  
```
{% include copy-curl.html %}

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

回應顯示文件中的 `protocol` 欄位值已轉換為大寫，且 name 欄位已移除：

```json
{  
  "_index": "testindex1",  
  "_id": "1",  
  "_version": 2,  
  "_seq_no": 1,  
  "_primary_term": 1,  
  "found": true,  
  "_source": {  
    "protocol": "HTTPS"  
  }  
}  
```

