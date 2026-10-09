---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "彙總"
parent: Processors
grand_parent: Pipelines
nav_order: 20
---

# 彙總處理器

`aggregate` 處理器會根據 `identification_keys` 的值將事件分組。接著，處理器會對每個群組執行一個動作，有助於減少不必要的記錄檔量，並隨時間建立彙總的記錄檔。您可以使用現有的動作，或使用 Java 程式碼建立您自己的自訂彙總。


## 組態

下表說明可用來設定 `aggregate` 處理器的選項。

選項 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`identification_keys` | 是 | 清單 | 用於將事件分組的無序清單。這些鍵的值相同的事件會被放入同一個群組。如果事件不包含其中一個 `identification_keys`，則該鍵的值會被視為等於 `null`。至少需要一個 identification_key（例如 `["sourceIp", "destinationIp", "port"]`）。
`action` | 是 | AggregateAction | 要對每個群組執行的動作。必須提供其中一個[可用的彙總動作](#available-aggregate-actions)，或者您也可以建立自訂彙總動作。`remove_duplicates` 和 `put_all` 是可用的動作。如需更多資訊，請參閱[建立新的彙總動作](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#creating-new-aggregate-actions)。
`group_duration` | 否 | 字串 | 群組在自動結束之前應存在的時間長度。支援 ISO_8601 表示法字串（例如「PT20.345S」或「PT15M」），以及秒（`"60s"`）和毫秒（`"1500ms"`）的簡易表示法。預設值為 `180s`。
`local_mode` | 否 | 布林值 | 當 `local_mode` 設定為 `true` 時，彙總會在每個 OpenSearch Data Prepper 節點上於本機執行，而不是使用雜湊函式根據 `identification_keys` 將事件轉送至特定節點。預設為 `false`。
`output_unaggregated_events` | 否 | 布林值 | 設定為 `true` 時，未彙總的事件會被轉送至管線中的下一個處理器或接收器。預設為 `false`。
`aggregated_events_tag` | 否 | 字串 | 要新增至彙總事件的標籤，用於將其與未彙總事件區分。當 `output_unaggregated_events` 為 `true` 時為必要。
`aggregate_when` | 否 | 字串 | 決定彙總處理器是否處理事件的條件運算式。當條件評估為 `false` 時，事件會在不經彙總的情況下被轉送。
`acknowledge_on_conclude` | 否 | 布林值 | 設定為 `true` 時，會在群組完成時（無論是達到 `group_duration` 逾時，或是因動作所定義的條件）釋放該群組的事件控制物件 (event handle)。這會犧牲端對端確認，但可防止重新處理。預設為 `false`。
`disable_group_acknowledgments` | 否 | 布林值 | 設定為 `true` 時，會停用群組確認。預設為 `false`。

## 可用的彙總動作

使用下列彙總動作來決定 `aggregate` 處理器如何處理每個群組中的事件。

<!-- vale off -->
### remove_duplicates 
<!-- vale on -->

`remove_duplicates` 動作會立即處理群組的第一個事件，並捨棄來源中與第一個事件重複的所有事件。例如，使用 `identification_keys: ["sourceIp", "destinationIp"]` 時：

1. `remove_duplicates` 動作會處理來源中的第一個事件 `{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200 }`。
2. 由於 `sourceIp` 和 `destinationIp` 與來源中的第一個事件相符，OpenSearch Data Prepper 會捨棄 `{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 1000 }` 事件。
3. `remove_duplicates` 動作會處理下一個事件 `{ "sourceIp": "127.0.0.2", "destinationIp": "192.168.0.1", "bytes": 1000 }`。由於 `sourceIp` 與群組的第一個事件不同，Data Prepper 會根據該事件建立新的群組。

<!-- vale off -->
### put_all
<!-- vale on -->

`put_all` 動作會透過覆寫現有的鍵並新增新的鍵，來合併屬於同一群組的事件，類似於 Java 的 `Map.putAll`。此動作會捨棄構成合併事件的所有事件。例如，使用 `identification_keys: ["sourceIp", "destinationIp"]` 時，`put_all` 動作會處理下列三個事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 1000 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "http_verb": "GET" }
```

接著，此動作會將這些事件合併為一個。然後，管線會使用下列合併後的事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200, "bytes": 1000, "http_verb": "GET" }
```

