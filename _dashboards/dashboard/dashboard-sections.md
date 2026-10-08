---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "儀表板區段"
parent: Creating dashboards
nav_order: 35
has_children: false
---

# 儀表板區段
**Introduced 3.9**
{: .label .label-purple }

這是一項實驗性功能，不建議在生產環境中使用。如需了解此功能的進度更新或想要提供回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。
{: .warning}

儀表板區段是可摺疊的容器，可將儀表板內的視覺化面板分組為具名的類別。使用區段來組織包含許多面板的儀表板，並透過將較少使用的區段設定為摺疊狀態來儲存，以縮短其初始載入時間。

下圖顯示了一個包含視覺化區段的儀表板。

![包含四個視覺化面板區段的儀表板]({{site.url}}{{site.baseurl}}/images/dashboard-sections/dashboard-with-sections.png)

## 啟用儀表板區段

要啟用儀表板區段，請將以下設定新增至您的 `opensearch_dashboards.yml` 檔案：

```yaml
uiSettings.overrides.home:useNewHomePage: true
dashboard.allowDashboardSections: true
```
{% include copy.html %}

然後重新啟動 OpenSearch Dashboards 以使變更生效。

## 建立與管理區段

除了摺疊與展開之外，所有區段操作都需要 [編輯模式]({{site.url}}{{site.baseurl}}/dashboards/dashboard/opening-a-dashboard/)。在編輯模式中，選取區段標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示以開啟區段快顯功能表，或選取面板上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/gear-icon.png" class="inline-icon" alt="gear icon"/>{:/} (齒輪) 圖示以開啟面板快顯功能表。

在區段內，面板具有自己的格線佈局，因此您可以像在沒有區段的儀表板上一樣拖曳並調整其大小。區段會根據其內容自動調整高度。

### 建立區段

當您在儀表板上建立第一個區段時，所有現有面板都會被分組到該區段中，以保留目前的佈局。後續建立的區段初始狀態為空。

要建立區段，請執行以下步驟：

1. 在編輯模式下開啟儀表板。
2. 在工具列中，選取 **Add**。
3. 選取 **Section**。

區段將被新增至儀表板中。

### 重新命名區段

要重新命名區段，請執行以下步驟：

1. 選取區段標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示。
2. 選取 **Rename**。
3. 在 **Rename section** 對話方塊中，輸入區段名稱。
4. 選取 **Save**。

區段名稱不需要唯一，但使用不同的名稱可以更輕鬆地在區段之間移動面板。
{: .tip}

### 摺疊與展開區段

要摺疊區段，請選取區段標題左側的箭頭。區段標題將保持可見，而面板則會被隱藏。要展開已摺疊的區段，請再次選取該箭頭。

### 重新排序區段

要重新排序區段，請執行以下步驟：

1. 選取並按住區段標題（其作為拖曳控制項）。
2. 將區段拖曳到新位置。
3. 放開區段以將其放置在該位置。

### 將面板移動到另一個區段

您可以將面板從一個區段移動到另一個區段，或從 **Ungrouped** 區域移動到區段中。

要移動面板，請執行以下步驟：

1. 選取面板右上角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/gear-icon.png" class="inline-icon" alt="gear icon"/>{:/} (齒輪) 圖示。
2. 選取 **Move to section**。
3. 在 **Move to section** 對話方塊中，選取目標區段。
4. 選取 **Move**。

面板將從目前的區段中移除並新增至目標區段。

### 將新視覺化新增至區段

要建立視覺化並將其新增至區段，請執行以下步驟：

1. 選取區段標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示。
2. 選取 **Create new visualization**。
3. 在視覺化編輯器中建立視覺化。
4. 選取 **Save and return**。

該視覺化將作為面板新增至區段中。

### 將已儲存的視覺化新增至區段

要從程式庫新增現有的視覺化，請執行以下步驟：

1. 選取區段標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示。
2. 選取 **Add from library**。
3. 搜尋並選取已儲存的視覺化。

該視覺化將被新增至區段中。

