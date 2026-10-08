---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Debian
parent: Installing OpenSearch Dashboards
nav_order: 20
---

{% comment %}
The following liquid syntax declares a variable, major_version_mask, which is transformed into "N.x" where "N" is the major version number. This is required for proper versioning references to the Yum repo.
{% endcomment %}
{% assign version_parts = site.opensearch_major_minor_version | split: "." %}
{% assign major_version_mask = version_parts[0] | append: ".x" %}

# 在 Debian 上安裝 OpenSearch Dashboards

使用 Advanced Packaging Tool (APT) 套件管理員安裝 OpenSearch Dashboards，與 [Tarball]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tar/) 方法相比，能大幅簡化安裝過程。例如，套件管理員會處理多項技術考量，例如安裝路徑、組態檔案位置以及建立由 `systemd` 管理的服務。

本指南假設您熟悉 Linux 命令列介面 (CLI) 的操作。您應該了解如何輸入命令、在目錄之間切換以及編輯文字檔案。部分範例命令參考了 `vi` 文字編輯器，但您可以使用任何可用的文字編輯器。
{:.note}

## 前置條件

安裝 OpenSearch。如需更多資訊，請參閱 [在 Debian 上安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/debian/)。

## 從套件安裝 OpenSearch Dashboards

1. 直接從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載所需版本的 Debian 套件。Debian 套件支援 **x64** 和 **arm64** 架構。
1. 從 CLI 使用 `dpkg` 進行安裝。

   x64:
   ```bash
   sudo dpkg -i opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.deb
   ```
   {% include copy.html %}

   arm64:
   ```bash
   sudo dpkg -i opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-arm64.deb
   ```
   {% include copy.html %}

   對於 OpenSearch Dashboards 3.7 及後續版本的新安裝，您可以使用以下環境變數來控制 Security Dashboards 外掛程式的行為：
   ```bash
   DISABLE_SECURITY_DASHBOARDS_PLUGIN=true
   ```
   {% include copy.html %}

1. 安裝完成後，重新載入 `systemd` 管理員組態：
    ```bash
    sudo systemctl daemon-reload
    ```
    {% include copy.html %}

1. 將 OpenSearch Dashboards 啟用為服務：
    ```bash
    sudo systemctl enable opensearch-dashboards
    ```
    {% include copy.html %}

1. 啟動 OpenSearch Dashboards 服務：
    ```bash
    sudo systemctl start opensearch-dashboards
    ```
    {% include copy.html %}

1. 驗證 OpenSearch Dashboards 是否正確啟動：
    ```bash
    sudo systemctl status opensearch-dashboards
    ```
    {% include copy.html %}

1. 在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行在遠端主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

### 指紋驗證

Debian 套件未經過簽署。如果您想要驗證指紋，OpenSearch Project 提供了 `.sig` 檔案以及可用於 GNU Privacy Guard (GPG) 的 `.deb` 套件。

1. 下載所需的 Debian 套件：
   ```bash
   curl -SLO https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.deb
   ```
   {% include copy.html %}

1. 下載對應的簽署檔案：
   ```bash
   curl -SLO https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{site.opensearch_dashboards_version}}/opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.deb.sig
   ```
   {% include copy.html %}

1. 下載並匯入 GPG 金鑰：
   ```bash
   curl -o- https://artifacts.opensearch.org/publickeys/opensearch-release.pgp | gpg --import -
   ```
   {% include copy.html %}

1. 驗證簽署：
   ```bash
   gpg --verify opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.deb.sig opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.deb
   ```
   {% include copy.html %}

## 從 APT 儲存庫安裝 OpenSearch Dashboards

APT 是基於 Debian 的作業系統主要套件管理工具，允許您從 APT 儲存庫下載並安裝 Debian 套件。

1. 安裝必要套件：
   ```bash
   sudo apt-get update && sudo apt-get -y install lsb-release ca-certificates curl gnupg2
   ```
   {% include copy.html %}

