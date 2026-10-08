---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢面板"
parent: Creating visualizations using queries
grand_parent: Building data visualizations
nav_order: 91
---

# 查詢面板

使用查詢面板選擇查詢語言和資料集、撰寫或建構查詢，然後執行查詢以產生視覺化所需的資料。

查詢面板支援 Piped Processing Language (PPL)、Prometheus Query Language (PromQL)，以及在啟用時支援 SQL。若要啟用 SQL，請將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

```yaml
explore.sqlSupport.enabled: true
```
{% include copy.html %}

當所選資料集啟用提示模式時，即可使用 AI 查詢產生功能。

## 查詢面板控制項

查詢面板包含下列控制項。

| 控制項 | 說明 |
| --- | --- |
| **Language toggle** | 在 PPL、PromQL、SQL 和 AI 選項可用時，於這些選項之間切換編輯器。 |
| **Dataset selector** | 選取編輯器要查詢的資料集或資料來源。可用的資料集取決於所選的語言。 |
| **Saved queries** | 儲存目前的查詢，或載入先前儲存的查詢。 |
| **Query editor** | 提供文字編輯器；選取 PromQL 時，則提供 PromQL 編輯器或建構器。 |

下圖顯示查詢面板，其中包含語言切換、資料集選取器、已儲存查詢選單和查詢編輯器。

![顯示語言切換、資料集選取器、已儲存查詢選單和查詢編輯器的查詢面板]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/query-panel.png){: width="100%" }

## 選取查詢語言

使用語言切換選取查詢語言。所選的語言決定可用的資料集，以及顯示哪些編輯器功能。

| 語言 | 說明 |
| --- | --- |
| **PPL** | 使用 Piped Processing Language 查詢 OpenSearch 資料集。 |
| **PromQL** | 查詢 Prometheus 資料來源，並顯示 PromQL 多重查詢編輯器。 |
| **SQL** | 使用 SQL 查詢 OpenSearch 資料集。只有在 `explore.sqlSupport.enabled` 設為 `true` 時，才會顯示此選項。 |
| **AI** | 從自然語言提示產生查詢。只有在提示模式可用時，才會顯示此選項。 |

## 選取資料集

使用資料集選取器選擇視覺化編輯器要查詢的資料。資料集是否可用取決於所選的查詢語言：

- **PPL** 和 **SQL** 使用 OpenSearch 資料集，例如索引和索引模式。
- **PromQL** 使用 Prometheus 資料集。

## 撰寫 PPL 查詢

選取資料集之後，您可以撰寫 PPL 查詢。視覺化編輯器會使用所選的資料集作為查詢來源。

例如，若選取了 `opensearch_dashboards_sample_data_logs`，您可以輸入下列查詢：

```sql
| stats count() by response
```
{% include copy.html %}

您也可以明確指定來源：

```sql
source = opensearch_dashboards_sample_data_logs | stats count() by response
```
{% include copy.html %}

## 撰寫 PromQL 查詢

選取 **PromQL** 時，編輯器會顯示多重查詢編輯器。每個查詢列都可以在 **Builder** 模式或 **Code** 模式下撰寫。

下圖顯示 PromQL 多重查詢編輯器。

![PromQL 多重查詢編輯器，其中有一個處於 Builder 模式的查詢列]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/promql-panel.png)

使用 **Builder** 模式，以指標名稱、標籤篩選條件和運算建構 PromQL 查詢。使用 **Code** 模式直接撰寫 PromQL。部分程式碼查詢無法以 **Builder** 模式呈現，因此對於複雜的查詢，可能無法切換回 **Builder** 模式。

下列範例使用 **Builder** 模式撰寫 PromQL 查詢：

```prometheus
sum(rate(go_gc_heap_allocs_bytes_total[50060s]))
```
{% include copy.html %}

下圖顯示在 **Builder** 模式中，以 `sum` 彙總、具有 `50060s` 時間範圍的 `rate` 函式，以及 `go_gc_heap_allocs_bytes_total` 指標所建構的相同查詢。

![在 Builder 模式中以 sum 彙總、rate 函式和指標名稱建構的 PromQL 查詢，產生的查詢顯示在控制項下方]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/promql-builder-case.png){: width="100%" }

您可以依下列方式管理 PromQL 查詢列：

- 選取 **Add query** 以新增另一個 PromQL 查詢列。
- 選取移除圖示以刪除查詢列。
- 拖曳查詢列以重新排序。
- 選取 **Update** 以執行查詢。在 **Code** 模式中，您也可以按 Command+Enter (macOS) 或 Ctrl+Enter (Windows 和 Linux)。

## PromQL 查詢選項

PromQL 為每個查詢列提供個別查詢選項，並為所有查詢列提供共用選項。若要設定單一查詢列的選項，請選取該列末端的齒輪圖示。若要設定所有查詢列共用的選項，請選取 **Query options**。

下圖顯示 PromQL 查詢列的個別查詢選項。

![PromQL 查詢列的個別查詢選項，包括 Series name 和 Min step，以及估計的步長和速率時間範圍]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/per-query-option.png){: width="100%" }

### 序列名稱

使用 **Series name** 自訂顯示的序列名稱。您可以使用雙大括號參照指標標籤。

例如，輸入 {% raw %}`{{job}}`{% endraw %} 以依 job 標籤為每個序列命名，或輸入 {% raw %}`{{job}}-{{instance}}`{% endraw %} 以組合多個標籤。

下列長條圖將 **Series name** 設為 {% raw %}`{{operation}}`{% endraw %}，因此圖例會依 operation 標籤為每個序列命名，即 `Read` 和 `Write`。

![長條圖的圖例依 operation 標籤 Read 和 Write 為每個序列命名，並在查詢列中設定 Series name 選項]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/series-name-operation.png)

### 最小步長

使用 **Min step** 設定 PromQL 查詢步長的下限。請輸入含單位的持續時間，例如 `15s`、`1m` 或 `2h`。請將此值設為與您的 Prometheus 擷取間隔相符。選項面板會以估計值顯示產生的步長 (`$__interval`) 和速率時間範圍 (`$__rate_interval`)；請執行查詢以確認這些值。

### 資料點數量上限

使用 **Max data points** 設定每個序列傳回的資料點數量上限。此選項由所有 PromQL 查詢列共用。將此設定留空即可使用自動值。

下圖顯示共用 **Query options** 面板中的 **Max data points**，其自動值為 `1440`。

![在共用 Query options 面板中，Max data points 設為自動值 1440]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/max-point.png)

## 儲存並重複使用查詢

若要儲存查詢以便重複使用，請選取 **Saved queries** > **Save query**。若要載入已儲存的查詢，請選取 **Saved queries** > **Open query**，然後選擇要載入的查詢。

下圖顯示 **Saved queries** 選單，其中包含 **Save query** 和 **Open query** 選項。

![展開的 Saved queries 選單，顯示 Save query 和 Open query 選項]({{site.url}}{{site.baseurl}}/images/dashboards/visualization-editor/query-panel/open-saved-query.png){: width="60%" }
