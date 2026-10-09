---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "無號長整數"
parent: Numeric field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/unsigned-long/
nav_order: 15
has_children: false
---

# 無號長整數欄位類型
**自 2.8 版起推出**
{: .label .label-purple }

`unsigned_long` 欄位類型是一種數值欄位類型，代表不帶正負號的 64 位元整數，最小值為 0，最大值為 2<sup>64</sup> &minus; 1。在下列範例中，`counter` 會對應為 `unsigned_long` 欄位：


```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "counter" : {
        "type" : "unsigned_long"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 編製索引

若要將含有 `unsigned_long` 值的文件編製索引，請使用下列請求：

```json
PUT testindex/_doc/1 
{
  "counter" : 10223372036854775807
}
```
{% include copy-curl.html %}

或者，您也可以使用 [Bulk API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/bulk/)，如下所示：

```json
POST _bulk
{ "index": { "_index": "testindex", "_id": "1" } }
{ "counter": 10223372036854775807 }
```
{% include copy-curl.html %}

如果 `unsigned_long` 類型的欄位將 `store` 參數設為 `true` (也就是該欄位是已儲存的欄位)，則會以字串形式儲存並傳回。`unsigned_long` 值不支援小數部分，因此若有提供小數部分，會將其截斷。
{: .note}

## 查詢

`unsigned_long` 欄位支援其他數值類型所支援的大多數查詢。例如，您可以對 `unsigned_long` 欄位使用詞項查詢：

```json
POST _search
{
  "query": {
    "term": {
      "counter": {
        "value": 10223372036854775807
      }
    }
  }
}
```
{% include copy-curl.html %}

您也可以使用範圍查詢：

```json
POST _search
{
  "query": {
    "range": {
      "counter": {
        "gte": 10223372036854775807
      }
    }
  }
}
```
{% include copy-curl.html %}

## 排序

您可以將 `sort` 值與 `unsigned_long` 欄位搭配使用，以排序搜尋結果，例如：

```json
POST _search
{
  "sort" : [
    { 
      "counter" : { 
        "order" : "asc" 
      } 
    }
  ],
  "query": {
    "range": {
      "counter": {
        "gte": 10223372036854775807
      }
    }
  }
}
```
{% include copy-curl.html %}


`unsigned_long` 欄位不能做為索引排序欄位 (在 `sort.field` 索引設定中)。
{: .warning}

## 彙總

與其他數值欄位一樣，`unsigned_long` 欄位支援彙總。對於 `terms` 和 `multi_terms` 彙總，`unsigned_long` 值會依原樣使用，但對於其他彙總類型，這些值會轉換為 `double` 類型 (可能損失精確度)。以下是 `terms` 彙總的範例：

```json
POST _search
{
  "query": {
    "match_all": {}
  },
  "aggs": {
    "counters": {
      "terms": { 
         "field": "counter" 
      }
    }
  }
}
```
{% include copy-curl.html %}

## 指令碼

在指令碼中，`unsigned_long` 欄位會以 `BigInteger` 類別的執行個體形式傳回：

```json
POST _search
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": "BigInteger amount = doc['counter'].value; return amount.compareTo(BigInteger.ZERO) > 0;"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}


## 限制

請注意 `unsigned_long` 欄位類型的下列限制：

- 當跨不同數值類型執行彙總，且其中一個類型是 `unsigned_long` 時，這些值會轉換為 `double` 類型，並使用 `double` 算術，很可能會損失精確度。

- `unsigned_long` 欄位不能做為索引排序欄位 (在 `sort.field` 索引設定中)。當對多個索引執行搜尋，且結果依至少其中一個索引中具有 `unsigned_long` 類型、但其他索引中具有不同數值類型的欄位排序時，這項限制也適用。 