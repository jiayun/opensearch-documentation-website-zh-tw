---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常用 API"
nav_order: 170
redirect_from:
  - /opensearch/popular-api/
---

# 常用 API
**1.0 版推出**
{: .label .label-purple }

本頁包含常用 OpenSearch 操作的請求範例。


---

#### 目錄
1. TOC
{:toc}


---

## 使用非預設設定建立索引

```json
PUT my-logs
{
  "settings": {
    "number_of_shards": 4,
    "number_of_replicas": 2
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "year": {
        "type": "integer"
      }
    }
  }
}
```


## 使用隨機 ID 將文件編製索引

```json
POST my-logs/_doc
{
  "title": "Your Name",
  "year": "2016"
}
```


## 使用指定 ID 將文件編製索引

```json
PUT my-logs/_doc/1
{
  "title": "Weathering with You",
  "year": "2019"
}
```


## 一次將多份文件編製索引

請求本文結尾的空白行為必要項目。如果您省略 `_id` 欄位，OpenSearch 會產生隨機 ID。

```json
POST _bulk
{ "index": { "_index": "my-logs", "_id": "2" } }
{ "title": "The Garden of Words", "year": 2013 }
{ "index" : { "_index": "my-logs", "_id" : "3" } }
{ "title": "5 Centimeters Per Second", "year": 2007 }

```


## 列出所有索引

```
GET _cat/indices?v&expand_wildcards=all
```


## 開啟或關閉符合模式的所有索引

```
POST my-logs*/_open
POST my-logs*/_close
```


## 刪除符合模式的所有索引

```
DELETE my-logs*
```


## 建立索引別名

此請求會為索引 `my-logs-2019-11-13` 建立別名 `my-logs-today`。

```
PUT my-logs-2019-11-13/_alias/my-logs-today
```


## 列出所有別名

```
GET _cat/aliases?v
```


## 搜尋一個索引或符合模式的所有索引

```
GET my-logs/_search?q=test
GET my-logs*/_search?q=test
```


## 取得叢集設定（包含預設值）

```
GET _cluster/settings?include_defaults=true
```


## 變更磁碟水位線（或其他叢集設定）

```json
PUT _cluster/settings
{
  "transient": {
    "cluster.routing.allocation.disk.watermark.low": "80%",
    "cluster.routing.allocation.disk.watermark.high": "85%"
  }
}
```


## 取得叢集健康狀態

```
GET _cluster/health
```


## 列出叢集中的節點

```
GET _cat/nodes?v
```


## 取得節點統計資料

```
GET _nodes/stats
```


## 取得儲存庫中的快照

```
GET _snapshot/my-repository/_all
```


## 建立快照

```
PUT _snapshot/my-repository/my-snapshot
```


## 還原快照

```json
POST _snapshot/my-repository/my-snapshot/_restore
{
  "indices": "-.opendistro_security",
  "include_global_state": false
}
```
