---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "HTTP 驗證"
has_children: false
nav_order: 40
parent: Connectors
grand_parent: Connecting to externally hosted models
great_grand_parent: Integrating ML models
---

# HTTP 驗證

使用 `http` 通訊協定的連接器會使用連接器 `credential` 物件中的值，向外部託管的模型進行驗證。大多數端點會接受權杖，例如 API 金鑰，連接器會將其放在請求標頭中傳遞。需要雙向 TLS (mTLS) 的端點則改為接受用戶端憑證。

## 權杖驗證

若要使用權杖進行驗證，請在 `credential` 物件中提供權杖，並使用 `${credential.*}` 預留位置從請求標頭中參照它。欄位名稱可任意指定——您平台的藍圖會指定要使用的名稱，例如 `openAI_key` 或 `cohere_key`：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "OpenAI Chat Connector",
    "description": "The connector to public OpenAI model service for gpt-4o-mini",
    "version": 1,
    "protocol": "http",
    "parameters": {
        "endpoint": "api.openai.com",
        "model": "gpt-4o-mini"
    },
    "credential": {
        "openAI_key": "<openai_key>"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.endpoint}/v1/chat/completions",
            "headers": {
                "Authorization": "Bearer ${credential.openAI_key}"
            },
            "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": ${parameters.messages} }"
        }
    ]
}
```
{% include copy-curl.html %}

如需您平台預期的權杖欄位名稱與標頭格式，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/) 中您平台與模型的藍圖。

## 用戶端憑證驗證
**於 3.9 版推出**
{: .label .label-purple }

用戶端憑證驗證也稱為雙向 TLS (mTLS)，可讓連接器在連線至外部託管的模型時出示用戶端憑證。連線的雙方會在 TLS 握手期間互相驗證：端點以伺服器憑證證明其身分，連接器則以用戶端憑證證明其身分。當模型端點要求用戶端憑證，而非在請求標頭中傳遞的權杖時，請使用 mTLS。

若要啟用 mTLS，請在連接器的 `client_config` 物件中將 `mutual_tls_enabled` 設為 `true`，並在連接器的 `credential` 物件中提供憑證資料。

### 請求本文欄位

當 `mutual_tls_enabled` 設為 `true` 時，`credential` 物件支援下列憑證欄位。請提供憑證內容本身，可以是將換行逸出為 `\n` 的 PEM 文字，或是 Base64 編碼的內容；不支援檔案路徑。OpenSearch 會以與其他任何認證相同的方式加密這些欄位，並讓它們在每個節點上都能使用，因此您不需要將憑證檔案複製到個別節點。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:---|:---|:---|:---|
| `client_cert_pem` | 字串 | 當 `keystore_type` 為 `PEM` 時為必要 | PEM 格式的用戶端憑證。若要出示由中繼憑證授權單位 (CA) 簽發的憑證，請包含完整鏈結，並以葉憑證排在最前面。 |
| `client_key_pem` | 字串 | 當 `keystore_type` 為 `PEM` 時為必要 | PEM 格式的用戶端私密金鑰。必須是未加密的 PKCS #8 金鑰 (`-----BEGIN PRIVATE KEY-----`)；不支援 PKCS #1 金鑰。 |
| `client_cert_pkcs12` | 字串 | 當 `keystore_type` 為 `PKCS12` 時為必要 | 包含用戶端憑證與私密金鑰的 Base64 編碼 PKCS12 金鑰庫。 |
| `keystore_password` | 字串 | 選用 | 保護 PKCS12 金鑰庫的密碼。若金鑰庫沒有密碼，請省略此欄位。 |
| `ca_cert_pem` | 字串 | 選用 | 一或多個 PEM 格式的 CA 憑證，用於驗證端點的伺服器憑證。可接受中繼與根憑證的組合。若省略，則使用 Java 預設信任存放區。當端點使用私人 CA 時，請提供此欄位。 |

`mutual_tls_enabled` 與 `keystore_type` 欄位屬於連接器的 `client_config` 物件。如需兩者的說明，請參閱 [連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。

### 先決條件

設定 mTLS 之前，請確認符合下列需求：

- 連接器使用 `http` 通訊協定。如需詳細資訊，請參閱 [限制](#restrictions)。
- 端點 URL 符合受信任的端點。如需詳細資訊，請參閱 [新增受信任的端點]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index#adding-trusted-endpoints)。
- PEM 格式的私密金鑰未加密，並使用 PKCS #8 編碼 (`-----BEGIN PRIVATE KEY-----`)。不支援 PKCS #1 金鑰 (`-----BEGIN RSA PRIVATE KEY-----`)。若要將 PKCS #1 金鑰轉換為 PKCS #8，請使用下列命令：

```bash
openssl pkcs8 -topk8 -inform PEM -outform PEM -nocrypt -in rsa_key.pem -out pkcs8_key.pem
```
{% include copy.html %}

Base64 編碼的 PEM 值會自動偵測並解碼。由於 Base64 編碼可避免手動逸出換行，因此對多行憑證而言是較方便的選項。若要將憑證或金鑰進行 Base64 編碼，請使用下列命令：

```bash
base64 -i client-cert.pem
```
{% include copy.html %}

### 使用 PEM 憑證

若要使用 PEM 憑證與私密金鑰進行驗證，請將 `keystore_type` 設為 `PEM`，並提供 `client_cert_pem` 與 `client_key_pem`：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Externally hosted model connector with mutual TLS",
  "description": "A connector that authenticates using a client certificate",
  "version": 1,
  "protocol": "http",
  "parameters": {
    "endpoint": "api.example.com"
  },
  "credential": {
    "client_cert_pem": "<BASE64-ENCODED CLIENT CERTIFICATE>",
    "client_key_pem": "<BASE64-ENCODED PRIVATE KEY>",
    "ca_cert_pem": "<BASE64-ENCODED CA CERTIFICATE>"
  },
  "client_config": {
    "mutual_tls_enabled": true,
    "keystore_type": "PEM"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/predict",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"input\": \"${parameters.input}\" }"
    }
  ]
}
```
{% include copy-curl.html %}

