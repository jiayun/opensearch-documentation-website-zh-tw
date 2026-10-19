---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用者代理程式"
parent: Ingest processors
nav_order: 330
---

# 使用者代理程式處理器

`user_agent` 處理器用於從使用者代理程式字串中擷取資訊，例如用戶端使用的瀏覽器、裝置與作業系統。`user_agent` 處理器特別適合用來分析使用者行為，並根據使用者的裝置、作業系統與瀏覽器識別趨勢。它也有助於疑難排解特定使用者代理程式組態的問題。

以下是 `user_agent` 處理器的語法：

```json
{
  "user_agent": {
    "field": "user_agent",
    "target_field": "user_agent_info"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `user_agent` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 包含使用者代理字串的欄位。
`target_field` | 選用 | 用於儲存擷取之使用者代理資訊的欄位。若未指定，則資訊會儲存在 `user_agent` 欄位中。
`ignore_missing`  | 選用  | 指定處理器是否應忽略未包含所指定 `field` 的文件。若設為 `true`，則當 `field` 不存在或為 `null` 時，處理器不會修改該文件。預設值為 `false`。 |
`regex_file` | 選用 | 包含用於剖析使用者代理字串之規則表達式模式的檔案名稱，例如 `custom-regexes.yml`。該檔案必須位於 `config/ingest-user-agent` 目錄中。若未指定，則處理器會使用 OpenSearch 隨附的規則表達式。如需詳細資訊，請參閱[使用自訂 regex 檔案](#using-a-custom-regex-file)。
`properties` | 選用 | 要從使用者代理字串擷取並新增至 `target_field` 的屬性清單。有效值為 `name`、`version`、`os`、`device` 及 `original`。若未指定，則會擷取所有這些屬性。
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設值為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |

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

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/user_agent_pipeline/_simulate
{
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

前述請求會將 `user_agent` 字串剖析為各個組成部分，並將文件（包括剖析後的組成部分）編製索引至 `testindex1` 索引，如下列回應所示：

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

回應包含原始的 `user_agent` 欄位，以及解析後的 `user_agent_info` 欄位，其中含有裝置、作業系統與瀏覽器資訊：

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

## 使用自訂正規表示式檔案

若要使用您自己的正規表示式剖析使用者代理程式字串，請建立正規表示式檔案，並在 `regex_file` 參數中指定其名稱。檔案必須符合下列要求：

- 檔案的副檔名為 `.yml`。
- 檔案位於每個節點上的 `config/ingest-user-agent` 目錄中。
- 檔案在節點啟動時已存在。OpenSearch 僅在啟動時載入正規表示式檔案，因此對現有檔案的變更和新增的檔案，只有在您重新啟動節點後才會生效。

隨附的正規表示式以 uap-core 專案中的 [`regexes.yaml`](https://github.com/ua-parser/uap-core/blob/master/regexes.yaml) 檔案為基礎。自訂正規表示式檔案通常是此檔案的較新版本或修改版本。

## 設定

`user_agent` 處理器會快取解析結果。節點上的所有 `user_agent` 處理器共用一個快取。您可以在 `opensearch.yml` 中使用下列靜態設定來設定快取：

- `ingest.user_agent.cache_size` (Static, long)：可快取的解析結果數量上限。預設為 `1000`。
