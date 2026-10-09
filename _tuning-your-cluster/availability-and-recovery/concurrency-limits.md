---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "並行限制"
nav_order: 65
has_children: false
parent: Availability and recovery
---

# 並行限制
**於 3.9 版導入**
{: .label .label-purple }

並行限制會限制特定動作可同時處理的請求數量，讓節點不會接受超出其可完成數量的請求。每個限制會持續根據觀察到的延遲進行調整：當節點維持輸送量時限制會增加，而當往返時間上升或下游元件開始拒絕請求時則會減少。達到限制時，額外的請求會被拒絕並回傳 HTTP `429 Too Many Requests` 回應。

預設情況下，並行限制為停用狀態。您可以為任何傳輸動作設定並行限制，例如 `indices:data/read/search` 或 `indices:data/write/bulk`，請參閱[設定並行限制](#concurrency-limit-settings)。您設定的每個限制都會建立一個 _限制器_：這是追蹤該動作請求、調整限制並拒絕超出限制之請求的元件。不需要修改程式碼或重新啟動。在您設定或變更限制後的前五分鐘，限制器會進行校準而不拒絕請求；可使用 `warmup_duration` 調整此期間。

## 並行限制設定

所有並行限制設定皆為動態設定。關於更新動態設定的資訊，請參閱[動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#dynamic-settings)。

這些設定遵循 `concurrency_limit.action.<limiter_name>.<setting>` 的模式，其中 `<limiter_name>` 是您自行選擇的名稱。該名稱將屬於同一個限制器的設定分組，本身沒有意義；`action_name` 設定則指定要限制的動作。您可以設定任意數量的限制器。

每個限制器支援下列設定：

- `concurrency_limit.action.<limiter_name>.action_name` (動態，字串)：要限制的傳輸動作名稱，例如 `indices:data/read/search` 或 `indices:data/write/bulk`。必要。清除此設定會移除該限制器。

- `concurrency_limit.action.<limiter_name>.mode` (動態，字串)：限制器的[模式](#modes)。有效值為 `disabled`、`monitor_only` 與 `enforced`。預設為 `disabled`。

- `concurrency_limit.action.<limiter_name>.algorithm` (動態，字串)：用於調整限制的[演算法](#algorithms)。有效值為 `vegas`、`gradient2` 與 `aimd`。預設為 `vegas`。

- `concurrency_limit.action.<limiter_name>.limit.initial` (動態，整數)：起始並行限制。必須至少為 `1` 且最多為 `limit.max`。預設為 `20`。

- `concurrency_limit.action.<limiter_name>.limit.max` (動態，整數)：演算法可達到的最大並行限制。必須至少為 `1` 且至少為 `limit.initial`。預設為 `200`。

- `concurrency_limit.action.<limiter_name>.warmup_duration` (動態，時間單位)：設定後限制器進行校準而不拒絕請求的期間。必須至少為 `0`。預設為 `5m`。

- `concurrency_limit.action.<limiter_name>.vegas.updrift_factor` (動態，整數)：乘以 Vegas 演算法提高限制的幅度。必須至少為 `1`。預設為 `1`，此值符合標準 Vegas 行為。

- `concurrency_limit.action.<limiter_name>.vegas.increase_barrier` (動態，整數)：Vegas 演算法提高限制前所需的連續合格樣本數。必須至少為 `1`。預設為 `1`。

- `concurrency_limit.action.<limiter_name>.vegas.decrease_barrier` (動態，整數)：Vegas 演算法降低限制前所需的連續合格樣本數。必須至少為 `1`。請求遭丟棄時，會略過此門檻並立即降低限制。預設為 `1`。

- `concurrency_limit.action.<limiter_name>.vegas.baseline_reset_load_threshold` (動態，雙精確度數)：允許探測 (probe) 重設無負載延遲基準的作用中請求數上限，以目前限制的比例表示。數值範圍為 [0, 1]。預設為 `0.5`。

- `concurrency_limit.action.<limiter_name>.gradient2.rtt_tolerance` (動態，雙精確度數)：短期往返時間可超出長期往返時間多遠，超過後 Gradient2 演算法便會降低限制。必須至少為 `1.0`。預設為 `1.5`。

- `concurrency_limit.action.<limiter_name>.aimd.backoff_ratio` (動態，雙精確度數)：當請求被丟棄時，AIMD 演算法乘以限制的因數。必須至少為 `0.5` 且小於 `1.0`。預設為 `0.9`。

- `concurrency_limit.action.<limiter_name>.burst.capacity` (動態，整數)：突發視窗開啟期間，在自適應限制之上額外新增的[突發容量](#burst-capacity)。必須至少為 `0`。預設為 `0`，此值會停用突發。

- `concurrency_limit.action.<limiter_name>.burst.close_after` (動態，整數)：突發視窗關閉前所需的連續飽和樣本數。必須至少為 `1`。預設為 `5`。

- `concurrency_limit.action.<limiter_name>.burst.open_after` (動態，整數)：突發視窗重新開啟前所需的連續未飽和樣本數。必須至少為 `1`。預設為 `5`。

- `concurrency_limit.action.<limiter_name>.partitions` (動態，清單)：[分割區](#partitions)名稱的清單。當此清單不為空時，`partition.resolver` 為必要。預設為空清單。

- `concurrency_limit.action.<limiter_name>.partition.<name>.percent` (動態，雙精確度數)：為分割區 `<name>` 保留的總限制比例。數值範圍為 [0, 1]，且所有分割區的比例總和不得超過 `1.0`。預設為 `0.0`。

- `concurrency_limit.action.<limiter_name>.partition.<name>.delay_ms` (動態，整數)：拒絕超出分割區 `<name>` 比例的請求前暫停的時間，以毫秒為單位。無論如何該請求都會被拒絕；暫停會佔住呼叫執行緒，以減緩用戶端傳送請求的速率。每個限制器最多同時暫停 100 個請求。額外的請求會直接拒絕而不暫停。必須至少為 `0`。預設為 `0`，此值會立即拒絕。

- `concurrency_limit.action.<limiter_name>.partition.resolver` (動態，字串)：將請求對應到分割區的解析器。有效值為 `byHeader`、`fixed` 與 `bySearchType`。當 `partitions` 不為空時為必要。

- `concurrency_limit.action.<limiter_name>.partition.resolver.fixed.partition` (動態，字串)：當解析器為 `fixed` 時接收所有請求的分割區。必須是 `partitions` 中列出的名稱之一。預設為 `default`。

- `concurrency_limit.action.<limiter_name>.partition.resolver.bySearchType.aggregation` (動態，字串)：當解析器為 `bySearchType` 時，接收包含彙總之搜尋請求的分割區。預設為 `aggregation`。

- `concurrency_limit.action.<limiter_name>.partition.resolver.bySearchType.filter` (動態，字串)：當解析器為 `bySearchType` 時，接收所有其他搜尋請求的分割區。預設為 `filter`。

[Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/) 會驗證每個數值，若數值超出範圍、分割區比例總和超過 `1.0`，或在未設定 `partition.resolver` 的情況下設定了 `partitions`，則會拒絕更新。若要停止限制某個動作，請將其 `mode` 設為 `disabled`，或移除該限制器的 `action_name` 設定。
{: .note}

## 模式

每個限制器會以三種模式之一執行，使用 `mode` 設定來設定：

- `disabled` (預設)：限制器未啟用。請求不會被追蹤或拒絕。
- `monitor_only`：限制器會追蹤請求並調整其限制，但絕不會拒絕請求。原本會被拒絕的請求會計入 `total_rejected` 統計資料中。使用此模式可在強制執行限制之前先觀察限制。
- `enforced`：一旦達到限制且暖機期間已過，限制器就會拒絕請求。

我們建議從 `monitor_only` 模式開始，[監視](#monitoring-concurrency-limits) `current_limit` 與 `total_rejected` 統計資料，並在限制穩定於合理值後切換至 `enforced`。
{: .tip}

## 被拒絕的請求

被拒絕的請求會以 HTTP 狀態 `429` 及 `rejected_execution_exception` 失敗。回應類似下列內容：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "rejected_execution_exception",
        "reason": "request rejected: concurrency limit reached for action [indices:data/read/search]"
      }
    ],
    "type": "rejected_execution_exception",
    "reason": "request rejected: concurrency limit reached for action [indices:data/read/search]"
  },
  "status": 429
}
```

OpenSearch 不會在這些回應中加入 `Retry-After` 標頭。請設定用戶端使用指數退避來重試。

## 演算法

`algorithm` 設定會選擇限制的調整方式。這三種演算法皆由 [Netflix concurrency-limits](https://github.com/Netflix/concurrency-limits) 程式庫提供。限制一律維持在 `limit.initial` 與 `limit.max` 之間。

每個完成的請求會產生一個 _取樣_，包含該請求的來回時間以及該請求是否成功。演算法會根據這些取樣調整限制：成功完成可讓限制增加，而下游的 `rejected_execution_exception` (例如執行緒集區拒絕) 會計為一次丟棄並降低限制。其他失敗不會影響限制。

### Vegas

預設的 `vegas` 演算法是以 TCP Vegas 壅塞控制為基礎。它會記錄觀察到的最低來回時間作為無負載基準，並將每個新取樣與其比較。當延遲維持接近基準時，限制會增加；當延遲上升時，限制會降低。Vegas 適合大多數工作負載，且為預設值。

下表列出設定 Vegas 演算法的設定。

設定 | 說明
:--- | :---
`vegas.updrift_factor` | 將演算法提高限制的量乘以一個倍數，適合有短暫流量尖峰的工作負載。預設值 `1` 符合標準 Vegas 行為。
`vegas.increase_barrier` | 要求連續數個符合條件的取樣後才提高限制，可減少震盪。
`vegas.decrease_barrier` | 要求連續數個符合條件的取樣後才降低限制，可減少震盪。丟棄會略過此障礙並立即降低限制。
`vegas.baseline_reset_load_threshold` | 防止在高負載下測得的延遲取代無負載基準。只有在作用中請求數低於目前限制的此比例時，探測才會重設基準。

### Gradient2

`gradient2` 演算法會比較短期來回時間平均值與長期平均值。當短期延遲高於長期延遲超過 `gradient2.rtt_tolerance` 時，限制器會降低限制。對於逐漸的延遲漂移，它的反應比 Vegas 更平順，適合基準延遲會隨時間變化的工作負載。

### AIMD

`aimd` 演算法採用加法增加與乘法減少。每有一個成功的取樣，限制就增加 1；每當請求遭丟棄，限制就乘以 `aimd.backoff_ratio`。此演算法簡單且可預測，但只會對請求遭丟棄作出反應，不會對延遲上升作出反應，因此最適合下游元件在飽和時會明確拒絕請求的動作。

## 暴衝容量

`burst.capacity` 設定會在調適性限制之上加入固定的餘裕量，讓短暫尖峰被吸收而非被拒絕。暴衝視窗一開始是開啟的，因此有效限制為調適性限制加上 `burst.capacity`。在連續 `burst.close_after` 個取樣中作用中請求數達到調適性限制後，視窗會關閉；而在連續 `burst.open_after` 個取樣中作用中請求數維持低於調適性限制後，視窗會重新開啟。將 `burst.capacity` 設為 `0` (預設值) 會停用暴衝。

## 分割區

將並行限制劃分為具名的子集區，讓某一類流量無法耗盡另一類可用的容量。在 `partitions` 中列出集區名稱，並使用 `partition.<name>.percent` 為每個集區指定總限制的份額。這些份額的總和最多必須為 `1.0`。不符合具名分割區的請求會路由至內建的未知集區，一旦達到整體限制，該集區一次只允許一個請求。您未分配的份額在高負載下不會提供給任何分割區使用，因此在大多數情況下，份額的總和應為 `1.0`。

分割區份額只有在限制器達到其整體限制時才會強制執行。低於整體限制時，分割區可以使用超出其份額的備用容量。一旦達到整體限制，每個分割區就會被限制在其自己的份額內。每個分割區 (包括份額為 `0.0` 的分割區) 都保證至少有一個並行請求，因此份額為 `0.0` 的分割區在高負載下一次允許一個請求，而非完全沒有。

設定 `partitions` 時，您也必須選擇一個 `partition.resolver`，將每個請求對應至分割區。下表列出可用的解析器。

解析器 | 說明
:--- | :---
`byHeader` | 讀取 `X-Request-Tier` 請求標頭，並將請求路由至名稱與標頭值完全相符的分割區。比對會區分大小寫。沒有此標頭或帶有無法辨識值的請求會前往未知集區。您無法變更標頭名稱。
`fixed` | 將每個請求路由至 `partition.resolver.fixed.partition` 中指定的單一分割區。
`bySearchType` | 將包含彙總的搜尋請求路由至 `partition.resolver.bySearchType.aggregation` 中指定的分割區，並將所有其他搜尋路由至 `partition.resolver.bySearchType.filter` 中指定的分割區。非搜尋請求會前往未知集區。

### 範例：為高階流量保留容量

下列請求會限制搜尋請求，並為帶有 `X-Request-Tier: premium` 的請求保留 70% 的限制，留下 30% 給帶有 `X-Request-Tier: standard` 的請求：

```json
PUT /_cluster/settings
{
  "persistent": {
    "concurrency_limit.action.search.action_name": "indices:data/read/search",
    "concurrency_limit.action.search.mode": "enforced",
    "concurrency_limit.action.search.partitions": ["premium", "standard"],
    "concurrency_limit.action.search.partition.resolver": "byHeader",
    "concurrency_limit.action.search.partition.premium.percent": 0.7,
    "concurrency_limit.action.search.partition.standard.percent": 0.3
  }
}
```
{% include copy-curl.html %}

用戶端接著在每個搜尋請求上設定標頭：

```bash
curl -X GET "http://localhost:9200/my-index/_search" \
  -H "X-Request-Tier: premium" \
  -H "Content-Type: application/json" \
  -d '{ "query": { "match_all": {} } }'
```
{% include copy.html %}

## 監控並行限制

若要監控每個節點上所有已設定的限制器，請向 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 請求 `concurrency_limiter` 指標：

```json
GET _nodes/stats/concurrency_limiter
```
{% include copy-curl.html %}

統計資料會顯示在回應中的 `concurrency_limiters` 鍵下。如需各項統計資料的說明，請參閱 [`concurrency_limiters`]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/#concurrency_limiters)：

```json
{
  "_nodes": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "cluster_name": "opensearch-cluster",
  "nodes": {
    "T7aqO6zaQX-lt8XBWBYLsA": {
      "timestamp": 1755530400000,
      "name": "node-1",
      "transport_address": "127.0.0.1:9300",
      "host": "127.0.0.1",
      "ip": "127.0.0.1:9300",
      "roles": [
        "cluster_manager",
        "data",
        "ingest",
        "remote_cluster_client"
      ],
      "attributes": {
        "shard_indexing_pressure_enabled": "true"
      },
      "concurrency_limiters": {
        "search": {
          "action_name": "indices:data/read/search",
          "mode": "enforced",
          "algorithm": "vegas",
          "current_limit": 42,
          "in_flight": 7,
          "total_rejected": 128,
          "last_rtt_millis": 12,
          "rtt_no_load_millis": 4
        }
      }
    }
  }
}
```

Cluster Stats API 不包含並行限制器的統計資料。
{: .note}

## 指標

[指標架構]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/metrics/getting-started/) 是一項實驗性功能，可將 OpenSearch 遙測資料匯出至外部監控後端。啟用後，每個作用中的限制器都會發布下列量測指標，其回報的值與對應統計資料的值相同。

量測指標 | 對應統計資料
:--- | :---
`concurrency_limit.current_limit` | `current_limit`
`concurrency_limit.in_flight` | `in_flight`
`concurrency_limit.total_rejected` | `total_rejected`
`concurrency_limit.last_rtt` | `last_rtt_millis`
`concurrency_limit.rtt_noload` | `rtt_no_load_millis`

每個量測指標都帶有 `action_name`、`mode` 和 `algorithm` 屬性，以及包含限制器名稱的 `alias` 屬性。
