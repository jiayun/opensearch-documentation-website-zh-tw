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

當可用值的清單是從資料來源取得時，請使用查詢變數。例如，您可以從範例網站記錄資料建立 `extension` 變數，並使用它依副檔名篩選多個視覺化。

以下範例使用 OpenSearch Dashboards 的範例網站記錄資料。如果您使用不同的資料集，請選取符合您資料的資料集與欄位。
{: .note}

若要建立查詢變數，請依照下列步驟操作：

1. 在您的 Observability 工作區中，於左側導覽選取 **Dashboards**。
1. 開啟現有的儀表板，或選取 **Create Dashboard** 來建立新的儀表板。如果您建立新的儀表板，請先輸入標題並選取 **Save** 加以儲存。
1. 如果儀表板處於檢視模式，請開啟 **Edit** 切換開關。
1. 在儀表板頂端，選取 **Add variable**。
1. 設定下列一般項目：
   - **Name**：輸入 `extension`。這是在查詢中參照變數時使用的識別字，例如 `$extension` 或 `${extension}`。
   - **Label**：輸入 `Extension`。這是顯示在儀表板頂端的顯示名稱。
   - **Description**：可選擇性輸入描述，例如 `Filters visualizations by file extension`。
   - **Type**：保持選取 **Query**。
