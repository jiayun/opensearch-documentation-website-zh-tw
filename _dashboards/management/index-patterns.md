---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引模式"
parent: Connecting data sources
nav_order: 10
---

# 索引模式

索引模式是存取 OpenSearch 資料的必要元素。_索引模式_會參照一或多個索引、資料串流或索引別名。例如，索引模式可以指向您昨天的記錄資料，或包含該資料的所有索引。

如果您將資料儲存在多個索引中，建立索引模式可讓您的視覺化從所有符合該索引模式的索引中擷取資料。您需要建立索引模式來定義資料的擷取方式以及欄位的格式，以便查詢、搜尋及顯示資料。



## 先決條件

在建立索引模式之前，您的資料必須已編製索引。若要了解如何在 OpenSearch 中將資料編製索引，請參閱[管理索引]({{site.url}}{{site.baseurl}}/im-plugin/index/)。

> 若要建立或修改索引模式，您的角色必須具備下列權限：
> - `kibana_user` 角色（或同等角色），此角色會授予 OpenSearch Dashboards 的存取權。
> - 您要在其中建立索引模式之租用戶的 `kibana_all_write` 租用戶權限。若具備 `kibana_all_read`，您可以檢視現有的索引模式，但無法建立或修改索引模式。
> - 索引模式將會符合之索引的讀取權限。
>
> 如需協助，請聯絡您的管理員。如需租用戶權限的詳細資訊，請參閱[多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/#give-roles-access-to-tenants)。如需角色的詳細資訊，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#predefined-roles)。
{: .note}

## 建立索引模式

如果您已新增範例資料，您就會有可用來分析該資料的索引模式。若要為您自己的資料建立索引模式，請依照下列步驟操作。

### 步驟 1：定義索引模式

1. 前往 OpenSearch Dashboards，然後選取 **Management** > **Dashboards Management** > **Index patterns**。
2. 選取 **Create index pattern**。
3. 在 **Create index pattern** 視窗中，於 **Index pattern name** 欄位輸入索引模式的名稱，以定義索引模式。當您開始輸入時，Dashboards 會自動加入萬用字元 `*`。使用萬用字元有助於讓索引模式符合多個來源或索引。當您開始輸入時，會出現一個下拉式清單，顯示所有符合您索引模式的索引。
4. 選取 **Next step**。

下圖顯示步驟 1 的範例。請注意，索引模式 `security*` 符合三個索引。透過使用萬用字元 `*` 定義模式，您可以查詢並視覺化索引中的所有資料。

![索引模式步驟 1 使用者介面]({{site.url}}{{site.baseurl}}/images/dashboards/index-patterns-step1.png){: width="700" }

### 步驟 2：設定各項設定

1. 從下拉式選單中選取 `@timestamp`，以指定 OpenSearch 依時間篩選文件時要使用的時間欄位。選取此時間篩選條件會決定時間篩選條件要套用至哪個欄位。該欄位可以是請求的時間戳記，或任何相關的時間戳記欄位。如果您不想使用時間篩選條件，請從下拉式選單中選取該選項。如果您選取此選項，OpenSearch 會傳回符合該模式之索引中的所有資料。

2. 選取 **Create index pattern.**。下圖顯示一個範例。

    ![索引模式步驟 2 使用者介面]({{site.url}}{{site.baseurl}}/images/dashboards/index-pattern-step2.png){: width="700" }

建立索引模式後，您可以檢視相符索引的對應。在表格中，您可以看到欄位清單，以及欄位的資料類型和屬性。下圖顯示一個範例。

![索引模式表格使用者介面]({{site.url}}{{site.baseurl}}/images/dashboards/index-pattern-table.png){: width="700" }

## 最佳實務

建立索引模式時，請考慮下列最佳實務：

- **讓索引模式具體明確**：與其建立符合所有索引的索引模式，不如建立符合所有以特定前置詞開頭之索引的索引模式，例如 `my-index-`。索引模式越具體，就越有利於查詢和分析您的資料。
- **謹慎使用萬用字元**：萬用字元在比對多個索引時很實用，但也可能讓索引模式更難管理。請盡可能具體地使用萬用字元。
- **測試您的索引模式**：請務必測試您的索引模式，確保其符合正確的索引。

## 後續步驟

- [透過視覺效果了解您的資料]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)。
- [深入探索您的資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。
