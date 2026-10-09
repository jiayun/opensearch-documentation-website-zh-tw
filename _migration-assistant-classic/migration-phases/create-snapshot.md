---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立快照"
parent: Migration phases
nav_order: 4
permalink: /classic/migration-assistant/migration-phases/create-snapshot/
---

# 建立快照

當您已備妥變更資料擷取 (change data capture) 解決方案，或已停用來源叢集的索引作業後，即可開始建立快照。為來源叢集建立快照，可擷取所有要遷移至新目標叢集的中繼資料與文件。

## 建立快照

執行下列命令，從來源叢集啟動快照建立作業：

```bash
console snapshot create [...]
```
{% include copy.html %}

**注意**：Migration Assistant 會自動產生快照名稱，並設定必要的 Amazon Simple Storage Service (Amazon S3) 儲存庫。您也可以選擇使用自己既有的快照。

如需使用既有快照的更多資訊，請參閱 [自備快照]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/deploy/configuration-options/#bring-your-own-snapshot) 組態。

若要檢查快照建立狀態，請執行下列命令：

```bash
console snapshot status
```
{% include copy.html %}

若要取得快照的更多資訊，請執行下列命令：

```bash
console snapshot status --deep-check
```
{% include copy.html %}

請等待快照建立完成後，再進入中繼資料遷移階段。

快照建立完成後，您應會收到下列回應：

```shell
SUCCESS
Snapshot is SUCCESS.
Percent completed: 100.00%
Data GiB done: 29.211/29.211
Total shards: 40
Successful shards: 40
Failed shards: 0
Start time: 2024-07-22 18:21:42
Duration: 0h 13m 4s
Anticipated duration remaining: 0h 0m 0s
Throughput: 38.13 MiB/sec
```

## 處理快照速度緩慢的問題

視來源叢集中的資料大小以及分配給快照的頻寬而定，此程序可能需要一些時間。您可以使用 `--max-snapshot-rate-mb-per-node` 選項，調整來源叢集節點建立快照的最大速率。提高快照速率會消耗更多節點資源，可能影響叢集處理一般流量的能力。

{% include migration-phase-navigation.html %}
