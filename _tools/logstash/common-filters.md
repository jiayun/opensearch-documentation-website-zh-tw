---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常見的篩選器外掛程式"
parent: Logstash
nav_order: 220
redirect_from:
 - /clients/logstash/common-filters/
---

# 常見的篩選器外掛程式

本頁列出常見的篩選器外掛程式。

<!-- vale off -->
## mutate
<!-- vale on -->

您可以使用 `mutate` 篩選器來變更欄位的資料類型。例如，當您將事件傳送至 OpenSearch，而需要變更欄位的資料類型以符合現有的對應時，可以使用 `mutate` 篩選器。

若要將 `quantity` 欄位從 `string` 類型轉換為 `integer` 類型：

```yml
input {
  http {
    host => "127.0.0.1"
    port => 8080
  }
}

filter {
  mutate {
   convert => {"quantity" => "integer"}
  }
}

output {
  file {
    path => "output.txt"
  }
}
```

#### 範例輸出

可以看到 `quantity` 欄位的類型已從 `string` 變更為 `integer`。

```yml
{
  "quantity" => 3,
  "host" => "127.0.0.1",
  "@timestamp" => 2021-05-23T19:02:08.026Z,
  "amount" => 10,
  "@version" => "1",
  "headers" => {
    "request_path" => "/",
    "connection" => "keep-alive",
    "content_length" => "41",
    "http_user_agent" => "PostmanRuntime/7.26.8",
    "request_method" => "PUT",
    "cache_control" => "no-cache",
    "http_accept" => "*/*",
    "content_type" => "application/json",
    "http_version" => "HTTP/1.1",
    "http_host" => "127.0.0.1:8080",
    "accept_encoding" => "gzip, deflate, br",
    "postman_token" => "ffd1cdcb-7a1d-4d63-90f8-0f2773069205"
   }
}
```

其他可轉換的資料類型包括 `float`、`string` 與 `boolean` 值。若傳入陣列，`mutate` 篩選器會轉換陣列中的所有元素。若傳入類似 "world" 的 `string` 並嘗試轉換為 `integer` 類型，結果為 0，且 Logstash 會繼續處理事件。

Logstash 為所有篩選器外掛程式支援幾個常見選項：

選項 | 說明
:--- | :---
`add_field` | 在事件中新增一或多個欄位。
`remove_field` | 從事件中移除一或多個欄位。
`add_tag` | 為事件新增一或多個標籤。您可以根據事件所包含的標籤，使用標籤對事件執行條件式處理。
`remove_tag` | 從事件中移除一或多個標籤。

例如，您可以從事件中移除 `host` 欄位：

```yml
input {
  http {
    host => "127.0.0.1"
    port => 8080
  }
}

filter {
  mutate {
    remove_field => {"host"}
  }
}

output {
  file {
    path => "output.txt"
  }
}
```

<!-- vale off -->
## grok
<!-- vale on -->

透過 `grok` 篩選器，您可以解析非結構化資料並將其結構化為欄位。`grok` 篩選器使用文字模式來比對記錄檔中的文字。您可以將文字模式視為包含正規表示式的變數。

文字模式的格式如下：

```bash
%{SYNTAX:SEMANTIC}
```

`SYNTAX` 是文字必須符合的格式，模式才能比對成功。您可以輸入 `grok` 的任何預先定義模式。例如，您可以使用 email 識別碼從給定的文字中比對電子郵件地址。

`SEMANTIC` 是比對到的文字的任意名稱。例如，若您使用 email 識別碼語法，可以將它命名為「email」。

下列請求包含訪客的 IP 位址、訪客名稱、請求的時間戳記、HTTP 動詞與 URL、HTTP 狀態碼，以及位元組數：

```bash
184.252.108.229 - joe [20/Sep/2017:13:22:22 +0200] GET /products/view/123 200 12798
```

若要將此請求拆分為不同欄位：

```yml
filter {
  grok {
   match => { "message" => " %{IP: ip_address} %{USER:identity}
                             %{USER:auth} \[%{HTTPDATE:reg_ts}\]
                             \"%{WORD:http_verb}
                             %{URIPATHPARAM: req_path}
                             \" %{INT:http_status:int}
                             %{INT:num_bytes:int}"}
  }
}
```

其中：

- `IP`：比對 IP 位址欄位。
- `USER`：比對使用者名稱。
- `WORD`：比對 HTTP 動詞。
- `URIPATHPARAM`：比對 URI 路徑。
- `INT`：比對 HTTP 狀態欄位。
- `INT`：比對位元組數。

以下是 `grok` 篩選器將事件拆解為個別欄位後的樣子：

```yml
ip_address: 184.252.108.229
identity: joe
reg_ts: 20/Sep/2017:13:22:22 +0200
http_verb:GET
req_path: /products/view/123
http_status: 200
num_bytes: 12798
```

對於常見的記錄檔格式，您可以使用此處定義的預先定義模式---[Logstash 模式](https://github.com/logstash-plugins/logstash-patterns-core/blob/main/patterns/ecs-v1)。您可以使用 `mutate` 篩選器對結果進行任何調整。
