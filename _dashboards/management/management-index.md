---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Dashboards 管理"
nav_order: 130
has_children: true
has_toc: false
---

# Dashboards 管理
於 2.10 版推出
{: .label .label-purple }

**Dashboards Management** 是直接在 OpenSearch Dashboards 中管理及自訂 OpenSearch 資料的中央樞紐。與管理員設定的部署層級設定不同，**Dashboards Management** 是您從 OpenSearch Dashboards 存取的產品內應用程式。您可以使用它設定資料存取，例如索引模式、資料來源、已儲存物件和進階設定，而不需要編輯組態檔案或存取主機。

OpenSearch 和 OpenSearch Dashboards 權限控管個別功能的存取。如果您沒有適當的存取權限，請洽詢您的管理員。
{: .warning}

## 應用程式

若要開啟 **Dashboards Management**，在傳統導覽中，請選取 **Management** > **Dashboards Management**。在工作區導覽中，這些應用程式位於 **Settings and setup** 選單中。

您可以在 **Dashboards Management** 中存取下列應用程式：

- **[Index Patterns]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)**：若要存取 OpenSearch 資料，您需要建立索引模式，以便選取要使用的資料並定義欄位的屬性。**Index Pattern** 工具可讓您從 UI 中建立索引模式。索引模式會指向一個或多個索引、資料串流或索引別名。
- **[Data Sources]({{site.url}}{{site.baseurl}}/dashboards/management/multi-data-sources/)**：**Data Sources** 工具用於設定和管理 OpenSearch 用來收集及分析資料的資料來源。您可以使用此工具在您的 [OpenSearch Dashboards 組態檔案](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml)副本中指定來源組態。
- **[Saved Objects]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects/)**：**Saved Objects** 工具可協助您整理和管理已儲存物件。已儲存物件是儲存資料以供日後使用的檔案，例如儀表板、視覺化和地圖。您可以使用此工具[匯出和匯入這些物件]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects/)，例如將儀表板複製到另一個叢集，或使用 [Saved Objects API]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects-api/) 以程式設計方式執行相同的操作。
- **[Advanced Settings]({{site.url}}{{site.baseurl}}/dashboards/management/advanced-settings/)**：**Advanced Settings** 工具讓您能彈性地個人化 OpenSearch Dashboards 的行為。此工具分為多個設定區段，例如 General、Accessibility 和 Notifications，您可以使用它自訂及最佳化許多 Dashboards 設定。
- **[Resource Access Management]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/)**（若已啟用資源共用）：**Resource Access Management** 工具為外掛程式定義的資源提供精細的存取控制，例如機器學習 (ML) 模型群組、異常偵測器和報告定義。您可以與特定使用者、角色或後端角色共用資源，並控制其存取層級。

## 相關文件

- 若要透過編輯 `opensearch_dashboards.yml` 檔案來設定部署層級設定，例如品牌和網路壓縮，請參閱[設定與管理]({{site.url}}{{site.baseurl}}/dashboards/settings-and-administration/)。