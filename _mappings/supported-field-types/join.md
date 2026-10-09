---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Join
nav_order: 44
has_children: false
parent: Object field types
grand_parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/join/
  - /opensearch/supported-field-types/join/
  - /field-types/join/
---

# Join 欄位類型
**於 1.0 版推出**
{: .label .label-purple }

`join` 欄位類型定義同一索引內文件之間的父子關係。它會執行下列操作，記錄文件之間的關係，讓查詢能夠連結相關文件：

- 定義關係名稱：指定父類型與子類型的名稱（例如，`brand` 和 `product`）。
- 儲存關係中繼資料：識別哪些文件是父文件、哪些是子文件，以及它們如何連結。
- 啟用父子查詢：支援 `join` 查詢，可透過子文件尋找父文件，或透過父文件尋找子文件。

## 範例

下列範例會建立一個索引，其中品牌是父文件，產品是子文件。 

### 步驟 1：建立對應

建立對應，以建立產品與其品牌之間的父子關係。`name` 欄位儲存產品或品牌名稱。`product_to_brand` 欄位是 `join` 欄位，定義了 `"brand": "product"` 關係，表示 `brand` 文件可以有 `product` 子文件：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      },
      "product_to_brand": {
        "type": "join",
        "relations": {
          "brand": "product"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 步驟 2：將父文件（品牌）編製索引

將代表品牌的父文件編製索引，並在 `product_to_brand` 欄位中定義其在父子關係中的角色（`"brand"`）：

```json
PUT testindex1/_doc/1
{
  "name": "Brand 1",
  "product_to_brand": {
    "name": "brand" 
  }
}
```
{% include copy-curl.html %}

您也可以使用不含物件表示法的簡寫，將父文件編製索引：

```json
PUT testindex1/_doc/1
{
  "name": "Brand 1",
  "product_to_brand" : "brand" 
}
```
{% include copy-curl.html %}

### 步驟 3：將子文件（產品）編製索引

將子文件編製索引時，您必須指定 `routing` 查詢參數，因為同一父子階層中的父文件與子文件必須在同一個分片上編製索引。如需詳細資訊，請參閱[路由]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/routing/)。

每個子文件都會在 `join` 欄位的 `parent` 欄位中參照其父文件的 ID。

將代表產品的兩個子文件編製索引。在 `product_to_brand` 欄位中定義每個文件在父子關係中的角色（`"product"`），指定它們屬於 ID 為 `1` 的品牌：

```json
PUT testindex1/_doc/3?routing=1
{
  "name": "Product 1",
  "product_to_brand": {
    "name": "product", 
    "parent": "1" 
  }
}
```
{% include copy-curl.html %}

```json
PUT testindex1/_doc/4?routing=1
{
  "name": "Product 2",
  "product_to_brand": {
    "name": "product",
    "parent": "1"
  }
}
```
{% include copy-curl.html %}

完成此步驟後，索引會包含三個具有此結構的文件。

| 文件 ID | 文件類型 | `name` 欄位 | `product_to_brand` 欄位 |
|-------------|---------------|--------------|--------------------------|
| 1 | 父文件（品牌） | "Brand 1" | `{"name": "brand"}` |
| 3 | 子文件（產品） | "Product 1" | `{"name": "product", "parent": "1"}` |
| 4 | 子文件（產品） | "Product 2" | `{"name": "product", "parent": "1"}` |


## 查詢 join 欄位

當您查詢 join 欄位時，回應會包含子欄位，指出傳回的文件是父文件還是子文件。對於子物件，也會傳回父文件 ID。

### 搜尋所有文件

```json
GET testindex1/_search
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

回應會指出文件是父文件還是子文件：

```json
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "name" : "Brand 1",
          "product_to_brand" : {
            "name" : "brand"
          }
        }
      },
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0,
        "_routing" : "1",
        "_source" : {
          "name" : "Product 1",
          "product_to_brand" : {
            "name" : "product",
            "parent" : "1"
          }
        }
      },
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "4",
        "_score" : 1.0,
        "_routing" : "1",
        "_source" : {
          "name" : "Product 2",
          "product_to_brand" : {
            "name" : "product",
            "parent" : "1"
          }
        }
      }
    ]
  }
}
```

### 搜尋父文件的所有子文件 

尋找與 Brand 1 相關聯的所有產品：

```json
GET testindex1/_search
{
  "query" : {
    "has_parent": {
      "parent_type":"brand",
      "query": {
        "match" : {
          "name": "Brand 1"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含與 Brand 1 相關聯的 Product 1 和 Product 2：

```json
{
  "took" : 7,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0,
        "_routing" : "1",
        "_source" : {
          "name" : "Product 1",
          "product_to_brand" : {
            "name" : "product",
            "parent" : "1"
          }
        }
      },
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "4",
        "_score" : 1.0,
        "_routing" : "1",
        "_source" : {
          "name" : "Product 2",
          "product_to_brand" : {
            "name" : "product",
            "parent" : "1"
          }
        }
      }
    ]
  }
}
```

### 搜尋子文件的父文件

尋找 Product 1 的父文件：

```json
GET testindex1/_search
{
  "query" : {
    "has_child": {
      "type":"product",
      "query": {
        "match" : {
            "name": "Product 1"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會傳回 Brand 1，作為 Product 1 的父文件：

```json
{
  "took" : 4,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "testindex1",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "name" : "Brand 1",
          "product_to_brand" : {
            "name" : "brand"
          }
        }
      }
    ]
  }
}
```

## 具有多個子文件的父文件

一個父文件可以有多個子文件。建立具有多個子類型的對應：

```json
PUT testindex1
{
  "mappings": {
    "properties": {
      "parent_to_child": {
        "type": "join",
        "relations": {
          "parent": ["child 1", "child 2"]  
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## Join 欄位類型注意事項

- 一個索引中只能有一個 join 欄位對應。
- 擷取、更新或刪除子文件時，您需要提供 routing 參數。這是因為同一關係中的父文件與子文件必須在同一個分片上編製索引。
- 不支援多個父文件。
- 只有在現有文件已標記為父文件時，您才能將子文件新增至該現有文件。
- 您可以將新關係新增至現有的 join 欄位。

## 後續步驟

- 瞭解 join 欄位的[聯結查詢]({{site.url}}{{site.baseurl}}/query-dsl/joining/)。
- 深入瞭解[擷取內部命中結果]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/inner-hits/)。