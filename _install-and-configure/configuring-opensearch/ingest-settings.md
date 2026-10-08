---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "匯入設定"
parent: Configuring OpenSearch
nav_order: 150
---

# 匯入設定

OpenSearch 提供匯入設定，用來控制資料處理管線中允許使用哪些匯入處理器。這些設定可透過限制資料匯入管線中可使用的處理器，協助維護資料轉換作業的安全性與控管。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## User agent 處理器設定

User agent 處理器設定控制資料匯入管線中允許使用哪些 user agent 剖析處理器。

OpenSearch 支援下列靜態 User agent 處理器設定：

- `ingest.useragent.processors.allowed`（靜態，清單）：指定資料匯入管線中允許使用哪些 User agent 處理器。當此清單為空（預設）時，不會套用任何限制，所有可用的 User agent 處理器皆可使用。當設定特定的處理器名稱時，管線中只允許使用這些處理器。此設定有助於基於安全性與資料治理目的，控制可使用哪些 user agent 剖析處理器。預設為 `[]`（空清單－無限制）。

## 通用處理器設定

通用處理器設定控制資料匯入管線中允許使用哪些標準匯入處理器。

OpenSearch 支援下列靜態通用處理器設定：

- `ingest.common.processors.allowed`（靜態，清單）：指定資料匯入管線中允許使用哪些通用匯入處理器。當此清單為空（預設）時，不會套用任何限制，所有可用的通用處理器（例如 `set`、`remove`、`rename` 和 `convert`）皆可使用。當設定特定的處理器名稱時，管線中只允許使用這些處理器。此設定可針對安全性與法規遵循需求，對資料轉換功能提供細緻的控制。預設為 `[]`（空清單－無限制）。

## 快取與效能設定

快取與效能設定控制各種匯入處理器的快取大小與執行限制。

OpenSearch 支援下列靜態快取與效能設定：

- `ingest.user_agent.cache_size`（靜態，long）：設定 User agent 字串剖析結果的快取大小。此快取會儲存已剖析的 user agent 資訊，以在處理含有重複 user agent 字串的文件時提升效能。較高的值可減少常見 user agent 的剖析負擔，但會使用更多記憶體。此快取會儲存 user agent 字串與其剖析後元件（瀏覽器、作業系統和裝置資訊）之間的對應關係。預設為 `1000`。最小值為 `0`。

- `ingest.grok.watchdog.interval`（靜態，時間單位）：設定 Grok 處理器監控程式 (watchdog) 檢查長時間執行之模式比對作業的間隔。監控程式有助於防止 Grok 處理器因複雜或效率不佳的模式而耗用過多 CPU 時間。較頻繁的檢查能對失控作業提供更好的防護，但會增加些微負擔。預設為 `1s`。

- `ingest.grok.watchdog.max_execution_time`（靜態，時間單位）：設定 Grok 模式比對作業在被監控程式中斷前允許的最長執行時間。這可防止設計不良或惡意的 Grok 模式造成過度的 CPU 使用量或阻塞匯入處理。超過此限制的作業會被終止，以維持叢集穩定性。預設為 `1s`。
