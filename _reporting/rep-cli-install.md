---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "下載並安裝 Reporting CLI 工具"
nav_order: 10
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /dashboards/reporting-cli/rep-cli-install/
---

# 下載並安裝 Reporting CLI 工具

您可以從 `npm` 套件註冊服務或 OpenSearch.org 的 [Artifacts](https://opensearch.org/artifacts) 中樞下載並安裝 Reporting CLI 工具。請參閱下列各節以取得操作說明。

如要進一步了解 `npm` 套件註冊服務，請參閱 [`npm`](https://docs.npmjs.com/about-npm) 文件。

## 從 `npm` 下載並安裝 Reporting CLI

如要從 `npm` 下載並安裝 Reporting CLI，請執行下列命令以開始安裝：

```
npm i @opensearch-project/reporting-cli
```

## 從 OpenSearch.org 下載並安裝 Reporting CLI

您可以從 OpenSearch.org 的 [Artifacts](https://artifacts.opensearch.org/reporting-cli/opensearch-reporting-cli-1.0.0.tgz) 中樞下載 `opensearch-reporting-cli` 工具。

接著，請執行下列命令以安裝 .tar 封存檔：

```
npm install -g opensearch-reporting-cli-1.0.0.tgz
```

為了提供成品更好的安全性，我們建議您下載 [Reporting CLI 簽章檔案](https://artifacts.opensearch.org/reporting-cli/opensearch-reporting-cli-1.0.0.tgz.sig) 來驗證簽章。
{: .important }

如要進一步了解如何驗證簽章，請參閱[如何驗證可下載成品的簽章](https://opensearch.org/verify-signatures.html)。