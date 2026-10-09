---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複製到"
parent: Mapping parameters
redirect_from:
  - /field-types/mapping-parameters/copy-to/
nav_order: 20
has_children: false
has_toc: false
---

# copy_to 對應參數

`copy_to` 參數可讓您將多個欄位的值複製到一個群組欄位中，之後即可將該群組欄位當作單一欄位進行查詢。當您經常跨多個欄位搜尋並希望簡化查詢時，這個功能非常實用。

請注意以下重要事項：

- 複製時，複製的是原始欄位值（而非分析過程中產生的詞元）。

- 原始的 `_source` 欄位不會因複製的值而有所修改。

- 使用 `"copy_to": ["field_1", "field_2"]` 語法可將同一個值複製到多個欄位。

- 您無法透過中繼欄位進行遞迴複製。例如，若將 `field_1` 複製到 `field_2`，並將 `field_2` 複製到 `field_3`，則對 `field_1` 編製索引並不會使值出現在 `field_3` 中。請改為直接從來源欄位使用 `copy_to` 複製到多個目標欄位。

## 範例

下列範例示範如何使用 `copy_to` 參數。

### copy_to 的基本用法

建立一個索引，將名字與姓氏複製到 `full_name` 欄位：

```json
PUT /user_profiles
{
  "mappings": {
    "properties": {
      "first_name": {
        "type": "text",
        "copy_to": "full_name"
      },
      "last_name": {
        "type": "text",
        "copy_to": "full_name"
      },
      "full_name": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有獨立姓名欄位的文件編製索引：

```json
PUT /user_profiles/_doc/1
{
  "first_name": "Jane",
  "last_name": "Doe"
}
```
{% include copy-curl.html %}

`first_name` 與 `last_name` 欄位仍可個別查詢，但 `full_name` 欄位可讓您同時搜尋兩個姓名。若要使用合併欄位進行搜尋，請傳送下列請求。`and` 運算子要求兩個詞都必須符合：

```json
GET /user_profiles/_search
{
  "query": {
    "match": {
      "full_name": {
        "query": "Jane Doe",
        "operator": "and"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

```json
{
  "took": 7,
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
    "max_score": 0.26152915,
    "hits": [
      {
        "_index": "user_profiles",
        "_id": "1",
        "_score": 0.26152915,
        "_source": {
          "first_name": "Jane",
          "last_name": "Doe"
        }
      }
    ]
  }
}
```

### 複製到多個目標欄位

若要將欄位內容複製到多個目標欄位，請建立一個索引，將 `title` 欄位同時複製到 `searchable_content` 與 `display_text` 欄位。`body` 欄位則僅複製到 `searchable_content`：

```json
PUT /content_library
{
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "copy_to": ["searchable_content", "display_text"]
      },
      "body": {
        "type": "text",
        "copy_to": "searchable_content"
      },
      "searchable_content": {
        "type": "text"
      },
      "display_text": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有 `title` 與 `body` 欄位的文件編製索引：

```json
PUT /content_library/_doc/1
{
  "title": "OpenSearch Documentation Guide",
  "body": "This comprehensive guide covers mapping parameters and their usage in OpenSearch."
}
```
{% include copy-curl.html %}

您可以使用 `searchable_content` 欄位搜尋標題與內文：

```json
GET /content_library/_search
{
  "query": {
    "match": {
      "searchable_content": "OpenSearch mapping parameters"
    }
  }
}
```
{% include copy-curl.html %}

回應包含符合的文件。該文件原始的 `_source` 欄位仍只包含 `title` 與 `body` 欄位：

```json
{
  "took": 21,
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
    "max_score": 0.44133043,
    "hits": [
      {
        "_index": "content_library",
        "_id": "1",
        "_score": 0.44133043,
        "_source": {
          "title": "OpenSearch Documentation Guide",
          "body": "This comprehensive guide covers mapping parameters and their usage in OpenSearch."
        }
      }
    ]
  }
}
```