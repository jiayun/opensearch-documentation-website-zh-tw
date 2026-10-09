---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "如何使用指令碼"
nav_order: 10
---

# 如何使用指令碼

每個接受指令碼的 OpenSearch API 都使用相同的請求語法，因此一旦您了解 `script` 物件的結構，就能將它套用至搜尋、彙總、更新、資料匯入管線和索引對應等各種用途：

```json
"script": {
  "lang": "painless",
  "source": "doc['price'].value * multiplier",
  "params": {
    "multiplier": 0.8
  }
}
```

下表列出 `script` 物件的欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`lang` | 字串 | 指令碼撰寫所用的語言。預設為 `painless`。
`source` | 字串 | 指令碼本文。內嵌指令碼請使用此欄位。`source` 或 `id` 兩者必須擇一。
`id` | 字串 | 以 [Create or Update Stored Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/) 儲存的指令碼識別碼。執行已儲存的指令碼時，請使用此欄位而非 `source`。`source` 或 `id` 兩者必須擇一。
`params` | 物件 | OpenSearch 以變數形式傳入指令碼的具名值。選用。

## 測試設定

本頁及整份指令碼編寫文件中的範例都使用產品記錄的索引。請使用下列對應建立索引：

```json
PUT scripting-products
{
  "mappings": {
    "properties": {
      "name":         { "type": "text" },
      "sku":          { "type": "keyword", "store": true },
      "brand":        { "type": "keyword", "store": true },
      "category":     { "type": "keyword" },
      "price":        { "type": "double" },
      "quantity":     { "type": "integer" },
      "ratings":      { "type": "integer" },
      "on_sale":      { "type": "boolean" },
      "release_date": { "type": "date" },
      "warehouse":    { "type": "geo_point" }
    }
  }
}
```
{% include copy-curl.html %}

接著將四項產品編製索引：

```json
POST scripting-products/_bulk?refresh=true
{"index":{"_id":"1"}}
{"name":"Wireless noise cancelling headphones","sku":"AUD-1001","brand":"Aurora","category":"audio","price":249.99,"quantity":42,"ratings":[5,4,5,3],"on_sale":true,"release_date":"2024-03-15","warehouse":{"lat":47.6062,"lon":-122.3321}}
{"index":{"_id":"2"}}
{"name":"Wireless earbuds","sku":"AUD-1002","brand":"Aurora","category":"audio","price":129.5,"quantity":8,"ratings":[4,4],"on_sale":false,"release_date":"2025-01-20","warehouse":{"lat":37.7749,"lon":-122.4194}}
{"index":{"_id":"3"}}
{"name":"Mechanical keyboard","sku":"ACC-2001","brand":"Northwind","category":"accessories","price":89.0,"quantity":120,"ratings":[5,5,5],"on_sale":true,"release_date":"2023-11-02","warehouse":{"lat":41.8781,"lon":-87.6298}}
{"index":{"_id":"4"}}
{"name":"Ultrawide monitor","sku":"DSP-3001","brand":"Northwind","category":"displays","price":599.0,"quantity":0,"on_sale":false,"release_date":"2025-06-10","warehouse":{"lat":30.2672,"lon":-97.7431}}
```
{% include copy-curl.html %}

## 執行內嵌指令碼

_內嵌_ 指令碼是在請求本文的 `source` 欄位中指定。下列搜尋會對某項產品的價格套用折扣，並將結果以 [指令碼欄位]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/retrieve-specific-fields/#using-scripted-fields) 傳回，而不會更動已儲存的文件：

```json
GET scripting-products/_search
{
  "_source": false,
  "query": { "term": { "sku": "AUD-1001" } },
  "script_fields": {
    "sale_price": {
      "script": {
        "lang": "expression",
        "source": "doc['price'] * discount",
        "params": { "discount": 0.8 }
      }
    }
  }
}
```
{% include copy-curl.html %}

