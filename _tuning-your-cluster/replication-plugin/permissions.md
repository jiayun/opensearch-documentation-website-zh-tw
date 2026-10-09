---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複寫安全性"
nav_order: 30
parent: Cross-cluster replication
redirect_from:
  - /replication-plugin/permissions/
---

# 跨叢集複寫安全性

您可以將[安全性外掛程式]({{site.url}}{{site.baseurl}}/security/index/)與跨叢集複寫搭配使用，以限制使用者只能執行特定動作。例如，您可能希望特定使用者只能在領導者或跟隨者叢集上執行複寫活動。

由於跨叢集複寫涉及多個叢集，叢集可能會有不同的安全性組態。支援下列組態：

- 兩個叢集都完整啟用安全性外掛程式
- 兩個叢集都只為 TLS 啟用安全性外掛程式 (`plugins.security.ssl_only`)
- 兩個叢集都未安裝或停用安全性外掛程式 (不建議)

在領導者與跟隨者叢集上都啟用節點對節點加密，以確保叢集之間的複寫流量經過加密。

## 基本權限

為了讓非管理員使用者執行複寫活動，必須將他們對應至適當的權限。

安全性外掛程式有兩個內建角色，涵蓋大多數複寫使用案例：`cross_cluster_replication_leader_full_access` 提供領導者叢集上的複寫權限，`cross_cluster_replication_follower_full_access` 則提供跟隨者叢集上的複寫權限。如需各自的說明，請參閱[預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

如果您不想使用預設角色，可以結合個別的複寫[權限]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/permissions/#replication-permissions)以符合您的需求。大多數權限對應於特定的 REST API 操作。例如，`indices:admin/plugins/replication/index/pause` 權限可讓您暫停複寫。

## 對應領導者與跟隨者叢集角色

[開始複寫]({{site.url}}{{site.baseurl}}/replication-plugin/api/#start-replication)與[建立複寫規則]({{site.url}}{{site.baseurl}}/replication-plugin/api/#create-replication-rule)操作是特殊情況。它們涉及領導者與跟隨者叢集上必須與角色相關聯的背景處理程序。當您執行其中一個動作時，必須在請求中明確傳遞 `leader_cluster_role` 與
`follower_cluster_role`，OpenSearch 接著會在所有後端複寫工作中使用它們。

若要讓非管理員能夠開始複寫並建立複寫規則，請在每個叢集上建立相同的使用者 (例如 `replication_user`)，並將他們對應至遠端叢集上的 `cross_cluster_replication_leader_full_access` 角色以及跟隨者叢集上的 `cross_cluster_replication_follower_full_access`。如需教學，請參閱[將使用者對應至角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles/#mapping-users-to-roles)。

接著將這些角色新增至請求，並使用適當的認證簽署該請求：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'replication_user:password' 'https://localhost:9200/_plugins/_replication/follower-01/_start?pretty' -d '
{
   "leader_alias": "leader-cluster",
   "leader_index": "leader-01",
   "use_roles":{
      "leader_cluster_role": "cross_cluster_replication_leader_full_access",
      "follower_cluster_role": "cross_cluster_replication_follower_full_access"
   }
}'
```

您可以使用個別權限建立自己的自訂領導者與跟隨者叢集角色，但我們建議使用預設角色，它們適合大多數使用案例。

## 複寫權限

下列各節列出跨叢集複寫可用的索引與叢集層級權限。

### 跟隨者叢集

安全性外掛程式支援跟隨者叢集的下列權限：

```
indices:admin/plugins/replication/index/setup/validate
indices:admin/plugins/replication/index/start
indices:admin/plugins/replication/index/pause
indices:admin/plugins/replication/index/resume
indices:admin/plugins/replication/index/stop
indices:admin/plugins/replication/index/update
indices:admin/plugins/replication/index/status_check
indices:data/write/plugins/replication/changes
cluster:admin/plugins/replication/autofollow/update
```

### 領導者叢集

安全性外掛程式支援領導者叢集的下列權限：

```
indices:admin/plugins/replication/index/setup/validate
indices:data/read/plugins/replication/file_chunk
indices:data/read/plugins/replication/changes
```
