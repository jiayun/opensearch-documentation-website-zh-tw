---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Atlassian Jira
parent: Sources
grand_parent: Pipelines
nav_order: 7
canonical_url: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/atlassian-jira/
redirect_to: https://docs.opensearch.org/latest/data-prepper/pipelines/configuration/sources/atlassian-jira/
---

# Atlassian Jira 來源

您可以使用 OpenSearch Data Prepper `jira` 來源，從一或多個 [Atlassian Jira](https://www.atlassian.com/software/jira) 專案匯入記錄。

## 使用方式

請從下列選項中選擇一種，設定 Jira 專案存取認證資訊：

- **基本驗證**（API 金鑰驗證）：請依照[這些說明](https://support.atlassian.com/atlassian-account/docs/manage-api-tokens-for-your-atlassian-account/)操作。
- **OAuth 2.0 驗證**：請依照[這些說明](https://developer.atlassian.com/cloud/jira/platform/oauth-2-3lo-apps/#faq-rrt-config)操作。

您也可以選擇另外將認證資訊儲存在 AWS Secrets Manager 中。如果您未將認證資訊儲存在 AWS Secrets Manager 中，則必須直接在管線組態中提供純文字認證資訊。

下列範例管線將 `jira` 指定為來源。此管線會從名為 `project1` 和 `project2` 的 Jira 專案匯入資料，並套用篩選條件，從這些專案中選取票證作為來源：

```yaml
version: "2"
extension:
  aws:
    secrets:
      jira-account-credentials:
        secret_id: "arn:aws:secretsmanager:us-east-1:123456789012:secret:jira-credentials-secret"
        region: "us-east-1"
        sts_role_arn: "arn:aws:iam::123456789012:role/Example-Role"
atlassian-jira-pipeline:
  source:
    jira:
      hosts: ["https://example.atlassian.net/"]
      acknowledgments: true
      authentication:
        # Provide one of the authentication method to use. Supported methods are 'basic' and 'oauth2'.
        # For basic authentication, password is the API key that you generate using your jira account
        basic:
          username: {% raw %}  ${{aws_secrets:jira-account-credentials:username}} {% endraw %} 
          password: {% raw %}  ${{aws_secrets:jira-account-credentials:password}} {% endraw %} 
          # For OAuth 2.0-based authentication, we require the following 4 key values stored in the secret
          # Follow atlassian instructions at the following link to generate these keys
          # https://developer.atlassian.com/cloud/confluence/oauth-2-3lo-apps/
          # If you are using OAuth 2.0 authentication, we also require, write permission to your aws secret to
          # be able to write the renewed tokens back into the secret
          # oauth2:
          # client_id: {% raw %} ${{aws_secrets:jira-account-credentials:clientId}} {% endraw %} 
          # client_secret: {% raw %} ${{aws_secrets:jira-account-credentials:clientSecret}} {% endraw %} 
          # access_token: {% raw %} ${{aws_secrets:jira-account-credentials:accessToken}} {% endraw %} 
          # refresh_token: {% raw %} ${{aws_secrets:jira-account-credentials:refreshToken}} {% endraw %} 
      filter:
        project:
          key:
            include:
              # This is not project name.
              # It is an alphanumeric project key that you can find under project details in jira
              - "PROJECT1"
              - "PROJECT2"
              # exclude:
              # - "<<project key>>"
              # - "<<project key>>"
        issue_type:
          include:
            - "Story"
              # - "Bug"
              # - "Task"
              # exclude:
            # - "Epic"
        status:
          include:
            - "To Do"
            # - "In Progress"
            # - "Done"
            # exclude:
            # - "Backlog"
```
{% include copy.html %}

## 組態選項

`jira` 來源支援下列組態選項。

| 選項 | 必要 | 類型 | 說明 |
|:------------------|:---------|:----------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `hosts` | 是 | 清單 | Atlassian Jira 主機名稱。目前僅支援一個主機，因此此清單的大小應為 1。 |
| `acknowledgments` | 否 | 布林值 | 設定為 `true` 時，可讓 `jira` 來源在 OpenSearch 接收器 (sink) 收到事件時接收[端對端確認]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#end-to-end-acknowledgments)。 |
| `authentication` | 是 | [驗證](#Authentication) | 設定用於從指定主機存取 `jira` 來源記錄的驗證方法。 |
| `filter` | 否 | [篩選器](#Filter) | 在擷取 Jira 工單時套用特定的篩選條件。 |

### 驗證

您可以使用下列其中一種驗證方法來存取指定的 Jira 主機。您必須提供下列其中一個參數。

| 選項   | 必要 | 類型              | 說明                                            |
|:---------|:---------|:------------------|:-------------------------------------------------------|
| `basic`  | 是      | [Basic](#basic-authentication)   | 用於存取 Jira 主機的基本驗證認證資訊。  |
| `oauth2` | 是      | [OAuth 2.0](#oauth-20-authentication)| 用於存取 Jira 主機的 OAuth 2.0 驗證認證資訊。 |

#### 基本驗證

存取 Jira 網站需要基本驗證或 OAuth 2.0 驗證的認證資訊。如果您使用 `basic` 驗證，則下列欄位為必要欄位。

| 選項     | 必要 | 類型   | 說明                                                                                     |
|:-----------|:---------|:-------|:------------------------------------------------------------------------------------------------|
| `username` | 是      | 字串 | 使用者名稱，或儲存使用者名稱之秘密金鑰的參照。           |
| `password` | 是      | 字串 | 密碼（API 金鑰），或儲存密碼之秘密金鑰的參照。 |

#### OAuth 2.0 驗證

存取 Jira 網站需要基本驗證或 OAuth 2.0 驗證的認證資訊。如果您使用 OAuth 2.0，則下列欄位為必要欄位。

| 選項          | 必要 | 類型   | 說明                                                                                     |
|:----------------|:---------|:-------|:------------------------------------------------------------------------------------------------|
| `client_id`     | 是      | 字串 | `client_id`，或儲存 `client_id` 之秘密金鑰的參照。         |
| `client_secret` | 是      | 字串 | `client_secret`，或儲存 `client_secret` 之秘密金鑰的參照。 |
| `access_token`  | 是      | 字串 | `access_token`，或儲存 `access_token` 之秘密金鑰的參照。   |
| `refresh_token` | 是      | 字串 | `refresh_token`，或儲存 `refresh_token` 之秘密金鑰的參照。 |

### 篩選條件

您可以選擇性地指定篩選條件，以選取特定內容。若未指定任何篩選條件，系統會擷取指定認證資訊可見的所有專案與工單，並傳送至管線中指定的接收器 (sink)。

| 選項       | 必要 | 類型   | 說明                                    |
|:-------------|:---------|:-------|:-----------------------------------------------|
| `project`    | 否       | 物件 | 依專案篩選工單 (issue)。包含 `key` 物件，此物件接受由專案索引鍵組成的 `include` 與 `exclude` 清單。每個專案索引鍵的長度必須為 2 到 100 個字元，且只能包含大寫英文字母與數字。同一個專案索引鍵不得同時出現在兩份清單中。 |
| `issue_type` | 否       | 物件 | 依工單類型篩選工單。接受由工單類型名稱組成的 `include` 與 `exclude` 清單，例如 `Story` 或 `Bug`。 |
| `status`     | 否       | 物件 | 依狀態篩選工單。接受由狀態名稱組成的 `include` 與 `exclude` 清單，例如 `In Progress` 或 `Done`。 |

來源會在開始爬取時驗證專案索引鍵。若專案篩選條件包含無效的索引鍵，來源會記錄錯誤，且不會匯入任何工單。

### AWS 秘密

如果您打算將認證資訊儲存在 AWS Secrets Manager 中，可以在 `aws` 秘密組態中使用下列選項。將秘密儲存在 AWS Secrets Manager 中為選用。如果未使用 AWS Secrets Manager，則必須直接在管線 YAML 中以純文字指定認證資訊。

如果將 OAuth 2.0 驗證與 `aws` 秘密搭配使用，此來源需要該秘密的寫入權限，才能在目前的權杖到期時寫回已更新（或已續期）的存取權杖。

| 選項         | 必要 | 類型   | 說明                                                                                                                                                                                                                                                                                    |
|:---------------|:---------|:-------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `region`       | 是      | 字串 | 用於認證資訊的 AWS 區域。預設採用[判斷區域的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/region-selection.html)。                                                                                         |
| `sts_role_arn` | 是      | 字串 | 向 Atlassian Jira 發出請求時要擔任的 AWS Security Token Service (AWS STS) 角色。預設為 `null`，即使用[認證資訊的標準 SDK 行為](https://docs.aws.amazon.com/sdk-for-java/latest/developer-guide/credentials.html)。 |
| `secret_id`    | 是      | Map    | 儲存認證資訊之秘密的 Amazon Resource Name (ARN)。                                                                                                                              

## 指標

`jira` 來源包含下列指標（計數器）：

* `crawlingTime`：爬取 Jira 中所有新變更所花費的時間。
* `ticketFetchLatency`：工單擷取 API 操作的延遲。
* `searchCallLatency`：搜尋 API 操作的延遲。
* `searchResultsFound`：在指定的搜尋 API 呼叫中找到的工單數量。
