---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Active Directory 與 LDAP"
parent: Authentication backends
nav_order: 60
redirect_from:
  - /security/configuration/ldap/
  - /security-plugin/configuration/ldap/
---

# Active Directory 與 LDAP

Active Directory 與 LDAP 可同時用於驗證和授權（分別對應組態中的 `authc` 和 `authz` 區段）。驗證會檢查使用者是否輸入了有效的認證資訊。授權則會擷取使用者的所有後端角色。

在大多數情況下，您會想要同時設定驗證和授權。您也可以只使用驗證，並將從 LDAP 擷取的使用者直接對應至 Security 外掛程式角色。


## Docker 範例

我們提供了一個功能完整的範例，可協助您了解如何使用 LDAP 伺服器同時進行驗證和授權。

1. 下載並解壓縮[範例 zip 檔案]({{site.url}}{{site.baseurl}}/assets/examples/ldap-example-v2.13.zip)。
1. 在 `.env` 檔案中，為 `admin` 使用者更新為高強度密碼。
1. 在命令列中執行 `docker compose up`。
1. 檢閱以下檔案：

   * `docker-compose.yml` 定義了單一 OpenSearch 節點、一個 LDAP 伺服器，以及一個用於 LDAP 伺服器的 PHP 管理工具。

     您可以透過 https://localhost:6443 存取管理工具。確認安全性警告後，使用 `cn=admin,dc=example,dc=org` 和 `changethis` 登入。

   * `directory.ldif` 會在 LDAP 伺服器中預先建立三個使用者和兩個群組。

     `psantos` 屬於 `Administrator` 和 `Developers` 群組。`jroe` 和 `jdoe` 屬於 `Developers` 群組。Security 外掛程式會將這些群組載入為後端角色。

   * `roles_mapping.yml` 會將 `Administrator` 和 `Developers` LDAP 群組（作為後端角色）對應至安全性角色，讓使用者在通過驗證後取得適當的權限。

   * `internal_users.yml` 會移除 `administrator` 和 `kibanaserver` 以外的所有預設使用者。

   * `config.yml` 包含所有必要的 LDAP 設定。

1. 以 `psantos` 身分將文件編製索引：

   ```bash
   curl -XPUT 'https://localhost:9200/new-index/_doc/1' -H 'Content-Type: application/json' -d '{"title": "Spirited Away"}' -u 'psantos:password' -k
   ```

   如果您以 `jroe` 身分嘗試相同的請求，請求會失敗。`Developers` 群組對應至 `readall`、`manage_snapshots` 和 `kibana_user` 角色，不具備寫入權限。

1. 以 `jroe` 身分搜尋該文件：

   ```bash
   curl -XGET 'https://localhost:9200/new-index/_search?pretty' -u 'jroe:password' -k
   ```

   此請求會成功，因為 `Developers` 群組對應至 `readall` 角色。

1. 如果您想檢查各個容器的內容，請執行 `docker ps` 找出容器 ID，然後執行 `docker exec -it <container-id> /bin/bash`。


## 連線設定

若要啟用 LDAP 驗證和授權，請將下列幾行新增至 `config/opensearch-security/config.yml`：

由於 OpenSearch Dashboards 會使用 `kibanaserver` 內部使用者連線至 OpenSearch，因此也應啟用內部使用者資料庫驗證。
{: .note}

```yml
authc:
  internal_auth:
    order: 0
    description: "HTTP basic authentication using the internal user database"
    http_enabled: true
    transport_enabled: true
    http_authenticator:
      type: basic
      challenge: false
    authentication_backend:
      type: internal
  ldap:
    http_enabled: true
    transport_enabled: true
    order: 1
    http_authenticator:
      type: basic
      challenge: false
    authentication_backend:
      type: ldap
      config:
        ...
```

```yml
authz:
  ldap:
    http_enabled: true
    transport_enabled: true
    authorization_backend:
      type: ldap
      config:
      ...
```

驗證和授權的連線設定完全相同，並新增至 `config` 區段中。


### 主機名稱與連接埠

若要設定 Active Directory 伺服器的主機名稱和連接埠，請使用下列設定：

```yml
config:
  hosts:
    - primary.ldap.example.com:389
    - secondary.ldap.example.com:389
```

您可以在此設定多個伺服器。如果 Security 外掛程式無法連線至第一個伺服器，會依序嘗試連線至其餘伺服器。


