---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Atlassian Confluence
parent: Sources
grand_parent: Pipelines
nav_order: 5
---

# Atlassian Confluence 來源

您可以使用 OpenSearch Data Prepper `confluence` 來源，從一或多個 [Atlassian Confluence](https://www.atlassian.com/software/confluence) 空間匯入記錄。

## 使用方式

請選擇下列其中一種方式，設定 Confluence 專案存取憑證：

- **基本驗證** (API 金鑰驗證)：請依照[這些指示](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)。
- **OAuth 2.0 驗證**：請依照[這些指示](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/#faq-rrt-config)。

您也可以選擇將憑證存放在 AWS Secrets Manager 中。如果您未將憑證存放在 AWS Secrets Manager，則必須直接在管線組態中提供純文字憑證。

下列範例管線將 `confluence` 指定為來源。此管線會從名為 `space1` 和 `space2` 的多個 Confluence 空間匯入資料，並套用篩選條件，從這些專案中選取 wiki 內容 (頁面和部落格文章) 作為來源：

```yaml
version: "2"
extension:
  aws:
    secrets:
      confluence-account-credentials:
        secret_id: "arn:aws:secretsmanager:us-east-1:123456789012:secret:confluence-credentials-secret"
        region: "us-east-1"
        sts_role_arn: "arn:aws:iam::123456789012:role/Example-Role"
atlassian-confluence-pipeline:
  source:
    confluence:
      hosts: ["https://example.atlassian.net/"]
      acknowledgments: true
      preserve_formatting: true
      authentication:
        # Provide one of the authentication method to use. Supported methods are 'basic' and 'oauth2'.
        # For basic authentication, password is the API key that you generate using your confluence account
        basic:
          username: {% raw %} ${{aws_secrets:confluence-account-credentials:username}} {% endraw %} 
          password: {% raw %} ${{aws_secrets:confluence-account-credentials:password}} {% endraw %} 
          # For OAuth 2.0-based authentication, we require the following 4 key values stored in the secret
          # Follow atlassian instructions at the following link to generate these keys
          # https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/
          # If you are using OAuth 2.0 authentication, we also require, write permission to your aws secret to
          # be able to write the renewed tokens back into the secret
          # oauth2:
          # client_id: {% raw %} ${{aws_secrets:confluence-account-credentials:clientId}} {% endraw %} 
          # client_secret: {% raw %} ${{aws_secrets:confluence-account-credentials:clientSecret}} {% endraw %} 
          # access_token: {% raw %} ${{aws_secrets:confluence-account-credentials:accessToken}} {% endraw %} 
          # refresh_token: {% raw %} ${{aws_secrets:confluence-account-credentials:refreshToken}} {% endraw %} 
      filter:
        space:
          key:
            include:
              # This is not space name.
              # It is an alphanumeric space key that you can find under space details in confluence
              - "space1"
              - "space2"
              # exclude:
              # - "<<space key>>"
              # - "<<space key>>"
        page_type:
          include:
            - "page"
              # - "blogpost"
              # - "comment"
              # exclude:
            # - "attachment"
```
{% include copy.html %}

## 組態選項

`confluence` 來源支援下列組態選項。

| 選項            | 必要 | 類型                              | 說明                                                                                                                                                                                                                         |
|:------------------|:---------|:----------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hosts`           | 是      | List                              | Atlassian Confluence 主機名稱。目前僅支援一部主機，因此此清單預期大小為 1。                                                                                                                 |
| `acknowledgments` | 否       | Boolean                           | 設為 `true` 時，可讓 `confluence` 來源在 OpenSearch 接收端收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。 |
| `preserve_formatting` | 否       | Boolean                           | 設為 `true` 時，Confluence 內容格式標記標籤會保持原樣。預設為 `false` (移除標記標籤並轉換為純文字)。                                                                 |
| `authentication`  | 是      | [authentication](#Authentication) | 設定用來從指定主機存取 `confluence` 來源記錄的驗證方法。                                                                                                                            |
| `filter`          | 否       | [filter](#Filter)                 | 在擷取 Confluence 內容時套用特定的篩選條件。                                                                                                                                                               |

### 驗證

您可以使用下列其中一種驗證方法來存取 Confluence 主機。您必須提供下列其中一個參數。

| 選項   | 必要 | 類型              | 說明                                                  |
|:---------|:---------|:------------------|:-------------------------------------------------------------|
| `basic`  | 是      | [Basic](#basic-authentication)  | 用來存取 Confluence 主機的基本驗證憑證。  |
| `oauth2` | 是      | [OAuth 2.0](#oauth-20-authentication) | 用來存取 Confluence 主機的 OAuth 2.0 驗證憑證。 |

#### 基本驗證

存取 Confluence 網站需要基本或 OAuth 2.0 憑證。如果您使用 `basic` 驗證，則需要下列欄位。

| 選項     | 必要 | 類型   | 說明                                                                                     |
|:-----------|:---------|:-------|:------------------------------------------------------------------------------------------------|
| `username` | 是      | String | 使用者名稱，或儲存該使用者名稱的私密金鑰參照。           |
| `password` | 是      | String | 密碼 (API 金鑰)，或儲存該密碼的私密金鑰參照。 |

#### OAuth 2.0 驗證

存取 Confluence 網站需要基本或 OAuth 2.0 憑證。如果您使用 OAuth 2.0，則需要下列欄位。

| 選項          | 必要 | 類型   | 說明                                                                                     |
|:----------------|:---------|:-------|:------------------------------------------------------------------------------------------------|
| `client_id`     | 是      | String | `client_id`，或儲存該 `client_id` 的私密金鑰參照。         |
| `client_secret` | 是      | String | `client_secret`，或儲存該 `client_secret` 的私密金鑰參照。 |
| `access_token`  | 是      | String | `access_token`，或儲存該 `access_token` 的私密金鑰參照。   |
| `refresh_token` | 是      | String | `refresh_token`，或儲存該 `refresh_token` 的私密金鑰參照。 |

### 篩選

您可以選擇指定篩選條件來選取特定內容，如下表所示。如果未指定任何篩選條件，則會擷取指定憑證可見的所有空間和內容，並傳送至管線中指定的接收端。

| 選項      | 必要 | 類型   | 說明                                   |
|:------------|:---------|:-------|:----------------------------------------------|
| `space`     | 否       | String | 要包含或排除的空間索引鍵清單。         |
| `page_type` | 否       | String | 要包含或排除的頁面類型篩選條件清單。 |

### AWS 秘密

如果您打算將憑證存放在 AWS Secrets Manager 中，可以在 `aws` 秘密組態中使用下列選項。將秘密存放在 AWS Secrets Manager 中是選用的。如果未使用 AWS Secrets Manager，則必須在管線 YAML 本身中以純文字指定憑證。

如果 OAuth 2.0 驗證與 `aws` 秘密搭配使用，則此來源需要 AWS Secrets Manager 的寫入權限，才能在目前權杖過期後寫回更新 (或續約) 的存取權杖。

| 選項         | 必要 | 類型   | 說明                                                                                                                                                                                                                                                                                    |
|:---------------|:---------|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `region`       | 是      | String | 要用於憑證的 AWS 區域。預設為[決定區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。                                                                                         |
| `sts_role_arn` | 是      | String | 對 Atlassian Confluence 提出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，其使用[憑證的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。 |
| `secret_id`    | 是      | Map    | 儲存憑證之秘密的 Amazon Resource Name (ARN)。                                                                                                                                                                                                                            |

## 指標

`confluence` 來源包含下列指標 (計數器)：

* `crawlingTime`：在 Confluence 中爬梳所有新變更所花費的時間量。
* `pageFetchLatency`：頁面擷取 API 作業延遲。
* `searchCallLatency`：搜尋 API 作業延遲。
* `searchResultsFound`：在指定搜尋 API 呼叫中找到的頁面數。
