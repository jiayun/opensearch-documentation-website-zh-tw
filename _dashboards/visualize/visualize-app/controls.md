---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "控制項"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 50
redirect_from:
  - /dashboards/visualize/controls/
---

# 控制項視覺化
**實驗性**
{: .label .label-purple }

這是一項實驗性功能，不建議在正式環境中使用。若要取得此功能的進度更新或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)上的討論。
{: .warning}

控制項視覺化會在儀表板中加入互動式篩選面板。控制項可讓您篩選資料，而無須修改儀表板本身。

控制項不需要資料來源。您會在每個個別控制項中設定資料來源。

## 何時使用控制項

使用控制項來篩選儀表板中的資料。許多視覺化已內建資料選取篩選功能。對於尚未提供資料選取功能的視覺化，或要強化現有視覺化的資料選取功能時，請使用控制項。

## 控制項類型

提供兩種類型的控制項：

- **Range slider**：為數值欄位定義最小值與最大值。
- **Options list**：提供下拉式選單，以從欄位中選取值。

## 建立控制項視覺化

若要建立控制項視覺化，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Controls**。
2. 選取 **Controls** 索引標籤。
3. 從 **Type** 下拉式選單中，選取 **Range slider** 或 **Options list**。
4. 選取 **Add**。

下圖顯示一個控制項視覺化，其中包含兩個 Options list 控制項（Origin City 與 Destination City）以及一個 Range slider 控制項（Average Ticket Price）。

![包含下拉式選單與範圍滑桿的控制項視覺化]({{site.url}}{{site.baseurl}}/images/dashboards/controls-example.png)

### 設定範圍滑桿

1. 在 **Control Label** 中，輸入顯示於控制項上的標籤。
2. 從 **Index Pattern** 中選取資料來源。
3. 從 **Field** 中選取數值欄位。
4. （選用）設定 **Step Size**（最小增量）與 **Decimal Places**。
5. 選取 **Update**。

### 設定選項清單

1. 在 **Control Label** 中，輸入顯示於控制項上的標籤。
2. 從 **Index Pattern** 中選取資料來源。
3. 從 **Field** 中選取要作為篩選依據的欄位。
4. （選用）啟用 **Multi-select**，以允許選取多個值。
5. （選用）啟用 **Dynamic Options**，以自動調整下拉式選單項目（僅限文字欄位）。
6. 若停用 **Dynamic Options**，請設定 **Size**（顯示的項目數量）。

   控制項只會顯示前 **Size** 個值，依資料欄位的排序方式決定。
   {: .note}

7. 選取 **Update**。

您可以重複上述步驟，在單一視覺化中新增多個控制項。

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
