---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理工作區"
parent: Workspaces
nav_order: 2
---

# 管理工作區
**於 2.18 版推出**
{: .label .label-purple }

您可以在 **Workspace details** 頁面上存取及修改工作區詳細資料，包括名稱、描述、使用案例和圖示色彩。

若要存取及修改您的工作區詳細資料，請依照下列步驟操作：

1. 開啟 OpenSearch Dashboards，然後前往 **My Workspaces**。
2. 選擇所需的工作區，然後選取 **Edit** 按鈕進行變更
3. 選取 **Save** 按鈕以確認變更，或選取 **Discard changes** 按鈕以取消修改。

## 工作區更新權限

變更工作區時，適用下列權限：

1. **未安裝 Security 外掛程式：**所有使用者皆可編輯及更新工作區。
2. **已安裝 Security 外掛程式，且 `config/opensearch_dashboards.yml` 檔案中設有 `savedObjects.permission.enabled: false`：**所有使用者皆可編輯及更新工作區。
3. **已安裝 Security 外掛程式，且 `config/opensearch_dashboards.yml` 中設有 `savedObjects.permission.enabled: true`：**只有[工作區擁有者]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#defining-workspace-collaborators)和[工作區管理員]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#configuring-dashboard-administrators)可以編輯及更新工作區。

## 工作區更新限制

更新工作區使用案例時，適用下列規則。

原始使用案例 | 目標使用案例 |
:---: | :---:
Analytics  | 無法變更為任何其他使用案例
Search  | Analytics
Security Analytics  | Analytics
Observability  | Analytics
Essentials  |    Analytics Search<br> Security Analytics<br> Observability

## 工作區控制面板

**Workspace details** 頁面的右上角提供下列按鈕：

1. **Delete**（{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/} 圖示）
    - **未安裝 Security 外掛程式：**所有使用者皆可刪除工作區。
    - **已安裝 Security 外掛程式，且 `config/opensearch_dashboards.yml` 檔案中設有 `savedObjects.permission.enabled: false`：**所有使用者皆可刪除工作區。
    - **已安裝 Security 外掛程式，且 `config/opensearch_dashboards.yml` 檔案中設有 `savedObjects.permission.enabled: true`：**只有管理員可以刪除工作區。
2. **Set as default workspace：**將目前的工作區設為預設的登入目的地。
3. **Workspace overview：**在新分頁中開啟 **Overview** 頁面。

## 將資產新增至工作區

在左側導覽選單中存取 **Sample data**。選取適當的資料集，即可將其安裝至您的叢集和 OpenSearch Dashboards。

## 在工作區之間複製資產

不支援複製資料來源和組態。
{: .warning}

資產頁面提供下列方法，可在工作區之間複製資產：

1. **Copy all assets to...：**複製表格中的所有資產。
2. **Copy to...：**移動表格中選取的資產。
3. **Copy to...：**從表格中複製單一資產。

選取複製選項後，請從下拉式選單中選擇目標工作區。**Copy related assets** 核取方塊可讓您一併傳輸相關聯的資產。

選取 **Copy** 按鈕後，會出現側邊面板，顯示成功和失敗的資產傳輸。資產複製的目的地取決於下列安全性組態：
 
1. **未安裝 Security 外掛程式：**可存取所有工作區。
2. **已安裝 Security 外掛程式，且 `config/opensearch_dashboards.yml` 檔案中設有 `savedObjects.permission.enabled: false`：**可存取所有工作區。
3. **已安裝 Security 外掛程式，且 `config/opensearch_dashboards.yml` 檔案中設有 `savedObjects.permission.enabled: true`：**只能存取使用者具有讀寫或管理員權限的工作區。

## 建立資料來源關聯

在資料來源管理頁面上，您可以存取完整的相關聯 OpenSearch 連線清單、監視與您目前工作區相關的直接查詢連線，並視需要建立新的資料來源關聯。

### 管理 OpenSearch 連線

OpenSearch 連線分頁會顯示目前工作區所有相關聯的連線。請依照下列步驟管理您的連線：

1. 在連線分頁上存取完整的相關聯 OpenSearch 連線清單。
2. 視需要使用 **Remove association** 按鈕取消連線的連結。
3. 選取 **OpenSearch data sources** 按鈕，並在隨後出現的對話方塊中新增資料來源。
4. 從尚未建立關聯的 OpenSearch 連線中進行選取，以擴充您工作區的功能。

### 新增直接查詢連線

**Direct query connections** 分頁會顯示與您目前工作區相關聯的所有直接查詢連線清單。若要將更多直接查詢連線新增至您的工作區，請選取 **Direct query data sources** 按鈕。此時會開啟一個對話方塊視窗。

關聯對話方塊會顯示包含直接查詢連線、且尚未與您目前工作區建立關聯的 OpenSearch 連線清單。當您將某個 OpenSearch 連線與目前的工作區建立關聯時，該 OpenSearch 連線中的所有直接查詢連線也會自動建立關聯。

## 刪除工作區

只有管理員可以刪除工作區。如果您沒有看到 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/} 圖示，請檢查您的權限。如需詳細資訊，請參閱[設定儀表板管理員]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#configuring-dashboard-administrators)。
{: .warning}

刪除工作區會永久清除其所有資產（資料來源除外）以及工作區本身。此動作無法復原。

若要刪除工作區，請依照下列步驟操作：

1. 在 **Workspace details** 頁面中，選取右上角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/dashboards/trash-can-icon.png" class="inline-icon" alt="trash can icon"/>{:/}（垃圾桶）圖示，即可刪除目前的工作區。
2. 或者，在工作區清單頁面中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/}（省略符號）圖示，然後選取 **Delete**。您也可以選擇選取多個工作區進行大量刪除。

## 瀏覽工作區清單

工作區清單頁面是您管理工作區的中樞，會顯示您具有存取權限的所有工作區。主要功能包括：

- 搜尋：依名稱快速尋找工作區。
- 篩選：依使用案例排序工作區。
- 一目瞭然：檢視每個工作區的名稱、使用案例、描述、上次更新時間以及相關聯的資料來源。

每個工作區項目都包含 **Actions** 欄，其中提供下列功能按鈕。這些工具可簡化您的工作區管理，讓您有效率地整理及自訂 OpenSearch Dashboards 環境：

1. Copy ID：一鍵複製工作區 ID。
2. Edit：直接存取工作區的詳細組態頁面。
3. Set as default：輕鬆將任何工作區設為您的預設工作區。
4. Delete：視需要移除工作區（可能需要管理員權限）。
