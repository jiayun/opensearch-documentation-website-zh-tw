---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搭配 Reporting CLI 使用環境變數"
nav_order: 35
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /dashboards/reporting-cli/rep-cli-env-var/
---

# 搭配 Reporting CLI 使用環境變數

您可以將值儲存為環境變數，而不必在命令列中明確提供這些值。Reporting CLI 會從專案內的目前目錄讀取環境變數。

若要在 Linux 中設定環境變數，請使用下列命令：

```
export NAME=VALUE
```

每一行都應使用 `NAME=VALUE` 格式。
以井字號（#）開頭的每一行都會被視為註解。
引號（"）不會受到任何特殊處理。

命令列引數的值比環境變數檔案中的值具有更高的優先順序。例如，若您在 *.env* 檔案中將檔案名稱設為 *test*，並且也加入 `--filename report` 命令選項，產生的報表名稱將會是 *report*。
{: .note }

#### 範例：設定環境變數後請求 PNG 報表

下列命令會使用基本驗證來請求 PNG 格式的報表：

```
opensearch-reporting-cli --url https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d --format png --auth basic --credentials admin:<custom-admin-password>
```

成功後，報表會下載至目前目錄。

## 使用 Amazon SES 請求附有報表附件的電子郵件

若要使用 Amazon SES 作為電子郵件傳輸機制，必須符合下列先決條件：

- 寄件者的電子郵件地址必須通過 [Amazon SES](https://aws.amazon.com/ses/) 驗證。與 Amazon SES 互動需要使用 [AWS Command Line Interface (AWS CLI)](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)。若要設定 AWS CLI 使用的基本設定，請參閱 AWS Command Line Interface 使用者指南中的[使用 `aws configure` 進行快速設定](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config)。
- Amazon SES 傳輸需要 `ses:SendRawEmail` 角色：

```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ses:SendRawEmail",
      "Resource": "*"
    }
  ]
}
```

下列命令會請求附有報表的電子郵件：

```
opensearch-reporting-cli --url https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d --transport ses --from <sender_email_id> --to <recipient_email_id>
```

下列命令會對所有其他選項使用預設值。您也可以在 .env 檔案中設定 `OPENSEARCH_FROM`、`OPENSEARCH_TO` 和 `OPENSEARCH_TRANSPORT`，並使用下列命令：

```
opensearch-reporting-cli --url https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d
```

若要修改電子郵件的本文，您可以編輯 *index.hbs* 檔案。

#### 範例：使用 SMTP 將報表寄送至電子郵件地址

若要使用簡易郵件傳輸通訊協定（SMTP）傳輸，將報表寄送至電子郵件地址，您需要在 .env 檔案中設定 `OPENSEARCH_SMTP_HOST`、`OPENSEARCH_SMTP_PORT`、`OPENSEARCH_SMTP_USER`、`OPENSEARCH_SMTP_PASSWORD` 和 `OPENSEARCH_SMTP_SECURE` 選項。

在 .env 檔案中設定傳輸選項後，您就可以使用下列命令寄送電子郵件：

```
opensearch-reporting-cli --url https://localhost:5601/app/dashboards#/view/7adfa750-4c81-11e8-b3d7-01146121b73d --transport smtp --from <sender_email_id> --to <recipient_email_id>
```

您可以任意組合使用 *.env* 檔案或命令列引數值來設定選項。請務必指定所有必要的值，以避免發生錯誤。

若要修改電子郵件的本文，您可以編輯 *index.hbs* 檔案。

## 限制

搭配 Reporting CLI 使用環境變數時，有下列限制：

- 支援的平台包括 Windows x86、Windows x64、Mac Intel、Mac ARM、Linux x86 和 Linux x64。
  
  對於任何其他平台，使用者可以利用 *CHROMIUM_PATH* 環境變數來使用自訂的 Chromium。

- 如果 URL 包含驚嘆號（!），則需要暫時停用歷史記錄展開功能。視您使用的 shell 而定，您可以使用下列其中一個命令來停用歷史記錄展開功能：

  * 若使用 bash，請使用 `set +H`。 
  * 若使用 `zsh`，請使用 `setopt nobanghist`。

  或者，您可以使用此格式將 URL 值新增為環境變數：`URL="<url-with-!>"`。

- 所有命令選項都只接受小寫字母。

## 疑難排解

若要解決 **MessageRejected: Email address is not verified**，請參閱 AWS 知識中心的[為什麼我會收到 Amazon SES 傳回的 400「message rejected」錯誤，並顯示「Email address is not verified」訊息？](https://repost.aws/knowledge-center/ses-554-400-message-rejected-error)。