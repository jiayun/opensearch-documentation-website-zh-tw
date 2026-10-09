---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引範本"
parent: Index APIs
nav_order: 50
has_children: true
has_toc: false
---

# 索引範本 API

索引範本 API 可讓您建立及管理範本，自動將設定、對應和別名套用至符合特定模式的新索引。範本是確保各索引之間一致性的強大方式。

## 可用的 API

OpenSearch 支援下列索引範本 API。

| API | 說明 |
|-----|-------------|
| [建立索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/create-index-template/) | 建立或更新索引範本。 |
| [刪除索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-index-template/) | 刪除索引範本。 |
| [取得索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-index-template/) | 傳回一或多個索引範本的相關資訊。 |
| [索引範本是否存在]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-template-exists/) | 檢查索引範本是否存在。 |
| [模擬索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/simulate-index-template/) | 模擬索引範本的套用。 |
| [元件範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/component-template/) | 管理可在多個索引範本之間重複使用的元件範本。 |

## 舊版範本 API

為了回溯相容性，OpenSearch 也支援下列舊版範本 API。這些 API 使用較舊的範本格式，且已被棄用，建議改用前述的索引範本 API。

| API | 說明 |
|-----|-------------|
| [Post 範本（舊版）]({{site.url}}{{site.baseurl}}/api-reference/index-apis/post-template-legacy/) | 使用 POST 建立或更新舊版索引範本。 |
| [Put 範本（舊版）]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-template-legacy/) | 使用 PUT 建立或更新舊版索引範本。 |
| [取得範本（舊版）]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-template-legacy/) | 傳回一或多個舊版索引範本的相關資訊。 |
| [範本是否存在（舊版）]({{site.url}}{{site.baseurl}}/api-reference/index-apis/template-exists-legacy/) | 檢查舊版索引範本是否存在。 |
| [刪除範本（舊版）]({{site.url}}{{site.baseurl}}/api-reference/index-apis/delete-template-legacy/) | 刪除舊版索引範本。 |