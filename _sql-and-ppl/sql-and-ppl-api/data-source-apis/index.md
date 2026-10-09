---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料來源 API"
nav_order: 1
has_children: true
parent: SQL and PPL API
has_toc: false
redirect_from:
  - /sql-and-ppl/sql-and-ppl-api/data-source-apis/
  - /sql-and-ppl/ppl/admin/datasources/
---

# 資料來源 API

這是實驗性功能，不建議在正式環境中使用。如需此功能的進度更新，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。    
{: .warning}

OpenSearch 支援使用 SQL 外掛程式查詢外部的非 OpenSearch 資料來源，例如 Prometheus。Direct Query API 可讓您使用這些資料來源的原生查詢語言（例如 Prometheus 的 PromQL）直接查詢它們。

支援下列資料來源 API：

- [執行直接查詢]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-and-ppl-api/data-source-apis/execute-direct-query/)
- [讀取資源]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-and-ppl-api/data-source-apis/read-resources/)
- [寫入資源]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-and-ppl-api/data-source-apis/write-resources/)