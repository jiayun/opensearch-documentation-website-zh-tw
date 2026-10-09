---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OTel 追蹤群組"
parent: Processors
grand_parent: Pipelines
nav_order: 270
---

# OTel 追蹤群組處理器

`otel_trace_group` 處理器會查詢 OpenSearch 後端，補齊 [span](https://github.com/opensearch-project/data-prepper/blob/834f28fdf1df6d42a6666e91e6407474b88e7ec6/data-prepper-api/src/main/java/org/opensearch/dataprepper/model/trace/Span.java) 記錄集合中缺少的追蹤群組相關欄位。`otel_trace_group` 處理器會查詢儲存在 OpenSearch 中的根 `span` 的相關欄位，找出 `spanId` 缺少的追蹤群組資訊。

## OpenSearch

當您使用使用者名稱和密碼連線至 OpenSearch 叢集時，請使用下列範例 `pipeline.yaml` 檔案設定 `otel_trace_group` 處理器：

``` YAML
pipeline:
  ...
  processor:
    - otel_trace_group:
        hosts: ["https://localhost:9200"]
        cert: path/to/cert
        username: YOUR_USERNAME_HERE
        password: YOUR_PASSWORD_HERE
```

請參閱 [OpenSearch 安全性]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/#opensearch-cluster-security)，以深入瞭解所需的 OpenSearch 憑證和權限，以及如何為 OTel 追蹤群組處理器設定這些憑證。

### Amazon OpenSearch Service

當您使用 [Amazon OpenSearch Service]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/sinks/opensearch/#amazon-opensearch-service-domain-security) 時，請使用下列範例 `pipeline.yaml` 檔案設定 `otel_trace_group` 處理器：

``` YAML
pipeline:
  ...
  processor:
    - otel_trace_group:
        hosts: ["https://your-amazon-opensearch-service-endpoint"]
        aws_sigv4: true
        cert: path/to/cert
        insecure: false
```

## 組態

您可以使用下列選項設定 `otel_trace_group` 處理器。

| 名稱 | 說明 | 預設值 |
| -----| ----| -----------|
| `hosts`| OpenSearch 節點的 IP 位址清單。必要。 | 無預設值。 | 
| `cert` | 以 PEM 編碼的憑證授權單位（CA）憑證。接受 .pem 或 .crt。這可讓用戶端信任為 OpenSearch 所使用憑證簽署的 CA。 | `null` |
| `aws_sigv4` | 用於以 AWS 憑證簽署 HTTP 請求的布林值旗標。僅適用於 Amazon OpenSearch Service。詳情請參閱 [OpenSearch 安全性](https://github.com/opensearch-project/data-prepper/blob/129524227779ee35a327c27c3098d550d7256df1/data-prepper-plugins/opensearch/security.md)。 | `false`。 |
| `aws_region` | 表示 Amazon OpenSearch Service 網域所在 AWS 區域的字串，例如 `us-west-2`。僅適用於 Amazon OpenSearch Service。 | `us-east-1` |
| `aws_sts_role_arn`| 接收端外掛程式擔任的 AWS Identity and Access Management（IAM）角色，用於簽署傳送至 Amazon OpenSearch Service 的請求。若未提供，外掛程式會使用[預設憑證](https://sdk.amazonaws.com/java/api/latest/software/amazon/awssdk/auth/credentials/DefaultCredentialsProvider.html)。 | `null` |
| `aws_sts_header_overrides` | IAM 角色為接收端外掛程式採用的標頭覆寫對應表。 | `null` |
| `insecure` | 用於關閉 SSL 憑證驗證的布林值旗標。若設為 `true`，會關閉 CA 憑證驗證，並傳送不安全的 HTTP 請求。 | `false` |
| `username` | 包含使用者名稱的字串，用於您 OpenSearch 叢集的[內部使用者]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/) `YAML` 組態檔案。 | `null` |
| `password` | 包含密碼的字串，用於您 OpenSearch 叢集的[內部使用者]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/) `YAML` 組態檔案。 | `null` |

## 組態選項範例

您可以在 `aws_sts_header_overrides` 選項中定義組態選項的值。請參閱下列範例：

```
aws_sts_header_overrides:
  x-my-custom-header-1: my-custom-value-1
  x-my-custom-header-2: my-custom-value-2
```

## 指標

下表說明 `otel_trace_group` 處理器專用的自訂指標。

| 指標名稱 | 類型 | 說明 |
| ------------- | ---- | ----------- |
| `recordsInMissingTraceGroup` | 計數器 | 缺少追蹤群組欄位的輸入記錄數量。 |
| `recordsOutFixedTraceGroup` | 計數器 | 成功補齊追蹤群組欄位的輸出記錄數量。 |
| `recordsOutMissingTraceGroup` | 計數器 | 缺少追蹤群組欄位的輸出記錄數量。 |