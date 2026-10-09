---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "組態"
nav_order: 2
has_children: true
has_toc: true
redirect_from:
  - /security-plugin/configuration/
  - /security-plugin/configuration/index/
  - /security/configuration/
---

# 安全性組態

Security 外掛程式內含示範憑證，讓您可以快速啟動並開始使用。若要在生產環境中搭配 Security 外掛程式使用 OpenSearch，您必須手動變更示範憑證及其他組態選項。

## 取代示範憑證

OpenSearch 隨附示範憑證，僅供快速設定與示範之用。在生產環境中，請務必依照下列步驟將其取代為您自己的受信任憑證，以確保通訊安全：

1. **產生您自己的憑證：** 使用 OpenSSL 之類的工具或憑證授權單位 (CA) 來產生您自己的憑證。如需使用 OpenSSL 產生憑證的詳細資訊，請參閱[產生自簽憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)。
2. **將產生的憑證與私密金鑰存放在適當的目錄：** 產生的憑證通常存放在 `<OPENSEARCH_HOME>/config/`。如需詳細資訊，請參閱[將憑證檔案加入 opensearch.yml]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/#add-certificate-files-to-opensearchyml)。
3. **設定下列檔案權限：**
    - 私密金鑰 (.key 檔案)：將檔案模式設為 `600`。此設定會限制存取權，僅允許檔案擁有者 (OpenSearch 使用者) 讀取與寫入該檔案，確保私密金鑰保持安全，未經授權的使用者無法存取。
    - 公開憑證 (.crt、.pem 檔案)：將檔案模式設為 `644`。此設定允許檔案擁有者讀取與寫入該檔案，其他使用者則只能讀取。

如需檔案模式的進一步指引，請參閱下表。
        
        | 項目        | 範例              | 數值 | 位元運算      |
        |-------------|---------------------|---------|--------------|
        | 公開金鑰  | `~/.ssh/id_rsa.pub` | `644`   | `-rw-r--r--` |
        | 私密金鑰 | `~/.ssh/id_rsa`     | `600`   | `-rw-------` |
        | SSH 資料夾  | `~/.ssh`            | `700`   | `drwx------` |

如需詳細資訊，請參閱[設定基本安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#configuring-basic-security-settings)。

## 重新設定 `opensearch.yml` 以使用您的憑證

`opensearch.yml` 檔案是 OpenSearch 的主要組態檔；您可以在 `<OPENSEARCH_HOME>/config/opensearch.yml` 找到該檔案。請依照下列步驟更新此檔案，使其指向您的自訂憑證：

在 `opensearch.yml` 中，為您的憑證與金鑰設定正確的路徑，如下列範例所示：
   ```
   plugins.security.ssl.transport.pemcert_filepath: /path/to/your/cert.pem
   plugins.security.ssl.transport.pemkey_filepath: /path/to/your/key.pem
   plugins.security.ssl.transport.pemtrustedcas_filepath: /path/to/your/ca.pem
   plugins.security.ssl.http.enabled: true
   plugins.security.ssl.http.pemcert_filepath: /path/to/your/cert.pem
   plugins.security.ssl.http.pemkey_filepath: /path/to/your/key.pem
   plugins.security.ssl.http.pemtrustedcas_filepath: /path/to/your/ca.pem
   ```
如需詳細資訊，請參閱[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。

## 重新設定 `config.yml` 以使用您的驗證後端

`config.yml` 檔案可讓您設定 OpenSearch 的驗證與授權機制。請依照您的需求更新 `<OPENSEARCH_HOME>/config/opensearch-security/config.yml` 中的驗證後端設定。

例如，若要使用內部驗證後端，請加入下列設定：

  ```
    authc:
      basic_internal_auth:
        http_enabled: true
        transport_enabled: true
        order: 1
        http_authenticator:
          type: basic
          challenge: true
        authentication_backend:
          type: internal
   ```
如需詳細資訊，請參閱[設定 Security 後端]({{site.url}}{{site.baseurl}}/security/configuration/configuration/)。

## 修改組態 YAML 檔案

判斷是否還有其他 YAML 檔案需要修改，例如 `roles.yml`、`roles_mapping.yml` 或 `internal_users.yml` 檔案。請以其他組態資訊更新這些檔案。如需詳細資訊，請參閱[修改 YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)。

## 設定密碼原則

使用內部使用者資料庫時，我們建議強制執行密碼原則，以確保使用足夠強度的密碼。如需設定原則的資訊，請參閱[密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#password-settings)。如需叢集中密碼的概觀、各密碼由誰設定，以及如何變更，請參閱[管理密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/)。

## 使用 `securityadmin` 指令碼套用變更

下列步驟不適用於初次使用的使用者，因為 OpenSearch 啟動時會自動從 YAML 組態檔初始化安全性索引。
{: .note}

完成初始設定後，如果您變更了安全性組態，或透過將 `plugins.security.allow_default_init_securityindex` 設為 `false` 停用自動初始化 (這會防止從 `yaml` 檔案初始化安全性索引)，則需要使用 `securityadmin` 指令碼手動套用變更：

1. 找到 `securityadmin` 指令碼。該指令碼通常存放在 OpenSearch 外掛程式目錄 `plugins/opensearch-security/tools/securityadmin.[sh|bat]` 中。
   - 注意：如果您使用的是 OpenSearch 1.x，`securityadmin` 指令碼位於 `plugins/opendistro_security/tools/` 目錄中。
   - 如需詳細資訊，請參閱[基本用法]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/#basic-usage)。
2. 使用下列命令執行該指令碼：
   ```
    ./plugins/opensearch-security/tools/securityadmin.[sh|bat]
   ```
3. 檢查 OpenSearch 的記錄檔與組態，確認變更已成功套用。

如需使用 `securityadmin` 指令碼的詳細資訊，請參閱[將變更套用至組態檔]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

## 新增使用者、角色、角色對應與租用戶

如果您不想使用 Security 外掛程式，可以在 `opensearch.yml` 檔案中加入下列設定來停用它：

```
plugins.security.disabled: true
```

之後只要移除 `plugins.security.disabled` 設定，即可重新啟用該外掛程式。

如需停用 Security 外掛程式的詳細資訊，請參閱[停用安全性]({{site.url}}{{site.baseurl}}/security/configuration/disable-enable-security/)。

Security 外掛程式為 OpenSearch Dashboards 提供數個名稱中包含 "Kibana" 的預設使用者、角色、動作群組、權限與設定。我們將在未來版本中變更這些名稱。
{: .note }

如需 `opensearch.yml` Security 外掛程式設定的完整清單，請參閱[安全性設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/security-settings/)。
{: .note}

