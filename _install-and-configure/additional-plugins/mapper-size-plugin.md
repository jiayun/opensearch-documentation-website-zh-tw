---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Mapper-size 外掛程式"
parent: Additional plugins
grand_parent: Managing OpenSearch plugins
nav_order: 25

---

# Mapper-size 外掛程式

`mapper-size` 外掛程式可讓您在 OpenSearch 索引中使用 `_size` 欄位。`_size` 欄位會儲存每份文件的大小（以位元組為單位）。

## 安裝外掛程式

您可以使用下列命令安裝 `mapper-size` 外掛程式：

```sh
./bin/opensearch-plugin install mapper-size
```

## 範例

啟動叢集後，您可以建立啟用大小對應的索引、將文件編製索引，以及搜尋文件，如下列範例所示。

### 建立啟用大小對應的索引

```sh
curl -XPUT example-index -H "Content-Type: application/json" -d '{
  "mappings": {
    "_size": {
      "enabled": true
    },
    "properties": {
      "name": {
        "type": "text"
      },
      "age": {
        "type": "integer"
      }
    }
  }
}'
```

### 將文件編製索引

```sh
curl -XPOST example-index/_doc -H "Content-Type: application/json" -d '{
  "name": "John Doe",
  "age": 30
}'
```

### 查詢索引

```sh
curl -XGET example-index/_search -H "Content-Type: application/json" -d '{
  "query": {
    "match_all": {}
  },
  "stored_fields": ["_size", "_source"]
}'
```

### 查詢結果

在下列範例中，查詢結果包含 `_size` 欄位，並顯示已編製索引之文件的大小（以位元組為單位）：

```json
{
  "took": 2,
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
        "_index": "example_index",
        "_id": "Pctw0I8BLto8I5f_NLKK",
        "_score": 1.0,
        "_size": 37,
        "_source": {
          "name": "John Doe",
          "age": 30
        }
      }
    ]
  }
}
```

