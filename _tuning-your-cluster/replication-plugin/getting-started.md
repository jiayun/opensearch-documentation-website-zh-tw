---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
nav_order: 15
parent: Cross-cluster replication
redirect_from:
  - /replication-plugin/get-started/
---

# 跨叢集複製入門

透過跨叢集複製，您可以將資料編製索引到領導者索引，OpenSearch 會將該資料複製到一或多個唯讀的追隨者索引。領導者索引上的所有後續操作都會複製到追隨者索引，例如建立、更新或刪除文件。

## 先決條件

在設定跨叢集複製之前，請確保符合下列先決條件：

- 領導者叢集與追隨者叢集都必須安裝 replication 外掛程式。
- 如果您在追隨者叢集中為任何節點覆寫了 `node.roles`（位於 `opensearch.yml` 中），請確保 `node.roles` 設定包含 `remote_cluster_client` 角色：

   ```yaml
   node.roles: [<other_roles>, remote_cluster_client]
   ```
   {% include copy.html %}

## 權限

請確保 Security 外掛程式在兩個叢集上都啟用，或在兩個叢集上都停用。如果您已停用 Security 外掛程式，可以略過本節。不過，我們強烈建議在正式環境中啟用 Security 外掛程式。

如果 Security 外掛程式已啟用，請確保非管理員使用者已對應到適當的權限，以便他們能執行複製操作。關於索引與叢集層級權限的需求，請參閱[跨叢集複製權限]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/)。

此外，請在領導者叢集上驗證並新增每個追隨者叢集節點的辨別名稱 (DN)，以允許追隨者連線到領導者。

首先，從每個追隨者叢集取得節點的 DN：

  ```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/_opendistro/_security/api/ssl/certs?pretty'

{
   "transport_certificates_list": [
      {
         "issuer_dn" : "CN=Test,OU=Server CA 1B,O=Test,C=US",
         "subject_dn" : "CN=follower.test.com", # To be added under leader's nodes_dn configuration
         "not_before" : "2021-11-12T00:00:00Z",
         "not_after" : "2022-12-11T23:59:59Z"
      }
   ]
}
  ```

然後驗證它是否屬於 `opensearch.yml` 中領導者叢集組態的一部分。否則，請在下列設定下新增它：

  ```yaml
plugins.security.nodes_dn:
  - "CN=*.leader.com, OU=SSL, O=Test, L=Test, C=DE" # Already part of the configuration
  - "CN=follower.test.com" # From the above response from follower
  ```
## 範例設定

若要在同一網路上啟動兩個單一節點叢集，請將此範例檔案儲存為 `docker-compose.yml` 並執行 `docker compose up`：

```yml
version: '3'
services:
  replication-node1:
    image: opensearchproject/opensearch:{{site.opensearch_version}}
    container_name: replication-node1
    environment:
      - cluster.name=leader-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - opensearch-data2:/usr/share/opensearch/data
    ports:
      - 9201:9200
      - 9700:9600 # required for Performance Analyzer
    networks:
      - opensearch-net
  replication-node2:
    image: opensearchproject/opensearch:{{site.opensearch_version}}
    container_name: replication-node2
    environment:
      - cluster.name=follower-cluster
      - discovery.type=single-node
      - bootstrap.memory_lock=true
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - opensearch-data1:/usr/share/opensearch/data
    ports:
      - 9200:9200
      - 9600:9600 # required for Performance Analyzer
    networks:
      - opensearch-net

volumes:
  opensearch-data1:
  opensearch-data2:

networks:
  opensearch-net:
```

叢集啟動後，驗證每個叢集的名稱：

```bash
curl -XGET -u 'admin:<custom-admin-password>' -k 'https://localhost:9201'
{
  "cluster_name" : "leader-cluster",
  ...
}

curl -XGET -u 'admin:<custom-admin-password>' -k 'https://localhost:9200'
{
  "cluster_name" : "follower-cluster",
  ...
}
```

在本範例中，使用連接埠 9201（`replication-node1`）作為領導者叢集，連接埠 9200（`replication-node2`）作為追隨者叢集。

若要取得領導者叢集的 IP 位址，請先識別其容器 ID：

```bash
docker ps
CONTAINER ID    IMAGE                                       PORTS                                                      NAMES
3b8cdc698be5    opensearchproject/opensearch:{{site.opensearch_version}}   0.0.0.0:9200->9200/tcp, 0.0.0.0:9600->9600/tcp, 9300/tcp   replication-node2
731f5e8b0f4b    opensearchproject/opensearch:{{site.opensearch_version}}   9300/tcp, 0.0.0.0:9201->9200/tcp, 0.0.0.0:9700->9600/tcp   replication-node1
```

然後取得該容器的 IP 位址：

```bash
docker inspect --format='{% raw %}{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}{% endraw %}' 731f5e8b0f4b
172.22.0.3
```

## 建立跨叢集連線

跨叢集複製採用「提取」模型，因此大多數變更發生在追隨者叢集，而非領導者叢集。

### 遠端叢集的連線模式

連線模式包括 _sniff mode_ 與 _proxy mode_。

在 sniff 模式中，追隨者叢集透過指定名稱以及來自領導者叢集的種子節點清單，建立與領導者叢集的遠端連線。在連線設定期間，追隨者叢集會從其中一個提供的種子節點擷取領導者叢集的狀態。此模式要求領導者叢集中種子節點的發布位址必須可從追隨者叢集存取。Sniff 模式是預設的連線模式。