<!-- vale off -->
### count
<!-- vale on -->

`count` 動作會計算屬於同一群組的事件數，並產生一個包含 `identification_keys` 值與計數的新事件，計數表示群組中的事件數量。此動作會捨棄構成合併事件的所有事件。

您可以使用下列組態選項自訂處理器：

* `count_key`：用於儲存計數的鍵。預設名稱為 `aggr._count`。
* `start_time_key`：用於儲存開始時間的鍵。預設名稱為 `aggr._start_time`。
* `end_time_key`：用於儲存結束時間的鍵。預設名稱為 `aggr._end_time`。
* `metric_name`：使用 `otel_metrics` 輸出格式時的指標名稱。預設為 `count`。
* `unique_keys`：要計算唯一值的鍵清單。指定時，計數反映的是這些鍵的唯一組合數量，而非事件總數。
* `output_format`：彙總事件的格式。有效值為：
    * `otel_metrics`（預設）：輸出類型為 `SUM` 的 OpenTelemetry 指標，其中 `value` 欄位包含群組中的事件數量。
    * `raw`：產生一個 JSON 物件，以 `count_key` 欄位作為計數，並以 `start_time_key` 欄位作為彙總開始時間。

例如，使用 `identification_keys: ["sourceIp", "destinationIp"]` 時，`count` 動作會計數並處理下列事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 503 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 400 }
```

處理器會建立下列事件：

```json
{"isMonotonic":true,"unit":"1","aggregationTemporality":"AGGREGATION_TEMPORALITY_DELTA","kind":"SUM","name":"count","description":"Number of events","startTime":"2022-12-02T19:29:51.245358486Z","time":"2022-12-02T19:30:15.247799684Z","value":3.0,"sourceIp":"127.0.0.1","destinationIp":"192.168.0.1"}
```

<!-- vale off -->
### histogram
<!-- vale on -->

`histogram` 動作會彙總屬於同一群組的事件，並根據設定的 `key` 產生一個包含 `identification_keys` 值與彙總事件直方圖的新事件。直方圖包含事件數量、總和、桶 (bucket)、桶計數，以及選擇性地包含 `key` 所對應值的最小值與最大值。此動作會捨棄構成合併事件的所有事件。

您可以使用下列組態選項自訂處理器：

* `key`：用於產生直方圖的欄位名稱。
* `generated_key_prefix`：彙總事件中所建立的所有欄位所使用的 `key_prefix`。使用前置詞可確保直方圖事件的名稱不會與事件中的欄位名稱衝突。
* `units`：`key` 中值的單位。
* `record_minmax`：布林值，表示直方圖是否應包含彙總中值的最小值與最大值。
* `buckets`：桶的清單（類型為 `double` 的值），表示直方圖中的桶。
* `metric_name`：使用 `otel_metrics` 輸出格式時的指標名稱。預設為 `histogram`。
* `output_format`：彙總事件的格式。有效值為：
    * `otel_metrics`（預設）：輸出類型為 `HISTOGRAM` 的 OpenTelemetry 指標，其中包含桶邊界以及每個桶中的值數量。
    * `raw`：產生一個 JSON 物件，其中包含總和、計數、桶、桶計數、彙總開始時間、持續時間，以及在啟用 `record_minmax` 時的最小值與最大值。每個欄位名稱都會使用 `generated_key_prefix`，因此總和預設為 `aggr._sum`。

例如，使用 `identification_keys: ["sourceIp", "destinationIp", "request"]`、`key: latency` 和 `buckets: [0.0, 0.25, 0.5]` 時，`histogram` 動作會處理下列事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "request" : "/index.html", "latency": 0.2 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "request" : "/index.html", "latency": 0.55}
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "request" : "/index.html", "latency": 0.25 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "request" : "/index.html", "latency": 0.15 }
```

接著，處理器會建立下列事件：

