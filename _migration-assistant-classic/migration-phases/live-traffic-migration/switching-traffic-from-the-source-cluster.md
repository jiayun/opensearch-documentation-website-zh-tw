---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "從來源叢集切換流量"
parent: Live traffic migration
grand_parent: Migration phases
nav_order: 110
permalink: /classic/migration-assistant/migration-phases/live-traffic-migration/switching-traffic-from-the-source-cluster/
---

# 從來源叢集切換流量

來源叢集與目標叢集同步後，需要將流量切換至目標叢集，以便將來源叢集下線。

## 前提假設

本頁假設在進行切換前，已完成下列事項：

- 所有用戶端流量都透過 [MigrationAssistant Application Load Balancer]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/backfill/) 中的切換接聽程式路由。
- 已驗證用戶端流量與目標叢集相容。
- 目標叢集處於可接受用戶端流量的良好狀態。
- 已部署目標代理服務。

## 切換流量

請使用下列步驟將流量從來源叢集切換至目標叢集：

1. 在 AWS Management Console 中，瀏覽至 **ECS** > **Migration Assistant Cluster**。記下 capture proxy 的期望數量，其應大於 1。

2. 將目標 proxy 的 **ECS Service** 更新為至少與 Traffic Capture Proxy 一樣大。等待任務啟動，並在目標 proxy 服務的 **Load balancer health** 區段中確認所有目標皆狀況良好。

3. 瀏覽至 **EC2** > **Load Balancers** > **Migration Assistant ALB**。

4. 瀏覽至 **ALB Metrics** 並檢查任何有用的資訊，特別是查看 **Active Connection Count** 與 **New Connection Count**。記下任何明顯的差異，這可能表示連線被重複使用而影響流量切換。

5. 瀏覽至 **Capture Proxy Target Group** (`ALBSourceProxy-<STAGE>-TG`) > **Monitoring**。

6. 檢查 **Metrics Requests**、**Target (2XX, 3XX, 4XX, 5XX)** 與 **Target Response Time** 指標。確認其顯示結果符合預期，且包含所有預期納入切換的流量。記下有助於在切換期間識別異常的詳細資料，包括預期的回應時間與回應碼比率。

7. 瀏覽回 **ALB Metrics** 並選擇 **Target Proxy Target Group** (`ALBTargetProxy-<STAGE>-TG`)。確認所有預期的目標皆狀況良好，且沒有目標處於 draining 狀態。

8. 瀏覽回 **ALB Metrics**，並前往連接埠 `9200` 上的 **Listener**。

9. 選擇 **Default rule** 並選擇 **Edit**。

10. 修改目標的權重，將所需的流量切換至目標 proxy。若要執行完整切換，請將 **Target Proxy** 權重修改為 `1`，並將 **Source Proxy** 權重修改為 `0`。

11. 選擇 **Save Changes**。

12. 瀏覽至 **SourceProxy** 與 **TargetProxy TG Monitoring** 兩者的指標，並確認流量正依預期切換。若連線被用戶端重複使用，請執行任何必要的動作將其終止。持續監視這些指標，直到所有用戶端皆完成切換且 **SourceProxy TG** 顯示 0 個請求。


## 回復

若您在切換期間的任何時間點需要回復至來源叢集，請還原 **Default rule**，讓 Application Load Balancer 路由至 **SourceProxy Target Group**。
