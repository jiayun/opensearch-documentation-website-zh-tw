---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文字處理"
parent: Common use cases
nav_order: 55
---

# 文字處理

OpenSearch Data Prepper 透過 [`grok processor`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/grok/) 提供文字處理功能。`grok` 處理器以 [`java-grok`](https://mvnrepository.com/artifact/io.krakens/java-grok) 程式庫為基礎，並支援所有相容的模式。`java-grok` 程式庫是使用 [`java.util.regex`](https://docs.oracle.com/javase/8/docs/api/java/util/regex/package-summary.html) 正規表示式程式庫建置的。

您可以使用 `patterns_definitions` 選項在管線中新增自訂模式。偵錯自訂模式時，[Grok Debugger](https://grokdebugger.com/) 可能會有所幫助。

## 基本用法

若要開始使用文字處理，請建立下列管線：

```json
patten-matching-pipeline:
  source
    ...
  processor:
    - grok:
        match:
          message: ['%{IPORHOST:clientip} \[%{HTTPDATE:timestamp}\] %{NUMBER:response_status:int}']
  sink:
    - opensearch:
        # Provide an OpenSearch cluster endpoint
```
{% include copy-curl.html %}

傳入的訊息可能包含下列內容：

```json
{"message": "127.0.0.1 198.126.12 [10/Oct/2000:13:55:36 -0700] 200"}
```
{% include copy-curl.html %}

在每個傳入的事件中，管線會找出 `message` 鍵中的值，並嘗試與模式進行比對。關鍵字 `IPORHOST`、`HTTPDATE` 和 `NUMBER` 已內建於此外掛程式中。

當傳入的記錄與模式比對成功時，會產生類似下列的內部事件，其中包含從原始訊息擷取的識別鍵：

```json
{ 
  "message":"127.0.0.1 198.126.12 [10/Oct/2000:13:55:36 -0700] 200",
  "response_status":200,
  "clientip":"198.126.12",
  "timestamp":"10/Oct/2000:13:55:36 -0700"
}
```
{% include copy-curl.html %}

`grok` 處理器的 `match` 組態會指定要與哪些模式比對哪些記錄鍵。

在下列範例中，`match` 組態會檢查傳入的記錄檔中是否有 `message` 鍵。如果該鍵存在，則會先將鍵值與 `SYSLOGBASE` 模式比對，再與 `COMMONAPACHELOG` 模式比對。接著會檢查記錄檔中是否有 `timestamp` 鍵。如果該鍵存在，則會嘗試將鍵值與 `TIMESTAMP_ISO8601` 模式比對。

```json
processor:
  - grok:
      match:
        message: ['%{SYSLOGBASE}', "%{COMMONAPACHELOG}"]
        timestamp: ["%{TIMESTAMP_ISO8601}"]  
```
{% include copy-curl.html %}

預設情況下，外掛程式會持續比對，直到找到成功的比對為止。例如，如果 `message` 鍵中的值已成功比對 `SYSLOGBASE` 模式，外掛程式就不會再嘗試比對其他模式。如果您想讓記錄檔與每個模式都進行比對，請加入 `break_on_match` 選項。

## 包含具名與空白擷取

在管線組態中加入 `keep_empty_captures` 選項以包含 null 擷取，或加入 `named_captures_only` 選項以僅包含具名擷取。具名擷取遵循 `%{SYNTAX:SEMANTIC}` 模式，而未具名擷取則遵循 `%{SYNTAX}` 模式。

例如，您可以修改先前的 Grok 組態，從 `%{IPORHOST}` 模式中移除 `clientip`：

```json
processor:
  - grok:
      match:
        message: ['%{IPORHOST} \[%{HTTPDATE:timestamp}\] %{NUMBER:response_status:int}']
```
{% include copy-curl.html %}

產生的 grokked 記錄檔會如下所示：

```json
{
  "message":"127.0.0.1 198.126.12 [10/Oct/2000:13:55:36 -0700] 200",
  "response_status":200,
  "timestamp":"10/Oct/2000:13:55:36 -0700"
}
```
{% include copy-curl.html %}

請注意，`clientip` 鍵已不存在，因為 `%{IPORHOST}` 模式現在是未具名擷取。

不過，如果您將 `named_captures_only` 設定為 `false`：

```json
processor:
  - grok:
      match:
        named_captures_only: false
        message: ['%{IPORHOST} \[%{HTTPDATE:timestamp}\] %{NUMBER:message:int}']
```
{% include copy-curl.html %}

則產生的 grokked 記錄檔會如下所示：

```json
{
  "message":"127.0.0.1 198.126.12 [10/Oct/2000:13:55:36 -0700] 200",
  "MONTH":"Oct",
  "YEAR":"2000",
  "response_status":200,
  "HOUR":"13",
  "TIME":"13:55:36",
  "MINUTE":"55",
  "SECOND":"36",
  "IPORHOST":"198.126.12",
  "MONTHDAY":"10",
  "INT":"-0700",
  "timestamp":"10/Oct/2000:13:55:36 -0700"
}
```
{% include copy-curl.html %}

請注意，`IPORHOST` 擷取現在會顯示為新的鍵，並伴隨一些內部的未具名擷取，例如 `MONTH` 和 `YEAR`。`HTTPDATE` 關鍵字目前使用這些模式，您可以在預設模式檔案中看到。

## 覆寫鍵

加入 `keys_to_overwrite` 選項，以指定當擷取具有相同鍵值時要覆寫哪些現有的記錄鍵。

例如，您可以修改先前的 Grok 組態，將 `%{NUMBER:response_status:int}` 取代為 `%{NUMBER:message:int}`，並將 `message` 加入要覆寫的鍵清單：

```json
processor:
  - grok:
      match:
        keys_to_overwrite: ["message"]
        message: ['%{IPORHOST:clientip} \[%{HTTPDATE:timestamp}\] %{NUMBER:message:int}']
```
{% include copy-curl.html %}

在產生的 grokked 記錄檔中，原始訊息會被數字 `200` 覆寫：

```json
{ 
  "message":200,
  "clientip":"198.126.12",
  "timestamp":"10/Oct/2000:13:55:36 -0700"
}
```
{% include copy-curl.html %}

## 使用自訂模式

在 Grok 組態中加入 `pattern_definitions` 選項，以指定自訂模式。

下列組態會建立名為 `CUSTOM_PATTERN-1` 和 `CUSTOM_PATTERN-2` 的自訂 regex 模式。預設情況下，外掛程式會持續比對，直到找到成功的比對為止。

```json
processor:
  - grok:
      pattern_definitions:
        CUSTOM_PATTERN_1: 'this-is-regex-1'
        CUSTOM_PATTERN_2: '%{CUSTOM_PATTERN_1} REGEX'
      match:
        message: ["%{CUSTOM_PATTERN_2:my_pattern_key}"]
```
{% include copy-curl.html %}

如果您將 `break_on_match` 指定為 `false`，管線會嘗試比對所有模式，並從傳入的事件中擷取鍵：

```json
processor:
  - grok:
      pattern_definitions:
        CUSTOM_PATTERN_1: 'this-is-regex-1'
        CUSTOM_PATTERN_2: 'this-is-regex-2'
        CUSTOM_PATTERN_3: 'this-is-regex-3'
        CUSTOM_PATTERN_4: 'this-is-regex-4'
      match:
        message: [ "%{PATTERN1}”, "%{PATTERN2}" ]
        log: [ "%{PATTERN3}", "%{PATTERN4}" ]
        break_on_match: false
```
{% include copy-curl.html %}

您可以定義自己的自訂模式，用於管線的模式比對。在上一個範例中，`my_pattern` 會在比對自訂模式後被擷取出來。

## 將擷取結果儲存在父鍵之下

在 Grok 組態中加入 `target_key` 選項，將所有記錄擷取結果包裝在一個額外的外層鍵值中。

例如，您可以修改先前的 Grok 組態，新增名為 `grokked` 的目標鍵：

```json
processor:
   - grok:
       target_key: "grokked"
       match:
         message: ['%{IPORHOST} \[%{HTTPDATE:timestamp}\] %{NUMBER:response_status:int}']
```

產生的 grokked 記錄檔會如下所示：

```json
{ 
  "message":"127.0.0.1 198.126.12 [10/Oct/2000:13:55:36 -0700] 200",
  "grokked": {
     "response_status":200,
     "clientip":"198.126.12",
     "timestamp":"10/Oct/2000:13:55:36 -0700"
  }
}
```
