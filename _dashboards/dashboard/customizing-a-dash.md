---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自訂儀表板"
parent: Creating dashboards
nav_order: 30
has_children: false
---

# 自訂儀表板

您可以使用以下方式自訂儀表板：

- [調整面板大小](#resizing-a-panel)。
- [移動面板](#moving-a-panel)。
- [以全螢幕模式檢視面板](#using-full-screen-mode)
- [自訂](#customizing-a-visualization-panel)視覺化圖表中的標題、圖例或顏色。


## 前置條件

您只能在開啟儀表板進行編輯時自訂儀表板。請參閱 [開啟儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/opening-a-dashboard/)。


### 調整面板大小

若要調整面板大小，請執行以下步驟：

1. 選取並按住面板右下角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/resize-icon.png" class="inline-icon" alt="resize icon"/>{:/} (調整大小) 圖示。

1. 拖曳至新的尺寸。

   其他面板會自動移開以適應新的面板大小。


### 移動面板

若要移動面板，請執行以下步驟：

1. 選取並按住面板標題或面板頂部，如以下圖片所示。

![在 Dashboards 中拖曳面板]({{site.url}}{{site.baseurl}}/images/dashboards/dash-panel-grab.png){: width="50%" }

1. 將面板拖曳至新位置。

   其他面板會自動移開以適應新的面板位置。

## 使用全螢幕模式

您可以以全螢幕模式檢視單一視覺化面板，然後返回儀表板模式。


### 以全螢幕模式檢視面板

若要以全螢幕模式檢視面板，請執行以下步驟：

1. 選擇面板右上角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/more-icon.png" class="inline-icon" alt="ellipses icon"/>{:/} (省略號) 圖示。

   只有在您將指標移至視覺化面板時，才會顯示 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/more-icon.png" class="inline-icon" alt="ellipses icon"/>{:/} (省略號) 圖示。
   {: .note}

1. 在 **Options** 下拉選單中，選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/maximize-icon.png" class="inline-icon" alt="maximize icon"/>{:/} (最大化) **Maximize panel**。


### 將面板從全螢幕模式還原

若要將面板從全螢幕模式還原，請執行以下步驟：

1. 選擇面板右上角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/more-icon.png" class="inline-icon" alt="ellipses icon"/>{:/} (省略號) 圖示。

   只有在您將指標移至視覺化面板時，才會顯示 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/more-icon.png" class="inline-icon" alt="ellipses icon"/>{:/} (省略號) 圖示。
   {: .note}

1. 選取 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/minimize-icon.png" class="inline-icon" alt="minimize icon"/>{:/} (最小化) **Minimize**。


## 自訂視覺化面板

您可以自訂儀表板中視覺化面板的以下面向：

- [隱藏或顯示圖例](#hiding-and-displaying-the-legend)。
- [變更視覺化圖表中的顏色](#changing-a-color)。
- [變更或隱藏面板標題](#changing-or-hiding-the-panel-title)。

### 隱藏與顯示圖例

若要顯示或隱藏面板圖例：

- 選擇面板左下角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/list-icon.png" class="inline-icon" alt="list icon"/>{:/} (清單) 圖示。

### 變更顏色

若要變更視覺化圖表中的顏色，請執行以下步驟：

1. 從視覺化圖例中選取一個類別。

1. 從彈出式選單中選取顏色。

    視覺化圖形會根據您的變更而更新。

    顏色變更僅儲存於目前的面板和儀表板中，不會影響已儲存的視覺化圖表。
    
<!--     To change the color in the visualization, see [Visualization colors]({{site.url}}{{site.baseurl}}/dashboards/visualize/viz-tool-ref/#visualization-colors).
    {: .note}
 -->

### 變更或隱藏面板標題

若要顯示、隱藏或自訂面板標題，請執行以下步驟：

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/gear-icon.png" class="inline-icon" alt="gear icon"/>{:/} (齒輪) 圖示。

1. 從 **Options** 視窗中，選取 **Edit panel title**。

1. 從 **Customize panel** 對話框中，在 **Panel title** 下輸入標題。

1. (選用) 切換 **Show panel title** 以隱藏標題。

1. 選擇 **Save**。

    變更面板標題僅會影響目前儀表板上的面板。此變更不會影響任何其他儀表板上的視覺化圖表，也不會影響包含該視覺化圖表的任何其他面板。
    {: .note}


## 後續步驟

如果您對儀表板進行了想要保留的變更，請儲存儀表板。請參閱 [儲存儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/managing-a-dash/#saving-a-dashboard)。