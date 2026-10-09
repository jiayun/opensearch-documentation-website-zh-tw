---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Meta
parent: Metadata fields
nav_order: 50
redirect_from:
  - /field-types/metadata-fields/meta/
---

# Meta 中繼資料欄位

`_meta` 欄位是一種對應屬性，可讓您將自訂中繼資料附加到索引對應。您的應用程式可以使用這些中繼資料來儲存與使用情境相關的資訊，例如版本管理、擁有權、分類或稽核。

## 用法

您可以在建立新索引或更新現有索引的對應時定義 `_meta` 欄位，如下列範例請求所示：

```json
PUT my-index
{
  "mappings": {
    "_meta": {
      "application": "MyApp",
      "version": "1.2.3",
      "author": "John Doe"
    },
    "properties": {
      "title": {
        "type": "text"
      },
      "description": {
        "type": "text"
      }
    }
  }
}

```
{% include copy-curl.html %}

在此範例中，新增了三個自訂中繼資料欄位：`application`、`version` 和 `author`。您的應用程式可以使用這些欄位來儲存與索引相關的任何資訊，例如索引所屬的應用程式、應用程式版本或索引的作者。

您可以使用 [Put Mapping API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/) 操作來更新 `_meta` 欄位，如下列範例請求所示：

```json
PUT my-index/_mapping
{
  "_meta": {
    "application": "MyApp",
    "version": "1.3.0",
    "author": "Jane Smith"
  }
}
```
{% include copy-curl.html %}

## 擷取 `meta` 資訊

您可以使用 [Get Mapping API]({{site.url}}{{site.baseurl}}/mappings/#retrieving-mappings) 操作來擷取索引的 `_meta` 資訊，如下列範例請求所示：

```json
GET my-index/_mapping
```
{% include copy-curl.html %}

回應會傳回完整的索引對應，包括 `_meta` 欄位：

```json
{
  "my-index": {
    "mappings": {
      "_meta": {
        "application": "MyApp",
        "version": "1.3.0",
        "author": "Jane Smith"
      },
      "properties": {
        "description": {
          "type": "text"
        },
        "title": {
          "type": "text"
        }
      }
    }
  }
}
```
{% include copy-curl.html %}
