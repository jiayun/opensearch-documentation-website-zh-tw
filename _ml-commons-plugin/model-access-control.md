---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模型存取控制"
parent: Integrating ML models
has_children: false
nav_order: 20
---

# 模型存取控制
**於 2.9 版推出**
{: .label .label-purple }

您可以將 Security 外掛程式與 ML Commons 搭配使用，為非管理員使用者管理特定模型的存取權。舉例來說，組織中的某個部門可能會想限制其他部門的使用者存取其模型。

為了達成此目的，使用者會被指派一或多個[_後端角色_]({{site.url}}{{site.baseurl}}/security/access-control/index/)。後端角色不是在設定使用者時將個別角色指派給個別使用者，而是在使用者登入時將後端角色指派給使用者，藉此提供一種將一組使用者對應至角色的方式。舉例來說，使用者可能會被指派包含 `ml_full_access` 角色的 `IT` 後端角色，並擁有所有 ML Commons 功能的完整存取權。或者，其他使用者可能會被指派包含 `ml_readonly_access` 角色的 `HR` 後端角色，並僅限於對機器學習 (ML) 功能的唯讀存取權。有了這樣的彈性，後端角色可以提供更精細的模型存取權，並且更容易將多個使用者指派至某個角色，而不必個別對應使用者和角色。

## ML Commons 角色

ML Commons 外掛程式有兩個保留角色：

- `ml_full_access`：授予所有 ML 功能的完整存取權，包括啟動新的 ML 工作以及讀取或刪除模型。
- `ml_readonly_access`：授予 ML 工作、已訓練模型，以及與模型所屬叢集相關之統計資料的唯讀存取權。不會授予啟動或刪除 ML 工作或模型的權限。

## 模型群組

為了進行存取控制，模型會組織成_模型群組_，也就是特定模型各版本的集合。與使用者一樣，模型群組可以被指派一或多個後端角色。同一個模型的所有版本共用相同的模型名稱，並具有相同的後端角色。

當您建立新的模型群組時，您會被視為該模型的_擁有者_。即使其他使用者將模型註冊到此模型群組，您仍是該模型及其所有版本的擁有者。當模型擁有者建立模型群組時，擁有者可以為此模型群組指定下列其中一種_存取模式_：

- `public`：所有可存取叢集的使用者都可以存取此模型群組。
- `private`：只有模型擁有者或管理員使用者可以存取此模型群組。
- `restricted`：擁有者、管理員使用者，或共用此模型群組其中一個後端角色的任何使用者，都可以存取此模型群組中的任何模型。建立 `restricted` 模型群組時，擁有者必須將擁有者的一或多個後端角色附加至該模型。

無論存取模式為何，管理員都可以存取叢集中的所有模型群組。
{: .note}

## 模型存取控制先決條件

使用模型存取控制之前，您必須符合下列先決條件：

