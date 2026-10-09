---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將流量切換至目標"
nav_order: 80
parent: Migration workflows
permalink: /migration-assistant/migration-phases/switch-traffic-to-target/
redirect_from:
  - /migration-assistant/migration-phases/reroute-traffic-from-capture-proxy-to-target/
---

# 將流量切換至目標

下列資訊僅適用於使用 Capture and Replay 的零停機遷移。
{: .note }

切換流量是轉換 (cutover) 步驟。到此階段，擷取 (capture) 已在回填期間保護寫入作業，重播 (replay) 已讓目標追上進度，而驗證應已完成。

## 轉換檢查清單

在切換流量之前，請確認下列事項：

- 重播已追上即時流量的進度。
- 目標叢集狀態良好。
- 具代表性的應用程式查詢可在目標上正常運作。
- 應用程式團隊已準備好移轉流量。
- 復原路徑仍然可用。

## 切換流量

確切機制取決於您的環境，但流程相同：

1. 將用戶端從擷取代理重新導向。
2. 將用戶端直接指向目標叢集。
3. 在第一個正式環境流量時段期間密切監控目標。

實務上，這通常表示要更新：

- DNS 記錄
- 負載平衡器後端
- 應用程式連線字串
- 服務探索項目

## 切換流量後驗證目標

切換流量後，請立即驗證下列事項：

- 叢集健康狀態
- 基本索引可見性
- 具代表性的應用程式行為

下列命令有助於驗證目標：

```bash
console clusters curl target /_cluster/health
console clusters cat-indices --cluster target
```
{% include copy.html %}

## 維持復原能力

請勿在切換流量後立即移除來源叢集或遷移基礎架構。如果您需要還原至來源，請執行下列步驟：

1. 將用戶端重新導向回原先的路由。
2. 調查目標端的問題。
3. 決定要繼續重播、重新執行遷移，還是稍後重試切換。

在確認目標於正式環境流量下穩定運作之前，請保持來源可用。復原時限過後，請移除遷移基礎架構及任何暫時性資源。

{% include migration-phase-navigation.html %}
