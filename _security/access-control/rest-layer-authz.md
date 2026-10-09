---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "REST 層授權"
parent: Access control
nav_order: 85
---


# REST 層授權

REST 層授權透過在 REST 層提供授權檢查機制，為外掛程式與擴充功能的 API 請求增加一層安全性。這一層安全性位於傳輸層之上，提供一種互補的授權方式，而不會取代、修改或以任何方式改變傳輸層上的相同程序。REST 層授權最初是為了滿足擴充功能的授權檢查需求而建立，因為擴充功能並不透過傳輸層通訊。不過，未來在為 OpenSearch 開發外掛程式時，希望使用此功能的開發人員也可以使用這項功能。

對使用 REST 層授權的使用者而言，指派角色、對應使用者與角色的方式，以及外掛程式與擴充功能的一般用法都維持不變——唯一額外的需求是使用者必須熟悉新的權限方案。

另一方面，開發人員則需要了解 `NamedRoute` 背後的概念，以及新路徑方案的建構方式。詳細資訊請參閱 [外掛程式的 REST 層授權](https://github.com/opensearch-project/security/blob/main/REST_AUTHZ_FOR_PLUGINS.md)。

使用 REST 層進行授權的好處包括能在 REST 層授權請求並過濾未經授權的請求。如此一來，可減輕傳輸層的處理負擔，同時對 API 的存取進行細緻的控制。

某些讀取操作（例如 [scroll]({{site.url}}{{site.baseurl}}/api-reference/scroll/)）會管理狀態。因此，建議使用 Security plugin 的 [權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/) 來控制讀寫存取，而不是允許/封鎖 HTTP 請求動詞。

您必須啟用 Security plugin 才能使用 REST 層授權。
{: .note }


## NamedRoute

REST 層授權讓叢集管理員能夠授予或撤銷對叢集中特定端點的存取權。為達成此目的，通往資源的路徑會使用一個唯一名稱。

為了支援 REST 層授權，OpenSearch Project 為路徑註冊導入了 [`NamedRoute`](https://github.com/opensearch-project/OpenSearch/blob/main/server/src/main/java/org/opensearch/rest/NamedRoute.java) 的概念。對開發人員而言，此標準要求使用唯一名稱的新路徑註冊方式。傳輸動作通常由方法名稱、一部分與對應的傳輸動作組成，而這個新的實作則要求方法名稱、一部分，以及路徑的唯一名稱。顧名思義，該名稱必須在所有外掛程式與擴充功能之間保持唯一，換句話說，不得註冊到任何其他路徑。

例如，請考慮以下 Anomaly Detection 資源的路徑：

`_/detectors/<detectorId>/profile`

對擴充功能而言，您可以透過在資源的 `settings.yml` 檔案中參照 `routeNamePrefix` 值（在此例中為 `ad`），並將其加入路徑以組成唯一名稱，從而建立 `NamedRoute`。結果如下列範例所示：

`ad:detectors/profile`

對外掛程式而言，您可以使用外掛程式的名稱取代 `routeNamePrefix` 值。

路徑名稱接著可以用與傳統權限相同的方式對應到角色。以下範例示範了這一點：

```yml
ad_role:
  reserved: true
  cluster_permissions:
    - 'ad:detectors/profile'
```


## 對應使用者與角色

使用 `NamedRoute` 對應使用者與角色的方式沒有任何改變。此外，新的權限格式與現有組態相容。本節提供一個範例，說明使用者與角色對應在舊式與 `NamedRoute` 組態中的呈現方式，以及它們如何為動作授權已註冊的路徑。

當使用者發起 REST 請求時，系統會檢查該使用者的角色，並評估與該使用者相關聯的每個權限，以判斷是否與指派給路徑的唯一名稱相符，或與路徑註冊時定義的任何舊式動作相符。使用者可以對應到包含唯一名稱格式權限或舊式動作的角色。請考慮以下虛構外掛程式 `abc` 的角色：

```yml
abcplugin_read_access:
   reserved: true
   cluster_permissions:
     - 'cluster:admin/opensearch/abcplugin/route/get'
```

同時請考慮以下角色對應：

```yml
abcplugin_read_access:
	 reserved: true
	 users:
		 - "user-A"
```

如果 `user-A` 對路徑 `/_plugins/_abcplugin/route/get` 發出 REST API 呼叫，該使用者將獲得此動作的授權。然而，對於其他路徑（例如 `/_plugins/_abcplugin/route/delete`），請求會被拒絕。

相同的邏輯也適用於對路徑使用唯一名稱以及 `NamedRoute` 概念的角色與角色對應。請考慮同一外掛程式 `abc` 的以下角色：

```yml
abcplugin_read_access_nr:
   reserved: true
   cluster_permissions:
     - 'abcplugin:routeGet'
     - 'abcplugin:routePut'
     - 'abcplugin:routeDelete'
```

同時請考慮以下角色對應：

```yml
abcplugin_read_access_nr:
	 reserved: true
	 users:
		 - "user-B"
```

在第二種情況中，如果 `user-B` 對路徑 `/_plugins/_abcplugin/route/get`、`/_plugins/_abcplugin/route/put` 或 `/_plugins/_abcplugin/route/delete` 中的任何一個發出 REST API 呼叫，該使用者將獲得此動作的授權。

