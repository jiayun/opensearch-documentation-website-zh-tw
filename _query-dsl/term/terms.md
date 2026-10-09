---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙"
parent: Term-level queries
nav_order: 20
---

# 詞彙查詢

使用 `terms` 查詢，在同一個欄位中搜尋多個詞彙。例如，下列查詢會搜尋 ID 為 `61809` 和 `61810` 的行：

```json
GET shakespeare/_search
{
  "query": {
    "terms": {
      "line_id": [
        "61809",
        "61810"
      ]
    }
  }
}
```
{% include copy-curl.html %}

如果文件符合陣列中的任一詞彙，就會傳回該文件。

預設情況下，`terms` 查詢允許的詞彙數量上限為 65,536。若要變更詞彙數量上限，請更新 `index.max_terms_count` 設定。

為了提升查詢效能，請將包含大量詞彙的陣列依排序順序傳入（依 UTF-8 位元組值遞增排序）。
{: .tip}


詞彙查詢是否能[醒目提示結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/)，取決於醒目提示器的類型和查詢中的詞彙數量，因此可能無法保證。
{: .note}

## 參數

此查詢接受下列參數。所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`<field>` | 字串 | 要搜尋的欄位。只有當文件的欄位值與至少一個詞彙完全相符，且空格和大小寫皆正確時，才會在結果中傳回該文件。
`boost` | 浮點數 | 指定此欄位對相關性分數之權重的浮點數值。大於 1.0 的值會提高欄位的相關性。介於 0.0 和 1.0 之間的值會降低欄位的相關性。預設為 1.0。
`_name` | 字串 | 用於查詢標記的查詢名稱。選用。
`value_type` | 字串 | 指定用於篩選的值類型。有效值為 `default` 和 `bitmap`。若省略，則預設值為 `default`。

## 詞彙查找

詞彙查找會擷取單一文件的欄位值，並將其用作搜尋詞彙。您可以使用詞彙查找來搜尋大量詞彙。

若要使用詞彙查找，您必須啟用 `_source` 對應欄位，因為詞彙查找會從文件擷取值。`_source` 欄位預設為啟用。

詞彙查找會嘗試從本機資料節點上的分片擷取文件欄位值。因此，使用具有單一主要分片，且在所有適用資料節點上都有完整副本的索引，可減少網路流量。

### 範例

舉例來說，建立包含學生資料的索引，並將 `student_id` 對應為 `keyword`：

