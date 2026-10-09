---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "數值欄位類型"
parent: Supported field types
nav_order: 30
has_children: true
redirect_from:
  - /field-types/supported-field-types/numeric/
  - /opensearch/supported-field-types/numeric/
  - /field-types/numeric/
---

# 數值欄位類型

下表列出 OpenSearch 支援的所有數值欄位類型。

欄位資料類型 | 說明  
:--- | :--- 
`byte` | 帶正負號的 8 位元整數。最小值為 &minus;128。最大值為 127。
`double` | 雙精度 64 位元 IEEE 754 浮點值。最小量值為 2<sup>&minus;1074 </sup>。最大量值為 (2 &minus; 2<sup>&minus;52</sup>) &middot; 2<sup>1023</sup>。有效位元數為 53。有效位數為 15.95。
`float` | 單精度 32 位元 IEEE 754 浮點值。最小量值為 2<sup>&minus;149 </sup>。最大量值為 (2 &minus; 2<sup>&minus;23</sup>) &middot; 2<sup>127</sup>。有效位元數為 24。有效位數為 7.22。
`half_float` | 半精度 16 位元 IEEE 754 浮點值。最小量值為 2<sup>&minus;24 </sup>。最大量值為 65504。有效位元數為 11。有效位數為 3.31。
`integer` | 帶正負號的 32 位元整數。最小值為 &minus;2<sup>31</sup>。最大值為 2<sup>31</sup> &minus; 1。
`long` | 帶正負號的 64 位元整數。最小值為 &minus;2<sup>63</sup>。最大值為 2<sup>63</sup> &minus; 1。
[`unsigned_long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/unsigned-long/) | 不帶正負號的 64 位元整數。最小值為 0。最大值為 2<sup>64</sup> &minus; 1。
`short` | 帶正負號的 16 位元整數。最小值為 &minus;2<sup>15</sup>。最大值為 2<sup>15</sup> &minus; 1。 
[`scaled_float`](#scaled-float-field-type) | 浮點值，會乘以 double 縮放係數並以 long 值儲存。

integer、long、float 和 double 欄位類型有對應的[範圍欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/range/)。
{: .note }

如果您的數值欄位包含 ID 之類的識別碼，您可以將此欄位對應為 [keyword]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/)，以最佳化更快速的詞彙層級查詢。如果您需要對此欄位使用範圍查詢，您可以將此欄位同時對應為數值欄位類型和 keyword 欄位類型。
{: .tip }

## 範例

建立一個對應，其中 integer_value 是 integer 欄位：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "integer_value" : {
        "type" : "integer"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有整數值的文件編製索引：

```json
PUT testindex/_doc/1 
{
  "integer_value" : 123
}
```
{% include copy-curl.html %}

## 範例：略過清單

使用 `skip_list` 參數可獲得更好的查詢效能。`skip_list` 參數對於經常在 `range` 查詢中使用的欄位特別有幫助，因為它可讓查詢引擎略過不符合查詢條件的文件範圍。

建立一個已啟用略過清單索引的對應：

```json
PUT /testindex_skiplist
{
  "mappings" : {
    "properties" :  {
      "price" : {
        "type" : "double",
        "skip_list" : true
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有數值的文件編製索引：

```json
PUT testindex_skiplist/_doc/1
{
  "price" : 19.99
}
```
{% include copy-curl.html %}


## 縮放浮點欄位類型

縮放浮點欄位類型是一種浮點值，會乘以縮放係數並以 long 值儲存。它接受數值欄位類型的所有選用參數，外加一個額外的 scaling_factor 參數。建立縮放浮點時必須提供縮放係數。 

縮放浮點適合用來節省磁碟空間。scaling_factor 值越大，準確度越高，但空間額外負荷也越大。  
{: .note }

## 縮放浮點範例

建立一個對應，其中 `scaled` 是 scaled_float 欄位：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "scaled" : {
        "type" : "scaled_float",
        "scaling_factor" : 10
      }
    }
  }
}

```
{% include copy-curl.html %}

將含有 scaled_float 值的文件編製索引：

```json
PUT testindex/_doc/1 
{
  "scaled" : 2.3
}
```
{% include copy-curl.html %}

`scaled` 值將儲存為 23。

## 參數

下表列出數值欄位類型接受的參數。所有參數都是選用。

參數 | 說明 
:--- | :--- 
`boost` | 浮點值，指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 與 1.0 之間的值會降低欄位的相關性。預設為 1.0。可動態更新。
`coerce` | 布林值，指出是否截斷整數值的小數，並將字串轉換為數值。預設為 `true`。可動態更新。
`doc_values` | 布林值，指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `true`。
`ignore_malformed` | 布林值，指定是否忽略格式錯誤的值且不擲回例外狀況。預設為 `false`。可動態更新。
`index` | 布林值，指定欄位是否應可供搜尋。預設為 `true`。對於使用可插拔資料格式的索引，預設為 `false`，且不支援 `true`。如需詳細資訊，請參閱[可插拔資料格式索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/#pluggable-data-format-indexes)。
`meta` | 接受此欄位的中繼資料。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須與欄位類型相同。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為缺少。預設為 `null`。
`skip_list` | 布林值，指定是否為 doc values 啟用略過清單索引。啟用後，這會建立已編製索引的 doc values，可讓查詢引擎略過不相關的文件範圍，進而改善 `range` 查詢的效能。預設為 `false`。
`store` | 布林值，指定是否應儲存欄位值，且可與 `_source` 欄位分開擷取。預設為 `false`。 

縮放浮點有一個額外的必要參數：`scaling_factor`。

參數 | 說明 
:--- | :--- 
`scaling_factor` | double 值，會乘以欄位值並四捨五入至最接近的 long。必要。 
`skip_list` | 布林值，指定是否為 doc values 啟用略過清單索引。啟用後，OpenSearch 會建立已編製索引的 doc values，可讓查詢引擎略過不相關的文件範圍，進而改善 `range` 查詢的效能。預設為 `false`。

## 衍生的來源

當索引使用[衍生的來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source)時，OpenSearch 在重建來源期間可能會對多重值欄位中的數值進行排序。此外，某些數值欄位類型可能會發生精確度遺失。

建立一個啟用衍生的來源並設定 `number` 欄位的索引：

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
      "number": {
        "type": "integer"
      }
    }
  }
}
```

將含有多個整數值的文件編製索引至該索引：

```json
PUT sample-index1/_doc/1
{
  "number": [1, 0, -1, 0]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會以數值方式排序這些值：

```json
{
  "number": [-1, 0, 0, 1]
}
```

使用 `half_float` 欄位時，可能會根據欄位儲存的精確度而發生精確度遺失。建立一個含有 `hf` 欄位的索引：

```json
PUT sample-index2
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
      "hf": {
        "type": "half_float"
      }
    }
  }
}
```

將含有精確小數值的文件編製索引至該索引：

```json
PUT sample-index2/_doc/1
{
  "hf": 1234.56
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會顯示精確度遺失：

```json
{
  "hf": 1235.0
}
```

使用 `scaled_float` 欄位時，可能會因縮放係數而發生精確度遺失。建立一個含有 `sf` 欄位的索引：

```json
PUT sample-index3
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
      "sf": {
        "type": "scaled_float",
        "scaling_factor": 100
      }
    }
  }
}
```

將含有小數值的文件編製索引至該索引：

```json
PUT sample-index3/_doc/1
{
  "sf": 12.345
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會顯示精確度遺失：

```json
{
  "sf": 12.34
}
```

