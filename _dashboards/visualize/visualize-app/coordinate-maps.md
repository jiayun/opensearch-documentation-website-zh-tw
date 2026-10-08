---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "座標地圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 55
redirect_from:
  - /dashboards/visualize/coordinate-maps/
---

# 座標地圖

座標地圖會使用緯度和經度座標，在地圖上標繪地理資料點。每個標記代表一份含有 geo_point 欄位的文件，標記大小則表示該位置的彙總值。

## 何時使用座標地圖

使用座標地圖可呈現各地點的分布模式與空間相關性，例如客戶所在位置、服務涵蓋區域、事件分布，或具有地理座標的事件。您可以選取地理區域，以篩選同一儀表板上的其他視覺化。若要建立多圖層的地理視覺化，請使用 [Maps 應用程式]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/)。

## 建立座標地圖

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立座標地圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Coordinate Map**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。
2. 將時間篩選器設定為 **Last 7 days**。
3. 在 **Buckets** 下，選取 **Add** > **Geo coordinates**。
4. 將 **Aggregation** 設定為 **Geohash**，並將 **Field** 設定為 **OriginLocation**。
5. 選取 **Update**。

地圖會在航班出發地點顯示標記，標記大小與各地點的文件數量成正比，如下圖所示。

![顯示航班出發地的座標地圖]({{site.url}}{{site.baseurl}}/images/dashboards/coordinate-map-example.png)

### 自訂地圖顯示

1. 選取 **Options** 索引標籤。
2. 在 **Map type** 下，選取標記樣式：**Scaled Circle Markers**、**Shaded Circle Markers**、**Shaded Geohash Grid** 或 **Heatmap**。
3. 調整 **Precision** 以控制 geohash 桶 (bucket) 的大小（精確度越高，桶越小、數量越多）。
4. 選取 **Update**。

## 設定座標地圖

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Options 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Map type** | 標記樣式。支援的值：**Scaled Circle Markers**（依值調整大小）、**Shaded Circle Markers**（依值著色）、**Shaded Geohash Grid**（依值著色的矩形網格）、**Heatmap**（連續的色彩漸層）。 |
| **Precision** | 控制 geohash 網格的解析度。值越高，產生的桶越小、數量越多。 |
| **Show tooltips** | 啟用時，滑鼠游標停留時會顯示彙總值。 |
| **WMS compliant map server** | 啟用時，會使用 WMS 伺服器提供底圖。如需詳細資訊，請參閱[設定 Web Map Service]({{site.url}}{{site.baseurl}}/dashboards/visualize/maptiles/)。 |

## 相關文件

- [設定地圖]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-maps/)

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
