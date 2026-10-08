---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快照 API"
has_children: true
has_toc: false
nav_order: 120
redirect_from:
  - /opensearch/rest-api/snapshots/
  - /api-reference/snapshots/
---

# 快照 API
**於 1.0 版導入**
{: .label .label-purple }

快照 API 可讓您管理快照與快照儲存庫。

## 快照 API 操作

下列快照 API 操作可供使用。

### 儲存庫管理
- [建立儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/)
- [取得快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/)
- [刪除快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/delete-snapshot-repository/)
- [驗證快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/verify-snapshot-repository/)
- [清理快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/cleanup-snapshot-repository/)

### 快照管理
- [建立快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/)
- [取得快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/)
- [取得快照狀態]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-status/)
- [刪除快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/delete-snapshot/)
- [複製快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/clone-snapshot/)
- [還原快照]({{site.url}}{{site.baseurl}}/api-reference/snapshots/restore-snapshot/)
