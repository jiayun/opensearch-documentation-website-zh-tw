---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在指令碼中存取文件欄位"
nav_order: 20
---

# 在指令碼中存取文件欄位

指令碼透過 OpenSearch 在執行指令碼前注入的變數來讀取文件資料。指令碼可用的變數取決於其情境：在更新期間修改文件的指令碼，與為搜尋結果評分的指令碼，會收到不同的變數集。選擇正確的存取路徑對效能至關重要，因為搜尋或彙總指令碼會針對每個候選文件執行一次，而讀取 `_source` 欄位所需的每份文件資源遠多於讀取 doc values。

本頁說明存取路徑，以及主要情境系列所提供的變數。如需每個個別情境的變數與傳回類型，請參閱[指令碼情境]({{site.url}}{{site.baseurl}}/scripting/script-contexts/)。

本頁的範例使用 `scripting-products` 索引。若要建立它，請參閱[測試設定]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#test-setup)。

## 更新指令碼

[Update Document]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-document/)、[Update By Query]({{site.url}}{{site.baseurl}}/api-reference/document-apis/update-by-query/) 和 [Reindex]({{site.url}}{{site.baseurl}}/api-reference/document-apis/reindex/) API 中的指令碼會收到單一 `ctx` 變數。下表列出 `ctx` 欄位。

欄位 | 說明
:--- | :---
`ctx._source` | 文件 [`_source`]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/)，為可修改的 map。對其項目賦值，即可變更 OpenSearch 寫入的文件。
`ctx.op` | 要套用至文件的操作。將其設為 `index` 以寫入修改後的文件，設為 `delete` 以移除文件，或設為 `noop` 以保持不變並略過寫入。
`ctx._index`、`ctx._id` 及其他[中繼資料欄位]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/index/) | 正在處理之文件的中繼資料。其中部分為唯讀。

下列更新會為文件 `4` 記錄一筆交貨，該文件的 `quantity` 為 `0`。指令碼會讀取 `ctx._source.quantity`，將收到的單位數加到其中，並從產生的值推導出 `on_sale`。若未收到任何單位，則將 `ctx.op` 設為 `noop`，讓 OpenSearch 略過寫入：

```json
POST scripting-products/_update/4
{
  "script": {
    "lang": "painless",
    "source": "if (params.received == 0) { ctx.op = 'noop' } else { ctx._source.quantity += params.received; ctx._source.on_sale = ctx._source.quantity > 20 }",
    "params": { "received": 25 }
  }
}
```
{% include copy-curl.html %}

