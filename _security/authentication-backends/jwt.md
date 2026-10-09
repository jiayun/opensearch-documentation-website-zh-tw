---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: JSON Web Token
parent: Authentication backends
nav_order: 47
redirect_from:
---


# JSON Web Token 驗證

JSON Web Token (JWT) 是以 JSON 為基礎的存取權杖，用來主張一或多項宣告。它們常用於實作單一登入 (SSO) 解決方案，屬於權杖型驗證系統的一類。JWT 的基本資訊傳輸與身分驗證生命週期如下列步驟所述：

1. 使用者提供憑證（例如使用者名稱與密碼）登入驗證伺服器。
1. 驗證伺服器驗證該憑證。
1. 驗證伺服器建立存取權杖並加以簽署。
1. 驗證伺服器將權杖傳回給使用者。
1. 使用者儲存該存取權杖。
1. 使用者在每次向想使用的服務發出請求時，都隨附該存取權杖。
1. 服務驗證權杖並准許或拒絕存取。
1. 取得存取授權後，使用者即可存取，直到權杖的到期時間為止。到期時間通常由簽發者在權杖的承載中設定。

JWT 是自包含的，也就是說它本身攜帶驗證使用者所需的全部資訊。這些權杖是經過 Base64 編碼並簽署的 JSON 物件。


## JWT 元素

JWT 由三個部分組成：

* 標頭
* 承載
* 簽章


### 標頭

標頭包含所用簽署機制的相關資訊，包括編碼權杖所用的演算法。下列範例顯示標頭的典型屬性與值：

```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

在此範例中，標頭指出訊息是使用雜湊演算法 HMAC-SHA256 簽署的。


### 承載

JWT 的承載包含 [JWT 宣告](https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims)。宣告是關於權杖使用者的一段資訊，可作為唯一識別碼，讓權杖的簽發者能夠驗證身分。宣告是名稱-值對，承載通常包含多個宣告。雖然新增宣告的選項很多，但良好的做法是避免加入過多宣告而使承載過於龐大，否則會失去 JWT 精簡的目的。

宣告有三種類型：

* [註冊宣告](https://www.iana.org/assignments/jwt/jwt.xhtml#claims)由 JWT 規格定義，是一組具有保留名稱的標準宣告。例如權杖簽發者 (`iss`)、到期時間 (`exp`) 與主體 (`sub`)。
* 公開宣告則由共用權杖的各方自行定義。它們可以包含任意資訊，例如使用者名稱與使用者的角色。為求謹慎，規格建議註冊該名稱，或至少確保該名稱與其他宣告[不易衝突](https://www.rfc-editor.org/rfc/rfc7519#section-4.2)。
* 私人宣告提供另一種將自訂資訊加入承載的方式，例如電子郵件地址。因此它們也稱為_自訂_宣告。共用權杖的雙方必須就其用法達成共識，因為它們既不屬於註冊宣告，也不屬於公開宣告。

下列範例以名稱-值對的形式顯示這些 JSON 屬性：

```json
{
  "iss": "example.com",
  "exp": 1300819380,
  "name": "John Doe",
  "roles": "admin, devops"
}
```

### 簽章

權杖的簽發者透過對 Base64 編碼的標頭與承載套用密碼學雜湊函式來產生權杖的簽章。接收 JWT 的用戶端會在傳輸的最後一步解密並驗證此簽章。

這三個部分---標頭、承載與簽章---以句點串接，形成完整的 JWT：

```
encoded = base64UrlEncode(header) + "." + base64UrlEncode(payload)
signature = HMACSHA256(encoded, 'secretkey');
jwt = encoded + "." + base64UrlEncode(signature)
```

範例：
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJsb2dnZWRJbkFzIjoiYWRtaW4iLCJpYXQiOjE0MjI3Nzk2Mzh9.gzSraSYS8EXBxLN_oWnFSRgCzcmJmMjLiuyu5CSpyHI
```


## 設定 JWT

