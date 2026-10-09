---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "IP 位址函式"
parent: Functions
grand_parent: PPL
nav_order: 8
---

# IP 位址函式

PPL 支援下列 IP 位址函式。

## CIDRMATCH

**用法**：`CIDRMATCH(ip, cidr)`

檢查 IP 位址是否位於指定的 CIDR 範圍內。

**參數**：

- `ip` (必要)：要檢查的 IP 位址，以字串或 IP 值表示。同時支援 IPv4 與 IPv6。
- `cidr` (必要)：要比對的 CIDR 範圍，以字串表示。同時支援 IPv4 與 IPv6 區塊。

**回傳類型**：`BOOLEAN`

### 範例
  
```sql
source=weblogs
| where cidrmatch(host, '1.2.3.0/24')
| fields host, url
```
{% include copy.html %}
  
查詢會傳回下列結果：
  
<!-- vale off -->

| host | url |
| --- | --- |
| 1.2.3.4 | /history/voyager1/ |
| 1.2.3.5 | /history/voyager2/ |

<!-- vale on -->

## GEOIP

**用法**：`GEOIP(dataSourceName, ipAddress[, options])`

使用 OpenSearch Geospatial 外掛程式 API 擷取 IP 位址的位置資訊。

**參數**：

- `dataSourceName` (必要)：OpenSearch Geospatial 外掛程式上已建立之資料來源的名稱。組態詳細資訊請參閱 [IP2Geo 處理器文件]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/ip2geo/)。
- `ipAddress` (必要)：要查詢的 IP 位址，以字串或 IP 值表示。同時支援 IPv4 與 IPv6。
- `options` (選用)：以逗號分隔的輸出欄位字串。可用欄位取決於資料來源供應商的結構描述。例如，`geolite2-city` 資料集包含 `country_iso_code`、`country_name`、`continent_name`、`region_iso_code`、`region_name`、`city_name`、`time_zone` 與 `location` 等欄位。

**回傳類型**：`OBJECT`

### 範例
  
```sql
source=weblogs
| eval LookupResult = geoip("dataSourceName", "50.68.18.229", "country_iso_code,city_name")
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| LookupResult |
| --- |
| {'city_name': 'Vancouver', 'country_iso_code': 'CA'} | <!-- vale on -->
