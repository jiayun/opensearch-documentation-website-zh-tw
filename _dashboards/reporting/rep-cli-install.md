---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "下載並安裝 Reporting CLI 工具"
nav_order: 10
parent: Reporting using the CLI
grand_parent: Reporting
redirect_from:
  - /reporting/rep-cli-install/
  - /dashboards/reporting-cli/rep-cli-install/
---

# 下載並安裝 Reporting CLI 工具

您可以從 `npm` 軟體套件庫，或從 OpenSearch.org 下載的封存檔安裝 Reporting CLI 工具。Reporting CLI 需要 Node.js。

如要進一步了解 `npm` 軟體套件庫，請參閱 [`npm`](https://docs.npmjs.com/about-npm) 文件。

## 從 npm 安裝 Reporting CLI

若要從 `npm` 安裝 Reporting CLI，請執行下列命令：

```bash
npm install -g @opensearch-project/reporting-cli
```
{% include copy.html %}

`-g` 選項會以全域方式安裝 Reporting CLI，讓您可以在每個目錄中使用 `opensearch-reporting-cli` 命令。如果您安裝套件時未使用 `-g`，請在安裝目錄中使用 `npx opensearch-reporting-cli` 執行該命令。

## 從封存檔安裝 Reporting CLI

下載 [Reporting CLI 封存檔](https://artifacts.opensearch.org/reporting-cli/opensearch-reporting-cli-1.1.0.tgz)，然後執行下列命令來安裝該封存檔：

```bash
npm install -g opensearch-reporting-cli-1.1.0.tgz
```
{% include copy.html %}

若要確認該封存檔是由 OpenSearch Project 發布且未經修改，請使用 [Reporting CLI 簽章檔案](https://artifacts.opensearch.org/reporting-cli/opensearch-reporting-cli-1.1.0.tgz.sig)驗證其簽章。
{: .important }

若要進一步了解如何驗證簽章，請參閱[如何驗證可下載成品的簽章](https://opensearch.org/verify-signatures/)。

## 驗證安裝

若要驗證安裝並列出所有可用選項，請執行下列命令：

```bash
opensearch-reporting-cli -h
```
{% include copy.html %}

## Chromium

Reporting CLI 使用 Chromium 來產生報表，Chromium 是由 `npm` 在安裝期間執行 Puppeteer 安裝指令碼時下載的。如果您的 `npm` 組態略過安裝指令碼，就不會下載 Chromium。

在所有 macOS 電腦上，下載的 Chromium 都是 x86-64 二進位檔。在配備 Apple 晶片的 Mac 上，若未安裝 Rosetta 2，Reporting CLI 會失敗並出現錯誤 `spawn Unknown system error -86`。

若要使用不同的 Chromium 或 Chrome 二進位檔，例如 Arm64 組建或由套件管理器安裝的瀏覽器，請將 `CHROMIUM_PATH` 環境變數設為瀏覽器執行檔的路徑：

```bash
export CHROMIUM_PATH=<path-to-chromium-executable>
```
{% include copy.html %}
