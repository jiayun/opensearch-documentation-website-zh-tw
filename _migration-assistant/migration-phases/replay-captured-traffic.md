---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重播擷取的流量"
nav_order: 70
parent: Migration workflows
permalink: /migration-assistant/migration-phases/replay-captured-traffic/
redirect_from:
  - /migration-assistant/migration-phases/live-traffic-migration/using-traffic-replayer/
  - /migration-assistant/migration-phases/using-traffic-replayer/
  - /migration-phases/using-traffic-replayer/
---

# 重播擷取的流量

下列資訊僅適用於使用 Capture and Replay 的零停機遷移。
{: .note }

重播是縮短回填所用快照與來源系統目前狀態之間時間差距的步驟。

## 重播開始條件

重播應僅在相依的快照遷移完成後才開始。在工作流程模型中，這通常以下列方式表示：

```text
dependsOnSnapshotMigrations
```

這項相依性非常重要。過早開始重播可能會在歷史回填與即時變更處理之間造成順序問題。

## 重播程序

Traffic Replayer 會執行下列步驟：

1. 從 Kafka 讀取擷取的流量。
2. 重建請求。
3. 套用重播時的轉換與驗證。
4. 將請求傳送至目標叢集。
5. 推進 Kafka 偏移量，讓重播可以安全地繼續。

## 關鍵重播設定

下表說明重播工作流程的關鍵設定。

| Setting | Description | Default |
|:--------|:------------|:--------|
| `podReplicas` | 平行執行的 Replayer pod 數量。 | N/A |
| `speedupFactor` | 控制重播相對於原始流量時間軸的追趕速度。值為 `2.0` 時，重播速度為原始速率的兩倍。 | `1.1` |
| `removeAuthHeader` | 在重播前移除擷取的 `Authorization` 標頭。當擷取的流量帶有對目標無效的憑證時使用。 | N/A |
| `authHeaderOverride` | 以靜態值取代擷取的 `Authorization` 標頭。 | N/A |
| `dependsOnSnapshotMigrations` | 指定在重播開始前必須完成哪一項快照遷移。 | N/A |
| `nonRetryableDocExceptionTypes` | 例外類別名稱清單，這些例外會計為失敗但不會重試，因為預期它們會確定性地失敗。此設定不同於 RFS 的 `allowedDocExceptionTypes`，後者將符合的例外視為成功。 | N/A |

請勿在同一個目標上同時設定 `replayerConfig.removeAuthHeader: true` 與 `authConfig` 區塊。結構描述會拒絕這種組合。請依賴目標的 `authConfig`（Replayer 會自動套用它），或移除擷取的標頭。
{: .warning }

## 影響重播時間的因素

重播時間取決於下列因素：

- 回填期間擷取的流量量。
- 目標叢集的處理吞吐量。
- 組態中的 `speedupFactor` 值。

## 監視重播

請盡可能使用互動式工作流程檢視：

```bash
workflow manage
```
{% include copy.html %}

下列命令可提供額外的監視資訊：

```bash
workflow status
workflow log all --follow
```
{% include copy.html %}

## 切換前驗證

請勿僅因為 Replayer 正在執行就切換流量。在繼續之前，請確認下列事項：

- 重播已達到即時邊緣。
- 文件數量在方向上正確。
- 具代表性的查詢在目標上行為正確。
- 目標端的錯誤已瞭解且可接受。

下列命令可協助驗證目標狀態：

```bash
console clusters cat-indices
console clusters curl target /my-index/_search --json '{"query":{"match_all":{}},"size":5}'
```
{% include copy.html %}

在重播達到即時邊緣且驗證通過後，即可繼續切換流量。請保持來源可用，直到回復窗口結束。

{% include migration-phase-navigation.html %}
