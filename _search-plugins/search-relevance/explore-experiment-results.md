---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "探索搜尋評估結果"
nav_order: 65
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_children: false
---

# 探索搜尋評估結果
**於 3.2 版推出**
{: .label .label-purple }

除了使用 API 擷取實驗結果之外，您也可以以視覺化方式探索結果。Search Relevance Workbench 隨附了一些儀表板，您可以安裝這些儀表板來檢閱搜尋評估與混合搜尋最佳化實驗的結果。

## 安裝儀表板

您可以使用下列其中一種方式安裝儀表板：

* 在實驗總覽的 **Actions** 欄中，選取視覺化圖示。

* 選取實驗總覽右上角的 **Install Dashboards** 按鈕。

![Search Relevance Workbench 的實驗總覽，包含儀表板安裝選項]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/experiment_overview_dashboard_installation_options.png)

此強制回應視窗會提供為使用者安裝儀表板的選項。

![安裝儀表板的強制回應視窗]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/install_dashboards_modal.png)

## 使用儀表板

安裝儀表板之後，請在實驗總覽的 **Actions** 欄中選取視覺化圖示。這會開啟實驗結果儀表板。顯示的檢視取決於您選擇的實驗類型：

* 搜尋評估儀表板著重於個別查詢層級，並提供效能良好查詢以及仍有相關性提升空間之查詢的深入解析。

* 混合搜尋儀表板提供不同混合搜尋參數組態效能表現的總覽，並讓您找出可進一步探索與實驗的候選查詢。

### 搜尋評估儀表板

如下圖所示的搜尋評估儀表板，會彙總您所選實驗中所有查詢的效能指標。使用搜尋評估儀表板可取得整體實驗效能的高階檢視，並找出需要留意的查詢。

![包含視覺化的搜尋評估儀表板]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/search_evaluation_dashboard.png)

**Deep Dive Summary** 面板會顯示 NDCG、MAP、精確度與涵蓋率的彙總指標（請參閱[評估搜尋品質]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/)）。

**Deep Dive Query Scores** 窗格會顯示依 NDCG 分數排序（由高至低）的個別查詢效能。使用此窗格可找出效能最佳與最差的查詢。

**Deep Dive Score Densities** 窗格會顯示指標值在您查詢集中的分布情形。使用此窗格可了解效能不佳的情況是普遍存在，還是集中在特定查詢。x 軸顯示指標值，而 y 軸則顯示這些值出現的頻率。

**Deep Dive Score Scatter Plot** 窗格會顯示前述分布資料的互動式檢視，並將每個查詢顯示為個別資料點。使用此窗格可調查效能極端值的特定查詢。資料點會以垂直方式分散以避免重疊，同時維持與前述分布檢視相同的 x 軸指標值。

### 混合搜尋評估儀表板

使用如下圖所示的混合搜尋評估儀表板，可比較實驗變體並找出混合實驗的最佳參數組態。

![包含視覺化的混合搜尋最佳化評估儀表板]({{site.url}}{{site.baseurl}}/images/search-relevance-workbench/hybrid_search_optimizer_dashboard.png)

**Variant Performance Chart** 會以視覺方式依效能由佳至差排列實驗變體（從左至右，NDCG 逐漸降低）。使用此圖表可快速找出效能最佳的查詢，並一眼看出不同參數組合的效能模式。

**Variant Performance** 窗格會以可排序的表格格式顯示相同的變體資料，並呈現所有指標。使用此窗格可比較各變體的特定指標值，並透過依不同效能衡量指標排序來自訂您的分析。若要依某欄排序，請選取該欄的標題。


### 自訂儀表板

這些儀表板會以已儲存物件的形式安裝。安裝之後，您可以編輯儀表板，或將其複製並自訂以符合您的特定需求。

若要了解如何自訂來源檔案，請參閱[更新預設儀表板](https://github.com/opensearch-project/dashboards-search-relevance/blob/main/DEVELOPER_GUIDE.md#updating-default-dashboards)。

### 重設儀表板

若要重設儀表板，請選取實驗總覽右上角的 **Install Dashboards** 按鈕。這會重新安裝儀表板。
