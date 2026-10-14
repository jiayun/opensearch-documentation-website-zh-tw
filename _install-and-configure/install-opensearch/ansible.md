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

1. 複製 OpenSearch [`ansible-playbook`](https://github.com/opensearch-project/ansible-playbook) 儲存庫並瀏覽至該儲存庫目錄：

   ```bash
   git clone https://github.com/opensearch-project/ansible-playbook
   cd ansible-playbook
   ```
   {% include copy.html %}

   `main` 分支會安裝最新的 OpenSearch {{os_major}}.x 版本。若要安裝 OpenSearch {{os_previous_major}}.x，請簽出 `{{os_previous_major}}.x` 分支。

1. 在 `inventories/opensearch/hosts` 檔案中設定目標主機。預設檔案定義了一個由五個 OpenSearch 節點與一個 OpenSearch Dashboards 節點組成的叢集。每一行指定一個主機名稱以及下列變數：

   - `ansible_host`：Ansible 用來連線至目標主機的 IP 位址。
   - `ansible_user`：Ansible 用來連線至目標主機的使用者。
   - `ip`：OpenSearch 與 OpenSearch Dashboards 繫結的 IP 位址。請指定目標主機的私人 IP 位址或 `0.0.0.0`。
   - `roles`：OpenSearch 節點的[節點角色]({{site.url}}{{site.baseurl}}/tuning-your-cluster/)。

   每部主機也必須列在檔案結尾的群組中：OpenSearch 節點列於 `os-cluster`、可擔任叢集管理員的節點列於 `master`，而 OpenSearch Dashboards 節點列於 `dashboards`。未列於群組中的主機不會被安裝。請將預設檔案中的 IP 位址替換為您主機的位址。

   若要在單一主機上安裝 OpenSearch 與 OpenSearch Dashboards，請將檔案內容替換為下列內容，並指定您主機的 IP 位址：

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

   若為單一主機，還需在 `inventories/opensearch/group_vars/all/all.yml` 檔案中將 `cluster_type` 設為 `single-node`：

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

   您可以使用 `admin_password`、`kibanaserver_password` 與 `logstash_password` 變數來設定保留使用者（`admin`、`kibanaserver` 與 `logstash`）的密碼。

1. 部署程序完成後，您可以使用使用者名稱 `admin` 以及您為 `admin_password` 變數設定的密碼來存取 OpenSearch 與 OpenSearch Dashboards。

   若要驗證 OpenSearch 正在執行，請將請求傳送至您在 `ip` 變數中指定的 IP 位址。如果您指定的是私人 IP 位址，請從同一網路中的機器傳送請求：

   ```bash
   curl https://<private-ip-address>:9200 -u 'admin:Test@123' --insecure
   ```
   {% include copy.html %}

   如果您指定了 `0.0.0.0`，您可以從目標主機將請求傳送至 `localhost`，或傳送至目標主機的任何 IP 位址。

1. 若要存取 OpenSearch Dashboards，請在瀏覽器中前往 `http://<ip-address>:5601`。playbook 完成後，OpenSearch Dashboards 可能需要約 1 分鐘才能啟動。

## 相關文件

- [準備正式環境的叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [準備正式環境的 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
