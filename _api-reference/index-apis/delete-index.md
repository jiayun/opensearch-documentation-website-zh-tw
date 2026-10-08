---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除索引"
parent: Core index APIs
grand_parent: Index APIs
nav_order: 20
redirect_from:
  - /opensearch/rest-api/index-apis/delete-index/
---

# Delete Index API
**於 1.0 版推出**
{: .label .label-purple }

刪除索引 API 作業會從您的叢集中刪除一或多個索引。

**警告**：刪除索引是永久性作業。索引中的所有資料都會遺失，且無法復原。刪除索引之前，請務必確認您已有備份，或已不再需要這些資料。
{: .warning}

<!-- spec_insert_start
api: indices.delete
component: endpoints
-->
## 端點
```json
DELETE /{index}
```
<!-- spec_insert_end -->

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 要刪除的索引名稱。您可以指定單一索引名稱、以逗號分隔的索引名稱清單，或萬用字元運算式。萬用字元運算式（`*`）只會比對開啟的實體索引。您無法使用別名刪除索引。若要刪除所有索引，請使用 `_all` 或 `*`。若要避免使用 `_all` 或萬用字元運算式意外刪除所有索引，請將 `action.destructive_requires_name` 叢集設定設為 `true`。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 | 預設 |
| :--- | :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 指定是否忽略未比對到任何索引的萬用字元。若為 `false`，當萬用字元未比對到任何索引時，請求會傳回錯誤。 | `true` |
| `expand_wildcards` | 字串 | 指定萬用字元運算式可展開為哪些類型的索引。支援以逗號分隔的值。有效值為：<br> - `all`：比對所有索引，包括隱藏索引。<br> - `open`：比對開啟的索引。<br> - `closed`：比對關閉的索引。<br> - `hidden`：比對隱藏索引。必須與 `open`、`closed` 或兩者搭配使用。<br> - `none`：不接受萬用字元運算式。 | `open` |
| `ignore_unavailable` | 布林值 | 指定是否忽略無法使用的索引（不存在或已關閉）。若為 `true`，回應中不會包含不存在或已關閉的索引。 | `false` |
| `cluster_manager_timeout` | 字串 | 等待連線至叢集管理員節點的時間長度。 | `30s` |
| `timeout` | 字串 | 等待回應的時間長度。若在逾時期限到期前未收到回應，請求會失敗並傳回錯誤。 | `30s` |

## 範例：刪除單一索引

下列範例請求會刪除名為 `sample-index` 的單一索引：

<!-- spec_insert_start
component: example_code
rest: DELETE /sample-index
-->
{% capture step1_rest %}
DELETE /sample-index
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete(
  index = "sample-index"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：刪除多個索引

下列範例請求會透過以逗號分隔的清單指定多個索引，以將其刪除：

<!-- spec_insert_start
component: example_code
rest: DELETE /logs-2024-01,logs-2024-02,logs-2024-03
-->
{% capture step1_rest %}
DELETE /logs-2024-01,logs-2024-02,logs-2024-03
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete(
  index = "logs-2024-01,logs-2024-02,logs-2024-03"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：使用萬用字元模式刪除索引

下列範例請求會刪除所有符合模式 `logs-2024-*` 的索引：

<!-- spec_insert_start
component: example_code
rest: DELETE /logs-2024-*
-->
{% capture step1_rest %}
DELETE /logs-2024-*
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete(
  index = "logs-2024-*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 範例：刪除所有索引

**警告**：下列作業具有極大的破壞性，會刪除您叢集中的所有索引。請極為謹慎地使用，且僅限於開發或測試環境。
{: .warning}

下列範例請求會刪除叢集中的所有索引：

<!-- spec_insert_start
component: example_code
rest: DELETE /*
-->
{% capture step1_rest %}
DELETE /*
{% endcapture %}

{% capture step1_python %}


response = client.indices.delete(
  index = "*"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要避免意外刪除所有索引，您可以將 `action.destructive_requires_name` 叢集設定設為 `true`。啟用此設定後，您必須明確指定索引名稱，且無法使用 `_all` 或萬用字元模式刪除所有索引。如需詳細資訊，請參閱[索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/)。

## 回應範例

刪除作業成功時，OpenSearch 會傳回下列回應：

```json
{
  "acknowledged": true
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`acknowledged` | 布林值 | 表示叢集是否已收到刪除請求。值為 `true` 表示索引已成功刪除。

## 必要權限

若您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/delete`。
