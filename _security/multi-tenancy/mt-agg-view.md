---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "已儲存物件的多租用戶彙總檢視"
parent: OpenSearch Dashboards multi-tenancy
nav_order: 150
---

# OpenSearch Dashboards 已儲存物件的多租用戶彙總檢視

這是在 OpenSearch 2.4 中推出的實驗性功能，不建議在正式環境中使用。如需瞭解此功能的進度更新，或想提供意見回饋，請參閱 GitHub 上的 [Dashboards 物件共用](https://github.com/opensearch-project/OpenSearch-Dashboards/issues/2249)議題。如需更全面地瞭解多租用戶功能未來的開發提案，請參閱 [Dashboards 物件共用](https://github.com/opensearch-project/security/issues/1869)議題。
{: .warning}

已儲存物件的彙總檢視可讓具有多個租用戶存取權的使用者，在單一檢視中查看與這些租用戶相關聯的所有已儲存物件，無須在租用戶之間切換。這包括使用者建立的租用戶，以及與使用者共用的租用戶。彙總檢視在 Saved Objects 表格中新增了 Tenant 下拉式選單與欄，讓使用者可以依租用戶篩選，並顯示與其相關聯的已儲存物件。

找到您感興趣的已儲存物件後，您就可以切換至該租用戶以操作該物件。

若要存取已儲存物件，請展開頂端選單，並選取 **Management > Dashboards Management > Saved Objects**。Saved Objects 視窗隨即開啟。預設會顯示使用者具有權限的所有租用戶，以及與這些租用戶相關聯的所有已儲存物件。

已儲存物件的彙總檢視是實驗性功能，由功能旗標控制，必須先在 `opensearch_dashboards.yml` 檔案中啟用，才能使用此功能。如需詳細資訊，請參閱[啟用彙總檢視](#enabling-aggregate-view-for-saved-objects)。
{: .note }

### 功能優點

- 在單一畫面中提供所有已儲存物件的彙總檢視，可讓您快速找到感興趣的物件，並確認與其相關聯的租用戶。找到物件後，您可以選取適當的租用戶並操作該物件。
- 此功能也會在 Saved Objects 表格中新增 Tenant 下拉式選單，讓您依租用戶及其相關聯的已儲存物件篩選檢視。

### 未來開發計畫

在後續版本中，我們計畫擴充此功能，讓您可以直接從彙總檢視執行動作及共用項目，無須先選取特定租用戶。長期而言，OpenSearch 計畫持續發展多租用戶功能，使其成為更具彈性的工具，讓使用者彼此共用物件，並採用更完善的方式指派促進共用的角色與權限。若要進一步瞭解未來版本的功能提案，請參閱 GitHub 上的 [Dashboards 物件共用](https://github.com/opensearch-project/security/issues/1869)議題。

### 已知限制

在開發的第一個實驗階段中，啟用此功能並在測試環境中使用前，應留意以下限制：

* 此功能只能用於新的叢集。已在使用中的叢集不支援此功能。
* 此外，此功能應僅用於測試環境，不應用於正式環境。 
* 最後，一旦在測試叢集中啟用並使用此功能，就無法再為該叢集停用此功能。在使用此功能操作租用戶與已儲存物件後將其停用，可能導致已儲存物件遺失，並影響租用戶之間的功能。透過下列三種方式中的任何一種停用此功能時，都可能發生這種情況：使用[功能旗標](#enabling-aggregate-view-for-saved-objects)停用彙總檢視功能；使用傳統的[多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/)設定停用多租用戶功能；或使用[動態組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/dynamic-config/)設定停用多租用戶功能。

這些限制將在即將推出的版本中解決。

## 啟用已儲存物件的彙總檢視

預設情況下，Saved Objects 表格中的彙總檢視為停用狀態。若要啟用此功能，請將 `opensearch_security.multitenancy.enable_aggregation_view` 旗標新增至 `opensearch_dashboards.yml` 檔案，並將其設為 `true`：

`opensearch_security.multitenancy.enable_aggregation_view: true`

啟用此功能後，您可以啟動新的叢集，然後啟動 Dashboards。 

## 在彙總檢視中操作

選取 **Tenant** 下拉式箭頭，以顯示使用者可用的租用戶清單。選單開啟時，您可以選取多個租用戶。每次在選單中選取租用戶時，已儲存物件清單都會依該租用戶，以及名稱旁有勾選標記的其他租用戶進行篩選。

![Dashboards Saved Objects 檢視，重點標示 Tenants 欄]({{site.url}}{{site.baseurl}}/images/Security/Tenant_column.png){: width="500" }
   
指定完租用戶後，請選取選單外的任意位置，將選單收合。 
* Title 欄顯示可用的已儲存物件名稱。 
* Tenant 欄顯示與已儲存物件相關聯的租用戶。 
* 此外，Tenant 下拉式選單標籤旁的紅色方框會顯示已選取用於篩選的租用戶數量。

![Dashboards Saved Objects 租用戶篩選]({{site.url}}{{site.baseurl}}/images/Security/ten-filter-results.png){: width="700" }

使用 **Type** 下拉式選單，依類型篩選已儲存物件。**Type** 下拉式選單的行為與 **Tenant** 下拉式選單相同。

### 選取並操作已儲存物件

找到您想操作的已儲存物件後，請依照下列步驟存取該物件：

1. 記下 Tenant 欄中與該物件相關聯的租用戶。
1. 在視窗右上角開啟使用者選單，並選取 **Switch tenants**。
   ![在使用者選單中切換租用戶]({{site.url}}{{site.baseurl}}/images/Security/switch_tenant.png){: width="425" }
1. 在 **Select your tenant** 視窗中，選擇 Global 或 Private 選項，或其中一個自訂租用戶選項，以指定正確的租用戶。選取 **Confirm** 按鈕。該租用戶隨即成為使用中的租用戶，並顯示在使用者選單中。
1. 租用戶成為使用中的租用戶後，您可以使用 Actions 欄中的控制項，操作與該租用戶相關聯的已儲存物件。
![Actions 欄控制項]({{site.url}}{{site.baseurl}}/images/Security/actions.png){: width="700" }

當租用戶未處於使用中狀態時，您無法使用 Actions 欄的控制項操作與其相關聯的物件。若要操作這些物件，請依照上述步驟，將該租用戶設為使用中的租用戶。
{: .note }

