---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "地理形狀"
nav_order: 57
has_children: false
parent: Geographic field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/geo-shape/
  - /opensearch/supported-field-types/geo-shape/
  - /field-types/geo-shape/
---

# Geoshape 欄位類型
**於 1.0 版導入**
{: .label .label-purple }

geoshape 欄位類型包含地理形狀，例如多邊形或地理點的集合。若要為 geoshape 編製索引，OpenSearch 會將該形狀細分為三角網格，並將每個三角形儲存在 BKD 樹中。這可提供 10<sup>-7</sup> 十進位度的精確度，代表近乎完美的空間解析度。此程序的效能主要受到您正在編製索引的多邊形頂點數量影響。

## 範例

建立包含 geoshape 欄位類型的對應：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_shape"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 格式

Geoshape 可以使用下列格式編製索引：

- [GeoJSON](https://geojson.org/)
- [Well-Known Text (WKT)](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html)

在 GeoJSON 和 WKT 中，座標必須在座標陣列中以 `longitude, latitude` 順序指定。請注意，在此格式中經度在前。
{: .note}

## Geoshape 類型

下表說明可能的 geoshape 類型，以及它們與 GeoJSON 和 WKT 類型的關係。

OpenSearch 類型 | GeoJSON 類型 | WKT 類型 | 說明 
:--- | :--- | :--- | :--- 
[`point`](#point) | Point | POINT | 由緯度和經度指定的地理點。OpenSearch 使用 1984 年世界大地測量系統 (WGS84) 座標系統，也稱為 EPSG:4326。
[`linestring`](#linestring) | LineString | LINESTRING | 由兩個或多個點指定的線。可以是直線，也可以是由連接的線段組成的路徑。
[`polygon`](#polygon) | Polygon | POLYGON | 以座標形式的頂點清單指定的多邊形。多邊形必須封閉，也就是最後一個點必須與第一個點相同。因此，若要建立 n 邊形，需要 n+1 個頂點。頂點的最小數量為四個，這會形成一個三角形。
[`multipoint`](#multipoint) | MultiPoint | MULTIPOINT | 未連接之離散相關點的陣列。
[`multilinestring`](#multilinestring) | MultiLineString | MULTILINESTRING | 線字串的陣列。
[`multipolygon`](#multipolygon) | MultiPolygon | MULTIPOLYGON | 多邊形的陣列。
[`geometrycollection`](#geometry-collection) | GeometryCollection | GEOMETRYCOLLECTION | 可能屬於不同類型的 geoshape 集合。
[`envelope`](#envelope) | N/A | BBOX | 由左上和右下頂點指定的邊界矩形。

## Point

點是由緯度和經度指定的單一座標對。

以 GeoJSON 格式為點編製索引：

```json
PUT testindex/_doc/1
{
  "location" : {
    "type" : "point",
    "coordinates" : [74.0060, 40.7128]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為點編製索引：

```json
PUT testindex/_doc/1
{
  "location" : "POINT (74.0060 40.7128)"
}
```
{% include copy-curl.html %}

## Linestring

線字串是由兩個或多個點指定的線。如果這些點共線，則線字串是一條直線；否則，線字串代表由線段組成的路徑。

以 GeoJSON 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : {
    "type" : "linestring",
    "coordinates" : [[74.0060, 40.7128], [71.0589, 42.3601]]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : "LINESTRING (74.0060 40.7128, 71.0589 42.3601)"
}
```
{% include copy-curl.html %}

## Polygon

多邊形是以座標形式的頂點清單指定的。多邊形必須封閉，也就是最後一個點必須與第一個點相同。在下列範例中，使用四個點建立一個三角形。

GeoJSON 要求您以逆時針方向列出多邊形的頂點。WKT 則不對頂點施加特定順序。
{: .note}

以 GeoJSON 格式為多邊形 (三角形) 編製索引：

```json
PUT testindex/_doc/3
{
  "location" : {
    "type" : "polygon",
    "coordinates" : [
      [
        [74.0060, 40.7128], 
        [73.7562, 42.6526], 
        [71.0589, 42.3601], 
        [74.0060, 40.7128]
      ]
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為多邊形 (三角形) 編製索引：

```json
PUT testindex/_doc/3
{
  "location" : "POLYGON ((74.0060 40.7128, 71.0589 42.3601, 73.7562 42.6526, 74.0060 40.7128))"
}
```
{% include copy-curl.html %}

多邊形內部可以有洞。在這種情況下，`coordinates` 欄位會包含多個陣列。第一個陣列代表外部多邊形，而每個後續陣列代表一個洞。洞以多邊形表示，並指定為座標陣列。

GeoJSON 要求您以逆時針方向列出多邊形的頂點，並以順時針方向列出洞的頂點。WKT 則不對頂點施加特定順序。
{: .note}

以 GeoJSON 格式為帶有三角形洞的多邊形 (三角形) 編製索引：

```json
PUT testindex/_doc/4
{
  "location" : {
    "type" : "polygon",
    "coordinates" : [
      [
        [74.0060, 40.7128], 
        [73.7562, 42.6526], 
        [71.0589, 42.3601], 
        [74.0060, 40.7128]
      ],
      [
        [72.6734,41.7658], 
        [73.0515, 41.5582], 
        [72.6506, 41.5623],
        [72.6734, 41.7658]
      ]
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為帶有三角形洞的多邊形 (三角形) 編製索引：

```json
PUT testindex/_doc/4
{
  "location" : "POLYGON ((74.0060 40.7128, 71.0589 42.3601, 73.7562 42.6526, 74.0060 40.7128), (72.6734 41.7658, 72.6506 41.5623, 73.0515 41.5582, 72.6734 41.7658))"
}
```
{% include copy-curl.html %}

您可以在 OpenSearch 中以順時針或逆時針順序列出頂點來指定多邊形。這對於不跨越日期變更線 (寬度小於 180&deg;) 的多邊形效果良好。然而，跨越日期變更線 (寬度大於 180&deg;) 的多邊形可能會有歧義，因為 WKT 不對頂點施加特定順序。因此，您必須以逆時針順序列出頂點來指定跨越日期變更線的多邊形。

您可以在對應時定義 [`orientation`](#parameters) 參數來指定頂點的走訪順序：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_shape",
        "orientation" : "left"
      }
    }
  }
}
```
{% include copy-curl.html %}

後續編製索引的文件可以覆寫 `orientation` 設定：

```json
PUT testindex/_doc/3
{
  "location" : {
    "type" : "polygon",
    "orientation" : "cw",
    "coordinates" : [
      [[74.0060, 40.7128], 
      [71.0589, 42.3601], 
      [73.7562, 42.6526], 
      [74.0060, 40.7128]]
    ]
  }
}
```
{% include copy-curl.html %}

## Multipoint

多點是未連接之離散相關點的陣列。

以 GeoJSON 格式為多點編製索引：

```json
PUT testindex/_doc/6
{
  "location" : {
    "type" : "multipoint",
    "coordinates" : [
      [74.0060, 40.7128], 
      [71.0589, 42.3601]
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為多點編製索引：

```json
PUT testindex/_doc/6
{
  "location" : "MULTIPOINT (74.0060 40.7128, 71.0589 42.3601)"
}
```
{% include copy-curl.html %}

## Multilinestring

多線字串是線字串的陣列。

以 GeoJSON 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : {
    "type" : "multilinestring",
    "coordinates" : [
      [[74.0060, 40.7128], [71.0589, 42.3601]],
      [[73.7562, 42.6526], [72.6734, 41.7658]]
      ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : "MULTILINESTRING ((74.0060 40.7128, 71.0589 42.3601), (73.7562 42.6526, 72.6734 41.7658))"
}
```
{% include copy-curl.html %}

## Multipolygon

多多邊形是多邊形的陣列。在此範例中，第一個多邊形包含一個洞，而第二個則沒有。

以 GeoJSON 格式為多多邊形編製索引：

```json
PUT testindex/_doc/4
{
  "location" : {
    "type" : "multipolygon",
    "coordinates" : [
    [
      [
        [74.0060, 40.7128], 
        [73.7562, 42.6526], 
        [71.0589, 42.3601], 
        [74.0060, 40.7128]
      ],
      [
        [73.0515, 41.5582], 
        [72.6506, 41.5623], 
        [72.6734, 41.7658], 
        [73.0515, 41.5582]
      ]
    ],
    [
      [
        [73.9146, 40.8252], 
        [73.8871, 41.0389], 
        [73.6853, 40.9747], 
        [73.9146, 40.8252]
      ]
    ]
  ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為多多邊形編製索引：

```json
PUT testindex/_doc/4
{
  "location" : "MULTIPOLYGON (((74.0060 40.7128, 71.0589 42.3601, 73.7562 42.6526, 74.0060 40.7128), (72.6734 41.7658, 72.6506 41.5623, 73.0515 41.5582, 72.6734 41.7658)), ((73.9146 40.8252, 73.6853 40.9747, 73.8871 41.0389, 73.9146 40.8252)))"
}
```
{% include copy-curl.html %}

## Geometry collection

幾何集合是可能屬於不同類型的 geoshape 集合。

以 GeoJSON 格式為幾何集合編製索引：

```json
PUT testindex/_doc/7
{
  "location" : {
    "type": "geometrycollection",
    "geometries": [
      {
        "type": "point",
        "coordinates": [74.0060, 40.7128]
      },
      {
        "type": "linestring",
        "coordinates": [[73.7562, 42.6526], [72.6734, 41.7658]]
      }
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為幾何集合編製索引：

```json
PUT testindex/_doc/7
{
  "location" : "GEOMETRYCOLLECTION (POINT (74.0060 40.7128), LINESTRING(73.7562 42.6526, 72.6734 41.7658))"
}
```
{% include copy-curl.html %}

## Envelope

封套是由左上和右下頂點指定的邊界矩形。GeoJSON 格式為 `[[minLon, maxLat], [maxLon, minLat]]`。

以 GeoJSON 格式為封套編製索引：

```json
PUT testindex/_doc/2
{
  "location" : {
    "type" : "envelope",
    "coordinates" : [[71.0589, 42.3601], [74.0060, 40.7128]]
  }
}
```
{% include copy-curl.html %}

在 WKT 格式中，請使用 `BBOX (minLon, maxLon, maxLat, minLat)`。

以 WKT BBOX 格式為封套編製索引：

```json
PUT testindex/_doc/8
{
  "location" : "BBOX (71.0589, 74.0060, 42.3601, 40.7128)"
}
```
{% include copy-curl.html %}

## 參數

下表列出 geoshape 欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`coerce` | 指定是否自動封閉未封閉線性環的布林值。預設為 `false`。
`doc_values` | 指定是否應將該欄位儲存在磁碟上，以便用於彙總、排序或指令碼的布林值。預設為 `true`。
`ignore_malformed` | 指定忽略格式錯誤的 GeoJSON 或 WKT geoshape 而不擲回例外的布林值。預設為 `false` (當 geoshape 格式錯誤時擲回例外)。
`ignore_z_value` | 專屬於具有三個座標的點。如果 `ignore_z_value` 為 `true`，則第三個座標不會編製索引，但仍會儲存在 `_source` 欄位中。如果 `ignore_z_value` 為 `false`，則會擲回例外。預設為 `true`。
`orientation` | 指定 geoshape 座標清單中頂點的走訪順序。`orientation` 接受下列值：<br> 1. RIGHT：逆時針。使用下列其中一個字串 (大寫或小寫) 指定 RIGHT 方向：`right`、`counterclockwise`、`ccw`。<br> 2. LEFT：順時針。使用下列其中一個字串 (大寫或小寫) 指定 LEFT 方向：`left`、`clockwise`、`cw`。  個別文件可以覆寫此值。<br> 預設為 `RIGHT`。
