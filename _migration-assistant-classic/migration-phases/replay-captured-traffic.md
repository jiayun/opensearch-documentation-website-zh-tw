---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Traffic Replayer"
nav_order: 7
parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/replay-captured-traffic/
---

# 使用 Traffic Replayer

**注意**：本頁面僅適用於您在遷移過程中使用 Capture and Replay 以避免停機的情況。如果您僅執行回填遷移，可以略過此步驟。
{: .note}

本指南說明如何在遷移過程中使用 Traffic Replayer，將來源叢集擷取的流量重新傳送至目標叢集。Traffic Replayer 可讓您驗證目標叢集是否能以與來源叢集相同的方式處理請求，並追上即時流量，以實現順利的遷移。

## 何時執行 Traffic Replayer

部署 Migration Assistant 之後，Traffic Replayer 預設不會執行。應在所有中繼資料與文件都遷移完成後才啟動，以確保來源叢集的近期變更能正確反映在目標叢集中。

例如，如果某份文件在取得快照之後被刪除，在文件遷移完成之前啟動 Traffic Replayer，可能會導致刪除請求在該文件加入目標之前執行。在所有其他遷移程序完成後再執行 Traffic Replayer，可確保目標叢集與來源叢集保持一致。

## 組態選項

[Traffic Replayer 設定]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/deploy/configuration-options/)是在部署 Migration Assistant 時設定的。請務必設定 Traffic Replayer 的驗證模式，使其能與目標叢集正確通訊。

## 使用 Traffic Replayer

若要管理 Traffic Replayer，請使用 `console replay` 命令。以下範例顯示可用的命令。

### 啟動 Traffic Replayer

下列命令會以部署時指定的選項啟動 Traffic Replayer：

```bash
console replay start
```

啟動 Traffic Replayer 時，您應該會收到類似以下的輸出：

```bash
root@ip-10-0-2-66:~# console replay start
Replayer started successfully.
Service migration-dev-traffic-Replayer-default set to 1 desired count. Currently 0 running and 0 pending.
```

## 檢查 Traffic Replayer 的狀態

使用下列命令顯示 Traffic Replayer 的狀態：

```bash
console replay status
```

Replay 會傳回下列其中一種狀態：

- `Running` 顯示目前正在執行的容器執行個體數量。
- `Pending` 表示正在佈建中的執行個體數量。
- `Desired` 顯示應執行的執行個體總數。

您應該會收到類似以下的輸出：

```bash
root@ip-10-0-2-66:~# console replay status
(<ReplayStatus.STOPPED: 4>, 'Running=0\nPending=0\nDesired=0')
```

## 停止 Traffic Replayer

下列命令會停止 Traffic Replayer：

```bash
console replay stop
```

您應該會收到類似以下的輸出：

```bash
root@ip-10-0-2-66:~# console replay stop
Replayer stopped successfully.
Service migration-dev-traffic-Replayer-default set to 0 desired count. Currently 0 running and 0 pending.
```



### 傳遞保證

Traffic Replayer 會從 Kafka 擷取流量，並在將請求傳送至目標叢集後更新其提交游標。這提供了「至少一次」的傳遞保證；然而，成功並非總是有保證。因此，您應該監視指標與 tuple 輸出，或執行外部驗證，以確保目標叢集如預期運作。

## 時間縮放

Traffic Replayer 會按照從每個連線接收自來源的順序傳送請求。但是，不同連線之間的相對時間順序並不保證。例如：

- **情境**：存在兩個連線：一個每分鐘傳送一次 PUT 請求，另一個每秒傳送一次 GET 請求。
- **行為**：Traffic Replayer 會維持每個連線內的順序，但連線之間（PUT 與 GET）的相對時間順序不會保留。

假設來源叢集在 100 ms 內回應請求（GET 與 PUT）：

- 在**加速係數為 1** 的情況下，目標會經歷與來源相同的請求速率與閒置期間。
- 在**加速係數為 2** 的情況下，請求會以兩倍速度傳送，GET 每 500 ms 傳送一次，PUT 每 30 秒傳送一次。
- 在**加速係數為 10** 的情況下，請求會以 10 倍速度傳送，只要目標回應夠快，Traffic Replayer 就能維持這個節奏。

如果目標無法及時回應，Traffic Replayer 會等待前一個請求完成後才傳送下一個請求。這可能會造成延遲，並影響全域的相對順序。

## 轉換