`sale_price` 欄位會在請求時計算：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 372,
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
          "sale_price": [
            199.99200000000002
          ]
        }
      }
    ]
  }
}
```
</details>

## 以參數傳遞值

請將每次請求之間會變動的每個值透過 `params` 傳遞，而不要將它寫入指令碼本文，這樣指令碼只需編譯一次，之後的每次請求都會重複使用編譯後的結果。OpenSearch 會在首次使用時編譯每個不同的指令碼並加以快取，而編譯相對於執行已編譯的指令碼較為緩慢。

例如，下列指令碼將折扣寫死，因此每個折扣值都是各自編譯的不同指令碼：

```json
"source": "doc['price'] * 0.8"
```

參數化的版本只編譯一次，並重複用於每個折扣：

```json
"source": "doc['price'] * discount",
"params": { "discount": 0.8 }
```

在短時間內編譯太多不同的指令碼，會導致 OpenSearch 以 `circuit_breaking_exception` 拒絕後續的編譯。提高編譯上限只能治標；將指令碼參數化才能治本。關於控管此上限的設定，請參閱 [編譯限制與快取](#compilation-limits-and-caching)。
{: .note}

## 使用簡短指令碼形式

當指令碼不需要 `lang` 也不需要 `params` 時，您可以用純字串形式的指令碼本文取代 `script` 物件。下列更新使用簡短形式來增加某項產品的庫存數量：

```json
POST scripting-products/_update/3
{
  "script": "ctx._source.quantity++"
}
```
{% include copy-curl.html %}

簡短形式等同於下列物件形式：

```json
"script": {
  "source": "ctx._source.quantity++"
}
```

文件會更新，且其版本會遞增：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "_index": "scripting-products",
  "_id": "3",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 4,
  "_primary_term": 1
}
```
</details>

## 使用已儲存的指令碼

_已儲存的_ 指令碼會以識別碼儲存在叢集狀態中，並以 `id` 而非 `source` 來參照。儲存指令碼可將單一定義保存在同一處，呼叫端就不必重複指令碼本文，您也能變更邏輯而不必重新部署呼叫它的應用程式。

建立名為 `stock-boosted-score` 的指令碼，依庫存數量調整相符文件的相關性分數：

```json
POST _scripts/stock-boosted-score
{
  "script": {
    "lang": "painless",
    "source": "_score * (1 + Math.log(1 + params.stock_weight * doc['quantity'].value))"
  }
}
```
{% include copy-curl.html %}

若要讓 OpenSearch 在儲存時就針對特定情境編譯指令碼，而非等到首次使用時才編譯，請將情境附加至路徑，成為 `_scripts/<id>/<context>`：

```json
POST _scripts/stock-boosted-score/score
{
  "script": {
    "lang": "painless",
    "source": "_score * (1 + Math.log(1 + params.stock_weight * doc['quantity'].value))"
  }
}
```
{% include copy-curl.html %}

如果指令碼對具名情境而言無效，提早編譯會在此請求傳回錯誤，而不是在首次使用該指令碼的搜尋時才傳回。關於您的叢集支援的情境清單，請使用 [Get Script Contexts API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-contexts/)。

若要確認指令碼已儲存，請擷取已儲存的指令碼：

```json
GET _scripts/stock-boosted-score
```
{% include copy-curl.html %}

回應會傳回語言和本文：

```json
{
  "_id": "stock-boosted-score",
  "found": true,
  "script": {
    "lang": "painless",
    "source": "_score * (1 + Math.log(1 + params.stock_weight * doc['quantity'].value))"
  }
}
```

若要執行已儲存的指令碼，請將 `source` 取代為 `id`，並提供指令碼所宣告的參數：

```json
GET scripting-products/_search
{
  "query": {
    "script_score": {
      "query": { "match": { "name": "wireless" } },
      "script": {
        "id": "stock-boosted-score",
        "params": { "stock_weight": 0.5 }
      }
    }
  }
}
```
{% include copy-curl.html %}

