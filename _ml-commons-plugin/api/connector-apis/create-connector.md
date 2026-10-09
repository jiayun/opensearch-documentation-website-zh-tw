---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立連接器"
parent: Connector APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 建立連接器 API

建立獨立的連接器。如需更多資訊，請參閱[連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)。

## 端點

```json
POST /_plugins/_ml/connectors/_create
```

## 請求本文欄位

如需請求欄位的清單，請參閱[請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints#request-body-fields)。

## 範例請求

若要建立獨立的連接器，請將請求傳送至 `connectors/_create` 端點，並提供[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/)中所述的所有參數：

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
        "openAI_key": "..."
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

## 範例回應

```json
{
  "connector_id": "a1eMb4kBJ1eYAeTMAljY"
}
```