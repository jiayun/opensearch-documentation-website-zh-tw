---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得連接器"
parent: Connector APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# Get Connector API

此 API 會依連接器 ID 擷取連接器。

### 端點

```json
GET /_plugins/_ml/connectors/{connector_id}
```

## 範例請求

```json
GET /_plugins/_ml/connectors/N8AE1osB0jLkkocYjz7D
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name" : "BedRock Claude-Instant v1",
  "version" : "1",
  "description" : "Bedrock connector for Claude Instant testing",
  "protocol" : "aws_sigv4",
  "parameters" : {
    "endpoint" : "bedrock.us-east-1.amazonaws.com",
    "content_type" : "application/json",
    "auth" : "Sig_V4",
    "service_name" : "bedrock",
    "region" : "us-east-1",
    "anthropic_version" : "bedrock-2023-05-31"
  },
  "actions" : [
    {
      "action_type" : "PREDICT",
      "method" : "POST",
      "url" : "https://bedrock-runtime.us-east-1.amazonaws.com/model/anthropic.claude-instant-v1/invoke",
      "headers" : {
        "x-amz-content-sha256" : "required",
        "content-type" : "application/json"
      },
      "request_body" : "{\"prompt\":\"${parameters.prompt}\", \"max_tokens_to_sample\":${parameters.max_tokens_to_sample}, \"temperature\":${parameters.temperature},  \"anthropic_version\":\"${parameters.anthropic_version}\" }"
    }
  ]
}
```
