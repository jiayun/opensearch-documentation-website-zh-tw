---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資源存取管理"
parent: Dashboards management
nav_order: 30
---

# 資源存取管理
**於 3.3 版推出**
{: .label .label-purple }

OpenSearch Dashboards 中的資源共用功能，可針對外掛程式所定義的個別資源，提供精細的文件層級存取控制。此功能擴充了 OpenSearch 以角色為基礎的存取控制，讓資源擁有者可以指定誰能存取資源，以及他們擁有的存取層級，包括唯讀或讀寫權限。請使用 OpenSearch Dashboards 進行日常存取管理，並使用 **Dev Tools** 主控台進行自動化與批次作業。

如果您在 OpenSearch Dashboards 中看不到資源共用功能，請聯絡您的 OpenSearch 管理員，以啟用此功能並指派適當的權限。
{: .note}

**資源**是外掛程式建立並儲存在受保護系統索引中的文件，例如機器學習 (ML) 模型群組、異常偵測器、報表定義或 Flow Framework 工作流程。

下表列出預設的資源存取權，這取決於使用者的角色以及與資源的關係。

| 使用者 | 存取權 |
|---|---|
| 資源建立者 | 完整存取權（檢視、編輯、刪除及共用） |
| 超級管理員 | 完整存取權 |
| 其他使用者 | 除非資源已與其共用，否則無存取權 |

當您將資源與特定使用者、角色或後端角色共用後，這些使用者便能在 OpenSearch Dashboards 中看到該資源。OpenSearch Dashboards 會根據每位使用者的身分、權限及資源共用組態來篩選資源清單。

## 先決條件

若要在 OpenSearch Dashboards 中使用資源共用，您必須符合下列先決條件：

* 管理員已授予您該資源所屬外掛程式的叢集權限。您需要這些權限才能建立資源。
* 您是資源的擁有者、您是超級管理員，或擁有者已將資源與您共用。
* 管理員已啟用下列設定：
    ```yaml
    plugins.security.resource_sharing.enabled: true
    plugins.security.resource_sharing.protected_types: ["<resource-type>"]
    plugins.security.system_indices.enabled: true
    ```
    {% include copy.html %}

    如需這些設定的詳細資訊，請參閱[設定資源共用]({{site.url}}{{site.baseurl}}/security/access-control/resources/#configuring-resource-sharing)。

## 管理所有資源類型的存取權

**Resource Access Management** 頁面會列出您可存取的所有受保護類型資源，讓您在同一處管理這些資源的共用。請依照下列步驟檢視及管理資源的存取權：

1. 在頂端選單中，前往 **Management** > **Resource Access Management**。

1. 在 **Resources** 面板右上角的下拉式清單中，選取資源類型。表格會列出您可存取的該類型資源，並在 **Owner** 欄中顯示每項資源的擁有者。**Shared With** 欄會列出與該資源共用的使用者、角色和後端角色及其存取層級；如果資源為私人資源，則會顯示 **Not shared**。如果沒有顯示任何資源，請建立資源，或請管理員或資源擁有者與您共用資源。

   下圖顯示異常偵測器資源類型的 **Resources** 面板。

   ![Resources 面板列出異常偵測器及其資源 ID、擁有者，以及與每個偵測器共用的使用者和角色]({{site.url}}{{site.baseurl}}/images/resource-sharing/4-after-selecting-resource.png)

1. 在 **Actions** 欄中，針對私人資源選取 **Share**，或針對已共用的資源選取 **Update Access**。只有您擁有的資源，或擁有者已授予您共用權限的資源，才會顯示這些選項。超級管理員可以共用任何資源。

1. 在 **Share Resource** 或 **Update Access** 對話方塊中，從 **Access-level** 下拉式清單選取存取層級。在 **Share Resource** 對話方塊中，請先選取 **Add access-level** 以顯示欄位。

1. 在 **Users**、**Roles** 和 **Backend roles** 欄位中，輸入您要授予此存取層級的使用者、角色和後端角色。若要將存取權授予所有使用者，請在 **Users** 欄位中輸入星號 (`*`)。

1. 若要將不同的存取層級授予另一組使用者，請選取 **Add access-level** 並重複前兩個步驟。若要刪除存取層級，請選取 **Remove**。

1. 選取 **Share** 或 **Update Access** 以套用變更。移除存取權後，受影響的使用者會立即無法看到該資源。

## 從外掛程式頁面管理存取權
**於 3.9 版推出**
{: .label .label-purple }

當資源類型已啟用資源共用時，您可以直接從外掛程式的資源清單管理資源的存取權。

下表列出支援從其外掛程式資源清單進行存取管理的資源，並連結至各資源可用的存取層級。

| 外掛程式 | 資源 |
|---|---|
| Alerting | [監視器和工作流程]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/alerting-access-control/) |
| Anomaly Detection | [偵測器]({{site.url}}{{site.baseurl}}/observing-your-data/ad/detector-access-control/)和[預測器]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/forecaster-access-control/) |
| Flow Framework | [工作流程]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-access-control/) |
| ML Commons | [模型群組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-sharing-access-control/) |
| Notifications | [通道]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/notification-access-control/) |
| Reporting | [報表定義]({{site.url}}{{site.baseurl}}/reporting/report-definition-access-control/)和[報表]({{site.url}}{{site.baseurl}}/reporting/report-instance-access-control/) |
| Security Analytics | [偵測器和關聯規則]({{site.url}}{{site.baseurl}}/security-analytics/resource-access-control/) |

