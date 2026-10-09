---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用者代理程式"
parent: Ingest processors
nav_order: 330
---

# 使用者代理程式處理器

`user_agent` 處理器用於從使用者代理程式字串中擷取資訊，例如用戶端所使用的瀏覽器、裝置和作業系統。`user_agent` 處理器特別適合用來分析使用者行為，以及根據使用者裝置、作業系統和瀏覽器找出趨勢。它也有助於針對特定使用者代理程式組態的問題進行疑難排解。

以下是 `user_agent` 處理器的語法：

```json
{
  "processor": {
    "user_agent": {
      "field": "user_agent",
      "target_field": "user_agent_info"
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `user_agent` 處理器的必要和選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 包含使用者代理程式字串的欄位。
`target_field` | 選用 | 用來儲存所擷取使用者代理程式資訊的欄位。若未指定，則資訊會儲存在 `user_agent` 欄位中。
`ignore_missing`  | 選用  | 指定處理器是否應忽略未包含所指定 `field` 的文件。若設為 `true`，則當 `field` 不存在時，處理器不會修改文件。預設為 `false`。 |
`regex_file` | 選用 | 包含用來剖析使用者代理程式字串之規則表達式模式的檔案。此檔案應位於 OpenSearch 套件內的 `config/ingest-user-agent` 目錄中。若未指定，則會使用預設檔案 `regexes.yaml`。
`properties` | 選用 | 要從使用者代理程式字串中擷取並新增至 `target_field` 的屬性清單。若未指定，則預設屬性為 `name`、`major`、`minor`、`patch`、`build`、`os`、`os_name`、`os_major`、`os_minor` 和 `device`。
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `user_agent_pipeline` 的管線，其使用 `user_agent` 處理器來擷取使用者代理程式資訊： 

```json
PUT _ingest/pipeline/user_agent_pipeline
{
  "description": "User agent pipeline",
  "processors": [
    {
      "user_agent": {
        "field": "user_agent",
        "target_field": "user_agent_info"
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
POST _ingest/pipeline/user_agent_pipeline/_simulate
{
  "pipeline": "user_agent_pipeline",
  "docs": [
    {
      "_source": {
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應可確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
          "user_agent_info": {
            "name": "Chrome",
            "original": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "os": {
              "name": "Windows",
              "version": "10",
              "full": "Windows 10"
            },
            "device": {
              "name": "Other"
            },
            "version": "58.0.3029.110"
          }
        },
        "_ingest": {
          "timestamp": "2024-04-25T21:41:28.744407425Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件 

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=user_agent_pipeline
{
  "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
}
```
{% include copy-curl.html %}

#### 回應

上述請求會將 `user_agent` 字串剖析為其組成部分，並將該文件以及所有包含這些組成部分的文件編製索引至 `testindex1` 索引，如下列回應所示：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 66,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 65,
  "_primary_term": 47
}
```

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

回應包含原始 `user_agent` 欄位，以及剖析後的 `user_agent_info` 欄位，其中包含裝置、作業系統和瀏覽器資訊： 

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 66,
  "_seq_no": 65,
  "_primary_term": 47,
  "found": true,
  "_source": {
    "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "user_agent_info": {
      "original": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
      "os": {
        "name": "Mac OS X",
        "version": "10.15.7",
        "full": "Mac OS X 10.15.7"
      },
      "name": "Chrome",
      "device": {
        "name": "Mac"
      },
      "version": "90.0.4430.212"
    }
  }
}
```
