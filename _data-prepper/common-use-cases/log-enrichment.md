---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "記錄檔擴充"
parent: Common use cases
nav_order: 35
---

# 記錄檔擴充

您可以使用 OpenSearch Data Prepper 執行不同類型的記錄檔擴充，包括：

- 篩選。
- 從字串擷取鍵值配對。
- 修改事件。
- 修改字串。
- 將清單轉換為映射表。
- 處理傳入的時間戳記。

## 篩選

使用 [`drop_events`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/drop-events/) 處理器，在將記錄事件傳送至接收端之前，篩除特定事件。例如，如果您正在收集網頁請求記錄檔，且只想儲存未成功的請求，可以建立下列管線，捨棄回應狀態碼小於 400 的所有請求，僅保留 HTTP 狀態碼為 400 及以上的記錄事件。

```yaml
log-pipeline:
  source:
  ...
  processor:
    - grok:
        match:
          log: [ "%{COMMONAPACHELOG_DATATYPED}" ]
    - drop_events:
        drop_when: "/response < 400"
  sink:
    - opensearch:
        ...
        index: failure_logs
```
{% include copy-curl.html %}

`drop_when` 選項指定要從管線捨棄哪些事件。

## 從字串擷取鍵值配對

記錄資料通常包含由鍵值配對組成的字串。例如，如果使用者查詢可分頁的 URL，HTTP 記錄檔可能包含下列 HTTP 查詢字串：

```json
page=3&q=my-search-term
```
{% include copy-curl.html %}

若要使用搜尋詞彙進行分析，您可以從查詢字串擷取 `q` 的值。[`key_value`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/key-value/) 處理器為從字串擷取鍵和值提供強大的支援。

下列範例結合 `split_string` 和 `key_value` 處理器，從 Apache 記錄檔的一行擷取查詢參數：

```yaml
pipeline:
 ...
  processor:
    - grok:
        match:
          message: [ "%{COMMONAPACHELOG_DATATYPED}" ]
    - split_string:
        entries:
          - source: request
            delimiter: "?"
    - key_value:
        source: "/request/1"
        field_split_characters: "&"
        value_split_characters: "="
        destination: query_params
```
{% include copy-curl.html %}

## 修改事件

各種[修改事件]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/mutate-event/)處理器可讓您重新命名、複製、新增及刪除事件項目。

在此範例中，如果事件中已存在 `debug` 鍵，第一個處理器會將其值設為 `true`。由於 `overwrite_if_key_exists` 設為 `true`，第二個處理器只會在事件中不存在 `debug` 鍵時，將該鍵設為 `true`。

```yaml
...
processor:
  - add_entries:
      entries:
        - key: "debug"
          value: true 
...
processor:
  - add_entries:
      entries:
        - key: "debug"
          value: true 
          overwrite_if_key_exists: true
...
```
{% include copy-curl.html %}

您也可以使用格式字串，從現有事件建立新項目。例如，`${date}-${time}` 會根據現有項目 `date` 和 `time` 的值建立新項目。

例如，下列管線會從現有事件動態新增事件項目：

```yaml
processor:
  - add_entries:
      entries:
        - key: "key_three"
          format: "${key_one}-${key_two}
```
{% include copy-curl.html %}

請考慮下列傳入事件：

```json
{
   "key_one": "value_one",
   "key_two": "value_two"
}
```
{% include copy-curl.html %}

處理器會將其轉換為具有名為 `key_three` 的新鍵的事件，此鍵結合原始事件中其他鍵的值，如下列範例所示：

```json
{
   "key_one": "value_one",
   "key_two": "value_two",
   "key_three": "value_one-value_two"
}
```
{% include copy-curl.html %}

## 修改字串

各種[修改字串]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/mutate-string/)處理器提供工具，讓您操作傳入資料中的字串。例如，如果您需要將字串分割為陣列，可以使用 `split_string` 處理器：

```yaml
...
processor:
  - split_string:
      entries:
        - source: "message"
          delimiter: "&"
...
```
{% include copy-curl.html %}

處理器會將 `a&b&c` 這類字串轉換為 `["a", "b", "c"]`。

## 將清單轉換為映射表

[`list_to_map`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/list-to-map/) 處理器是修改事件處理器之一，可將事件中的物件清單轉換為映射表。

例如，請考慮下列處理器組態：

```yaml
...
processor:
  - list_to_map:
      key: "name"
      source: "A-car-as-list"
      target: "A-car-as-map"
      value_key: "value"
      flatten: true
...
```
{% include copy-curl.html %}

下列處理器會將包含物件清單的事件轉換為映射表，如下所示：

```json
{
  "A-car-as-list": [
    {
      "name": "make",
      "value": "tesla"
    },
    {
      "name": "model",
      "value": "model 3"
    },
    {
      "name": "color",
      "value": "white"
    }
  ]
}
```
{% include copy-curl.html %}

