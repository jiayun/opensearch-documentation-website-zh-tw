---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Ansible playbook
parent: Installing OpenSearch
nav_order: 35
redirect_from:
  - /opensearch/install/ansible/
---

{% assign os_major = site.opensearch_major_minor_version | split: "." | first %}
{% assign os_previous_major = os_major | minus: 1 %}

# 使用 Ansible 安裝 OpenSearch 與 OpenSearch Dashboards

您可以使用 Ansible playbook 來安裝並設定可供正式環境使用的 OpenSearch 叢集以及 OpenSearch Dashboards。

Ansible playbook 會將 OpenSearch 與 OpenSearch Dashboards 部署到使用 `systemd` 的 Linux 主機。關於 OpenSearch 測試過的作業系統，請參閱[相容的作業系統]({{site.url}}{{site.baseurl}}/install-and-configure/os-comp/)。
{: .note }

## 先決條件

執行 playbook 的機器（控制節點）必須安裝下列項目：

- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/index.html) 2.9 或更新版本。如果您只安裝 `ansible-core` 而非完整的 `ansible` 套件，還需安裝 playbook 使用的集合：

  ```bash
  ansible-galaxy collection install ansible.posix community.general
  ```
  {% include copy.html %}

- Java 8 或更新版本。playbook 會使用控制節點上的 Java 來產生叢集的 TLS 憑證。如果未安裝 Java，playbook 會失敗並出現 `java: command not found` 錯誤。

控制節點必須能直接以 SSH 存取每部目標主機上的 `root` 使用者。

## 組態