`result` 欄位回報文件已寫入，且 `_version` 會遞增：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "_index": "scripting-products",
  "_id": "4",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 5,
  "_primary_term": 1
}
```
</details>

該文件現在的 `quantity` 為 `25`，且 `on_sale` 值為 `true`。以 `"received": 0` 傳送相同的請求會走 `noop` 分支，其會傳回 `"result": "noop"` 並使 `_version` 保持不變。

更新指令碼僅透過 `ctx._source` 讀取及修改文件資料。下列各節所述的三種存取路徑皆無法供其使用：`doc` 會因 `cannot resolve symbol [doc]` 而無法編譯，而 `params._source` 與 `params._fields` 為 `null`，因此從其中任一者讀取欄位會在執行階段失敗並產生 `null_pointer_exception`。
{: .note}

## 搜尋與彙總指令碼

搜尋與彙總中的指令碼會針對每個可能相符的文件執行一次，這在大型索引上意味著單一請求會執行指令碼數百萬次。[指令碼欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields)是例外：它們會針對每個傳回的結果執行一次，因此其執行次數受頁面大小而非索引大小限制。

這些指令碼透過 doc values、`_source` 欄位或已儲存的欄位讀取欄位值。下表摘要說明這三種存取類型。

存取類型 | 語法 | 資源用量 | 適用情況
:--- | :--- | :--- | :---
文件值（doc values） | `doc['field']` | 最低 | 對數字、日期、地理點或關鍵字進行評分、排序、篩選或彙總。
`_source` | `params._source.field` | 最高 | 指令碼欄位需要 JSON 物件、`text` 欄位，或單一頁面上結果的確切原始值。
已儲存的欄位 | `params._fields['field'].value` | 高 | `_source` 很大，而指令碼只需要其中幾個小欄位。

對評分或排序有貢獻的指令碼也會收到 `_score`，即目前文件的相關性分數。

### 文件值（doc values）

在指令碼中讀取欄位最快的方式是使用[文件值]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)。Doc values 會將欄位值儲存在一個以欄為導向的結構中，該結構在建立索引時建置，並直接從磁碟讀取，這正是指令碼所需的存取模式：一個欄位、多份文件。使用 `doc['field_name']` 語法存取欄位。

除了經過分析的 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位外，所有欄位類型預設都會啟用 doc values。

下列搜尋會將每個音訊產品的價格乘以其庫存數量，以計算其總庫存價值。它會從 doc values 讀取這兩個變數：

```json
GET scripting-products/_search
{
  "_source": false,
  "query": { "term": { "category": "audio" } },
  "script_fields": {
    "inventory_value": {
      "script": {
        "lang": "expression",
        "source": "doc['price'] * doc['quantity']"
      }
    }
  }
}
```
{% include copy-curl.html %}

每個結果都包含計算出的欄位：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": 1.0,
        "fields": {
          "inventory_value": [
            10499.58
          ]
        }
      },
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": 1.0,
        "fields": {
          "inventory_value": [
            1036.0
          ]
        }
      }
    ]
  }
}
```
</details>

Doc values 會傳回純量值，例如數字、日期、地理點和詞彙，或針對多值欄位傳回純量陣列。它們無法傳回 JSON 物件，因此需要巢狀物件結構的指令碼必須改為讀取 `_source`。

#### 處理缺少的欄位

若讀取對應中不存在之欄位的 `doc['field']`，會引發 `script_exception`，原因為 `runtime error`，肇因於 `No field found for [discount] in mapping`。在 Painless 中，請使用 `doc.containsKey('field')` 保護該存取：

```json
"source": "doc.containsKey('discount') ? doc['discount'].value : 0"
```

`expression` 指令碼沒有對等的保護機制，因為該語言未提供任何方法來測試欄位是否存在於對應中。它只能使用 `doc['field'].empty` 來區分已對應但不存在於目前文件中的欄位。如需更多資訊，請參閱 [Lucene 運算式語言]({{site.url}}{{site.baseurl}}/scripting/expressions/)。
{: .note}

#### 讀取文字欄位

在 Painless 中，`doc['field']` 語法僅在已分析的 `text` 欄位上啟用 [`fielddata`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/field-data/) 時才能運作，且它會傳回分析後的詞元，而非原始字串。啟用 `fielddata` 會將欄位中的每個詞元載入 JVM 堆積，這會同時消耗記憶體與 CPU，並可能導致節點不穩定。請對應一個 `keyword` 子欄位，並讓指令碼改為讀取該子欄位。
{: .warning}

### 文件來源

`_source` 欄位包含已編製索引的原始 JSON 文件本文。若要讀取 `_source`，請使用 `params._source.field_name` 語法。若要讀取巢狀欄位，請使用完整路徑。例如，測試索引的 `warehouse` 欄位是一個以 `{"lat": 47.6062, "lon": -122.3321}` 編製索引的 `geo_point`，因此其緯度會讀取為 `params._source.warehouse.lat`。

下列搜尋會從兩個 `_source` 欄位組出一個型錄標籤：

```json
GET scripting-products/_search
{
  "_source": false,
  "query": { "term": { "sku": "AUD-1002" } },
  "script_fields": {
    "catalog_label": {
      "script": {
        "lang": "painless",
        "source": "params._source.brand + ': ' + params._source.name"
      }
    }
  }
}
```
{% include copy-curl.html %}

