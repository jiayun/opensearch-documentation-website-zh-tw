---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ".NET 用戶端注意事項"
nav_order: 20
has_children: false
parent: .NET clients
---

# .NET 用戶端注意事項與最佳做法

以下各節提供使用 .NET 用戶端時的注意事項與最佳做法相關資訊。

## 將 OpenSearch.Client 註冊為單一執行個體

原則上，您應將 OpenSearch.Client 設定為單一執行個體 (singleton)。OpenSearch.Client 會管理與伺服器的連線，以及叢集中各節點的狀態。此外，每個用戶端在設定時都會使用大量組態。因此，建立一次 OpenSearch.Client 執行個體，並在所有 OpenSearch 作業中重複使用，會比較有利。此用戶端具備執行緒安全性，因此多個執行緒可以共用同一個執行個體。

## 例外狀況

以下是 .NET 用戶端可能擲回的例外狀況類型：

- `OpenSearchClientException` 是已知的例外狀況，發生在請求管線中（例如達到逾時）或 OpenSearch 中（例如查詢格式錯誤）。如果是 OpenSearch 例外狀況，`ServerError` 回應屬性會包含 OpenSearch 傳回的錯誤。
- `UnexpectedOpenSearchClientException` 是未知的例外狀況（例如還原序列化期間發生的錯誤），且為 OpenSearchClientException 的子類別。
- 未正確使用 API 時，會擲回系統例外狀況。

## 節點

若要建立節點，請將 `Uri` 物件傳入其建構函式：

```cs
var uri = new Uri("http://example.org/opensearch");
var node = new Node(uri);
```
{% include copy.html %}

節點在初次建立時具備叢集管理員資格，且其 `HoldsData` 屬性會設為 true。
先前建立之節點的 `AbsolutePath` 屬性為 `"/opensearch/"`：系統會附加結尾的正斜線，以便輕鬆組合路徑。若未指定，預設的 `Port` 為 80。

如果節點具有相同的端點，即視為相等。檢查節點是否相等時，不會將中繼資料納入考量。
{: .note}

## 連線集區

連線集區是 `IConnectionPool` 的執行個體，負責管理 OpenSearch 叢集中的節點。我們建議建立搭配單一 `ConnectionSettings` 物件的[單一執行個體用戶端](#registering-opensearchclient-as-a-singleton)。用戶端及其 `ConnectionSettings` 的存留期間皆與應用程式的存留期間相同。

以下是連線集區的類型。

- **SingleNodeConnectionPool**

`SingleNodeConnectionPool` 是預設的連線集區，在未將連線集區傳入 `ConnectionSettings` 建構函式時使用。如果叢集中只有一個節點，或叢集以負載平衡器作為進入點，請使用 `SingleNodeConnectionPool`。`SingleNodeConnectionPool` 不支援探查 (sniffing) 或 ping，也不會將節點標記為失效或存活。

- **CloudConnectionPool**

`CloudConnectionPool` 是 `SingleNodeConnectionPool` 的子類別，會接受 Cloud ID 與認證。與 `SingleNodeConnectionPool` 相同，`CloudConnectionPool` 不支援探查或 ping。

- **StaticConnectionPool**

`StaticConnectionPool` 適用於您不想開啟探查來了解叢集拓撲的小型叢集。`StaticConnectionPool` 不支援探查，但可以支援 ping。

- **SniffingConnectionPool**

`SniffingConnectionPool` 是 `StaticConnectionPool` 的子類別。它具備執行緒安全性，並支援探查與 ping。`SniffingConnectionPool` 可以在執行階段重新植入節點，且您可以在植入時指定節點角色。

- **StickyConnectionPool**

`StickyConnectionPool` 設定為傳回第一個存活的節點，該節點隨後會在各請求之間持續使用。您可以使用 `Uri` 或 `Node` 物件的可列舉集合來植入節點。`StickyConnectionPool` 不支援探查，但支援 ping。

- **StickySniffingConnectionPool**

`StickySniffingConnectionPool` 是 `SniffingConnectionPool` 的子類別。與 `StickyConnectionPool` 相同，它會傳回第一個存活的節點，該節點隨後會在各請求之間持續使用。`StickySniffingConnectionPool` 支援探查與排序，讓應用程式的每個執行個體都能優先使用不同的節點。節點具有相關聯的權重，並可依權重排序。

## 重試

如果請求未成功，系統會自動重試。根據預設，重試次數為 OpenSearch.Client 所知叢集中的節點數量。重試次數也受逾時參數限制，因此 OpenSearch.Client 會在逾時期間內盡可能多次重試請求。

若要設定最大重試次數，請在 `ConnectionSettings` 物件的 `MaximumRetries` 屬性中指定次數。

```cs
var settings = new ConnectionSettings(connectionPool).MaximumRetries(5);
```
{% include copy.html %}

您也可以設定 `RequestTimeout` 來指定單一請求的逾時，並設定 `MaxRetryTimeout` 來指定所有重試嘗試的時間限制。在以下範例中，`RequestTimeout` 設為 4 秒，`MaxRetryTimeout` 設為 12 秒，因此查詢的最大嘗試次數為 3 次。

```cs
var settings = new ConnectionSettings(connectionPool)
            .RequestTimeout(TimeSpan.FromSeconds(4))
            .MaxRetryTimeout(TimeSpan.FromSeconds(12));
```
{% include copy.html %}

## 容錯移轉

如果您使用的連線集區包含多個節點，當請求傳回 502 (Bad Gateway)、503 (Service Unavailable) 或 504 (Gateway Timeout) HTTP 錯誤回應碼時，系統會重試該請求。如果回應碼為 400–501 或 505–599 範圍內的錯誤碼，則不會重試請求。

如果回應碼在 2xx 範圍內，或回應碼為此請求的預期值之一，該回應即視為有效。例如，對於檢查索引是否存在的請求，404 (Not Found) 是有效的回應。