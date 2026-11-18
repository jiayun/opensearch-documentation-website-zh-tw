---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Atlassian Confluence
parent: Sources
grand_parent: Pipelines
nav_order: 5
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/atlassian-confluence/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/atlassian-confluence/
---

# Atlassian Confluence 來源

您可以使用 OpenSearch Data Prepper `confluence` 來源，從一或多個 [Atlassian Confluence](https://www.atlassian.com/software/confluence) 空間匯入記錄。

## 用法

請選擇下列其中一個選項，設定 Confluence 專案的存取認證資訊：

- **基本驗證**（API 金鑰驗證）：請依照[這些說明](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)操作。
- **OAuth 2.0 驗證**：請依照[這些說明](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/#faq-rrt-config)操作。
- **Bearer 權杖驗證**：提供一個權杖，來源會在每個請求的 `Authorization: Bearer` 標頭中傳送此權杖。

您也可以選擇額外執行一個步驟，將認證資訊儲存在 AWS Secrets Manager 中。如果您未將認證資訊儲存在 AWS Secrets Manager 中，則必須直接在管線組態中提供純文字認證資訊。

下列範例管線將 `confluence` 指定為來源。此管線會從名為 `space1` 和 `space2` 的多個 Confluence 空間匯入資料，並套用篩選條件，從這些專案中選取 wiki 內容（頁面和部落格文章）作為來源：

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
        # Provide one of the authentication method to use. Supported methods are 'basic', 'oauth2', and 'bearer_token'.
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

| 選項 | 必要 | 類型 | 說明 |
|:------------------|:---------|:----------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hosts` | 是 | 清單 | Atlassian Confluence 主機名稱。目前僅支援一個主機，因此此清單的大小應為 1。 |
| `acknowledgments` | 否 | 布林值 | 設定為 `true` 時，可讓 `confluence` 來源在 OpenSearch 接收器收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。 |
| `preserve_formatting` | 否 | 布林值 | 設定為 `true` 時，Confluence 內容的格式標記標籤會保持原樣。預設為 `false`（移除標記標籤並轉換為純文字）。 |
| `allow_internal_address` | 否 | 布林值 | 設定為 `true` 時，允許 `hosts` 中指定的主機解析為私人、迴路或鏈路本機 IP 位址。設定為 `false` 時，來源會拒絕解析為這些位址的主機。預設為 `false`。 |
| `authentication` | 是 | [驗證](#Authentication) | 設定從指定主機存取 `confluence` 來源記錄時所使用的驗證方法。 |
| `filter` | 否 | [篩選器](#Filter) | 擷取 Confluence 內容時套用特定的篩選條件。 |

### 驗證

請使用下列其中一種驗證方法存取 Confluence 主機。您必須提供下列參數中的恰好一個。

| 選項   | 必要 | 類型              | 說明                                                  |
|:---------|:---------|:------------------|:-------------------------------------------------------------|
| `basic`  | 是      | [Basic](#basic-authentication)  | 用於存取 Confluence 主機的基本驗證認證資訊。  |
| `oauth2` | 是      | [OAuth 2.0](#oauth-20-authentication) | 用於存取 Confluence 主機的 OAuth 2.0 驗證認證資訊。 |
| `bearer_token` | 是 | 字串 | 持有人權杖（bearer token），或指向儲存該持有人權杖之秘密金鑰的參照。來源會在每個請求的 `Authorization: Bearer` 標頭中傳送此權杖。如果權杖儲存在 AWS Secrets Manager 中，當主機傳回 `401` 回應時，來源會重新載入秘密值。 |

#### 基本驗證

如果您使用 `basic` 驗證，則必須提供下列欄位。

| 選項 | 必要 | 類型 | 說明 |
|:-----------|:---------|:-------|:------------------------------------------------------------------------------------------------|
| `username` | 是 | 字串 | 使用者名稱，或儲存使用者名稱之秘密金鑰的參照。 |
| `password` | 是 | 字串 | 密碼（API 金鑰），或儲存密碼之秘密金鑰的參照。 |

#### OAuth 2.0 驗證

如果您使用 OAuth 2.0，則必須提供下列欄位。

| 選項          | 必要 | 類型   | 說明                                                                                     |
|:----------------|:---------|:-------|:------------------------------------------------------------------------------------------------|
| `client_id`     | 是      | 字串 | `client_id`，或對儲存 `client_id` 之秘密金鑰的參照。         |
| `client_secret` | 是      | 字串 | `client_secret`，或對儲存 `client_secret` 之秘密金鑰的參照。 |
| `access_token`  | 是      | 字串 | `access_token`，或對儲存 `access_token` 之秘密金鑰的參照。   |
| `refresh_token` | 是      | 字串 | `refresh_token`，或對儲存 `refresh_token` 之秘密金鑰的參照。 |

### 篩選條件

您可以選擇性地指定篩選條件來選取特定內容，如下表所示。若未指定任何篩選條件，則會擷取指定認證資訊可見的所有空間與內容，並傳送至管線中指定的接收器 (sink)。

| 選項      | 必要 | 類型   | 說明                                   |
|:------------|:---------|:-------|:----------------------------------------------|
| `space`     | 否       | 物件 | 依空間篩選內容。包含 `key` 物件，此物件接受由空間鍵 (space key) 組成的 `include` 與 `exclude` 清單。請使用空間鍵，而非空間名稱。每個空間鍵的長度必須為 2 至 100 個字元，且只能包含字母與數字。同一個空間鍵不能同時出現在兩份清單中。 |
| `page_type` | 否       | 物件 | 依類型篩選內容。接受由內容類型組成的 `include` 與 `exclude` 清單。有效值為 `page`、`blogpost`、`comment` 與 `attachment`。同一個內容類型不能同時出現在兩份清單中。 |

來源會在開始爬取時驗證篩選條件的值。若篩選條件包含無效的值，來源會記錄錯誤，且不會匯入內容。

### AWS 秘密

如果您打算將認證資訊儲存在 AWS Secrets Manager 中，可以在 `aws` 秘密組態中使用下列選項。將秘密儲存在 AWS Secrets Manager 中是選用的。如果未使用 AWS Secrets Manager，則必須在管線 YAML 本身中以純文字指定認證資訊。

如果 OAuth 2.0 驗證與 `aws` 秘密搭配使用，則此來源需要 AWS Secrets Manager 的寫入權限，才能在目前權杖過期後寫回更新（或續期）的存取權杖。

| 選項         | 必要 | 類型   | 說明                                                                                                                                                                                                                                                                                    |
|:---------------|:---------|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `region`       | 是      | 字串 | 要用於認證資訊的 AWS 區域。預設為[決定區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。                                                                                         |
| `sts_role_arn` | 是      | 字串 | 對 Atlassian Confluence 提出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，其使用[認證資訊的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。 |
| `secret_id`    | 是      | 對應    | 儲存認證資訊之秘密的 Amazon Resource Name (ARN)。                                                                                                                                                                                                                            |

## 指標

`confluence` 來源包含下列指標 (計數器)：

* `crawlingTime`：在 Confluence 中爬梳所有新變更所花費的時間量。
* `pageFetchLatency`：頁面擷取 API 作業延遲。
* `searchCallLatency`：搜尋 API 作業延遲。
* `searchResultsFound`：在指定搜尋 API 呼叫中找到的頁面數。
