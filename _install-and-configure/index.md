---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安裝與設定 OpenSearch"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /install-and-configure/
redirect_from:
  - /install-and-configure/index/
---

# 安裝與設定 OpenSearch

您可以將 OpenSearch 和 OpenSearch Dashboards 安裝在容器、Kubernetes、Linux 主機或 Windows 上。安裝完成後，請針對您的部署設定叢集，並安裝任何您需要的額外外掛程式。

## 試用 OpenSearch

若要在您的電腦上試用 OpenSearch，請參閱 [安裝快速入門]({{site.url}}{{site.baseurl}}/getting-started/quickstart/)。快速入門使用 Docker Compose 啟動 OpenSearch 和 OpenSearch Dashboards，旨在用於測試而非生產環境。

## 安裝前準備

在安裝 OpenSearch 之前，請查看以下資訊：

- [安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/) 中的主機需求與重要設定
- [相容的作業系統]({{site.url}}{{site.baseurl}}/install-and-configure/os-comp/) 中支援的作業系統

## 選擇安裝方法

下表列出了安裝方法以及每個產品的安裝指南連結。OpenSearch Kubernetes Operator 和 Ansible playbook 會將 OpenSearch 和 OpenSearch Dashboards 一併安裝，因此各僅有一份指南。

| 方法 | 安裝指南 |
| :--- | :--- |
| Docker | [OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/), [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/docker/) |
| OpenSearch Kubernetes Operator | [OpenSearch and OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/) |
| Helm | [OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/), [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/helm/) |
| Debian | [OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/debian/), [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/debian/) |
| RPM | [OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/rpm/), [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/rpm/) |
| Tarball | [OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/tar/), [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/tar/) |
| Ansible playbook | [OpenSearch and OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/ansible/) |
| Windows | [OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/windows/), [OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/windows/) |

## 安裝後步驟

安裝 OpenSearch 後，請使用以下指南來設定您的部署：

- [設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/)
- [設定 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-dashboards/)
- [管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)
- [管理 OpenSearch Dashboards 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-dashboards/plugins/)

## 相關文件

- 若要升級現有叢集，請參閱 [遷移或升級]({{site.url}}{{site.baseurl}}/migrate-or-upgrade/)。