1. 在 **Query options** 區段中，選取 **Open variable editor**。查詢編輯器會在彈出視窗中開啟，並附上固定的 **Preview of values** 面板。
1. 將查詢語言保持為 **PPL**。若要改為以 Prometheus 中繼資料建置查詢，請參閱[使用 PromQL 查詢變數](#using-a-promql-query-variable)。
1. 確認選取的資料集為 `opensearch_dashboards_sample_data_logs`。若要選擇不同的資料集，請選取該資料集名稱。
1. 輸入下列查詢：

   ```sql
   source = opensearch_dashboards_sample_data_logs | stats count() by extension | fields extension
   ```
   {% include copy.html %}

1. 選取 **Preview**。預覽會執行查詢，並在 **Preview of values** 面板中顯示前 100 個變數選項。您必須先成功預覽查詢變數，才能套用它。
1. 在 **Value field** 下拉式選單中，確認已選取 `extension`。此欄位會由預覽自動填入。當您使用 `$extension` 或 `${extension}` 時，值欄位會提供插入查詢中的值。
1. 在 **Label field** 下拉式選單中，保持 **None**。僅當查詢傳回獨立的欄位以取代儲存值顯示在下拉式清單中時，才選取標籤欄位。
1. 選用：在 **Regex** 中輸入正規表示式，以篩選可用選項，或從查詢結果中擷取值與標籤。例如，`^(css|gz|zip)$` 只會顯示 `css`、`gz` 與 `zip` 選項。預覽會更新以顯示篩選後的選項。如需更多資訊，請參閱[以正規表示式篩選與擷取選項](#filtering-and-extracting-options-with-a-regular-expression)。
1. 選取 **Apply** 以儲存查詢並關閉編輯器。
1. 回到變數編輯器後，在 **Query options** 區段中選取 **Refresh** 選項，以選擇 OpenSearch Dashboards 更新變數選項的時機：
   - **On dashboard load**（預設）：在載入儀表板時重新整理選項。
   - **On time range change**：在儀表板的時間範圍變更時重新整理選項。當可用值取決於所選的時間範圍時，請使用此選項。
1. 設定 **Selection options** 區段中的各項設定。如需更多資訊，請參閱[設定變數選項設定](#configuring-variable-option-settings)。
1. 選取 **Add variable**。

變數會顯示在儀表板頂端。下圖顯示使用範例網站記錄資料設定的 `extension` 查詢變數的查詢編輯器。

![使用範例網站記錄資料設定的副檔名 PPL 查詢變數查詢編輯器]({{site.url}}{{site.baseurl}}/images/dashboard-variables/query-variable-config.png){: width="700" }

### 對應查詢結果欄位

查詢變數可以使用一個欄位作為儲存值，另一個欄位作為顯示標籤：

- **Value field**：用作變數值的欄位。當您參照變數時，OpenSearch Dashboards 會將此值插入查詢中。
- **Label field**：選用，用作變數下拉式清單中顯示標籤的欄位。標籤不會改變插入查詢中的值。

例如，如果您的查詢傳回 `service_id` 和 `service_name`，請將 **Value field** 設定為 `service_id`，並將 **Label field** 設定為 `service_name`。下拉式清單會顯示服務名稱，而查詢則會接收服務 ID。

如果您沒有選取 **Value field**，OpenSearch Dashboards 會使用查詢傳回的第一個欄位。為了避免出現非預期的值，請預覽查詢並明確選取要用作變數值的欄位。
{: .tip}

### 使用 PromQL 查詢變數

當查詢變數使用由 Prometheus 資料連線支援的資料集時，您可以將查詢語言設為 **PromQL**。您不需要撰寫原始查詢，而是從下列其中一種 PromQL 查詢類型來建立變數：

- **Label names**：列出資料中的標籤名稱。您可以選擇將結果範圍限定於某個指標。
- **Label values**：列出您所選標籤的值。您可以使用標籤比對器（`=`、`!=`、`=~` 和 `!~`）縮小結果範圍，並從 Metrics Explorer 中選取指標。
- **Metrics**：列出指標名稱。您可以選擇使用指標名稱的正規表示式來篩選結果。
- **Series query**：列出符合序列選取器的完整時間序列（標籤集）。
- **Query result**：執行原始 PromQL 運算式，與 PPL 所使用的自由文字輸入方式相同。

若要建立 PromQL 查詢變數，請依照下列步驟操作：

1. 在儀表板頂端選取 **Add variable**，並將 **Type** 設為 **Query**。
1. 在 **Query options** 區段中，選取 **Open variable editor**。
1. 將查詢語言設為 **PromQL**。
1. 選取資料集名稱，並選擇由 Prometheus 資料連線支援的資料集。
1. 在 **Query type** 中選取查詢類型（例如 **Label values**），並填寫其欄位。針對 **Label values**，選取標籤，並選擇性地選取指標及一或多個標籤比對器。
1. 選取 **Preview** 以載入選項，然後選取 **Apply** 以儲存查詢並關閉編輯器。
1. 設定重新整理行為，然後選取 **Add variable**。

下圖顯示以 **Label values** 查詢類型設定的 PromQL 查詢變數。

![為 PromQL label values 查詢變數設定的變數編輯器面板]({{site.url}}{{site.baseurl}}/images/dashboard-variables/promql-query-variable-config.png){: width="700" }

PromQL 查詢變數需要由您 Observability 工作區中的 Prometheus 資料連線支援的資料集。
{: .note}

### 使用正規表示式篩選與擷取選項

查詢變數中的 **Regex** 欄位支援兩種行為。您可以輸入單純的模式（例如 `^win`），或以 `/pattern/flags` 形式輸入（例如 `/^win/i`）。

以下範例使用由範例網站記錄資料的 `machine.os` 欄位建立的查詢變數：

```sql
source = opensearch_dashboards_sample_data_logs | stats count() by `machine.os` | fields `machine.os`
```
{% include copy.html %}

預覽此查詢會傳回選項 `ios`、`osx`、`win 7`、`win 8` 與 `win xp`。接著您可對這些結果套用正規表示式：

- **篩選**：當正規表示式沒有 `value` 或 `label` 擷取群組時，OpenSearch Dashboards 只會保留符合的選項，且不做任何更動。例如，`^win` 只會保留 `win 7`、`win 8` 與 `win xp`。
- **擷取**：當正規表示式包含具名的 `(?<value>...)` 擷取群組時，OpenSearch Dashboards 會以擷取到的文字取代每個選項的值。選用的具名 `(?<label>...)` 群組可用來設定顯示標籤。解析為相同值的選項會自動去除重複。例如，`^(?<value>ios|osx|win)` 會擷取作業系統系列，因此 `win 7`、`win 8` 與 `win xp` 會合併為單一的 `win` 選項，留下 `ios`、`osx` 與 `win`。

若要設定另行的顯示標籤，請加入 `(?<label>...)` 群組。例如，若查詢傳回複合值（例如 `env=dev,label=Development`），模式 `^env=(?<value>[^,]+),label=(?<label>.+)$` 會將 `dev` 儲存為值，並在下拉式選單中顯示 `Development`。

![從範例網站記錄資料的 machine.os 欄位擷取作業系統系列的 Regex 欄位]({{site.url}}{{site.baseurl}}/images/dashboard-variables/regex-capture-groups.png){: width="700" }

當您編輯現有的變數時，查詢預覽會自動執行，讓您能立即看到擷取後的選項。
{: .tip}

## 建立自訂變數

當可用值清單固定且不需要從資料來源擷取時，請使用自訂變數。例如，您可以建立一個 `environment` 變數，其中包含 `dev`、`staging` 和 `prod` 選項。

若要建立自訂變數，請依照下列步驟操作：

1. 在您的 Observability 工作區中，於左側導覽選取 **Dashboards**。
1. 開啟現有的儀表板，或選取 **Create Dashboard** 以建立新的儀表板。如果您建立新的儀表板，請先輸入標題並選取 **Save** 來儲存。
1. 如果儀表板處於檢視模式，請開啟 **Edit** 切換開關。
1. 在儀表板頂端，選取 **Add variable**。
1. 設定下列一般設定：
   - **Name**：輸入 `environment`。這是用來在查詢中參照該變數的識別碼，例如 `$environment` 或 `${environment}`。
   - **Label**：輸入 `Environment`。
   - **Description**：可選擇性輸入說明，例如 `Filters visualizations by deployment environment`。
   - **Type**：選取 **Custom**。
1. 在 **Custom options** 中，選取 **Add option**。
1. 在第一個選項列中，於 **Value** 輸入 `dev`，並於 **Label** 輸入 `Development`。當您參照該變數時，OpenSearch Dashboards 會將值插入查詢中，並使用選用的標籤作為下拉式清單中的顯示文字。
1. 再次選取 **Add option**，於 **Value** 輸入 `staging`，並於 **Label** 輸入 `Staging`。
1. 再次選取 **Add option**，於 **Value** 輸入 `prod`，並於 **Label** 輸入 `Production`。
1. 設定共用的選項設定。如需詳細資訊，請參閱[設定變數選項設定](#configuring-variable-option-settings)。
1. 選取 **Add variable**。

自訂選項值必須是唯一值，且不能為空。OpenSearch Dashboards 在下拉式清單中最多顯示 100 個選項。
{: .note}

下圖顯示一個 `environment` 自訂變數，其中設定了值與標籤配對。

![變數編輯器面板已設定為環境自訂變數，並包含值與標籤選項列]({{site.url}}{{site.baseurl}}/images/dashboard-variables/custom-variable-config.png){: width="500" }

## 建立文字變數

當您想直接輸入單一自由格式值、而不使用選項清單時，請使用文字變數。例如，您可以建立 `search_term` 變數，並從變數列變更其值，而不需開啟編輯器。

若要建立文字變數，請依照下列步驟操作：

1. 在您的 Observability 工作區中，於左側導覽選取 **Dashboards**。
1. 開啟現有的儀表板，或選取 **Create Dashboard** 建立新的儀表板。如果您建立新的儀表板，請先輸入標題並選取 **Save** 來儲存。
1. 如果儀表板處於檢視模式，請開啟 **Edit** 切換開關。
1. 在儀表板頂端，選取 **Add variable**。
1. 設定下列一般設定：
   - **Name**：輸入 `search_term`。這是在查詢中參照變數時使用的識別碼，例如 `$search_term` 或 `${search_term}`。
   - **Label**：輸入 `Search term`。
   - **Description**：選用，輸入描述。
   - **Type**：選取 **Text**。
1. 在 **Value** 中輸入初始值。
1. 選取 **Add variable**。

文字變數會以輸入框的形式出現在儀表板頂端。輸入值後按 **Enter**，或在框外選取，即可套用該值。該值會在您完成編輯時套用，而不是在每次按鍵時套用，因此參照該變數的視覺化不會在您輸入時重新執行。

![設定為文字變數並具有自由格式值的變數編輯器面板]({{site.url}}{{site.baseurl}}/images/dashboard-variables/text-variable-config.png){: width="500" }

文字變數沒有選項清單，因此 **Sort**、**Allow multiple selections**、**Include All option** 與 **Allow custom values** 等設定不適用，且在此類型中會隱藏。
{: .note}

## 設定變數選項設定

查詢變數與自訂變數共用下列選項設定：

- **Sort**：控制選項在下拉式清單中的排序方式。選取 **Disabled**、**Alphabetical** 遞增或遞減，或 **Numerical** 遞增或遞減。
- **Allow multiple selections**：允許您從變數下拉式清單中選取多個值。
- **Include All option**：在下拉式清單中新增 **All** 選項。只有在開啟 **Allow multiple selections** 時，才能使用此設定。
- **Allow custom values**：讓您提交不在產生或靜態選項清單中的值。開啟此設定後，在變數下拉式清單的搜尋方塊中輸入內容時，會將輸入的值顯示為第一列，並標示 **Hit enter to add**。按下 **Enter** 或選取該列即可新增。在多重選取變數中，自訂值會附加到目前的選取項目；在單一選取變數中，則會取代目前的值。自訂值只會儲存為變數的選取值，不會新增到變數定義中。

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

- 傳送已預先選取特定變數值的儀表板連結。
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
