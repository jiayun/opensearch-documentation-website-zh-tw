---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位選取工具"
parent: Exploring data with Discover
grand_parent: Exploring data
nav_order: 40
---

# 使用欄位選取工具

根據預設，Discover 應用程式的 **Results** 表格會顯示表格中每份文件的所有欄位。在欄位選取工具中，您可以選取要在 **Results** 表格中顯示哪些資料欄位。

欄位選取工具位於 [Discover]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/) 應用程式窗格正左方的垂直面板中。它僅在 **Discover** 應用程式中提供。


## 導覽欄位選取工具

![Field select tool]({{site.url}}{{site.baseurl}}/images/dashboards/field-select-collapsed-callouts.png){: width="44%" }

欄位選取工具由下列元件組成。

- **Index patterns** 下拉式選單 (A) 顯示所有可用的索引模式。所選的索引模式決定載入哪些資料，因此也決定欄位選取工具中有哪些欄位可用。
- **Search field names** (B) 方塊會將欄位名稱與您的搜尋字串比對，以縮小選取工具中可用欄位的範圍。
- **Filter by type** 下拉式選單 (C) 會根據資料屬性 (例如資料類型和可搜尋性) 縮小可用欄位的範圍。
- **Selected fields** 清單 (D) 是所有已選取欄位的可摺疊清單。
- **Popular fields** 清單 (E) 是最近選取欄位的可摺疊清單。
- **Available fields** 清單 (F) 是所有尚未選取欄位的可摺疊清單。

**Selected fields**、**Popular fields** 和 **Available fields** 清單互斥。一個欄位只會出現在這些可摺疊清單的其中一個。
{: .important}


## 選取索引模式

在探索和視覺化資料之前，您必須先選取一個索引模式。

索引模式等同於傳統關聯式資料庫系統中的表格檢視。它定義了您想要探索和視覺化的資料集。如需建立索引模式的資訊，請參閱 [Index patterns]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。

若要選取索引模式，請依照下列步驟操作：

1. 在欄位選取工具中，從 **Index patterns** 下拉式選單選取一個索引模式。


## 選取要顯示的欄位

若要選取要在 **Results** 表格中顯示的欄位，請依照下列步驟操作：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-right-icon.png" class="inline-icon" alt="expand icon"/>{:/} (展開) **Available fields** 以展開 **Available fields**。

   如果該欄位最近曾經使用過，它可能會出現在 **Popular fields** 清單中，而非 **Available fields**。
   {: .note}

1. (選用) [使用 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="funnel icon"/>{:/} **Filter by type**](#filtering-fields-by-type   ) 彈出視窗，依類型縮小可用欄位的範圍。

1. (選用) 在 **Search field names** 方塊中輸入文字，以縮小可用欄位清單的範圍。

1. 在 **Available fields** 或 **Popular fields** 清單中選取一個欄位。

1. 選擇所選欄位的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/green-plus-icon.png" class="inline-icon" alt="green plus icon"/>{:/} (新增) 圖示。

   該欄位會以資料欄的形式新增至 **Discover** 應用程式窗格中的 **Results** 表格。

## 移除欄位

若要從 **Results** 表格的顯示中移除欄位，請依照下列步驟操作：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-right-icon.png" class="inline-icon" alt="expand icon"/>{:/} (展開) **Selected fields** 以展開 **Selected fields**。

1. 在 **Selected fields** 清單中選擇一個欄位。

1. 選擇所選欄位的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/red-cross-icon.png" class="inline-icon" alt="red cross icon"/>{:/} (移除) 圖示。

   該欄位會從 **Discover** 應用程式窗格中的 **Results** 表格移除。

   如果移除的欄位是最後一個已選取的欄位，**Results** 表格會恢復預設，顯示所有欄位。
   {: .note}


## 依類型篩選欄位

可用欄位的清單通常很長。為了避免捲動整份清單，可以在欄位選取工具中依資料類型，以及欄位是否可彙總或可搜尋來篩選欄位。

{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="funnel icon"/>{:/} **Filter by type** 右側的數字表示目前啟用的類型篩選數量。
{: .tip}

### 依資料類型篩選欄位

若要在欄位選取工具中依資料類型縮小欄位範圍，請依照下列步驟操作：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="funnel icon"/>{:/} **Filter by type**。

1. 在 **Filter by type** 彈出視窗中，從 **Type** 下拉式選單選取一種資料類型。

   欄位會限定為所選的類型。

   所有清單中的欄位都會受到限定：**Selected fields**、**Popular fields** 和 **Available fields**。
   {: .note}

### 依屬性篩選欄位

若要依屬性篩選欄位，請依照下列步驟操作：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="funnel icon"/>{:/} **Filter by type**。

1. 在 **Filter by type** 彈出視窗中，選取一個 **Aggregatable** 選項。例如，選取 **yes** 會篩選掉所有不可彙總的欄位。

1. 在 **Filter by type** 彈出視窗中，選取一個 **Searchable** 選項。例如，選取 **yes** 會篩選掉所有不可搜尋的欄位。

   可搜尋的欄位是指包含在反向索引中並可供搜尋的欄位。如需更多資訊，請參閱 [Index]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/)。

### 篩選缺少資料的欄位

若要篩選掉缺少資料的欄位，請依照下列步驟操作：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="funnel icon"/>{:/} **Filter by type**。

1. 在 **Filter by type** 彈出視窗中，啟用 **Hide missing fields** 切換開關。