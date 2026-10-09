---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "路由"
parent: Metadata fields
nav_order: 60
redirect_from:
  - /field-types/metadata-fields/routing/
---

# 路由中繼資料欄位

OpenSearch 使用雜湊演算法將文件路由至索引中的特定分片。根據預設，系統會使用文件的 `_id` 欄位作為路由值，但您也可以為每份文件指定自訂的路由值。

## 預設路由

以下是 OpenSearch 的預設路由公式。`_routing` 值是文件的 `_id`。

```json
shard_num = hash(_routing) % num_primary_shards
```

## 自訂路由

您可以在將文件編製索引時指定自訂的路由值，如下列範例請求所示：

```json
PUT sample-index1/_doc/1?routing=JohnDoe1
{
  "title": "This is a document"
}
```
{% include copy-curl.html %}

在此範例中，文件是使用值 `JohnDoe1` 進行路由，而非預設的 `_id`。

在擷取、刪除或更新文件時，您必須提供相同的路由值，如下列範例請求所示：

```json
GET sample-index1/_doc/1?routing=JohnDoe1
```
{% include copy-curl.html %}

## 依路由查詢

您可以使用 `_routing` 欄位，依文件的路由值查詢文件，如下列範例所示。此查詢只會搜尋與 `JohnDoe1` 路由值相關聯的分片：

```json
GET sample-index1/_search
{
  "query": {
    "terms": {
      "_routing": [ "JohnDoe1" ]
    }
  }
}
```
{% include copy-curl.html %}

## 必要路由

您可以將自訂路由設為索引上所有 CRUD 作業的必要條件，如下列範例請求所示。如果您嘗試在未提供路由值的情況下將文件編製索引，OpenSearch 會擲回例外狀況。

```json
PUT sample-index2
{
  "mappings": {
    "_routing": {
      "required": true
    }
  }
}
```
{% include copy-curl.html %}

## 路由至特定分片

您可以設定索引，將自訂值路由至分片的子集，而非單一分片。這是在建立索引時設定 `index.routing_partition_size` 來完成。計算分片的公式為 `shard_num = (hash(_routing) + hash(_id)) % routing_partition_size) % num_primary_shards`。

下列範例請求會將文件路由至索引中四個分片的其中一個：

```json
PUT sample-index3
{
  "settings": {
    "index.routing_partition_size": 4
  },
  "mappings": {
    "_routing": {
      "required": true
    }
  }
}
```
{% include copy-curl.html %}