如果您使用 JWT 作為唯一的驗證方式，請將 `plugins.security.cache.ttl_minutes` 屬性設為 `0` 以停用使用者快取。關於此屬性的更多資訊，請參閱 [opensearch.yml]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#opensearchyml)。
{: .important }

建立一個驗證網域，並選擇 `jwt` 作為 HTTP 驗證類型。由於權杖已包含驗證請求所需的全部資訊，`challenge` 必須設為 `false`，`authentication_backend` 設為 `noop`：

```yml
jwt_auth_domain:
  http_enabled: true
  transport_enabled: true
  order: 0
  http_authenticator:
    type: jwt
    challenge: false
    config:
      signing_key: "base64 encoded key"
      jwt_header: "Authorization"
      jwt_url_parameter: null
      subject_key: null
      roles_key: null
      required_audience: null
      required_issuer: null
      jwt_clock_skew_tolerance_seconds: 20
  authentication_backend:
    type: noop
```

下表列出組態參數。

名稱 | 說明
:--- | :---
`signing_key` | 用於驗證權杖的簽署金鑰。若使用對稱金鑰演算法，此為 Base64 編碼的共用密鑰；若使用非對稱演算法，則包含公開金鑰。若要傳遞多個金鑰，請使用以逗號分隔的清單或逐一列舉金鑰。
`jwt_header` | 傳輸權杖的 HTTP 標頭。通常是帶有 `Bearer` 架構的 `Authorization` 標頭，`Authorization: Bearer <token>`。預設為 `Authorization`。若將此欄位替換為 `Authorization` 以外的值，會導致稽核記錄無法正確遮蔽稽核訊息中的 JWT 標頭。建議使用者在搭配稽核記錄使用 JWT 時，僅使用 `Authorization`。
`jwt_url_parameter` | 若權杖不是透過 HTTP 標頭傳輸，而是以 URL 參數傳輸，請在此定義參數名稱。
`subject_key` | JSON 承載中儲存使用者名稱的金鑰。若未設定，則使用[主體](https://tools.ietf.org/html/rfc7519#section-4.1.2)註冊宣告。若要從巢狀 JWT 宣告中擷取使用者名稱，可將 `subject_key` 設定為清單。
`roles_key` | JSON 承載中儲存使用者角色的金鑰。值必須是以逗號分隔的角色清單。可將 `roles_key` 設定為清單，以從巢狀 JWT 宣告中擷取角色。
`required_audience` | JWT 必須指定的對象名稱。可設定單一值（例如 `project1`）或多個以逗號分隔的值（例如 `project1,admin`）。若設定多個值，JWT 必須至少包含其中一個必要的對象。此參數對應於 [JWT 的 `aud` 宣告](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3)。
`required_issuer` | 儲存在 JSON 承載中的 JWT 目標簽發者。此對應於 [JWT 的 `iss` 宣告](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.1)。
`jwt_clock_skew_tolerance_seconds` | 設定一段以秒為單位的時間窗，用於補償 JWT 驗證伺服器與 OpenSearch 節點時鐘之間的任何差異，從而避免因時間不一致而導致驗證失敗。安全性功能預設為 30 秒。可使用此設定套用自訂值。

由於 JWT 是自包含的，且使用者已在 HTTP 層級完成驗證，因此不需要額外的 `authentication_backend`。請將此值設為 `noop`。


### 對稱金鑰演算法：HMAC

雜湊式訊息驗證碼 (HMAC) 是一組演算法，可透過共用金鑰為訊息簽章。此金鑰由驗證伺服器與 Security 外掛程式共用。您必須在 `signing_key` 設定中將其設定為 Base64 編碼值：

```yml
jwt_auth_domain:
  ...
    config:
      signing_key: "a3M5MjEwamRqOTAxOTJqZDE="
      ...
```


### 非對稱金鑰演算法：RSA 與 ECDSA

RSA 與 ECDSA 是使用公開/私密金鑰對來簽署及驗證權杖的非對稱加密與數位簽章演算法。這表示它們使用私密金鑰來簽署權杖，而 Security 外掛程式只需知道公開金鑰即可驗證權杖。

由於您無法使用公開金鑰簽發新權杖，且您可以對權杖的建立者做出有效的假設，因此 RSA 與 ECDSA 被認為比 HMAC 更安全。

若要使用 RS256，您只需在 JWT 組態中將 (未經 Base64 編碼的) 公開 RSA 金鑰設定為 `signing_key`：

```yml
jwt_auth_domain:
  ...
    config:
      signing_key: |-
        -----BEGIN PUBLIC KEY-----
        MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQK...
        -----END PUBLIC KEY-----
      ...
```

Security 外掛程式會自動偵測演算法 (RSA/ECDSA)。如有需要，您可以將金鑰分成多行。


### HTTP 請求的持有人驗證

在 HTTP 請求中傳輸 JWT 最常見的方式，是使用持有人驗證結構將其新增為 HTTP 標頭：

```
Authorization: Bearer <JWT>
```

標頭的預設名稱為 `Authorization`。若您的驗證伺服器或代理伺服器要求，您也可以使用 `jwt_header` 組態索引鍵來使用不同的 HTTP 標頭名稱。

如同 HTTP 基本驗證，在 HTTP 請求中傳輸 JWT 時，您應使用 HTTPS 而非 HTTP。


### HTTP 請求的查詢參數

雖然在 HTTP 請求中傳輸 JWT 最常見的方式是使用標頭欄位，但 Security 外掛程式也支援參數。請使用下列索引鍵設定 `GET` 參數的名稱：

```yml
    config:
      signing_key: ...
      jwt_url_parameter: "parameter_name"
      subject_key: ...
      roles_key: ...
```

如同 HTTP 基本驗證，您應使用 HTTPS 而非 HTTP。


### 經驗證的註冊宣告

下列註冊宣告會自動驗證：

* `iat` (Issued At) 宣告
* `nbf` (Not Before) 宣告
* `exp` (Expiration Time) 宣告


### 支援的格式與演算法

Security 外掛程式支援使用所有標準演算法進行數位簽章的精簡 JWT：

```
HS256: HMAC using SHA-256
HS384: HMAC using SHA-384
HS512: HMAC using SHA-512
RS256: RSASSA-PKCS-v1_5 using SHA-256
RS384: RSASSA-PKCS-v1_5 using SHA-384
RS512: RSASSA-PKCS-v1_5 using SHA-512
PS256: RSASSA-PSS using SHA-256 and MGF1 with SHA-256
PS384: RSASSA-PSS using SHA-384 and MGF1 with SHA-384
PS512: RSASSA-PSS using SHA-512 and MGF1 with SHA-512
ES256: ECDSA using P-256 and SHA-256
ES384: ECDSA using P-384 and SHA-384
ES512: ECDSA using P-521 and SHA-512
```


## 使用 JWKS 端點驗證 JWT

驗證已簽署 JWT 的簽章是授予使用者存取權的最後一個步驟。當用戶端以 REST 請求傳送 JWT 時，OpenSearch 會驗證簽章。每個驗證請求都會驗證簽章。

您可以指定 JSON Web Key Set (JWKS) 端點，從簽發者伺服器上的位置擷取金鑰，而不必將用於驗證的密碼編譯金鑰儲存在本機 `config.yml` 檔案的 `authc` 區段中。這種驗證 JWT 的方法有助於簡化公開金鑰與憑證的管理。

如需 JSON Web Key 內容與格式的詳細資訊，請參閱 [JSON Web Key (JWK) 格式](https://datatracker.ietf.org/doc/html/rfc7517#section-4)。

### 為 JWT 驗證設定 JWKS 端點

您可以直接在 JWT 驗證網域中設定 JWKS 端點。此方法透過自動金鑰輪替與動態金鑰管理來提供增強的安全性：

```yml
jwt_auth_domain:
  description: "Authenticate via JSON Web Token"
  http_enabled: true
  transport_enabled: true
  order: 0
  http_authenticator:
    type: jwt
    challenge: false
    config:
      jwks_uri: "https://example.com/.well-known/jwks.json"
      signing_key: null  # Not used when jwks_uri is specified
      jwt_header: "Authorization"
      jwt_url_parameter: null
      jwt_clock_skew_tolerance_seconds: 30
      roles_key: "roles"
      subject_key: "sub"
  authentication_backend:
    type: noop
```
{% include copy.html %}

### JWKS 組態參數

下表說明 JWKS 專屬的組態參數。

名稱 | 說明 | 預設值
:--- | :--- | :---
`jwks_uri` | JWKS 端點 URL。指定後，會忽略 `signing_key`，並從此端點擷取金鑰。 | `null`

### (進階) 安全性保護

為了防範阻斷服務 (DoS) 攻擊並確保 JWKS 作業安全，Security 外掛程式提供多項保護措施，包括請求限制、逾時及回應大小限制。下表說明可用於保護 JWKS 作業的設定。

名稱 | 說明 | 預設值
:--- | :--- | :---
`max_jwks_keys` | 要從 JWKS 回應處理的金鑰數量上限。設為 `-1` 表示無限制。 | `-1`
`jwks_request_timeout_ms` | 對 JWKS 端點的單一 HTTP 請求允許的最長時間，以毫秒為單位。 | `5000`
`jwks_queued_thread_timeout_ms` | 請求在處理前可在佇列中等待的最長時間，以毫秒為單位。 | `2500`
`max_jwks_response_size_bytes` | JWKS 端點回應的大小上限，以位元組為單位。 | `1048576` (1 MB)
`refresh_rate_limit_count` | 在時間範圍內允許的 JWKS 重新整理請求數量上限。 | `10`
`refresh_rate_limit_time_window_ms` | JWKS 重新整理請求速率限制的時間範圍，以毫秒為單位。 | `10000` (10 秒)

<!-- vale off -->
### 含 Key ID 的 JWT 標頭
<!-- vale on -->

使用 JWKS 時，您的 JWT 標頭必須包含金鑰 ID (`kid`)，以識別要用於驗證的特定金鑰：

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "V-diposfUJIk5jDBFi_QRouiVinG5PowskcSWy5EuCo"
}
```
{% include copy.html %}

使用 JWKS 端點時必須提供 `kid` 參數，且其必須符合 JWKS 回應中的金鑰識別碼。

### JWKS 回應範例

JWKS 端點必須傳回包含公開金鑰陣列的 JSON 物件。每個金鑰都必須包含中繼資料，例如金鑰類型 (`kty`)、用途 (`use`)、金鑰 ID (`kid`) 及演算法 (`alg`)：

```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "V-diposfUJIk5jDBFi_QRouiVinG5PowskcSWy5EuCo",
      "alg": "RS256",
      "n": "nCJ9ve8zRv_4pdSja5i_8GgozoVZrUocD6UnMyQmh6fRBZWspoIRSGdTjcKktevnKWXlg7mqe7FIx6CdVqR5rVfM0o61_7cgxJqdNdnCXsFR8_S_98qMIJ-gxmlwE2a1X1VrCSmYh60APUGoGypm0sAsjvYTzU04LTN7K0Gip3H5qpkFD-Mxlev75WeC8WrvsfUFl6XN1h55HZW2wlYJGmbFVQx5839d8o6BxDVvQrGdN8MzLRFTMG8wiPhVDQL5NHt3vKgDnD6zT0c_S5Kz42i4bcktRRoAbR3LjDn5YbAatmfKzwOuL0XsbEnn-kgnt2aJ5GCaggukY3mMc-Bhew",
      "e": "AQAB"
    }
  ]
}
```
{% include copy.html %}

### 快取與效能

JWKS 回應會被快取以最佳化效能：

- **初始快取**：啟用 JWKS 時，系統會快取 JWKS 端點的回應。
- **在下列情況會觸發快取重新整理**：
  - 當 JWT 包含快取中找不到的 `kid` 時
  - 當快取項目依據 HTTP 快取標頭到期時
  - 在背景重新整理週期期間
- **速率限制**：防止對 JWKS 端點發出過多請求（預設為每 10 秒時間範圍 10 個請求）。

### 回溯相容性

從 OpenSearch 3.3 開始，JWT 驗證支援直接設定 JWKS 端點。此功能維持完整的回溯相容性：

- 當未指定 `jwks_uri` 或將其設為 `null` 時，系統會使用現有的靜態 `signing_key` 機制。
- 現有的 JWT 組態無需修改即可繼續運作。
- 您可以透過更新組態，在靜態金鑰與 JWKS 之間切換。
- 當 `jwks_uri` 與 `signing_key` 同時設定時，`jwks_uri` 具有優先權，而 `signing_key` 會被忽略。

<!-- vale off -->
## 搭配 Teleport 使用 JWT
<!-- vale on -->

您可以使用 Teleport 簽發的 JWT 權杖，在 OpenSearch Dashboards 中驗證使用者。此整合會將 Teleport 角色對應至 OpenSearch 後端角色，以進行存取控制。

### Teleport 組態

在 Teleport 中，您需要建立一個角色，其名稱與 OpenSearch 執行個體中的某個後端角色相同：

```yaml
apiVersion: resources.teleport.dev/v1
kind: TeleportRoleV7
metadata:
  name: admin # Match Opensearch "Backend roles" names
