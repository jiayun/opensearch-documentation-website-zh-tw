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

若要設定動態標頭，請在連接器的 `actions[].headers` 欄位中使用 `${parameters.*}` 預留位置定義該標頭。您也可以選擇在最上層的 `parameters` 欄位中為該參數設定預設值。

以下範例使用預留位置端點 `api.example.com`。連接器 URL 必須符合 `plugins.ml_commons.trusted_connector_endpoints_regex` 中的模式，因此請將該端點替換為您模型的端點，或將其加入信任的端點清單。如需更多資訊，請參閱[新增信任的端點]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/#adding-trusted-endpoints)。

若要建立包含動態標頭的連接器，請傳送以下請求：

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

在預測時，請在 `_predict` 請求的 `parameters` 欄位中傳入執行階段的值：

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

傳送至遠端端點的最終 HTTP 請求會包含替換後的標頭：

```json
POST https://api.example.com/predict
Authorization: test-api-key
X-Test-Request-Id: request-123
```

若未提供執行階段的值，且連接器的 `parameters` 欄位中也未設定預設值，預測請求將被拒絕並回傳 400 錯誤。若要避免這種情況，請在連接器的 `parameters` 欄位中為該參數定義預設值。若未提供執行階段的值，則會使用預設值。

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

在進行替換之前，OpenSearch 會對 `_predict` 請求中的參數值進行 JSON 逸出處理。執行階段值中的換行字元會以兩個字元 `\n` 的形式送達標頭，其他控制字元則會以 `\u0001` 等逸出序列的形式送達。下列值在替換時不會進行逸出處理：

- `_predict` 請求之 `no_escape_params` 參數中所列參數的值
- 有效 JSON 物件或陣列的值
- 連接器 `parameters` 欄位的預設值

在預測時，替換後的標頭值會先經過驗證，之後才會將請求傳送至模型端點。若預測請求的標頭未通過下列任一項檢查，就會傳回 400 錯誤：

- 含有歸位字元（`\r`）、換行字元（`\n`）或其他控制字元（`0x00–0x1F`，但不含定位字元，以及 `0x7F`）的標頭值會遭到拒絕，以防止 HTTP 回應分割。由於執行階段值會經過逸出處理，因此這項限制僅適用於未經逸出處理即替換的值。
- 每個標頭（包括其名稱與值）不得超過 8 KB（8,192 個字元）。
- 所有標頭名稱與值的合計大小不得超過 64 KB（65,536 個字元）。

大小限制適用於逸出後的值，因此逸出序列也會計入其中。例如，執行階段值中的 `"` 字元會計為兩個字元（`\"`）。

## 後續步驟

- 如需所有連接器欄位的說明，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。
- 如需向連接器提供驗證認證資訊的相關資訊，請參閱[連接器驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connector-authentication/)中適用於您平台通訊協定的驗證方法。
