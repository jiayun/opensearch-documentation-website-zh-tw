---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: xy point
nav_order: 58
has_children: false
parent: Cartesian field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/xy-point/
  - /opensearch/supported-field-types/xy-point/
  - /field-types/xy-point/
---

# xy point 欄位類型
**於 2.4 版推出**
{: .label .label-purple }

xy point 欄位類型包含二維笛卡兒座標系統中的一個點，由 x 和 y 座標指定。它是以 Lucene 的 [`XYPoint`](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/geo/XYPoint.html) 欄位類型為基礎。xy point 欄位類型與 [geopoint]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/geo-point/) 欄位類型類似，但沒有 geopoint 的範圍限制。xy point 的座標為單精度浮點數值。如需浮點數值的範圍與精確度相關資訊，請參閱[數值欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/)。

## 範例

建立具有 xy point 欄位類型的對應：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "point": {
        "type": "xy_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 格式

xy point 可以下列格式編製索引：

- 具有 x 和 y 座標的物件

```json
PUT testindex1/_doc/1
{
  "point": { 
    "x": 0.5,
    "y": 4.5
  }
}
```
{% include copy-curl.html %}

- 「`x`, `y`」格式的字串

```json
PUT testindex1/_doc/2
{
  "point": "0.5, 4.5" 
}
```
{% include copy-curl.html %}

- [`x`, `y`] 格式的陣列

```json
PUT testindex1/_doc/3
{
  "point": [0.5, 4.5] 
}
```
{% include copy-curl.html %}

- 「POINT(`x` `y`)」格式的 [well-known text (WKT)](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html) POINT

```json
PUT testindex1/_doc/4
{
  "point": "POINT (0.5 4.5)"
}
```
{% include copy-curl.html %}

- GeoJSON 格式

```json
PUT testindex1/_doc/5
{
  "point" : {
    "type" : "Point",
    "coordinates" : [0.5, 4.5]        
  }
}
```
{% include copy-curl.html %}

在所有 xy point 格式中，座標必須以 `x, y` 順序指定。
{: .note}

## 參數

下表列出 xy point 欄位類型可接受的參數。所有參數皆為選用。

參數 | 說明
:--- | :---
`doc_values` | 布林值，指定欄位是否應儲存在磁碟上，以便用於彙總、排序或指令碼。預設值為 `true`。
`ignore_malformed` | 布林值，指定是否忽略格式錯誤的值，且不擲回例外狀況。預設值為 `false`。
`ignore_z_value` | 專用於具有三個座標的點。若 `ignore_z_value` 為 `true`，則不會將第三個座標編製索引，但仍會儲存在 `_source` 欄位中。若 `ignore_z_value` 為 `false`，則會擲回例外狀況。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。該值必須與欄位具有相同的類型。若未指定此參數，則當欄位的值為 `null` 時，會將其視為缺少。預設值為 `null`。