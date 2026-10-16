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

查詢索引中特定的 IP 位址：

```json
GET testindex/_search
{
  "query": {
    "term": {
      "ip_address": "10.24.34.0"
    }
  }
}
```
{% include copy-curl.html %}

## 搜尋 IP 位址及其相關的網路遮罩

您可以使用[無類別網域間路由 (CIDR) 表示法](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation)在索引中查詢 IP 位址。使用 CIDR 表示法時，請指定 IP 位址和前置長度，並以 `/` 分隔。IPv4 位址的前置長度必須介於 0 到 32 之間，IPv6 位址的前置長度則必須介於 0 到 128 之間。例如，前置長度為 24 時，會比對所有前 24 個位元相同的 IP 位址。

### IPv4 格式的查詢範例

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

### IPv6 格式的查詢範例

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

如果您在 `query_string` 查詢中使用 IPv6 格式的 IP 位址，則需要將 `:` 字元逸出，因為這些字元會被剖析為特殊字元。您可以用引號括住 IP 位址，並使用 `\` 將這些引號逸出，以達成此目的。

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

下表列出 `ip` 欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`boost` | 一個浮點數值，指定此欄位對相關性分數的權重。高於 1.0 的值會提高該欄位的相關性；介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。可動態更新。如需更多資訊，請參閱[權重提升]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/boost/)。
`doc_values` | 一個布林值，指定是否應將該欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `true`。如需更多資訊，請參閱[文件值]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/doc-values/)。
`ignore_malformed` | 一個布林值，指定是否忽略格式錯誤的值而不擲回例外狀況。預設為 `false`。可動態更新。如需更多資訊，請參閱[忽略格式錯誤的值]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/ignore-malformed/)。
`index` | 一個布林值，指定該欄位是否可搜尋。預設為 `true`。對於使用可插拔資料格式的索引，預設為 `false`，且不支援 `true`。如需更多資訊，請參閱[使用可插拔資料格式的索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/#pluggable-data-format-indexes)。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須是 IPv4 或 IPv6 位址。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為遺失。預設為 `null`。
`store` | 一個布林值，指定是否應儲存欄位值，並可從 `_source` 欄位個別擷取。預設為 `false`。如需更多資訊，請參閱[儲存]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/store/)。

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
