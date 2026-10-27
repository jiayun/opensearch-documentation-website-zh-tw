---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "控制器 API"
parent: ML APIs
has_children: true
has_toc: false
nav_order: 60
redirect_from:
  - /ml-commons-plugin/api/controller-apis/
---

# 控制器 API
**於 2.12 版導入**
{: .label .label-purple }

您可以呼叫 Controller APIs，為模型的一位或多位特定使用者設定速率限制。

OpenSearch 支援下列控制器 API：

- [建立或更新控制器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/create-controller/)
- [取得控制器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/get-controller/)
- [刪除控制器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/delete-controller/)

## 必要權限

若要呼叫 Controller API，您必須具備 `cluster:admin/opensearch/ml/controllers/` 權限。各 Controller API 的詳細資訊連結已在前一節提供。