由於 `PEM` 是預設值，因此使用 PEM 憑證時可以省略 `keystore_type`。
{: .note}

### 使用 PKCS12 金鑰庫

若要使用 PKCS12 金鑰庫進行驗證，請將 `keystore_type` 設為 `PKCS12`，並在 `client_cert_pkcs12` 中提供 Base64 編碼的金鑰庫。PKCS12 金鑰庫是二進位格式，因此必須一律以 Base64 編碼：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Externally hosted model connector with a PKCS12 keystore",
  "description": "A connector that authenticates using a client certificate",
  "version": 1,
  "protocol": "http",
  "parameters": {
    "endpoint": "api.example.com"
  },
  "credential": {
    "client_cert_pkcs12": "<BASE64-ENCODED PKCS12 KEYSTORE>",
    "keystore_password": "<KEYSTORE PASSWORD>",
    "ca_cert_pem": "<BASE64-ENCODED CA CERTIFICATE>"
  },
  "client_config": {
    "mutual_tls_enabled": true,
    "keystore_type": "PKCS12"
  },
  "actions": [
    {
      "action_type": "predict",
      "method": "POST",
      "url": "https://${parameters.endpoint}/predict",
      "headers": {
        "content-type": "application/json"
      },
      "request_body": "{ \"input\": \"${parameters.input}\" }"
    }
  ]
}
```
{% include copy-curl.html %}

若要從現有的 PEM 憑證與金鑰建立 PKCS12 金鑰庫，再將其進行 Base64 編碼，請使用下列命令：

```bash
openssl pkcs12 -export -in client-cert.pem -inkey client-key.pem -out client.p12 -name client
base64 -i client.p12
```
{% include copy.html %}

### 憑證鏈結與自訂 CA 憑證

如果您的用戶端憑證是由中繼憑證授權單位 (CA) 簽發，請在 `client_cert_pem` 中包含完整鏈結。鏈結的順序以葉憑證排在最前面，接著是每個簽發的中繼憑證，讓每個憑證都是由其後方的憑證所簽發。順序錯誤的鏈結會被拒絕，並顯示指出相關憑證的錯誤。

`ca_cert_pem` 欄位是選用的，可控制如何驗證端點的伺服器憑證：

- 如果您提供 `ca_cert_pem`，OpenSearch 只會依據其中包含的憑證來驗證伺服器憑證。此欄位可接受組合，因此您可以同時包含中繼與根憑證。當端點使用私人 CA 時，請提供此欄位。
- 如果您省略 `ca_cert_pem`，OpenSearch 會依據 Java 預設信任存放區來驗證伺服器憑證。

由於私人 CA 通常不存在於預設信任存放區中，請提供 `ca_cert_pem`，而不要將 `skip_ssl_verification` 設為 `true`。啟用 mTLS 時，會拒絕略過驗證。
{: .important}

### 輪替憑證

若要輪替即將到期的憑證，請在更新請求中傳送新的憑證資料，如 [更新連接器認證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/#updating-connector-credentials) 所述。您不需要取消部署模型，也不需要重新啟動任何節點。

OpenSearch 會偵測到變更，並為後續的預測請求建立新的 HTTP 用戶端。被取代的用戶端會在寬限期後關閉，因此已在進行中的請求會使用先前的憑證完成。

### 限制

下列限制適用於用戶端憑證驗證：

- mTLS 僅適用於使用 `http` 通訊協定的連接器。使用 `aws_sigv4`、`mcp_sse` 或 `mcp_streamable_http` 通訊協定的連接器在建立時會接受 `mutual_tls_enabled`，但在執行階段會忽略它。
- `skip_ssl_verification` 與 `mutual_tls_enabled` 不能同時設為 `true`。停用伺服器憑證驗證會移除雙向 TLS 中的雙向部分，因此請提供 `ca_cert_pem`，以依據私人 CA 驗證伺服器憑證。
- 啟用 mTLS 時，`credential` 物件不能包含 `api_key`。OpenSearch 會強制僅使用憑證驗證，並拒絕混合的驗證方法。
- 憑證欄位不支援檔案路徑。請提供憑證內容本身。
- 憑證資料會在第一次預測請求時驗證。憑證組態無效的連接器可以成功建立，但在第一次使用時會失敗。

## 後續步驟

- 若要尋找您平台與模型的藍圖，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。
- 若要註冊並部署使用此連接器的模型，請參閱 [連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
- 如需所有連接器欄位 (包括 `client_config` 物件) 的說明，請參閱 [連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。
