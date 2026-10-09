---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Foreach
parent: Ingest processors
nav_order: 110
---

<!-- vale off -->
# Foreach 處理器
<!-- vale on -->

`foreach` 處理器用於迭代輸入文件中的值清單，並對每個值套用轉換。這對於以一致方式處理陣列中的所有元素等任務非常有用，例如將字串中的所有元素轉換為小寫或大寫。

以下是 `foreach` 處理器的語法：

```json
{
  "foreach": {
    "field": "<field_name>",
    "processor": {
      "<processor_type>": {
        "<processor_config>": "<processor_value>"
      }
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `foreach` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 要迭代的陣列欄位。
`processor` | 必要 | 要對每個欄位執行的處理器。
`ignore_missing` | 選用 | 若為 `true` 且指定的欄位不存在或為 null，則處理器會靜默結束，不會修改文件。
`description` | 選用 | 處理器的簡短描述。
`if` | 選用 | 執行處理器的條件。
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤也繼續執行。若設為 `true`，則會忽略失敗。預設值為 `false`。
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。

## 使用處理器

依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `test-foreach` 的管線，使用 `foreach` 處理器迭代 `protocols` 欄位中的每個元素：

```json
PUT _ingest/pipeline/test-foreach  
{  
  "description": "Lowercase all the elements in an array",  
  "processors": [  
    {  
      "foreach": {  
        "field": "protocols",  
        "processor": {  
          "lowercase": {  
            "field": "_ingest._value"  
          }  
        }  
      }  
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/test-foreach/_simulate  
{  
  "docs": [  
    {  
      "_index": "testindex1",  
      "_id": "1",  
      "_source": {  
        "protocols": ["HTTP","HTTPS","TCP","UDP"]  
      }  
    }  
  ]  
} 
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線如預期運作，顯示四個元素已轉換為小寫：

```json
{  
  "docs": [  
    {  
      "doc": {  
        "_index": "testindex1",  
        "_id": "1",  
        "_source": {  
          "protocols": [  
            "http",  
            "https",  
            "tcp",  
            "udp"  
          ]  
        },  
        "_ingest": {  
          "_value": null,  
          "timestamp": "2024-05-23T02:44:10.8201Z"  
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
POST testindex1/_doc/1?pipeline=test-foreach  
{  
  "protocols": ["HTTP","HTTPS","TCP","UDP"]  
}  
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引到索引 `testindex1`，並在編製索引之前套用管線：

```json
{  
  "_index": "testindex1",  
  "_id": "1",  
  "_version": 6,  
  "result": "created",  
  "_shards": {  
    "total": 2,  
    "successful": 1,  
    "failed": 0  
  },  
  "_seq_no": 5,  
  "_primary_term": 67  
}  
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

回應會顯示文件，其中包含從 `users` 欄位擷取的 JSON 資料：

```json
{  
  "_index": "testindex1",  
  "_id": "1",  
  "_version": 6,  
  "_seq_no": 5,  
  "_primary_term": 67,  
  "found": true,  
  "_source": {  
    "protocols": [  
      "http",  
      "https",  
      "tcp",  
      "udp"  
    ]  
  }  
}  

{  
  "docs": [  
    {  
      "doc": {  
        "_index": "testindex1",  
        "_id": "1",  
        "_source": {  
          "protocols": [  
            "http",  
            "https",  
            "tcp",  
            "udp"  
          ]  
        },  
        "_ingest": {  
          "_value": null,  
          "timestamp": "2024-05-23T02:44:10.8201Z"  
        }  
      }  
    }  
  ]  
}  
```
{% include copy-curl.html %}