```json
{"max":0.55,"kind":"HISTOGRAM","buckets":[{"min":-3.4028234663852886E38,"max":0.0,"count":0},{"min":0.0,"max":0.25,"count":2},{"min":0.25,"max":0.50,"count":1},{"min":0.50,"max":3.4028234663852886E38,"count":1}],"count":4,"bucketCountsList":[0,2,1,1],"description":"Histogram of latency in the events","sum":1.15,"unit":"seconds","aggregationTemporality":"AGGREGATION_TEMPORALITY_DELTA","min":0.15,"bucketCounts":4,"name":"histogram","startTime":"2022-12-14T06:43:40.848762215Z","explicitBoundsCount":3,"time":"2022-12-14T06:44:04.852564623Z","explicitBounds":[0.0,0.25,0.5],"request":"/index.html","sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "key": "latency"}
```

<!-- vale off -->
### sum
<!-- vale on -->

`sum` 動作會針對屬於同一群組的所有事件，加總所設定 `key` 的數值，並產生一個新事件，其中包含 `identification_keys` 的值與總和。此動作會捨棄組成合併事件的所有事件。

您可以使用下列組態選項來自訂此處理器：

* `key`：要加總之事件中欄位的名稱。此欄位的值必須是數值。必要。
* `metric_name`：使用 `otel_metrics` 輸出格式時指標的名稱。預設為 `sum`。
* `count_key`：使用 `raw` 輸出格式時，用來儲存加總所納入事件數目的索引鍵。預設名稱為 `aggr._count`。
* `output_format`：彙總事件的格式。有效值為：
    * `otel_metrics` (預設)：輸出類型為 `SUM` 的 OpenTelemetry 指標，其中 `value` 欄位包含總和。此指標為非單調，因為加總的值不保證為非負數。
    * `raw`：產生 JSON 物件，其中 `aggr._sum` 欄位為總和、`count_key` 欄位為加總所納入的事件數目，而 `aggr._start_time` 欄位為彙總開始時間。

例如，使用 `identification_keys: ["sourceIp", "destinationIp"]` 和 `key: bytes_out` 時，`sum` 動作會處理下列事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes_out": 1234 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes_out": 4321 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes_out": 100 }
```

此處理器會建立下列事件：

```json
{"isMonotonic":false,"unit":"1","aggregationTemporality":"AGGREGATION_TEMPORALITY_DELTA","kind":"SUM","name":"sum","description":"Sum of the events","startTime":"2022-12-02T19:29:51.245358486Z","time":"2022-12-02T19:30:15.247799684Z","value":5655.0,"sourceIp":"127.0.0.1","destinationIp":"192.168.0.1"}
```

<!-- vale off -->
### rate_limiter
<!-- vale on -->

`rate_limiter` 動作會控制每秒彙總的事件數目。根據預設，如果 `rate_limiter` 收到的事件數超過所設定的允許數目，就會封鎖 `aggregate` 處理器執行。您可以使用 `when_exceeds` 組態選項來覆寫觸發 `rate_limiter` 的事件數目。

您可以使用下列組態選項來自訂此處理器：

* `events_per_second`：每秒允許的事件數目。
* `when_exceeds`：指出當收到的事件數目大於每秒允許的事件數目時，`rate_limiter` 會採取的動作。預設值為 `block`，其會在達到每秒允許的事件數目上限後封鎖處理器執行，直到下一秒為止。或者，`drop` 選項會捨棄該秒內收到的過多事件。

例如，如果 `events_per_second` 設為 `1`，且 `when_exceeds` 設為 `drop`，則此動作會在一秒的時間間隔內收到下列事件時嘗試處理它們：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 1000 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "http_verb": "GET" }
```

