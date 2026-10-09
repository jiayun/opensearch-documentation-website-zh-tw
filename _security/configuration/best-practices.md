---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "最佳做法"
parent: Configuration
nav_order: 5
---

# OpenSearch 安全性最佳做法

在 OpenSearch 中設定安全性對於保護您的資料至關重要。以下是 10 項最佳做法，為維持系統安全提供明確的步驟。

## 1. 使用您自己的 PKI 來設定 SSL/TLS

雖然使用您自己的公開金鑰基礎架構 (PKI)，例如 [AWS Certificate Manager](https://docs.aws.amazon.com/crypto/latest/userguide/awspki-service-acm.html)，需要較多的初始投入，但自訂的 PKI 能提供您以最安全且效能最佳的方式設定 SSL/TLS 所需的彈性。

### 為節點層與 REST 層流量啟用 SSL/TLS

SSL/TLS 在傳輸層預設為啟用，該層用於節點之間的通訊。SSL/TLS 在 REST 層預設為停用。

若要在 REST 層啟用加密，需要下列設定：

```
plugins.security.ssl.http.enabled: true
```
{% include copy.html %}


如需其他組態選項，例如指定憑證路徑、金鑰與憑證授權單位檔案，請參閱[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。

### 將所有示範憑證替換為您自己的 PKI

使用 `install_demo_configuration.sh` 初始化 OpenSearch 叢集時所產生的憑證不適合用於正式環境。這些憑證應替換為您自己的憑證。

您可以用幾種不同的方式產生自訂憑證。其中一種方式是使用 OpenSSL，詳細說明請見[產生自我簽署憑證]({{site.url}}{{site.baseurl}}/security/configuration/generate-certificates/)。此外，也有一些線上工具可以簡化憑證建立流程，例如：

- [SearchGuard TLS Tool](https://docs.search-guard.com/latest/offline-tls-tool)
- [`TLSTool` (由 `dylandreimerink` 提供)](https://github.com/dylandreimerink/tlstool)

## 2. API 驗證建議優先使用用戶端憑證驗證

用戶端憑證驗證為密碼驗證提供了安全的替代方案，更適合機器對機器的互動。由於驗證是在 TLS 層級進行，因此也能確保低效能負擔。幾乎所有的用戶端軟體，例如 cURL 與用戶端程式庫，都支援這種驗證方式。

如需用戶端憑證驗證的詳細設定說明與其他資訊，請參閱[啟用用戶端憑證驗證]({{site.url}}{{site.baseurl}}/security/authentication-backends/client-auth/#enabling-client-certificate-authentication)。


## 3. OpenSearch Dashboards 驗證建議優先使用 SAML 或 OpenID 的 SSO

使用 SAML 或 OpenID 等通訊協定為 OpenSearch Dashboards 驗證實作單一登入 (SSO)，可將登入認證資訊的管理委派給專門的系統，從而提升安全性。

這種做法可減少在 OpenSearch 中直接操作密碼、簡化驗證流程，並避免內部使用者資料庫雜亂。如需更多資訊，請前往 [OpenSearch 文件的 SAML 章節]({{site.url}}{{site.baseurl}}/security/authentication-backends/saml/)。

## 4. 限制指派給使用者的角色數量

優先採用數量較少但更精細的使用者角色，而非大量過於簡化的角色，可提升安全性並簡化管理。

其他角色管理的最佳做法包括：

1. 角色粒度：依據特定工作職能或存取需求定義角色，以減少不必要的權限。
2. 定期角色審查：定期審查與稽核已指派的角色，以確保符合組織政策與存取需求。

如需更多關於角色的資訊，請前往[在 OpenSearch 中定義使用者與角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/)的文件。

## 5. 驗證 DLS、FLS 與欄位遮罩

如果您已設定文件層級安全性 (DLS)、欄位層級安全性 (FLS) 或欄位遮罩，請務必仔細檢查您的角色定義，尤其是當使用者被對應到多個角色時。強烈建議您透過向 `_plugins/_security/authinfo` 發出 GET 請求來進行測試。

下列資源提供詳細範例與其他組態：

 - [文件層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/document-level-security/)。
 - [欄位層級安全性]({{site.url}}{{site.baseurl}}/security/access-control/field-level-security/)。
 - [欄位遮罩]({{site.url}}{{site.baseurl}}/security/access-control/field-masking/)。

## 6. 稽核記錄組態只保留必要的項目

過多的稽核記錄可能會因下列原因降低系統效能：

- 每個記錄的事件都會增加處理負擔。
- 稽核記錄檔可能會快速成長，佔用大量磁碟空間。

為確保最佳效能，請停用不必要的記錄，並審慎選擇要使用的記錄。如果合規法規沒有嚴格要求，請考慮關閉稽核記錄。如果稽核記錄對您的叢集至關重要，請依據您的合規需求進行設定。

請盡可能遵循下列建議：

- 將 `audit.log_request_body` 設為 `false`。
- 將 `audit.resolve_bulk_requests` 設為 `false`。
- 啟用 `compliance.write_log_diffs`。
- 減少 `compliance.read_watched_fields` 的項目。
- 減少 `compliance.write_watched_indices` 的項目。

## 7. 考慮停用私有租用戶

在許多情況下，私有租用戶並非必要，但此功能預設為啟用。因此，每位 OpenSearch Dashboards 使用者都會獲得自己的私有租用戶，以及一個用來儲存物件的新索引。這可能導致大量不必要的索引。請評估您的叢集是否需要私有租用戶。如果不需要，請在 `config.yml` 檔案中加入下列組態以停用此功能：

```yaml
config:
  dynamic:
    kibana:
      multitenancy_enabled: true
      private_tenant_enabled: false
```
{% include copy.html %}

## 8. 使用 `securityadmin.sh` 管理組態

請使用 `securityadmin.sh` 來管理叢集的組態。`securityadmin.sh` 是 OpenSearch 提供的命令列工具，用於管理安全性組態。它讓管理員能夠有效率地管理安全性設定，包括 OpenSearch 叢集內的角色、角色對應與其他安全性相關組態。

使用 `securityadmin.sh` 具有下列好處：

1. 一致性：透過使用 `securityadmin.sh`，管理員可以確保叢集內安全性組態的一致性，有助於維持標準化且安全的環境。
2. 自動化：`securityadmin.sh` 可將安全性組態工作自動化，讓跨多個節點或叢集部署與管理安全性設定更加容易。
3. 版本控制：透過 `securityadmin.sh` 管理的安全性組態可以使用 Git 等標準版本控制系統進行版本控制，便於追蹤變更、稽核以及還原至先前的組態。

您可以先備份目前使用 OpenSearch Dashboards 網頁介面或 OpenSearch API 建立的組態，以 `-backup` 選項執行 `securityadmin.sh` 工具，藉此防止組態被覆寫。這可確保在使用 `securityadmin.sh` 上傳修改後的組態之前，所有組態都已被擷取。

如需更多關於使用 `securityadmin.sh` 與管理 OpenSearch 安全性組態的詳細資訊，請參閱下列資源：
- [套用組態檔案變更]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)
- [修改 YAML 檔案]({{site.url}}{{site.baseurl}}/security/configuration/yaml/)

## 9. 替換所有預設密碼

使用示範組態初始化 OpenSearch 時，`internal_users.yml` 中會為內部使用者提供許多預設密碼，例如 `admin`、`kibanaserver` 與 `logstash`。

您應在啟動時或叢集開始執行後盡快將這些使用者的密碼更改為強式且複雜的密碼。建立密碼組態是一個簡單的程序，尤其是使用 OpenSearch 隨附的指令碼時，例如位於 `plugin/OpenSearch security/tools` 目錄中的 `hash.sh` 或 `hash.bat`。

`kibanaserver` 使用者是讓 OpenSearch Dashboards 與 OpenSearch 叢集通訊的重要元件。預設情況下，此使用者在示範組態中已預先設定預設密碼。您應在 OpenSearch 組態中將其替換為強式且唯一的密碼，並更新 `opensearch_dashboards.yml` 檔案以反映此變更。


## 10. 尋求協助

如果您需要更多協助，可以執行下列操作：

- 在 GitHub 的 [OpenSearch-project/security](https://github.com/opensearch-project/security/security) 或 [OpenSearch-project/OpenSearch](https://github.com/opensearch-project/OpenSearch/security) 建立議題。
- 在 [OpenSearch 論壇](https://forum.opensearch.org/tag/cve)提出問題。