### LDAP 轉介

LDAP 轉介 (referral) 會將用戶端導向另一個目錄位置以繼續查詢。根據預設，Security 外掛程式會在 LDAP 搜尋和查詢期間追蹤轉介。若要停用此行為，請將 `follow_referrals` 設為 `false`：

```yml
config:
  follow_referrals: false
```

視需要將此設定新增至 `authc` 下的 LDAP `authentication_backend.config` 區段，以及 `authz` 下的 LDAP `authorization_backend.config` 區段。每個後端會讀取各自的設定。若要同時針對驗證和授權停用轉介追蹤，請設定這兩個區段。

停用轉介追蹤時，可能會找不到僅能透過轉介取得的使用者或角色。此設定不會停用 `hosts` 中所列伺服器之間的容錯移轉。

### 逾時

若要設定與 Active Directory 伺服器的連線逾時和回應逾時，請使用下列設定（數值單位為毫秒）：

```yml
config:
  connect_timeout: 5000
  response_timeout: 0
```

如果您的伺服器支援雙重驗證 (2FA)，預設的逾時設定可能會導致登入錯誤。您可以增加 `connect_timeout` 以配合 2FA 流程。將 `response_timeout` 設為 0（預設值）表示無限期等待。


### 繫結 DN 與密碼

若要設定 Security 外掛程式向伺服器發出查詢時所使用的 `bind_dn` 和 `password`，請使用下列設定：

```yml
config:
  bind_dn: cn=admin,dc=example,dc=com
  password: password
```

如果您的伺服器支援匿名驗證，可將 `bind_dn` 和 `password` 都設為 `null`。


### TLS 設定

使用下列參數設定連線至伺服器時的 TLS：

```yml
config:
  enable_ssl: <true|false>
  enable_start_tls: <true|false>
  enable_ssl_client_auth: <true|false>
  verify_hostnames: <true|false>
```

名稱 | 說明
:--- | :---
`enable_ssl` | 是否使用 LDAP over SSL (LDAPS)。
`enable_start_tls` | 是否使用 STARTTLS。無法與 LDAPS 搭配使用。
`enable_ssl_client_auth` | 是否將用戶端憑證傳送至 LDAP 伺服器。
`verify_hostnames` | 是否驗證伺服器 TLS 憑證的主機名稱。


### 憑證驗證

根據預設，Security 外掛程式會根據 `opensearch.yml` 中設定的根 CA（PEM 憑證或信任存放區）驗證 LDAP 伺服器的 TLS 憑證：

```
plugins.security.ssl.transport.pemtrustedcas_filepath: ...
plugins.security.ssl.transport.truststore_filepath: ...
```

如果您的伺服器使用由其他 CA 簽署的憑證，請將該 CA 匯入您的信任存放區，或在每個節點上將其新增至您的受信任 CA 檔案。

您也可以使用另一個 PEM 格式的獨立根 CA。

為 LDAP 設定獨立的根 CA 時，請務必在所有 LDAP `config:` 設定中加入此設定，包括組態中的 `authc` 和 `authz` 選項。
{: .note}

若要設定獨立的根 CA，請使用下列其中一個組態選項：

```yml
config:
  pemtrustedcas_filepath: /full/path/to/trusted_cas.pem
```

```yml
config:
  pemtrustedcas_content: |-
    -----BEGIN CERTIFICATE-----
    MIID/jCCAuagAwIBAgIBATANBgkqhkiG9w0BAQUFADCBjzETMBEGCgmSJomT8ixk
    ARkWA2NvbTEXMBUGCgmSJomT8ixkARkWB2V4YW1wbGUxGTAXBgNVBAoMEEV4YW1w
    bGUgQ29tIEluYy4xITAfBgNVBAsMGEV4YW1wbGUgQ29tIEluYy4gUm9vdCBDQTEh
    ...
    -----END CERTIFICATE-----
```


名稱 | 說明
:--- | :---
`pemtrustedcas_filepath` | 包含 Active Directory/LDAP 伺服器根 CA 的 PEM 檔案絕對路徑。
`pemtrustedcas_content` | Active Directory/LDAP 伺服器的根 CA 內容。設定 `pemtrustedcas_filepath` 時無法使用。


### 用戶端驗證

