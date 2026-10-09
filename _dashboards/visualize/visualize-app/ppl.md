---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "PPL 視覺化"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 140
redirect_from:
  - /dashboards/visualize/ppl/
---

# PPL 視覺化

Piped Processing Language (PPL) 視覺化可讓您使用 PPL 查詢來處理資料並建立視覺化。在 **New Visualization** 對話方塊中選取 **PPL**，即可開啟 Observability Logs Explorer。您可以在其中撰寫 PPL 查詢，並將結果對應至圖表。

## 何時使用 PPL 視覺化

如果您想直接使用 PPL 管線語法撰寫查詢，而不是透過點選式介面設定彙總，請使用 PPL 視覺化。如需詳細資訊，請參閱[可觀測性]({{site.url}}{{site.baseurl}}/observing-your-data/)和[探索資料]({{site.url}}{{site.baseurl}}/observing-your-data/exploring-observability-data/index/)。

## 建立 PPL 視覺化

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立 PPL 視覺化，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **PPL**。Observability Logs Explorer 隨即開啟。
2. 在 PPL 查詢列中輸入查詢。例如：

   ```sql
   source = opensearch_dashboards_sample_data_flights | stats count() by Carrier
   ```
   {% include copy.html %}

3. 將時間篩選器設定為包含資料的範圍（例如選取 **Last 7 days**）。
4. 選取 **Run**。
5. 選取 **Visualizations** 索引標籤以檢視圖表。
6. （選用）使用右側的圖表類型選取器變更圖表類型（例如 **Pie**）。

Explorer 會自動將查詢結果欄位對應至圖表。**Configuration** 面板會顯示 **Series**（指標）和 **Dimensions**（分組欄位），如下圖所示。

![以圓餅圖顯示各航空公司航班數的 PPL 視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/ppl-example.png)


## 相關文件

- [使用查詢建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/)

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。