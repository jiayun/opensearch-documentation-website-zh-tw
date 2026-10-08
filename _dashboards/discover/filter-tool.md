---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "篩選工具"
parent: Exploring data with Discover
grand_parent: Exploring data
nav_order: 30
---

# 使用篩選工具

篩選工具位於 [Discover]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)、[Dashboard]({{site.url}}{{site.baseurl}}/dashboards/dashboard/index/) 和 [Visualize]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/) 應用程式的頂端，就在 **[Search]({{site.url}}{{site.baseurl}}/dashboards/discover/search-bar/)** 搜尋列的正下方。您可以使用它來為這些應用程式中顯示的資料新增或移除離散篩選器。

 您可以建立任意數量的篩選器。篩選器列在 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示與 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/add-filter-icon.png" class="inline-icon" alt="add filter icon"/>{:/} (圓圈加號) **Add filter** 控制項之間的篩選器顯示區域中。


## 瀏覽篩選工具

![Filter tool]({{site.url}}{{site.baseurl}}/images/dashboards/filter-tool-callouts.png){: width="75%" }

篩選工具由以下元件組成：

- {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示 (A) 提供篩選選項的下拉式選單。
- 篩選器清單 (B) 顯示目前定義的篩選器。
- {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/add-filter-icon.png" class="inline-icon" alt="add filter icon"/>{:/} (圓圈加號) **Add filter** (C) 提供用於新增資料篩選器的彈出式選單。

## 新增篩選器

若要使用 **Add filter** 工具新增篩選器，請執行以下步驟：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/add-filter-icon.png" class="inline-icon" alt="add filter icon"/>{:/} (新增) **Add filter**。

1. 在 **Edit filter** 彈出視窗中，選擇一個資料欄位。

![Edit filter popover]({{site.url}}{{site.baseurl}}/images/dashboards/edit-filter-popover-filled.png){: width="79%" }

1. 在 **Operator** 欄位中，選擇一個運算子。

   **Operator** 下拉式選單的選項由所選資料欄位的類型決定。
   {: .note}

   如果需要，則會出現 Value 欄位。

1. 如果必要，請在 **Value** 欄位中輸入或選取一個值。

   **Value** 的輸入模式和選項由所選的運算子和資料欄位類型決定。
   {: .note}

1. (選用) 選擇 **Create custom label?**。

   自訂標籤會取代由資料欄位名稱和運算子組成的預設標籤。

1. 選取 **Save**。

## 編輯篩選器

若要變更現有篩選器，請執行以下步驟：

1. 在篩選器清單中選取該篩選器。

1. 在篩選器下拉式選單中，選取 **Edit filter>**。

1. 在 **Edit filter** 彈出視窗中，根據需要變更 **Field**、**Operator** 或 **Values**。

1. (選用) 新增或變更 **Custom label**。

1. 選取 **Save**。


## 移除篩選器

若要移除篩選器，請選擇篩選器名稱右側的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/} (叉號) 圖示。

## 停用篩選器

您可以暫時停用篩選器，而無需將其從篩選器清單中移除。若要停用篩選器，請執行以下步驟：

1. 在篩選器清單中選取該篩選器。

1. 在篩選器下拉式選單中，選取 **Temporarily disable**。

   已停用的篩選器名稱會以 ~~刪除線~~ 文字顯示。
   {: .note}

## 重新啟用篩選器

若要啟用已停用的篩選器，請執行以下步驟：

1. 在篩選器清單中選取一個 ~~已停用~~ 的篩選器。

1. 在篩選器下拉式選單中，選取 **Re-enable**。


## 固定篩選器

您可以固定篩選器，使其適用於 OpenSearch Dashboards 中的所有應用程式 (Discover、Dashboards 和 Visualize)。若要固定篩選器，請執行以下步驟：

1. 在篩選器清單中選取該篩選器。

1. 在篩選器下拉式選單中，選取 **Pin across all apps**。


## 取消固定篩選器

若要取消固定已固定到所有應用程式的篩選器，請執行以下步驟：

1. 在篩選器清單中選取該篩選器。

1. 在篩選器下拉式選單中，選取 **Unpin**。


## 將所有篩選器作為群組進行修改

您可以使用 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) **Filters** 下拉式選單，透過多種方式一次變更所有篩選器。

使用 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) **Filters** 下拉式選單所做的修改僅適用於篩選器清單中的篩選器，不適用於 **Search** 搜尋列中的查詢或時間篩選器。
{: .note}

### 啟用或停用所有篩選器

若要啟用或停用所有篩選器，請執行以下步驟：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示。

1. 在 **Filters** 下拉式選單中，選取 **Enable all** 或 **Disable all**。


### 反轉已啟用的篩選器

若要排除所有已包含的篩選器並包含所有已排除的篩選器，請執行以下步驟：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示。

1. 在 **Filters** 下拉式選單中，選取 **Invert enabled/disabled**。


### 反轉所有篩選器的包含意義

若要否定所有篩選器運算式，使所有包含的文件被排除，且所有排除的文件被包含，請執行以下步驟：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示。

1. 在 **Filters** 下拉式選單中，選取 **Invert inclusion**。

   排除篩選器的標題會附加 **NOT**，如下所示。再次反轉包含關係將移除 **NOT** 修飾詞。
   
   ![Exclusion filter]({{site.url}}{{site.baseurl}}/images/dashboards/excluded-filter.png){: width="36%" }

   已停用的篩選器會被反轉，但仍保持停用狀態。
   {: .note}

### 固定或取消固定所有篩選器

若要在所有 OpenSearch Dashboards 應用程式 (Discover、Dashboards 和 Visualize) 中固定或取消固定所有篩選器，請執行以下步驟：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示。

1. 在 **Filters** 下拉式選單中，選取 **Pin all** 或 **Unpin all**。


### 移除所有篩選器

若要從篩選器清單中移除所有篩選器，請執行以下步驟：

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/funnel-icon.png" class="inline-icon" alt="filter menu icon"/>{:/} (漏斗) 圖示。

1. 在 **Filters** 下拉式選單中，選取 **Remove all**。