### 刪除區段

要刪除區段，請執行以下步驟：

1. 選取區段標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示。
2. 選取 **Delete section**。
3. 在確認對話方塊中，確認刪除。

刪除區段會永久移除其中的所有面板。儲存儀表板後，此操作無法復原。若要保留面板，請先將其移動到另一個區段。
{: .warning}

### 移除所有區段

您可以將所有面板恢復到單一格線，並從儀表板中移除區段結構。

要移除所有區段，請執行以下步驟：

1. 選取任何區段標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示。
2. 選取 **Ungroup all sections**。
3. 在確認對話方塊中，確認此操作。

所有面板將恢復到單一格線，且區段將被移除。

## 未分組面板

未分配到任何區段的面板會顯示在儀表板底部的 **Ungrouped** 區域。要將未分組面板移動到區段中，請使用面板快顯功能表中的 **Move to section**。您無法將面板移回 **Ungrouped** 區域。

## 摺疊區段與資料載入

摺疊區段會隱藏其面板，但不會將其移除。尚未顯示的面板在其區段摺疊時不會請求資料；當您展開區段並將面板捲動至可視範圍內時，它才會擷取資料。已經顯示過的面板即使在區段摺疊時，仍會隨儀表板其餘部分持續重新整理。

在包含許多視覺化的儀表板上，將較少使用的區段設定為摺疊狀態後儲存儀表板，可以縮短初始頁面載入時間，並減輕 OpenSearch 叢集的負載。
{: .tip}

## 範例：將儀表板組織成區段

若要跟隨此操作，請前往 OpenSearch Dashboards 首頁，選取 **Add sample data**，然後為 **Sample eCommerce orders** 選取 **Add data**。

以下步驟將範例電子商務儀表板組織成兩個區段：

1. 在頂端功能表上，選取 **Dashboards**，然後選取 **[eCommerce] Revenue Dashboard**。
2. 選取工具列中的 **Edit** 切換按鈕以進入編輯模式。
3. 在工具列中，選取 **Add** > **Section**。所有現有面板都會被分組到名為 **Section 1** 的區段中。
4. 選取 **Section 1** 標題上的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/kebab-icon.png" class="inline-icon" alt="vertical ellipsis icon"/>{:/} (垂直省略號) 圖示，選取 **Rename**，輸入 `Revenue and trends`，然後選取 **Save**。
5. 在工具列中，再次選取 **Add** > **Section**。第一個區段下方會出現一個空區段，同樣名為 **Section 1**（因為第一個區段已重新命名）。將此區段重新命名為 `Customer breakdown`。
6. 在 **[eCommerce] Sales by Gender** 面板上，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/gear-icon.png" class="inline-icon" alt="gear icon"/>{:/} (齒輪) 圖示，然後選取 **Move to section**，如下圖所示。
    ![標示出 Move to section 操作的面板選項功能表]({{site.url}}{{site.baseurl}}/images/dashboard-sections/panel-context-menu.png)
7. 在 **Move to section** 對話方塊中，選取 **Customer breakdown**，然後選取 **Move**。
8. 對 **[eCommerce] Sales Count Map** 和 **[eCommerce] Top Selling Products** 面板重複前兩個步驟。
9. 選取 **Customer breakdown** 標題左側的箭頭以摺疊該區段。
10. 選取 **Save**。

儀表板現在包含兩個區段，您可以獨立地摺疊、展開和重新排序，且摺疊的 **Customer breakdown** 區段在您展開之前不會載入任何資料。

## 限制

儀表板區段有以下限制：

- 不支援將面板從一個區段拖曳到另一個區段。要移動面板，請使用面板快顯功能表中的 **Move to section**。
- 不支援區段範圍的篩選器和變數。所有篩選器均適用於整個儀表板。
- 新增、重新命名、重新排序和刪除區段需要編輯模式。在檢視模式中，您只能摺疊和展開區段。

## 相關文件

- [建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)
- [自訂儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/customizing-a-dash/)
- [將視覺化新增至儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/adding-a-viz/)
