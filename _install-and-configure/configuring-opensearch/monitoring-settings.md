---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "監控設定"
parent: Configuring OpenSearch
nav_order: 90
---

# 監控設定

OpenSearch 提供多項設定，可用來監控叢集健康狀態與效能的各個面向，包括檔案系統操作、JVM 垃圾回收、作業系統指標與處理程序統計資料。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 檔案系統健康狀態監控設定

OpenSearch 支援下列檔案系統健康狀態監控設定：

- `monitor.fs.health.enabled`（動態，布林值）：啟用檔案系統健康狀態監控，以偵測緩慢或無回應的檔案系統操作。預設值為 `true`。

- `monitor.fs.health.healthy_timeout_threshold`（動態，時間單位）：判定檔案系統操作為健康狀態的閾值。耗時超過此值的操作會被標記為緩慢。預設值為 `60s`。強制最小值為 `1ms`。

- `monitor.fs.health.slow_path_logging_threshold`（動態，時間單位）：記錄緩慢檔案系統路徑操作的閾值。預設值為 `5s`。強制最小值為 `1ms`。

- `monitor.fs.health.refresh_interval`（靜態，時間單位）：檔案系統健康狀態監控的重新整理間隔。預設值為 `60s`。最小值為 `1ms`。

- `monitor.fs.refresh_interval`（靜態，時間單位）：檔案系統統計資料監控的重新整理間隔。預設值為 `1s`。最小值為 `1s`。

## JVM 監控設定

OpenSearch 支援下列 JVM 監控設定：

- `monitor.jvm.gc.enabled`（靜態，布林值）：啟用 JVM 垃圾回收監控。預設值為 `true`。

- `monitor.jvm.gc.overhead.debug`（靜態，整數）：除錯 (debug) 層級記錄的 GC 額外負荷百分比閾值。預設值為 `10`。範圍為 `0-100`。

- `monitor.jvm.gc.overhead.info`（靜態，整數）：資訊 (info) 層級記錄的 GC 額外負荷百分比閾值。預設值為 `25`。範圍為 `0-100`。

- `monitor.jvm.gc.overhead.warn`（靜態，整數）：警告 (warning) 層級記錄的 GC 額外負荷百分比閾值。預設值為 `50`。範圍為 `0-100`。

- `monitor.jvm.gc.refresh_interval`（靜態，時間單位）：JVM GC 監控的重新整理間隔。預設值為 `1s`。最小值為 `1s`。

- `monitor.jvm.refresh_interval`（靜態，時間單位）：JVM 統計資料監控的重新整理間隔。預設值為 `1s`。最小值為 `1s`。

## 作業系統與處理程序監控設定

OpenSearch 支援下列作業系統與處理程序監控設定：

- `monitor.os.refresh_interval`（靜態，時間單位）：作業系統統計資料監控的重新整理間隔。預設值為 `1s`。最小值為 `1s`。

- `monitor.process.refresh_interval`（靜態，時間單位）：處理程序統計資料監控的重新整理間隔。預設值為 `1s`。最小值為 `1s`。
