---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多租用戶組態"
parent: OpenSearch Dashboards multi-tenancy
nav_order: 145
---


# 多租用戶組態

OpenSearch Dashboards 預設會啟用多租用戶。如果您需要停用或變更與多租用戶相關的設定，請參閱 `config/opensearch-security/config.yml` 中的 `kibana` 設定，如下列範例所示：

```yml
config:
  dynamic:
    kibana:
      multitenancy_enabled: true
      private_tenant_enabled: true
      default_tenant: global tenant
      server_username: kibanaserver
      index: '.kibana'
    do_not_fail_on_forbidden: false
```

| 設定 | 說明 |
| :--- | :--- |
| `multitenancy_enabled` | 啟用或停用多租用戶。預設為 `true`。 |
| `private_tenant_enabled` | 啟用或停用私有租用戶。預設為 `true`。 |
| `default_tenant` | 用於設定使用者登入時可用的租用戶。 |
| `server_username` | 必須與 `opensearch_dashboards.yml` 中 OpenSearch Dashboards 伺服器使用者的名稱相符。預設為 `kibanaserver`。如果設定了其他使用者，請確保該使用者已透過 `role_mappings.yml` 檔案對應至 `kibana_server` 角色，以取得 [kibana_server 角色詳細資料]({{site.url}}{{site.baseurl}}/security/multi-tenancy/multi-tenancy-config/#kibana_server-role-details) 中列出的適當權限。 |
| `index` | 必須與 `opensearch_dashboards.yml` 中的 OpenSearch Dashboards 索引名稱相符。預設為 `.kibana`。 |
| `do_not_fail_on_forbidden` | 當設定為 `true` 時，Security 外掛程式會從搜尋結果中移除使用者無權檢視的任何內容。當設定為 `false` 時，外掛程式會回傳安全性例外。預設為 `false`。 |

`opensearch_dashboards.yml` 檔案包含其他設定：

```yml
opensearch.username: kibanaserver
opensearch.password: kibanaserver
opensearch.requestHeadersAllowlist: ["securitytenant","Authorization"]
opensearch_security.multitenancy.enabled: true
opensearch_security.multitenancy.tenants.enable_global: true
opensearch_security.multitenancy.tenants.enable_private: true
opensearch_security.multitenancy.tenants.preferred: ["Private", "Global"]
opensearch_security.multitenancy.enable_filter: false
```

| 設定 | 說明 |
| :--- | :--- |
| `opensearch.requestHeadersAllowlist` | OpenSearch Dashboards 要求您將所有 HTTP 標頭加入允許清單，以便這些標頭傳遞至 OpenSearch。多租用戶使用特定的標頭 `securitytenant`，該標頭必須與標準的 `Authorization` 標頭一併存在。如果 `securitytenant` 標頭不在允許清單中，OpenSearch Dashboards 會以紅色狀態啟動。
| `opensearch_security.multitenancy.enabled` | 啟用或停用 OpenSearch Dashboards 中的多租用戶。預設為 `true`。 |
| `opensearch_security.multitenancy.tenants.enable_global` | 啟用或停用全域租用戶。預設為 `true`。 |
| `opensearch_security.multitenancy.tenants.enable_private` | 啟用或停用私有租用戶。預設為 `true`。 |
| `opensearch_security.multitenancy.tenants.preferred` | 可讓您變更 OpenSearch Dashboards 中 **Tenants** 索引標籤的排序。預設情況下，清單會以 Global 和 Private (如果已啟用) 開頭，然後按字母順序排列。您可以在此新增租用戶，將它們移至清單頂端。 |
| `opensearch_security.multitenancy.enable_filter` | 如果您有許多租用戶，可以在清單頂端新增搜尋列。預設為 `false`。 |


## 新增租用戶

若要建立租用戶，請使用 OpenSearch Dashboards、REST API 或 `tenants.yml`。


#### OpenSearch Dashboards

1. 開啟 OpenSearch Dashboards。
1. 選擇 **Security**、**Tenants**，然後選擇 **Create tenant**。
1. 為租用戶提供名稱與描述。
1. 選擇 **Create**。


#### REST API

請參閱[建立租用戶]({{site.url}}{{site.baseurl}}/security/api/tenants/create-tenant/)。


#### tenants.yml

```yml
---
_meta:
  type: "tenants"
  config_version: 2

## Demo tenants
admin_tenant:
  reserved: false
  description: "Demo tenant for admin user"
```

## 將租用戶的存取權授予角色

建立租用戶後，請使用 OpenSearch Dashboards、REST API 或 `roles.yml` 將該租用戶的存取權授予角色。

- 讀寫 (`kibana_all_write`) 權限可讓角色檢視及修改租用戶中的物件。
- 唯讀 (`kibana_all_read`) 權限可讓角色檢視物件，但無法修改。


#### OpenSearch Dashboards

1. 開啟 OpenSearch Dashboards。
1. 選擇 **Security**、**Roles**，然後選擇一個角色。
1. 在 **Tenant permissions** 中，新增租用戶、按 Enter 鍵，並為該角色授予讀取及/或寫入權限。


#### REST API

請參閱[建立角色]({{site.url}}{{site.baseurl}}/security/api/roles/create-role/)。


#### roles.yml

```yml
---
test-role:
  reserved: false
  hidden: false
  cluster_permissions:
  - "cluster_composite_ops"
  - "indices_monitor"
  index_permissions:
  - index_patterns:
    - "movies*"
    dls: ""
    fls: []
    masked_fields: []
    allowed_actions:
    - "read"
  tenant_permissions:
  - tenant_patterns:
    - "human_resources"
    allowed_actions:
    - "kibana_all_read"
  static: false
_meta:
  type: "roles"
  config_version: 2
```


## 管理 OpenSearch Dashboards 索引

OpenSearch Dashboards 的開放原始碼版本會將所有物件儲存至單一索引：`.kibana`。Security 外掛程式會將此索引用於全域租用戶，並為其他每個租用戶使用個別的索引。每位使用者也有自己的私有租用戶，因此您可能會看到大量遵循兩種模式的索引：

```
.kibana_<hash>_<tenant_name>
.kibana_<hash>_<username>
```

Security 外掛程式會清除這些索引名稱中的特殊字元，因此它們可能與租用戶名稱和使用者名稱不完全相符。
{: .tip }

若要備份您的 OpenSearch Dashboards 資料，請使用 `.kibana*` 之類的索引模式，對所有租用戶索引[建立快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/)。

<!-- vale off -->
## `kibana_server` 角色詳細資料
<!-- vale on -->

OpenSearch Dashboards 使用 `kibana_server` 角色來執行必要的 OpenSearch 作業。預設情況下，`kibanauser` 會透過 `role_mappings.yml` 檔案對應至此角色。您可以向 `_plugins/_security/api/roles/kibana_server` API 傳送 GET 請求，以檢視指派給此角色的完整權限清單 (請在 GET 請求中包含管理員憑證、金鑰與憑證授權單位檔案)。
下列清單包含指派給此角色的權限：

```
{
  "kibana_server" : {
    "reserved" : true,
    "hidden" : false,
    "description" : "Provide the minimum permissions for the Kibana server",
    "cluster_permissions" : [
      "cluster_monitor",
      "cluster_composite_ops",
      "manage_point_in_time",
      "indices:admin/template*",
      "indices:admin/index_template*",
      "indices:data/read/scroll*"
    ],
    "index_permissions" : [
      {
        "index_patterns" : [
          ".kibana",
          ".opensearch_dashboards"
        ],
        "fls" : [ ],
        "masked_fields" : [ ],
        "allowed_actions" : [
          "indices_all"
        ]
      },
      {
        "index_patterns" : [
          ".kibana-6",
          ".opensearch_dashboards-6"
        ],
        "fls" : [ ],
        "masked_fields" : [ ],
        "allowed_actions" : [
          "indices_all"
        ]
      },
      {
        "index_patterns" : [
          ".kibana_*",
          ".opensearch_dashboards_*"
        ],
        "fls" : [ ],
        "masked_fields" : [ ],
        "allowed_actions" : [
          "indices_all"
        ]
      },
      {
        "index_patterns" : [
          ".tasks"
        ],
        "fls" : [ ],
        "masked_fields" : [ ],
        "allowed_actions" : [
          "indices_all"
        ]
      },
      {
        "index_patterns" : [
          ".management-beats*"
        ],
        "fls" : [ ],
        "masked_fields" : [ ],
        "allowed_actions" : [
          "indices_all"
        ]
      },
      {
        "index_patterns" : [
          "*"
        ],
        "fls" : [ ],
        "masked_fields" : [ ],
        "allowed_actions" : [
          "indices:admin/aliases*"
        ]
      }
    ],
    "tenant_permissions" : [ ],
    "static" : true
  }
}
```

## 以多位使用者測試租用戶

如果您在同一個瀏覽器中測試多位使用者，而所選租用戶意外變更，請在個別的私密瀏覽視窗中以每位使用者登入，例如 Google Chrome 的無痕視窗或 Firefox 的私密視窗。
