---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 CLI 產生報告"
nav_order: 20
parent: Reporting
has_children: true
redirect_from:
  - /reporting/rep-cli-index/
  - /dashboards/reporting-cli/rep-cli-index/
---

# 使用 CLI 產生報告

使用 Reporting CLI 從指令碼或排程器產生報告，不必在瀏覽器中開啟 OpenSearch Dashboards。Reporting CLI 會在無頭 Chromium 瀏覽器中開啟儀表板、視覺化、筆記本或已儲存搜尋的 URL，擷取頁面，然後將報告儲存到目前目錄，或使用 Amazon Simple Email Service (Amazon SES) 或 SMTP 以電子郵件附件形式傳送。

Reporting CLI 會從執行中的 OpenSearch Dashboards 執行個體載入頁面，因此執行 Reporting CLI 的機器必須能夠連線到該執行個體。

Reporting CLI 支援下列報告格式：

- 儀表板、視覺化與筆記本的 PDF 和 PNG 報告。這些報告不需要 Reporting 外掛程式。
- 已儲存搜尋的 CSV 報告。Reporting CLI 使用 **Discover** 中的 **Reporting** 功能表產生 CSV 報告，因此 CSV 報告需要在 OpenSearch Dashboards 中安裝 Reporting 外掛程式。

若要連線至 OpenSearch Dashboards，Reporting CLI 支援下列驗證類型：

- 基本 HTTP 驗證：指定 `-a basic` 並提供認證資訊。
- Amazon Cognito 驗證：指定 `-a cognito` 並提供認證資訊。若要進一步瞭解 Amazon Cognito，請參閱[什麼是 Amazon Cognito？](https://docs.aws.amazon.com/cognito/latest/developerguide/what-is-amazon-cognito.html)。
- 使用 Okta 作為身分提供者的 SAML 驗證：指定 `-a saml` 並提供認證資訊。
- 不驗證：省略 `-a` 選項。

若要開始使用，請參閱[下載並安裝 Reporting CLI 工具]({{site.url}}{{site.baseurl}}/dashboards/reporting/rep-cli-install/)。