在追隨者叢集上，為每個種子節點新增 IP 位址（含連接埠 9300）。由於這是單一節點叢集，您只有一個種子節點。請為連線提供一個描述性名稱，您將在啟動複製的請求中使用它：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_cluster/settings?pretty' -d '
{
  "persistent": {
    "cluster": {
      "remote": {
        "my-connection-alias": {
          "seeds": ["172.22.0.3:9300"]
        }
      }
    }
  }
}'
```


在 proxy 模式中，追隨者叢集透過指定名稱與單一 proxy 位址，建立與領導者叢集的遠端連線。在連線設定期間，會開啟可設定的數量的 socket 連線到提供的 proxy 位址。proxy 的職責是將這些連線導向領導者叢集中適當的節點。與其他連線模式不同，proxy 模式不要求領導者叢集中的節點具有可公開存取的發布位址：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_cluster/settings?pretty' -d '
{
  "persistent": {
    "cluster": {
      "remote": {
        "my-connection-alias": {
          "mode": "proxy"
          "proxy_address": "172.22.0.3:9300"
        }
      }
    }
  }
}'
```

## 啟動複製

首先，在領導者叢集上建立名為 `leader-01` 的索引：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9201/leader-01?pretty'
```

然後從追隨者叢集啟動複製。在請求本文中，提供連線名稱與您要複製的領導者索引，以及您要使用的安全性角色：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_start?pretty' -d '
{
   "leader_alias": "my-connection-alias",
   "leader_index": "leader-01",
   "use_roles":{
      "leader_cluster_role": "all_access",
      "follower_cluster_role": "all_access"
   }
}'
```

如果 Security 外掛程式已停用，請省略 `use_roles` 參數。但如果已啟用，您必須指定 OpenSearch 用來驗證請求的領導者與追隨者叢集角色。本範例為簡化起見使用 `all_access`，但我們建議在每個叢集上建立複製使用者並[進行相應對應]({{site.url}}{{site.baseurl}}/replication-plugin/permissions/#map-the-leader-and-follower-cluster-roles)。
{: .tip }

此命令會在追隨者叢集上建立一個名為 `follower-01` 的相同唯讀索引，該索引會持續隨領導者叢集上 `leader-01` 索引的變更保持更新。啟動複製會建立新的追隨者索引——您無法將現有索引轉換為追隨者索引。 

## 確認複寫

複寫開始後，取得狀態：

```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_status?pretty'

{
  "status" : "SYNCING",
  "reason" : "User initiated",
  "leader_alias" : "my-connection-alias",
  "leader_index" : "leader-01",
  "follower_index" : "follower-01",
  "syncing_details" : {
    "leader_checkpoint" : -1,
    "follower_checkpoint" : -1,
    "seq_no" : 0
  }
}
```

可能的狀態有 `SYNCING`、`BOOTSTRAPPING`、`PAUSED` 和 `REPLICATION NOT IN PROGRESS`。

領導者和追隨者的檢查點值一開始為負數，並反映分片數量（一個分片為 -1，五個分片為 -5，依此類推）。這些值會隨著每次變更而遞增，並顯示追隨者落後領導者多少個更新。如果索引已完全同步，這些值會相同。

若要確認複寫確實正在進行，請在領導者索引中新增一份文件：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9201/leader-01/_doc/1?pretty' -d '{"The Shining": "Stephen King"}'
```

然後在追隨者索引上驗證複寫的內容：

```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/follower-01/_search?pretty'

{
  ...
  "hits": [{
    "_index": "follower-01",
    "_id": "1",
    "_score": 1.0,
    "_source": {
      "The Shining": "Stephen King"
    }
  }]
}
```
### `.replication-metadata-store` 索引

`.replication-metadata-store` 索引是叢集內複寫相關中繼資料與自動跟隨規則的持久資料存放區。它會儲存從領導者叢集複寫到追隨者叢集的每個索引的複寫中繼資料。

在第一次觸發複寫 API 之後，`.replication-metadata-store` 索引會在追隨者叢集內建立。複寫任務或規則的任何更新或新增也會更新到該索引中。這讓外掛程式能夠維護跨叢集的複寫狀態與規則的完整記錄。
   
 `.replication-metdata-store` 是隱藏索引。
 {: .note}

## 暫停與繼續複寫

如果您需要修正問題或降低領導者叢集的負載，可以暫時暫停索引的複寫：

```bash
curl -XPOST -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_pause?pretty' -d '{}'
```

若要確認複寫已暫停，取得狀態：

```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_status?pretty'

{
  "status" : "PAUSED",
  "reason" : "User initiated",
  "leader_alias" : "my-connection-alias",
  "leader_index" : "leader-01",
  "follower_index" : "follower-01"
}
```

完成變更後，繼續複寫：

```bash
curl -XPOST -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_resume?pretty' -d '{}'
```

複寫繼續後，追隨者索引會接續複寫暫停期間對領導者索引所做的任何變更。

如果複寫暫停的時間超過保留租約期間，您就無法繼續複寫，因為保留租約會過期。若要復原，請使用強制繼續，這會從領導者的快照還原追隨者索引。如需詳細資訊，請參閱[強制繼續複寫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/force-resume/)。

## 停止複寫

當您不再需要複寫某個索引時，請從追隨者叢集終止複寫：

```bash
curl -XPOST -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_stop?pretty' -d '{}'
```

當您停止複寫時，追隨者索引會取消跟隨領導者，並成為您可寫入的標準索引。停止複寫後就無法重新開始複寫。

取得狀態以確認該索引不再被複寫：

```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_replication/follower-01/_status?pretty'

{
  "status" : "REPLICATION NOT IN PROGRESS"
}
```

您也可以對領導者索引進行修改，並確認這些修改不會出現在追隨者索引上，進一步確認複寫已停止。