spec:
  allow:
    # App
    app_labels_expression: |
      regexp.match(labels["hostname"], "^(.*)opensearch(.*)$")
```
{% include copy.html %}

然後將此角色套用至您要使用該角色的使用者。

### OpenSearch Dashboards 組態

若要設定 OpenSearch 以使用 Teleport，請執行下列動作。

#### Teleport 組態

在代理程式組態檔（通常位於 `/etc/teleport.yaml`）中，設定應用程式服務以自動將 JWT 包含在請求標頭中：

```yaml
# [...]
app_service:
  enabled: "yes"
  apps:
  - name: opensearch-dashboard
    uri: "https://127.0.0.1:5601"
    insecure_skip_verify: true
    rewrite:
      headers:
      - "Authorization: {% raw %}{{internal.jwt}}{% endraw %}"
    labels:
      # [...]
```
{% include copy.html %}

然後執行此命令以套用新組態：

```bash
systemctl restart teleport
```
{% include copy.html %}

#### OpenSearch Dashboards 組態

在 OpenSearch Dashboards 組態檔（通常位於 `/usr/share/opensearch-dashboards/config/opensearch_dashboards.yml`）中，啟用 JWT 驗證，並保留基本 HTTP 驗證作為後備方法：

```yaml
opensearch_security.auth.multiple_auth_enabled: true
opensearch_security.auth.type: ["basicauth", "jwt"]
```
{% include copy.html %}

然後執行此命令以套用新組態：

```bash
systemctl restart dashboards
```
{% include copy.html %}

### Security 節點組態

在執行 `securityadmin.sh` 指令碼的節點上，更新 Security 外掛程式組態檔（例如 `/usr/share/opensearch/config/opensearch-security/config.yml`），以設定兩種驗證方法：

```yaml
_meta:
  type: "config"
  config_version: 2

