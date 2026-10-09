---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "熱門分片識別"
parent: Root Cause Analysis
grand_parent: Performance Analyzer
nav_order: 30
---

# 熱門分片識別

熱門分片識別根本原因分析（RCA）可讓您識別索引中的熱門分片。熱門分片是比其他分片消耗更多資源的異常分片，可能導致編製索引和搜尋效能不佳。熱門分片識別 RCA 會監視下列指標：

- CPU 使用率
- 堆積記憶體配置速率

分片可能因工作負載的性質而成為熱門分片。當您使用 `_routing` 參數或自訂文件 ID 時，叢集中的特定分片或多個分片會頻繁收到更新，消耗比其他分片更多的 CPU 和堆積記憶體資源。

熱門分片識別 RCA 會將 CPU 使用率和堆積記憶體配置速率與其閾值比較。如果任一指標的使用量大於閾值，該分片就會被視為 _熱門_。

如需熱門分片識別 RCA 實作的詳細資訊，請參閱[熱門分片 RCA](https://github.com/opensearch-project/performance-analyzer-rca/blob/main/src/main/java/org/opensearch/performanceanalyzer/rca/store/rca/hotshard/docs/README.md)。

#### 請求範例

下列查詢會請求識別熱門分片：

```bash
GET _plugins/_performanceanalyzer/rca?name=HotShardClusterRca
```
{% include copy-curl.html %}

#### 回應範例

回應包含狀況不良的分片清單：

```json
"HotShardClusterRca": [{
  "rca_name": "HotShardClusterRca",
  "timestamp": 1680721367563,
  "state": "unhealthy",
  "HotClusterSummary": [
    {
      "number_of_nodes": 3,
      "number_of_unhealthy_nodes": 1,
      "HotNodeSummary": [
        {
          "node_id": "7kosAbpASsqBoHmHkVXxmw",
          "host_address": "192.168.80.4",
          "HotResourceSummary": [
            {
              "resource_type": "cpu usage",
              "resource_metric": "cpu usage(num of cores)",
              "threshold": 0.027397981341796683,
              "value": 0.034449630200405396,
              "time_period_seconds": 60,
              "meta_data": "ssZw1WRUSHS5DZCW73BOJQ index9 4"
            },
            {
              "resource_type": "heap",
              "resource_metric": "heap alloc rate(heap alloc rate in bytes per second)",
              "threshold": 7605441.367010161,
              "value": 10872119.748328414,
              "time_period_seconds": 60,
              "meta_data": "ssZw1WRUSHS5DZCW73BOJQ index9 4"
            },
            {
              "resource_type": "heap",
              "resource_metric": "heap alloc rate(heap alloc rate in bytes per second)",
              "threshold": 7605441.367010161,
              "value": 8019622.354388569,
              "time_period_seconds": 60,
              "meta_data": "QRF4rBM7SNCDr1g3KU6HyA index9 0"
            }
          ]
        }
      ]
    }
  ]
}]
```

## 回應本文欄位

下表列出回應欄位。

欄位 | 類型 | 說明
:--- | :--- | :---
`rca_name` | 字串 | RCA 的名稱。在此案例中為「HotShardClusterRca」。
`timestamp` | 整數 | RCA 的時間戳記。
`state` | 物件 | RCA 判定的叢集狀態。`state` 可以是 `healthy`、`unhealthy` 或 `unknown`。
`HotClusterSummary.HotNodeSummary.number_of_nodes` | 整數 | 叢集中的節點數量。
`HotClusterSummary.HotNodeSummary.number_of_unhealthy_nodes` | 整數 | 發現處於 `unhealthy` 狀態的節點數量。
`HotClusterSummary.HotNodeSummary.HotResourceSummary.resource_type` | 物件 | 導致狀況不良的資源類型，為 `cpu usage` 或 `heap`。
`HotClusterSummary.HotNodeSummary.HotResourceSummary.resource_metric` | 字串 | `resource_type` 的定義。為 `cpu usage(num of cores)` 或 `heap alloc rate(heap alloc rate in bytes per second)`。
`HotClusterSummary.HotNodeSummary.HotResourceSummary.threshold` | 浮點數 | 用於判定資源是否發生競爭的值。
`HotClusterSummary.HotNodeSummary.HotResourceSummary.value` | 浮點數 | 資源的目前值。
`HotClusterSummary.HotNodeSummary.HotResourceSummary.time_period_seconds` | 時間 | 分片在被判定為狀況良好或不良之前，受監視的時間長度。
`HotClusterSummary.HotNodeSummary.HotResourceSummary.meta_data` | 字串 | 與 resource_type 相關聯的中繼資料。

在上述回應範例中，`meta_data` 為 `QRF4rBM7SNCDr1g3KU6HyA index9 0`。`meta_data` 字串由三個欄位組成：

- 節點名稱：`QRF4rBM7SNCDr1g3KU6HyA`
- 索引名稱：`index9`
- 分片 ID：`0`

這表示節點 `QRF4rBM7SNCDr1g3KU6HyA` 上索引 `index9` 的分片 `0` 是熱門分片。