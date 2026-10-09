---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/index-parameter/
nav_order: 150
has_children: false
has_toc: false
---

# Index 對應參數

`index` 對應參數可控制欄位是否納入反向索引。設為 `true` 時，該欄位會編製索引並可供查詢。設為 `false` 時，該欄位會儲存在文件中但不編製索引，因此在未啟用 [`doc_values`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/) 時無法搜尋。如果您不需要搜尋特定欄位，停用該欄位的索引與 `doc_values` 可縮小索引大小並提升索引效能。例如，您可以對僅供顯示的大型文字欄位或中繼資料停用索引。

根據預設，所有欄位類型都會編製索引。對於使用可插拔資料格式的索引，若欄位類型的值儲存在 doc values 中，`index` 會預設為 `false`。如需詳細資訊，請參閱[可插拔資料格式索引](#pluggable-data-format-indexes)。

##  index 與 doc values 參數比較

啟用 `index` 參數時，OpenSearch 會建立詞彙與包含這些詞彙之文件的對應。對於每份新文件，已編製索引欄位的值會拆解為詞彙，而每個詞彙都會在對應中連結至文件 ID。

啟用 `doc_values` 參數時，OpenSearch 會建立反向對應：每份文件都會連結至在該欄位中找到的詞彙清單。這對於排序等作業很有用，因為系統需要快速存取文件的欄位值。

下表說明 `index` 與 `doc_values` 不同組合下的欄位行為。

| `index` 參數值 | `doc_values` 參數值 | 行為       | 使用案例       
| :--       | :--               | :--            | :--            |
| `true`   | `true`          | 該欄位可搜尋，並支援排序、指令碼與彙總。    | 適用於您想直接查詢並執行複雜作業的任何欄位。          |
| `true`   | `false`          | 該欄位可搜尋，但不支援文件對詞彙的查閱 (因此排序、指令碼與彙總會耗時較久)。 |  適用於您想查詢但不需要用於排序或彙總的欄位，例如 `text` 欄位。          |
| `false`   | `true`         | 該欄位可搜尋 (雖然效率較低)，並支援排序、指令碼與彙總。請注意，並非所有欄位類型都支援 `doc_values` (例如 `text` 欄位不支援 `doc_values`)。     | 適用於您想彙總但不想篩選或查詢的欄位。          |
| `false`  | `false`          | 該欄位無法搜尋。嘗試搜尋該欄位的查詢會傳回錯誤。    | 適用於您不想對其執行任何作業的欄位，例如中繼資料欄位。          |

## 支援的資料類型

`index` 對應參數可套用於下列資料類型：

- [文字]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/)
- [關鍵字]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/)
- [布林值]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/boolean/)
- [IP 位址]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/ip/)
- [日期欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/dates/)
- [數值欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)

## 在欄位上啟用索引

下列請求會建立名為 `products` 的索引，其中包含已編製索引的 `description` 與 `name` 欄位 (預設行為)：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text"
      },
      "name": {
        "type": "keyword"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求將文件編製索引：

```json
PUT /products/_doc/1
{
  "description": "This product has a searchable description.",
  "name": "doc1"
}
```
{% include copy-curl.html %}

查詢 description 欄位：

```json
POST /products/_search
{
  "query": {
    "match": {
      "description": "searchable"
    }
  }
}
```
{% include copy-curl.html %}

下列回應確認已編製索引的文件成功符合查詢：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 0.13076457,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 0.13076457,
        "_source": {
          "description": "This product has a searchable description.",
          "name": "doc1"
        }
      }
    ]
  }
}
```

## 在欄位上停用索引

建立名為 `products-no-index` 的索引，其中包含未編製索引的 `description` 欄位與 `name` 欄位：

```json
PUT /products-no-index
{
  "mappings": {
    "properties": {
      "description": {
        "type": "text",
        "index": false
      },
      "name": {
        "type": "keyword",
        "index": false
      }
    }
  }
}
```
{% include copy-curl.html %}

使用下列請求將文件編製索引：

```json
PUT /products-no-index/_doc/1
{
  "description": "This product has a non-searchable description.",
  "name": "doc1"
}
```
{% include copy-curl.html %}

使用 `description` 欄位查詢 `products-no-index`：

```json
POST /products-no-index/_search
{
  "query": {
    "match": {
      "description": "non-searchable"
    }
  }
}
```
{% include copy-curl.html %}

下列錯誤回應指出搜尋查詢失敗，因為 description 欄位未編製索引：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "query_shard_exception",
        "reason": "failed to create query: Cannot search on field [description] since it is not indexed.",
        "index": "products-no-index",
        "index_uuid": "yX2F4En1RqOBbf3YWihGCQ"
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "products-no-index",
        "node": "0tmy2tf7TKW8qCmya9sG2g",
        "reason": {
          "type": "query_shard_exception",
          "reason": "failed to create query: Cannot search on field [description] since it is not indexed.",
          "index": "products-no-index",
          "index_uuid": "yX2F4En1RqOBbf3YWihGCQ",
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "Cannot search on field [description] since it is not indexed."
          }
        }
      }
    ]
  },
  "status": 400
}
```

對於 `text` 欄位，將 `index` 參數設為 `false` 會停用該欄位的搜尋，因為 `text` 欄位不支援 `doc_values`。若要讓其他欄位無法搜尋，您必須另外將 `doc_values` 設為 `false`。  

使用 `name` 欄位查詢 `products-no-index`：

```json
POST /products-no-index/_search
{
  "query": {
    "term": {
      "name": {
        "value": "doc1"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列回應確認搜尋查詢成功，因為 `name` 欄位雖然未編製索引，但已啟用 `doc_values`：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "products-no-index",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "description": "This product has a non-searchable description.",
          "name": "doc1"
        }
      }
    ]
  }
}
```

## 可插拔資料格式索引
**3.9 版引入**
{: .label .label-purple }

這是實驗性功能，不建議在生產環境中使用。如需此功能進展的最新資訊，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。    
{: .warning}

對於使用可插拔資料格式的索引，下列類型的欄位預設不會編製索引：

- 數值類型，包括 `scaled_float`
- `date`
- `date_nanos`
- `ip`
- `boolean`

這些類型的欄位仍可搜尋，因為 OpenSearch 會從 doc values 提供對它們的 `range`、`term` 與 `terms` 查詢。所有其他類型的欄位則預設會編製索引。如需啟用與停用實驗性功能的相關資訊，請參閱[啟用實驗性功能]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/experimental/)。

不支援為這些欄位將 `index` 設為 `true`。

由於預設值不會儲存在對應中，`index` 參數不會出現在這些欄位的 `GET _mapping` 請求回應中，且 Field Capabilities API 會將它們回報為 `"searchable": false`。
