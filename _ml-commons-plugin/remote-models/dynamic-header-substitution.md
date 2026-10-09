---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "動態標頭替換"
has_children: false
nav_order: 70
parent: Connectors
grand_parent: Connecting to externally hosted models
great_grand_parent: Integrating ML models
---

# 動態標頭替換
**於 3.7 版引入**
{: .label .label-purple }

預設情況下，連接器標頭只會在建立連接器時解析一次。動態連接器標頭可讓您在標頭值中使用 `${parameters.*}` 預留位置，以便在預測時替換為個別請求的值。這有助於將交易 ID、關聯 ID 或追蹤權杖等請求範圍內的中繼資料傳遞至外部託管的模型端點。

## 設定動態標頭

若要設定動態標頭，請在連接器的 `actions[].headers` 欄位中定義含有 `${parameters.*}` 預留位置的標頭。您也可以選擇在頂層的 `parameters` 欄位中設定參數的預設值：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "My connector",
  "description": "Connector with dynamic headers",
  "version": 1,
  "protocol": "http",
  "parameters": {
    "endpoint": "api.example.com",
    "request_id": "default-request-id"
  },
  "credential": {
    "api_key": "test-api-key"
  },
  "actions": [{
    "action_type": "predict",
    "method": "POST",
    "url": "https://${parameters.endpoint}/predict",
    "headers": {
      "Authorization": "${credential.api_key}",
      "X-Test-Request-Id": "${parameters.request_id}"
    },
    "request_body": "{ \"input\": \"${parameters.input}\" }"
  }]
}
```
{% include copy-curl.html %}

進行預測時，請在 `_predict` 請求的 `parameters` 欄位中傳入執行階段值：

```json
POST /_plugins/_ml/models/{model_id}/_predict
{
  "parameters": {
    "request_id": "request-123",
    "input": "hello world"
  }
}
```
{% include copy-curl.html %}

傳送至遠端端點的 HTTP 請求會包含替換後的標頭：

```json
POST https://api.example.com/predict
Authorization: test-api-key
X-Test-Request-Id: request-123
```

如果未提供執行階段值，且連接器的 `parameters` 欄位中未設定預設值，預測請求就會遭到拒絕，並傳回 400 錯誤。若要避免此情況，請在連接器的 `parameters` 欄位中定義參數的預設值。如果未提供執行階段值，就會使用預設值。

## 安全性限制

下列標頭不能包含 `${parameters.*}` 預留位置。使用這些預留位置會在建立或更新連接器時傳回 400 錯誤。驗證標頭請改用 `${credential.*}`：

- 認證資訊標頭：
  - `Authorization`
  - `Proxy-Authorization`
  - `Cookie`
  - `X-API-Key`
  - `X-Auth-Token`
  - `X-Auth-Header`

- IP 與主機偽冒標頭：
  - `Host`
  - `X-Forwarded-Host`
  - `X-Forwarded-Server`
  - `X-Forwarded-For`
  - `Forwarded`
  - `X-Real-IP`
  - `X-Client-IP`
  - `CF-Connecting-IP`
  - `True-Client-IP`
  - `X-Originating-IP`

## 執行階段驗證

進行預測時，系統會在傳送請求前驗證替換後的標頭值：

- 含有 `\r` 或 `\n` 字元的標頭值會遭到拒絕，以防止 HTTP 回應分割。
- 含有控制字元（`0x00–0x1F`，定位字元除外）的值會遭到拒絕。
- 每個標頭值不得超過 8 KB。
- 所有標頭的總大小不得超過 64 KB。

## 後續步驟

- 如需所有連接器欄位的說明，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。
- 如需向連接器提供驗證認證資訊的相關資訊，請參閱[連接器驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connector-authentication/)中適用於您平台通訊協定的驗證方法。