兩項相符的產品都會傳回，並附上由已儲存指令碼產生的分數：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "took": 77,
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
    "max_score": 1.2791357,
    "hits": [
      {
        "_index": "scripting-products",
        "_id": "1",
        "_score": 1.2791357,
        "_source": {
          "name": "Wireless noise cancelling headphones",
          "sku": "AUD-1001",
          "brand": "Aurora",
          "category": "audio",
          "price": 249.99,
          "quantity": 42,
          "ratings": [5, 4, 5, 3],
          "on_sale": true,
          "release_date": "2024-03-15",
          "warehouse": { "lat": 47.6062, "lon": -122.3321 }
        }
      },
      {
        "_index": "scripting-products",
        "_id": "2",
        "_score": 1.1143811,
        "_source": {
          "name": "Wireless earbuds",
          "sku": "AUD-1002",
          "brand": "Aurora",
          "category": "audio",
          "price": 129.5,
          "quantity": 8,
          "ratings": [4, 4],
          "on_sale": false,
          "release_date": "2025-01-20",
          "warehouse": { "lat": 37.7749, "lon": -122.4194 }
        }
      }
    ]
  }
}
```
</details>

當已儲存的指令碼不再被參照時，請傳送下列請求將它刪除：

```json
DELETE _scripts/stock-boosted-score
```
{% include copy-curl.html %}

刪除指令碼並不會使參照它的請求失效。指名已刪除指令碼的搜尋會在請求時失敗，因此請先移除呼叫端。
{: .warning}

由於叢集狀態會儲存這些指令碼，建立、擷取和刪除它們都是叢集層級的操作，需要 `cluster:admin/script/put`、`cluster:admin/script/get` 和 `cluster:admin/script/delete` 權限。如需詳細資訊，請參閱 [權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。

## 儲存搜尋範本

`_scripts` 端點也會儲存 _搜尋範本_：以 `mustache` 語言撰寫的完整搜尋請求，並以預留位置取代每次呼叫之間會變動的值。呼叫者只需提供範本識別碼與預留位置的值，而無需提供完整的請求本文，如此可將經常重複的查詢保存在一份經過審核的定義中。如需更多資訊，請參閱 [Search Templates API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/)。

## 編譯限制與快取

OpenSearch 會快取已編譯的指令碼，因此只有在指令碼定義變更時才會重新編譯。此外，OpenSearch 會限制新編譯的發生頻率，避免大量不重複的指令碼在編譯時耗盡節點的 CPU。超過限制時，請求會失敗並傳回 `circuit_breaking_exception`。

預設情況下，每個指令碼情境都有自己的快取與自己的編譯頻率，因此某個情境中頻繁的重新編譯不會驅逐另一個情境中已快取的指令碼。將 `script.max_compilations_rate` 設定為明確的頻率，會以一個共用快取與單一叢集層級限制取代每個情境的快取與頻率。另有獨立的設定可限制單一指令碼的大小；接近該上限的指令碼表示其邏輯應該放在外掛程式中。如需控制快取、編譯頻率與指令碼大小的設定及其預設值，請參閱 [指令碼與資源設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/script-and-resource-settings/)。

若要確認快取是否如預期運作，請檢查 [Nodes Stats API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-stats/) 回應中的 `script` 區段，其中會報告每個節點的 `compilations`、`cache_evictions` 與 `compilation_limit_triggered`：

```json
GET _nodes/stats/script
```
{% include copy-curl.html %}

在工作負載不變的情況下，`compilations` 次數持續增加，表示有指令碼將應透過 `params` 傳入的值寫死在程式碼中。`cache_evictions` 次數持續增加，表示快取對於使用中的不重複指令碼數量而言太小。

## 解讀指令碼錯誤

當指令碼失敗時，OpenSearch 會以 `script_exception` 傳回失敗資訊，其中的 `reason` 可區分在指令碼無法解析時引發的 `compile error`，以及在已編譯的指令碼對特定文件執行失敗時引發的 `runtime error`。例如，下列錯誤的查詢省略了乘法的右側運算元：

```json
GET scripting-products/_search
{
  "script_fields": {
    "sale_price": {
      "script": { "source": "doc['price'].value *" }
    }
  }
}
```
{% include copy-curl.html %}

`script_stack` 欄位會以插入號（^）標記錯誤在指令碼本文中的位置：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "compile error",
        "script_stack": [
          "doc['price'].value *",
          "                    ^---- HERE"
        ],
        "script": "doc['price'].value *",
        "lang": "painless",
        "position": {
          "offset": 20,
          "start": 0,
          "end": 20
        }
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed"
  },
  "status": 400
}
```
</details>

`position` 物件以自指令碼本文開頭起算的字元數提供相同的位置資訊：`offset` 是錯誤的位置，`start` 與 `end` 則界定周圍的區域。當指令碼是由程式產生而非手寫時，計算字元數特別有用，因為 `script_stack` 中的插入號很難對應回產生它的程式碼。

## 相關文件

- [在指令碼中存取文件欄位]({{site.url}}{{site.baseurl}}/scripting/accessing-fields/)
- [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)
- [指令碼 API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/)
