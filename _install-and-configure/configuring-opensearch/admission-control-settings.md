---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "准入控制設定"
parent: Configuring OpenSearch
nav_order: 130
---

# 准入控制設定

OpenSearch 提供准入控制設定，透過限制不同類型操作的資源使用量，協助防止叢集過載。准入控制會監視 CPU 與 I/O 使用量，並可在資源使用率超過所設定的閾值時拒絕請求。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 傳輸層設定

OpenSearch 支援下列傳輸層准入控制設定：

- `admission_control.transport.mode`（動態，字串）：控制傳輸層的整體准入控制模式。有效值如下：
  - `disabled`（預設）：停用准入控制。
  - `shadow`：准入控制僅以監視模式執行，只收集指標而不拒絕請求。
  - `enforced`：准入控制會在超過閾值時主動拒絕請求。

## 以 CPU 為基礎的准入控制設定

以 CPU 為基礎的准入控制會監視 CPU 使用量，並對不同類型的操作套用限制。所有 CPU 限制皆以百分比（0--100）指定。

OpenSearch 支援下列以 CPU 為基礎的動態准入控制設定：

- `admission_control.cluster.admin.cpu_usage.limit`（動態，long）：叢集管理操作的 CPU 使用量閾值。當 CPU 使用量超過此限制時，可能會拒絕叢集管理請求，以維持叢集穩定性。預設值為 `95`。

- `admission_control.search.cpu_usage.limit`（動態，long）：搜尋操作的 CPU 使用量閾值。當 CPU 使用量超過此限制時，可能會拒絕新的搜尋請求，以防止叢集過載。預設值為 `95`。

- `admission_control.indexing.cpu_usage.limit`（動態，long）：編製索引操作的 CPU 使用量閾值。當 CPU 使用量超過此限制時，可能會拒絕編製索引請求，以維持叢集效能。預設值為 `95`。

- `admission_control.transport.cpu_usage.mode_override`（動態，字串）：專門針對以 CPU 為基礎的准入控制覆寫全域傳輸模式。可接受的值與 `admission_control.transport.mode` 相同：`disabled`、`shadow` 或 `enforced`。若未指定，則使用全域傳輸模式設定。

## 以 I/O 為基礎的准入控制設定

以 I/O 為基礎的准入控制會監視磁碟 I/O 使用量，並對不同類型的操作套用限制。所有 I/O 限制皆以百分比（0--100）指定。

OpenSearch 支援下列以 I/O 為基礎的准入控制設定：

- `admission_control.search.io_usage.limit`（動態，long）：搜尋操作的 I/O 使用量閾值。當 I/O 使用量超過此限制時，可能會拒絕搜尋請求。預設值為 `95`。

- `admission_control.indexing.io_usage.limit`（動態，long）：編製索引操作的 I/O 使用量閾值。當 I/O 使用量超過此限制時，可能會拒絕編製索引請求。預設值為 `95`。

- `admission_control.cluster_admin.io_usage.limit`（靜態，long）：叢集管理操作的 I/O 使用量閾值。此為靜態設定，修改後需要重新啟動叢集。預設值為 `100`。

- `admission_control.transport.io_usage.mode_override`（動態，字串）：專門針對以 I/O 為基礎的准入控制覆寫全域傳輸模式。可接受的值與 `admission_control.transport.mode` 相同：`disabled`、`shadow` 或 `enforced`。若未指定，則使用全域傳輸模式設定。
