---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "範圍欄位類型"
nav_order: 70
has_children: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/range/
  - /opensearch/supported-field-types/range/
  - /field-types/range/
---

# 範圍欄位類型
**1.0 版新增**
{: .label .label-purple }

下表列出 OpenSearch 支援的所有範圍欄位類型。

欄位資料類型 | 說明
:--- | :---
`integer_range` | [integer]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 值的範圍。 
`long_range` | [long]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 值的範圍。   
`double_range` | [double]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 值的範圍。  
`float_range` | [float]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/numeric/) 值的範圍。 
`ip_range` | IPv4 或 IPv6 格式的 [IP 位址]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/ip/)範圍。起始與結束 IP 位址可以使用不同的格式。  
`date_range` | [date]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/) 值的範圍。起始與結束日期可以使用不同的[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/#formats)。在內部，所有日期都以不帶正負號的 64 位元整數儲存，代表自 epoch 起算的毫秒數。

## 範例

建立一個包含 double 範圍與 date 範圍的對應：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "gpa" : {
        "type" : "double_range"
      },
      "graduation_date" : {
        "type" : "date_range",
        "format" : "strict_year_month||strict_year_month_day"
      }
    }
  }
}
```
{% include copy-curl.html %}

將一份包含 double 範圍與 date 範圍的文件編製索引：

```json
PUT testindex/_doc/1
{
  "gpa" : {
    "gte" : 1.0,
    "lte" : 4.0
  },
  "graduation_date" : {
    "gte" : "2019-05-01",
    "lte" : "2019-05-15"
  }
}
```
{% include copy-curl.html %}

## IP 位址範圍

您可以用兩種格式指定 IP 位址範圍：範圍表示法，以及[無類別網域間路由 (CIDR) 表示法](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation)。

建立一個包含 IP 位址範圍的對應：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "ip_address_range" : {
        "type" : "ip_range" 
      },
      "ip_address_cidr" : {
        "type" : "ip_range" 
      }
    }
  }
}
```
{% include copy-curl.html %}

將一份同時包含兩種格式 IP 位址範圍的文件編製索引：

```json
PUT testindex/_doc/2
{
  "ip_address_range" : {
    "gte" : "10.24.34.0",
    "lte" : "10.24.35.255"
  },
  "ip_address_cidr" : "10.24.34.0/24"
}
```
{% include copy-curl.html %}

## 查詢範圍欄位

您可以使用 [Term query](#term-query) 或 [Range query](#range-query) 來搜尋範圍欄位中的值。 

### Term query

Term query 會接受一個值，並比對所有該值落在範圍內的範圍欄位。

下列查詢會傳回文件 1，因為 3.5 落在範圍 [1.0, 4.0] 內：

```json
GET testindex/_search
{
  "query" : {
    "term" : {
      "gpa" : {
        "value" : 3.5
      }
    }
  }
}
```
{% include copy-curl.html %}

### Range query

對範圍欄位執行 Range query 會傳回落在該範圍內的文件。 

查詢 2019 年的所有畢業日期，並以 "MM/dd/yyyy" 格式提供日期範圍：

```json
GET testindex1/_search
{
  "query": {
    "range": {
      "graduation_date": {
        "gte": "01/01/2019",
        "lte": "12/31/2019",
        "format": "MM/dd/yyyy",
        "relation" : "within"       
      }
    }
  }
}
```
{% include copy-curl.html %}

上述查詢對於 `within` 與 `intersects` 關係會傳回文件 1，但對於 `contains` 關係則不會傳回。如需關係類型的詳細資訊，請參閱 [範圍查詢參數]({{site.url}}{{site.baseurl}}/query-dsl/term/range#parameters)。

## 參數

下表列出範圍欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`boost` | 一個浮點數值，指定此欄位對相關性分數的權重。高於 1.0 的值會提高欄位的相關性；介於 0.0 與 1.0 之間的值會降低欄位的相關性。預設值為 1.0。可動態更新。
`coerce` | 一個布林值，表示要將整數值的小數部分截斷，並將字串轉換為數值。預設值為 `true`。可動態更新。
`doc_values` | 一個布林值，指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設值為 `true`。
`index` | 一個布林值，指定欄位是否應可被搜尋。預設值為 `true`。 
`store` | 一個布林值，指定是否應儲存欄位值，並可從 `_source` 欄位另外擷取。預設值為 `false`。 