config:
  dynamic:
    authc:
      basic_internal_auth_domain:
        description: "Authenticate via HTTP Basic against internal users database"
        http_enabled: true
        transport_enabled: true
        order: 1
        http_authenticator:
            type: basic
            challenge: true
        authentication_backend:
            type: internal

      jwt_auth_domain:
        description: "Authenticate via Json Web Token provide by Teleport"
        http_enabled: true
        transport_enabled: true
        order: 0
        http_authenticator:
            type: jwt
            challenge: false
            config:
                signing_key: null
                jwks_uri: "https://example.com/.well-known/jwks.json" # URL of the Teleport's leaf the machine is in, not the root
                jwt_header: "Authorization"
                jwt_url_parameter: null
                jwt_clock_skew_tolerance_seconds: 30
                subject_key: "sub"
                roles_key: "roles"
        authentication_backend:
            type: noop
```
{% include copy.html %}

請確保基本驗證是使用 `order: 1` 與 `challenge: true` 設定，且 JWT 驗證是使用 `order: 0` 與 `challenge: false` 設定。否則，除非明確包含 JWT 標頭，直接 API 呼叫將會失敗。

若要套用新組態，請執行以下命令：

```bash
{% raw %}
export JAVA_HOME="[OPENSEARCH_INSTALL_DIR]/jdk"

