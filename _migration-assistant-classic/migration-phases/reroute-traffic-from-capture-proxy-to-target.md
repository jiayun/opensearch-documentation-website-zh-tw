---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將流量重新導向至目標"
nav_order: 8
parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/reroute-traffic-from-capture-proxy-to-target/
---

# 從來源叢集切換流量

**注意**：本頁面僅適用於您使用 Capture and Replay 以避免遷移期間停機的情況。如果您只執行回填遷移，則可以略過此步驟。
{: .note}

來源叢集與目標叢集同步後，需要將流量切換至目標叢集，以便將來源叢集下線。

## 假設

本頁面假設在進行切換之前，已發生下列情況：

- 所有用戶端流量都透過 [Migration Assistant Application Load Balancer]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/reroute-source-to-proxy/) 中的切換接聽程式路由。
- 已驗證用戶端流量與目標叢集相容。
- 目標叢集處於可接受用戶端流量的良好狀態。
- 已部署目標代理服務。

## 切換流量

使用下列步驟將流量從來源叢集切換至目標叢集：

1. 在 AWS Management Console 中，瀏覽至 **ECS** > **Migration Assistant Cluster**。記下 Capture Proxy 的期望計數，其應大於 1。

2. 將目標代理的 **ECS Service** 更新為至少與 Traffic Capture Proxy 一樣大。等待任務啟動，並在目標代理服務的 **Load balancer health** 區段中確認所有目標皆狀況良好。

3. 瀏覽至 **EC2** > **Load Balancers** > **Migration Assistant ALB**。

4. 瀏覽至 **ALB Metrics** 並檢查任何實用資訊，特別是查看 **Active Connection Count** 和 **New Connection Count**。記下任何大幅差異，這可能表示連線被重複使用而影響流量切換。

5. 瀏覽至 **Capture Proxy Target Group** (`ALBSourceProxy-<STAGE>-TG`) > **Monitoring**。

6. 檢查 **Metrics Requests**、**Target (2XX, 3XX, 4XX, 5XX)** 和 **Target Response Time** 指標。確認這些指標顯示如預期，並包含預期納入切換的所有流量。記下可能有助於在切換期間識別異常的詳細資料，包括預期的回應時間和回應碼比率。

7. 瀏覽回 **ALB Metrics** 並選擇 **Target Proxy Target Group** (`ALBTargetProxy-<STAGE>-TG`)。確認所有預期目標皆狀況良好，且沒有目標處於排空狀態。

8. 瀏覽回 **ALB Metrics**，並前往連接埠 `9200` 上的 **Listener**。

9. 選擇 **Default rule** 和 **Edit**。

10. 修改目標的權重，將所需流量切換至目標代理。若要執行完整切換，請將 **Target Proxy** 權重修改為 `1`，並將 **Source Proxy** 權重修改為 `0`。

11. 選擇 **Save Changes**。

12. 瀏覽至 **SourceProxy** 和 **TargetProxy TG Monitoring** 兩者的指標，並確認流量正按預期切換。如果連線被用戶端重複使用，請執行任何必要的動作來終止它們。持續監視這些指標，直到所有用戶端皆切換完成且 **SourceProxy TG** 顯示 0 個請求為止。


## 回復

如果您在切換期間的任何時間點需要回復至來源叢集，請還原 **Default rule**，讓 Application Load Balancer 路由至 **SourceProxy Target Group**。

{% include migration-phase-navigation.html %}
