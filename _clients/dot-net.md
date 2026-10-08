---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: ".NET 用戶端"
nav_order: 75
has_children: true
has_toc: false
---

# .NET 用戶端

OpenSearch 有兩個 .NET 用戶端：低階的 [OpenSearch.Net]({{site.url}}{{site.baseurl}}/clients/OpenSearch-dot-net/) 用戶端，以及高階的 [OpenSearch.Client]({{site.url}}{{site.baseurl}}/clients/OSC-dot-net/) 用戶端。

[OpenSearch.Net]({{site.url}}{{site.baseurl}}/clients/OpenSearch-dot-net/) 是低階的 .NET 用戶端，提供與 OpenSearch 通訊的基礎層。它沒有相依性，可處理輪詢式負載平衡、傳輸，以及基本的請求／回應循環。OpenSearch.Net 包含所有 OpenSearch API 端點的方法。

[OpenSearch.Client]({{site.url}}{{site.baseurl}}/clients/OSC-dot-net/) 是建構於 OpenSearch.Net 之上的高階 .NET 用戶端。它提供強型別的請求和回應，以及 Query DSL。它提供可自動解析與序列化／還原序列化請求和回應的模型，讓您不必自行建構原始 JSON 請求和解析原始 JSON 回應。如有需要，OpenSearch.Client 也會公開 OpenSearch.Net 低階用戶端。OpenSearch.Client 包含下列進階功能：

- 自動對應：給定 C# 類型，OpenSearch.Client 可推斷要傳送至 OpenSearch 的正確對應。
- 查詢中的運算子多載。
- 類型和索引推斷。

您可以在主控台程式、.NET Core 應用程式、ASP.NET Core 應用程式或背景工作服務中使用這兩個 .NET 用戶端。

若要開始使用 OpenSearch.Client，請依照[高階 .NET 用戶端入門]({{site.url}}{{site.baseurl}}/clients/OSC-dot-net#installing-opensearchclient)或[高階 .NET 用戶端的更多進階功能]({{site.url}}{{site.baseurl}}/clients/OSC-example/)中的指示操作，後者是稍微更進階的逐步解說。

## 相容性

下表列出與各 OpenSearch 版本相容的 OpenSearch.Client 和 OpenSearch.Net 版本。

| OpenSearch 版本 | 用戶端版本 |
|:---|:---|
| 1.x | 1.0.0, 1.1.0 |
| 2.x | 1.1.0 或更新版本 |
| 3.x | 2.0.0 或更新版本 |

2.x 用戶端支援 .NET 8 或更新版本，以及 .NET Framework 4.7.2 或更新版本。這兩個用戶端都以 .NET Standard 2.0 和 .NET Standard 2.1 為目標。OpenSearch.Net 和 OpenSearch.Net.Auth.AwsSigV4 也以 .NET 8 和 .NET 10 為目標。

如需最新的相容性資訊，請參閱用戶端儲存庫中的 [`COMPATIBILITY.md`](https://github.com/opensearch-project/opensearch-net/blob/main/COMPATIBILITY.md) 檔案。如需用戶端版本之間重大變更的資訊，請參閱[升級指南](https://github.com/opensearch-project/opensearch-net/blob/main/UPGRADING.md)。
