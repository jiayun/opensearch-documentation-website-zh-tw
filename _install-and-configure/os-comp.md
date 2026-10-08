---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "相容的作業系統"
nav_order: 120
---

# 相容的作業系統

OpenSearch 與 OpenSearch Dashboards 相容於 Red Hat Enterprise Linux (RHEL) 以及使用 [`systemd`](https://en.wikipedia.org/wiki/Systemd) 的 Debian 系列 Linux 發行版（例如 Amazon Linux）和 Ubuntu 長期支援 (LTS) 版本。雖然 OpenSearch 與 OpenSearch Dashboards 應該可以在大多數 Linux 發行版上執行，但我們僅測試其中一部分。

## 支援的作業系統

下表列出了我們針對 OpenSearch 與 OpenSearch Dashboards {{site.opensearch_major_minor_version}} 進行測試的作業系統版本。若要查看不同 OpenSearch 版本的測試作業系統，請在文件版本選擇器中選擇該版本。

作業系統 | 版本
:---------- | :-------- 
Rocky Linux | 8
Alma Linux | 8
Amazon Linux | 2023
Ubuntu | 24.04
Windows Server | 2019


## 變更記錄 

下表列出了作業系統相容性的變更內容。

| 日期 | 問題 | PR | 詳細資訊 |
|:-----------|:-------|:-------|:--------------------------|
| `2026-09-29` | [`opensearch-build` issue 5227](https://github.com/opensearch-project/opensearch-build/issues/5227) | [PR 12853](https://github.com/opensearch-project/documentation-website/pull/12853) | 移除 [Amazon Linux 2](https://aws.amazon.com/amazon-linux-2/faqs/) |
| `2025-02-06` | [`opensearch-build` issue 5270](https://github.com/opensearch-project/opensearch-build/issues/5270) | [PR 9165](https://github.com/opensearch-project/documentation-website/pull/9165) | 移除 [Ubuntu 20.04](https://ubuntu.com/blog/ubuntu-20-04-lts-end-of-life-standard-support-is-coming-to-an-end-heres-how-to-prepare) |
| `2024-07-23` | [`opensearch-build` issue 4379](https://github.com/opensearch-project/opensearch-build/issues/4379) | [PR 7821](https://github.com/opensearch-project/documentation-website/pull/7821) | 移除 [CentOS7](https://blog.centos.org/2023/04/end-dates-are-coming-for-centos-stream-8-and-centos-linux-7/) |
| `2024-03-08` | [`opensearch-build` issue 4573](https://github.com/opensearch-project/opensearch-build/issues/4573) | [PR 6637](https://github.com/opensearch-project/documentation-website/pull/6637) | 移除 CentOS8，新增 Almalinux8/Rockylinux8，並移除 Ubuntu 16.04/18.04，因為我們目前僅在 20.04 上進行測試 |
| `2023-06-06` | [`documentation-website` issue 4217](https://github.com/opensearch-project/documentation-website/issues/4217) | [PR 4218](https://github.com/opensearch-project/documentation-website/pull/4218) | 建立支援矩陣 |
