---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Grok
parent: Ingest processors
nav_order: 120
---

# Grok 處理器 

`grok` 處理器用於透過模式比對來解析並結構化非結構化資料。您可以使用 `grok` 處理器從記錄訊息、網頁伺服器存取記錄、應用程式記錄以及其他遵循一致格式的記錄資料中擷取欄位。

本文件說明如何在 OpenSearch 資料匯入管線中使用 `grok` 處理器。如果您的使用案例涉及大型或複雜的資料集，建議考慮使用在 OpenSearch 叢集之外執行的 [Data Prepper `grok` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/grok/)。
{: .note}

## Grok 基礎

`grok` 處理器使用一組預先定義的模式來比對輸入文字的部分內容。每個模式由名稱與規則運算式組成。例如，模式 `%{IP:ip_address}` 會比對 IP 位址並將其指派給欄位 `ip_address`。您可以組合多個模式來建立更複雜的運算式。例如，模式 `%{IP:client} %{WORD:method} %{URIPATHPARAM:request} %{NUMBER:bytes} %{NUMBER:duration}` 會比對 Web 伺服器存取記錄中的一行，並擷取用戶端 IP 位址、HTTP 方法、請求 URI、傳送的位元組數以及請求的持續時間。

如需可用的預先定義模式清單，請參閱 [Grok 模式](https://github.com/opensearch-project/OpenSearch/blob/main/libs/grok/src/main/resources/patterns/grok-patterns)。
{: .tip}

`grok` 處理器建構於 [Oniguruma 規則運算式程式庫](https://github.com/kkos/oniguruma/blob/master/doc/RE) 之上，並支援該程式庫的所有模式。您可以在 OpenSearch Dashboards Dev Tools 中使用內建的 [Grok Debugger]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/grok-debugger/) 來測試及偵錯您的 grok 運算式。

模式參照採用下列其中一種形式：

- `%{PATTERN_NAME}`：比對文字，但不會將其儲存到欄位中。
- `%{PATTERN_NAME:field_name}`：將比對到的文字以字串形式儲存在 `field_name` 中。
- `%{PATTERN_NAME:field_name:type}`：將比對到的文字儲存在 `field_name` 中，並轉換為 `type`。有效的類型為 `int`、`long`、`float`、`double` 和 `boolean`。

例如，給定文字 `3 items 0.25 2048`，模式 `%{NUMBER} items %{NUMBER:response_time:float} %{NUMBER:body_size:long}` 會略過項目計數，將 `response_time` 儲存為 float，並將 `body_size` 儲存為 long。

請注意，模式*不會錨定*。為了效能與可靠性，請在模式中加入行首錨點（`^`）。
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

若要設定 `grok` 處理器，您有多種選項可定義模式、比對特定鍵，並控制處理器的行為。下表列出 `grok` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含待剖析文字之欄位的名稱。 |
`patterns`  | 必要  | 用於比對並擷取具名擷取項的 grok 運算式清單。系統會傳回清單中第一個相符的運算式。 | 
`pattern_definitions`  | 選用  | 模式名稱與模式元組的字典，用於為目前處理器定義自訂模式。若模式與現有名稱相符，則會覆寫既有的定義。 |
`trace_match` | 選用 | 當此參數設為 `true` 時，處理器會將 `_grok_match_index` 欄位加入已處理文件的匯入中繼資料（`_ingest._grok_match_index`）。此欄位包含 `patterns` 陣列中成功比對該文件之模式的索引。此資訊有助於偵錯，並了解套用至文件的是哪個模式。預設值為 `false`。 |
`capture_all_matches` | 選用 | 設為 `true` 時，會擷取重複 grok 模式的所有相符項，而不只是第一個相符項。例如，給定文字 `192.168.1.1 10.0.0.1 172.16.0.1` 與模式 `%{IP:ipAddress} %{IP:ipAddress} %{IP:ipAddress}`，三個 IP 位址都會收集到 `ipAddress` 欄位中的陣列。僅適用於明確重複的模式，不適用於 `(%{IP:ipAddress})+` 這類量化的模式。預設值為 `false`。 |
`description` | 選用 | 處理器的簡短說明。 |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設值為 `false`。 |
`ignore_missing` | 選用 | 指定處理器是否應忽略不含指定欄位的文件。若設為 `true`，則當欄位不存在或為 `null` 時，處理器不會修改文件。預設值為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於偵錯，以區分相同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |

## 建立管線

下列步驟將引導您使用 `grok` 處理器建立[資料匯入管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/index/)。

**步驟 1：建立管線**

下列查詢會建立一個名為 `log_line` 的管線。它使用指定的模式從文件的 `message` 欄位中擷取欄位。在此範例中，它會擷取 `clientip`、`timestamp` 和 `response_status` 欄位：

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

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/log_line/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "198.51.100.12 10/Oct/2000:13:55:36 -0700 200"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "198.51.100.12 10/Oct/2000:13:55:36 -0700 200",
          "response_status": 200,
          "clientip": "198.51.100.12",
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

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=log_line
{
  "message": "198.51.100.12 10/Oct/2000:13:55:36 -0700 200"
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

## 自訂模式

您可以使用預設模式，或使用 `pattern_definitions` 參數將自訂模式新增至管線。自訂 grok 模式可用於管線中，從不符合內建 grok 模式的記錄檔訊息擷取結構化資料。這對於剖析來自自訂應用程式的記錄檔訊息，或剖析經過某種修改的記錄檔訊息很有用。自訂模式遵循簡單的結構：每個模式都有唯一的名稱，以及定義其比對行為的對應規則運算式。

以下範例說明如何在組態中包含自訂模式。在此範例中，問題編號為 3 到 4 位數，並剖析至 `issue_number` 欄位，而狀態則剖析至 `status` 欄位：

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

## 擷取內建模式

若要檢視可在 grok 運算式中參照的內建模式，請使用下列請求：

```json
GET _ingest/processor/grok
```
{% include copy-curl.html %}

回應包含一個 `patterns` 物件，將每個模式名稱對應到其正規表示式。以下是經過截斷的範例回應：

```json
{
  "patterns": {
    "IP": "(?:%{IPV6}|%{IPV4})",
    ...
  }
}
```

若要依名稱以字母順序排序模式，請將 `s` 查詢參數設為 `true`：

```json
GET _ingest/processor/grok?s=true
```
{% include copy-curl.html %}

## Grok 看門狗設定

為了保護節點免於執行時間異常過長的運算式，OpenSearch 會使用看門狗執行緒監視每次 grok 評估。若評估執行時間超過允許的時間，看門狗會將其停止，且 `grok` 處理器會傳回錯誤。您可以在 `opensearch.yml` 中使用下列靜態設定來設定看門狗：

- `ingest.grok.watchdog.interval`（靜態，時間單位）：看門狗執行之間的間隔。每次執行時，看門狗會停止任何已超過 `ingest.grok.watchdog.max_execution_time` 的評估。預設值為 `1s`。

- `ingest.grok.watchdog.max_execution_time`（靜態，時間單位）：grok 運算式評估在被中斷前可執行的最長時間。預設值為 `1s`。

## 記錄 grok 處理

當 OpenSearch 編譯處理器中的 grok 運算式時（這會在建立或載入管線時，或將管線定義傳遞給 Simulate Pipeline API 時發生），規則運算式編譯器可能會回報與這些運算式相關的警告。OpenSearch 會以 `DEBUG` 層級記錄這些警告。若要將這些警告納入 OpenSearch 記錄檔，請提高該處理器的記錄層級：

```json
PUT _cluster/settings
{
  "persistent": {
    "logger.org.opensearch.ingest.common.GrokProcessor": "DEBUG"
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱[記錄檔]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/logs/)。

## 追蹤符合的樣式

若要追蹤哪些樣式符合並填入欄位，您可以使用 `trace_match` 參數。以下範例說明如何將此參數納入您的組態：

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

當您模擬管線時，OpenSearch 會傳回包含 `_grok_match_index` 的 `_ingest` 中繼資料，如下列輸出所示。索引從零開始，因此值為 `1` 表示第二個樣式符合。由於 `_grok_match_index` 是匯入中繼資料，因此不會編製索引：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "198.51.100.12 10/Oct/2000:13:55:36 -0700 200",
          "response_status": 200,
          "clientip": "198.51.100.12",
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

