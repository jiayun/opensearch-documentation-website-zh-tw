---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料串流 API"
nav_order: 40
has_children: true
has_toc: false
redirect_from:
  - /api-reference/data-stream/
---

# 資料串流 API

使用資料串流 API 建立及刪除[資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)、修改其後端索引，以及擷取其相關資訊與統計資料。

## 可用的 API

OpenSearch 支援下列資料串流 API。

| API | 說明 |
|-----|-------------|
| [建立資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/create-data-stream/) | 建立資料串流。 |
| [取得資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-info/) | 傳回一個或多個資料串流的相關資訊。 |
| [取得資料串流統計資料]({{site.url}}{{site.baseurl}}/api-reference/data-stream/data-stream-stats/) | 傳回一個或多個資料串流的統計資料。 |
| [修改資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/modify-data-stream/) | 新增或移除資料串流的後端索引。 |
| [刪除資料串流]({{site.url}}{{site.baseurl}}/api-reference/data-stream/delete-data-stream/) | 刪除資料串流及其後端索引。 |

## 相關文件

- 如需資料串流的詳細資訊，包括何時使用資料串流，請參閱[資料串流]({{site.url}}{{site.baseurl}}/im-plugin/data-streams/)。