第一個事件會獲得處理，但其餘事件會遭到捨棄，因為 `when_exceeds` 設為 `drop`：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "status": 200 }
```

如果 `when_exceeds` 設為 `block`，則處理器會暫停到下一秒，然後再處理其餘事件。

<!-- vale off -->
### append
<!-- vale on -->

`append` 動作會附加群組中所有事件之指定索引鍵的值，將多個事件合併成單一事件。與會覆寫值的 `put_all` 不同，`append` 會將指定索引鍵的所有值收集到清單中。

您可以使用下列組態選項來自訂此處理器：

* `keys_to_append`：索引鍵的清單，其值應在群組中的事件之間附加。彙總事件會包含每個索引鍵所遇到之所有值的清單。

例如，使用 `identification_keys: ["sourceIp"]` 和 `keys_to_append: ["status"]` 時，`append` 動作會處理下列事件：

```json
{ "sourceIp": "127.0.0.1", "status": 200 }
{ "sourceIp": "127.0.0.1", "status": 503 }
{ "sourceIp": "127.0.0.1", "status": 400 }
```

此處理器會建立下列事件：

```json
{ "sourceIp": "127.0.0.1", "status": [200, 503, 400] }
```

<!-- vale off -->
### tail_sampler
<!-- vale on -->

`tail_sampler` 動作會在群組持續時間內收集某個追蹤的所有跨度後，對 OpenTelemetry 追蹤進行取樣。它可讓您保留所有錯誤追蹤，同時對成功追蹤的某個百分比進行取樣，藉此減少儲存空間，同時保留所有錯誤追蹤。

您可以使用下列組態選項來自訂此處理器：

* `wait_period`：在將追蹤視為完成之前要等待的時間量。必須大於 0 且不得超過 60 秒。必要。
* `percent`：要取樣的非錯誤追蹤百分比 (0--100，不含)。所有錯誤追蹤一律保留。必要。
* `condition`：條件運算式，用來判斷事件是否為錯誤事件。符合此條件的事件一律保留，不受 `percent` 設定影響。

例如，使用 `identification_keys: ["traceId"]`、`wait_period: "10s"`、`percent: 20` 和 `condition: '/status_code == 2'` 時，`tail_sampler` 動作會保留所有包含至少一個 `status_code == 2` (錯誤) 跨度的追蹤，並對其餘成功追蹤的 20% 進行取樣。

<!-- vale off -->
### percent_sampler
<!-- vale on -->

`percent_sampler` 動作會根據事件百分比來控制彙總的事件數目。此動作會捨棄未包含在該百分比內的所有事件。

您可以使用 `percent` 組態來設定事件百分比，其表示在一秒間隔內處理的事件百分比 (0%--100%)。

例如，如果 percent 設為 `50`，則此動作會在一秒間隔內嘗試處理下列事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 2500 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 500 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 1000 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 3100 }
```

此管線會處理 50% 的事件、捨棄其他事件，且不會產生新事件：

```json
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 500 }
{ "sourceIp": "127.0.0.1", "destinationIp": "192.168.0.1", "bytes": 3100 }
```

## 指標

下表說明常見的 [Abstract processor](https://github.com/opensearch-project/data-prepper/blob/main/data-prepper-api/src/main/java/org/opensearch/dataprepper/model/processor/AbstractProcessor.java) 指標。

| 指標名稱 | 類型 | 說明 |
| ------------- | ---- | -----------|
| `recordsIn` | Counter | 代表記錄流入管線元件的指標。 |
| `recordsOut` | Counter | 代表記錄流出管線元件的指標。 |
| `timeElapsed` | Timer | 代表管線元件執行期間所經過時間的指標。 |


`aggregate` 處理器包含下列自訂指標。

**Counter**

* `actionHandleEventsOut`：從所設定 [action](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#action) 的 `handleEvent` 呼叫傳回的事件數目。
* `actionHandleEventsDropped`：未從所設定 [action](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#action) 的 `handleEvent` 呼叫傳回的事件數目。
* `actionHandleEventsProcessingErrors`：對所設定 [action](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#action) 呼叫 `handleEvent` 而導致錯誤的次數。
* `actionConcludeGroupEventsOut`：從所設定 [action](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#action) 的 `concludeGroup` 呼叫傳回的事件數目。
* `actionConcludeGroupEventsDropped`：未從所設定 [action](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#action) 的 `concludeGroup` 呼叫傳回的事件數目。
* `actionConcludeGroupEventsProcessingErrors`：對所設定 [action](https://github.com/opensearch-project/data-prepper/tree/main/data-prepper-plugins/aggregate-processor#action) 呼叫 `concludeGroup` 而導致錯誤的次數。

**Gauge**

* `currentAggregateGroups`：此量表代表目前作用中的彙總群組數目。當彙總群組完成並發出其結果時會減少，而當新事件起始建立新的彙總群組時會增加。
