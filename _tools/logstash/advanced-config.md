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

管線組態可以參照每個事件的欄位。使用欄位參照與字串展開，從事件資料建構值，並使用條件陳述式依據事件內容以不同方式處理事件。諸如 `date`、`useragent` 與 `geoip` 等篩選外掛程式會設定事件時間戳記，並為事件新增瀏覽器與位置資訊。

## 參照欄位值

若要參照欄位，請將欄位名稱放在方括號中，例如 `[request]`。若要參照巢狀欄位，請指定欄位的路徑，並將每一層都放在方括號中。

例如，請參考下列事件：

```json
{
  "request": "/products/view/123",
  "verb": "GET",
  "response": 200,
  "http": {
    "method": "PUT"
  }
}
```

若要參照 `request` 欄位，請使用 `[request]`。若要參照巢狀的 `method` 欄位，請使用 `[http][method]`。

若要將欄位值插入字串中，請使用 `sprintf` 格式，此格式也稱為_字串展開 (string expansion)_：加上百分比符號（`%`），並將欄位參照放在大括號中，例如 `%{[request]}`。

`type` 選項通常用於根據所處理事件的類型，有條件地套用篩選器外掛程式。例如，下列管線會在每個事件中加入名為 `type`、值為 `access` 的欄位。`file` 輸出使用字串展開，以 `type` 欄位的值來命名輸出檔案：

