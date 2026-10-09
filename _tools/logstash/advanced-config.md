---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "進階組態"
parent: Logstash
nav_order: 230
redirect_from:
 - /clients/logstash/advanced-config/
---

# 進階組態

本節說明如何為 Logstash 設定進階組態選項，例如參照欄位值與條件陳述式。

## 參照欄位值

若要存取欄位，請使用 `- field` 語法。
您也可以用方括號 `- [field]` 包住欄位名稱，讓您參照欄位這件事更加明確。


例如，如果您有下列事件：

```bash
{
  "request": "/products/view/123",
  "verb": "GET",
  "response": 200,
  "headers": {
  "request_path" => "/"
  }
}
```

若要存取 `request` 欄位，請使用 `- request` 或 `- [request]`。

如果您想參照巢狀欄位，請使用方括號語法並指定欄位的路徑。每一層都包在方括號內：`- [headers][request_path]`。

您可以使用 `sprintf` 格式來參照欄位。這也稱為字串展開。您需要加上 % 符號，然後將欄位參照包在花括號內。

使用條件陳述式時，您需要參照欄位值。

例如，您可以讓檔案名稱變成動態，並包含已處理事件的類型 - 也就是 `access` 或 `error`。`type` 選項主要用於根據正在處理的事件類型，以條件方式套用篩選外掛程式。

讓我們新增一個 `type` 選項，並指定值為 `access`。


```yml
input {
  file {
    path => ""
  start_position => "beginning"
  type => "access"
  }
  http {
    type => "access"
  }
}

filter {
  mutate {
    remove_field => {"host"}
  }
}

output {
  stdout {
    codec => rubydebug
  }
file {
  path => "%{[type]}.log"
  }
}
```

啟動 Logstash 並傳送 HTTP 請求。已處理的事件會輸出到終端機。該事件現在包含一個名為 `type` 的欄位。

您會看到 Logstash 目錄中建立了 `access.log` 檔案。

## 條件陳述式

您可以使用條件陳述式，根據某些條件控制程式碼執行的流程。

語法：

```yml
if EXPR {
  ...
} else if EXPR {
  ...
} else {
  ...
}
```

`EXPR` 是任何可評估為布林值的有效 Logstash 語法。
例如，您可以檢查事件類型是否設為 `access` 或 `error`，並據此執行某些動作：

```yml
if [type] == "access" {
...
} else if [type] == "error" {
file { .. }
} else {
...
}
```

您可以將欄位值與某個任意值進行比較：

```yml
if [headers][content_length] >= 1000 {
...
}
```

您可以使用正規表達式：

```yml
if [some_field =~ /[0-9]+/ {
  //some field only contains digits
}
```

您可以使用陣列：

```yml
if [some_field] in ["one", "two", "three"] {
  some field is either "one", "two", or "three"
}
```

您可以使用布林運算子：

```yml
if [type] == "access" or [type] == "error" {
  ...
}
```


## 格式化日期

您可以使用 `sprintf` 格式或字串展開來格式化日期。
例如，您可能希望目前的日期成為檔案名稱的一部分。

若要格式化日期，請在花括號中加上加號，後面接著日期格式 - `%{+yyyy-MM-dd}`。

```yml
file {
  path => "%{[type]}_%{+yyyy_MM_dd}.log"
}
```

這是儲存在 @timestamp 欄位內的日期，也就是事件的時間與日期。
傳送請求至管線，並確認輸出的檔案名稱包含事件日期。

您也可以將日期嵌入其他輸出，例如嵌入 OpenSearch 中的索引名稱。

## 傳送時間資訊

您可以設定事件的時間。

Logstash 在輸入外掛程式收到事件時，已經將時間設定在 @timestamp 欄位內。
在某些情況下，您可能需要使用不同的時間戳記。
例如，如果您有一間電子商務商店，且您每天午夜處理訂單。當 Logstash 在午夜收到事件時，會將時間戳記設為目前時間。
但您希望時間是下單的時間，而不是 Logstash 收到事件的時間。