只有當您是資源的擁有者、超級管理員，或擁有者已授予共用權限的使用者時，才能共用該資源。
{: .note}

### 共用資源

若要從外掛程式頁面共用資源，請依照下列步驟操作：

1. 開啟支援之外掛程式的資源清單。例如，在頂端選單中，前往 **OpenSearch Plugins** > **Anomaly Detection**，然後選取 **Detectors**。

1. 在 **Access** 欄中，檢閱每項資源的共用狀態。每項資源都會顯示 **Private** 或 **Shared** 狀態。您有權共用的資源還會顯示共用圖示，如下圖所示。

   ![偵測器清單顯示 Access 欄，其中包含 Private 和 Shared 狀態以及共用圖示]({{site.url}}{{site.baseurl}}/images/resource-sharing/share-button-access-column.png)

1. 選取您要管理之資源的共用圖示。

1. 在 **Manage access** 對話方塊中，設定下列值：

   1. 從 **Access level** 下拉式清單選取存取層級。可用的層級依資源類型而異。

   1. 在 **Users** 欄位中輸入使用者名稱，然後按下 Enter。若要以所選存取層級將資源與所有使用者共用，請輸入星號 (`*`)。

   1. 若要將資源與角色或後端角色共用，請展開 **Advanced access options**，並在 **Roles** 或 **Backend roles** 欄位中輸入角色名稱。

   1. 若要以多個存取層級共用資源，請選取 **Add access level** 並重複前述步驟。每個層級各自維護其使用者、角色和後端角色。若要刪除層級，請選取 **Remove level**。

   1. 選取 **Save changes**。

### 將資源設為私人

若要停止共用資源，請依照下列步驟操作：

1. 在 **Access** 欄中，選取該資源的共用圖示。

1. 在 **Manage access** 對話方塊的 **Remove all sharing** 區段中，選取 **Remove access**。

資源狀態會恢復為 **Private**，先前與其共用的使用者、角色和後端角色將無法再存取該資源。

## 列出與您共用的資源

OpenSearch Dashboards 只會顯示您可存取的資源，因此不需要執行其他動作。在下列任一情況下，資源會出現在您的資源清單中：

* 您是資源的擁有者。
* 擁有者已明確將資源與您共用。
* 擁有者已將資源與您的其中一個角色或後端角色共用。
* 資源已與所有使用者共用。

在所有情況下，列出資源還需要具備該資源所屬外掛程式的叢集權限。

## 使用 API 管理資源共用

您可以使用 REST API 以程式設計方式管理資源共用。只有當您是擁有者、超級管理員，或具有該資源的共用存取權時，才能執行這些操作。您可以使用命令列或 **Dev Tools** 主控台傳送 API 請求。

如需完整的 API 文件，包括端點、參數和範例，請參閱[資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/)。

## 疑難排解

請使用下表排解常見問題。

| 問題 | 可能原因 | 解決方式 |
|---|---|---|
| 看不到 **Resource Access Management** 頁面。 | 此功能已停用。 | 請管理員啟用 `plugins.security.resource_sharing.enabled`。 |
| 您無法建立資源。 | 您沒有該資源所屬外掛程式的叢集權限。 | 請管理員將您對應至授予這些權限的角色。 |
| 您無法存取資源。 | 該資源未與您共用。 | 請擁有者以適當的存取層級與您共用資源。 |
| API 請求傳回 `403` 錯誤。 | 該資源未與您共用。 | 請擁有者以適當的存取層級與您共用資源。 |
| 資源未列在 OpenSearch Dashboards 中。 | 該資源類型未標示為受保護。 | 請管理員將該資源類型新增至 `plugins.security.resource_sharing.protected_types`。 |
| 更新存取權沒有作用。 | 該存取層級對此資源類型無效。 | 請對照該資源所屬外掛程式的文件，確認存取層級。 |

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源共用 API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) -- 用於程式設計管理的 REST API 參考資料