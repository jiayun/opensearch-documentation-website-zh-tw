---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Querqy
parent: Query rewriting
grand_parent: Optimizing search quality
has_children: false
redirect_from:
  - /search-plugins/querqy/
nav_order: 60
---

# Querqy

Querqy for OpenSearch 是一個社群外掛程式，用於查詢重寫，可提升搜尋相關性。它透過套用規則來提升、壓低、篩選及重新導向搜尋結果等能力，讓 OpenSearch 在比對與評分上更精確。

Querqy 支援 OpenSearch 2.19.2 及更早版本。
{: .warning }

如需更多資訊，請參閱 [Querqy 文件](https://docs.querqy.org/querqy/index.html)。


## 安裝 Querqy 外掛程式

Querqy 外掛程式現已適用於 OpenSearch 2.19.2。執行下列命令以安裝 Querqy 外掛程式：

````bash
./bin/opensearch-plugin install \
   "https://repo1.maven.org/maven2/org/querqy/opensearch-querqy/1.1.os2.19.2/opensearch-querqy-1.1.os2.19.2.zip"
````

安裝期間請在安全性提示中回答 `yes`，因為 Querqy 需要額外的權限才能載入查詢重寫器。


## 端點

```
POST /myindex/_search
```

## 範例查詢

````json
{
   "query": {
       "querqy": {
           "matching_query": {
               "query": "books"
           },
           "query_fields": [ "title^3.0", "words^2.1", "shortSummary"]
       }
   }
}
````