讓我們將事件時間戳記改為網頁伺服器收到請求的日期。您可以使用名為 `dates` 的篩選外掛程式來完成。
`dates` 篩選器會從欄位傳遞 `date` 或 `datetime` 值，並將結果用作事件時間戳記。

在 `filter` 區塊底部新增 `date` 外掛程式：

```yml
date {
  match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
}
```

timestamp 是 `grok` 模式建立的欄位。
`Z` 是時區 (UTC 位移)。

啟動 Logstash 並傳送 HTTP 請求。

您可以看到檔案名稱包含請求的日期，而不是目前的日期。

如果日期傳遞失敗，`filter` 外掛程式會將名為 `_datepassfailure` 的標籤新增至文字欄位。

將 @timestamp 欄位設為新值之後，您其實就不再需要另一個 `timestamp` 欄位了。您可以使用 `remove_field` 選項將其移除。

```yml
date {
  match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
  remove_field => [ "timestamp" ]
}
```

## 剖析使用者代理程式

使用者代理程式是記錄項目最後一部分，由瀏覽器名稱、瀏覽器版本及裝置的作業系統組成。

使用者可能使用各式各樣的瀏覽器、裝置及作業系統。手動處理這件事很困難。

您無法使用 `grok` 模式，因為 `grok` 模式只會比對字串整體的用法，例如無法判斷訪客使用的是哪個瀏覽器。

Logstash 隨附一個內含正規表達式的檔案來達成此目的。這讓擷取使用者代理程式資訊變得非常容易，您可以將這些資訊傳送至 OpenSearch 並執行彙總。

若要這麼做，請新增一個包含欄位名稱的 `source` 選項。在此情況下，就是 `agent` 欄位。
根據預設，使用者代理程式外掛程式會在事件的頂層新增多個欄位。
由於這可能會變得相當混亂，我們可以新增一個名為 `target` 的選項，其值為 `ua`，也就是 user agent 的縮寫。這麼做會將這些欄位巢狀置於名為 `ua` 的物件內，讓內容更有條理。

```yml
useragent {
  source => "agent"
  target => "ua"
}
```

啟動 Logstash 並傳送 HTTP 請求。

您可以看到一個名為 `ua` 的欄位，其中包含多個索引鍵，包括瀏覽器名稱與版本、作業系統及裝置。

您可以使用 OpenSearch Dashboards 建立圓餅圖，顯示有多少訪客使用行動裝置，以及有多少是桌上型電腦使用者。或者，您也可以取得哪些瀏覽器版本受歡迎的統計資料。

## 擴充地理資料

您可以使用 `geoip` 篩選器取得 IP 位址並執行地理查閱，以解析使用者的地理位置。

`geoip` 篩選外掛程式隨附一個名為 `geolite 2` 的資料庫，該資料庫由名為 MaxMind 的公司提供。`geolite 2` 是熱門的地理資料來源，且可免費取得。
在 `else` 區塊底部新增 `geoip` 外掛程式。

`source` 選項的值是包含 IP 位址的欄位名稱，在此情況下就是 `clientip`。您可以使用 `grok` 模式讓此欄位可供使用。

```yml
geoip {
  source => "clientip"
}
```

啟動 Logstash 並傳送 HTTP 請求。

在終端機中，您會看到一個名為 `geoip` 的新欄位，其中包含時區、國家、洲、城市、郵遞區號及經緯度配對等資訊。

例如，如果您只需要國家名稱，請加入一個名為 `fields` 的選項，其中包含您希望 `geoip` 外掛程式傳回的欄位名稱陣列。

有些欄位 (例如城市名稱與地區) 並非總是可用，因為將 IP 位址轉譯為地理位置通常不是那麼準確。如果 `geoip` 外掛程式查閱地理位置失敗，會新增一個名為 `geoip_lookup_failure` 的標籤。

您可以將 `geoip` 外掛程式與 OpenSearch 輸出搭配使用，因為 `geoip` 物件內的 `location` 物件，是在 JSON 中表示地理空間資料的標準格式。這與 OpenSearch 用於其 `geo_point` 資料類型的格式相同。

您可以使用 OpenSearch 強大的地理空間查詢來處理地理資料。