```ruby
input {
  http {
    host => "127.0.0.1"
    port => 8080
    type => "access"
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
{% include copy.html %}

啟動 Logstash，並將 HTTP 請求傳送至連接埠 8080。Logstash 會將包含 `type` 欄位的事件輸出至終端機，並將其寫入 Logstash 目錄中的 `access.log` 檔案。

## 條件陳述式

使用條件陳述式，將 filter 或 output 外掛程式僅套用至符合條件的事件。條件陳述式的語法如下：

```ruby
if <expression> {
  ...
} else if <expression> {
  ...
} else {
  ...
}
```

每個 `<expression>` 都必須評估為布林值。例如，下列陳述式會根據 `type` 欄位的值，將事件寫入不同的檔案：

```ruby
output {
  if [type] == "access" {
    file { path => "access.log" }
  } else if [type] == "error" {
    file { path => "error.log" }
  } else {
    stdout { }
  }
}
```
{% include copy.html %}

若要比較欄位值與數字，請使用比較運算子。如果事件不包含該欄位，比較會失敗，Logstash 會捨棄該事件。若要保留這些事件，請先檢查欄位是否存在：

```ruby
if [amount] and [amount] >= 1000 {
  ...
}
```

若要檢查欄位值是否符合規則運算式，請使用 `=~` 運算子：

```ruby
if [some_field] =~ /^[0-9]+$/ {
  # some_field contains only digits
}
```

若要檢查欄位值是否存在於陣列中，請使用 `in` 運算子：

```ruby
if [some_field] in ["one", "two", "three"] {
  # some_field is "one", "two", or "three"
}
```

若要合併多個條件，請使用 `and`、`or` 與 `not` 布林運算子：

```ruby
if [type] == "access" or [type] == "error" {
  ...
}
```

## 格式化日期

若要將事件日期插入字串中，請使用字串展開，並在加號後接上日期格式，例如 `%{+yyyy-MM-dd}`。Logstash 會格式化儲存在事件 `@timestamp` 欄位中的日期。

例如，下列 `file` 輸出會在檔案名稱中包含事件日期：

```ruby
file {
  path => "%{[type]}_%{+yyyy_MM_dd}.log"
}
```
{% include copy.html %}

您可以在其他輸出中使用相同的模式，例如在 OpenSearch 索引的名稱中。

## 設定事件時間戳記

當輸入外掛程式收到事件時，Logstash 會將事件的 `@timestamp` 欄位設為目前時間。在某些情況下，您需要不同的時間戳記。例如，如果您在午夜處理前一天的訂單，您可能希望每個事件的時間戳記是下訂單的時間，而不是 Logstash 收到該事件的時間。

若要使用事件中的欄位來設定事件時間戳記，請使用 `date` 篩選器。`match` 設定會指定來源欄位及其值的日期格式。在下列範例中，日期儲存在 `timestamp` 欄位中，而格式中的 `Z` 代表時區位移：

```ruby
filter {
  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
  }
}
```
{% include copy.html %}

例如，如果事件的 `timestamp` 欄位包含 `20/Sep/2017:13:22:22 +0200`，篩選器會將 `@timestamp` 設為 `2017-09-20T11:22:22.000Z`。如果您同時使用上一節中的 `file` 輸出，Logstash 會將此事件寫入 `access_2017_09_20.log` 檔案。

如果篩選器無法剖析日期，便會將 `_dateparsefailure` 標籤新增至事件。

篩選器設定 `@timestamp` 欄位後，您可能不再需要原始的 `timestamp` 欄位。若要移除該欄位，請新增 `remove_field` 選項：

```ruby
filter {
  date {
    match => [ "timestamp", "dd/MMM/yyyy:HH:mm:ss Z" ]
    remove_field => [ "timestamp" ]
  }
}
```
{% include copy.html %}

只有在篩選器成功剖析日期時，`remove_field` 選項才會生效。

## 剖析使用者代理 (user agent)

使用者代理 (user agent) 字串可識別傳送請求的瀏覽器、瀏覽器版本、作業系統與裝置。由於使用者代理字串的格式差異很大，`grok` 模式無法可靠地擷取這些資訊。

請使用 `useragent` 篩選器將使用者代理字串剖析為獨立的欄位。`source` 設定用來指定包含使用者代理字串的欄位。預設情況下，篩選器會將剖析後的欄位加入 `user_agent` 欄位。若要將欄位儲存在其他欄位，請在 `target` 設定中指定欄位名稱：

```ruby
filter {
  useragent {
    source => "agent"
    target => "ua"
  }
}
```
{% include copy.html %}

例如，若 `agent` 欄位包含 `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36`，篩選器會將下列 `ua` 物件加入事件：

```
"ua" => {
         "os" => {
           "name" => "Windows",
        "version" => "10",
           "full" => "Windows 10"
    },
       "name" => "Chrome",
     "device" => {
        "name" => "Other"
    },
    "version" => "120.0"
}
```

您可以將這些欄位傳送至 OpenSearch，然後進行彙總。例如，在 OpenSearch Dashboards 中建立圓餅圖，顯示使用各種瀏覽器或作業系統的訪客比例，或建立長條圖顯示最常見的瀏覽器版本。

## 擴充地理資料

使用 `geoip` 篩選器查詢 IP 位址的地理位置。此篩選器使用 MaxMind 的 GeoLite2 資料庫。

`source` 設定指定包含 IP 位址的欄位，`target` 設定指定用來儲存位置資訊的欄位。若要從記錄檔行擷取 IP 位址至欄位，請使用 `grok` 模式，例如 `%{IP:clientip}`。如需詳細資訊，請參閱 [grok]({{site.url}}{{site.baseurl}}/tools/logstash/common-filters/#grok)。除非 `source` 欄位是 `ip` 子欄位（例如 `[client][ip]`），否則必須提供 `target` 設定：

```ruby
filter {
  geoip {
    source => "clientip"
    target => "client"
  }
}
```
{% include copy.html %}

此篩選器會將包含位置資訊（例如國家、洲、時區與座標）的 `geo` 物件新增至 `target` 欄位：

```
"client" => {
    "geo" => {
          "continent_code" => "NA",
            "country_name" => "United States",
        "country_iso_code" => "US",
                "timezone" => "America/Chicago",
                "location" => {
            "lon" => -97.822,
            "lat" => 37.751
        }
    },
     "ip" => "8.8.8.8"
}
```

若只要新增部分位置欄位，請在 `fields` 設定中列出這些欄位，例如 `fields => ["country_name"]`。

並非所有欄位（例如城市名稱與地區）都適用於每個 IP 位址。如果篩選器找不到 IP 位址的位置（例如因為該位址是私人位址），就會將 `_geoip_lookup_failure` 標籤新增至事件。

`location` 物件包含 `lat` 與 `lon` 欄位，這是 OpenSearch `geo_point` 欄位類型接受的格式之一。若要對位置執行地理空間查詢，請在索引中將 `location` 欄位對應為 `geo_point`。如需詳細資訊，請參閱 [Geopoint 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/)。