```json
PUT students
{
  "mappings": {
    "properties": {
      "student_id": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

接著，將三份對應學生的文件編製索引：

```json
PUT students/_doc/1
{
  "name": "Jane Doe",
  "student_id" : "111"
}
```
{% include copy-curl.html %}

```json
PUT students/_doc/2
{
  "name": "Mary Major",
  "student_id" : "222"
}
```
{% include copy-curl.html %}

```json
PUT students/_doc/3
{
  "name": "John Doe",
  "student_id" : "333"
}
```
{% include copy-curl.html %}

建立另一個索引，包含課程資訊，其中包括課程名稱，以及由修讀該課程之學生的 ID 所組成的陣列：

```json
PUT classes/_doc/101
{
  "name": "CS101",
  "enrolled" : ["111" , "222"]
}
```
{% include copy-curl.html %}

若要搜尋修讀 `CS101` 課程的學生，請指定對應該課程之文件的文件 ID、該文件的索引，以及詞彙所在欄位的路徑：

```json
GET students/_search
{
  "query": {
    "terms": {
      "student_id": {
        "index": "classes",
        "id": "101",
        "path": "enrolled"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含 `students` 索引中所有 ID 與 `enrolled` 陣列中任一值相符之學生的文件：

```json
{
  "took": 13,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Jane Doe",
          "student_id": "111"
        }
      },
      {
        "_index": "students",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Mary Major",
          "student_id": "222"
        }
      }
    ]
  }
}
```

### 範例：巢狀欄位

第二個範例示範如何查詢巢狀欄位。假設有一個索引包含下列文件：

```json
PUT classes/_doc/102
{
  "name": "CS102",
  "enrolled_students" : {
    "id_list" : ["111" , "333"]
  }
}
```
{% include copy-curl.html %}

若要搜尋修讀 `CS102` 的學生，請使用點號路徑表示法，在 `path` 參數中指定欄位的完整路徑：

```json
GET students/_search
{
  "query": {
    "terms": {
      "student_id": {
        "index": "classes",
        "id": "102",
        "path": "enrolled_students.id_list"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會包含相符的文件：

```json
{
  "took": 18,
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
    "max_score": 1,
    "hits": [
      {
        "_index": "students",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Jane Doe",
          "student_id": "111"
        }
      },
      {
        "_index": "students",
        "_id": "3",
        "_score": 1,
        "_source": {
          "name": "John Doe",
          "student_id": "333"
        }
      }
    ]
  }
}
```

### 參數

下表列出詞彙查找參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 要從中擷取欄位值的索引名稱。必要。
`id` | 字串 | 要從中擷取欄位值之文件的文件 ID。必要。
`query` | 物件 | 用於選取多份文件以擷取欄位值的查詢物件。若未提供 `id`，則為必要。
`path` | 字串 | 要從中擷取欄位值的欄位名稱。使用點號路徑表示法指定巢狀欄位。必要。
`routing` | 字串 | 要從中擷取欄位值之文件的自訂路由值。選用。若在將文件編製索引時提供了自訂路由值，則為必要。
`store` | 布林值 | 是否對儲存的欄位執行查找，而非對 `_source` 執行查找。選用。

## 透過查詢進行詞彙查找
**於 3.2 版推出**
{: .label .label-purple}

您可以使用查詢，動態擷取多份文件中的值，並將其用於 `terms` 查詢。`query` 參數讓您無須指定文件 ID，即可比對文件，並收集所有相符文件中指定欄位的全部值。

當您想根據另一個索引中文件的欄位值來搜尋某個索引時，這項功能很有用。

如需支援的參數清單，請參閱[詞彙查找參數](#parameters-1)。若要透過查詢進行詞彙查找，您必須在詞彙查找物件中提供 `query` 參數，而非 `id`。  

### 值的收集方式

詞彙查閱的行為取決於目標欄位在符合的文件中出現的方式：

- 如果符合查詢的文件未包含指定的欄位，則該文件會被忽略，不進行詞彙擷取。
- 如果欄位是清單，則會收集其所有項目。
- 如果欄位是純量，則會收集其值。
- 如果同一個欄位在不同文件中是單一值或清單，則所有值會扁平化為單一清單並去除重複。
- 多個清單會扁平化為單一清單。
- 如果欄位缺少、`null` 或為空清單，則會略過。
- 來自多個文件的重複項目會去除重複。
- 如果沒有文件符合查詢，則 `terms` 查詢的行為就如同未指定任何值（通常不會符合任何項目）。
- 如果符合的文件中沒有任何一個包含該欄位，則查詢不會符合任何項目。

### 範例

首先，建立名為 `users` 的索引，其中包含使用者資訊：

```json
PUT /users
{
  "mappings": {
    "properties": {
      "username": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將使用者資料新增至索引：

```json
PUT users/_doc/u1
{ "username": "alice" }
```
{% include copy-curl.html %}

```json
PUT users/_doc/u2
{ "username": "bob" }
```
{% include copy-curl.html %}

```json
PUT users/_doc/u3
{ "username": "carol" }
```
{% include copy-curl.html %}

```json
PUT users/_doc/u4
{ "username": "dave" }
```
{% include copy-curl.html %}

接著，建立包含群組成員資格的索引：

```json
PUT groups
{
  "mappings": {
    "properties": {
      "group": { "type": "keyword" },
      "members": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將群組成員資格資料新增至索引：

```json
PUT groups/_doc/1
{
  "group": "g1",
  "members": ["alice", "bob"]
}
```
{% include copy-curl.html %}

```json
PUT groups/_doc/2
{
  "group": "g1",
  "members": "carol"
}
```
{% include copy-curl.html %}

```json
PUT groups/_doc/3
{
  "group": "g1"
}
```
{% include copy-curl.html %}

```json
PUT groups/_doc/4
{
  "group": "g1",
  "members": []
}
```
{% include copy-curl.html %}

```json
PUT groups/_doc/5
{
  "group": "g1",
  "members": null
}
```
{% include copy-curl.html %}

```json
PUT groups/_doc/6
{
  "group": "g2",
  "members": "carol"
}
```
{% include copy-curl.html %}

若要在 `users` 索引中搜尋所有屬於 `g1` 群組的成員使用者，請使用下列請求：

```json
GET /users/_search
{
  "query": {
    "terms": {
      "username": {
        "index": "groups",
        "path": "members",
        "query": {
          "term": { "group": "g1" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢會從 `groups` 中文件的 `members` 欄位收集所有值，這些文件的 `group` 設為 `g1`，並將這些值用作 `users` 索引中 `username` 欄位的詞彙：

```json
{
  "hits": {
    "total": { "value": 3, "relation": "eq" },
    "hits": [
      { "_index": "users", "_id": "u1", "_score": 1.0, "_source": { "username": "alice" } },
      { "_index": "users", "_id": "u2", "_score": 1.0, "_source": { "username": "bob" } },
      { "_index": "users", "_id": "u3", "_score": 1.0, "_source": { "username": "carol" } }
    ]
  }
}
```

此查詢會以下列方式處理符合的文件：

- 查閱查詢符合文件 1、2、3、4 和 5（全都指定群組 `g1`）。
- 文件 6（使用不同的群組 `g2`）會被查詢忽略。
- 每個符合文件的 `members` 欄位會以下列方式處理：
    - 文件 1：`["alice", "bob"]`（清單）→ 同時收集 `alice` 和 `bob`。
    - 文件 2：`"carol"`（純量）→ 收集 `carol`。
    - 文件 3：缺少 `members` 欄位 → 忽略。
    - 文件 4：空清單 → 忽略。
    - 文件 5：null → 忽略。
- 所有收集到的值都會扁平化並去除重複，因此最終結果為 `["alice", "bob", "carol"]`。

## 點陣圖篩選
**於 2.17 版推出**
{: .label .label-purple }

`terms` 查詢可以同時篩選多個詞彙。然而，當輸入篩選條件中的詞彙數量增加到很大的值（約 10,000 個）時，隨之而來的網路和記憶體額外負荷可能會變得相當可觀，導致查詢效率低落。在這種情況下，請考慮使用 [roaring bitmap](https://github.com/RoaringBitmap/RoaringBitmap) 來編碼您的大型詞彙篩選條件，以獲得更有效率的篩選。

下列範例假設您有兩個索引：`products` 索引，其中包含某家公司販售的所有產品，以及 `customers` 索引，其中儲存代表擁有特定產品之客戶的篩選條件。

首先，建立 `products` 索引並將 `product_id` 對應為整數：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "product_id": { "type": "integer" }
    }
  }
}
```
{% include copy-curl.html %}

接著，將三個對應至產品的文件編製索引：

```json
PUT /products/_doc/1
{
  "name": "Product 1",
  "product_id" : 111
}
```
{% include copy-curl.html %}

```json
PUT /products/_doc/2
{
  "name": "Product 2",
  "product_id" : 222
}
```
{% include copy-curl.html %}

```json
PUT /products/_doc/3
{
  "name": "Product 3",
  "product_id" : 333
}
```
{% include copy-curl.html %}

若要儲存客戶點陣圖篩選條件，您將在 `customers` 索引中建立 `customer_filter` [二進位欄位]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/binary/)。指定 `store` 為 `true` 以儲存該欄位：

```json
PUT /customers
{
  "mappings": {
    "properties": {
      "customer_filter": {
        "type": "binary",
        "store": true
      }
    }
  }
}
```
{% include copy-curl.html %}

針對每位客戶，您需要產生一個點陣圖，代表該客戶擁有之產品的產品 ID。此點陣圖會有效地編碼該客戶的篩選條件。在此範例中，您將為 ID 為 `customer123` 且擁有產品 `111`、`222` 和 `333` 的客戶建立 `terms` 篩選條件。

若要為該客戶編碼 `terms` 篩選條件，請先為該篩選條件建立 roaring bitmap。此範例使用 [PyRoaringBitMap] 程式庫建立點陣圖，因此請先執行 `pip install pyroaring` 來安裝該程式庫。然後將點陣圖序列化，並使用 [Base64](https://en.wikipedia.org/wiki/Base64) 編碼配置進行編碼：

```py
from pyroaring import BitMap
import base64

# Create a bitmap, serialize it into a byte string, and encode into Base64
bm = BitMap([111, 222, 333]) # product ids owned by a customer
encoded = base64.b64encode(BitMap.serialize(bm))

# Convert the Base64-encoded bytes to a string for storage or transmission
encoded_bm_str = encoded.decode('utf-8')

# Print the encoded bitmap
print(f"Encoded Bitmap: {encoded_bm_str}")
```
{% include copy.html %}

接著，將客戶篩選條件編製索引至 `customers` 索引。篩選條件的文件 ID 與對應客戶的 ID 相同（在此範例中為 `customer123`）。`customer_filter` 欄位包含您為此客戶產生的點陣圖：

```json
POST customers/_doc/customer123
{
  "customer_filter": "OjAAAAEAAAAAAAIAEAAAAG8A3gBNAQ=="
}
```
{% include copy-curl.html %}

現在您可以在 `products` 索引上執行 `terms` 查詢，以在 `customers` 索引中查閱特定客戶。因為您查閱的是已儲存的欄位而非 `_source`，請將 `store` 設為 `true`。在 `value_type` 欄位中，將 `terms` 輸入的資料類型指定為 `bitmap`：

```json
POST /products/_search
{
  "query": {
    "terms": {
      "product_id": {
        "index": "customers",
        "id": "customer123",
        "path": "customer_filter",
        "store": true               
      },
      "value_type": "bitmap"      
    }
  }
}
```
{% include copy-curl.html %}

您也可以直接將點陣圖傳遞至 `terms` 查詢。在此範例中，`product_id` 欄位包含 ID 為 `customer123` 之客戶的客戶篩選條件點陣圖：

```json
POST /products/_search
{
  "query": {
    "terms": {
      "product_id": [
        "OjAAAAEAAAAAAAIAEAAAAG8A3gBNAQ=="
      ],
      "value_type": "bitmap"
    }
  }
}
```
{% include copy-curl.html %}
