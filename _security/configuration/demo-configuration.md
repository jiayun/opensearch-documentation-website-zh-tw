---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定示範組態"
parent: Configuration
nav_order: 10
---

# 設定安全性示範組態

歡迎使用 OpenSearch Security 外掛程式示範組態設定指南。此工具可讓您快速、輕鬆地複製生產環境以進行測試。示範組態包含安全性相關元件的設定，例如內部使用者、角色、角色對應、稽核組態、基本驗證、租用戶及允許清單。

示範組態工具會執行下列工作：

1. 設定安全性設定，這些設定接著會載入安全性索引。
2. 產生示範憑證。
3. 將安全性相關設定新增至 `opensearch.yml` 檔案。

## 管理員密碼需求

從 OpenSearch 2.12 開始，示範組態需要自訂的管理員密碼，您需在 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 環境變數中提供此密碼。密碼必須符合下列所有需求：

- 包含 8 到 100 個字元。
- 至少包含一個大寫字母、一個小寫字母、一個數字及一個特殊字元。
- 在 [`zxcvbn`](https://github.com/dropbox/zxcvbn) 密碼強度評估工具中獲得 `strong` 或更高的評等。
- 與使用者名稱 `admin` 不相似。

`zxcvbn` 評等衡量的是熵，因此即使密碼符合所有字元需求，仍可能遭到拒絕。常見單字、日期、`1234` 或 `qwerty` 之類的序列，以及以 `3` 取代 `E` 之類可預測的字元替換，都會降低評等；而長度與不可預測性則會提高評等。若要在使用密碼前檢查其評等，請使用 [`zxcvbn` 示範](https://lowe.github.io/tryzxcvbn)。

如果密碼不符合這些需求，安裝會失敗，且 OpenSearch 會在記錄檔中回報未符合的需求。

這些需求內建於示範組態安裝程式中，無法變更。`opensearch.yml` 中的[密碼設定]({{site.url}}{{site.baseurl}}/security/configuration/yaml/#password-settings)僅適用於透過 REST API 或 OpenSearch Dashboards 建立的密碼。
{: .note}

若要在安裝後變更管理員密碼，以及了解叢集中其他密碼的概觀，請參閱[管理密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/)。

## 安裝示範組態

示範組態會在 OpenSearch 各個受支援發行版本的設定過程中自動呼叫。以下是各發行版本的說明。

**注意**：從 OpenSearch 2.12 開始，必須提供自訂的管理員密碼才能安裝示範組態。若未提供，叢集將無法啟動。請注意，此變更只會影響新叢集。現有叢集不受影響，因為它們已設定 `opensearch.yml`，所以安裝工具不會執行。

### Docker

請依照下列步驟，使用 Docker 設定 Security 外掛程式：

1. 下載 [`docker-compose.yml`](https://opensearch.org/downloads.html)。
2. 執行下列命令：

```bash
docker compose up
```
{% include copy.html %}

如果您想在使用 Docker 時停用 Security 外掛程式，請在 `docker-compose.yml` 檔案中將 `DISABLE_SECURITY_PLUGIN` 環境變數設為 `true`。不建議停用 Security 外掛程式。如需詳細資訊，請參閱 GitHub 上的 [Docker 映像檔發行 README](https://github.com/opensearch-project/opensearch-build/tree/main/docker/release#disable-security-plugin-security-dashboards-plugin-security-demo-configurations-and-related-configurations)。

### 設定自訂管理員密碼
**注意**：對於 OpenSearch 2.12 及更新版本，您必須在安裝前設定初始管理員密碼。若要自訂管理員密碼，您可以執行下列步驟：

1. 下載下列範例 [`docker-compose.yml`](https://github.com/opensearch-project/documentation-website/blob/{{site.opensearch_major_minor_version}}/assets/examples/docker-compose.yml) 檔案。
2. 建立 `.env` 檔案。
3. 新增變數 `OPENSEARCH_INITIAL_ADMIN_PASSWORD`，並將其設為符合[管理員密碼需求](#admin-password-requirements)的密碼。
4. 確認 Docker 正在您的本機電腦上執行
5. 從 `docker-compose.yml` 檔案與 `.env` 檔案所在的目錄執行 `docker compose up`。

<!-- vale off -->
### TAR (Linux) 與 macOS

對於 Linux 上的 TAR 發行版本，請從 OpenSearch [下載與入門](https://opensearch.org/downloads.html)頁面下載 Linux 設定檔案。
<!-- vale on --> 接著使用下列命令執行示範組態：

```bash
./opensearch-tar-install.sh
```
{% include copy.html %}

對於 OpenSearch 2.12 或更新版本，請在安裝前使用下列命令設定新的自訂管理員密碼：

```bash
export OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
```
{% include copy.html %}

### Windows

對於 Windows 上的 ZIP 發行版本，下載並解壓縮設定檔案後，請執行下列命令：

```powershell
> .\opensearch-windows-install.bat
```
{% include copy.html %}

對於 OpenSearch 2.12 或更新版本，請在安裝前執行下列命令設定新的自訂管理員密碼：

```powershell
> set OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>
```
{% include copy.html %}

### Helm

對於 Helm chart，示範組態會在 OpenSearch 安裝期間自動安裝。對於 OpenSearch 2.12 或更新版本，請依照[管理員密碼需求](#admin-password-requirements)，在 `values.yaml` 的 `extraEnvs` 下自訂管理員密碼：

```yaml
extraEnvs:
  - name: OPENSEARCH_INITIAL_ADMIN_PASSWORD
    value: <custom-admin-password>
```

### RPM

對於 RPM 套件，請執行下列命令安裝 OpenSearch 並設定示範組態：

```bash
sudo yum install opensearch-{{site.opensearch_version}}-linux-x64.rpm
```
{% include copy.html %}

對於 OpenSearch 2.12 或更新版本，請在安裝前使用下列命令設定新的自訂管理員密碼：

```bash
sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> yum install opensearch-{{site.opensearch_version}}-linux-x64.rpm
```
{% include copy.html %}

### DEB

對於 DEB 套件，請執行下列命令安裝 OpenSearch 並設定示範組態：

```bash
sudo dpkg -i opensearch-{{site.opensearch_version}}-linux-arm64.deb
```
{% include copy.html %}

對於 OpenSearch 2.12 或更新版本，請在安裝前使用下列命令設定新的自訂管理員密碼：

```bash
sudo env OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password> dpkg -i opensearch-{{site.opensearch_version}}-linux-arm64.deb
```
{% include copy.html %}

## 本機發行版本

如果您正在建置本機發行版本，請參閱 [DEVELOPER_GUIDE.md](https://github.com/opensearch-project/security/blob/main/DEVELOPER_GUIDE.md)，以了解如何為 Security 外掛程式建置本機二進位檔。

對於 OpenSearch 2.12 或更新版本，請務必在安裝前設定強式密碼。
