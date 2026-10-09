---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Grok
parent: Ingest processors
nav_order: 120
---

# Grok 處理器

`grok` 處理器可用於透過模式比對來解析及結構化非結構化資料。您可以使用 `grok` 處理器，從記錄訊息、網頁伺服器存取記錄檔、應用程式記錄檔，以及其他遵循一致格式的記錄資料中擷取欄位。

本文件說明如何在 OpenSearch 資料匯入管線中使用 `grok` 處理器。如果您的使用情境涉及大型或複雜的資料集，請考慮使用 [Data Prepper `grok` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/grok/)，其執行於 OpenSearch 叢集上。
{: .note}

## Grok 基礎

`grok` 處理器使用一組預先定義的模式來比對輸入文字的各個部分。每個模式由名稱和規則運算式組成。例如，模式 `%{IP:ip_address}` 會比對 IP 位址，並將其指派給 `ip_address` 欄位。您可以合併多個模式來建立更複雜的運算式。例如，模式 `%{IP:client} %{WORD:method} %{URIPATHPARM:request} %{NUMBER:bytes %NUMBER:duration}` 會比對網頁伺服器存取記錄檔中的一行，並擷取用戶端 IP 位址、HTTP 方法、請求 URI、傳送的位元組數，以及請求的持續時間。

如需可用的預先定義模式清單，請參閱 [Grok 模式](https://github.com/opensearch-project/OpenSearch/blob/main/libs/grok/src/main/resources/patterns/grok-patterns)。
{: .tip}

`grok` 處理器建構於 [Oniguruma 規則運算式程式庫](https://github.com/kkos/oniguruma/blob/master/doc/RE) 之上，並支援該程式庫的所有模式。您可以使用 OpenSearch Dashboards Dev Tools 中內建的 [Grok Debugger]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/grok-debugger/) 來測試及偵錯您的 grok 運算式。

請注意，模式*不會錨定*。為了效能與可靠性，請在模式中包含行首錨點（`^`）。
{: .note}

## 語法

以下是 `grok` 處理器的基本語法：

```json
{
  "grok": {
    "field": "your_message",
    "patterns": ["your_patterns"]
  }
}
```
{% include copy.html %}

## 組態參數

若要設定 `grok` 處理器，您有多種選項可定義模式、比對特定索引鍵，以及控制處理器的行為。下表列出 `grok` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含待解析文字的欄位名稱。 |
`patterns`  | 必要  | 用於比對並擷取具名捕獲內容的 grok 運算式清單。傳回清單中第一個符合的運算式。 | 
`pattern_definitions`  | 選用  | 由模式名稱與模式元組組成的字典，用於定義目前處理器的自訂模式。如果模式名稱與現有名稱相符，則會覆寫既有定義。 |
`trace_match` | 選用 | 當此參數設為 `true` 時，處理器會在處理後的文件中新增名為 `_grok_match_index` 的欄位。此欄位包含 `patterns` 陣列中成功比對文件的模式索引值。這項資訊有助於偵錯，以及瞭解文件套用了哪個模式。預設為 `false`。 |
`capture_all_matches` | 選用 | 設為 `true` 時，會擷取重複 grok 模式的所有比對結果，而非僅擷取第一個比對結果。例如，指定文字 `192.168.1.1 10.0.0.1 172.16.0.1` 和模式 `%{IP:ipAddress} %{IP:ipAddress} %{IP:ipAddress}` 時，全部三個 IP 位址都會收集至 `ipAddress` 欄位中的陣列。僅適用於明確重複的模式，不適用於使用量詞的模式，例如 `(%{IP:ipAddress})+`。預設為 `false`。 |
`description` | 選用 | 處理器的簡短說明。 |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器是否在遇到錯誤時仍繼續執行。如果設為 `true`，則會忽略失敗。預設為 `false`。 |
`ignore_missing` | 選用 | 指定處理器是否應忽略不含指定欄位的文件。如果設為 `true`，則當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於在偵錯時區分相同類型的處理器。 |

## 建立管線

以下步驟將引導您使用 `grok` 處理器建立[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/index/)。

**步驟 1：建立管線**

以下查詢會建立名為 `log_line` 的管線。其會使用指定的模式，從文件的 `message` 欄位中擷取欄位。在此情況下，其會擷取 `clientip`、`timestamp` 及 `response_status` 欄位：

```json
PUT _ingest/pipeline/log_line
{
  "description": "Extract fields from a log line",
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["^%{IPORHOST:clientip} %{HTTPDATE:timestamp} %{NUMBER:response_status:int}"]
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2（選用）：測試管線。**

{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/alert-icon.png" class="inline-icon" alt="alert icon"/>{:/} **注意**<br>建議您在匯入文件之前先測試管線。
{: .note}

若要測試管線，請執行以下查詢：

```json
POST _ingest/pipeline/log_line/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "127.0.0.1 198.126.12 10/Oct/2000:13:55:36 -0700 200"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

以下回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "127.0.0.1 198.126.12 10/Oct/2000:13:55:36 -0700 200",
          "response_status": 200,
          "clientip": "198.126.12",
          "timestamp": "10/Oct/2000:13:55:36 -0700"
        },
        "_ingest": {
          "timestamp": "2023-09-13T21:41:52.064540505Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

以下查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=log_line
{
  "message": "127.0.0.1 198.126.12 10/Oct/2000:13:55:36 -0700 200"
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行以下查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

## 自訂模式

您可以使用預設模式，也可以使用 `patterns_definitions` 參數將自訂模式新增至管線。自訂 grok 模式可用於管線中，從不符合內建 grok 模式的記錄訊息中擷取結構化資料。這對於解析來自自訂應用程式的記錄訊息，或解析經過某種修改的記錄訊息很有用。自訂模式遵循簡單的結構：每個模式都有唯一的名稱，以及定義其比對行為的對應規則運算式。

以下範例說明如何在組態中包含自訂模式。在此範例中，問題編號為 3 到 4 位數，並會解析至 `issue_number` 欄位，而狀態則會解析至 `status` 欄位：

```json
PUT _ingest/pipeline/log_line
{
  "processors": [
    {
      "grok": {
        "field": "message",
        "patterns": ["^The issue number %{NUMBER:issue_number} is %{STATUS:status}"],
        "pattern_definitions" : {
          "NUMBER" : "\\d{3,4}",
          "STATUS" : "open|closed"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 追蹤符合的模式

若要追蹤哪些模式符合並填入欄位，您可以使用 `trace_match` 參數。以下範例說明如何在組態中包含此參數：

```json
PUT _ingest/pipeline/log_line  
{  
  "description": "Extract fields from a log line",  
  "processors": [  
    {  
      "grok": {  
        "field": "message",  
        "patterns": ["^%{HTTPDATE:timestamp} %{IPORHOST:clientip}", "%{IPORHOST:clientip} %{HTTPDATE:timestamp} %{NUMBER:response_status:int}"],
        "trace_match": true  
      }  
    }  
  ]  
}  
```
{% include copy-curl.html %}

當您模擬管線時，OpenSearch 會傳回包含 `grok_match_index` 的 `_ingest` 中繼資料，如下列輸出所示：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "127.0.0.1 198.126.12 10/Oct/2000:13:55:36 -0700 200",
          "response_status": 200,
          "clientip": "198.126.12",
          "timestamp": "10/Oct/2000:13:55:36 -0700"
        },
        "_ingest": {
          "_grok_match_index": "1",
          "timestamp": "2023-11-02T18:48:40.455619084Z"
        }
      }
    }
  ]
}
```

