---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: SQL
nav_order: 4
has_children: true
has_toc: false
redirect_from:
  - /sql-and-ppl/sql/
  - /search-plugins/sql/sql/
  - /search-plugins/sql/sql/index/
---

# SQL

OpenSearch 中的 SQL 銜接了傳統關聯式資料庫概念與 OpenSearch 文件導向資料儲存之間的落差。這項整合讓您能夠運用 SQL 知識，查詢、分析並從 OpenSearch 資料中萃取洞察。

## SQL 與 OpenSearch 術語

以下是核心 SQL 概念對應至 OpenSearch 的方式：

SQL | OpenSearch
:--- | :---
資料表 | 索引
資料列 | 文件
資料行 | 欄位

## REST API

如需 SQL 外掛程式的完整 REST API 參考，請參閱 [SQL/PPL API]({{site.url}}{{site.baseurl}}/search-plugins/sql/sql-ppl-api/)。

若要將 SQL 外掛程式與您自己的應用程式搭配使用，請將請求傳送至 `_plugins/_sql` 端點：

```json
POST _plugins/_sql
{
  "query": "SELECT * FROM my-index LIMIT 50"
}
```
{% include copy-curl.html %}

您可以使用以逗號分隔的清單來查詢多個索引：

```json
POST _plugins/_sql
{
  "query": "SELECT * FROM my-index1,myindex2,myindex3 LIMIT 50"
}
```
{% include copy-curl.html %}

您可以使用萬用字元運算式指定索引模式：

```json
POST _plugins/_sql
{
  "query": "SELECT * FROM my-index* LIMIT 50"
}
```
{% include copy-curl.html %}

若要在命令列中執行上述查詢，請使用 [cURL](https://curl.haxx.se/) 命令：

```bash
curl -XPOST https://localhost:9200/_plugins/_sql -u 'admin:<custom-admin-password>' -k -H 'Content-Type: application/json' -d '{"query": "SELECT * FROM my-index* LIMIT 50"}'
```
{% include copy.html %}


您可以將[回應格式]({{site.url}}{{site.baseurl}}/search-plugins/sql/response-formats/)指定為 JDBC、標準 OpenSearch JSON、CSV 或 raw。根據預設，查詢會以 JDBC 格式傳回資料。下列查詢會將格式設為 JSON：

```json
POST _plugins/_sql?format=json
{
  "query": "SELECT * FROM my-index LIMIT 50"
}
```
{% include copy-curl.html %}

如需請求參數、設定、支援的操作及工具的詳細資訊，請參閱 [SQL]({{site.url}}{{site.baseurl}}/search-plugins/sql/sql/index/) 下的相關主題。
