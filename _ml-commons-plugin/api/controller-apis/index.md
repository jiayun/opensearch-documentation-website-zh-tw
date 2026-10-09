---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Controller APIs
parent: ML Commons APIs
has_children: true
has_toc: false
nav_order: 60
redirect_from:
  - /ml-commons-plugin/api/controller-apis/
---

# Controller APIs
**於 2.12 版導入**
{: .label .label-purple }

您可以透過呼叫 Controller API，為特定使用者或某模型的多位使用者設定速率限制。

ML Commons 支援下列控制器層級的 API：

- [建立或更新控制器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/create-controller/)
- [取得控制器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/get-controller/)
- [刪除控制器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/delete-controller/)

## 必要權限

若要呼叫 Controller API，您必須具備 `cluster:admin/opensearch/ml/controllers/` 權限。各 Controller API 的詳細資訊連結已在前一節提供。