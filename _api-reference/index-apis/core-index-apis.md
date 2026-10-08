---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "核心索引 API"
parent: Index APIs
nav_order: 20
has_children: true
has_toc: false
---

# 核心索引 API

核心索引 API 提供管理 OpenSearch 叢集中索引生命週期的基本操作。這些 API 可讓您建立、刪除索引，並對索引執行基本操作。

## 可用的 API

OpenSearch 支援下列核心索引 API。

| API | 說明 |
|-----|-------------|
| [Create index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index/) | 建立新的索引。 |
| [Delete index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index/) | 刪除現有的索引。 |
| [Get index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-index/) | 傳回一或多個索引的資訊。 |
| [Index exists]({{site.url}}{{site.baseurl}}/api-reference/index-apis/exists/) | 檢查索引是否存在。 |
| [Open index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/open-index/) | 開啟已關閉的索引。 |
| [Close index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/close-index/) | 關閉已開啟的索引。 |
| [Resolve index]({{site.url}}{{site.baseurl}}/api-reference/index-apis/resolve-index/) | 將索引名稱與別名解析為其具體索引。 |