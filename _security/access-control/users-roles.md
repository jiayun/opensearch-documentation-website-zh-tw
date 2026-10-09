---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "定義使用者與角色"
parent: Access control
nav_order: 70
redirect_from:
 - /security-plugin/access-control/users-roles/
---

# 定義使用者與角色

您在 OpenSearch 中定義使用者，以控制誰可以存取 OpenSearch 資料。您可以使用內部使用者資料庫來儲存使用者，也可以將使用者儲存在外部驗證系統中，例如 [LDAP 或 Active Directory]({{site.url}}{{site.baseurl}}/security/authentication-backends/ldap/)。

您定義角色來決定權限或動作群組的範圍。您可以建立具有特定權限的角色，例如包含叢集層級權限、索引專屬權限、文件與欄位層級安全性，以及租用戶之任意組合的角色。

您可以在建立使用者時，或在使用者與角色定義完成後，將使用者對應到角色。此對應會根據指派給使用者的角色，決定該使用者的權限與存取層級。

---

<details closed markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 定義使用者

您可以使用 OpenSearch Dashboards、`internal_users.yml` 或 REST API 來定義使用者。建立使用者時，您可以使用 `internal_users.yml` 或 REST API 將使用者對應到角色。如果您使用 OpenSearch Dashboards 定義使用者，請依照[將使用者對應到角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#mapping-users-to-roles)教學中的步驟操作。

除非您要定義新的[保留或隱藏使用者]({{site.url}}{{site.baseurl}}/security/access-control/api/#reserved-and-hidden-resources)，否則建議使用 OpenSearch Dashboards 或 REST API 來建立新的使用者、角色與角色對應。`.yml` 檔案僅用於初始設定，不適合持續使用。
{: .warning }

### OpenSearch Dashboards

1. 選擇 **Security**、**Internal Users**，然後選擇 **Create internal user**。
1. 提供使用者名稱與密碼。Security 外掛程式會自動將密碼雜湊，並儲存在 `.opendistro_security` 索引中。
1. 視需要指定使用者屬性。

   屬性是選用的使用者屬性，可用於索引權限或文件層級安全性中的變數替換。

1. 選擇 **Submit**。

### `internal_users.yml`

請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#internal_usersyml)。


### REST API

請參閱[建立使用者]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。


## 定義角色

與定義使用者類似，您可以使用 OpenSearch Dashboards、`roles.yml` 或 REST API 來定義角色。OpenSearch 提供預先定義的角色以及一個特殊的唯讀角色。

除非您要定義新的 [保留或隱藏使用者]({{site.url}}{{site.baseurl}}/security/access-control/api/#reserved-and-hidden-resources)，否則建議使用 OpenSearch Dashboards 或 REST API 來建立新的使用者、角色與角色對應。`.yml` 檔案僅用於初始設定，不適合持續使用。
{: .warning }

### OpenSearch Dashboards

1. 選擇 **Security**、**Roles**，然後選擇 **Create role**。
1. 提供角色名稱。
1. 視需要新增權限。

   例如，您可以給予某個角色沒有叢集權限、給兩個索引 `read` 權限、給第三個索引 `unlimited` 權限，並給予 `analysts` 租用戶讀取權限。

1. 選擇 **Submit**。


### `roles.yml`

請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#rolesyml)。


### REST API

請參閱[建立角色]({{site.url}}{{site.baseurl}}/security/api/roles/create-role/)。

## 編輯角色

您可以使用下列其中一種方法編輯角色。

### OpenSearch Dashboards

1. 選擇 **Security** > **Roles**。在 **Create role** 區段中，選取 **Explore existing roles**。
1. 選取您要編輯的角色。
1. 選擇 **edit role**。對角色進行任何必要的更新。
1. 若要儲存變更，請選取 **Update**。

### `roles.yml`

請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#rolesyml)。

### REST API

請參閱[修補角色]({{site.url}}{{site.baseurl}}/security/api/roles/patch-roles/)。

## 將使用者對應到角色

如果您在建立使用者時未指定角色，可以在之後將角色對應到該使用者。

與使用者和角色一樣，您可以使用 OpenSearch Dashboards、`roles_mapping.yml` 或 REST API 來建立角色對應。

### OpenSearch Dashboards

1. 選擇 **Security**、**Roles**，然後選擇一個角色。
1. 選擇 **Mapped users** 索引標籤，然後選擇 **Manage mapping**。
1. 指定使用者或外部身分 (也稱為後端角色)。
1. 選擇 **Map**。


### `roles_mapping.yml`

請參閱 [YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#roles_mappingyml)。


### REST API

請參閱[建立角色對應]({{site.url}}{{site.baseurl}}/security/api/role-mappings/create-role-mapping/)。

## 定義唯讀角色

唯讀角色授予使用者從 OpenSearch 叢集讀取資料的能力，但不能修改或刪除任何資料。當您想要提供資料存取權以進行報告、分析或視覺化，而不允許修改資料或叢集本身時，唯讀角色非常實用。這可維持資料完整性，並防止意外或未經授權的變更。

與 OpenSearch 中的任何角色一樣，唯讀角色可以使用下列方法設定：
 
- 使用 OpenSearch Dashboards
- 修改 `yml` 組態檔案
- 使用 Cluster Settings API

熟悉角色與角色對應最簡單的方式是使用 OpenSearch Dashboards。此介面透過易於瀏覽的工作流程，簡化了建立角色以及將角色指派給使用者的過程。
{: .tip}

### 定義基本唯讀角色

若要建立一個基本唯讀角色，允許使用者存取 OpenSearch Dashboards、檢視現有的儀表板與視覺化，以及查詢不同的索引，請使用下列權限。這些權限會授予使用者存取叢集上所有租用戶與索引的權限。


#### 叢集權限

對於需要唯讀存取叢集層級資源 (例如視覺化或儀表板) 的使用者，請將 `cluster_composite_ops_ro` 權限新增至該使用者的角色。

#### 索引權限

需要存取權以檢視視覺化的使用者，也需要存取用來建立該視覺化的索引。若要授予使用者所有索引的唯讀存取權，請在 **Index** 下拉式選單中指定所有索引（`*`），並在 **Index Permissions** 中選擇 **Read**。

#### 租用戶權限

如果您使用租用戶來劃分團隊或專案之間的工作，請使用所有租用戶（`*`）選項，然後選擇 **Read only** 選項，如下圖所示。

![建立角色]({{site.url}}{{site.baseurl}}/images/role_creation_read_only.png)

設定完所有權限類型並定義角色之後，您可以在角色的 **Mapped users** 索引標籤上，將該角色直接對應到使用者。選取 **Map users**，然後選擇要對應到該角色的使用者，如下圖所示。

![對應使用者]({{site.url}}{{site.baseurl}}/images/mapping-users.png)

### OpenSearch Dashboards `readonly_mode`

OpenSearch Dashboards 的 `readonly_mode` 功能用於僅授予使用者存取 `Dashboards` 介面的權限，並將所有其他 UI 元素從畫面中移除。

若要設定此角色，請在您的 `opensearch_dashboards.yml` 檔案中新增下列一行：

`opensearch_security.readonly_mode.roles: [new_role]`

即使指派的角色授予額外權限，或使用者被對應到其他具有索引寫入權限的角色，OpenSearch Dashboards 仍會限制此存取權。使用 cURL 或 API 直接存取 OpenSearch 資料仍然允許，OpenSearch Dashboards 不會參與此通訊。

如果使用者被對應到 `readonly_mode` 角色，除了 `Dashboards` 之外，UI 的所有其他元素都會被移除。在下圖中，左側的畫面顯示被對應到 `readonly_mode` 角色的使用者所看到的畫面，右側的畫面則顯示使用者的標準畫面。

![compare read only mode]({{site.url}}{{site.baseurl}}/images/compare_read_only_mode.png)

僅將使用者對應到 `readonly_mode` 角色，並不允許該使用者檢視相關索引或現有的儀表板。對索引與儀表板的讀取權限需要另外設定。
{: .note }


如果使用者同時被對應到 `opensearch.yml` 中 `plugins.security.restapi.roles_enabled` 底下所列的任何角色，例如 `all_access` 或 `security_rest_api_access`，則 `readonly_mode` 會被忽略，使用者將可以存取標準的 UI 元素。

### 額外權限

如果使用者需要 `read_only` 角色所包含權限以外的權限，例如執行警示或異常偵測工作所需的權限，您可以指派預先定義的角色，例如 `alerting_read_access` 或 `anomaly_read_access`。

## 預先定義的角色

Security 外掛程式包含數個預先定義的角色，可作為實用的預設角色。

### 內建角色

下表列出一律提供的內建靜態角色。

| 角色 | 說明 |
| :--- | :--- |
| `all_access`| 具有完整叢集存取權的超級使用者角色。授予執行所有叢集操作、寫入所有索引及存取所有租用戶的權限。|
| `kibana_server` | OpenSearch Dashboards 伺服器使用者用來讀取／寫入其內部儲存物件與系統索引的角色。請勿指派給人員使用者。 |
| `kibana_user` | 允許使用者登入並使用 OpenSearch Dashboards。授予讀取與搜尋叢集、監控索引，以及寫入 OpenSearch Dashboards 索引的權限。請搭配您資料的讀取權限使用。 |
| `logstash`| 授予 Logstash 與 OpenSearch 互動所需的權限。 |
| `manage_snapshots`| 授予管理快照儲存庫及執行快照與快照還原操作的權限。 |
| `own_index` | 授予每位使用者完整存取自己索引（以使用者名稱命名）的權限。適用於個人工作區或多租用戶環境。 |
| `readall` | 授予對叢集中所有索引的讀取與搜尋權限，例如呼叫 `_search` 和 `_msearch` API。 |
| `readall_and_monitor` | 授予與 `readall` 相同的權限，並提供額外的叢集監控權限（例如檢視叢集健全狀態與統計資料）。 |

如需這些角色各項權限的詳細資訊，請參閱 [static_roles.yml](https://github.com/opensearch-project/security/blob/main/src/main/resources/static_config/static_roles.yml)。

### 示範角色

下表列出初始化 Security 外掛程式時，若未提供 `roles.yml` 檔案，預設會建立的示範角色。

| **角色** | **說明** |
| :--- | :--- |
| `alerting_ack_alerts`| 授予檢視及確認警示的權限，但不授予修改目的地或監視器的權限。 |
| `alerting_full_access` | 授予執行所有警示動作的完整權限。 |
| `alerting_read_access` | 授予檢視警示、目的地及監視器的權限，但不授予確認警示或修改目的地或監視器的權限。 |
| `anomaly_full_access`| 授予執行所有異常偵測動作的完整權限。 |
| `anomaly_read_access`| 授予檢視偵測器的權限，但不授予建立、修改或刪除偵測器的權限。 |
| `asynchronous_search_full_access`| 授予執行所有非同步搜尋動作的完整權限。 |
| `asynchronous_search_read_access`| 授予檢視非同步搜尋的權限，但不授予提交、修改或刪除這些搜尋的權限。 |
| `cross_cluster_replication_follower_full_access` | 授予在追隨者叢集上執行跨叢集複寫動作的完整存取權。 |
| `cross_cluster_replication_leader_full_access` | 授予在領導者叢集上執行跨叢集複寫動作的完整存取權。 |
| `index_management_full_access` | 授予執行所有索引管理動作的完整權限，包括 ISM、轉換及彙整。 |
| `ml_full_access` | 授予使用所有機器學習（ML）功能的完整權限，包括啟動工作及管理模型。 |
| `ml_read_access` | 授予檢視 ML 組態、統計資料、模型及工作的權限，但不授予修改這些項目的權限。 |
| `notifications_full_access`| 授予執行所有 Notifications 動作的完整權限。 |
| `notifications_read_access`| 授予檢視 Notifications 組態／通道及功能的權限，但不授予修改這些項目的權限。 |
| `point_in_time_full_access`| 授予執行所有時間點操作的完整權限。|
| `reports_instances_read_access`| 授予依需求產生報表及下載現有報表執行個體的權限，但不授予檢視／建立報表定義的權限。 |
| `security_analytics_ack_alerts`| 授予檢視及確認 Security Analytics 警示的權限。 |
| `security_analytics_full_access` | 授予使用所有 Security Analytics 功能的完整權限。 |
| `security_analytics_read_access` | 授予檢視 Security Analytics 偵測器、警示、發現結果、對應及規則的權限。 |
| `snapshot_management_full_access`| 授予執行所有快照管理動作（包括儲存庫與快照）的完整權限。|
| `snapshot_management_read_access`| 授予檢視快照管理政策、儲存庫及快照的權限，但不授予修改這些項目的權限。 |

如需指派給各角色的各項權限詳細資訊，請參閱 [roles.yml](https://github.com/opensearch-project/security/blob/main/config/roles.yml)。

## 範例 

以下教學說明在 OpenSearch Dashboards 中建立大量存取角色的步驟。

建立新的 `bulk_access` 角色：

1. 開啟 OpenSearch Dashboards。
1. 選取 **Security**、**Roles**。
1. 建立名為 `bulk_access` 的新角色。
1. 在 **Cluster permissions** 中，新增 `cluster_composite_ops` 動作群組。
1. 在 **Index Permissions** 中，新增索引模式。例如，您可以指定 `my-index-*`。
1. 在索引權限中，新增 `write` 動作群組。
1. 選取 **Create**。

將角色對應至您的使用者：

1. 選取 **Mapped users** 索引標籤及 **Manage mapping**。
1. 在 **Internal users** 中，新增您的大量存取使用者。
1. 選取 **Map**。

## 管理員與超級管理員角色

OpenSearch 使用者角色對於控制叢集資源的存取至關重要。根據使用者的存取權限與職責，可將使用者分為一般使用者、管理員使用者或超級管理員使用者。

如需定義使用者的詳細資訊，請參閱[定義使用者]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#defining-users)。如需定義角色的詳細資訊，請參閱[定義角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#defining-roles)。


### 一般使用者
一般使用者具有基本存取權限，可與 OpenSearch 叢集互動，例如查詢資料及使用儀表板，但不具備管理權限。

### 管理員使用者
管理員使用者具有較高的權限，可在叢集中執行各種管理工作。相較於一般使用者，他們具有更廣泛的存取權，包括下列權限：
- 管理使用者與角色。
- 設定權限。
- 調整後端設定。

管理員使用者可以透過設定 `opensearch.yml` 檔案中的設定、使用 OpenSearch Dashboards，或與 REST API 互動來執行這些工作。如需設定使用者與角色的詳細資訊，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#predefined-roles)。

### 超級管理員使用者
超級管理員使用者在 OpenSearch 環境中具有最高層級的管理權限。此角色通常保留給特定使用者，且應謹慎管理。

超級管理員使用者可不受限制地存取叢集中的所有設定與資料，包括下列權限：
- 修改 Security 外掛程式組態。
- 存取及管理安全性索引 `.opendistro_security`。
- 覆寫任何安全性限制。

#### 超級管理員角色的驗證

超級管理員使用者是透過憑證驗證，而非密碼。必要的憑證定義於 `opensearch.yml` 檔案的 `admin_dn` 區段中，且必須由相同的根憑證授權單位 (CA) 簽署，如下列範例所示：
```
YAML
plugins.security.authcz.admin_dn:
- CN=kirk,OU=client,O=client,L=test, C=de
``` 

如果超級管理員憑證是由不同的 CA 簽署，則必須在 `opensearch.yml` 中 `plugins.security.ssl.http.pemtrustedcas_filepath` 所定義的檔案裡，將管理員 CA 與節點的 CA 串接起來。

如需更多資訊，請參閱[設定超級管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)。