如果您使用 TLS 用戶端驗證，Security 外掛程式會傳送節點的 PEM 憑證，其設定方式如 `opensearch.yml` 中所設定。請設定下列其中一個組態選項：

```yml
config:
  pemkey_filepath: /full/path/to/private.key.pem
  pemkey_password: private_key_password
  pemcert_filepath: /full/path/to/certificate.pem
```

或

```yml
config:
  pemkey_content: |-
    -----BEGIN PRIVATE KEY-----
    MIID2jCCAsKgAwIBAgIBBTANBgkqhkiG9w0BAQUFADCBlTETMBEGCgmSJomT8ixk
    ARkWA2NvbTEXMBUGCgmSJomT8ixkARkWB2V4YW1wbGUxGTAXBgNVBAoMEEV4YW1w
    bGUgQ29tIEluYy4xJDAiBgNVBAsMG0V4YW1wbGUgQ29tIEluYy4gU2lnbmluZyBD
    ...
    -----END PRIVATE KEY-----
  pemkey_password: private_key_password
  pemcert_content: |-
    -----BEGIN CERTIFICATE-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCHRZwzwGlP2FvL
    oEzNeDu2XnOF+ram7rWPT6fxI+JJr3SDz1mSzixTeHq82P5A7RLdMULfQFMfQPfr
    WXgB4qfisuDSt+CPocZRfUqqhGlMG2l8LgJMr58tn0AHvauvNTeiGlyXy0ShxHbD
    ...
    -----END CERTIFICATE-----
```

名稱 | 說明
:--- | :---
`pemkey_filepath` | 包含您憑證私密金鑰之檔案的絕對路徑。
`pemkey_content` | 您憑證私密金鑰的內容。設定 `pemkey_filepath` 時無法使用。
`pemkey_password` | 您私密金鑰的密碼 (若有)。
`pemcert_filepath` | 用戶端憑證的絕對路徑。
`pemcert_content` | 用戶端憑證的內容。設定 `pemcert_filepath` 時無法使用。


### 啟用的加密套件與通訊協定

您可以限制 LDAP 連線允許使用的加密套件與 TLS 通訊協定。例如，您可以只允許強式加密套件，並將 TLS 版本限制為最新的版本：

```yml
ldap:
  http_enabled: true
  transport_enabled: true
  ...
  authentication_backend:
    type: ldap
    config:
      enabled_ssl_ciphers:
        - "TLS_DHE_RSA_WITH_AES_256_CBC_SHA"
        - "TLS_DHE_DSS_WITH_AES_128_CBC_SHA256"
      enabled_ssl_protocols:
        - "TLSv1.1"
        - "TLSv1.2"
```

名稱 | 說明
:--- | :---
`enabled_ssl_ciphers` | 陣列，啟用的 TLS 加密套件。僅支援 Java 格式。
`enabled_ssl_protocols` | 陣列，啟用的 TLS 通訊協定。僅支援 Java 格式。


---

## 使用 Active Directory 與 LDAP 進行驗證

若要使用 Active Directory/LDAP 進行驗證，請先在 `config/opensearch-security/config.yml` 的 `authc` 區段中設定對應的驗證網域：

```yml
authc:
  ldap:
    http_enabled: true
    transport_enabled: true
    order: 1
    http_authenticator:
      type: basic
      challenge: true
    authentication_backend:
      type: ldap
      config:
        ...
```

