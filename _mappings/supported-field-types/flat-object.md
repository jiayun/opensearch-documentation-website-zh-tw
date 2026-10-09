---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "扁平物件"
nav_order: 43
has_children: false
parent: Object field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/flat-object/
  - /field-types/flat-object/
---

# 扁平物件欄位類型
**於 2.7 版推出**
{: .label .label-purple }

在 OpenSearch 中，您不需要在將文件編製索引前指定對應。如果您未指定對應，OpenSearch 會使用[動態對應]({{site.url}}{{site.baseurl}}/mappings/index#dynamic-mapping)自動對應文件中的每個欄位及其子欄位。當您匯入記錄檔等文件時，您可能無法事先得知每個欄位的子欄位名稱與類型。在這種情況下，動態對應所有新的子欄位可能會迅速導致「對應爆炸」，也就是欄位數量不斷增加，可能降低叢集的效能。

扁平物件欄位類型將整個 JSON 物件視為字串，藉此解決這個問題。JSON 物件內的子欄位可使用標準點路徑標記法存取，但不會編製索引以供快速查閱。

點標記法中的欄位值長度上限為 2<sup>24</sup> &minus; 1。
{: .note}

扁平物件欄位類型提供下列優點：

- 高效率讀取：擷取效能與 keyword 欄位類似。
- 記憶體效率：將整個複雜的 JSON 物件儲存在單一欄位中，而不為其所有子欄位編製索引，可減少索引中的欄位數量。
- 空間效率：OpenSearch 不會為扁平物件中的子欄位建立倒排索引，因此可節省空間。
- 遷移相容性：您可以將資料從支援類似扁平類型的系統遷移至 OpenSearch。

將欄位對應為扁平物件適用於欄位及其子欄位大多僅供讀取，且不會用作搜尋條件的情況，因為子欄位不會編製索引。扁平物件適用於欄位數量龐大的物件，或您事先不知道索引鍵的情況。

扁平物件支援使用及不使用點路徑標記法的完全相符查詢。如需支援的查詢類型完整清單，請參閱[支援的查詢](#supported-queries)。

在文件中搜尋巢狀欄位的特定值可能效率不佳，因為可能需要完整掃描索引，這可能是相當耗費資源的操作。
{: .note}

扁平物件不支援：

- 類型特定的剖析。
- 數值操作，例如數值比較或數值排序。
- 文字分析。
- 醒目提示。
- 使用點標記法彙總子欄位。
- 依子欄位篩選。

## 支援的查詢

扁平物件欄位類型支援下列查詢：

- [Term]({{site.url}}{{site.baseurl}}/query-dsl/term/term/) 
- [Terms]({{site.url}}{{site.baseurl}}/query-dsl/term/terms/) 
- [Terms set]({{site.url}}{{site.baseurl}}/query-dsl/term/terms-set/)  
- [Prefix]({{site.url}}{{site.baseurl}}/query-dsl/term/prefix/) 
- [Range]({{site.url}}{{site.baseurl}}/query-dsl/term/range/) 
- [Match]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/) 
- [Multi-match]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/) 
- [Query string]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) 
- [Simple query string]({{site.url}}{{site.baseurl}}/query-dsl/full-text/simple-query-string/) 
- [Exists]({{site.url}}{{site.baseurl}}/query-dsl/term/exists/)
- [Wildcard]({{site.url}}{{site.baseurl}}/query-dsl/term/wildcard/)

## 限制

下列限制適用於 OpenSearch 2.7 中的扁平物件：

- 扁平物件不支援開放參數。
- 不支援使用 Painless 指令碼與萬用字元查詢來擷取子欄位的值。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

此功能預計於未來版本推出。

## 使用扁平物件

下列範例說明如何將欄位對應為扁平物件、為含有扁平物件欄位的文件編製索引，以及搜尋這些文件中扁平物件的葉值。

首先，為您的索引建立對應，其中 `issue` 的類型為 `flat_object`：

```json
PUT /test-index/
{
  "mappings": {
    "properties": {
      "issue": {
        "type": "flat_object"
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，為兩份含有扁平物件欄位的文件編製索引：

```json
PUT /test-index/_doc/1
{
  "issue": {
    "number": "123456",
    "labels": {
      "version": "2.1",
      "backport": [
        "2.0",
        "1.3"
      ],
      "category": {
        "type": "API",
        "level": "enhancement"
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /test-index/_doc/2
{
  "issue": {
    "number": "123457",
    "labels": {
      "version": "2.2",
      "category": {
        "type": "API",
        "level": "bug"
      }
    }
  }
}
```
{% include copy-curl.html %}

若要搜尋扁平物件的葉值，請使用 GET 或 POST 請求。即使您不知道欄位名稱，仍可在整個扁平物件中搜尋葉值。例如，下列請求會搜尋所有標示為 bug 的問題：

```json
GET /test-index/_search
{
  "query": {
    "match": {"issue": "bug"}
  }
}
```

或者，如果您知道要在哪個子欄位中搜尋，請以點標記法提供該欄位的路徑：

```json
GET /test-index/_search
{
  "query": {
    "match": {"issue.labels.category.level": "bug"}
  }
}
```
{% include copy-curl.html %}

在兩種情況下，回應都相同，且包含文件 2：

```json
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0303539,
    "hits": [
      {
        "_index": "test-index",
        "_id": "2",
        "_score": 1.0303539,
        "_source": {
          "issue": {
            "number": "123457",
            "labels": {
              "version": "2.2",
              "category": {
                "type": "API",
                "level": "bug"
              }
            }
          }
        }
      }
    ]
  }
}
```

使用前置詞查詢，您可以搜尋版本開頭為 `2.` 的所有問題：

```json
GET /test-index/_search
{
  "query": {
    "prefix": {"issue.labels.version": "2."}
  }
}
```

使用範圍查詢，您可以搜尋版本 2.0--2.1 的所有問題：

```json
GET /test-index/_search
{
  "query": {
    "range": {
      "issue": {
        "gte": "2.0",
        "lte": "2.1"
      }
    }
  }
}
```

## 將子欄位定義為扁平物件

您可以將 JSON 物件的子欄位定義為扁平物件。例如，使用下列查詢將 `issue.labels` 定義為 `flat_object`：

```json
PUT /test-index/
{
  "mappings": {
    "properties": {
      "issue": {
        "properties": {
          "number": {
            "type": "double"
          },
          "labels": {
            "type": "flat_object"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

由於 `issue.number` 不屬於扁平物件的一部分，您可以使用它來彙總及排序文件。

## 相關文件

- [停用物件]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/disable-objects/)
