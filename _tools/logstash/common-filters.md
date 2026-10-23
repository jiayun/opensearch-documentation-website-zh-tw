---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常見的篩選器外掛程式"
parent: Logstash
nav_order: 220
redirect_from:
 - /clients/logstash/common-filters/
---

# 常用篩選外掛程式

篩選外掛程式會在事件通過管線時修改事件。使用 `mutate` 篩選器來變更欄位的值與類型，並使用 `grok` 篩選器將非結構化文字剖析為欄位。所有篩選外掛程式也都支援一組常用選項，可用於新增與移除欄位和標籤。

<!-- vale off -->
## mutate
<!-- vale on -->

使用 `mutate` 篩選器來重新命名、移除、取代及修改欄位。例如，如果您將事件傳送到 OpenSearch，而某個欄位的資料類型與現有的索引對應不符，可以使用 `mutate` 篩選器將該欄位轉換為對應的類型。

下列管線會將 `quantity` 欄位轉換為整數：

```ruby
input {
  http {
    host => "127.0.0.1"
    port => 8080
  }
}

filter {
  mutate {
    convert => { "quantity" => "integer" }
  }
}

output {
  stdout { }
}
```
{% include copy.html %}

若要測試此管線，請啟動 Logstash 並傳送一個 `quantity` 為字串的請求：

```bash
curl -XPUT -H "Content-Type: application/json" -d '{"amount": 10, "quantity": "3"}' http://localhost:8080
```
{% include copy.html %}

在產生的事件中，`quantity` 是整數：

```
{
      "quantity" => 3,
        "amount" => 10,
    "@timestamp" => 2026-10-16T17:57:09.851542204Z,
      "@version" => "1",
    ...
}
```

您也可以將欄位轉換為 `float`、`string` 和 `boolean` 類型。如果欄位包含陣列，篩選器會轉換陣列的每個元素。如果值無法轉換，例如將字串 `world` 轉換為整數，篩選器會保持該值不變，並在事件中新增 `_mutate_error` 標籤，Logstash 會繼續處理該事件。

## 常用選項

所有篩選器外掛程式皆支援下列選項。

選項 | 說明
:--- | :---
`add_field` | 在事件中新增一或多個欄位。
`remove_field` | 從事件中移除一或多個欄位。
`add_tag` | 在事件中新增一或多個標籤。使用標籤可根據事件所包含的標籤，有條件地處理事件。
`remove_tag` | 從事件中移除一或多個標籤。

下列管線會從每個事件中移除 `host` 欄位：

```ruby
input {
  http {
    host => "127.0.0.1"
    port => 8080
  }
}

filter {
  mutate {
    remove_field => ["host"]
  }
}

output {
  stdout { }
}
```
{% include copy.html %}

<!-- vale off -->
## grok
<!-- vale on -->

使用 `grok` 篩選器將非結構化文字剖析為欄位。`grok` 篩選器使用模式來比對文字，這些模式是具名的正規表示式。

`grok` 模式的格式如下：

```
%{SYNTAX:SEMANTIC}
```

模式包含下列元素：

- `SYNTAX`：文字必須符合的模式名稱。使用任一預先定義的 `grok` 模式。例如，`EMAILADDRESS` 模式會比對電子郵件地址。
- `SEMANTIC`：用來儲存相符文字的欄位名稱。例如，如果您比對電子郵件地址，可以將欄位命名為 `email`。

若要將相符文字轉換為數字，請在欄位名稱後面加上 `:int` 或 `:float`，例如 `%{INT:http_status:int}`。

下列存取記錄行包含用戶端的 IP 位址、用戶端的身分與使用者名稱、請求時間、HTTP 方法與路徑、HTTP 狀態碼，以及以位元組為單位的回應大小：

```bash
184.252.108.229 - joe [20/Sep/2017:13:22:22 +0200] GET /products/view/123 200 12798
```

下列 `grok` 篩選器會將此行剖析為欄位：

```ruby
filter {
  grok {
    match => { "message" => "%{IP:ip_address} %{USER:identity} %{USER:auth} \[%{HTTPDATE:reg_ts}\] %{WORD:http_verb} %{URIPATHPARAM:req_path} %{INT:http_status:int} %{INT:num_bytes:int}" }
  }
}
```
{% include copy.html %}

此模式的 `%{...}` 運算式內不含空格。運算式之間的空格必須與記錄行中的空格完全相符。

此篩選器使用下列模式。

模式 | 比對內容
:--- | :---
`IP` | 用戶端的 IP 位址。
`USER` | 用戶端的身分（本範例中為 `-`）與使用者名稱。
`HTTPDATE` | 請求時間。
`WORD` | HTTP 方法。
`URIPATHPARAM` | 請求路徑。
`INT` | HTTP 狀態碼與回應大小。

此篩選器會將下列欄位新增至事件：

```
{
     "ip_address" => "184.252.108.229",
       "identity" => "-",
           "auth" => "joe",
         "reg_ts" => "20/Sep/2017:13:22:22 +0200",
      "http_verb" => "GET",
       "req_path" => "/products/view/123",
    "http_status" => 200,
      "num_bytes" => 12798,
    ...
}
```

如果文字不符合模式，篩選器會將 `_grokparsefailure` 標籤新增至事件。

Logstash 包含適用於常見記錄檔格式的預先定義模式。如需模式清單，請參閱 [Logstash 模式](https://github.com/logstash-plugins/logstash-patterns-core/tree/main/patterns/ecs-v1)。若要修改剖析後的欄位，請使用 `mutate` 篩選器。
