---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 CLI 產生報告"
nav_order: 10
has_children: true
redirect_from:
  - /dashboards/reporting-cli/rep-cli-index/
---

# 使用 CLI 產生報告

您可以使用 Reporting CLI 以程式設計方式建立 PDF 或 PNG 格式的儀表板報告，而不需使用 OpenSearch Dashboards 或 Reporting 外掛程式。這讓您可以在電子郵件工作流程中自動建立報告。

如果您想下載 CSV 檔案，則必須安裝 Reporting 外掛程式。
{: .note }

對於任何儀表板檢視，您都可以請求以 PNG 或 PDF 格式將報告傳送至電子郵件地址。這對於透過電子郵件別名將報告傳送給多位收件者非常實用。唯一支援建立 CSV 報告的儀表板應用程式是 **Discover**。

透過 Reporting CLI，您可以在命令列中指定報告的選項。報告預設會以 PDF 附件形式傳送至電子郵件地址。您也可以使用 `--formats` 參數請求 PNG 圖片或 CSV 檔案。

您可以將報告下載到執行 Reporting CLI 的目錄中，也可以透過在電子郵件傳輸選項中指定 Amazon Simple Email Service (Amazon SES) 或 SMTP 來以電子郵件傳送報告。

您可以使用下列任一驗證類型連線至 OpenSearch：

- **Basic** – 基本 HTTP 驗證。使用 `-a basic`。
- **Cognito** – 透過 Amazon Cognito 進行驗證。使用 `-a cognito`。
- **SAML** – 身分識別提供者與服務提供者之間的驗證。使用 `-a saml`。Okta 提供 SAML 第三方驗證。
<!-- vale off -->
- **No auth** – 無驗證。使用 `-a none`。如果未指定 `-a` 旗標，驗證預設為無驗證。
<!-- vale on -->

若要進一步了解 Amazon Cognito，請參閱[什麼是 Amazon Cognito？](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)。

<!--
### Bypass authentication option

The Reporting CLI tool allows you to integrate it into your own workflow or environment so that you can bypass authentication or potential security issues. For example, if you use the Reporting CLI tool within an AWS Lambda instance, no security issues would occur as long as you run the Reporting plugin in OpenSearch Dashboards. In this case, you would use "No auth" to bypass the authentication process. To specify "No Auth" use `--auth none` in your request. Lambda users should test to make sure they can bypass access to Dashboards without credentials using No Auth.  

To get a list of all options, see [Reporting CLI options](#reporting-cli-options).
-->