bash [OPENSEARCH_INSTALL_DIR]/plugins/opensearch-security/tools/securityadmin.sh \
-cacert [PATH_TO_ROOT_CA] \
-cert [PATH_TO_ADMIN_CERT_PEM] \
-key [PATH_TO_ADMIN_CERT_KEY] \
-cd [PATH_TO_OPENSEARCH_SECURITY_CONFIG_DIR] \
-nhnv -icl \
-h 127.0.0.1
{% endraw %}
```
{% include copy.html %}

## 搭配 gRPC 使用 JWT 驗證
**於 3.5 版導入**
{: .label .label-purple }

JWT 驗證支援透過 gRPC 傳輸進行。gRPC 傳輸與 HTTP 層共用相同的驗證網域，因此 JWT 權杖會依據相同的驗證後端組態進行驗證。您可以透過 gRPC 提供與使用 REST API 時相同的 JWT 標頭。

透過 gRPC 傳輸 JWT 時，您必須啟用 TLS。有關為 gRPC 設定 TLS 的資訊，請參閱[為 gRPC 設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-tls-certificates-for-grpc)。

請注意以下限制：

- gRPC 不支援超級使用者驗證（用戶端憑證驗證）。需要超級使用者權限的組態變更必須使用 REST API。
- gRPC 不支援匿名驗證。帶有匿名驗證標頭的請求會被拒絕，視為未授權。

## 疑難排解常見問題

本節詳細說明如何疑難排解安全性組態的常見問題。


### 驗證宣告是否正確

請確保 JWT 權杖包含正確的 `iat`（簽發時間）、`nbf`（生效時間）與 `exp`（到期時間）宣告，OpenSearch 會自動驗證這些項目。


### JWT URL 參數

當使用包含預設管理員角色 `all_access` 的 JWT URL 參數時（例如 `curl http://localhost:9200?jwtToken=<jwt-token>`），請求會失敗並擲回以下錯誤：

