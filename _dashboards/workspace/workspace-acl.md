---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作區存取控制清單"
parent: Workspaces
nav_order: 3
---

# 工作區存取控制清單
**於 2.18 版推出**
{: .label .label-purple }

工作區存取控制清單 (ACL) 負責管理已儲存物件的授權，並仰賴 [Security 外掛程式]({{site.url}}{{site.baseurl}}/security/)進行驗證。

## 角色類型

**工作區**使用案例涉及下列主要角色類型：

* **儀表板管理員：**擁有所有 OpenSearch Dashboards 功能與資料的完整存取權。
* **工作區管理員（亦稱為_擁有者_）：**對特定工作區擁有完整控制權，包括其組態與已儲存物件。建立工作區時，其建立者會自動被指派為工作區擁有者角色。
* **工作區內容製作者：**可以檢視、建立及更新工作區內的已儲存物件。
* **工作區檢視者：**對工作區中的已儲存物件擁有唯讀存取權。

 角色因工作區而異，使用者可以在不同工作區中擔任不同角色。
{: .note}

## 啟用權限控制

如需相關說明，請參閱[啟用 ACL 功能]({{site.url}}{{site.baseurl}}/dashboards/management/acl#enabling-the-acl-feature)。

## 設定儀表板管理員

若要授予 OpenSearch Dashboards 中所有工作區與物件的完整存取權，請設定管理員權限。編輯 `opensearch_dashboards.yml` 檔案，依使用者 ID 與後端角色定義管理員，如下列組態所示：

```yaml
opensearchDashboards.dashboardAdmin.users: ["UserID"]
opensearchDashboards.dashboardAdmin.groups: ["BackendRole"]
savedObjects.permission.enabled: true
```
{% include copy.html %}

根據預設，組態會設為 `[]`，表示沒有任何使用者被指定為管理員。若未安裝 Security 外掛程式且 `savedObjects.permission.enabled: false`，則所有使用者都會被授予管理員權限。

### 設定全域管理員存取權

使用此萬用字元設定將所有使用者設為管理員：

```yaml
opensearchDashboards.dashboardAdmin.users: ["*"]
```
{% include copy.html %}

### 為單一使用者設定管理員存取權

使用 `admin-user-id` 設定來設定使用者：

```yaml
opensearchDashboards.dashboardAdmin.users: ["admin-user-id"]
```
{% include copy.html %}

### 依後端角色設定管理員存取權

使用 `admin-role` 設定來設定使用者：

```yaml
opensearchDashboards.dashboardAdmin.groups: ["admin-role"]
```
{% include copy.html %}

### 僅限管理員的操作

僅限管理員的操作包括下列項目：

- 建立工作區
- 刪除工作區
- 資料來源連線
- 中斷資料來源與工作區的連線

## 定義工作區協作者

協作者管理的存取權僅限管理員。**Collaborators** 功能僅在啟用權限控制時才可使用。如需啟用權限控制的說明，請參閱[啟用權限控制](#enabling-permission-control)。存取層級包括下列項目：

- **Read only：**授予檢視工作區及其資產的權限。
- **Read and write：**允許檢視及編輯工作區內的資產。
- **Admin：**提供完整存取權，包括檢視及編輯工作區內的資產，以及更新工作區中繼資料，例如名稱、描述、資料來源與協作者。

#### 權限模式

當您透過 UI 指派協作者時，系統會自動套用存取層級。當您透過[工作區 API]({{site.url}}{{site.baseurl}}/dashboards/workspace/apis/) 指派協作者時，每個存取層級都對應特定的權限模式組合。下表說明可用的權限模式。

| 權限模式 | 目標 | 描述 |
| :--- | :--- | :--- |
| `read` | 工作區本身 | 主體可以開啟並檢視工作區。 |
| `write` | 工作區本身 | 主體可以管理工作區本身：編輯其名稱、描述與設定、管理協作者，以及關聯資料來源。 |
| `library_read` | 工作區中的已儲存物件（資產） | 主體可以檢視儀表板、視覺化及索引模式等資產。 |
| `library_write` | 工作區中的已儲存物件（資產） | 主體可以在工作區中建立、編輯及刪除資產。 |

每個存取層級都需要一個針對工作區的權限模式，以及一個針對工作區資產的權限模式，如下表所列。若使用者或群組僅被指派部分的權限模式組合（例如有 `read` 但沒有 `library_read`），該使用者或群組就不會顯示為協作者。

| 存取層級 | 必要的權限模式 |
| :--- | :--- |
| Read only | `library_read` + `read` |
| Read and write | `library_write` + `read` |
| Admin | `library_write` + `write` |

在 **Collaborators** 頁面中，您可以依協作者 ID 進行搜尋，並依協作者類型與存取層級篩選結果。

### 新增協作者

工作區建立者會以協作者身分被授予 **Admin** 存取層級。若要新增更多協作者，請選取 **Add collaborators** 按鈕，此時會顯示下拉式選單。選擇 **Add Users** 或 **Add Groups** 以開啟對應的對話方塊來新增協作者。

#### 新增使用者

若要新增使用者，請依照下列步驟操作：

1. 選取 **Add Users** 按鈕以開啟對話方塊。根據預設，對話方塊會顯示一個空白的 `User ID` 欄位。
2. 選擇存取層級：**Read only**、**Read and write** 或 **Admin**。
3. 選擇 **Add another User** 以新增多個使用者。請勿使用重複或已存在的 `User ID` 欄位，以免發生錯誤。
4. 完成前請先解決所有錯誤。成功新增的使用者會顯示在協作者表格中。

#### 新增群組

若要新增群組，請依照下列步驟操作：

1. 選取 **Add Groups** 按鈕以開啟對話方塊。根據預設，對話方塊會顯示一個空白的 `Group ID` 欄位。
2. 選擇存取層級：**Read only**、**Read and write** 或 **Admin**。
3. 使用 **Add another group** 以新增多個群組。請勿使用重複或已存在的 `Group ID` 欄位，以免發生錯誤。
4. 完成前請先解決所有錯誤。成功新增的群組會顯示在協作者表格中。

### 修改存取層級

將協作者新增至協作者表格後，若您擁有必要的權限，即可修改其存取層級。協作者可以被指派任何存取層級。不過，若所有 **Admin** 協作者都被變更為較低的存取層級，則只有管理員能夠管理工作區協作。

#### 修改個別存取層級

若要修改單一協作者的存取層級，請依照下列步驟操作：

1. 選取表格列右側的動作圖示。
2. 從下拉式選單中選取 **Change access level**。
3. 從清單中選擇所需的存取層級。
4. 在出現的對話方塊中確認變更，然後選取 **Confirm**。確認後，表格中該協作者的存取層級便會更新。

#### 批次修改存取層級

若要同時變更多個協作者的存取層級，請依照下列步驟操作：

1. 在表格中選取所需的協作者列。
2. 選取出現的 **Actions** 按鈕。
3. 從下拉式選單中選取 **Change access level**。
4. 從提供的清單中選取新的存取層級。
5. 在出現的對話方塊中檢閱並確認變更。確認後，表格中所有已選取協作者的存取層級便會更新。

### 刪除協作者

將協作者新增至表格後，您可以選擇將其刪除。移除管理員協作者時請謹慎，因為刪除所有管理員協作者後，工作區協作者管理將僅限管理員執行。完成此動作前會顯示確認對話方塊。

#### 刪除個別協作者

若要刪除個別協作者，請依照下列步驟操作：

1. 選取表格列右側的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/ellipsis-icon.png" class="inline-icon" alt="ellipsis icon"/>{:/} 圖示以顯示下拉式選單。
2. 從下拉式選單中選取 **Delete collaborator**。此時會出現確認對話方塊以確認您的動作。
3. 在對話方塊中選取 **Confirm**，即可從表格中移除該協作者。

#### 批次刪除協作者

若要同時移除多個協作者，請依照下列步驟操作：

1. 在表格中選取包含您要移除之協作者的列。此時會出現「Delete x collaborators」按鈕。
2. 選取 **Delete x collaborators** 按鈕。
3. 檢閱出現的確認對話方塊。
4. 選取 **Confirm** 以從表格中移除所有已選取的協作者。

## 設定工作區隱私

啟用權限控制時，工作區管理員可以設定下列三種存取層級之一：

* **Private to collaborators（預設）：**只有工作區協作者可以存取工作區。
* **Anyone can view：**授予所有工作區使用者 **Read only** 權限，讓他們能夠檢視工作區資產。
* **Anyone can edit：**授予所有使用者 **Read and write** 權限，讓他們能夠檢視、建立及更新工作區資產。

協作者會取得兩者中較高的權限：其個別存取層級，或工作區層級的隱私設定。例如，若工作區隱私設為「Anyone can edit」，具有唯讀存取權的協作者也能編輯工作區資產。
您可以以**儀表板管理員**身分在 **Create workspace** 頁面上設定工作區隱私。您也可以以**工作區管理員**或**儀表板管理員**身分，在 **Collaborators** 或 **Workspace details** 頁面上修改此設定。

### 在建立工作區時設定工作區隱私

建立新工作區時，請依照下列步驟變更工作區隱私設定：

1. 從 **Set up privacy** 面板中選擇所需的存取層級。
2. （選用）選取 **Add collaborators after workspace creation** 核取方塊，以便稍後新增協作者。
3. 選取 **Create workspace** 以建立工作區。

### 在 **Collaborators** 頁面上修改工作區隱私

請依照下列步驟在 **Collaborators** 頁面上編輯工作區隱私設定：

1. 在 **Workspace privacy** 旁，選取 **Edit**。
2. 從下拉式選單中選取新的存取層級。
3. 選取 **Save changes** 以套用修改。

### 在 **Workspace details** 頁面上修改工作區隱私

請依照下列步驟在 **Workspace details** 頁面上編輯工作區隱私設定：

1. 選取 **Details** 面板右上角的 **Edit** 按鈕。
2. 從下拉式選單中選取新的存取層級。
3. 選取 **Save** 以套用修改。
