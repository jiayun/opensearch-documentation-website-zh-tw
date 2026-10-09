---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: xy shape
nav_order: 59
has_children: false
parent: Cartesian field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/xy-shape/
  - /opensearch/supported-field-types/xy-shape/
  - /field-types/xy-shape/
---

# xy shape 欄位類型
**於 2.4 版推出**
{: .label .label-purple }

xy shape 欄位類型包含一個形狀，例如多邊形或 xy 點的集合。它以 Lucene 的 [`XYShape`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/document/XYShape.html) 欄位類型為基礎。若要為 xy shape 編製索引，OpenSearch 會將該形狀細分為三角網格，並將每個三角形儲存在 BKD 樹（一組平衡的 k 維樹）中。這可提供 10<sup>-7</sup> 十進位度的精確度，代表近乎完美的空間解析度。

xy shape 欄位類型類似於 [geoshape]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-shape/) 欄位類型，但它表示笛卡兒平面上的形狀，並非以固定於地球的地面參考系統為基礎。xy shape 的座標是單精度浮點數值。關於浮點數值的範圍與精確度，請參閱 [數值欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/)。

## 範例

建立一個包含 xy shape 欄位類型的對應：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "location": {
        "type": "xy_shape"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 格式

xy shape 可以以下列格式編製索引：

- [GeoJSON](https://geojson.org/)
- [Well-known text (WKT)](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html)

在 GeoJSON 與 WKT 中，座標陣列內的座標都必須以 `x, y` 順序指定。
{: .note}

## xy shape 類型

下表說明可能的 xy shape 類型，以及它們與 GeoJSON 和 WKT 類型的關係。

OpenSearch type | GeoJSON type | WKT type | Description 
:--- | :--- | :--- | :--- 
[`point`](#point) | Point | POINT | 由 x 與 y 座標指定的地理點。 
[`linestring`](#linestring) | LineString | LINESTRING | 由兩個或多個點指定的線。可以是直線，或由相連線段組成的路徑。
[`polygon`](#polygon) | Polygon | POLYGON | 以座標形式的頂點清單指定的多邊形。多邊形必須封閉，也就是最後一點必須與第一點相同。因此，若要建立 n 邊形，需要 n+1 個頂點。頂點數量最少為四個，即形成一個三角形。
[`multipoint`](#multipoint) | MultiPoint | MULTIPOINT | 一組互不相連但彼此相關的離散點陣列。
[`multilinestring`](#multilinestring) | MultiLineString | MULTILINESTRING | 線字串的陣列。
[`multipolygon`](#multipolygon) | MultiPolygon | MULTIPOLYGON | 多邊形的陣列。
[`geometrycollection`](#geometry-collection) | GeometryCollection | GEOMETRYCOLLECTION | 可能屬於不同類型的 xy shape 集合。
[`envelope`](#envelope) | N/A | BBOX | 由左上與右下頂點指定的邊界矩形。

## Point

點由一組座標指定。

以 GeoJSON 格式為點編製索引：

```json
PUT testindex/_doc/1
{
  "location" : {
    "type" : "point",
    "coordinates" : [0.5, 4.5]        
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為點編製索引：

```json
PUT testindex/_doc/1
{
  "location" : "POINT (0.5 4.5)"        
}
```
{% include copy-curl.html %}

## Linestring

線字串是由兩個或多個點指定的線。若這些點共線，線字串就是一條直線；否則，線字串代表由線段組成的路徑。

以 GeoJSON 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : {
    "type" : "linestring",
    "coordinates" : [[0.5, 4.5], [-1.5, 2.3]]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : "LINESTRING (0.5 4.5, -1.5 2.3)"
}
```
{% include copy-curl.html %}

## Polygon

多邊形是以座標形式的頂點清單指定。多邊形必須封閉，也就是最後一點必須與第一點相同。在下列範例中，使用四個點建立一個三角形。

GeoJSON 要求您以逆時針方向列出多邊形的頂點。WKT 則不對頂點順序施加特定要求。
{: .note}

以 GeoJSON 格式為多邊形（三角形）編製索引：

```json
PUT testindex/_doc/3
{
  "location" : {
    "type" : "polygon",
    "coordinates" : [
      [[0.5, 4.5], 
      [2.5, 6.0], 
      [1.5, 2.0], 
      [0.5, 4.5]]
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為多邊形（三角形）編製索引：

```json
PUT testindex/_doc/3
{
  "location" : "POLYGON ((0.5 4.5, 2.5 6.0, 1.5 2.0, 0.5 4.5))"
}
```
{% include copy-curl.html %}

多邊形內部可以有洞。在此情況下，`coordinates` 欄位會包含多個陣列。第一個陣列代表外層多邊形，其後每個陣列代表一個洞。洞以多邊形表示，並以座標陣列指定。

GeoJSON 要求您以逆時針方向列出多邊形的頂點，並以順時針方向列出洞的頂點。WKT 則不對頂點順序施加特定要求。
{: .note}

以 GeoJSON 格式為帶有三角形洞的多邊形（三角形）編製索引：

```json
PUT testindex/_doc/4
{
  "location" : {
    "type" : "polygon",
    "coordinates" : [
      [[0.5, 4.5], 
      [2.5, 6.0], 
      [1.5, 2.0], 
      [0.5, 4.5]],
      
      [[1.0, 4.5], 
      [1.5, 4.5], 
      [1.5, 4.0], 
      [1.0, 4.5]]
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為帶有三角形洞的多邊形（三角形）編製索引：

```json
PUT testindex/_doc/4
{
  "location" : "POLYGON ((0.5 4.5, 2.5 6.0, 1.5 2.0, 0.5 4.5), (1.0 4.5, 1.5 4.5, 1.5 4.0, 1.0 4.5))"
}
```
{% include copy-curl.html %}

預設情況下，多邊形的頂點以逆時針順序走訪。您可以在對應時定義 [`orientation`](#parameters) 參數來指定頂點走訪順序：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "location": {
        "type": "xy_shape",
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
      [[0.5, 4.5], 
      [2.5, 6.0], 
      [1.5, 2.0], 
      [0.5, 4.5]]
    ]
  }
}
```
{% include copy-curl.html %}

## Multipoint

多點是一組互不相連但彼此相關的離散點陣列。

以 GeoJSON 格式為多點編製索引：

```json
PUT testindex/_doc/6
{
  "location" : {
    "type" : "multipoint",
    "coordinates" : [
      [0.5, 4.5], 
      [2.5, 6.0]
    ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為多點編製索引：

```json
PUT testindex/_doc/6
{
  "location" : "MULTIPOINT (0.5 4.5, 2.5 6.0)"
}
```
{% include copy-curl.html %}

## Multilinestring

多線字串是線字串的陣列。

以 GeoJSON 格式為多線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : {
    "type" : "multilinestring",
    "coordinates" : [
      [[0.5, 4.5], [2.5, 6.0]],
      [[1.5, 2.0], [3.5, 3.5]]
      ]
  }
}
```
{% include copy-curl.html %}

以 WKT 格式為線字串編製索引：

```json
PUT testindex/_doc/2
{
  "location" : "MULTILINESTRING ((0.5 4.5, 2.5 6.0), (1.5 2.0, 3.5 3.5))"
}
```
{% include copy-curl.html %}

## Multipolygon

多多邊形是多邊形的陣列。在此範例中，第一個多邊形包含一個洞，第二個則沒有。

以 GeoJSON 格式為多多邊形編製索引：

```json
PUT testindex/_doc/4
{
  "location" : {
    "type" : "multipolygon",
    "coordinates" : [
    [
      [[0.5, 4.5], 
      [2.5, 6.0], 
      [1.5, 2.0], 
      [0.5, 4.5]],
      
      [[1.0, 4.5], 
      [1.5, 4.5], 
      [1.5, 4.0], 
      [1.0, 4.5]]
    ],
    [
      [[2.0, 0.0], 
      [1.0, 2.0], 
      [3.0, 1.0], 
      [2.0, 0.0]]
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
  "location" : "MULTIPOLYGON (((0.5 4.5, 2.5 6.0, 1.5 2.0, 0.5 4.5), (1.0 4.5, 1.5 4.5, 1.5 4.0, 1.0 4.5)), ((2.0 0.0, 1.0 2.0, 3.0 1.0, 2.0 0.0)))"
}
```
{% include copy-curl.html %}

## Geometry collection

幾何集合是可能屬於不同類型的 xy shape 集合。

以 GeoJSON 格式為幾何集合編製索引：

```json
PUT testindex/_doc/7
{
  "location" : {
    "type": "geometrycollection",
    "geometries": [
      {
        "type": "point",
        "coordinates": [0.5, 4.5]
      },
      {
        "type": "linestring",
        "coordinates": [[2.5, 6.0], [1.5, 2.0]]
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
  "location" : "GEOMETRYCOLLECTION (POINT (0.5 4.5), LINESTRING(2.5 6.0, 1.5 2.0))"
}
```
{% include copy-curl.html %}

## Envelope

封套是由左上與右下頂點指定的邊界矩形。GeoJSON 格式為 `[[minX, maxY], [maxX, minY]]`。

以 GeoJSON 格式為封套編製索引：

```json
PUT testindex/_doc/2
{
  "location" : {
    "type" : "envelope",
    "coordinates" : [[3.0, 2.0], [6.0, 0.0]]
  }
}
```
{% include copy-curl.html %}

在 WKT 格式中，請使用 `BBOX (minX, maxX, maxY, minY)`。

以 WKT BBOX 格式為封套編製索引：

```json
PUT testindex/_doc/8
{
  "location" : "BBOX (3.0, 6.0, 2.0, 0.0)"
}
```
{% include copy-curl.html %}

## 參數

下表列出 xy shape 欄位類型接受的參數。所有參數皆為選用。

Parameter | Description 
:--- | :--- 
`coerce` | 一個布林值，指定是否自動封閉未封閉的線性環。預設為 `false`。
`doc_values` | 一個布林值，指定該欄位是否應儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `false`。
`ignore_malformed` | 一個布林值，指定是否忽略格式錯誤的 GeoJSON 或 WKT xy shape 而不擲回例外狀況。預設為 `false`（當 xy shape 格式錯誤時擲回例外狀況）。
`ignore_z_value` | 專用於具有三個座標的點。若 `ignore_z_value` 為 `true`，第三個座標不會編製索引，但仍會儲存在 `_source` 欄位中。若 `ignore_z_value` 為 `false`，則會擲回例外狀況。預設為 `true`。
`orientation` | 指定 xy shape 座標清單中頂點的走訪順序。`orientation` 接受下列值：<br> 1. RIGHT：逆時針。使用下列其中一個字串（大寫或小寫）指定 RIGHT 方向：`right`、`counterclockwise`、`ccw`。<br> 2. LEFT：順時針。使用下列其中一個字串（大寫或小寫）指定 LEFT 方向：`left`、`clockwise`、`cw`。 個別文件可以覆寫此值。<br> 預設為 `RIGHT`。