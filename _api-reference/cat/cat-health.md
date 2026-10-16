---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: CAT health
parent: CAT APIs
nav_order: 20
has_children: false
redirect_from:
- /opensearch/rest-api/cat/cat-health/
---

# CAT Health API
**於 1.0 版導入**
{: .label .label-purple }

CAT health 操作會列出叢集的狀態、叢集已啟動多久、節點數量，以及其他有助於分析叢集健康狀態的實用資訊。它以緊湊的單行格式傳回與 [Cluster Health API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-health/) 相同的資訊。

每個回應行都以兩個時間戳開頭：`epoch` 是自 Unix 紀元起算的秒數，`timestamp` 是以 `HH:MM:SS` 格式表示的當日時間。`epoch` 值包含日期，因此可用於排序或比較跨數天收集的結果。若要省略這兩個時間戳，請將 `ts` 設為 `false`。

由於每次呼叫只傳回一行，CAT Health API 適合用於長期監控叢集，例如在叢集重新啟動後復原的過程中。下列命令每 60 秒檢查一次叢集健康狀態：

```bash
while true; do curl -s "localhost:9200/_cat/health?h=epoch,timestamp,status,init,unassign"; sleep 60; done
```
{% include copy.html %}

隨著復原進行，叢集狀態會從 `red` 變為 `yellow` 再變為 `green`，未指派分片的數量（`unassign`）也會減少。如果 `unassign` 在多次檢查中維持不變，請使用 [Cluster Allocation Explain API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-allocation/) 找出分片未被指派的原因。


<!-- spec_insert_start
api: cat.health
component: endpoints
-->
## 端點
```json
GET /_cat/health
```
<!-- spec_insert_end -->


<!-- spec_insert_start
api: cat.health
component: query_parameters
columns: Parameter, Data type, Description, Default
include_deprecated: false
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `format` | 字串 | `Accept` 標頭的簡短版本，例如 `json` 或 `yaml`。 | N/A |
| `h` | 清單 | 以逗號分隔的欄位名稱清單，用於指定要顯示的欄位。 | N/A |
| `help` | 布林值 | 傳回說明資訊。 | `false` |
| `s` | 清單 | 以逗號分隔的欄位名稱或欄位別名清單，用於排序。 | N/A |
| `time` | 字串 | 用於顯示時間值的單位。<br> 有效值為：`nanos`、`micros`、`ms`、`s`、`m`、`h` 與 `d`。 | N/A |
| `ts` | 布林值 | 設為 `true` 時，傳回 `HH:MM:SS` 與 Unix 紀元時間戳記。 | `true` |
| `v` | 布林值 | 啟用詳細模式，以顯示欄位標題。 | `false` |

<!-- spec_insert_end -->

## 範例請求

下列範例請求會提供過去 5 天的叢集健康狀態資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_cat/health?v&time=5d
-->
{% capture step1_rest %}
GET /_cat/health?v&time=5d
{% endcapture %}

{% capture step1_python %}


response = client.cat.health(
  params = { "v": "true", "time": "5d" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例回應

```json
GET _cat/health?v&time=5d

epoch | timestamp | cluster | status | node.total | node.data | shards | pri | relo | init | unassign | pending_tasks | max_task_wait_time | active_shards_percent
1624248112 | 04:01:52 | odfe-cluster | green | 2 | 2 | 16 | 8 | 0 | 0 | 0 | 0 | - | 100.0%
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:monitor/health`。
