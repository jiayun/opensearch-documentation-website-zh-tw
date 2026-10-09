---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得稽核組態"
parent: Audit log APIs
grand_parent: Security APIs
nav_order: 30
---

# 取得稽核組態 API
**於 1.0 版引入**
{: .label .label-purple }

擷取稽核記錄與合規組態。

如需使用稽核記錄追蹤 OpenSearch 叢集存取情形的詳細資訊，以及其他組態的資訊，請參閱[稽核記錄檔]({{site.url}}{{site.baseurl}}/security/audit-logs/index/)。

<!-- spec_insert_start
api: security.get_audit_configuration
component: endpoints
-->
## 端點
```json
GET /_plugins/_security/api/audit
```
<!-- spec_insert_end -->

## 請求範例

```json
GET _plugins/_security/api/audit
```
{% include copy-curl.html security=true %}

## 回應範例

此處的回應已省略部分內容：

```json
{
  "_readonly": [],
  ...
}
```

## 回應本文欄位

`_readonly` 欄位列出無法修改的組態路徑。變更這些路徑會導致 409 錯誤。`config` 欄位包含目前的稽核與合規設定。如需各項設定的說明，請參閱[更新稽核組態 API]({{site.url}}{{site.baseurl}}/security/api/audit/update-audit-configuration/#request-body-fields)。
