---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AWS Signature Version 4 驗證"
has_children: false
nav_order: 50
parent: Connectors
grand_parent: Connecting to externally hosted models
great_grand_parent: Integrating ML models
---

# AWS Signature Version 4 驗證

使用 `aws_sigv4` 通訊協定的連接器會使用 AWS Signature Version 4 簽署每個請求。Amazon SageMaker、Amazon Bedrock、Amazon Comprehend 和 Amazon Textract 等 AWS 服務皆使用此通訊協定。此通訊協定會使用您提供的憑證簽署每個請求，並新增必要的 `Authorization` 標頭，因此您不需要指定此標頭。

下列請求會建立使用 `aws_sigv4` 通訊協定的獨立連接器。此範例顯示通訊協定所需的 `credential` 和 `parameters` 欄位。`url` 和 `request_body` 欄位則取決於您呼叫的服務和模型：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "sagemaker: embedding",
    "description": "Connector for a SageMaker embedding model",
    "version": 1,
    "protocol": "aws_sigv4",
    "credential": {
        "access_key": "<access_key>",
        "secret_key": "<secret_key>",
        "session_token": "<session_token>"
    },
    "parameters": {
        "region": "us-west-2",
        "service_name": "sagemaker"
    },
    "actions": [
        {
            "action_type": "predict",
            "method": "POST",
            "headers": {
                "content-type": "application/json"
            },
            "url": "https://runtime.sagemaker.${parameters.region}.amazonaws.com/endpoints/<endpoint_name>/invocations",
            "request_body": "[\"${parameters.inputs}\"]"
        }
    ]
}
```
{% include copy-curl.html %}

如需適用於您服務和模型的完整請求，包括 `url`、`request_body` 和任何處理函式，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)中適用於您平台和模型的藍圖。

## 請求本文欄位

當 `protocol` 設為 `aws_sigv4` 時，`credential` 物件支援下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:---|:---|:---|:---|
| `access_key` | 字串 | 必要 | AWS 帳戶的存取金鑰。 |
| `secret_key` | 字串 | 必要 | AWS 帳戶的秘密金鑰。 |
| `session_token` | 字串 | 選用 | AWS 帳戶的暫時工作階段權杖。 |

當 `protocol` 設為 `aws_sigv4` 時，`parameters` 物件支援下列欄位。

| 欄位 | 資料類型 | 必要/選用 | 說明 |
|:---|:---|:---|:---|
| `region` | 字串 | 必要 | 託管服務的 AWS 區域。 |
| `service_name` | 字串 | 必要 | 連接器呼叫的 AWS 服務名稱。 |

## 後續步驟

- 若要尋找適用於您服務和模型的藍圖，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。
- 若要註冊並部署使用此連接器的模型，請參閱[連接至外部託管的模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/index/)。
