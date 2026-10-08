---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立工作區"
parent: Workspaces
nav_order: 1
---

# 建立工作區
**2.18 版推出**
{: .label .label-purple }

開始本教學之前，您必須啟用工作區功能旗標。如需詳細資訊，請參閱[啟用工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace/#enabling-workspaces)。

啟用已儲存物件權限時，只有具備管理員身分的使用者才能建立工作區。如需詳細資訊，請參閱[設定儀表板管理員]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#configuring-dashboard-administrators)。

若要建立工作區，請依照下列步驟操作：

1. 開啟 OpenSearch Dashboards。
2. 在主頁面中，選擇適合您使用案例的卡片，例如 **Observability**、**Security Analytics**、**Search**、**Essentials** 或 **Analytics**。或者，您也可以選取 **Create workspace** 按鈕，然後從下拉式選單中選擇適當的使用案例。
3. 在 **Workspace details** 視窗中輸入必要資訊。
  - **Workspace name** 為必要項目。有效字元為 `a-z`、`A-Z`、`0-9`、圓括號 (`()`)、方括號 (`[]`)、底線 (`_`)、連字號 (`-`) 和空格。請在字元限制 (40 個字元) 內選擇唯一的工作區名稱。當工作區名稱已存在或超過字元限制時，**Create workspace** 按鈕會停用，並顯示錯誤訊息。
  - **Use case and features** 為必要項目。請選擇最符合您需求的使用案例。如果您使用 Amazon OpenSearch Serverless 並已啟用[多個資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)功能，系統會自動指派 **Essentials**。
4. (選用) 選取色彩選擇器，以自訂工作區圖示的色彩。
5. (選用) 新增最多 200 個字元的工作區說明。當說明超過字元限制時，此選項會停用。
6. (選用) 輸入自訂的 **Workspace ID**。如果保留空白，系統會自動產生 ID。自訂 ID 必須為 6 到 36 個字元，且只能使用字母、數字、底線 (`_`) 和連字號 (`-`)。如果已存在具有所提供 ID 的工作區，系統會傳回錯誤。
7. 儲存您的工作區。
  - 當您輸入所有必要欄位的資訊後，**Create workspace** 按鈕就會變成可用狀態。您會自動成為工作區擁有者。如果已啟用已儲存物件權限，系統會將您重新導向至協作者頁面；如果已停用已儲存物件權限，則會重新導向至概觀頁面。如需權限的詳細資訊，請參閱[設定儀表板管理員]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#configuring-dashboard-administrators)。

若要設定權限，請參閱[工作區存取控制清單]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/)以取得詳細資訊。

## 將資料來源與工作區建立關聯

只有在啟用多個資料來源功能時，才會顯示 **Associate data source** 選項。建立工作區之前，您必須將其連接至至少一個資料來源。如果您尚未設定資料來源，請參閱[資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。連接資料來源後，您就可以將其連結至新的工作區。
{: .warning}

### 建立 OpenSearch 資料來源的關聯

若要建立 OpenSearch 資料來源的關聯，請依照下列步驟操作：

1. 選取 **Associate OpenSearch Data Sources** 按鈕以開啟選取對話視窗。
2. 在對話視窗中檢視可用的資料來源：
  - 標準 OpenSearch 來源會顯示為單一項目。
  - 具有直接查詢連線的來源會顯示 +N 指示符號。
3. 選取適當的資料來源名稱。
4. 選取 **Associate data sources** 按鈕以完成關聯。

### 建立直接查詢來源的關聯

若要建立直接查詢來源的關聯，請依照下列步驟操作：

1. 選取 **Associate direct query data sources** 按鈕以開啟選取對話視窗。對話視窗只會顯示具有直接查詢連線的來源。
2. 選取資料來源，即可自動展開其直接查詢連線。
3. 選取 **Associate data sources** 按鈕以完成關聯。
