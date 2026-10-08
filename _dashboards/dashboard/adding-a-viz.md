---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將視覺化新增至儀表板"
parent: Creating dashboards
nav_order: 20
has_children: false
---

# 將視覺化新增至儀表板

您可以將現有的面板新增至儀表板，或直接在儀表板中建立新的視覺化。

## 前置條件

您僅在開啟儀表板進行編輯時，才能將視覺化新增至儀表板。請參閱 [開啟儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/opening-a-dashboard/)。


## 在儀表板中建立新的視覺化

您可以在儀表板中建立新的視覺化，但不能建立新的搜尋。

若要將搜尋新增至儀表板，您必須先在 Discover 應用程式中建立，然後再將其新增。請參閱 [使用 Discover 探索資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。
{: .note}

若要在儀表板中建立新的視覺化，請執行以下步驟：

1. 從應用程式工具列中，選擇 **Create new**。

1. 從 **New Visualization** 視窗中，選擇視覺化類型。

1. 在 **New _\<type\>_/Choose a source** 對話框中，選取索引模式。

   在此步驟中，Maps 和 VisBuilder 等進階視覺化工具將來源選取功能內建於工具中，而不會顯示來源選取對話框。
   {: .note}

1. Dashboards 應用程式會開啟 Visualize 編輯器，並顯示預設的 (count) 視覺化。

<!-- Edit the visualization as described in [Building visualizations]({{site.url}}{{site.baseurl}}/dashboards/visualize/viz-index/#building-visualizations). -->
   
1. 儲存該視覺化。

<!-- See [Saving a new visualization]({{site.url}}{{site.baseurl}}/dashboards/visualize/saving-a-viz/#saving-a-new-visualization). -->

   請確保 **Save visualization** 對話框中的 **Add to dashboard after saving** 切換按鈕已選取。
   
   當您透過在儀表板中建立來新增視覺化時，**Save visualization** 對話框中的 **Save** 按鈕會顯示為 **Save and return**。
   {: .note}

## 將面板新增至儀表板

若要將視覺化或搜尋新增至儀表板，請執行以下步驟：

1. 在應用程式功能表中，選取 **Add**。

   應用程式會顯示 **Add panels** 對話框。

1. (選用) 在 **Search** 欄位中，輸入詞彙以篩選面板清單。

   搜尋 _不_ 區分大小寫。不允許使用特殊字元，即使面板名稱中允許使用這些字元。

1. (選用) 在 Sort 下拉式選單中，選擇 Ascending 或 Descending 以選取字母升冪或降冪排序。

   排序 _會_ 區分大小寫。排序中包含特殊字元。例如，搜尋 `ecommerce` 會將所有這些視覺化包含在篩選清單中：`[eCommerce] Markdown`、`[Ecommerce] Order Count` 和 `eCommerce Orders`。

1. (選用) 在 **Types** 下拉式選單中，選取一個或多個面板類型。該下拉式選單包含視覺化、搜尋以及特殊的視覺化類型，例如 **Maps** 和 **VisBuilder** 面板。如果未選取任何項目，則篩選器預設包含所有類型。

1. (選用) 在 Rows per page 下拉式選單中，選取每個對話框頁面要列出的面板數量。預設為 10。

1. (選用) 從頁碼清單中選取要跳轉的頁碼，或使用 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-right-icon.png" class="inline-icon" alt="right icon"/>{:/} (右) 和 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/arrow-left-icon.png" class="inline-icon" alt="left icon"/>{:/} (左) 圖示翻頁。

1. 從清單中選取一個或多個面板。

   對話框會保持啟動狀態，以便您可以選擇多個面板新增至儀表板。
   {: .note}

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/} (叉叉) 圖示以關閉對話框。

