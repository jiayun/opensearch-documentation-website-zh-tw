---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Query Insights Settings API
parent: Query insights
nav_order: 25
---

# Query Insights Settings API
**3.5 版引入**
{: .label .label-purple }

Query Insights Settings API 可讓您透過專用端點管理查詢洞察組態。使用此 API 可設定前 N 名查詢監控、分組與匯出器設定，並具備細緻的設定層級存取控制。

此 API 在功能上等同於用於查詢洞察組態的 [Cluster Settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)。在正式環境中，您可以使用專用權限 `cluster:admin/opensearch/insights/settings/*` 僅授予效能工程師或監控團隊查詢洞察設定的存取權，而不會暴露所有叢集設定。
{: .note}

此 API 提供下列端點：

- [擷取設定](#retrieve-query-insights-settings)
- [更新設定](#update-query-insights-settings)

## 擷取查詢洞察設定

擷取所有查詢洞察設定，包括延遲、CPU、記憶體、分組與匯出器組態。

### 端點

```json
GET /_insights/settings
GET /_insights/settings/{metric_type}
```

### 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `metric_type` | 字串 | 要擷取設定的特定指標類型。有效值為 `latency`、`cpu` 與 `memory`。若省略，則傳回所有指標的設定。 |

### 範例請求

```json
GET /_insights/settings/
```
{% include copy-curl.html %}

### 範例回應

```json
{
  "persistent": {
    "latency": {
      "enabled": true,
      "top_n_size": 10,
      "window_size": "5m"
    },
    "cpu": {
      "enabled": true,
      "top_n_size": 10,
      "window_size": "5m"
    },
    "memory": {
      "enabled": true,
      "top_n_size": 10,
      "window_size": "5m"
    },
    "grouping": {
      "group_by": "none"
    },
    "exporter": {
      "type": "local_index",
      "delete_after_days": 7
    }
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `persistent` | 物件 | 包含查詢洞察的持久性叢集設定。 |
| `persistent.latency` | 物件 | 延遲指標組態設定。 |
| `persistent.latency.enabled` | 布林值 | 是否啟用延遲的前 N 名查詢監控。 |
| `persistent.latency.top_n_size` | 整數 | 延遲正在追蹤的前幾名查詢數量。 |
| `persistent.latency.window_size` | 字串 | 收集前幾名延遲查詢的時間視窗。 |
| `persistent.cpu` | 物件 | CPU 指標組態設定。 |
| `persistent.cpu.enabled` | 布林值 | 是否啟用 CPU 的前 N 名查詢監控。 |
| `persistent.cpu.top_n_size` | 整數 | CPU 正在追蹤的前幾名查詢數量。 |
| `persistent.cpu.window_size` | 字串 | 收集前幾名 CPU 查詢的時間視窗。 |
| `persistent.memory` | 物件 | 記憶體指標組態設定。 |
| `persistent.memory.enabled` | 布林值 | 是否啟用記憶體的前 N 名查詢監控。 |
| `persistent.memory.top_n_size` | 整數 | 記憶體正在追蹤的前幾名查詢數量。 |
| `persistent.memory.window_size` | 字串 | 收集前幾名記憶體查詢的時間視窗。 |
| `persistent.grouping` | 物件 | 查詢分組組態設定。 |
| `persistent.grouping.group_by` | 字串 | 對相似查詢進行分組的方法。 |
| `persistent.exporter` | 物件 | 匯出器組態設定。 |
| `persistent.exporter.type` | 字串 | 前 N 名查詢資料的匯出器類型。 |
| `persistent.exporter.delete_after_days` | 整數 | 使用 `local_index` 匯出器時，本機索引資料的保留天數。 |

## 更新查詢洞察設定

更新查詢洞察設定。您可以在單一請求中更新一或多個指標的設定。

### 端點

```json
PUT /_insights/settings
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `latency` | 物件 | 延遲指標組態。選用。 |
| `latency.enabled` | 布林值 | 啟用或停用延遲的前 N 名查詢監控。選用。預設為 `true`。 |
| `latency.top_n_size` | 整數 | 延遲要追蹤的前幾名查詢數量。有效值為 1–100。選用。預設為 `10`。 |
| `latency.window_size` | 字串 | 收集前幾名延遲查詢的時間視窗。有效值：`1m`、`5m`、`10m`、`30m`、`1h`。選用。預設為 `5m`。 |
| `cpu` | 物件 | CPU 指標組態。選用。 |
| `cpu.enabled` | 布林值 | 啟用或停用 CPU 的前 N 名查詢監控。選用。預設為 `false`。 |
| `cpu.top_n_size` | 整數 | CPU 要追蹤的前幾名查詢數量。有效值為 1–100。選用。預設為 `10`。 |
| `cpu.window_size` | 字串 | 收集前幾名 CPU 查詢的時間視窗。有效值：`1m`、`5m`、`10m`、`30m`、`1h`。選用。預設為 `5m`。 |
| `memory` | 物件 | 記憶體指標組態。選用。 |
| `memory.enabled` | 布林值 | 啟用或停用記憶體的前 N 名查詢監控。選用。預設為 `false`。 |
| `memory.top_n_size` | 整數 | 記憶體要追蹤的前幾名查詢數量。有效值為 1–100。選用。預設為 `10`。 |
| `memory.window_size` | 字串 | 收集前幾名記憶體查詢的時間視窗。有效值：`1m`、`5m`、`10m`、`30m`、`1h`。選用。預設為 `5m`。 |
| `grouping` | 物件 | 查詢分組組態。選用。 |
| `grouping.group_by` | 字串 | 對相似查詢進行分組的方法。有效值為 `similarity` 與 `none`。選用。預設為 `none`。 |
| `exporter` | 物件 | 匯出器組態。選用。 |
| `exporter.type` | 字串 | 前 N 名查詢資料的匯出器類型。有效值為 `local_index` 與 `debug`。選用。預設為 `local_index`。 |
| `exporter.delete_after_days` | 整數 | 本機索引資料的保留天數 (1–180)。僅在 `type` 為 `local_index` 時適用。選用。預設為 `7`。 |

如需指標設定的詳細資訊，請參閱 [前 N 名查詢]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/#configuring-top-n-query-monitoring)。

如需查詢分組的詳細資訊，請參閱 [前 N 名查詢分組]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/grouping-top-n-queries/)。

如需匯出器的詳細資訊，請參閱 [匯出前 N 名查詢資料]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/#exporting-top-n-query-data)。

### 範例請求：更新延遲設定

```json
PUT /_insights/settings
{
  "latency": {
    "enabled": true,
    "top_n_size": 20,
    "window_size": "10m"
  }
}
```
{% include copy-curl.html %}

### 範例請求：更新多個指標設定

```json
PUT /_insights/settings
{
  "latency": {
    "enabled": true,
    "top_n_size": 15
  },
  "cpu": {
    "enabled": true,
    "top_n_size": 10,
    "window_size": "10m"
  },
  "memory": {
    "enabled": false
  }
}
```
{% include copy-curl.html %}

### 範例請求：更新分組設定

```json
PUT /_insights/settings
{
  "grouping": {
    "group_by": "similarity"
  }
}
```
{% include copy-curl.html %}

### 範例請求：更新匯出器設定

```json
PUT /_insights/settings
{
  "exporter": {
    "type": "local_index",
    "delete_after_days": 7
  }
}
```
{% include copy-curl.html %}

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：

- GET 請求需要 `cluster:admin/opensearch/insights/settings/get`
- PUT 請求需要 `cluster:admin/opensearch/insights/settings/update`
- 所有查詢洞察設定 API 操作需要 `cluster:admin/opensearch/insights/settings/*`

您可以在 Security 外掛程式或存取控制系統中設定這些權限。

對於正式環境部署，建議建立僅能存取這些端點的專用角色，而不是授予完整的叢集設定權限。

## 相關文件

- [前 N 名查詢]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/top-n-queries/)
- [前 N 名查詢分組]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/grouping-top-n-queries/)
- [查詢洞察儀表板]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/query-insights-dashboard/)
- [Cluster settings API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)
