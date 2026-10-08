---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理儀表板變數"
parent: Dashboard variables
grand_parent: Creating visualizations using queries
great_grand_parent: Building data visualizations
nav_order: 10
---

# 管理儀表板變數

您可以在儀表板中建立、編輯、刪除、整理及檢視儀表板變數。

## 前置條件

在開始之前，請確保您已滿足下列前置條件：

- 您的 `opensearch_dashboards.yml` 檔案中已[啟用]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/#enabling-dashboard-variables)儀表板變數。
- 您已設定[Observability 工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/create-workspace/)。

如需完整的設定步驟，請參閱[建立與使用儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/#creating-and-using-dashboard-variables)。

## 建立查詢變數

當可用值清單是從資料來源擷取時，請使用查詢變數。例如，您可以從範例 Web 記錄資料建立 `extension` 變數，並使用該變數依副檔名篩選多個視覺化。

下列範例使用 OpenSearch Dashboards 範例 Web 記錄資料。如果您使用不同的資料集，請選取符合您資料的資料集和欄位。
{: .note}

若要建立查詢變數，請依照下列步驟操作：

1. 在您的 Observability 工作區中，於左側導覽列選取 **Dashboards**。
1. 開啟現有的儀表板，或選取 **Create** > **Dashboard** 以建立新的儀表板。如果您建立新的儀表板，請先輸入標題並選取 **Save** 以儲存。
1. 在儀表板頂端，選取 **Add variable**。
1. 設定下列一般設定：
   - **Name**：輸入 `extension`。這是在查詢中參照變數時使用的識別碼，例如 `$extension` 或 `${extension}`。
   - **Label**：輸入 `Extension`。這是顯示在儀表板頂端的顯示名稱。
   - **Description**：選用，輸入描述，例如 `Filters visualizations by file extension`。
   - **Type**：選取 **Query**。
1. 在 **Options Query** 中，將語言保持設定為 **PPL**。
1. 在資料集選取器中，選取 `opensearch_dashboards_sample_data_logs`。
1. 輸入下列查詢：

   ```sql
   source = opensearch_dashboards_sample_data_logs | stats count() by extension | fields extension
   ```
   {% include copy.html %}

1. 選取 **Preview**。預覽會執行查詢、載入查詢傳回的欄位，並顯示前 100 個變數選項。您必須先成功預覽查詢變數，才能儲存該變數。
1. 在 **Value field** 中，選取 `extension`。當您使用 `$extension` 或 `${extension}` 時，value field 會提供插入查詢中的值。
1. 在 **Label field** 中，保持 **None**。僅在查詢傳回另一個欄位以取代儲存值並顯示在下拉式清單中時，才選取 label field。
1. 選用：在 **Regex** 中，輸入正規表示式以依值篩選可用選項。例如，`^(css|gz|zip)$` 僅顯示 `css`、`gz` 和 `zip` 選項。
1. 在 **Refresh** 中，選擇 OpenSearch Dashboards 更新變數選項的時間點：
   - **On dashboard load**：在儀表板載入時重新整理選項。
   - **On time range change**：在儀表板時間範圍變更時重新整理選項。當可用值取決於選定的時間範圍時，請使用此選項。
1. 設定共用選項設定。如需更多資訊，請參閱[設定變數選項設定](#configuring-variable-option-settings)。
1. 選取 **Add variable**。

該變數會出現在儀表板頂端。下列圖片顯示使用範例 Web 記錄資料設定的 `extension` 查詢變數。

![使用範例 Web 記錄資料設定副檔名查詢變數的變數編輯面板]({{site.url}}{{site.baseurl}}/images/dashboard-variables/query-variable-config.png){: width="500" }

### 對應查詢結果欄位

查詢變數可以使用一個欄位作為儲存值，另一個欄位作為顯示標籤：

- **Value field**：用作變數值的欄位。當您參照變數時，OpenSearch Dashboards 會將此值插入查詢中。
- **Label field**：選用，用作變數下拉式清單中顯示標籤的欄位。標籤不會改變插入查詢中的值。

例如，如果您的查詢傳回 `service_id` 和 `service_name`，請將 **Value field** 設定為 `service_id`，並將 **Label field** 設定為 `service_name`。下拉式清單會顯示服務名稱，而查詢則會接收服務 ID。

如果您沒有選取 value field，OpenSearch Dashboards 會使用查詢傳回的第一個欄位。為了避免出現非預期的值，請預覽查詢並明確選取要用作變數值的欄位。
{: .tip}

## 建立自訂變數

當可用值清單是固定的且不需要從資料來源擷取時，請使用自訂變數。例如，您可以建立一個包含 `dev`、`staging` 和 `prod` 選項的 `environment` 變數。

若要建立自訂變數，請依照下列步驟操作：

1. 在您的 Observability 工作區中，於左側導覽列選取 **Dashboards**。
1. 開啟現有的儀表板，或選取 **Create** > **Dashboard** 以建立新的儀表板。如果您建立新的儀表板，請先輸入標題並選取 **Save** 以儲存。
1. 在儀表板頂端，選取 **Add variable**。
1. 設定下列一般設定：
   - **Name**：輸入 `environment`。這是在查詢中參照變數時使用的識別碼，例如 `$environment` 或 `${environment}`。
   - **Label**：輸入 `Environment`。
   - **Description**：選用，輸入描述，例如 `Filters visualizations by deployment environment`。
   - **Type**：選取 **Custom**。
1. 在 **Custom options** 中，選取 **Add option**。
1. 在第一個選項列中，在 **Value** 中輸入 `dev`，在 **Label** 中輸入 `Development`。當您參照變數時，OpenSearch Dashboards 會將值插入查詢中，並將選用的標籤用作下拉式清單中的顯示文字。
1. 再次選取 **Add option**，在 **Value** 中輸入 `staging`，在 **Label** 中輸入 `Staging`。
1. 再次選取 **Add option**，在 **Value** 中輸入 `prod`，在 **Label** 中輸入 `Production`。
1. 設定共用選項設定。如需更多資訊，請參閱[設定變數選項設定](#configuring-variable-option-settings)。
1. 選取 **Add variable**。

自訂選項值必須唯一且不能為空。OpenSearch Dashboards 在下拉式清單中最多顯示 100 個選項。
{: .note}

下列圖片顯示設定了值與標籤配對的 `environment` 自訂變數。

![設定了值與標籤選項列之環境自訂變數的變數編輯面板]({{site.url}}{{site.baseurl}}/images/dashboard-variables/custom-variable-config.png){: width="500" }

## 設定變數選項設定

查詢變數與自訂變數共用下列選項設定：

- **Sort**：控制選項在下拉式清單中的排序方式。選取 **Disabled**、**Alphabetical**（升冪或降冪）或 **Numerical**（升冪或降冪）。
- **Allow multiple selections**：允許您從變數下拉式清單中選取多個值。
- **Include All option**：在下拉式清單中新增 **All** 選項。此設定僅在啟用 **Allow multiple selections** 時可用。

## 管理現有變數

**Manage variables** 面板會列出所有現有變數，包括其類型、名稱和組態選項。若要進入此面板，請依照下列步驟操作：

1. 導覽至您的工作區。
1. 從 **Dashboards** 中，選取要更新的儀表板。
1. 在頂端，切換 **Edit** 選取器以進入編輯模式。
1. 在左上角，選取 **Manage variables** 圖示，如下圖所示。

![顯示變數名稱、類型和操作圖示的 Manage variables 面板]({{site.url}}{{site.baseurl}}/images/dashboard-variables/manage_panel.png)

**Manage variables** 圖示僅在儀表板中已建立變數時才會出現。如果不存在變數，請先建立一個變數，再進入管理介面。
{: .note}

## 編輯變數

若要編輯現有變數，請依照下列步驟操作：

1. 開啟 **Manage variables** 面板。
1. 選取您要修改之變數的 **Edit** 圖示。
1. 進行變更。
1. 選取 **Update variable** 以儲存。

變更變數名稱會導致任何參照舊名稱的查詢失敗。
{: .note}

## 刪除變數

若要刪除變數，請依照下列步驟操作：

1. 開啟 **Manage variables** 面板。
1. 選取您要移除之變數的 **Delete** 圖示。
1. 在對話方塊中確認刪除。

被其他變數或視覺化編輯器參照的變數會在管理面板中顯示指示標記。刪除被參照的變數會導致任何使用該變數的查詢失敗。
{: .note}

## 整理變數

變數會依照其在管理面板中出現的順序顯示在儀表板頂端。

若要重新排列變數，請依照下列步驟操作：

1. 開啟 **Manage variables** 面板。
1. 拖曳變數左側的重新排列控制項。
1. 將其放置在所需位置。
1. 儲存儀表板以套用新順序。

## 隱藏變數

您可以將變數從儀表板頂端隱藏，同時保留其在查詢中的可用性。

若要隱藏或顯示變數，請依照下列步驟操作：

1. 開啟 **Manage variables** 面板。
1. 選取該變數的 **Hide/Show** 圖示。
1. 儲存儀表板以套用變更。

隱藏的變數在管理面板中會標記為 **Hidden** 徽章，且不會出現在儀表板中。
{: .note}

## 變數狀態指示器

每個變數在儀表板頂端都會顯示狀態指示器：

- **Loading**：系統擷取選項時會出現旋轉圖示。
- **Error**：出現錯誤圖示，且工具提示會顯示錯誤訊息。下拉式清單將被停用。
- **No options**：如果變數查詢沒有傳回結果，下拉式清單中會顯示 "No options"。

## URL 同步

變數值會使用 `variableValues` 查詢參數自動同步到儀表板 URL：

```js
?variableValues=(service:(api),region:(us-east,us-west))
```

URL 同步可實現下列功能：

- 發送一個已預先選取特定變數值的儀表板連結。
- 儲存具有您偏好變數設定的儀表板檢視。
- 在頁面重新整理後保留變數選取內容。

## 變數相依性

查詢類型的變數可以在其查詢中參照其他變數。下列範例顯示了一個參照另一個變數的查詢變數：

```sql
source=logs | where region=$region | dedup service | fields service
```
{% include copy.html %}

在此範例中，`service` 變數相依於 `region` 變數。當 `region` 變數變更時，`service` 變數會自動重新整理其選項。

請記住下列考量因素：

- 避免循環相依，例如變數 A 參照變數 B，而變數 B 又參照變數 A。
- 變數會依照其在管理面板中出現的順序進行評估。請將相依變數放置在被參照變數之後。

## 後續步驟

- [使用儀表板變數]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/dashboard-variables/using-variables/)
