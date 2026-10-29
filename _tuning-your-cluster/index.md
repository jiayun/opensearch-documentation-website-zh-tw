---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "管理您的叢集"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
permalink: /tuning-your-cluster/
redirect_from: 
  - /tuning-your-cluster/index/
setup_steps:
- heading: 安裝 OpenSearch
  description: 使用 Docker、tarball、套件管理程式或 Kubernetes，在每個節點上安裝並設定 OpenSearch。
  link: /install-and-configure/install-opensearch/index/
- heading: 設定 OpenSearch
  description: 了解如何在 `opensearch.yml` 中、啟動時或使用 Cluster Settings API 指定設定，以及是否可以在叢集執行期間變更各項設定。
  link: /install-and-configure/configuring-opensearch/index/
- heading: 建立叢集
  description: 選擇節點類型、指派節點角色，並設定 `opensearch.yml` 中的節點，以組成多節點叢集。
  link: /tuning-your-cluster/creating-a-cluster/
- heading: 設定探索與叢集組成
  description: 設定種子主機、叢集啟動程序與投票機制，讓節點能互相找到彼此並選出叢集管理員。
  link: /tuning-your-cluster/discovery-cluster-formation/
- heading: 設定安全性
  description: 在將正式環境流量傳送至叢集之前，先設定 TLS 憑證、使用者與角色。
  link: /security/configuration/index/
data_protection:
- heading: 快照
  description: 將索引與叢集狀態備份至儲存庫，並還原至相同或其他叢集。
  link: /tuning-your-cluster/availability-and-recovery/snapshots/index/
- heading: 遠端後端儲存空間
  description: 將每筆索引交易傳送至遠端儲存空間，以便在節點或叢集故障後還原資料。
  link: /tuning-your-cluster/availability-and-recovery/remote-store/index/
- heading: 分段複寫
  description: 從主要分片將分段檔案複製到副本，而不是在每個分片副本上為每份文件編製索引。
  link: /tuning-your-cluster/availability-and-recovery/segment-replication/index/
- heading: 跨叢集複寫
  description: 將索引從領導叢集複寫到一或多個追隨叢集。
  link: /tuning-your-cluster/replication-plugin/index/
---

# 管理您的叢集

建立 OpenSearch 叢集、保護其資料，並控制其處理索引與搜尋工作負載的方式。

## 設定叢集

請依照下列步驟設定正式環境叢集。

{% include list.html list_items=page.setup_steps %}

## 備份與複寫資料

將資料備份至遠端儲存空間，並在其他節點與叢集上保留副本。

{% include cards.html cards=page.data_protection %}

## 控制資源用量

當節點收到的請求超出其可完成的數量時，OpenSearch 可以限制、拒絕或取消請求。下表列出控制資源用量的功能。

功能 | 效果
:--- | :---
[工作負載管理]({{site.url}}{{site.baseurl}}/tuning-your-cluster/workload-management/wlm-feature-overview/) | 將搜尋請求分組為工作負載群組，並限制每個群組可使用的 CPU 與記憶體。
[搜尋背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/load-protection/search-backpressure/) | 當節點處於高負載狀態時，取消耗用大量資源的搜尋請求。
[分片索引背壓]({{site.url}}{{site.baseurl}}/tuning-your-cluster/load-protection/shard-indexing-backpressure/) | 拒絕超載分片上的索引請求。
[並行限制]({{site.url}}{{site.baseurl}}/tuning-your-cluster/load-protection/concurrency-limits/) | 限制動作同時處理的請求數量。
[叢集管理員任務節流]({{site.url}}{{site.baseurl}}/tuning-your-cluster/load-protection/cluster-manager-task-throttling/) | 限制節點可提交至叢集管理員的任務數量。

## 調整效能

如要提高索引輸送量，請參閱[調整索引速度]({{site.url}}{{site.baseurl}}/tuning-your-cluster/performance-tuning/indexing-speed/)。如要在不同節點上執行索引與搜尋，請參閱[分離索引與搜尋工作負載]({{site.url}}{{site.baseurl}}/tuning-your-cluster/performance-tuning/separate-index-and-search-workloads/)。

## 管理排程工作

Index State Management、快照管理與異常偵測等 OpenSearch 外掛程式會依排程執行任務。如要檢視這些任務的狀態並調整其排程方式，請參閱[排程工作]({{site.url}}{{site.baseurl}}/tuning-your-cluster/scheduled-jobs/index/)。

## 監視您的叢集

OpenSearch 可以產生自身運作相關的指標與追蹤，並使用 OpenTelemetry 匯出，也可以回報叢集中執行最慢且最耗用資源的查詢。如需詳細資訊，請參閱[監視您的叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/monitoring/index/)。