串接後的標籤會隨結果一併傳回：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 23,
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": 1.0,
        "fields": {
          "catalog_label": [
            "Aurora: Wireless earbuds"
          ]
        }
      }
    ]
  }
}
```
</details>

讀取 `_source` 比讀取 doc values 慢得多，因為 OpenSearch 必須載入並剖析整個已儲存的 JSON 本文才能讀取一個欄位。`_source` 欄位經過最佳化，適合從少數文件中傳回許多欄位；doc values 則經過最佳化，適合從許多文件中傳回單一欄位。

當指令碼欄位為單一頁面的結果建立輸出，且您需要的值是 JSON 物件或 doc values 無法提供的 `text` 欄位時，請使用 `_source`。若用於評分、排序、篩選及彙總，請使用 doc values。
{: .note}

### 已儲存的欄位

使用 [`"store": true`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/) 對應的欄位會與 `_source` 分開寫入索引，並可使用 `params._fields['field_name'].value` 語法讀取。在測試索引中，`sku` 與 `brand` 是已儲存的欄位。

必須加上 `.value` 後置字元。單獨使用 `params._fields['field_name']` 會傳回內部的欄位查閱物件而非值，且從指令碼欄位傳回它會失敗並出現 `cannot write xcontent for unknown value of type`。當欄位有多個值時，請使用 `.value` 取得第一個值，並使用 `.values` 取得完整清單。
{: .note}

下列搜尋會將 `brand` 與 `sku` 這兩個已儲存的欄位合併成單一識別碼：

```json
GET scripting-products/_search
{
  "_source": false,
  "query": { "term": { "sku": "AUD-1001" } },
  "script_fields": {
    "brand_sku": {
      "script": {
        "lang": "painless",
        "source": "params._fields['brand'].value + ' ' + params._fields['sku'].value"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含合併後的值：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 9,
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": 1.0,
        "fields": {
          "brand_sku": [
            "Aurora AUD-1001"
          ]
        }
      }
    ]
  }
}
```
</details>

`_source` 欄位本身即為已儲存的欄位，因此讀取已儲存的欄位所需花費的時間與記憶體，與讀取 `_source` 大致相同。與已儲存的欄位不同，`_source` 會傳回編製索引當時的完整 JSON：它會保留 `null` 與欄位不存在之間的差異，以及單一元素陣列與純量之間的差異。

當 `_source` 很大，但指令碼只需要其中幾個小值時，已儲存的欄位可縮短讀取時間：將這些值個別儲存可避免載入整個本文。在其他所有情況下，將欄位標示為已儲存會增加索引大小，卻不會縮短讀取時間。

### 存取相關性分數

[`script_score` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/script-score/)、[`function_score` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/)、[以指令碼為基礎的排序]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/sort/) 及彙總中的指令碼會收到 `_score`，也就是外層查詢為目前文件計算出的相關性分數。讀取 `_score` 可讓指令碼調整查詢產生的排名，因此文字相關性仍會影響最終順序。

下列搜尋會依庫存項目數調整每項產品的文字相關性，提升同時符合查詢且有充足庫存的產品。將數量除以 10 可讓加成維持在合理比例，因此庫存數量會影響排名，但不會主導排名：

```json
GET scripting-products/_search
{
  "_source": ["name", "quantity"],
  "query": {
    "function_score": {
      "query": { "match": { "name": "wireless" } },
      "script_score": {
        "script": {
          "lang": "expression",
          "source": "_score * (1 + doc['quantity'] / 10)"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

儘管耳罩式耳機的文字比對較弱，仍因庫存遠多於入耳式耳機而排名較前：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.5083568,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": 0.5083568,
        "_source": {
          "quantity": 42,
          "name": "Wireless noise cancelling headphones"
        }
      },
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": 0.3282812,
        "_source": {
          "quantity": 8,
          "name": "Wireless earbuds"
        }
      }
    ]
  }
}
```
</details>

## 相關文件

- [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)
- [Lucene 運算式語言]({{site.url}}{{site.baseurl}}/scripting/expressions/)
