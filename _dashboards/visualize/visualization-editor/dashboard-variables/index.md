---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "儀表板變數"
has_children: true
has_toc: false
nav_order: 100
parent: Creating visualizations using queries
grand_parent: Building data visualizations
redirect_from:
  - /dashboards/visualize/visualization-editor/dashboard-variables/
---

# 儀表板變數
**3.7 版推出**
{: .label .label-purple }

儀表板變數是可重複使用的值，您可以在[視覺化編輯器]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/)的查詢中參照這些變數。您可以將變數用於篩選條件、指標、維度、間隔、欄位、彙總及任何其他查詢參數，在不同資料檢視之間切換時，無需手動編輯 PPL 或 PromQL 查詢。

儀表板變數僅適用於 **Observability** 工作區。若要使用儀表板變數，請先建立 Observability 工作區（如果您還沒有）。如需詳細資訊，請參閱 [OpenSearch Dashboards 的工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)。
{: .note}

使用儀表板變數可以：

- 變更查詢參數，而無需編輯視覺化。
- 只需定義一次值，即可在多個視覺化中參照。
- 在變數值變更時自動更新視覺化。
- 使用相依變數建立串聯篩選條件。
- 動態控制分組、彙總和時間間隔。

## 變數類型

OpenSearch Dashboards 支援兩種變數類型：

- **查詢變數**：選項是使用 Piped Processing Language (PPL) 或 Prometheus Query Language (PromQL) 查詢，從資料來源動態擷取而來。當值會隨時間變化或取決於基礎資料時，請使用查詢變數，例如記錄檔中的服務名稱或指標中的可用區域。

- **自訂變數**：選項以靜態清單的形式手動定義。針對預先定義的類別，例如環境類型（`dev`、`staging`、`prod`）或固定的狀態碼，請使用自訂變數。

## 變數語法

您可以使用 `$variableName` 或 `${variableName}` 語法在查詢中參照變數：

```sql
source=logs | where service='${service}' | stats count() by region
```
{% include copy.html %}

當您在儀表板中變更變數的值時，所有參照該變數的視覺化都會自動使用新值重新整理。

## 啟用儀表板變數

除了[啟用工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/#enabling-workspaces)之外，請將下列設定新增至您的 `opensearch_dashboards.yml` 檔案：

```yaml
explore.enabled: true
```
{% include copy.html %}

重新啟動 OpenSearch Dashboards，變更才會生效。

## 建立和使用儀表板變數

下列教學使用 OpenSearch Dashboards 的範例 Web 記錄資料集來建立變數，並在視覺化中使用該變數。

### 步驟 1：建立工作區

1. 前往 OpenSearch Dashboards 首頁。
1. 選取 **Create workspace**。
1. 輸入工作區名稱（例如 `My Observability`）。
1. 在 **Use case** 下方，選取 **Observability**。
1. 選取 **Create workspace**。

如需詳細資訊，請參閱[建立工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/create-workspace/)。

### 步驟 2：設定範例資料

1. 在工作區中，前往 **Manage workspace** > **Sample data**，並為 Web 記錄資料集選取 **Add data**。
1. 為範例資料建立索引模式：
   1. 前往 **Manage workspace** > **Index patterns**。
   1. 選取 **Create index pattern**。
   1. 在 **Index pattern name** 欄位中，輸入 `opensearch_dashboards_sample_data_logs`。
   1. 選取 **Next step**。
   1. 在 **Time field** 下拉式選單中，選取 `timestamp`。
   1. 選取 **Create index pattern**。

### 步驟 3：建立變數

1. 在左側導覽中選取 **Dashboards**。
1. 選取 **Create** > **Dashboard**。
1. 輸入標題（例如 `Log Analysis`）並選取 **Save** 以儲存儀表板。
1. 在儀表板頂端，選取 **Add variable**。
1. 設定下列設定：
   - **Name**：`extension`
   - **Type**：**Query**
   - **Dataset**：選取 `opensearch_dashboards_sample_data_logs`
   - **Options Query**：

     ```sql
     source=opensearch_dashboards_sample_data_logs | stats count() by extension | fields extension
     ```
     {% include copy.html %}

1. 選取 **Preview** 以驗證結果。預覽應顯示下列值：`css`、`deb`、`gz`、`rpm` 和 `zip`。
1. 選取 **Add variable** 以儲存。

`extension` 變數現在會顯示在儀表板頂端，並附有一個下拉式選單。

如需詳細資訊，請參閱[管理儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/managing-variables/)。

### 步驟 4：在視覺化中使用變數

1. 在儀表板中，選取 **Create new**。
1. 選取 **Add visualization** 以開啟視覺化編輯器。
1. 在查詢編輯器中，輸入下列參照 `$extension` 變數的 PPL 查詢：

   ```sql
   | where extension='$extension' | stats count() by response
   ```
   {% include copy.html %}

1. 在編輯器頂端的 `extension` 下拉式選單中，選取一個值（例如 `css`）。
1. 選取 **Update** 以執行查詢。

視覺化會顯示依所選副檔名篩選的回應碼分布，如下圖所示。

![視覺化編輯器顯示依所選副檔名值篩選的回應碼長條圖]({{site.url}}{{site.baseurl}}/images/dashboard-variables/variable-visualization-result.png)

當您在下拉式選單中變更 `extension` 值時，視覺化會自動更新以反映新的選擇。

如果沒有顯示任何結果，請使用右上角的[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)擴大時間範圍（例如 **Last 90 days**）。
{: .tip}

如需詳細資訊，請參閱[使用儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/using-variables/)。

## 變數儲存

變數會儲存為 OpenSearch 中儀表板已儲存物件的一部分。每個儀表板都會各自獨立維護自己的一組變數。

儀表板已儲存物件中的 `variablesJSON` 屬性包含變數組態：

```typescript
{
  type: "dashboard",
  id: "dashboard-id",
  attributes: {
    title: "My Dashboard",
    variablesJSON: "{\"variables\":[...]}"
  }
}
```
{% include copy.html %}

變數組態包含下列元件：

- 中繼資料（名稱、標籤、描述、類型）。
- 選項（查詢類型的查詢定義，或自訂類型的自訂值）。
- 設定（多重選取、「All」選項、排序順序、可見性）。
- 目前的值（每個變數所選取的值）。

目前的變數值也會同步至儀表板 URL，讓您可以：

- 分享已預先選取特定篩選值的儀表板。
- 將具有所需變數狀態的儀表板加入書籤。
- 在重新整理頁面後保留變數選擇。

## 相關文件

- [管理儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/managing-variables/)
- [使用儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/using-variables/)
- [使用查詢建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/)
- [OpenSearch Dashboards 的工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)