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
`name` | 必要	| 要執行的管線名稱。支援[範本片段](#selecting-a-pipeline-dynamically)。
`description` | 選用 | 處理器用途或組態的描述。
`if` | 選用 | 指定是否依條件執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 選用 | 處理器的識別碼。適用於除錯與指標。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `general-pipeline` 的一般管線，然後建立名為 `outer-pipeline` 的新管線，該管線會參照 `general-pipeline`：

```json
PUT _ingest/pipeline/general-pipeline  
{  
  "description": "a general pipeline",  
  "processors": [  
    {  
      "uppercase": {  
        "field": "protocol"  
      }  
    },  
    {  
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

以下範例回應確認管線如預期運作：

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

此請求會將文件編製索引至 `testindex1` 索引，並將 `protocol` 欄位轉為大寫、移除 `name` 欄位，如下列回應所示：

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

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

回應顯示的文件中，`protocol` 欄位已轉換為大寫，且 `name` 欄位已移除：

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


## 動態選取管線

`name` 參數支援範本片段，因此您可以根據文件中的欄位值來選取要執行的管線。下列請求會建立一個剖析 NGINX 記錄檔的管線：

```json
PUT _ingest/pipeline/logs-nginx
{
  "processors": [
    {
      "set": {
        "field": "parsed_by",
        "value": "{% raw %}{{_ingest.pipeline}}{% endraw %}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

下列請求會建立一個管線，該管線會執行名稱由 `logs-` 加上文件 `service` 欄位值組成的管線：

```json
PUT _ingest/pipeline/logs-router
{
  "processors": [
    {
      "set": {
        "field": "routed_by",
        "value": "{% raw %}{{_ingest.pipeline}}{% endraw %}"
      }
    },
    {
      "pipeline": {
        "name": "logs-{% raw %}{{service}}{% endraw %}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

將 `service` 欄位為 `nginx` 的文件編製索引：

```json
PUT logs/_doc/1?pipeline=logs-router
{
  "service": "nginx",
  "message": "GET /index.html 200"
}
```
{% include copy-curl.html %}

擷取該文件：

```json
GET logs/_doc/1
```
{% include copy-curl.html %}

回應顯示 `logs-router` 管線執行了 `logs-nginx` 管線：

```json
{
  "_index": "logs",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "parsed_by": "logs-nginx",
    "service": "nginx",
    "message": "GET /index.html 200",
    "routed_by": "logs-router"
  }
}
```

如果解析後的管線不存在，或執行該管線會造成循環（即管線執行自身），則 `pipeline` 處理器會失敗。

## 存取目前的管線名稱

`_ingest.pipeline` 匯入中繼資料欄位包含目前執行中之管線的 ID。在前述範例中，`routed_by` 欄位包含 `logs-router`，而 `parsed_by` 欄位包含 `logs-nginx`，因為每個 `set` 處理器都在不同的管線中執行。內部管線完成後，`_ingest.pipeline` 會再次包含外部管線的 ID。