```json
{
   "error":{
      "root_cause":[
         {
            "type":"security_exception",
            "reason":"no permissions for [cluster:monitor/main] and User [name=admin, backend_roles=[all_access], requestedTenant=null]"
         }
      ],
      "type":"security_exception",
      "reason":"no permissions for [cluster:monitor/main] and User [name=admin, backend_roles=[all_access], requestedTenant=null]"
   },
   "status":403
}
```

若要修正此問題，請確保角色 `all_access` 直接對應至內部使用者，而非對應至後端角色。若要這麼做，請前往 **Security > Roles > all_access**，然後選取 **Mapped users** 索引標籤。選取 **Manage mapping**，並在 **Users** 區段中新增 "admin"。

![在 Users 區段中新增 admin 的對應管理畫面](https://user-images.githubusercontent.com/5849965/179158704-b2bd6d48-8816-4b03-a960-8c612465cf75.png)

使用者隨後應會出現在 **Mapped Users** 索引標籤上。

![Mapped Users 索引標籤中顯示已對應的使用者](https://user-images.githubusercontent.com/5849965/179158750-1bb5e232-dd61-449a-a561-0613b71bfd68.png)


### OpenSearch Dashboards 組態

雖然 JWT URL 參數驗證在直接查詢 OpenSearch 時可正常運作，但用於存取 OpenSearch Dashboards 時會失敗。

**解決方案：** 請確認 `opensearch_dashboards.yml` 組態檔案中包含下列幾行：

```yml
opensearch_security.auth.type: "jwt"
opensearch_security.jwt.url_param: <your-param-name-here>
```
