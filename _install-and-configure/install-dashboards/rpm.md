---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: RPM
parent: Installing OpenSearch Dashboards
nav_order: 25
redirect_from: 
  - /dashboards/install/rpm/
---

{% comment %}
The following liquid syntax declares a variable, major_version_mask, which is transformed into "N.x" where "N" is the major version number. This is required for proper versioning references to the Yum repo.
{% endcomment %}
{% assign version_parts = site.opensearch_major_minor_version | split: "." %}
{% assign major_version_mask = version_parts[0] | append: ".x" %}

# 使用 RPM 安裝 OpenSearch Dashboards

OpenSearch Dashboards 是 OpenSearch 資料的預設視覺化工具。它同時也是許多 OpenSearch 外掛程式的使用者介面，包括安全性、警示、Index State Management、SQL 等。

## 必要條件

安裝 OpenSearch。如需更多資訊，請參閱[使用 RPM 安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/rpm/)。

## 從套件安裝 OpenSearch Dashboards

1. 直接從 [OpenSearch 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'} 下載所需版本的 RPM Package Manager (RPM) 套件。RPM 套件可下載 **x64** 與 **arm64** 兩種架構的版本。
1. 匯入公開 GPG 金鑰。此金鑰可驗證您的 OpenSearch 執行個體已簽署。
    ```bash
    sudo rpm --import https://artifacts.opensearch.org/publickeys/opensearch-release.pgp
    ```
    {% include copy.html %}

1. 在命令列介面 (CLI) 中，您可以使用 `rpm` 或 `yum` 安裝套件。

    **x64**

    使用 yum 安裝 x64 套件：
    ```bash
    sudo yum install opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.rpm
    ```
    {% include copy.html %}

    使用 rpm 安裝 x64 套件：
    ```bash
    sudo rpm -ivh opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.rpm
    ```
    {% include copy.html %}

    **arm64**

    使用 yum 安裝 arm64 套件：
    ```bash
    sudo yum install opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-arm64.rpm
    ```
    {% include copy.html %}

    使用 rpm 安裝 arm64 套件：
    ```bash
    sudo rpm -ivh opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-arm64.rpm
    ```
    {% include copy.html %}

    對於 OpenSearch Dashboards 3.7 及更新版本的新安裝，您可以使用下列環境變數來控制 Security Dashboards 外掛程式的行為：
    ```bash
    DISABLE_SECURITY_DASHBOARDS_PLUGIN=true
    ```
    {% include copy.html %}
1. 安裝成功後，將 OpenSearch Dashboards 啟用為服務：
    ```bash
    sudo systemctl enable opensearch-dashboards
    ```
    {% include copy.html %}

1. 啟動 OpenSearch Dashboards：
    ```bash
    sudo systemctl start opensearch-dashboards
    ```
    {% include copy.html %}

1. 驗證 OpenSearch Dashboards 是否已正確啟動：
    ```bash
    sudo systemctl status opensearch-dashboards
    ```
    {% include copy.html %}

1. 在網頁瀏覽器中前往 `http://localhost:5601`，並以 `admin` 使用者身分，使用您安裝 OpenSearch 時設定的自訂管理員密碼登入。如果 OpenSearch Dashboards 執行於遠端主機，請將 `localhost` 取代為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

## 從本機 YUM 儲存庫安裝 OpenSearch Dashboards

YUM 是 Red Hat 系作業系統的主要套件管理工具，可讓您從 YUM 儲存庫下載並安裝 RPM 套件。

1. 為 OpenSearch Dashboards 建立本機儲存庫檔案：
   ```bash
   sudo curl -SL https://artifacts.opensearch.org/releases/bundle/opensearch-dashboards/{{major_version_mask}}/opensearch-dashboards-{{major_version_mask}}.repo -o /etc/yum.repos.d/opensearch-dashboards-{{major_version_mask}}.repo
   ```
   {% include copy.html %}

1. 驗證儲存庫是否已成功建立：
    ```bash
    sudo yum repolist
    ```
    {% include copy.html %}

1. 清除 YUM 快取，以確保安裝順利進行：
   ```bash
   sudo yum clean all
   ```
   {% include copy.html %}

1. 下載儲存庫檔案後，列出所有可用的 OpenSearch-Dashboards 版本：
   ```bash
   sudo yum list opensearch-dashboards --showduplicates
   ```
   {% include copy.html %}

1. 選擇您要安裝的 OpenSearch Dashboards 版本：
   - 若無特別指定，將會安裝 OpenSearch 的最高次要版本：
   ```bash
   sudo yum install opensearch-dashboards
   ```
   {% include copy.html %}

   - 若要安裝特定版本的 OpenSearch Dashboards：
   ```bash
   sudo yum install 'opensearch-dashboards-{{site.opensearch_dashboards_version}}'
   ```
   {% include copy.html %}

1. 安裝過程中，安裝程式會顯示 GPG 金鑰指紋。請確認資訊與下列內容相符：
   ```bash
   Fingerprint: A8B2 D9E0 4CD5 1FEF 6AA2 DB53 BA81 D999 8119 1457
   ```
   {% include copy.html %}

    - 若正確，請輸入 `yes` 或 `y`。OpenSearch 安裝將會繼續進行。
1. 啟動 OpenSearch Dashboards：
    ```bash
    sudo systemctl start opensearch-dashboards
    ```
    {% include copy.html %}

1. 在網頁瀏覽器中前往 `http://localhost:5601`，並以 `admin` 使用者身分，使用您安裝 OpenSearch 時設定的自訂管理員密碼登入。如果 OpenSearch Dashboards 執行於遠端主機，請將 `localhost` 取代為該主機的 IP 位址或 DNS 名稱。如需更多資訊，請參閱[存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#accessing-opensearch-dashboards)。

## 升級至較新版本

使用 RPM 或 YUM 安裝的 OpenSearch Dashboards 執行個體可以輕鬆升級至較新版本。我們建議使用 YUM，但您也可以選擇 RPM。


### 使用 RPM 手動升級

直接從 [OpenSearch Project 下載頁面](https://opensearch.org/downloads.html){:target='\_blank'} 下載所需升級版本的 RPM 套件。

瀏覽至包含發行版的目錄，並執行下列命令：

```bash
rpm -Uvh opensearch-dashboards-{{site.opensearch_dashboards_version}}-linux-x64.rpm
```
{% include copy.html %}

### 使用 YUM 升級

若要使用 YUM 升級至最新版本的 OpenSearch Dashboards，請執行下列命令：

```bash
sudo yum update opensearch-dashboards
```
{% include copy.html %}

您也可以提供版本號，升級至特定的 OpenSearch Dashboards 版本：
 
 ```bash
 sudo yum update opensearch-dashboards-<version-number>
 ```
 {% include copy.html %}

### 套件升級後自動重新啟動服務

OpenSearch Dashboards RPM 套件不支援在套件升級後自動重新啟動服務。

## 相關文件

- [為正式環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
