---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "儀表板教學"
parent: Creating dashboards
nav_order: 5
has_children: false
---

# 教學：建立儀表板

您可以使用 OpenSearch Dashboards 中的 **Dashboards** 應用程式，建立一個包含多種資料視覺呈現方式的頁面。

請透過以下教學，了解如何使用 **Dashboards** 應用程式和 OpenSearch 範例資料建立儀表板。範例資料集已附有現成的範例視覺化，您可以將其用於儀表板，也可以自行建立視覺化。本教學將示範這兩種做法。

如需 Dashboards 使用者介面的概觀，請參閱[瀏覽 Dashboards 應用程式使用者介面]({{site.url}}{{site.baseurl}}/dashboards/dashboard/#navigating-the-dashboards-application-ui)。

## 先決條件

本頁的教學使用 [**Sample eCommerce data**](https://playground.opensearch.org/app/home#/tutorial_directory) 資料集，此資料集已安裝在 [OpenSearch Playground](https://playground.opensearch.org/app/home#/) 中。

如果您使用的是本機安裝的 OpenSearch Dashboards，且尚未新增範例資料，請參閱[準備您的資料]({{site.url}}{{site.baseurl}}/dashboards/getting-started/data-setup/#add-sample-data)。

以下教學假設您使用的是現有安裝的 OpenSearch Dashboards，或是 [OpenSearch Playground](https://playground.opensearch.org/app/home#/)。視您使用的環境而定，某些功能可能無法使用。例如，您現有的安裝可能未包含範例資料集，而 OpenSearch Playground 則無法儲存儀表板。
{: .note}

## 建立儀表板

若要建立新的儀表板，請依照下列步驟操作：

1. | 在傳統導覽中 | 在工作區導覽中 |
   | :-- | :-- |
   | - 選取 **OpenSearch Dashboards** > **Dashboards**。<br/>- 選取 **Dashboards**。 | 選取 **Dashboards**。 |

1. | 在傳統導覽中 | 在工作區導覽中 |
   | :-- | :-- |
   | - 在 Dashboards 面板中，選取 **Create**。<br/>- 從下拉式選單中選取 **Dashboard**。 | 從應用程式選單中選取 **Create Dashboard**。 |

## 新增現有的視覺化

若要將已儲存的視覺化新增至儀表板，請依照下列步驟操作：

1. 在應用程式面板中，選擇 **Add an existing**。

1. 在 **Add panels** 對話方塊中，於 **Search** 方塊輸入 `ecommerce`，以篩選可用的視覺化清單。

1. 在 **Add panels** 對話方塊中，選擇 **[eCommerce] Sales by Category**。

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/}（叉號）圖示以關閉對話方塊。

1. 使用[時間篩選器]({{site.url}}{{site.baseurl}}/dashboards/discover/time-filter/)選取 `Last 2 years` 作為時間範圍，如下圖所示。

![時間篩選器設定為過去 2 年]({{site.url}}{{site.baseurl}}/images/dashboards/dash-tut-time-2-years.png){: width="40%" }

1. 在區域圖中拖曳選取一段狹窄的資料範圍，如下圖所示。

   ![顯示拖曳選取的視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/dash-tut-sales-drag.png){: width="60%" }

   資料會調整為延展至整個資料顯示區域的寬度，刻度也會自動調整，如下圖所示。

   ![依類別顯示銷售額的區域視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/dash-tut-sales-area.png){: width="60%" }

   以互動方式選取日期範圍，會產生絕對時間間隔。
{: .note}

您已建立一個只有單一面板的儀表板，接下來您會在本教學中繼續修改它。請依照下一節的說明儲存儀表板。


## 儲存儀表板

若要儲存新的儀表板，請依照下列步驟操作：

1. 在 **Dashboards** 工具列中，選擇 **Save**。

1. 在 **Save dashboard** 對話方塊中，於 **Title** 方塊輸入 `[Ecommerce] tutorial dashboard`。

1. 選取 **Store time with dashboard**，將時間篩選器與儀表板一併儲存。

1. 選擇 **Save**。

1. 從應用程式選單中選擇 **Edit**，以繼續編輯儀表板。


## 建立視覺化

若要在 **Dashboards** 中建立新的視覺化，請依照下列步驟操作：

1. 在應用程式工具列中，選擇 **Create new**。

1. 在 **New Visualization** 視窗中，選擇 **Metric**。

1. 在 **New Metric/Choose a source** 對話方塊中，選取索引模式 **opensearch_dashboards_sample_data_ecommerce**。

1. 在工具列中，選擇 **Save**。

1. 在 **Save visualization** 對話方塊中，輸入視覺化的標題。在本教學中，請輸入 `[eCommerce] Order Count`。

1. 選擇 **Save and return**。

   **Dashboards** 應用程式會儲存此指標視覺化，並將其新增至儀表板，如下圖所示。

   ![包含 Sales by Category 與 Order Count 指標面板的儀表板]({{site.url}}{{site.baseurl}}/images/dashboards/dash-tut-combined.png)


## 新增後續面板

將 Markdown 視覺化新增至儀表板。請依照下列步驟操作：

1. 在儀表板工具列中，選擇 **Add**。

1. 在 **Add panels** 對話方塊中，選擇 **[eCommerce] Markdown**。

1. 選擇 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/cross-icon.png" class="inline-icon" alt="cross icon"/>{:/}（叉號）圖示以關閉對話方塊。

   **Dashboards** 應用程式會將 Markdown 面板新增至儀表板，如下圖所示。

   ![範例儀表板]({{site.url}}{{site.baseurl}}/images/dashboards/dash-tut-three-panel.png)


## 整理儀表板

您可以透過調整面板大小及重新排列面板來整理儀表板。移動 Markdown 面板並調整其大小，使其作為儀表板的標題與說明。請依照下列步驟操作：

1. 在面板頂端、{::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/gear-icon.png" class="inline-icon" alt="options icon"/>{:/}（選項）圖示左側的任意位置選取並按住。

1. 將面板拖曳至應用程式面板的頂端。

   當您向上移動 Markdown 面板時，Sales by Category 面板會自動與其交換位置。
1. 選取並按住面板右下角的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/resize-icon.png" class="inline-icon" alt="resize icon"/>{:/}（調整大小）圖示。

1. 拖曳以將面板拉長並縮窄，使其成為橫跨儀表板整個上方區域的橫幅。

   指標面板會自動向下移動，為調整大小後的 Markdown 面板騰出空間。

   完成後的儀表板應如下圖所示。

   ![範例儀表板]({{site.url}}{{site.baseurl}}/images/dashboards/dash-tut-banner.png)

1. 儲存您的儀表板。請參閱[儲存儀表板](#saving-a-dashboard)。