1. 複製 OpenSearch 的 [`ansible-playbook`](https://github.com/opensearch-project/ansible-playbook) 儲存庫並前往該儲存庫目錄：

   ```bash
   git clone https://github.com/opensearch-project/ansible-playbook
   cd ansible-playbook
   ```
   {% include copy.html %}

   `main` 分支會安裝最新的 OpenSearch {{os_major}}.x 版本。若要安裝 OpenSearch {{os_previous_major}}.x，請切換至 `{{os_previous_major}}.x` 分支。

1. 在 `inventories/opensearch/hosts` 檔案中設定目標主機。預設檔案定義了一個由五個 OpenSearch 節點與一個 OpenSearch Dashboards 節點組成的叢集。每一行指定一個主機名稱以及下列變數：

   - `ansible_host`：Ansible 用來連線至目標主機的 IP 位址。
   - `ansible_user`：Ansible 用來連線至目標主機的使用者。
   - `ip`：OpenSearch 與 OpenSearch Dashboards 綁定的 IP 位址。請指定目標主機的私有 IP 位址或 `0.0.0.0`。
   - `roles`：OpenSearch 節點的[節點角色]({{site.url}}{{site.baseurl}}/tuning-your-cluster/creating-a-cluster/#nodes)。

   每個主機也必須列在檔案結尾的群組中：`os-cluster` 用於 OpenSearch 節點，`master` 用於可擔任叢集管理員的節點，`dashboards` 用於 OpenSearch Dashboards 節點。未列在任何群組中的主機不會被安裝。請將預設檔案中的 IP 位址替換為您主機的位址。

   若要在單一主機上安裝 OpenSearch 與 OpenSearch Dashboards，請將檔案內容替換為以下內容，並指定您主機的 IP 位址：

   ```ini
   os1 ansible_host=<public-ip-address> ansible_user=root ip=<private-ip-address> roles=data,master

   [os-cluster]
   os1

   [master]
   os1

   [dashboards]
   os1
   ```
   {% include copy.html %}

   對於單一主機，還需在 `inventories/opensearch/group_vars/all/all.yml` 檔案中將 `cluster_type` 設定為 `single-node`：

   ```yaml
   cluster_type: single-node
   ```
   {% include copy.html %}

1. 您可以修改 `inventories/opensearch/group_vars/all/all.yml` 檔案中的預設組態值。例如，您可以增加 Java 記憶體堆積大小：

   ```yaml
   xms_value: 8
   xmx_value: 8
   ```
   {% include copy.html %}

## 使用 Ansible playbook 安裝 OpenSearch 與 OpenSearch Dashboards

1. 在 `ansible-playbook` 目錄中執行 Ansible playbook：

   ```bash
   ansible-playbook -i inventories/opensearch/hosts opensearch.yml --extra-vars "admin_password=Test@123 kibanaserver_password=Test@6789 logstash_password=Test@456"
   ```
   {% include copy.html %}

   您可以使用 `admin_password`、`kibanaserver_password` 與 `logstash_password` 變數，為保留使用者（`admin`、`kibanaserver` 與 `logstash`）設定密碼。若要在部署後變更管理員密碼，請參閱[變更管理員密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#changing-the-admin-password)。

1. 部署程序完成後，您可以使用使用者名稱 `admin` 以及為 `admin_password` 變數設定的密碼，存取 OpenSearch 與 OpenSearch Dashboards。

   若要確認 OpenSearch 正在執行，請向您在 `ip` 變數中指定的 IP 位址傳送請求。若您指定的是私有 IP 位址，請從同一網路中的機器傳送請求：

   ```bash
   curl https://<private-ip-address>:9200 -u 'admin:Test@123' --insecure
   ```
   {% include copy.html %}

   若您指定 `0.0.0.0`，則可從目標主機向 `localhost` 傳送請求，或向目標主機的任何 IP 位址傳送請求。

1. 若要存取 OpenSearch Dashboards，請在瀏覽器中前往 `http://<ip-address>:5601`。playbook 執行完畢後，OpenSearch Dashboards 大約需要 1 分鐘才能啟動。

## 重新執行 playbook

playbook 每次執行時都會同時重新啟動所有目標主機上的 OpenSearch，因此節點重新啟動期間叢集將無法使用。請規劃重新執行的時機，例如套用組態變更時，安排在維護時段內進行。

預設情況下，playbook 會在控制節點的 `/tmp/opensearch-nodecerts` 目錄中產生 TLS 憑證。當您重新執行 playbook 時，如果該目錄存在，它會重複使用這些憑證，且不會再次將安全性組態複製到目標主機。如果該目錄不存在，例如控制節點重新啟動且 `/tmp` 已被清除，playbook 會產生新的根憑證授權單位 (CA) 以及新的節點與管理員憑證，並將它們複製到所有目標主機。驗證叢集憑證的用戶端屆時將需要新的 `root-ca.pem` 檔案。

若要透過重複執行 playbook 來管理現有叢集，請在 `inventories/opensearch/group_vars/all/all.yml` 檔案中將 `iac_enable` 設定為 `true`。在此模式下，playbook 每次執行都會更新組態檔，但只有在至少有一部主機缺少至少一個憑證時才會複製新憑證，例如將主機加入叢集時。在這種情況下，它會取代所有主機上的憑證。

### 輪替憑證

產生的憑證有效期為 `cert_valid_days` 變數設定的天數（預設為 `730`）。若要改用新憑證取代，請刪除控制節點上的 `/tmp/opensearch-nodecerts` 目錄，確認 `iac_enable` 為 `false`，然後重新執行 playbook。所有節點會同時使用新憑證重新啟動。

## 升級使用 playbook 安裝的叢集

此 playbook 會安裝 OpenSearch，但不會升級 OpenSearch。變更 `os_version` 後重新執行 playbook 並非支援的升級方法，原因如下：

- playbook 會將 OpenSearch 封存檔下載到每個目標主機上的 `/tmp/opensearch.tar.gz`，且若該檔案已存在，便會略過下載。除非 `iac_enable` 為 `true`，否則仍保有先前執行所下載封存檔的主機不會安裝新版本。
- 安裝新版本時，playbook 會將其解壓縮並覆蓋 `/usr/share/opensearch` 中的現有安裝，因此先前版本中不屬於新版本的檔案仍會留在安裝目錄中。
- playbook 會同時重新啟動所有節點，而不是一次重新啟動一個節點。

若要升級使用 playbook 安裝的叢集，請依照[滾動升級]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/rolling-upgrade/)程序，一次升級一個節點。playbook 會將 OpenSearch 安裝在 `/usr/share/opensearch` 中，並將組態、憑證及 Security 外掛程式組態儲存在 `/usr/share/opensearch/config` 中。在每個節點上安裝新版本時，請保留這些檔案。升級所有節點後，請更新 `inventories/opensearch/group_vars/all/all.yml` 中的 `os_version` 和 `os_dashboards_version`，使其與已安裝的版本相符。

## 相關文件

- [準備正式環境的叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [準備正式環境的 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