在遷移過程中，某些請求可能需要在版本之間進行轉換。例如，Elasticsearch 過去支援索引中的多種 type 對應，但在 OpenSearch 中已不再如此。用戶端可能需要相應調整，例如將文件拆分到多個索引，或轉換請求資料。

Traffic Replayer 會自動改寫主機與驗證標頭，但對於更複雜的轉換，可以使用 `--transformer-config` 選項指定自訂轉換規則。如需更多資訊，請參閱 [Traffic Replayer `README`](https://github.com/opensearch-project/opensearch-migrations/blob/c3d25958a44ec2e7505892b4ea30e5fbfad4c71b/TrafficCapture/trafficReplayer/README.md#transformations)。

### 轉換範例

假設來源請求包含一個需要移除的 `tagToExcise` 元素，且其子元素需被提升，同時 URI 路徑包含也應移除的 `extraThingToRemove`。下列 Jolt 指令碼可處理此轉換：

```json
[{ "JsonJoltTransformerProvider":
[
 {
 "script": {
 "operation": "shift",
 "spec": {
 "payload": {
 "inlinedJsonBody": {
 "top": {
 "tagToExcise": {
 "*": "payload.inlinedJsonBody.top.&" 
 },
 "*": "payload.inlinedJsonBody.top.&"
 },
 "*": "payload.inlinedJsonBody.&"
 },
 "*": "payload.&"
 },
 "*": "&"
 }
 }
 }, 
 {
 "script": {
 "operation": "modify-overwrite-beta",
 "spec": {
 "URI": "=split('/extraThingToRemove',@(1,&))"
 }
 }
 },
 {
 "script": {
 "operation": "modify-overwrite-beta",
 "spec": {
 "URI": "=join('',@(1,&))"
 }
 }
 }
]
}]
```

傳送至目標的結果請求會類似如下：

```bash
PUT /oldStyleIndex/moreStuff HTTP/1.0
host: testhostname

{"top":{"properties":{"field1":{"type":"text"},"field2":{"type":"keyword"}}}}
```
{% include copy.html %}

您可以使用 `--transformer-config-base64` 傳遞 Base64 編碼的轉換指令碼。

## 結果記錄檔

來源擷取的 HTTP 交易以及重新傳送至目標叢集的交易，會記錄在位於 `/shared-logs-output/traffic-replayer-default/*/tuples/tuples.log` 的檔案中。`/shared-logs-output` 目錄由所有容器共用，包括 Migration Console。您可以從 Migration Console 使用相同路徑存取這些檔案。先前的執行結果也以 `gzipped` 格式提供。

每筆記錄項目都是一個以換行符分隔的 JSON 物件，包含來源與目標請求/回應的資訊，以及其他交易詳細資料，例如回應時間。

這些記錄檔包含所有請求的內容，包括授權標頭以及所有 HTTP 訊息的內容。請確保對遷移環境的存取受到限制，因為這些記錄檔是判斷來源與目標叢集中發生什麼事情的依據。來源的回應時間是指代理程式傳送請求結尾到收到回應之間的時間長度。目標的回應時間雖以相同方式記錄，但請注意擷取代理程式、Traffic Replayer 與目標的位置可能不同，且這些記錄檔並未考量用戶端的位置。
{: .note}


### 範例記錄項目

下列範例記錄項目顯示同時傳送至來源與目標叢集的 `/_cat/indexes?v` 請求：

```json
{
 "sourceRequest": {
 "Request-URI": "/_cat/indexes?v",
 "Method": "GET",
 "HTTP-Version": "HTTP/1.1",
 "Host": "capture-proxy:9200",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "User-Agent": "curl/8.5.0",
 "Accept": "*/*",
 "body": ""
 },
 "sourceResponse": {
 "HTTP-Version": {"keepAliveDefault": true},
 "Status-Code": 200,
 "Reason-Phrase": "OK",
 "response_time_ms": 59,
 "content-type": "text/plain; charset=UTF-8",
 "content-length": "214",
 "body": "aGVhbHRoIHN0YXR1cyBpbmRleCAgICAgICB..."
 },
 "targetRequest": {
 "Request-URI": "/_cat/indexes?v",
 "Method": "GET",
 "HTTP-Version": "HTTP/1.1",
 "Host": "opensearchtarget",
 "Authorization": "Basic YWRtaW46bXlTdHJvbmdQYXNzd29yZDEyMyE=",
 "User-Agent": "curl/8.5.0",
 "Accept": "*/*",
 "body": ""
 },
 "targetResponses": [{
 "HTTP-Version": {"keepAliveDefault": true},
 "Status-Code": 200,
 "Reason-Phrase": "OK",
 "response_time_ms": 721,
 "content-type": "text/plain; charset=UTF-8",
 "content-length": "484",
 "body": "aGVhbHRoIHN0YXR1cyBpbmRleCAgICAgICB..."
 }],
 "connectionId": "0242acfffe13000a-0000000a-00000005-1eb087a9beb83f3e-a32794b4.0",
 "numRequests": 1,
 "numErrors": 0
}
```
{% include copy.html %}


### 解碼記錄內容

HTTP 訊息本文的內容會以 Base64 編碼，以處理各種類型的流量，包括壓縮資料。若要以更易於閱讀的格式檢視記錄，請使用主控台程式庫 `tuples show`。以下列方式執行指令碼，將於家目錄中產生 `readable-tuples.log`：

```shell
console tuples show --in /shared-logs-output/traffic-Replayer-default/d3a4b31e1af4/tuples/tuples.log > readable-tuples.log
```

`readable-tuples.log` 應類似下列內容：

```json
{
 "sourceRequest": {
 "Request-URI": "/_cat/indexes?v",
 "Method": "GET",
 "HTTP-Version": "HTTP/1.1",
 "Host": "capture-proxy:9200",
 "Authorization": "Basic YWRtaW46YWRtaW4=",
 "User-Agent": "curl/8.5.0",
 "Accept": "*/*",
 "body": ""
 },
 "sourceResponse": {
 "HTTP-Version": {"keepAliveDefault": true},
 "Status-Code": 200,
 "Reason-Phrase": "OK",
 "response_time_ms": 59,
 "content-type": "text/plain; charset=UTF-8",
 "content-length": "214",
 "body": "health status index uuid ..."
 },
 "targetRequest": {
 "Request-URI": "/_cat/indexes?v",
 "Method": "GET",
 "HTTP-Version": "HTTP/1.1",
 "Host": "opensearchtarget",
 "Authorization": "Basic YWRtaW46bXlTdHJvbmdQYXNzd29yZDEyMyE=",
 "User-Agent": "curl/8.5.0",
 "Accept": "*/*",
 "body": ""
 },
 "targetResponses": [{
 "HTTP-Version": {"keepAliveDefault": true},
 "Status-Code": 200,
 "Reason-Phrase": "OK",
 "response_time_ms": 721,
 "content-type": "text/plain; charset=UTF-8",
 "content-length": "484",
 "body": "health status index uuid ..."
 }],
 "connectionId": "0242acfffe13000a-0000000a-00000005-1eb087a9beb83f3e-a32794b4.0",
 "numRequests": 1,
 "numErrors": 0
}
```


## Amazon CloudWatch 指標與儀表板
Migration Assistant 會建立名為 `MigrationAssistant_ReindexFromSnapshot_Dashboard` 的 Amazon CloudWatch 儀表板，以視覺化呈現回填程序的健康狀態與效能。此儀表板結合了回填工作程式與遷移至 Amazon OpenSearch Service 的指標，提供 Capture Proxy 與 Traffic Replayer 元件的效能與健康狀態深入解析，包括下列指標：

- 讀取與寫入的位元組數。
- 作用中連線數。
- 重播速度倍數。 

您可以在部署 Migration Assistant 的 AWS 區域中，於 Amazon CloudWatch 儀表板的 AWS Management Console 找到 Capture and Replay 儀表板。

Traffic Replayer 會將各種 OpenTelemetry 指標發出至 Amazon CloudWatch，並透過 AWS X-Ray 傳送追蹤。下列是一些有助於評估遷移效能的有用指標。

### `sourceStatusCode`

此指標會追蹤來源與目標叢集的 HTTP 狀態碼，並包含 HTTP 動詞的維度，例如 `GET` 或 `POST`，以及狀態碼系列 (200--299)。這些維度有助於快速找出來源與目標之間的差異，例如當 `DELETE 200s` 變成 `4xx`，或 `GET 4xx` 錯誤變成 `5xx` 錯誤時。

### `lagBetweenSourceAndTargetRequests`

此指標顯示請求到達來源與目標叢集之間的延遲。在加速倍數大於 1 且目標叢集能有效處理請求的情況下，此值應會隨著重播進行而降低，表示重播延遲減少。

### 其他指標

下列指標也會一併回報：

- **輸送量**：`bytesWrittenToTarget` 與 `bytesReadFromTarget` 表示進出叢集的輸送量。
- **重試**：`numRetriedRequests` 會追蹤因來源與目標之間的狀態碼不符而重試的請求數。
- **事件計數**：各種 `(*)Count` 指標會追蹤已完成的事件數。
- **持續時間**：`(*)Duration` 指標會測量程序中每個步驟的持續時間。
- **例外狀況**：`(*)ExceptionCount` 顯示每個處理階段中遇到的例外狀況數。


## CloudWatch 注意事項

推送至 CloudWatch 的指標與儀表板可能會有約 5 分鐘的可見性延遲。CloudWatch 保留高解析度資料的時間也比低解析度資料短。如需詳細資訊，請參閱 [Amazon CloudWatch concepts](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/cloudwatch_concepts.html)。

## 疑難排解

下列各節可能有助於診斷常見的問題。

### Elasticsearch 內容類型與 accept 標頭相容性

較新的 Elasticsearch 用戶端 (7.11 版及更新版本，包括所有 8.x 版本) 會在 `Content-Type` 與 `Accept` 標頭中使用 Elasticsearch 專屬的媒體類型。這些用戶端可能會傳送如下列所示的標頭：

- `Content-Type: application/vnd.elasticsearch+json;compatible-with=8`
- `Accept: application/vnd.elasticsearch+json;compatible-with=8`

當遷移至 OpenSearch 或其他不支援這些 Elasticsearch 專屬媒體類型的服務時，來自這些用戶端的請求可能會失敗，或被目標叢集拒絕。

**重要**：如果您使用 7.11 版或更新版本的 Elasticsearch 用戶端，並遷移至 OpenSearch 或無法辨識 `application/vnd.elasticsearch+json` 媒體類型的服務，您必須套用轉換，以將 `Content-Type` 與 `Accept` 標頭轉換為標準的 `application/json` 格式。請注意，遷移後必須更新用戶端，以使用標準媒體類型。
{: .important}

若要解決此問題，請為 Traffic Replayer 設定轉換，將 Elasticsearch 專屬的媒體類型轉換為標準的 `application/json` 格式。 

首先，在 `/shared-logs-output/content-type-transformer.js` 建立 JavaScript 轉換檔案：

```javascript
const NEW_CONTENT_TYPE = "application/json";
const ELASTIC_CONTENT_TYPE = "application/vnd.elasticsearch+json";

function transform(request, context) {
 let headers = request.get("headers");
 if (headers) {
 let contentType = headers.get("Content-Type");
 if (Array.isArray(contentType)) {
 headers.set("Content-Type", contentType.map(v => v.includes(ELASTIC_CONTENT_TYPE) ? NEW_CONTENT_TYPE : v));
 } else if (typeof contentType === "string") {
 if (contentType.includes(ELASTIC_CONTENT_TYPE)) {
 headers.set("Content-Type", NEW_CONTENT_TYPE);
 }
 }
 let accept = headers.get("Accept");
 if (Array.isArray(accept)) {
 headers.set("Accept", accept.map(v => v.includes(ELASTIC_CONTENT_TYPE) ? NEW_CONTENT_TYPE : v));
 } else if (typeof accept === "string") {
 if (accept.includes(ELASTIC_CONTENT_TYPE)) {
 headers.set("Accept", NEW_CONTENT_TYPE);
 }
 }
 }
 return request;
}

function main(context) {
 return (request) => {
 if (Array.isArray(request)) {
 return request.flat().map(item => transform(item, context));
 }
 return transform(request, context);
 };
}
(() => main)();
```
{% include copy.html %}

接著，在 `/shared-logs-output/replayer-transformation.json` 建立轉換組態檔：

```json
[
 {
 "JsonJSTransformerProvider": {
 "initializationScriptFile": "/shared-logs-output/content-type-transformer.js",
 "bindingsObject": "{}"
 }
 }
]
```
{% include copy.html %}

最後，將下列引數新增至您的 `trafficReplayerExtraArgs`，以設定 Traffic Replayer 使用此轉換：

```bash
--transformer-config-file /shared-logs-output/Replayer-transformation.json
```

此轉換指令碼會自動偵測 `Content-Type` 與 `Accept` 標頭中的 Elasticsearch 專屬媒體類型 (包括含有版本參數的類型，例如 `compatible-with=8`)，並將其取代為標準的 `application/json` 格式，確保與 OpenSearch 及其他不支援 Elasticsearch 專屬媒體類型的服務相容。

{% include migration-phase-navigation.html %}
