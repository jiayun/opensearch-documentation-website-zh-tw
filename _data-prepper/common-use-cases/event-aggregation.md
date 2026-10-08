---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "事件彙總"
parent: Common use cases
nav_order: 25
---

# 事件彙總

您可以使用 OpenSearch Data Prepper 在一段時間內彙總來自不同事件的資料。彙總事件有助於減少不必要的記錄資料量，並處理多行記錄以個別事件形式接收等使用案例。[`aggregate` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/aggregate/) 是一種有狀態的處理器，會根據一組指定識別鍵的值將事件分組，並對每個群組執行可設定的動作。

`aggregate` 處理器的狀態儲存在記憶體中。例如，若要將四個事件合併為一個，處理器需要保留前三個事件的部分內容。事件彙總群組的狀態會保留一段可設定的時間。依據您的記錄檔、所使用的彙總動作，以及處理器組態中記憶體選項的數量，彙總可能會在很長的一段時間內進行。

## 基本用法

下列範例管線使用 [`grok` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/grok/) 擷取 `sourceIp`、`destinationIp` 和 `port` 欄位，然後使用 [`aggregate` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/aggregate/) 與 `put_all` 動作，在 30 秒的期間內對這些欄位進行彙總。在 30 秒期間結束時，彙總後的記錄檔會傳送至 OpenSearch 接收端。

```json
aggregate_pipeline:  
   source:
     http:
      path: "/${pipelineName}/logs"
   processor:
     - grok:
         match: 
           log: ["%{IPORHOST:sourceIp} %{IPORHOST:destinationIp} %{NUMBER:port:int}"]
     - aggregate:
         group_duration: "30s"
         identification_keys: ["sourceIp", "destinationIp", "port"]
         action:
           put_all:
   sink:
     - opensearch:
         ...
         index: aggregated_logs
```
{% include copy-curl.html %}

例如，請考慮以下這批記錄檔：

```json
{ "log": "127.0.0.1 192.168.0.1 80", "status": 200 }
{ "log": "127.0.0.1 192.168.0.1 80", "bytes": 1000 }
{ "log": "127.0.0.1 192.168.0.1 80" "http_verb": "GET" }
```
{% include copy-curl.html %}

`grok` 處理器會擷取鍵值，使記錄事件呈現如下例所示。這些事件現在具備 `aggregate` 處理器執行 `identification_keys` 所需的資料。

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "port": 80, "status": 200 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "port": 80, "bytes": 1000 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "port": 80, "http_verb": "GET" }
```
{% include copy-curl.html %}

30 秒後，`aggregate` 處理器會將以下彙總後的記錄檔寫入接收端：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "port": 80, "status": 200, "bytes": 1000, "http_verb": "GET" }
```
{% include copy-curl.html %}

## 移除重複項目

您可以從傳入事件衍生鍵值，並為 `aggregate` 處理器指定 `remove_duplicates` 選項，以移除重複的項目。此動作會立即處理群組中的第一個事件，並捨棄該群組中所有後續的事件。

在下列範例中，第一個事件會以識別鍵 `sourceIp` 和 `destinationIp` 進行處理：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200 }
```
{% include copy-curl.html %}

管線接著會捨棄以下事件，因為它具有相同的鍵值：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 1000 }
```
{% include copy-curl.html %}

管線會處理此事件並建立新的群組，因為 `sourceIp` 不同：

```json
{ "sourceIp": "127.0.0.2", "destinationIp": "192.168.0.1", "bytes": 1000 }
```
{% include copy-curl.html %}

## 記錄彙總與條件式路由

您可以結合多個外掛程式，將記錄彙總與條件式路由結合。在此範例中，管線 `log-aggregate-pipeline` 透過 HTTP 用戶端 (例如 FluentBit) 接收記錄檔，並將 `log` 鍵中的值與 [Apache Common Log Format](https://httpd.apache.org/docs/2.4/logs.html) 進行比對，以從記錄檔中擷取重要的值。

管線使用 Grok 模式從記錄檔中擷取的其中兩個值是 `response` 和 `clientip`。接著，`aggregate` 處理器會使用 `clientip` 值搭配 `remove_duplicates` 選項，捨棄任何包含在給定 `group_duration` 內已處理過之 `clientip` 的記錄檔。

管線中存在三條路由 (即條件陳述式)。這些路由會將回應的值區分為 `2xx`、`3xx`、`4xx` 和 `5xx` 回應。具有 `2xx` 或 `3xx` 狀態的記錄檔會傳送至 `aggregated_2xx_3xx` 索引，具有 `4xx` 狀態的記錄檔會傳送至 `aggregated_4xx index`，而具有 `5xx` 狀態的記錄檔則會傳送至 `aggregated_5xx` 索引。

```json
log-aggregate-pipeline:
  source:
    http:
      # Provide the path for ingestion. ${pipelineName} will be replaced with pipeline name configured for this pipeline.
      # In this case it would be "/log-aggregate-pipeline/logs". This will be the FluentBit output URI value.
      path: "/${pipelineName}/logs"
  processor:
    - grok:
        match:
          log: [ "%{COMMONAPACHELOG_DATATYPED}" ]
    - aggregate:
        identification_keys: ["clientip"]
        action:
          remove_duplicates:
        group_duration: "180s"
  route:
    - 2xx_status: "/response >= 200 and /response < 300"
    - 3xx_status: "/response >= 300 and /response < 400"
    - 4xx_status: "/response >= 400 and /response < 500"
    - 5xx_status: "/response >= 500 and /response < 600"
  sink:
    - opensearch:
        ...
        index: "aggregated_2xx_3xx"
        routes:
          - 2xx_status
          - 3xx_status
    - opensearch:
        ...
        index: "aggregated_4xx"
        routes:
          - 4xx_status
    - opensearch:
        ...
        index: "aggregated_5xx"
        routes:
          - 5xx_status
```
