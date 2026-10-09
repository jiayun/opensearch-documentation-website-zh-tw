---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理密碼"
parent: Configuration
nav_order: 12
---

# 管理密碼

執行 Security 外掛程式的叢集會使用數個不同的密碼。每個密碼由不同的人設定、儲存在不同的位置，並透過不同的程序變更，因此任何密碼任務的第一步，就是確認您正在處理的是哪一個密碼。

下表列出 OpenSearch 叢集中的密碼。

| 密碼 | 由誰設定 | 儲存位置 |
| :--- | :--- | :--- |
| [管理員密碼](#admin-password) | 安裝 OpenSearch 的人 | `.opendistro_security` 索引，由 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 環境變數初始化 |
| [內部使用者密碼](#internal-user-passwords) | 叢集管理員 | `.opendistro_security` 索引 |
| [您自己的密碼](#your-own-password) | 擁有該帳戶的使用者 | `.opendistro_security` 索引 |
| [Dashboards 服務帳戶密碼](#dashboards-service-account-password) | 設定 OpenSearch Dashboards 的人 | `opensearch_dashboards.yml` 中的 `opensearch.password` 設定 |
| [Keystore 與 truststore 密碼](#keystore-and-truststore-passwords) | 設定 TLS 的人 | OpenSearch keystore |

由外部後端 (例如 LDAP 或 Active Directory) 驗證的使用者，其密碼是在該後端中管理，而不是在 OpenSearch 中管理。如需更多資訊，請參閱[驗證後端]({{site.url}}{{site.baseurl}}/security/authentication-backends/authc-index/)。

`OPENSEARCH_PASSWORD` 環境變數不是 OpenSearch 設定。用戶端與工具 (例如 [Reporting CLI]({{site.url}}{{site.baseurl}}/reporting/rep-cli-options/)) 會讀取它，以取得連線至叢集時所使用的認證。
{: .note}

## 管理員密碼

`admin` 使用者是由安全性示範組態建立，並具有叢集的完整存取權。其密碼會在安裝示範組態時透過環境變數設定一次，之後若要變更則需要不同的程序。

沒有預設的管理員密碼。除非您提供一個，否則叢集不會啟動，而且舊版本所使用的 `admin:admin` 認證已不再有效。

### 設定初始管理員密碼

新的叢集必須先有自訂的管理員密碼，才能安裝安全性示範組態。請在第一次啟動前設定 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 環境變數：

```bash
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
```
{% include copy.html %}

此變數會由示範組態安裝程式讀取一次，並成為 `admin` 使用者的密碼。它對之後的啟動沒有影響，也不適用於已設定 `opensearch.yml` 檔案的叢集，因為安裝程式不會在現有叢集上執行。設定此變數的語法因發行版而異。如需更多資訊，請參閱[設定示範組態]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#installing-the-demo-configuration)。

如果密碼不符合[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)，安裝會失敗，且叢集不會啟動。

### 變更管理員密碼

安裝之後，管理員密碼就無法再透過 REST API 或 OpenSearch Dashboards 變更，因為示範組態會將 `admin` 使用者標示為[保留]({{site.url}}{{site.baseurl}}/security/access-control/api/#reserved-and-hidden-resources)。再次設定 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 也沒有作用。若要重設管理員密碼，請依照下列步驟：

1. 為新密碼產生密碼雜湊：

   ```bash
   ./plugins/opensearch-security/tools/hash.sh -p <new-password>
   ```
   {% include copy.html %}

1. 將 `<OPENSEARCH_HOME>/config/opensearch-security/internal_users.yml` 中 `admin` 使用者的 `hash` 值取代為產生的雜湊。

1. 將檔案載入 `.opendistro_security` 索引：

   ```bash
   ./plugins/opensearch-security/tools/securityadmin.sh \
     -f ../../../config/opensearch-security/internal_users.yml \
     -t internalusers \
     -icl -nhnv \
     -cacert ../../../config/root-ca.pem \
     -cert ../../../config/kirk.pem \
     -key ../../../config/kirk-key.pem
   ```
   {% include copy.html %}

`-f` 與 `-t` 引數會將作業限制在內部使用者，這會保留透過 REST API 建立的角色與角色對應。任何透過 REST API 建立的內部使用者都會被覆寫。如需更多資訊，請參閱[將變更套用至組態檔案]({{site.url}}{{site.baseurl}}/security/configuration/security-admin/)。

## 內部使用者密碼

管理員會在建立或更新內部使用者時設定該使用者的密碼。請使用下列任一方法：

- 在 OpenSearch Dashboards 中建立使用者，系統會提示您輸入密碼。如需更多資訊，請參閱[定義使用者]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#defining-users)。
- 在 REST API 請求的 `password` 欄位中傳送純文字密碼。Security 外掛程式會在儲存前將密碼雜湊。如需更多資訊，請參閱[建立或更新使用者 API]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。
- 將 `hash.sh` 產生的 `bcrypt` 雜湊新增至 `internal_users.yml`，並執行 `securityadmin.sh` 以載入檔案。請將此方法保留給叢集的初始設定使用。如需更多資訊，請參閱 [internal_users.yml]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#internal_usersyml)。

透過 OpenSearch Dashboards 或 REST API 設定的密碼，會依據 `opensearch.yml` 中的[密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#password-settings)進行驗證。直接寫入 `internal_users.yml` 的雜湊會略過該驗證。

## 您自己的密碼

任何已驗證的使用者都可以在不需要管理員介入的情況下變更自己的密碼，只要同時提供目前密碼與新密碼即可：

```json
PUT /_plugins/_security/api/account
{
  "current_password": "<old-password>",
  "password": "<new-password>"
}
```
{% include copy-curl.html security=true %}

如需更多資訊，請參閱[變更密碼 API]({{site.url}}{{site.baseurl}}/security/api/account/change-password/)。

## Dashboards 服務帳戶密碼

OpenSearch Dashboards 會以內部使用者身分向 OpenSearch 進行驗證，並透過 `opensearch_dashboards.yml` 中的 `opensearch.username` 與 `opensearch.password` 設定進行設定。示範組態會使用 `kibanaserver` 使用者來達成此目的。變更此密碼需要兩個步驟：先在 OpenSearch 中更新 `kibanaserver` 使用者的密碼，然後在 `opensearch_dashboards.yml` 中設定相符的值，並重新啟動 OpenSearch Dashboards。

這是服務帳戶，而不是登入帳戶。終端使用者會以自己的認證登入 OpenSearch Dashboards。如需更多資訊，請參閱[設定登入選項]({{site.url}}{{site.baseurl}}/security/configuration/multi-auth/)。

## Keystore 與 truststore 密碼

Keystore 與 truststore 密碼會保護 TLS 憑證存放區，與使用者驗證無關。請將它們儲存在 OpenSearch keystore 中，而不是儲存在 `opensearch.yml` 中。如需更多資訊，請參閱 [OpenSearch keystore]({{site.url}}{{site.baseurl}}/security/configuration/opensearch-keystore/) 與[設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。

## 示範組態密碼

除了 `admin` 使用者之外，示範組態還會建立 `kibanaserver`、`kibanaro`、`logstash`、`readall` 與 `snapshotrestore` 使用者。只有 `admin` 密碼來自 `OPENSEARCH_INITIAL_ADMIN_PASSWORD`。其他使用者會保留 `internal_users.yml` 中公布的預設密碼，因此其認證是公開資訊。

在將叢集移入正式環境之前，請變更您保留的每個示範使用者密碼，並刪除您不需要的使用者。示範憑證同樣不適合用於正式環境。如需更多資訊，請參閱[最佳實務]({{site.url}}{{site.baseurl}}/security/configuration/best-practices/)。
{: .warning}

## 密碼需求

視密碼的設定方式而定，會套用兩組獨立的規則。只有第二組是可設定的密碼原則：

- 初始管理員密碼會依據示範組態安裝程式內建的規則進行檢查，這些規則無法變更。如需更多資訊，請參閱[管理員密碼需求]({{site.url}}{{site.baseurl}}/security/configuration/demo-configuration/#admin-password-requirements)。
- 透過 OpenSearch Dashboards 或 REST API 設定的密碼，會依據 `plugins.security.restapi.password_validation_regex`、`plugins.security.restapi.password_min_length` 與 `plugins.security.restapi.password_score_based_validation_strength` 進行檢查。如需更多資訊，請參閱[密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#password-settings)。

兩組規則都使用 [`zxcvbn`](https://github.com/dropbox/zxcvbn) 強度估算器，它會依據熵為密碼評分。常見的單字、日期、`1234` 或 `qwerty` 等序列，以及 `3` 取代 `E` 這類可預測的替換，都會降低分數，而長度與不可預測性則會提高分數。即使密碼符合所有字元規則，仍可能因強度不足而被拒絕。若要檢查密碼的分數，請使用 [`zxcvbn` 示範](https://lowe.github.io/tryzxcvbn)。
