---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch 安全性入門"
nav_order: 1
redirect_from:
  - /getting-started/security/
---

# OpenSearch 安全性入門

示範組態是開始使用 OpenSearch 安全性最直接的方式。OpenSearch 隨附了許多實用的指令碼，包括 `install_demo_configuration.sh`（Windows 則為 `install_demo_configuration.bat`）。

此指令碼位於 `plugins/opensearch-security/tools`，並執行下列動作：

- 建立示範憑證，用於傳輸層與 REST 層的 TLS 加密。
- 設定示範使用者、角色與角色對應。
- 設定安全性外掛程式，使用內部資料庫進行驗證與授權。
- 以啟動叢集所需的基本組態更新 `opensearch.yml` 檔案。

您可以在[設定示範組態]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/)找到更多關於示範組態以及如何快速入門的資訊。
{: .note}

此組態的某些部分（例如示範憑證與預設密碼）絕不應在正式環境中使用。在進入正式環境之前，應以您的自訂資訊取代示範組態的這些部分。
{: .warning}

## 設定示範組態

在執行 `install_demo_configuration.sh` 指令碼之前，您必須建立名為 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 的環境變數並設定高強度密碼。這將做為 admin 使用者向 OpenSearch 進行驗證的密碼。關於密碼必須符合的規則，請參閱[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)。關於叢集中其他密碼的概觀以及如何變更這些密碼，請參閱[管理密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/)。完成後，您可以執行 `install_demo_configuration.sh` 並依照終端機提示輸入必要的詳細資料。

指令碼執行完畢後，您可以啟動 OpenSearch 並執行下列命令來測試組態：

```
curl -k -XGET -u admin:<password> https://<opensearch-ip>:9200
```
{% include copy.html %}

您應該會看到類似下列的輸出：

```
{
  "name" : "smoketestnode",
  "cluster_name" : "opensearch",
  "cluster_uuid" : "0a5DYAk0Rbi14wqT3TqMiQ",
  "version" : {
    "distribution" : "opensearch",
    "number" : "2.13.0",
    "build_type" : "tar",
    "build_hash" : "7ec678d1b7c87d6e779fdef94e33623e1f1e2647",
    "build_date" : "2024-03-26T00:04:51.025238748Z",
    "build_snapshot" : false,
    "lucene_version" : "9.10.0",
    "minimum_wire_compatibility_version" : "7.10.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

## 設定 OpenSearch Dashboards

為了快速開始使用 OpenSearch Dashboards，您可以將下列組態新增至 `opensearch_dashboards.yml`：

```
opensearch.hosts: [https://localhost:9200]
opensearch.ssl.verificationMode: none
opensearch.username: kibanaserver
opensearch.password: kibanaserver
opensearch.requestHeadersWhitelist: [authorization, securitytenant]

opensearch_security.multitenancy.enabled: true
opensearch_security.multitenancy.tenants.preferred: [Private, Global]
opensearch_security.readonly_mode.roles: [kibana_read_only]
# Use this setting if you are running opensearch-dashboards without https
opensearch_security.cookie.secure: false
```
{% include copy.html %}

您可以啟動二進位檔或服務，取決於安裝 OpenSearch 與 OpenSearch Dashboards 所使用的方法。

使用二進位檔時，您需要將 `--no-base-path` 提供給 `yarn start` 命令，以設定不含基礎路徑的 URL。若未設定此項，將會新增隨機的三個字母基礎路徑。
{: .note}

啟動 OpenSearch Dashboards 之後，您應該會看到下列兩行記錄：

```
[info][listening] Server running at http://localhost:5601
[info][server][OpenSearchDashboards][http] http server running at http://localhost:5601
```
{% include copy.html %}

您現在可以在瀏覽器中使用 http://localhost:5601 存取 OpenSearch Dashboards。請使用使用者名稱 `admin` 以及設定於 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 環境變數中的密碼。

# 新增使用者

有三種方式可以新增使用者、角色與其他安全性相關組態：

  - 更新適當的組態檔案（`internal_users.yml` 用於新增/更新/移除使用者）
  - 使用 API
  - 使用 OpenSearch Dashboards

安全性組態檔案位於 `config/opensearch-security` 目錄中。
{: .note}

您可以藉由以下列設定更新 `internal_users.yml` 檔案來新增 OpenSearch Dashboards 使用者：

```
test-user:
  hash: "$2y$12$CkxFoTAJKsZaWv/m8VoZ6ePG3DBeBTAvoo4xA2P21VCS9w2RYumsG"
  backend_roles:
  - "test-backend-role"
  - "kibanauser"
  description: "test user user"
```
{% include copy.html %}

`hash` 字串是使用位於 `plugins/opensearch-security/tools/` 目錄中的 `hash.sh` 指令碼所產生。在此情況下，使用了字串 `secretpassword` 的雜湊值。

請注意使用了內建後端角色 `kibanauser`，其提供瀏覽 OpenSearch Dashboards 所需的使用者權限。

## 建立角色

`roles.yml` 中包含的角色使用下列結構：

```
<rolename>:
  cluster_permissions:
    - <cluster permission>
  index_permissions:
    - index_patterns:
      - <index pattern>
      allowed_actions:
        - <index permissions>
```
{% include copy.html %}

使用此結構，您可以設定新角色以提供特定索引的存取權，例如下列範例中所設定的角色：

```
human_resources:
  index_permissions:
    - index_patterns:
      - "humanresources"
      allowed_actions:
        - "READ"
```
{% include copy.html %}

請注意，此範例中未列出叢集權限，因為這些權限是由內建角色 `kibana_user` 所提供，而該角色已使用 `kibanauser` 後端角色進行對應。


## 將使用者對應至角色

當使用者登入 OpenSearch 時，必須將其對應至適當的角色，才能取得正確的權限。此對應是使用 `roles_mapping.yml` 檔案並採用下列結構來執行：

```
<role_name>:
  users:
    - <username>
    - ...
  backend_roles:
    - <rolename>
```
{% include copy.html %}

為了將新建的使用者 `test-user` 對應至角色 `human_resources`，您可以在 `roles_mapping.yml` 檔案中使用下列組態：

```
human_resources:
  backend_roles:
    - test-backend-role
```
{% include copy.html %}

另一個範例是，`roles_mappings.yml` 檔案包含已對應至 `kibana_user` 角色的後端角色 `kibanauser`：

```
kibana_user:
  reserved: false
  backend_roles:
  - "kibanauser"
  description: "Maps kibanauser to kibana_user"
```
{% include copy.html %}

## 將組態上傳至安全性索引

設定使用者、角色或任何其他安全性組態的最後一個步驟，是將其組態上傳至 OpenSearch 安全性索引。僅更新檔案而未上傳，並不會變更已在執行中的 OpenSearch 叢集組態。

若要上傳組態，可以搭配 `install_demo_configuration.sh` 執行期間所產生的管理員憑證使用下列命令：

```
./plugins/opensearch-security/tools/securityadmin.sh -cd "config/opensearch-security" -icl -key "../kirk-key.pem" -cert "../kirk.pem" -cacert "../root-ca.pem" -nhnv
```
{% include copy.html %}

## 後續步驟

[OpenSearch 安全性最佳實務]({{site.url}}{{site.baseurl}}/security/configuration/best-practices/)指南涵蓋開始使用 OpenSearch 安全性時應考量的 10 件事。

[安全性組態]({{site.url}}{{site.baseurl}}/security/configuration/index/)概觀提供在 OpenSearch 實作中設定安全性的基本步驟，並包含可讓您為業務需求自訂安全性的相關資訊連結。 