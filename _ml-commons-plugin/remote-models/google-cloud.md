---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Google Cloud 驗證"
has_children: false
nav_order: 60
parent: Connectors
grand_parent: Connecting to externally hosted models
great_grand_parent: Integrating ML models
---

# Google Cloud 驗證
**3.9 版新增**
{: .label .label-purple }

`google_cloud` 連接器協定讓 OpenSearch 能夠呼叫 Google Cloud Vertex AI 模型。OpenSearch 會產生並重新整理 Google Cloud OAuth 2.0 存取權杖，並在每個請求中加入 `Authorization` 標頭，因此您不需要手動提供或輪替權杖。此協定相當於 AWS 服務 [`aws_sigv4` 協定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/aws-sigv4/) 的 Google Cloud 版本。

## 必要條件

在建立 `google_cloud` 連接器之前，請在您的 Google Cloud 專案中啟用 Vertex AI，並準備服務帳戶金鑰，或者（若節點託管於 Google Cloud）準備 Workload Identity。然後設定下列叢集設定。

`google_cloud` 協定預設為停用。若要啟用，請將 `plugins.ml_commons.connector.vertexai_enabled` 叢集設定設為 `true`：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.connector.vertexai_enabled": true
  }
}
```
{% include copy-curl.html %}

將 Vertex AI 主機模式加入 `plugins.ml_commons.trusted_connector_endpoints_regex` 設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.ml_commons.trusted_connector_endpoints_regex": [
      "^https://.*-aiplatform\\.googleapis\\.com/.*$"
    ]
  }
}
```
{% include copy-curl.html %}

此設定會取代整個信任端點清單，因此請包含叢集所需的每個模式。預設清單請參閱[新增信任端點]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/#adding-trusted-endpoints)。
{: .warning}

## 驗證模式

`google_cloud` 協定支援兩種驗證模式。

### 服務帳戶金鑰模式

在 `credential` 物件中提供服務帳戶的 `private_key` 與 `client_email`：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Vertex AI Connector: Gemini",
    "description": "Vertex AI Gemini generateContent connector",
    "version": 1,
    "protocol": "google_cloud",
    "parameters": {
        "project_id": "<project_id>",
        "location": "us-central1",
        "model": "gemini-2.5-flash",
        "scopes": "https://www.googleapis.com/auth/cloud-platform"
    },
    "credential": {
        "private_key": "<private_key>",
        "client_email": "<client_email>",
        "token_uri": "https://oauth2.googleapis.com/token"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.location}-aiplatform.googleapis.com/v1/projects/${parameters.project_id}/locations/${parameters.location}/publishers/google/models/${parameters.model}:generateContent",
            "headers": {
                "Content-Type": "application/json"
            },
            "request_body": "{\"contents\":[{\"role\":\"user\",\"parts\":[{\"text\":\"${parameters.prompt}\"}]}]}"
        }
    ]
}
```
{% include copy-curl.html %}

### Application Default Credentials 模式

在託管於 Google Cloud 的節點上，請使用 Application Default Credentials (ADC) 或 Workload Identity，而非服務帳戶金鑰。在 `parameters` 中將 `auth_mode` 設為 `adc`，並省略 `credential` 物件：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Vertex AI Connector: Gemini (ADC)",
    "description": "Vertex AI Gemini generateContent connector using ADC",
    "version": 1,
    "protocol": "google_cloud",
    "parameters": {
        "project_id": "<project_id>",
        "location": "us-central1",
        "model": "gemini-2.5-flash",
        "auth_mode": "adc",
        "scopes": "https://www.googleapis.com/auth/cloud-platform"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "url": "https://${parameters.location}-aiplatform.googleapis.com/v1/projects/${parameters.project_id}/locations/${parameters.location}/publishers/google/models/${parameters.model}:generateContent",
            "headers": {
                "Content-Type": "application/json"
            },
            "request_body": "{\"contents\":[{\"role\":\"user\",\"parts\":[{\"text\":\"${parameters.prompt}\"}]}]}"
        }
    ]
}
```
{% include copy-curl.html %}

ADC 模式僅適用於託管於 Google Cloud 的節點。ADC 會從節點環境解析憑證，這需要聯絡 Google Cloud 中繼資料伺服器。服務帳戶金鑰模式與 ADC 模式互斥：若您在 ADC 模式中包含 `credential` 物件，其中不得包含 `private_key` 或 `client_email`，否則 OpenSearch 會拒絕該連接器。

## 請求本文欄位

當 `protocol` 設為 `google_cloud` 時，`credential` 物件支援下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:---|:---|:---|:---|
| `private_key` | 字串 | 服務帳戶金鑰模式中必要 | 服務帳戶的私密金鑰。ADC 模式中請省略。 |
| `client_email` | 字串 | 服務帳戶金鑰模式中必要 | 服務帳戶的用戶端電子郵件。ADC 模式中請省略。 |
| `token_uri` | 字串 | 選用 | Google OAuth 2.0 權杖端點。預設為 `https://oauth2.googleapis.com/token`。URL 必須使用 HTTPS，主機必須是 `oauth2.googleapis.com`，連接埠必須是 `443` 或省略。 |

當 `protocol` 設為 `google_cloud` 時，`parameters` 物件支援下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:---|:---|:---|:---|
| `project_id` | 字串 | 必要 | 您的 Google Cloud 專案 ID。 |
| `location` | 字串 | 必要 | Vertex AI 區域，例如 `us-central1`。 |
| `model` | 字串 | 必要 | Vertex AI 模型 ID，例如 `gemini-2.5-flash`。 |
| `auth_mode` | 字串 | 選用 | 設為 `adc` 以使用 Application Default Credentials 或 Workload Identity。服務帳戶金鑰模式中請省略。 |
| `scopes` | 字串 | 選用 | 要請求的 OAuth 2.0 範圍。請指定單一範圍。預設為 `https://www.googleapis.com/auth/cloud-platform`。 |

## 後續步驟

- 若要尋找模型的藍圖，包括 Gemini、嵌入、串流與批次推論，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。
- 若要註冊並部署使用此連接器的模型，請參閱[連線至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