1. 如果 keyrings 目錄尚不存在，請建立該目錄：
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   ```
   {% include copy.html %}

1. 匯入公開 GPG 金鑰。此金鑰用於驗證 APT 儲存庫是否經過簽署。
    ```bash
    curl -o- https://artifacts.opensearch.org/publickeys/opensearch-release.pgp | sudo gpg --dearmor --batch --yes -o /etc/apt/keyrings/opensearch-release-keyring
    ```
    {% include copy.html %}

1. 為 OpenSearch Dashboards 建立 APT 儲存庫：
   ```bash
   echo "deb [signed-by=/etc/apt/keyrings/opensearch-release-keyring] https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{major_version_mask}}/apt stable main" | sudo tee /etc/apt/sources.list.d/opensearch-dashboards-{{major_version_mask}}.list
   ```
   {% include copy.html %}

1. 驗證儲存庫是否成功建立：
    ```bash
    sudo apt-get update
    ```
    {% include copy.html %}

1. (選用) 自 2024 年 5 月 22 日起，APT 儲存庫的 `Origin` 和 `Label` 值已作為 [此變更](https://github.com/opensearch-project/opensearch-build/issues/4485) 的一部分進行更新。如果您在此日期之前建立了 APT 儲存庫，請執行以下命令以接受更新後的發行資訊：
    ```bash
    sudo apt-get update --allow-releaseinfo-change
    ```
    {% include copy.html %}

1. 在加入儲存庫資訊後，列出所有可用的 OpenSearch Dashboards 版本：
   ```bash
   sudo apt list -a opensearch-dashboards
   ```
   {% include copy.html %}

1. 選擇您想要安裝的 OpenSearch Dashboards 版本：
   - 除非另有說明，否則將安裝最新可用的 OpenSearch Dashboards 版本：
   ```bash
   sudo apt-get install opensearch-dashboards
   ```
   {% include copy.html %}

   - 若要安裝特定版本的 OpenSearch Dashboards，請在套件名稱後傳遞版本號碼：
   ```bash
   sudo apt-get install opensearch-dashboards={{site.opensearch_dashboards_version}}
   ```
   {% include copy.html %}

1. 完成後，啟用 OpenSearch Dashboards：
    ```bash
    sudo systemctl enable opensearch-dashboards
    ```
    {% include copy.html %}

1. 啟動 OpenSearch Dashboards：
    ```bash
    sudo systemctl start opensearch-dashboards
    ```
    {% include copy.html %}

1. 驗證 OpenSearch Dashboards 是否正確啟動：
    ```bash
    sudo systemctl status opensearch-dashboards
    ```
    {% include copy.html %}

1. 在網頁瀏覽器中，前往 `http://localhost:5601` 並使用您在安裝 OpenSearch 時設定的自訂管理員密碼，以 `admin` 使用者身分登入。如果 OpenSearch Dashboards 執行在遠端主機上，請將 `localhost` 替換為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱 [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

## (選用) 允許來自其他主機的存取

預設情況下，OpenSearch Dashboards 與 OpenSearch 一樣，在初次安裝時會綁定到 `localhost`。因此，除非更新組態，否則無法從遠端主機存取 OpenSearch Dashboards。

1. 開啟 `opensearch_dashboards.yml`：
    ```bash
    sudo vi /etc/opensearch-dashboards/opensearch_dashboards.yml
    ```
    {% include copy.html %}

1. 指定 OpenSearch Dashboards 應綁定的網路介面。使用 `0.0.0.0` 可綁定到任何可用的介面：
    ```bash
    server.host: 0.0.0.0
    ```
    {% include copy.html %}

1. 儲存並退出。
1. 重新啟動 OpenSearch Dashboards 以套用組態變更：
    ```bash
    sudo systemctl restart opensearch-dashboards
    ```
    {% include copy.html %}

## 升級至較新版本

使用 `dpkg` 或 `apt-get` 安裝的 OpenSearch Dashboards 執行個體可以升級至較新版本。

在升級 OpenSearch Dashboards 之前，請先升級您的 OpenSearch 叢集。OpenSearch Dashboards 必須執行與其連接的叢集相同的版本，且安裝的外掛程式必須與該版本相符。如需更多資訊，請參閱 [外掛程式相容性]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/#plugin-compatibility)。
{: .important}

### 為升級準備主機

`opensearch-dashboards` 套件不宣告對其他 Debian 套件的依賴關係。因此，若升級因未解決的依賴關係而失敗，則是指向主機上的 APT 組態而非 OpenSearch Dashboards 本身。在執行升級命令之前，請完成以下步驟。

1. 安裝 APT 用於透過 HTTPS 讀取 OpenSearch Dashboards 儲存庫所需的套件：
   ```bash
   sudo apt-get update && sudo apt-get -y install lsb-release ca-certificates curl gnupg2
   ```
   {% include copy.html %}

