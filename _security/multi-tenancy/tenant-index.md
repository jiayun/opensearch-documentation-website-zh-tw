---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch Dashboards 多租用戶"
nav_order: 140
has_children: true
has_toc: false
redirect_from:
  - /security/multi-tenancy/
  - /security-plugin/access-control/multi-tenancy/
  - /security/access-control/multi-tenancy/
---

# OpenSearch Dashboards 多租用戶

OpenSearch Dashboards 中的*租用戶*是用來儲存索引模式、視覺化、儀表板及其他 OpenSearch Dashboards 物件的空間。OpenSearch 允許使用者建立多個租用戶以供多種用途使用。租用戶適合用來安全地與其他 OpenSearch Dashboards 使用者分享您的工作。您可以控制哪些角色可以存取租用戶，以及這些角色是否具有讀取或寫入權限。根據預設，所有 OpenSearch Dashboards 使用者都可以存取兩個獨立的租用戶：全域租用戶與私人租用戶。多租用戶也提供建立自訂租用戶的選項。

- **全域** -- 此租用戶由每個 OpenSearch Dashboards 使用者共用。它允許在可存取該租用戶的使用者之間分享物件。
- **私人** -- 此租用戶專屬於每位使用者，無法共用。它不允許您存取該使用者的全域租用戶所建立的路由或索引模式。
- **自訂** -- 管理員可以建立自訂租用戶並將其指派給特定角色。建立後，這些租用戶便可為特定使用者群組提供空間。

OpenSearch Dashboards 中的全域租用戶不會將其內容與私人租用戶同步。當您在全域租用戶中進行修改時，這些變更僅限於全域租用戶。它們不會自動反映或複寫到私人租用戶中。私人租用戶與全域租用戶的一些範例變更包括下列項目：

- 變更進階設定
- 建立視覺化
- 建立索引模式

舉一個實際的例子，您可以使用私人租用戶進行探索性工作，在 `analysts` 租用戶中與團隊建立詳細的視覺化，並在 `executive` 租用戶中為公司領導階層維護摘要儀表板。

如果您與某人分享視覺化或儀表板，您可以看到 URL 中包含該租用戶：

```
http://<opensearch_dashboards_host>:5601/app/opensearch-dashboards?security_tenant=analysts#/visualize/edit/c501fa50-7e52-11e9-ae4e-b5d69947d32e?_g=()
```

## 後續步驟

若要開始使用租用戶，請參閱[多租用戶組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/)，以取得啟用多租用戶、新增租用戶及將角色指派給租用戶的相關資訊。

如需對多租用戶組態進行動態變更的相關資訊，請參閱 [OpenSearch Dashboards 中的動態組態]({{site.url}}{{site.baseurl}}/security/multi-tenancy/dynamic-config/)。

