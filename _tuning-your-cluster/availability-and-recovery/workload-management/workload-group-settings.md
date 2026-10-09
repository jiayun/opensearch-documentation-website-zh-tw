---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載群組設定"
nav_order: 30
parent: Workload management
grand_parent: Availability and recovery
---

# 工作負載群組設定
**於 3.7 版導入**
{: .label .label-purple }

OpenSearch 的運作通常由叢集層級的預設值與每個請求的參數控制。在多租用戶叢集中，您可能需要對不同的租用戶套用不同的限制。

工作負載群組設定可滿足這項需求，讓您將群組專屬的組態直接附加到[工作負載群組]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-groups/)。當請求被路由到某個群組時，該群組的設定會自動套用。這種做法提供下列優點：

- 您可以對資源密集或未經驗證的租用戶套用更嚴格的限制，同時為其他租用戶保留寬鬆的預設值，而且完全不必修改叢集設定。
- 限制會繫結到工作負載群組，因此無論是哪個用戶端送出請求，只要路由到該群組就會套用，不需要任何用戶端組態。
- 工作負載群組可以選擇性地優先於寬鬆的請求層級數值，在不完全拒絕查詢的情況下保護叢集。
- 租用戶的所有防護機制都集中在一處，與群組的 `resource_limits` 和 `resiliency_mode` 並列。

## 支援的設定

您可以在工作負載群組的 `settings` 物件中設定這些設定。所有設定皆為選用。只有您在工作負載群組上明確定義的設定才會生效；任何省略的設定都會預設為對應的請求參數或叢集預設值。每個工作負載群組設定可接受的值範圍，與其所對應的請求參數或叢集設定相同。

下表列出支援的工作負載群組設定。

| 設定 | 類型 | 說明 |
| :--- | :--- | :--- |
| `search.default_search_timeout` | 時間單位 | 分片在查詢執行上可花費的最長時間。當分片超過此逾時時間時，會停止蒐集命中結果，並將目前的結果傳回協調節點，可能因此產生部分結果。 <br><br>**對應的請求參數**：[`timeout`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#query-parameters) <br>**對應的叢集設定**：[`search.default_search_timeout`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/search-settings/) |
| `search.cancel_after_time_interval` | 時間單位 | 整個搜尋請求在協調節點層級可執行的最長時間。當達到此時間間隔時，請求與所有相關工作都會被取消，用戶端會收到錯誤而非部分結果。 <br><br>**對應的請求參數**：[`cancel_after_time_interval`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#query-parameters) <br>**對應的叢集設定**：[`search.cancel_after_time_interval`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/search-settings/) |
| `search.max_concurrent_shard_requests` | 整數 | 單一搜尋在每個節點上可發出的並行分片層級請求數上限。用於限制搜尋的扇出規模。 <br><br>**對應的請求參數**：[`max_concurrent_shard_requests`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#query-parameters) <br>**對應的叢集設定**：無 |
| `search.batched_reduce_size` | 整數 | 在最終縮減步驟之前，協調節點上合併為單一批次的分片結果數量。當搜尋橫跨許多分片時，較低的值可降低協調器的記憶體用量。 <br><br>**對應的請求參數**：[`batched_reduce_size`]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#query-parameters) <br>**對應的叢集設定**：無 |
| `search.max_buckets` | 整數 | 單一回應中允許的彙總桶數上限。可防止大型彙總造成過度的記憶體用量。 <br><br>**對應的請求參數**：無 <br>**對應的叢集設定**：[`search.max_buckets`]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/search-settings/) |
| `override_request_values` | 布林值 | 工作負載群組的設定是否優先於請求上提供的數值。預設為 `false`。請參閱[設定優先順序](#setting-precedence)。 <br><br>**對應的請求參數**：無 <br>**對應的叢集設定**：無 |

## 設定優先順序

當設定定義在工作負載群組上時，OpenSearch 會在請求時使用下列優先順序規則來解析有效值：

- 當工作負載群組設定與對應的叢集設定同時定義時，工作負載群組設定一律優先。
- 預設情況下，請求上明確提供的數值優先於工作負載群組的設定。您可以將 `override_request_values` 設為 `true` 來反轉此行為。

下表摘要說明有效值的解析方式。

| `override_request_values` 的值 | 優先順序（由高至低） |
| :--- | :--- |
| `false`（預設） | 請求參數 > 工作負載群組設定 > 叢集設定 |
| `true` | 工作負載群組設定 > 請求參數 > 叢集設定 |

## 建立包含設定的工作負載群組

在現有的工作負載群組欄位旁加入 `settings` 物件：

```json
PUT _wlm/workload_group
{
  "name": "analytics",
  "resiliency_mode": "enforced",
  "resource_limits": {
    "cpu": 0.4,
    "memory": 0.2
  },
  "settings": {
    "search.default_search_timeout": "30s",
    "search.cancel_after_time_interval": "1m",
    "search.max_concurrent_shard_requests": 5,
    "search.batched_reduce_size": 512,
    "search.max_buckets": 10000
  }
}
```
{% include copy-curl.html %}

## 更新工作負載群組設定

您可以更新個別設定，而不影響其他設定。

例如，若只要變更 `analytics` 工作負載群組的搜尋逾時時間：

```json
PUT _wlm/workload_group/analytics
{
  "settings": {
    "search.default_search_timeout": "1m"
  }
}
```
{% include copy-curl.html %}

若要移除單一設定，請將其值設為 `null`：

```json
PUT _wlm/workload_group/analytics
{
  "settings": {
    "search.batched_reduce_size": null
  }
}
```
{% include copy-curl.html %}

若要清除所有設定，請送出空的 `settings` 物件：

```json
PUT _wlm/workload_group/analytics
{
  "settings": {}
}
```
{% include copy-curl.html %}

## 擷取工作負載群組設定

若要擷取工作負載群組設定，請使用 [Workload Group API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-groups/#retrieving-a-workload-group)：

```json
GET _wlm/workload_group/analytics
```
{% include copy-curl.html %}

## 刪除工作負載群組設定

當工作負載群組被刪除時，其設定也會一併移除。若要在不刪除群組的情況下移除個別設定，請參閱[更新工作負載群組設定](#updating-workload-group-settings)。
