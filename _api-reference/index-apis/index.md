---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "索引 API"
has_children: true
has_toc: false
nav_order: 60
redirect_from:
  - /opensearch/rest-api/index-apis/index/
  - /opensearch/rest-api/index-apis/
  - /api-reference/index-apis/
---

# 索引 API
**於 1.0 版推出**
{: .label .label-purple }

索引 API 操作可讓您與叢集中的索引互動。使用這些操作，您可以建立、刪除、關閉索引，以及完成其他索引相關操作。

## 索引 API 操作

下列索引 API 操作依類別整理如下：

- [別名 API]({{site.url}}{{site.baseurl}}/api-reference/alias/) - 建立、更新、刪除索引別名，以及擷取索引別名的資訊
- [核心索引 API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/core-index-apis/) - 管理索引生命週期的基本操作
- [索引操作]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-operations/) - 維護及最佳化索引的進階功能
- [索引設定與對應]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-settings-mappings/) - 設定及修改索引的行為與結構
- [索引範本]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-templates/) - 建立及管理用於自動設定索引組態的範本
- [索引封鎖與分配]({{site.url}}{{site.baseurl}}/api-reference/index-apis/index-blocks-allocation/) - 控制索引存取限制與分片分配
- [懸置索引]({{site.url}}{{site.baseurl}}/api-reference/index-apis/dangling-index/) - 管理存在於磁碟上但不屬於叢集狀態的索引

若要管理資料串流，請使用[資料串流 API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/)。

如果您使用 Security 外掛程式，請確認您具備適當的權限。
{: .note }
