---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "新增評論"
nav_order: 35
parent: Alerting
has_children: false
redirect_from:
  - /monitoring-plugins/alerting/comments/
---

# 新增警示評論

當產生警示時，可以新增評論來分享根本原因的相關資訊，並協助解決問題。若要啟用評論，請使用 [`cluster/settings` API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/settings/) 將 `plugins.alerting.comments_enabled` 設定為 `true`。

您可以透過警示表格檢視來存取評論，只要選取警示列中的評論圖示即可。從那裡可以新增、編輯或刪除評論。此外也提供 Alerting Comments API，可用於以程式化管理評論。如需更多資訊，請參閱 [Alerting API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/)。

## 檢視評論作者

如果已安裝 Security 外掛程式，則會顯示評論的作者。否則會顯示 `Unknown`。

## 指派權限

評論權限由與警示相關聯的後端角色決定。這些後端角色繼承自產生警示的監視器。如需如何根據後端角色限制存取權的詳細資訊，請參閱[依後端角色限制存取權]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/security/#advanced-limit-access-by-backend-role)。
