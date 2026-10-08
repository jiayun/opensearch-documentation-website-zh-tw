---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼與資源設定"
parent: Configuring OpenSearch
nav_order: 160
---

# 指令碼與資源設定

OpenSearch 提供用於管理指令碼編譯行為與資源檔案監控的設定。這些設定有助於控制指令碼效能、安全性，以及組態檔案和其他資源的自動重新載入。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 資源重新載入設定

資源重新載入設定控制組態檔案、安全性憑證，以及 OpenSearch 需要監看變更的其他資源的監控與自動重新載入。

OpenSearch 支援下列靜態資源重新載入設定：

- `resource.reload.enabled`（靜態，布林值）：啟用或停用資源監看服務。啟用時，OpenSearch 會監控已註冊資源的變更，並定期重新載入這些資源。這有助於自動偵測組態檔案、安全性憑證和其他資源的變更，而不需要重新啟動叢集。預設值為 `true`。

- `resource.reload.interval.low`（靜態，時間單位）：設定低頻率資源監控的重新載入間隔。以低頻率註冊的資源會以此間隔檢查變更。這通常用於不常變更的資源，例如組態檔案。預設值為 `60s`（60 秒）。

- `resource.reload.interval.medium`（靜態，時間單位）：設定中頻率資源監控的重新載入間隔。以中頻率註冊的資源會以此間隔檢查變更。這可為變更頻率適中的資源，在回應速度與系統負載之間取得平衡。預設值為 `30s`（30 秒）。

- `resource.reload.interval.high`（靜態，時間單位）：設定高頻率資源監控作業的重新載入間隔。此設定控制 OpenSearch 檢查需要頻繁監控之資源（例如組態檔案或安全性憑證）變更的頻率。較頻繁的檢查能更快回應變更，但會消耗更多系統資源。資源監看服務會將此設定用於高優先順序的資源。預設值為 `5s`。

## 指令碼大小設定

OpenSearch 支援下列動態指令碼大小設定：

- `script.max_size_in_bytes`（動態，整數）：設定單一指令碼的大小上限（以位元組為單位）。OpenSearch 會拒絕超過此長度的指令碼。預設值為 `65535`。

請務必先刪除所有超過新值的已儲存指令碼，再調低 `script.max_size_in_bytes`。OpenSearch 會接受此設定，但隨後無法套用，而且在移除此設定之前，節點會停止套用後續的叢集狀態更新。
{: .warning}

## 指令碼編譯設定

OpenSearch 會在第一次使用指令碼時進行編譯並快取編譯結果，因此只有在指令碼定義變更時才會重新編譯。編譯速率限制會限定節點在一段時間範圍內執行的新編譯次數，以防止大量不重複的指令碼將節點的 CPU 耗用在編譯上。如需快取與速率限制如何套用至工作負載的說明，請參閱[編譯限制與快取]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#compilation-limits-and-caching)。

`script.max_compilations_rate` 的值決定快取與速率限制是針對每個指令碼內容分別追蹤，還是在整個叢集中共用。OpenSearch 支援下列指令碼編譯設定：

- `script.max_compilations_rate`（動態，字串）：設為 `use-context` 可讓每個指令碼內容擁有各自的快取與編譯速率，並透過[指令碼內容設定](#script-context-settings)進行設定。若改設為 `<count>/<time>` 形式的速率（例如 `150/5m`），則會改用單一的全叢集限制與一個共用快取，此時各內容的設定會遭到拒絕。預設值為 `use-context`。

- `script.cache.max_size`（靜態，整數）：設定每個節點的共用快取中保留的已編譯指令碼數量。快取已滿時，會移出最近最少使用的指令碼。明確設定此設定也會將 `script.context.<context>.cache_max_size` 的預設值變更為相同的值。預設值為 `100`。

- `script.cache.expire`（靜態，時間單位）：設定已編譯指令碼從共用快取中移出的時間，移出後必須在下次使用時重新編譯。明確設定此設定也會將 `script.context.<context>.cache_expire` 的預設值變更為相同的值。預設值為 `0ms`，表示快取的指令碼不會依計時器到期。

- `script.disable_max_compilations_rate`（靜態，布林值）：設為 `true` 時會完全移除編譯速率限制。此設定與明確設定的 `script.max_compilations_rate` 以及任何各內容的速率皆會衝突，因此請先移除這些設定再設定此項。預設值為 `false`。

`script.max_compilations_rate`、`script.cache.max_size` 和 `script.cache.expire` 已遭棄用，因為它們是為了支援單一共用快取而存在。請將 `script.max_compilations_rate` 保持為 `use-context`，並設定各內容的設定；這些設定為動態設定，不需重新啟動即可生效。
{: .note}

沒有編譯限制的叢集，會讓任何能提交指令碼的用戶端無限制地耗用編譯所需的 CPU。請將觸發限制的指令碼參數化，而不要關閉限制。如需更多資訊，請參閱[以參數傳遞值]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#passing-values-as-parameters)。
{: .warning}

## 指令碼內容設定

指令碼內容設定控制個別指令碼內容的快取與編譯，讓某個內容中大量的重新編譯不會移出另一個內容的快取指令碼。這些設定只有在 `script.max_compilations_rate` 設為 `use-context` 時才會套用。請將 `<context>` 替換為 [Get Script Contexts API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-contexts/) 傳回的內容名稱。

OpenSearch 支援下列動態指令碼內容設定：

- `script.context.<context>.cache_max_size`（動態，整數）：設定此內容保留的已編譯指令碼數量。較大的快取可降低使用許多不同指令碼之工作負載的編譯負擔，但會耗用更多記憶體。大多數內容的預設值為 `100`；若已明確設定 `script.cache.max_size`，則預設值為該設定的值。

- `script.context.<context>.cache_expire`（動態，時間單位）：設定此內容的已編譯指令碼從快取中移出的時間，移出後必須在下次使用時重新編譯。預設值為 `0ms`，表示快取的指令碼不會依計時器到期；若已明確設定 `script.cache.expire`，則預設值為該設定的值。

- `script.context.<context>.max_compilations_rate`（動態，字串）：設定此內容在一段時間範圍內允許的編譯次數，格式為 `<count>/<time>`，例如 `200/1m`。設為 `unlimited` 可移除此內容的限制。超過速率時，OpenSearch 會傳回 `circuit_breaking_exception`，並附帶「Too many dynamic script compilations」訊息。大多數內容的預設值為 `75/5m`。

有三個內容的預設值不同。下表列出這些內容。

內容 | 用途 | `cache_max_size` | `max_compilations_rate`
:--- | :--- | :--- | :---
`search` | [`script` 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/script-processor/)。 | `200` | `unlimited`
`ingest` | [`script` 匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/script/)。 | `200` | `unlimited`
`processor_conditional` | 匯入處理器上的 `if` 條件。 | `200` | `unlimited`

在 `script.max_compilations_rate` 設為明確速率時設定任何各內容的設定，會失敗並傳回 `Context cache settings [<settings>] requires [script.max_compilations_rate] to be [use-context]`。
{: .note}

如需限制叢集接受哪些指令碼，以及如何約束 Painless 中規則運算式的設定，請參閱[指令碼安全性]({{site.url}}{{site.baseurl}}/scripting/script-security/)。