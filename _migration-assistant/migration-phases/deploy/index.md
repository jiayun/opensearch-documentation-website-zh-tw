---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "選擇您的部署方式"
parent: Migration workflows
nav_order: 20
has_children: true
has_toc: true
permalink: /migration-assistant/migration-phases/deploy/
redirect_from:
  - /migration-assistant/deploying-migration-assistant/
  - /migration-assistant/getting-started-with-data-migration/
  - /deploying-migration-assistant/
---

# 選擇您的部署方式

Migration Assistant 一律在 Kubernetes 上執行。首要的決定是您希望工具自動化多少平台組態。

## 部署類型

下表比較兩種部署類型。

| 類型 | 最適合的情況 | 包含內容 |
|:-----|:----------|:-------------|
| [部署在 Kubernetes 上]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-kubernetes/) | 您已經營運 Kubernetes 平台、您不在 AWS 上，或您正在本機評估 | 核心 Migration Assistant 引擎與工作流程模型，由您提供平台整合 |
| [部署在 Amazon Elastic Kubernetes Service (EKS) 上]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/) | 您在 AWS 上，且想要建議的正式環境路徑 | 相同的引擎，外加 AWS 啟動自動化、Pod 身分、映像鏡像、快照協助工具，以及 CloudWatch 整合 |

兩種路徑都會安裝相同的 Migration Assistant Helm chart。差別在於周圍環境有多少是為您準備好的。

## 預設元件

下表說明 Migration Assistant Helm chart 所安裝的元件。

| 元件 | 用途 |
|:----------|:--------|
| Migration Console | 內含 CLI 工具的 Pod，用於設定及執行遷移 |
| Workflow Engine | 協調遷移工作 (Argo Workflows) |
| Strimzi | 用於擷取與重播的 Kafka operator |
| 與 Prometheus 相容的指標 | 指標收集與平台可觀測性整合 |

來源與目標叢集組態是透過 Workflow CLI 動態處理，而不是透過大型的 Helm value 檔案。

## 為何在 AWS 上建議使用 Amazon EKS

在 AWS 上，Amazon EKS 是建議的路徑，因為它免除了大量與遷移無關的工作：

- 叢集與 VPC 啟動。
- 用於 AWS API 存取的 Pod 身分。
- 隔離子網路的私有映像支援。
- 快照桶與角色協助工具。
- CloudWatch 儀表板與記錄。
- 具 AWS 意識的儲存空間與節點集區預設值。

此做法可減少平台組態的工作量，讓您專注於驗證遷移。

## 必要條件

所有部署路徑都需要：

- **Kubernetes 叢集**：1.24 版或更新版本。
- **Helm 3**：已安裝並設定完成
- **`kubectl`**：已設定可存取您的叢集。
- **網路存取**：從叢集到來源與目標叢集的連線能力。

如果您要自備 Kubernetes 平台，請使用[部署在 Kubernetes 上]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-kubernetes/)。

如果您想要其餘新版 Migration Assistant 文件預設假設的 AWS 正式環境路徑，請使用[部署在 Amazon EKS 上]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)。

{% include migration-phase-navigation.html %}
