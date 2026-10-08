---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "區域地圖"
parent: Visualization types
grand_parent: Creating visualizations in the Visualize application
great_grand_parent: Building data visualizations
nav_order: 145
redirect_from:
  - /dashboards/visualize/region-maps/
  - /dashboards/visualize/geojson-regionmaps/
  - /dashboards/geojson-regionmaps/
---

# 區域地圖

區域地圖會根據彙總值為地理區域（國家、州或郡）著色，並以色彩深淺呈現指標在各區域間的差異。

## 何時使用區域地圖

使用區域地圖比較依地理邊界彙總的資料值，例如各國的銷售額、各州的人口或各郡的事件數。若要建立多圖層的地理視覺化，請使用 [Maps 應用程式]({{site.url}}{{site.baseurl}}/dashboards/visualize/maps/)。

## 建立區域地圖

本頁的範例使用 **Sample flight data** 資料集。開始之前，請先完成[先決條件]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/#prerequisites)。
{: .note}

若要建立區域地圖，請依照下列步驟操作：

1. 在 **New Visualization** 對話方塊中，選取 **Region Map**，然後選取您的索引模式（例如 **opensearch_dashboards_sample_data_flights**）。
2. 將時間篩選器設定為 **Last 7 days**。
3. 在 **Buckets** 下，選取 **Add** > **Shape field**。
4. 將 **Aggregation** 設定為 **Terms**，並將 **Field** 設定為 **OriginCountry**。
5. 選取 **Update**。

地圖會依航班數量為每個國家著色，如下圖所示。

![依出發國家顯示航班數量的區域地圖]({{site.url}}{{site.baseurl}}/images/dashboards/region-map-example.png)

### 自訂地圖顯示

1. 選取 **Options** 索引標籤。
2. 在 **Layer settings** 下，選取向量地圖（例如 **World Countries**）。
3. 在 **Join field** 中，選取向量地圖中與您的資料相符的欄位（例如 `ISO 3166-1 alpha-2`）。
4. 在 **Style settings** 下，調整色彩配置。
5. 選取 **Update**。

## 搭配 GeoJSON 使用自訂向量地圖

如果內建的向量地圖未包含您需要的區域（例如美國的郡或郵遞區號），您可以上傳自訂的 GeoJSON 檔案。

若要搭配 GeoJSON 使用自訂向量地圖，請安裝下列外掛程式：
- OpenSearch Dashboards Maps [`dashboards-maps`](https://github.com/opensearch-project/dashboards-maps) 前端外掛程式
- OpenSearch [`geospatial`](https://github.com/opensearch-project/geospatial) 後端外掛程式
{: .note}

### 上傳自訂 GeoJSON 檔案

1. 準備副檔名為 `.geojson` 或 `.json` 的 JSON 檔案。
2. 在 **Region Map** 編輯器右側面板中，選取 **Import Vector Map**。
3. 在 **Upload map** 中，選取或拖放您的 JSON 檔案。
4. 輸入 **Map name prefix**（例如 `usa-counties`）。地圖名稱會變成 `<prefix>-map`。
5. 選取 **Import file**，然後在確認快顯視窗中選取 **Refresh**。

### 選取自訂向量地圖

1. 在 **Layer Options** > **Layer settings** 中，選取 **Custom vector map**。
2. 在 **Vector map** 下，選取您上傳的地圖。
3. （選用）在 **Style settings** 下，增加 **Border thickness** 以提高辨識度。
4. 選取 **Update**。

### GeoJSON 檔案範例

下列 GeoJSON 檔案定義了兩個美國的郡：

```json
{
  "type": "FeatureCollection",
  "name": "usa counties",
  "features": [
    {
      "type": "Feature",
      "properties": { "iso2": "US", "iso3": "LA-CA", "name": "Los Angeles County", "country": "US", "county": "LA" },
      "geometry": { "type": "Polygon", "coordinates": [[[-118.718, 34.071], [-118.696, 34.034], [-118.570, 34.030], [-118.488, 33.957], [-118.372, 33.861], [-118.455, 33.756], [-118.339, 33.715], [-118.229, 33.756], [-118.141, 33.679], [-117.911, 33.578], [-117.751, 33.496], [-117.559, 33.555], [-117.307, 33.596], [-117.070, 33.674], [-116.697, 34.062], [-116.944, 34.284], [-117.180, 34.430], [-117.378, 34.543], [-117.625, 34.570], [-118.048, 34.615], [-118.449, 34.543], [-118.619, 34.389], [-118.740, 34.212], [-118.718, 34.071]]] }
    },
    {
      "type": "Feature",
      "properties": { "iso2": "US", "iso3": "SD-CA", "name": "San Diego County", "country": "US", "county": "SD" },
      "geometry": { "type": "Polygon", "coordinates": [[[-117.235, 32.861], [-117.241, 32.755], [-117.164, 32.681], [-117.142, 32.584], [-117.092, 32.463], [-117.054, 32.292], [-116.960, 32.194], [-116.856, 32.166], [-116.675, 32.204], [-116.367, 32.320], [-116.147, 32.551], [-116.164, 32.806], [-116.411, 33.073], [-116.730, 33.082], [-117.092, 32.995], [-117.252, 32.963], [-117.235, 32.861]]] }
    }
  ]
}
```

## 設定 GeoJSON 複雜度

上傳之 GeoJSON 檔案的複雜度可使用下列叢集設定進行設定：

| 設定 | 預設 | 說明 |
| :--- | :--- | :--- |
| `plugins.geospatial.geojson.max_coordinates_per_geo` | `10000` | 每個幾何圖形允許的座標數上限。 |
| `plugins.geospatial.geojson.max_holes_per_polygon` | `1000` | 每個多邊形允許的孔洞數上限。 |
| `plugins.geospatial.geojson.max_multi_geometries` | `100` | 多重幾何物件中的幾何圖形數上限。 |
| `plugins.geospatial.geojson.max_geometry_collection_nested_depth` | `5` | 幾何集合的巢狀深度上限。 |

如需更新動態設定的詳細資訊，請參閱[動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#dynamic-settings)。

## 設定區域地圖

如需一般視覺化組態的相關資訊，請參閱[設定視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/configuring-viz/)。

### Options 索引標籤

| 設定 | 說明 |
| :--- | :--- |
| **Vector map** | 包含地理邊界的底圖。請選取內建地圖或自訂上傳的地圖。 |
| **Join field** | 向量地圖中用來比對您資料值的欄位。 |
| **Color schema** | 用來表示數值的色彩漸層。 |
| **Show tooltips** | 啟用時，滑鼠游標停留在區域上會顯示該區域的值。 |

## 後續步驟

- 若要選擇其他視覺化類型，請參閱[視覺化類型]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/viz-types/)。
- 若要將此視覺化新增至儀表板，請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。

