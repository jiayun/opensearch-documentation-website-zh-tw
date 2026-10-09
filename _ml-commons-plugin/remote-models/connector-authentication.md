---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "連接器驗證"
has_children: false
nav_order: 30
parent: Connectors
grand_parent: Connecting to externally hosted models
great_grand_parent: Integrating ML models
---

# 連接器驗證

連接器使用其 `credential` 物件中的值向外部託管的模型進行驗證。驗證方法在連接器的 `protocol` 欄位中指定，並由您所連接的平台決定。每種通訊協定都有各自的憑證欄位和叢集必要條件。

下表列出可用的通訊協定。

| 通訊協定 | 平台 | 文件 |
|:---|:---|:---|
| `http` | 沒有專屬通訊協定的平台，包括 OpenAI、Cohere、Azure OpenAI、DeepSeek、Ollama、Aleph Alpha 和 Yandex Cloud | [HTTP 驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/http-authentication/) |
| `aws_sigv4` | AWS 服務，例如 Amazon SageMaker、Amazon Bedrock、Amazon Comprehend 和 Amazon Textract | [AWS Signature Version 4 驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/aws-sigv4/) |
| `google_cloud` | Google Cloud Vertex AI | [Google Cloud 驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/google-cloud/) |

`aws_sigv4` 和 `google_cloud` 通訊協定會為您產生並更新短期存取權杖，因此您不需要手動提供或輪替權杖。`http` 通訊協定則會傳遞您提供的憑證，最常見的是 API 金鑰之類的權杖。若要找出您的平台和模型適用的通訊協定，請參閱 [OpenSearch 提供的連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/supported-connectors/)。

需要相互 TLS (mTLS) 的端點會接受用戶端憑證而非權杖。這僅適用於使用 `http` 通訊協定的連接器。如需更多資訊，請參閱[用戶端憑證驗證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/http-authentication/#client-certificate-authentication)。

## 後續步驟

- 如需所有連接器欄位的說明，包括 `client_config` 物件，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。
- 若要變更現有連接器上的憑證，請參閱[更新連接器憑證]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/#updating-connector-credentials)。
