---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動跟隨"
nav_order: 20
parent: Cross-cluster replication
redirect_from:
  - /replication-plugin/auto-follow/
---

# 跨叢集複製的自動跟隨

自動跟隨讓您能根據符合的模式，自動複製在領導者叢集上建立的索引。當您在領導者叢集上建立名稱符合指定模式 (例如 `index-01*`) 的索引時，對應的跟隨者索引會自動在跟隨者叢集上建立。

您可以為單一叢集設定多個複製規則。這些模式僅支援萬用字元比對。

## 必要條件

在啟用自動跟隨之前，您需要先在兩個叢集之間[建立跨叢集連線]({{site.url}}{{site.baseurl}}/replication-plugin/get-started/#set-up-a-cross-cluster-connection)。

## 權限

如果已啟用 Security 外掛程式，請確定非管理員使用者已對應至適當的權限，以便執行複製動作。關於索引與叢集層級權限的需求，請參閱[跨叢集複製權限]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/)。

## 開始使用自動跟隨

複製規則是針對單一跟隨者叢集建立的一組模式。當您建立複製規則時，它會先自動複製任何符合模式的*現有*索引，然後持續複製您所建立且符合模式的任何*新*索引。

在跟隨者叢集上建立複製規則：

```bash
curl -XPOST -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/_autofollow?pretty' -d '
{
   "leader_alias" : "my-connection-alias",
   "name": "my-replication-rule",
   "pattern": "movies*",
   "use_roles":{
      "leader_cluster_role": "all_access",
      "follower_cluster_role": "all_access"
   }
}'
```
{% include copy.html %}

如果已停用 Security 外掛程式，您可以省略 `use_roles` 參數。但如果已啟用，您需要指定 OpenSearch 用來驗證請求的領導者與跟隨者叢集角色。此範例為求簡便使用 `all_access`，但我們建議在每個叢集上建立複製使用者並[進行對應]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/#map-the-leader-and-follower-cluster-roles)。
{: .tip }

若要測試此規則，請在領導者叢集上建立符合的索引：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9201/movies-0001?pretty'
```
{% include copy.html %}

確認副本出現在跟隨者叢集上：

```bash
curl -XGET -u 'admin:<custom-admin-password>' -k 'https://localhost:9200/_cat/indices?v'
```
{% include copy.html %}

索引可能需要數秒才會出現。

```bash
health status index        uuid                     pri rep docs.count docs.deleted store.size pri.store.size
yellow open   movies-0001  kHOxYYHxRMeszLjTD9rvSQ     1   1          0            0       208b           208b
```

## 自訂跟隨者索引名稱

預設情況下，自動跟隨會為每個跟隨者索引指定與其領導者索引相同的名稱。若要對複製規則建立的所有跟隨者索引套用不同的命名慣例，請指定 `follower_index_pattern` 參數。當跟隨者叢集已包含與領導者索引同名的本機索引，或當您從多個領導者叢集複製索引時，自訂名稱可避免名稱衝突。

`follower_index_pattern` 值可以包含靜態文字與 {% raw %}`{{leader_index}}`{% endraw %} 預留位置。在複製時，OpenSearch 會將預留位置取代為符合的領導者索引名稱，因此您可以加入前置詞、後置詞或兩者。

下列請求會建立一個複製規則，為每個跟隨者索引名稱附加 `-replica` 後置詞：

```bash
curl -XPOST -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/_autofollow?pretty' -d '
{
   "leader_alias" : "my-connection-alias",
   "name": "my-replication-rule",
   "pattern": "movies*",
   "follower_index_pattern": "{% raw %}{{leader_index}}{% endraw %}-replica",
   "use_roles":{
      "leader_cluster_role": "all_access",
      "follower_cluster_role": "all_access"
   }
}'
```
{% include copy.html %}

使用此規則時，OpenSearch 會將名為 `movies-2025` 的領導者索引複製到名為 `movies-2025-replica` 的跟隨者索引。

## 擷取複製規則

若要擷取叢集上已設定的現有複製規則清單，請傳送下列請求：

```bash
curl -XGET -u 'admin:<custom-admin-password>' -k 'https://localhost:9200/_plugins/_replication/autofollow_stats'
```
{% include copy.html %}

回應包含複製規則及其統計資料：

```json
{
   "num_success_start_replication": 1,
   "num_failed_start_replication": 0,
   "num_failed_leader_calls": 0,
   "failed_indices":[
      
   ],
   "autofollow_stats":[
      {
         "name":"my-replication-rule",
         "pattern":"movies*",
         "num_success_start_replication": 1,
         "num_failed_start_replication": 0,
         "num_failed_leader_calls": 0,
         "failed_indices":[
            
         ]
      }
   ]
}
```

## 刪除複製規則

若要刪除複製規則，請將下列請求傳送至跟隨者叢集：

```bash
curl -XDELETE -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/_autofollow?pretty' -d '
{
   "leader_alias" : "my-connection-alias",
   "name": "my-replication-rule"
}'
```
{% include copy.html %}

當您刪除複製規則時，OpenSearch 會停止複製符合模式的*新*索引，但該規則先前建立的現有索引仍保持唯讀並持續複製。如果您需要停止現有的複製活動並開放索引寫入，請使用[停止複製 API 操作]({{site.url}}{{site.baseurl}}/replication-plugin/api/#stop-replication)。
