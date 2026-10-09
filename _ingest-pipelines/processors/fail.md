---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Fail
parent: Ingest processors
nav_order: 100
---

# Fail 處理器

`fail` 處理器適合在編製索引的過程中執行資料轉換與擴充。`fail` 處理器的主要用途是在符合特定條件時讓編製索引作業失敗。

以下是 `fail` 處理器的語法：

```json
"fail": { 
  "if": "ctx.foo == 'bar'", 
  "message": "Custom error message" 
  }
```
{% include copy.html %}

## 組態參數

下表列出 `fail` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`message` | 必要 | 要包含在失敗回應中的自訂錯誤訊息。
`description`  | 選用  | 處理器的簡短說明。  |  
`if` | 選用 | 執行處理器的條件。 |  
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |  
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |  
`tag` | 選用 | 處理器的識別碼標籤。用於偵錯，以區分相同類型的處理器。 |  

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `fail-log-pipeline` 的管線，該管線使用 `fail` 處理器來刻意讓記錄事件的管線執行失敗：

```json
PUT _ingest/pipeline/fail-log-pipeline  
{  
  "description": "A pipeline to test the fail processor for log events",  
  "processors": [  
    {  
      "fail": {  
        "if": "ctx.user_info.contains('password') || ctx.user_info.contains('credit card')",  
        "message": "Document containing personally identifiable information (PII) cannot be indexed!"  
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
POST _ingest/pipeline/fail-log-pipeline/_simulate  
{  
  "docs": [  
    {  
      "_source": {  
        "user_info": "Sensitive information including credit card"  
      }  
    }  
  ]  
}  
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "error": {
        "root_cause": [
          {
            "type": "fail_processor_exception",
            "reason": "Document containing personally identifiable information (PII) cannot be indexed!"
          }
        ],
        "type": "fail_processor_exception",
        "reason": "Document containing personally identifiable information (PII) cannot be indexed!"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=fail-log-pipeline  
{  
  "user_info": "Sensitive information including credit card"  
} 
```
{% include copy-curl.html %}

#### 回應

由於 `user_info` 中出現字串 `credit card`，請求無法將記錄事件編製索引至索引 `testindex1`。下列回應包含在 fail 處理器中指定的自訂錯誤訊息：

```json

  "error": {
    "root_cause": [
      {
        "type": "fail_processor_exception",
        "reason": "Document containing personally identifiable information (PII) cannot be indexed!"
      }
    ],
    "type": "fail_processor_exception",
    "reason": "Document containing personally identifiable information (PII) cannot be indexed!"
  },
  "status": 500
}
```
{% include copy-curl.html %}

### 步驟 4 (選用)：擷取文件

由於管線失敗，記錄事件未被編製索引，因此嘗試擷取它會導致找不到文件的錯誤 `"found": false`：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 文件錯誤範例

```json
{  
  "_index": "testindex1",  
  "_id": "1",  
  "found": false  
}  
```
