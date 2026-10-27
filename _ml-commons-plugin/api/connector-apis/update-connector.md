---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新連接器"
parent: Connector APIs
grand_parent: ML APIs
nav_order: 27
---

# 更新連接器 API
**2.12 版新增**
{: .label .label-purple }

使用此 API，可依據連接器 ID 更新獨立連接器。若要更新在特定模型內建立的連接器，請使用[更新模型 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/update-model/)。

在更新獨立連接器之前，您必須先取消部署所有使用該連接器的模型。關於取消部署模型的資訊，請參閱[取消部署模型 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/undeploy-model/)。
{: .note}

使用此 API，您可以更新[請求欄位](#request-body-fields)一節所列的連接器欄位，並為連接器新增選用欄位。您無法使用此 API 刪除連接器中的欄位。

關於此 API 的使用者存取權資訊，請參閱[模型存取控制注意事項]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/index/#model-access-control-considerations)。

## 端點

```json
PUT /_plugins/_ml/connectors/{connector_id}
```

## 請求本文欄位

下表列出可更新的欄位。如需所有連接器欄位的詳細資訊，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints#request-body-fields)。

| 欄位 | 資料類型   | 說明                                                                                                                                                                                                                                                                                                                                                                                   |
| :---  |:------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `name` | 字串      | 連接器的名稱。                                                                                                                                                                                                                                                                                                                                                                    |
| `description` | 字串      | 連接器的說明。                                                                                                                                                                                                                                                                                                                                                               |
| `version` | 整數     | 連接器版本。                                                                                                                                                                                                                                                                                                                                 |
| `protocol` | 字串      | 連線的通訊協定。若是 Amazon SageMaker 和 Amazon Bedrock 等 AWS 服務，請使用 `aws_sigv4`。若是其他所有服務，請使用 `http`。                                                                                                                                                                                                                                          |
| `parameters` | JSON 物件 | 預設連接器參數，包括 `endpoint` 和 `model`。此欄位中的任何參數皆可被預測請求中指定的參數覆寫。                                                                                                                                                                                                                     |
| `credential` | JSON 物件 | 定義連線至所選端點所需的任何認證資訊變數。OpenSearch 使用 **AES/GCM/NoPadding** 對稱式加密來加密您的認證資訊。當與叢集的連線首次啟動時，OpenSearch 會建立隨機的 32 位元組加密金鑰，並保存在 OpenSearch 的系統索引中。因此，您不需要手動設定加密金鑰。 |
| `actions` | JSON 陣列  | 定義連接器內可執行哪些動作。如果您是建立連線的管理員，請為所需的連線新增[藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)。                                                                                                                                                              |
| `backend_roles` | JSON 陣列  | OpenSearch 後端角色清單。如需設定後端角色的詳細資訊，請參閱[為使用者指派後端角色]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control#assigning-backend-roles-to-users)。                                                                                                                                                        |
| `add_all_backend_roles` | 布林值 | 更新連接器時沒有作用。若要變更連接器的後端角色，請在 `backend_roles` 中指定。 |
| `client_config` | JSON 物件 | 用戶端組態物件，用於控制連線限制、逾時、重試和 TLS 選項。如需詳細資訊，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints#request-body-fields)。 |
| `access_mode` | 字串      | 設定連接器的存取模式，可為 `public`、`restricted` 或 `private`。若省略，連接器會保留目前的存取模式。如需 `access_mode` 的詳細資訊，請參閱[模型群組]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control#model-groups)。                                                                                                                                        |
| `parameters.skip_validating_missing_parameters`  | 布林值     | 設為 `true` 時，此選項可讓您使用連接器傳送請求，而不驗證任何缺少的參數。預設值為 `false`。                                                                                                                                                                                                                                                                     |



## 請求範例

```json
PUT /_plugins/_ml/connectors/u3DEbI0BfUsSoeNTti-1
{
  "description": "The connector to public OpenAI model service for gpt-4o-mini"
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-connector",
  "_id": "u3DEbI0BfUsSoeNTti-1",
  "_version": 2,
  "result": "updated",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 2,
  "_primary_term": 1
}
```