---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: AD LDAP
parent: Supported log types
nav_order: 20
---

# AD LDAP 記錄類型

`ad_ldap` 記錄類型會追蹤 Active Directory 記錄檔，例如：

- 輕量型目錄存取協定 (LDAP) 查詢。
- LDAP 伺服器的錯誤。
- 逾時事件。
- 未受保護的 LDAP 繫結。

下列程式碼片段包含此記錄類型的所有 `raw_field` 與 `ecs` 對應：

```json
 "mappings": [
   {
      "raw_field":"TargetUserName",
      "ecs":"azure.signinlogs.properties.user_id"
    },
    {
      "raw_field":"creationTime",
      "ecs":"timestamp"
    },
    {
      "raw_field":"Category",
      "ecs":"azure.activitylogs.category"
    },
    {
      "raw_field":"OperationName",
      "ecs":"azure.platformlogs.operation_name"
    },
    {
      "raw_field":"ModifiedProperties_NewValue",
      "ecs":"modified_properties.new_value"
    },
    {
      "raw_field":"ResourceProviderValue",
      "ecs":"azure.resource.provider"
    },
    {
      "raw_field":"conditionalAccessStatus",
      "ecs":"azure.signinlogs.properties.conditional_access_status"
    },
    {
      "raw_field":"SearchFilter",
      "ecs":"SearchFilter"
    },
    {
      "raw_field":"Operation",
      "ecs":"azure.platformlogs.operation_name"
    },
    {
      "raw_field":"ResultType",
      "ecs":"azure.platformlogs.result_type"
    },
    {
      "raw_field":"DeviceDetail_isCompliant",
      "ecs":"azure.signinlogs.properties.device_detail.is_compliant"
    },
    {
      "raw_field":"ResourceDisplayName",
      "ecs":"resource_display_name"
    },
    {
      "raw_field":"AuthenticationRequirement",
      "ecs":"azure.signinlogs.properties.authentication_requirement"
    },
    {
      "raw_field":"TargetResources",
      "ecs":"target_resources"
    },
    {
      "raw_field":"Workload",
      "ecs":"workload"
    },
    {
      "raw_field":"DeviceDetail.deviceId",
      "ecs":"azure.signinlogs.properties.device_detail.device_id"
    },
    {
      "raw_field":"OperationNameValue",
      "ecs":"azure.platformlogs.operation_name"
    },
    {
      "raw_field":"ResourceId",
      "ecs":"azure.signinlogs.properties.resource_id"
    },
    {
      "raw_field":"ResultDescription",
      "ecs":"azure.signinlogs.result_description"
    },
    {
      "raw_field":"EventID",
      "ecs":"EventID"
    },
    {
      "raw_field":"NetworkLocationDetails",
      "ecs":"azure.signinlogs.properties.network_location_details"
    },
    {
      "raw_field":"CategoryValue",
      "ecs":"azure.activitylogs.category"
    },
    {
      "raw_field":"ActivityDisplayName",
      "ecs":"azure.auditlogs.properties.activity_display_name"
    }
  ]
```