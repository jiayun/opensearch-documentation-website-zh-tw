---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "IP 範圍"
parent: Bucket aggregations
nav_order: 110
redirect_from:
  - /query-dsl/aggregations/bucket/ip-range/
---

# IP 範圍彙總

`ip_range` 彙總會根據 IP 位址範圍將文件分組到桶 (bucket) 中。它適用於對應為 `ip` 類型的欄位，並支援明確的 `from`/`to` 邊界，以及使用 `mask` 參數的 [CIDR](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing) 表示法。

## 參數

`ip_range` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | 字串 | 要進行彙總的 `ip` 欄位。 |
| `ranges` | 必要 | 陣列 | IP 範圍清單。每個範圍可以指定 `from` 和/或 `to`（明確邊界），或指定 `mask`（CIDR 表示法）。您可以選擇性地加入 `key` 來為桶命名。 |
| `keyed` | 選用 | 布林值 | 若為 `true`，則以範圍名稱作為鍵的物件傳回桶，而非陣列。預設值為 `false`。 |

## 範例設定

若要試用本頁的範例，請建立包含 `ip` 欄位的索引：

```json
PUT /network_logs
{
  "mappings": {
    "properties": {
      "ip": { "type": "ip" },
      "status": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將一些文件編製索引：

```json
POST /network_logs/_bulk?refresh=true
{"index":{}}
{"ip": "10.0.0.1", "status": "ok"}
{"index":{}}
{"ip": "10.0.0.50", "status": "ok"}
{"index":{}}
{"ip": "10.0.0.100", "status": "error"}
{"index":{}}
{"ip": "10.0.0.200", "status": "ok"}
{"index":{}}
{"ip": "10.0.1.5", "status": "ok"}
{"index":{}}
{"ip": "10.0.1.100", "status": "error"}
{"index":{}}
{"ip": "172.16.0.1", "status": "ok"}
{"index":{}}
{"ip": "172.16.0.50", "status": "ok"}
{"index":{}}
{"ip": "192.168.1.1", "status": "ok"}
{"index":{}}
{"ip": "192.168.1.100", "status": "error"}
```
{% include copy-curl.html %}

## 範例：明確的 IP 範圍

下列範例使用 `from` 和 `to` 邊界，將網路記錄檔項目分割為三個 IP 範圍：

```json
GET /network_logs/_search
{
  "size": 0,
  "aggs": {
    "ip_ranges": {
      "ip_range": {
        "field": "ip",
        "ranges": [
          { "to": "10.0.1.0" },
          { "from": "10.0.1.0", "to": "172.16.0.0" },
          { "from": "172.16.0.0" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

桶會以陣列形式傳回，並根據範圍邊界自動產生鍵。`from` 值包含在範圍內，而 `to` 值不包含在範圍內：

```json
{
  ...
  "aggregations": {
    "ip_ranges": {
      "buckets": [
        {
          "key": "*-10.0.1.0",
          "to": "10.0.1.0",
          "doc_count": 4
        },
        {
          "key": "10.0.1.0-172.16.0.0",
          "from": "10.0.1.0",
          "to": "172.16.0.0",
          "doc_count": 2
        },
        {
          "key": "172.16.0.0-*",
          "from": "172.16.0.0",
          "doc_count": 4
        }
      ]
    }
  }
}
```

## 範例：使用 CIDR 遮罩並傳回具鍵回應

您可以使用 CIDR 表示法定義範圍，並指派自訂鍵。將 `keyed` 設定為 `true` 會傳回物件而非陣列。下列範例依 RFC 1918 私人位址類別將流量分組：

```json
GET /network_logs/_search
{
  "size": 0,
  "aggs": {
    "ip_ranges": {
      "ip_range": {
        "field": "ip",
        "ranges": [
          { "key": "private_a", "mask": "10.0.0.0/8" },
          { "key": "private_b", "mask": "172.16.0.0/12" },
          { "key": "private_c", "mask": "192.168.0.0/16" }
        ],
        "keyed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

使用 CIDR 表示法時，回應會包含根據遮罩計算出的 `from` 和 `to` 邊界。由於 `keyed` 為 `true`，桶會以具有自訂鍵的物件形式傳回，而非陣列：

```json
{
  ...
  "aggregations": {
    "ip_ranges": {
      "buckets": {
        "private_a": {
          "from": "10.0.0.0",
          "to": "11.0.0.0",
          "doc_count": 6
        },
        "private_b": {
          "from": "172.16.0.0",
          "to": "172.32.0.0",
          "doc_count": 2
        },
        "private_c": {
          "from": "192.168.0.0",
          "to": "192.169.0.0",
          "doc_count": 2
        }
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `buckets` | 陣列或物件 | IP 範圍桶。預設以陣列形式傳回；當 `keyed` 為 `true` 時，則以物件形式傳回。 |
| `buckets.key` | 字串 | 自動產生的範圍標籤（例如 `*-10.0.1.0` 或 `10.0.0.0/24`），若有指定則為自訂鍵。 |
| `buckets.from` | 字串 | 範圍的下限 IP 位址（包含）。 |
| `buckets.to` | 字串 | 範圍的上限 IP 位址（不包含）。 |
| `buckets.doc_count` | 整數 | IP 位址位於此範圍內的文件數量。 |
