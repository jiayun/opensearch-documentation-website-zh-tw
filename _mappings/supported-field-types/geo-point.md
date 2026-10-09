---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "地理點"
nav_order: 56
has_children: false
parent: Geographic field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/geo-point/
  - /opensearch/supported-field-types/geo-point/
  - /field-types/geo-point/
---

# 地理點欄位類型
**於 1.0 版引入**
{: .label .label-purple }

地理點欄位類型包含以緯度和經度指定的地理點。 

## 範例

建立具有地理點欄位類型的對應：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "point": {
        "type": "geo_point"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 格式

地理點可以下列格式編製索引：

- 具有緯度和經度的物件

```json
PUT testindex1/_doc/1
{
  "point": { 
    "lat": 40.71,
    "lon": 74.00
  }
}
```
{% include copy-curl.html %}

- 採用「`latitude`,`longitude`」格式的字串

```json
PUT testindex1/_doc/2
{
  "point": "40.71,74.00" 
}
```
{% include copy-curl.html %}

- 地理雜湊

```json
PUT testindex1/_doc/3
{
  "point": "txhxegj0uyp3"
}
```
{% include copy-curl.html %}

- 採用 [`longitude`, `latitude`] 格式的陣列

```json
PUT testindex1/_doc/4
{
  "point": [74.00, 40.71] 
}
```
{% include copy-curl.html %}

- 採用「POINT(`longitude` `latitude`)」格式的[標準文字表示法](https://docs.opengeospatial.org/is/12-063r5/12-063r5.html) POINT

```json
PUT testindex1/_doc/5
{
  "point": "POINT (74.00 40.71)"
}
```
{% include copy-curl.html %}

- GeoJSON 格式，其中 `coordinates` 採用 [`longitude`, `latitude`] 格式

```json
PUT testindex1/_doc/6
{
  "point": {
    "type": "Point",
    "coordinates": [74.00, 40.71]
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出地理點欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`doc_values` | 布林值，指定是否將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `true`。
`ignore_malformed` | 布林值，指定忽略格式錯誤的值，且不擲回例外。緯度的有效值為 [-90, 90]。經度的有效值為 [-180, 180]。預設為 `false`。
`ignore_z_value` | 僅適用於具有三個座標的點。如果 `ignore_z_value` 為 `true`，則不會為第三個座標編製索引，但仍會將其儲存在 `_source` 欄位中。如果 `ignore_z_value` 為 `false`，則會擲回例外。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須與欄位的類型相同。如果未指定此參數，當欄位的值為 `null` 時，該欄位會被視為缺漏。預設為 `null`。

## 衍生來源

當索引使用[衍生來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source)時，OpenSearch 會在重建來源的過程中，將地理點值正規化為一致的緯度／經度物件格式，不受原始輸入格式影響。OpenSearch 也可能對多值地理點欄位進行排序，且轉換過程中可能會損失精確度。

建立索引，啟用衍生來源並設定 `geo_point` 欄位：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "geo_point": {
        "type": "geo_point"
      }
    }
  }
}
```

將採用地理雜湊格式的文件編製索引至該索引中：

```json
PUT sample-index1/_doc/1
{
  "geo_point": "txhxegj0uyp3"
}
```

OpenSearch 重建 `_source` 後，衍生的 `_source` 如下：

```json
{
  "geo_point": {"lat": 40.71, "lon": 74.00}
}
```

將另一份採用標準文字表示法格式的文件編製索引至該索引中：

```json
PUT sample-index1/_doc/2
{
  "geo_point": "POINT (74.00 40.71)"
}
```

OpenSearch 重建 `_source` 後，衍生的 `_source` 如下：

```json
{
  "geo_point": {"lat": 40.71, "lon": 74.00}
}
```

將具有多個地理點的文件編製索引至該索引中：

```json
PUT sample-index1/_doc/3
{
  "geo_point": [
    {"lat": 75.98, "lon": 40.34},
    {"lat": -90, "lon": -80}
  ]
}
```

OpenSearch 重建 `_source` 後，衍生的 `_source` 顯示已排序的值，且精確度可能有所變化：

```json
{
  "geo_point": [
    {
      "lat": -90.0,
      "lon": -80.00000000931323
    },
    {
      "lat": 75.97999997902662,
      "lon": 40.339999962598085
    }
  ]
}
```