接著，將 Active Directory/LDAP 伺服器的[連線設定](#connection-settings)新增至驗證網域的 config 區段：

```yml
config:
  enable_ssl: true
  enable_start_tls: false
  enable_ssl_client_auth: false
  verify_hostnames: true
  hosts:
    - ldap.example.com:8389
  bind_dn: cn=admin,dc=example,dc=com
  password: passw0rd
```

驗證的運作方式是對 LDAP 樹狀結構的使用者子樹發出包含使用者名稱的 LDAP 查詢。

Security 外掛程式會先取得已設定的 LDAP 查詢，並將預留位置 `{0}` 取代為使用者憑證中的使用者名稱。

```yml
usersearch: '(sAMAccountName={0})'
```

接著，它會對使用者子樹發出此查詢。目前會搜尋已設定之 `userbase` 下的整個子樹：

```yml
userbase: 'ou=people,dc=example,dc=com'
```

如果查詢成功，Security 外掛程式會從 LDAP 項目擷取使用者名稱。您可以指定 Security 外掛程式應使用 LDAP 項目中的哪個屬性作為使用者名稱：

```yml
username_attribute: uid
```

如果未設定此索引鍵或設為 null，則會使用 LDAP 項目的辨別名稱 (DN)。


### 組態摘要

名稱 | 說明
:--- | :---
`userbase` | 指定目錄中儲存使用者資訊的子樹。
`follow_referrals` | 布林值。搜尋與查閱期間是否要遵循 LDAP 轉介。預設為 `true`。請參閱 [LDAP 轉介](#ldap-referrals)。
`usersearch` | Security 外掛程式在嘗試驗證使用者時所執行的實際 LDAP 查詢。變數 {0} 會取代為使用者名稱。
`username_attribute` | Security 外掛程式會使用目錄項目的此屬性來尋找使用者名稱。若設為 null，則會使用 DN (預設)。


### 完整驗證範例

```yml
ldap:
  http_enabled: true
  transport_enabled: true
  order: 1
  http_authenticator:
    type: basic
    challenge: true
  authentication_backend:
    type: ldap
    config:
      enable_ssl: true
      enable_start_tls: false
      enable_ssl_client_auth: false
      verify_hostnames: true
      hosts:
        - ldap.example.com:636
      bind_dn: cn=admin,dc=example,dc=com
      password: password
      userbase: 'ou=people,dc=example,dc=com'
      usersearch: '(sAMAccountName={0})'
      username_attribute: uid
```


---

## 使用 Active Directory 與 LDAP 進行授權

若要使用 Active Directory/LDAP 進行授權，請先在 `config.yml` 的 `authz` 區段中設定對應的授權網域：

```yml
authz:
  ldap:
    http_enabled: true
    transport_enabled: true
    authorization_backend:
      type: ldap
      config:
      ...
```

授權是從 LDAP 伺服器為已驗證使用者擷取後端角色的程序。這通常是您用於驗證的相同伺服器，但您也可以使用不同的伺服器。唯一的要求是您用來擷取角色的使用者必須確實存在於 LDAP 伺服器上。

由於 Security 外掛程式一律會檢查使用者是否存在於 LDAP 伺服器，因此您也必須在 `authz` 區段中設定 `userbase`、`usersearch` 與 `username_attribute`。

授權的運作方式與驗證類似。Security 外掛程式會對 LDAP 樹狀結構的角色子樹發出包含使用者名稱的 LDAP 查詢。

或者，Security 外掛程式也可以擷取在使用者子樹中定義為使用者項目直接屬性的角色。


### 方法 1：查詢角色子樹

Security 外掛程式會先取得用於擷取角色的 LDAP 查詢 (`rolesearch`)，並取代查詢中找到的任何變數。例如，對於標準的 Active Directory 安裝，您會使用下列角色搜尋：

```yml
rolesearch: '(member={0})'
```

您可以使用下列變數：

- `{0}` 會取代為使用者的 DN。
- `{1}` 會取代為使用者名稱，其定義方式如 `username_attribute` 設定所定義。
- `{2}` 會取代為已驗證使用者目錄項目中的任意屬性值。

變數 `{2}` 指的是使用者目錄項目中的屬性。您應使用的屬性由 `userroleattribute` 設定所指定：

```yml
userroleattribute: myattribute
```

接著，Security 外掛程式會對已設定的角色子樹發出取代後的查詢。會搜尋 `rolebase` 下的整個子樹：

```yml
rolebase: 'ou=groups,dc=example,dc=com'
```

如果您使用巢狀角色 (屬於其他角色成員的角色)，您可以設定 Security 外掛程式來解析它們：

```yml
resolve_nested_roles: false
```

擷取所有角色之後，Security 外掛程式會從角色項目的可設定屬性中擷取最終角色名稱：

```yml
rolename: cn
```

如果未設定此項，則會使用角色項目的 DN。您現在可以使用此角色名稱，將其對應至 `roles_mapping.yml` 中定義的一或多個 Security 外掛程式角色。


### 方法 2：使用使用者的屬性作為角色名稱

如果您將角色儲存為使用者子樹中使用者項目的直接屬性，則只需設定屬性名稱：

```yml
userrolename: roles
```

您可以設定多個屬性名稱：

```yml
userrolename: roles, otherroles
```

此方法可以與查詢角色子樹結合使用。Security 外掛程式會從使用者的角色屬性取得角色，然後執行角色搜尋。

如果您不使用或沒有角色子樹，可以完全停用角色搜尋：

```yml
rolesearch_enabled: false
```


### (進階) 控制 LDAP 使用者屬性

預設情況下，Security 外掛程式會讀取所有 LDAP 使用者屬性，並將其提供給索引名稱變數替換和 DLS 查詢變數替換使用。如果您的 LDAP 項目有大量屬性，您可能會想控制哪些屬性應該開放使用。屬性越少，效能越好。

請注意，此設定是在 config.yml 檔案的驗證 `authc` 區段中進行。

名稱 | 說明
:--- | :---
`custom_attr_allowlist`  | 字串陣列。指定應開放供變數替換使用的 LDAP 屬性。
`custom_attr_maxval_len`  | 整數。指定每個屬性允許的最大長度。所有超過此值的屬性都會被捨棄。值為 `0` 時會完全停用自訂屬性。預設為 36。

範例：

```yml
authc:
  ldap:
    http_enabled: true
    transport_enabled: true
    authentication_backend:
      type: ldap
      config:
        custom_attr_allowlist:
          - attribute1
          - attribute2
        custom_attr_maxval_len: 36
      ...
```


### (進階) 將特定使用者排除在角色查詢之外

如果您使用多種驗證方法，將某些使用者排除在 LDAP 角色查詢之外可能會有意義。

請考慮典型 OpenSearch Dashboards 設定的以下情境：所有 OpenSearch Dashboards 使用者都儲存在 LDAP/Active Directory 伺服器中。

然而，您還有一個 OpenSearch Dashboards 伺服器使用者。OpenSearch Dashboards 使用此使用者來管理已儲存的物件，並執行監視與維護工作。您不會想將此使用者加入您的 Active Directory 安裝，而是將其儲存在 Security 外掛程式的內部使用者資料庫中。

在這種情況下，將 OpenSearch Dashboards 伺服器使用者排除在 LDAP 授權之外是合理的，因為我們已經知道沒有對應的項目。您可以使用 `skip_users` 組態設定來定義應略過哪些使用者。支援萬用字元和規則運算式：

```yml
skip_users:
  - kibanaserver
  - 'cn=Jane Doe,ou*people,o=TEST'
  - '/\S*/'
```


### (進階) 將角色排除在巢狀角色查詢之外

如果您的 LDAP 安裝中的使用者擁有大量角色，而且您還需要解析巢狀角色，可能會遇到效能問題。

不過在大多數情況下，並非所有使用者角色都與 OpenSearch 和 OpenSearch Dashboards 相關。您可能只需要少數幾個角色。在這種情況下，您可以使用巢狀角色篩選功能來定義一份角色清單，將其從使用者的角色清單中篩除。支援萬用字元和規則運算式。

此功能僅在 `resolve_nested_roles` 為 `true` 時有效：

```yml
nested_role_filter:
  - 'cn=Jane Doe,ou*people,o=TEST'
  - ...
```


### 組態摘要

名稱 | 說明
:--- | :---
`rolebase`  | 指定目錄中儲存角色/群組資訊的子樹。
`follow_referrals` | 布林值。搜尋與查詢時是否遵循 LDAP 轉介。預設為 `true`。請參閱 [LDAP 轉介](#ldap-referrals)。
`rolesearch` | Security 外掛程式在嘗試判斷使用者角色時執行的實際 LDAP 查詢。您可以在這裡使用三個變數（請參閱以下說明）。
`userroleattribute`  | 使用者項目中用於 `{2}` 變數替換的屬性。
`userrolename`  | 如果使用者的角色/群組不是儲存在群組子樹中，而是作為使用者目錄項目的屬性，請在此定義此屬性名稱。
`rolename`  | 應用作角色名稱的角色項目屬性。
`resolve_nested_roles`  | 布林值。是否解析巢狀角色。預設為 `false`。
`max_nested_depth`  | 整數。當 `resolve_nested_roles` 為 `true` 時，此設定定義可遍訪的巢狀角色數量上限。設定較小的值可以減少從 LDAP 擷取的資料量並改善驗證時間，代價是無法發現深層巢狀的角色。預設為 `30`。
`skip_users`  | 擷取角色時應略過的使用者陣列。支援萬用字元和規則運算式。
`exclude_roles`  | 擷取角色時應排除的角色陣列。支援萬用字元。
`nested_role_filter`  | 解析巢狀角色之前應篩除的角色 DN 陣列。支援萬用字元和規則運算式。
`rolesearch_enabled`  | 布林值。啟用或停用角色搜尋。預設為 `true`。
`custom_attr_allowlist`  | 字串陣列。指定應開放供變數替換使用的 LDAP 屬性。
`custom_attr_maxval_len`  | 整數。指定每個屬性允許的最大長度。所有超過此值的屬性都會被捨棄。值為 `0` 時會完全停用自訂屬性。預設為 36。
`custom_return_attributes`  | 字串陣列。指定要向 LDAP 伺服器請求的屬性。


### 完整授權範例

```yml
authz:
  ldap:
    http_enabled: true
    transport_enabled: true
    authorization_backend:
      type: ldap
      config:
        enable_ssl: true
        enable_start_tls: false
        enable_ssl_client_auth: false
        verify_hostnames: true
        hosts:
          - ldap.example.com:636
        bind_dn: cn=admin,dc=example,dc=com
        password: password
        userbase: 'ou=people,dc=example,dc=com'
        usersearch: '(uid={0})'
        username_attribute: uid
        rolebase: 'ou=groups,dc=example,dc=com'
        rolesearch: '(member={0})'
        userroleattribute: null
        userrolename: none
        rolename: cn
        resolve_nested_roles: true
        skip_users:
          - kibanaserver
          - 'cn=Jane Doe,ou*people,o=TEST'
          - '/\S*/'
```

### (進階) 設定多個使用者和角色基準

若要在 `authc` 和/或 `authz` 區段中設定多個使用者基準，請使用以下語法：

```yml
        ...
        bind_dn: cn=admin,dc=example,dc=com
        password: password
        users:
          primary-userbase:
             base: 'ou=people,dc=example,dc=com'
             search: '(uid={0})'
          secondary-userbase:
             base: 'cn=users,dc=example,dc=com'
             search: '(uid={0})'
        username_attribute: uid
        ...
```

同樣地，若要在 `authz` 區段中設定多個角色基準，請使用以下設定：

```yml
        ...
        username_attribute: uid
        roles:
          primary-rolebase:
            base: 'ou=groups,dc=example,dc=com'
            search: '(uniqueMember={0})'
          secondary-rolebase:
            base: 'ou=othergroups,dc=example,dc=com'
            search: '(member={0})'
        userroleattribute: null
        ...
```

### 使用多個使用者與角色基底進行完整驗證與授權的範例：

```yml
authc:
  ...
  ldap:
    http_enabled: true
    transport_enabled: true
    order: 1
    http_authenticator:
      type: basic
      challenge: true
    authentication_backend:
      type: ldap
      config:
        enable_ssl: true
        enable_start_tls: false
        enable_ssl_client_auth: false
        verify_hostnames: true
        hosts:
          - ldap.example.com:636
        bind_dn: cn=admin,dc=example,dc=com
        password: password
        users:
          primary-userbase:
             base: 'ou=people,dc=example,dc=com'
             search: '(uid={0})'
          secondary-userbase:
             base: 'cn=users,dc=example,dc=com'
             search: '(uid={0})'
        username_attribute: uid
authz:
  ldap:
    http_enabled: true
    transport_enabled: true
    authorization_backend:
      type: ldap
      config:
        enable_ssl: true
        enable_start_tls: false
        enable_ssl_client_auth: false
        verify_hostnames: true
        hosts:
          - ldap.example.com:636
        bind_dn: cn=admin,dc=example,dc=com
        password: password
        users:
          primary-userbase:
             base: 'ou=people,dc=example,dc=com'
             search: '(uid={0})'
          secondary-userbase:
             base: 'cn=users,dc=example,dc=com'
             search: '(uid={0})'
        username_attribute: uid
        roles:
          primary-rolebase:
            base: 'ou=groups,dc=example,dc=com'
            search: '(uniqueMember={0})'
          secondary-rolebase:
            base: 'ou=othergroups,dc=example,dc=com'
            search: '(member={0})'
        userroleattribute: null
        userrolename: none
        rolename: cn
        resolve_nested_roles: true
```
