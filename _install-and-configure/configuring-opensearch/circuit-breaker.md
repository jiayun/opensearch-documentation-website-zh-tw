---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "斷路器設定"
parent: Configuring OpenSearch
nav_order: 120
---

# 斷路器設定

斷路器可防止 OpenSearch 引發 Java OutOfMemoryError。父斷路器指定所有子斷路器可用的記憶體總量。子斷路器則指定其本身可用的記憶體總量。

若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 父斷路器設定

OpenSearch 支援下列父斷路器設定：

- `indices.breaker.total.use_real_memory`（靜態，布林值）：若為 `true`，父斷路器會考量實際的記憶體使用量。否則，父斷路器會考量子斷路器所保留的記憶體量。預設為 `true`。

- `indices.breaker.total.limit`（動態，百分比）：指定父斷路器的初始記憶體限制。若 `indices.breaker.total.use_real_memory` 為 `true`，預設為 JVM 堆積的 95%。若 `indices.breaker.total.use_real_memory` 為 `false`，預設為 JVM 堆積的 70%。

## 欄位資料斷路器設定

欄位資料斷路器會限制將欄位載入欄位資料快取所需的堆積記憶體。OpenSearch 支援下列欄位資料斷路器設定：

- `indices.breaker.fielddata.limit`（動態，百分比）：指定欄位資料斷路器的記憶體限制。預設為 JVM 堆積的 40%。

- `indices.breaker.fielddata.overhead`（動態，double）：用於乘以欄位資料估計值以決定最終估計值的常數。預設為 1.03。

## 請求斷路器設定

請求斷路器會限制建構請求所需資料結構（例如計算彙總時）所需的記憶體。OpenSearch 支援下列請求斷路器設定：

- `indices.breaker.request.limit`（動態，百分比）：指定請求斷路器的記憶體限制。預設為 JVM 堆積的 60%。

- `indices.breaker.request.overhead`（動態，double）：用於乘以請求估計值以決定最終估計值的常數。預設為 1。

## 進行中請求斷路器設定

進行中請求斷路器會限制傳輸層與 HTTP 層上所有目前正在執行之傳入請求的記憶體使用量。請求的記憶體使用量是根據請求的內容長度計算，並包含原始請求以及代表該請求之結構化物件所需的記憶體。OpenSearch 支援下列進行中請求斷路器設定：

- `network.breaker.inflight_requests.limit`（動態，百分比）：指定進行中請求斷路器的記憶體限制。預設為 JVM 堆積的 100%（因此，進行中請求的記憶體使用量限制由父斷路器的記憶體限制決定）。

- `network.breaker.inflight_requests.overhead`（動態，double）：用於乘以進行中請求估計值以決定最終估計值的常數。預設為 2。

## 指令碼編譯斷路器設定

指令碼編譯斷路器會限制 OpenSearch 在一段時間間隔內編譯的不重複指令碼數量。超過限制時，OpenSearch 會傳回 `circuit_breaking_exception`。根據預設，每個指令碼內容各自有每 5 分鐘 75 次編譯的限制，由 `script.context.<context>.max_compilations_rate` 設定。`script.max_compilations_rate` 設定會以單一的叢集層級限制取代各內容的個別限制。如需詳細資訊，請參閱[指令碼編譯設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/script-and-resource-settings/#script-compilation-settings)。

## 規則運算式斷路器設定

規則運算式斷路器可啟用或停用規則運算式，並限制其複雜度。OpenSearch 支援下列規則運算式斷路器設定：

- `script.painless.regex.enabled`（靜態，字串）：決定 Painless 指令碼是否可包含規則運算式，以及其複雜度是否受到限制。有效值為 `limited`、`true` 與 `false`。預設為 `limited`。如需各值的說明，請參閱[控制規則運算式]({{site.url}}{{site.baseurl}}/scripting/painless/#controlling-regular-expressions)。

- `script.painless.regex.limit-factor`（靜態，整數）：僅在 `script.painless.regex.enabled` 設為 `limited` 時套用。限制 Painless 指令碼中的規則運算式可檢查的字元數。字元限制的計算方式為將指令碼輸入的字元數乘以 `script.painless.regex.limit-factor`。預設為 `6`，因此若輸入有 5 個字元，規則運算式最多可檢查 5 &middot; 6 = 30 個字元。
