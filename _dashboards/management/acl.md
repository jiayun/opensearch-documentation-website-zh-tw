---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "已儲存物件的存取控制清單"
parent: Saved objects
grand_parent: Dashboards management
nav_order: 20
---

# 已儲存物件的存取控制清單
於 2.18 版引入
{: .label .label-purple }

您可以使用存取控制清單 (ACL) 管理已儲存物件的權限，無需整合後端外掛程式即可提供授權 (AuthZ) 功能。

## 了解 ACL 類型

ACL 會在兩個層級套用：

1. **工作區 ACL：**工作區物件會繼承其上層工作區的權限。如需詳細資訊，請參閱[工作區 ACL]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/)。
2. **物件 ACL：**每個個別物件都可以擁有自己的 ACL 政策。對這些物件執行的所有操作都必須通過 ACL 政策驗證。

## 啟用 ACL 功能

您必須先啟用 ACL 功能，才能定義任何存取控制。請依下列步驟啟用：

1. 開啟您的 `opensearch_dashboards.yml` 檔案。
2. 使用 `savedObjects.permission.enabled: true` 啟用權限。

## 定義 ACL 權限

ACL 權限使用下列結構描述定義：

```json
{
  "permissions": {
    "<permission_type_1>": {
        "users": ["<principal_1>", "<principal_2>"],
        "groups": ["<principal_3>", "<principal_4>"]
    }
  } 
}
```
{% include copy-curl.html %}

### 將權限授予已驗證的使用者

萬用字元 (`*`) 會將權限授予所有已驗證的使用者。在下列範例中，ACL 將工作區管理權限授予 `finance_manager` 群組，並將儀表板建立權限授予 `finance_analyst` 群組：

```json
{
  "permissions": {
    "write": {
        "groups": ["finance_manager"]
    },
    "library_write": {
        "groups": ["finance_analyst"]
    }
  } 
}
```
{% include copy-curl.html %}

### 設定混合層級權限

若要允許某個使用者（例如 `user-1`）修改物件，同時為其他使用者提供唯讀存取權，您可以依下列方式設定 ACL 政策：

```json
{
  "permissions": {
    "read": {
        "users": ["*"]
    },
    "write": {
        "users": ["user-1"]
    },
  }
}
```
{% include copy-curl.html %}
