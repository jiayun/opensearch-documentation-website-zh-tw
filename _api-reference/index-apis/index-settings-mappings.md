---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引設定與對應"
parent: Index APIs
nav_order: 40
has_children: true
has_toc: false
---

# 索引設定與對應

索引設定與對應 API 可讓您設定及修改索引的行為與結構。這些 API 可控制索引層級的設定與欄位對應，決定資料的儲存與編製索引方式。

## 可用的 API

OpenSearch 支援下列索引設定與對應 API。

| API | 說明 |
|-----|-------------|
| [Get settings]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-settings/) | 傳回一或多個索引的設定資訊。 |
| [Update settings]({{site.url}}{{site.baseurl}}/api-reference/index-apis/update-settings/) | 更新一或多個索引的設定。 |
| [Put mapping]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/) | 新增欄位或更新現有的欄位對應。 |