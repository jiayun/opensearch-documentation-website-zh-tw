---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Playbooks
nav_order: 80
has_children: true
has_toc: false
permalink: /migration-assistant/playbooks/
---

# Migration Assistant playbook

Playbook 是針對特定來源與目標組合的逐步遷移指南。每個 playbook 都會提供該遷移路徑所需的完整命令序列與組態。

## 先決條件

使用 playbook 之前，請確認下列事項：

- Migration Assistant 已部署於 Kubernetes 或 Amazon EKS。
- 您已確定您的遷移需要計畫性停機或零停機。
- 您已藉由執行 `workflow configure sample --load` 載入版本相符的範例組態。

## 使用 playbook

若要使用 playbook，請依照下列步驟：

1. 選擇符合您來源與目標的 playbook。
2. 在編輯工作流程之前，先依照先決條件檢查清單操作。
3. 先執行試驗性遷移。
4. 試驗性遷移成功後，執行完整遷移。

## 可用的 playbook

下表列出可用的 playbook。

| Playbook | 使用案例 |
|:---------|:---------|
| [Elasticsearch 6.8 至 OpenSearch 3.5]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-elasticsearch-6-8-to-opensearch-3/) | 需要中介資料轉換與以快照為基礎之回填的自我管理 Elasticsearch 來源 |
| [Amazon OpenSearch Service 至 OpenSearch Serverless NextGen]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-amazon-opensearch-service-to-serverless/) | 以 Serverless NextGen 集合為目標的受管理 AWS 來源 |
| [Solr 8.11 至 OpenSearch 3]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-solr-8.11-to-opensearch-3/) | 以 Solr 快照為基礎回填至 OpenSearch |

若為 AWS 生產部署，請先將 Migration Assistant 部署於 Amazon Elastic Kubernetes Service (EKS)，再依照 playbook 操作。如需更多資訊，請參閱[部署於 Amazon EKS]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)。
