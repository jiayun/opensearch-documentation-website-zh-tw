---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "地理與 xy 查詢"
has_children: true
nav_order: 65
redirect_from:
   - /opensearch/query-dsl/geo-and-xy/index/
   - /query-dsl/query-dsl/geo-and-xy/
   - /query-dsl/query-dsl/geo-and-xy/index/
   - /query-dsl/geo-and-xy/
---

# 地理與 xy 查詢

地理與 xy 查詢可讓您搜尋包含地圖或座標平面上點與形狀的欄位。地理查詢適用於地理空間資料，而 xy 查詢適用於二維座標資料。在所有地理查詢中，geoshape 查詢與 xy 查詢非常相似，但前者搜尋[地理欄位]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geographic/)，後者搜尋[笛卡兒欄位]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy)。

## xy 查詢

[xy 查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/geo-and-xy/xy)搜尋在笛卡兒座標系統中包含幾何圖形的文件。這些幾何圖形可以指定在支援點的 [`xy_point`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-point) 欄位，以及支援點、線、圓形與多邊形的 [`xy_shape`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/xy-shape) 欄位中。

xy 查詢會回傳包含以下內容的文件：
- 與所提供形狀具有四種空間關係之一（`INTERSECTS`、`DISJOINT`、`WITHIN` 或 `CONTAINS`）的 xy 形狀與 xy 點。
- 與所提供形狀相交的 xy 點。

## 地理查詢

地理查詢搜尋包含地理空間幾何圖形的文件。這些幾何圖形可以指定在支援地圖上點的 [`geo_point`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/) 欄位，以及支援點、線、圓形與多邊形的 [`geo_shape`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-shape/) 欄位中。

OpenSearch 提供下列地理查詢類型：

| 查詢類型 | 說明 |
| :--- | :--- |
| [Geo-bounding box]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/geo-and-xy/geo-bounding-box/) | 回傳地理點欄位值位於邊界框內的文件。 |
| [Geodistance]({{site.url}}{{site.baseurl}}/query-dsl/geo-and-xy/geodistance/) | 回傳其地理點與所提供地理點的距離在指定範圍內的文件。 |
| [Geopolygon]({{site.url}}{{site.baseurl}}/query-dsl/geo-and-xy/geopolygon/) | 回傳包含位於多邊形內之地理點的文件。 |
| [Geoshape]({{site.url}}{{site.baseurl}}/query-dsl/geo-and-xy/geoshape/) | 回傳包含與所提供形狀具有四種空間關係之一（`INTERSECTS`、`DISJOINT`、`WITHIN` 或 `CONTAINS`）的地理形狀與地理點，或與所提供形狀相交之地理點的文件。 |