1. 在您的叢集上啟用 Security 外掛程式。如需詳細資訊，請參閱 [OpenSearch 中的安全性]({{site.url}}{{site.baseurl}}/security/)。
2. 對於 `restricted` 模型群組，請確認管理員已[將後端角色指派給使用者](#assigning-backend-roles-to-users)。
3. 在您的叢集上[啟用模型存取控制](#enabling-model-access-control)。

如果有任何先決條件未符合，叢集中的所有模型都會是 `public`，且任何可存取叢集的使用者都可以存取。
{: .note}

## 將後端角色指派給使用者

建立適當的後端角色，並將這些角色指派給使用者。後端角色通常來自 [LDAP 伺服器]({{site.url}}{{site.baseurl}}/security/configuration/ldap/)或 [SAML 提供者]({{site.url}}{{site.baseurl}}/security/configuration/saml/)，但如果您使用內部使用者資料庫，則可以使用 REST API [手動新增它們]({{site.url}}{{site.baseurl}}/security/api/users/create-user/)。

只有管理員使用者可以將後端角色指派給使用者。
{: .note}

指派後端角色時，請考量下列兩個使用者的範例：`alice` 和 `bob`。

下列請求會將 `analyst` 後端角色指派給使用者 `alice`：

```json
PUT _plugins/_security/api/internalusers/alice
{
  "password": "alice",
  "backend_roles": [
    "analyst"
  ],
  "attributes": {}
}
```

下一個請求會將 `human-resources` 後端角色指派給使用者 `bob`：

```json
PUT _plugins/_security/api/internalusers/bob
{
  "password": "bob",
  "backend_roles": [
    "human-resources"
  ],
  "attributes": {}
}
```

最後，最後一個請求會將可讓使用者完整存取 ML Commons 的角色同時指派給 `alice` 和 `bob`：

```json
PUT _plugins/_security/api/rolesmapping/ml_full_access
{
  "backend_roles": [],
  "hosts": [],
  "users": [
    "alice",
    "bob"
  ]
}
```

如果 `alice` 建立了模型群組並為其指派 `analyst` 後端角色，則 `bob` 無法存取此模型。

## 啟用模型存取控制

您可以如下動態啟用模型存取控制：

```json
PUT _cluster/settings
{
  "transient": {
    "plugins.ml_commons.model_access_control_enabled": "true"
  }
}
```
{% include copy-curl.html %}

## 模型存取控制 API

模型存取控制是透過 Model Group API 來達成。這些 API 包括註冊、搜尋、更新和刪除模型群組等操作。

如需與模型存取控制相關之 API 的資訊，請參閱 [Model Group API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-group-apis/index/)。

## 隱藏模型
**於 2.12 版推出**
{: .label .label-purple }

若要對終端使用者 (包括叢集管理員) 隱藏模型詳細資料，您可以註冊_隱藏_模型。如果模型已隱藏，非超級管理員使用者就沒有權限呼叫該模型上的任何 [Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/)，但 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 除外。

只有超級管理員使用者可以註冊隱藏模型。隱藏模型可以是 OpenSearch 提供的預先訓練模型、您自己的自訂模型，或外部託管的模型。若要註冊隱藏模型，您必須先使用[管理員憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/#configuring-admin-certificates)進行驗證：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem -XGET 'https://localhost:9200/.opendistro_security/_search'
```

超級管理員使用者建立的所有模型都會自動註冊為隱藏。若要註冊隱藏模型，請將請求傳送至 `_register` 端點：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem -X POST 'https://localhost:9200/_plugins/_ml/models/_register' -H 'Content-Type: application/json' -d '
{
    "name": "OPENSEARCH_ASSISTANT_MODEL",
    "function_name": "remote",
    "description": "OpenSearch Assistant Model",
    "connector": {
        "name": "Bedrock Claude Connector",
        "description": "The connector to Bedrock Claude",
        "version": 1,
        "protocol": "aws_sigv4",
        "parameters": {
          "region": "us-east-1",
          "service_name": "bedrock"
        },
        "credential": {
            "access_key": "<YOUR_ACCESS_KEY>",
            "secret_key": "<YOUR_SECRET_KEY>",
            "session_token": "<YOUR_SESSION_TOKEN>"
        },
        "actions": [
           {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "url": "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-v2/invoke",
            "request_body": "{\"prompt\":\"\\n\\nHuman: ${parameters.inputs}\\n\\nAssistant:\",\"max_tokens_to_sample\":300,\"temperature\":0.5,\"top_k\":250,\"top_p\":1,\"stop_sequences\":[\"\\\\n\\\\nHuman:\"]}"
          }
       ]
    }
}'
```
{% include copy.html %}

註冊隱藏模型之後，只有超級管理員可以對該模型叫用作業，包括部署、取消部署、刪除和取得 API 作業。舉例來說，若要部署隱藏模型，請傳送下列請求。在此請求中，`q7wLt4sBaDRBsUkl9BJV` 是模型 ID：

```json
curl -k --cert ./kirk.pem --key ./kirk-key.pem -X POST 'https://localhost:9200/_plugins/_ml/models/q7wLt4sBaDRBsUkl9BJV/_deploy'
```
{% include copy.html %}

隱藏模型的 `model_id` 是模型 `name`。隱藏模型包含設為 `true` 的 `is_hidden` 參數。您無法變更隱藏模型的 `is_hidden` 參數。

管理員使用者可以透過更新模型的後端角色來變更模型的存取權。 