---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "IP 位址"
nav_order: 55
has_children: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/ip/
  - /opensearch/supported-field-types/ip/
  - /field-types/ip/
---

# IP 位址欄位類型
**於 1.0 版推出**
{: .label .label-purple }

`ip` 欄位類型包含 IPv4 或 IPv6 格式的 IP 位址。

若要表示 IP 位址範圍，另有 IP [範圍欄位類型]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/range/)。
{: .note }

## 範例

建立含有 IP 位址的對應：

```json
PUT testindex 
{
  "mappings" : {
    "properties" :  {
      "ip_address" : {
        "type" : "ip"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有 IP 位址的文件編製索引：

```json
PUT testindex/_doc/1 
{
  "ip_address" : "10.24.34.0"
}
```
{% include copy-curl.html %}

查詢索引中的特定 IP 位址：

```json
GET testindex/_doc/1 
{
  "query": {
    "term": {
      "ip_address": "10.24.34.0"
    }
  }
}
```
{% include copy-curl.html %}

## 搜尋 IP 位址及其相關聯的網路遮罩

您可以使用 [Classless Inter-Domain Routing (CIDR) 標記法](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation) 查詢索引中的 IP 位址。使用 CIDR 標記法時，請指定 IP 位址與前置長度 (0–32)，兩者以 `/` 分隔。例如，前置長度 24 會比對開頭 24 位元相同的所有 IP 位址。

#### IPv4 格式的範例查詢

```json
GET testindex/_search 
{
  "query": {
    "term": {
      "ip_address": "10.24.34.0/24"
    }
  }
}
```
{% include copy-curl.html %}

#### IPv6 格式的範例查詢

```json
GET testindex/_search 
{
  "query": {
    "term": {
      "ip_address": "2001:DB8::/24"
    }
  }
}
```
{% include copy-curl.html %}

如果您在 `query_string` 查詢中使用 IPv6 格式的 IP 位址，必須逸出 `:` 字元，因為這些字元會被剖析為特殊字元。您可以將 IP 位址以引號括住，並使用 `\` 逸出這些引號。

```json
GET testindex/_search 
{
  "query" : {
    "query_string": {
      "query": "ip_address:\"2001:DB8::/24\""
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出 `ip` 欄位類型可接受的參數。所有參數皆為選用。

參數 | 說明
:--- | :---
`boost` | 浮點值，用於指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 與 1.0 之間的值會降低欄位的相關性。預設值為 1.0。可動態更新。
`doc_values` | 布林值，用於指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設值為 `true`。
`ignore_malformed` | 布林值，用於指定是否忽略格式錯誤的值而不擲回例外狀況。預設值為 `false`。可動態更新。
`index` | 布林值，用於指定欄位是否可供搜尋。預設值為 `true`。對於使用可插式資料格式的索引，預設值為 `false`，且不支援 `true`。如需詳細資訊，請參閱[可插式資料格式索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/#pluggable-data-format-indexes)。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用於取代 `null` 的值。其類型必須與欄位相同。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為缺少。預設值為 `null`。
`store` | 布林值，用於指定是否應儲存欄位值，並可與 `_source` 欄位分開擷取。預設值為 `false`。

## 衍生的來源

當索引使用[衍生的來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source)時，OpenSearch 在重建來源期間可能會排序 IP 位址值，並移除多重值 IP 欄位中的重複項目。

建立可啟用衍生的來源並設定 `ip` 欄位的索引：

```json
PUT sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "ip": {
        "type": "ip"
      }
    }
  }
}
```

將含有多個 IP 位址 (包括重複項目) 的文件編製索引至該索引：

```json
PUT sample-index1/_doc/1
{
  "ip": ["10.16.0.1", "192.168.0.1", "10.16.0.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 會移除重複項目並排序值：

```json
{
  "ip": ["10.16.0.1", "192.168.0.1", "2001:0db8:85a3:0000:0000:8a2e:0370:7334"]
}
```