1. 備份您的組態。該套件將下列檔案註冊為組態檔案，且 `dpkg` 會提示您保留或替換每個您編輯過的檔案：

   - `/etc/opensearch-dashboards/opensearch_dashboards.yml`
   - `/etc/opensearch-dashboards/node.options`
   - `/etc/default/opensearch-dashboards`
   - `/etc/init.d/opensearch-dashboards`

   若要備份主組態檔案，請執行下列命令：
   ```bash
   sudo cp /etc/opensearch-dashboards/opensearch_dashboards.yml /etc/opensearch-dashboards/opensearch_dashboards.yml.bak
   ```
   {% include copy.html %}

   請從互動式 shell 執行升級，以便您可以回應這些提示。非互動式升級會停在提示處，或套用主機上 `Dpkg::Options` 中設定的預設答案。
   {: .note}

1. 重新整理套件清單並確認有可用之較新版本：
   ```bash
   sudo apt-get update && sudo apt list -a opensearch-dashboards
   ```
   {% include copy.html %}

   如果 `apt-get update` 回報公鑰不可用，或者列出的最新版本是您已經擁有的版本，請參閱 [跨主版本升級](#upgrade-across-major-versions)。

### 使用 `dpkg` 手動升級

直接從 [OpenSearch Project 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'}下載所需升級版本的 Debian 套件。

導航至包含發行版本的目錄並執行下列命令：

```bash
sudo dpkg -i opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.deb
```
{% include copy.html %}

此方法直接讀取套件檔案且不使用 APT 儲存庫，因此它也可以跨主版本升級。
{: .tip}

### 使用 `apt-get` 升級

若要升級到最新可用版本的 OpenSearch Dashboards，請執行下列命令：

```bash
sudo apt-get install --only-upgrade opensearch-dashboards
```
{% include copy.html %}

您也可以透過提供版本號碼來升級到特定的 OpenSearch Dashboards 版本：

```bash
sudo apt-get install opensearch-dashboards=<version>
```
{% include copy.html %}

`apt-get upgrade` 子命令作用於主機上每個已安裝的套件，且無法安裝或移除套件，因此若 APT 暫緩更新不相關的套件，會導致 OpenSearch Dashboards 升級停止。`--only-upgrade` 選項將操作限制在 `opensearch-dashboards` 套件。
{: .note}

### 跨主版本升級

您在安裝期間建立的儲存庫定義被固定在一個主版本，因此當您嘗試遷移到不同的主版本時，APT 會回報沒有較新版本。不同主版本的儲存庫也使用不同的 GPG 金鑰簽署，因此當 APT 使用您現有的金鑰環讀取新儲存庫時，會回報缺少公鑰。

1. 匯入新儲存庫的公用 GPG 金鑰：
   ```bash
   curl -o- https://artifacts.opensearch.org/publickeys/opensearch-release.pgp | sudo gpg --dearmor --batch --yes -o /etc/apt/keyrings/opensearch-release-keyring
   ```
   {% include copy.html %}

   OpenSearch Dashboards 2.x 的儲存庫使用發佈在 `https://artifacts.opensearch.org/publickeys/opensearch.pgp` 的金鑰簽署。在您移除 2.x 儲存庫定義之前，請保留該金鑰的金鑰環。否則，`apt-get update` 在讀取 2.x 儲存庫時會失敗。
   {: .note}

1. 新增新主版本的儲存庫：
   ```bash
   echo "deb [signed-by=/etc/apt/keyrings/opensearch-release-keyring] https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{major_version_mask}}/apt stable main" | sudo tee /etc/apt/sources.list.d/opensearch-dashboards-{{major_version_mask}}.list
   ```
   {% include copy.html %}

1. 移除先前主版本的儲存庫定義，將 `<previous-major-version>` 替換為如 `2.x` 之類的值：
   ```bash
   sudo rm /etc/apt/sources.list.d/opensearch-dashboards-<previous-major-version>.list
   ```
   {% include copy.html %}

1. 重新整理套件清單並確認新版本已出現：
   ```bash
   sudo apt-get update && sudo apt list -a opensearch-dashboards
   ```
   {% include copy.html %}

1. 安裝新版本：
   ```bash
   sudo apt-get install opensearch-dashboards=<version>
   ```
   {% include copy.html %}

### 在套件升級後自動重新啟動服務

若要在套件升級後自動重新啟動 OpenSearch Dashboards，請透過 `systemd` 啟用 `opensearch-dashboards.service`：

```bash
sudo systemctl enable opensearch-dashboards.service
```
{% include copy.html %}

## 相關文件

- [準備將 OpenSearch Dashboards 用於生產環境]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
