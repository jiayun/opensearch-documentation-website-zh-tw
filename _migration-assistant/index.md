---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch 的 Migration Assistant"
nav_order: 30
has_children: true
has_toc: false
nav_exclude: true
permalink: /migration-assistant/
redirect_from:
  - /migration-assistant/overview/
  - /migration-assistant/index/

items:
- heading: Migration Assistant 是否適合您？
  description: 判斷 Migration Assistant 是否符合您的遷移路徑、停機目標與維運模式。
  link: /migration-assistant/is-migration-assistant-right-for-you/
- heading: 為什麼選擇 Kubernetes 與 EKS？
  description: 新版 Migration Assistant 背後的理念，以及為什麼 Amazon EKS 是 AWS 上建議的正式環境路徑。
  link: /migration-assistant/why-kubernetes-and-eks/
- heading: 選擇您的部署方式
  description: 比較一般 Kubernetes 與 Amazon EKS，並決定哪條路徑適合您的環境。
  link: /migration-assistant/migration-phases/deploy/
- heading: 遷移如何執行
  description: 以工作流程為導向的生命週期，涵蓋回填、Capture 與 Replay、驗證及切換。
  link: /migration-assistant/migration-phases/
- heading: 執行遷移
  description: 使用 Workflow CLI 作為設定、提交與管理遷移的主要介面。
  link: /migration-assistant/workflow-cli/
- heading: 使用劇本 (playbook)
  description: 依照特定路徑的指南，處理常見的來源與目標組合。
  link: /migration-assistant/playbooks/
---

# ![Migration Assistant icon]({{site.url}}{{site.baseurl}}/images/icons/MigrationUpgrade_Color_Icon.svg){: .heading-icon} OpenSearch 的 Migration Assistant

Migration Assistant 是以 Kubernetes 為本質的遷移平台，可將資料、中繼資料與即時流量從 Elasticsearch、OpenSearch 及 Apache Solr 遷移至 OpenSearch。

Migration Assistant 的維運模式如下：

- 您在工作流程組態中定義遷移。
- Migration Assistant 在 Kubernetes 上執行工作。
- 您使用 Migration Console 與 Workflow CLI 來提交、觀察、核准、驗證，並將流量切換至目標叢集。

Migration Assistant 可在任何 Kubernetes 發行版上執行，但 **Amazon EKS 是 AWS 上建議的正式環境路徑**，因為它提供實際遷移通常需要的 AWS 身分、映像檔、快照與可觀測性整合。

如果您使用的是較舊的 ECS/CDK 版 Migration Assistant，請參閱 [與傳統版本的差異](#changes-from-the-classic-version)。

## 主要功能

Migration Assistant 提供以下功能：

- **單一遷移模型**：同時支援有計畫停機的快照式遷移（稱為 *backfill-only*），以及使用即時流量 Capture 與 Replay 的零停機遷移。
- **可重複的工作流程**，取代一次性的基礎架構編排。
- **對來源叢集影響低**：透過快照式回填與 [Reindex-from-Snapshot (RFS)]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/backfill/) 達成。
- **維運檢查點**：透過核准關卡、記錄檔、狀態檢視與驗證步驟實現。
- **務實的 AWS 路徑**：在 EKS 上減少周邊平台工作。

## 入門

1. [判斷 Migration Assistant 是否為合適的工具]({{site.url}}{{site.baseurl}}/migration-assistant/is-migration-assistant-right-for-you/)。
2. [了解此產品為何改用 Kubernetes，以及為何在 AWS 上建議使用 EKS]({{site.url}}{{site.baseurl}}/migration-assistant/why-kubernetes-and-eks/)。
3. [評估您的遷移]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/assessment/)。檢視重大變更、停機限制與必要的轉換。
4. [選擇您的部署路徑]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/)。
5. [了解遷移如何執行]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/)。
6. [使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/)，然後[挑選劇本 (playbook)]({{site.url}}{{site.baseurl}}/migration-assistant/playbooks/)。

正在尋找較舊的 ECS 部署模式？請參閱[傳統版 Migration Assistant 文件]({{site.url}}{{site.baseurl}}/classic/migration-assistant/)。
{: .note }

## 與傳統版本的差異

如果您先前使用的是 ECS/CDK 版 Migration Assistant，此版本的維運模式有所不同：

- 遷移是在工作流程組態中定義，而非長期存在的基礎架構堆疊。
- Migration Assistant 在 Kubernetes 上執行工作（Amazon EKS 是 AWS 上建議的路徑）。
- 日常維運透過 Migration Console 與 Workflow CLI 進行，而非自訂指令碼。

如需設計理念的背景說明，請參閱 [為什麼選擇 Kubernetes 與 EKS]({{site.url}}{{site.baseurl}}/migration-assistant/why-kubernetes-and-eks/)。

{% include list.html list_items=page.items %}
