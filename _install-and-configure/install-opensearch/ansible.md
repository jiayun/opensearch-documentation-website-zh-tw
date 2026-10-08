---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Ansible playbook
parent: Installing OpenSearch
nav_order: 35
redirect_from:
  - /opensearch/install/ansible/
---

# 使用 Ansible 安裝 OpenSearch 與 OpenSearch Dashboards

您可以使用 Ansible playbook 來安裝並設定一個可用於生產環境的 OpenSearch 叢集以及 OpenSearch Dashboards。

此 Ansible playbook 僅支援將 OpenSearch 與 OpenSearch Dashboards 部署到最熱門的 Linux 發行版（CentOS 7、RHEL7、Amazon Linux 2、Ubuntu 20.04）主機。
{: .note }

## 前置條件

請確保您已安裝 [Ansible](https://www.ansible.com/) 與 [Java 8](https://www.java.com/en/download/manual.jsp)。

## 組態設定

1. 複製 OpenSearch [`ansible-playbook`](https://github.com/opensearch-project/ansible-playbook) 儲存庫：

   ```bash
   git clone https://github.com/opensearch-project/ansible-playbook
   ```
   {% include copy.html %}

2. 在 `inventories/opensearch/hosts` 檔案中設定節點屬性：

   ```bash
   ansible_host=<Public IP address> ansible_user=root ip=<Private IP address / 0.0.0.0>
   ```
   {% include copy.html %}

   其中：

   - `ansible_host` 是您希望 Ansible playbook 安裝 OpenSearch 與 OpenSearch Dashboards 的目標節點 IP 位址。
   - `ip` 是您希望 OpenSearch 與 OpenSearch Dashboards 綁定的 IP 位址。您可以指定目標節點的私有 IP、localhost 或 0.0.0.0。

3. 您可以在 `inventories/opensearch/group_vars/all/all.yml` 檔案中修改預設的組態值。例如，您可以增加 Java 記憶體堆積大小：

   ```bash
   xms_value: 8
   xmx_value: 8
   ```
   {% include copy.html %}

請確保您具有直接透過 SSH 存取目標節點 root 使用者的權限。
{: .note }

## 使用 Ansible playbook 安裝 OpenSearch 與 OpenSearch Dashboards

1. 以 root 權限執行 Ansible playbook：

   ```bash
   ansible-playbook -i inventories/opensearch/hosts opensearch.yml --extra-vars "admin_password=Test@123 kibanaserver_password=Test@6789 logstash_password=Test@456"
   ```
   {% include copy.html %}

   您可以使用 `admin_password`、`kibanaserver_password` 與 `logstash_password` 變數來設定保留使用者的密碼（`admin`、`kibanaserver` 與 `logstash`）。

2. 部署程序完成後，您可以使用使用者名稱 `admin` 以及您為 `admin_password` 變數設定的密碼來存取 OpenSearch 與 OpenSearch Dashboards。

   如果您將 `ip` 綁定到私有 IP 或 localhost，請確保您已登入部署 playbook 的伺服器，以存取 OpenSearch 與 OpenSearch Dashboards：

   ```bash
   curl https://localhost:9200 -u 'admin:Test@123' --insecure
   ```
   {% include copy.html %}

   如果您將 `ip` 綁定到 0.0.0.0，請將 `localhost` 替換為公有 IP 或私有 IP（如果在同一網路中）。

## 相關文件

- [為生產環境準備叢集]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/#preparing-a-cluster-for-production)
- [為生產環境準備 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/index/#preparing-opensearch-dashboards-for-production)