```json
{
  "A-car-as-map": {
    "make": "tesla",
    "model": "model 3",
    "color": "white"
  }
}
```
{% include copy-curl.html %}

另一個範例是具有下列結構的傳入事件：

```json
{
  "mylist" : [
    {
      "somekey" : "a",
      "somevalue" : "val-a1",
      "anothervalue" : "val-a2"
    },
    {
      "somekey" : "b",
      "somevalue" : "val-b1",
      "anothervalue" : "val-b2"
    },
    {
      "somekey" : "b",
      "somevalue" : "val-b3",
      "anothervalue" : "val-b4"
    },
    {
      "somekey" : "c",
      "somevalue" : "val-c1",
      "anothervalue" : "val-c2"
    }
  ]
}
```
{% include copy-curl.html %}

您可以在處理器組態中定義下列選項：

```yaml
...
processor:            
  - list_to_map:
      key: "somekey"
      source: "mylist"
      target: "myobject"
      flatten: true
...
```
{% include copy-curl.html %}

處理器會新增 `myobject` 物件來修改事件：

```json
{
  "myobject" : {
    "a" : [
      {
        "somekey" : "a",
        "somevalue" : "val-a1",
        "anothervalue" : "val-a2"
      }  
    ],
    "b" : [
      {
        "somekey" : "b",
        "somevalue" : "val-b1",
        "anothervalue" : "val-b2"
      },
      {
        "somekey" : "b",
        "somevalue" : "val-b3",
        "anothervalue" : "val-b4"
      }
    ]
    "c" : [
      {
        "somekey" : "c",
        "somevalue" : "val-c1",
        "anothervalue" : "val-c2"
      }  
    ]
  }
}
```
{% include copy-curl.html %}

在許多情況下，您可能想要將每個鍵的陣列扁平化。在這些情況下，您可以選擇要保留哪個物件。處理器提供保留第一個或最後一個物件的選擇。例如，請考慮下列內容：

```yaml
...
processor:
  - list_to_map:
      key: "somekey"
      source: "mylist"
      target: "myobject"
      flatten: true
      flattened_element: first
...
```
{% include copy-curl.html %}

接著，新建立的 `myobject` 中的欄位會依此扁平化：

```json
{
  "myobject" : {
    "a" : {
      "somekey" : "a",
      "somevalue" : "val-a1",
      "anothervalue" : "val-a2"
    },
    "b" : {
      "somekey" : "b",
      "somevalue" : "val-b1",
      "anothervalue" : "val-b2"
    }
    "c" : {
      "somekey" : "c",
      "somevalue" : "val-c1",
      "anothervalue" : "val-c2"
    }
  }
}
```
{% include copy-curl.html %}

## 處理傳入的時間戳記

[`date`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/date/) 處理器會解析傳入事件中的 `timestamp` 鍵，將其轉換為國際標準化組織（ISO）8601 格式：

```yaml
...
  processor:          
    - date:
        match:
          - key: timestamp
            patterns: ["dd/MMM/yyyy:HH:mm:ss"] 
        destination: "@timestamp"
        source_timezone: "America/Los_Angeles"
        destination_timezone: "America/Chicago"
        locale: "en_US"
...
```
{% include copy-curl.html %}

如果上述管線處理下列事件：

```json
{"timestamp": "10/Feb/2000:13:55:36"}
```
{% include copy-curl.html %}

它會將事件轉換為下列格式：

```json
{
  "timestamp":"10/Feb/2000:13:55:36",
  "@timestamp":"2000-02-10T15:55:36.000-06:00"
}
```
{% include copy-curl.html %}

### 產生時間戳記

如果您為 `destination` 選項指定 `@timestamp`，`date` 處理器便可為傳入事件產生時間戳記：

```yaml
...
  processor:
    - date:
        from_time_received: true
        destination: "@timestamp"
...
```
{% include copy-curl.html %}

### 推導標點符號模式

[`substitute_string`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/substitute-string/) 處理器（修改字串處理器之一）可讓您從傳入事件推導標點符號模式。在下列管線範例中，處理器會掃描傳入的 Apache 記錄事件，並從中推導標點符號模式：

```yaml
processor:  
  - substitute_string:
      entries:
        - source: "message"
          from: "[a-zA-Z0-9_]+"
          to:""
        - source: "message"
          from: "[ ]+"
          to: "_"  
```
{% include copy-curl.html %}

下列傳入的 Apache HTTP 記錄檔：

```json
[{"message":"10.10.10.11 - admin [19/Feb/2015:15:50:36 -0500] \"GET /big2.pdf HTTP/1.1\" 200 33973115 0.202 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36\""}]
```

會產生下列標點符號模式：
```json
{"message":"..._-_[//:::_-]_\"_/._/.\"_._\"-\"_\"/._(;_)_/._(,_)_/..._/.\""}
```
{% include copy-curl.html %}

您可以將這些產生的模式傳入使用 `count` 動作的 [`aggregate`]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/aggregate/) 處理器，以計算這些模式的數量。
