---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "跨叢集搜尋"
nav_order: 230
redirect_from:
 - /security/access-control/cross-cluster-search/
 - /security-plugin/access-control/cross-cluster-search/
---

# 跨叢集搜尋

您可以使用 OpenSearch 中的跨叢集搜尋（CCS），跨多個叢集搜尋與分析資料，從分散式資料來源取得洞察。Security 外掛程式預設提供跨叢集搜尋，但您需要設定每個叢集，允許其他叢集的遠端連線。這包括建立遠端叢集連線及設定存取權限。

---

#### 目錄
1. 目錄
{:toc}


---

## 先決條件

設定跨叢集搜尋之前，請確保符合下列先決條件：

- 如果您已在參與跨叢集搜尋的叢集中，覆寫任何節點的 `opensearch.yml` 中的 `node.roles`，請確保 `node.roles` 設定包含 `remote_cluster_client` 角色：

   ```yaml
   node.roles: [<other_roles>, remote_cluster_client]
   ```
   {% include copy.html %}

## 驗證流程

下列步驟說明使用跨叢集搜尋，從*協調叢集*存取*遠端叢集*時的驗證流程。您可以在遠端叢集與協調叢集上使用不同的驗證與授權組態，但我們建議兩者使用相同的設定。

1. Security 外掛程式在協調叢集上驗證使用者。
1. Security 外掛程式在協調叢集上擷取使用者的後端角色。
1. 呼叫連同已通過驗證的使用者資訊一起轉送至遠端叢集。
1. 在遠端叢集上評估使用者的權限。

## 遠端叢集角色評估
**於 3.9 版推出**
{: .label .label-purple }

預設情況下，遠端叢集會結合協調叢集傳遞的安全性角色及自身的角色對應來評估權限。因此，在協調叢集上具有廣泛權限（例如 `all_access`）的使用者，在遠端叢集上也會取得相同的權限。

若要讓遠端叢集獨立控制 CCS 使用者取得的權限，請在遠端叢集上設定下列叢集設定：

```json
PUT /_cluster/settings
{
  "persistent": {
    "plugins.security.ccs.ignore_source_security_roles": true
  }
}
```
{% include copy-curl.html %}

當 `plugins.security.ccs.ignore_source_security_roles` 為 `true` 時，遠端叢集會移除協調叢集傳遞的安全性角色，並僅透過自身的 `roles_mapping.yml` 組態評估存取權限。接著，您便可以在每個叢集上獨立定義 CCS 使用者權限。此設定預設為 `false`，因此既有的 CCS 部署不受影響。

### 限制

此設定有下列限制：

- 遠端叢集不會重新驗證 CCS 使用者，因此不會查閱 `internal_users.yml` 中的角色指派。啟用此設定時，您必須使用 `roles_mapping.yml` 授予 CCS 使用者遠端叢集的存取權限。在 `internal_users.yml` 中使用 `opendistro_security_roles` 進行的角色指派，對 CCS 使用者授權沒有影響。
- 此設定僅適用於跨叢集搜尋請求。其他跨叢集作業不受影響。

## 設定權限

若要查詢遠端叢集上的索引，使用者必須具有 `READ` 或 `SEARCH` 權限。此外，當搜尋請求包含查詢參數 `ccs_minimize_roundtrips=false`（此參數告知 OpenSearch 不要盡量減少傳送至遠端叢集及從遠端叢集接收的請求）時，使用者還需要具有下列額外的索引權限：

```
indices:admin/shards/search_shards
```

如需 `ccs_minimize_roundtrips` 參數的詳細資訊，請參閱 Search API 的[參數]({{site.url}}{{site.baseurl}}/api-reference/search/#query-parameters)清單。

#### roles.yml 組態範例

```yml
humanresources:
  cluster:
    - CLUSTER_COMPOSITE_OPS_RO
  indices:
    'humanresources':
      '*':
        - READ
        - indices:admin/shards/search_shards # needed when the search request includes parameter setting 'ccs_minimize_roundtrips=false'.
```


#### OpenSearch Dashboards 中的角色範例

![用於建立跨叢集搜尋角色的 OpenSearch Dashboards 面板]({{site.url}}{{site.baseurl}}/images/security-ccs.png)


## Docker 設定範例

若要定義 Docker 權限，請將下列範例檔案儲存為 `docker-compose.yml`，並執行 `docker compose up`，以在同一個網路上啟動兩個單一節點叢集：

```yml
version: '3'
services:
  opensearch-ccs-node1:
    image: opensearchproject/opensearch:{{site.opensearch_version}}
    container_name: opensearch-ccs-node1
    environment:
      - cluster.name=opensearch-ccs-cluster1
      - discovery.type=single-node
      - bootstrap.memory_lock=true # along with the memlock settings below, disables swapping
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" # minimum and maximum Java heap size, recommend setting both to 50% of system RAM
      - "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>" # The initial admin password used by the demo configuration
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

  opensearch-ccs-node2:
    image: opensearchproject/opensearch:{{site.opensearch_version}}
    container_name: opensearch-ccs-node2
    environment:
      - cluster.name=opensearch-ccs-cluster2
      - discovery.type=single-node
      - bootstrap.memory_lock=true # along with the memlock settings below, disables swapping
      - "OPENSEARCH_JAVA_OPTS=-Xms512m -Xmx512m" # minimum and maximum Java heap size, recommend setting both to 50% of system RAM
      - "OPENSEARCH_INITIAL_ADMIN_PASSWORD=<custom-admin-password>" # The initial admin password used by the demo configuration
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - opensearch-data2:/usr/share/opensearch/data
    ports:
      - 9250:9200
      - 9700:9600 # required for Performance Analyzer
    networks:
      - opensearch-net

volumes:
  opensearch-data1:
  opensearch-data2:

networks:
  opensearch-net:
```

叢集啟動後，請使用下列命令確認每個叢集的名稱：

```json
curl -XGET -u 'admin:<custom-admin-password>' -k 'https://localhost:9200'
{
  "cluster_name" : "opensearch-ccs-cluster1",
  ...
}

curl -XGET -u 'admin:<custom-admin-password>' -k 'https://localhost:9250'
{
  "cluster_name" : "opensearch-ccs-cluster2",
  ...
}
```

兩個叢集都在 `localhost` 上執行，因此重要的識別資訊是連接埠號碼。在此範例中，使用連接埠 9200（`opensearch-ccs-node1`）作為遠端叢集，並使用連接埠 9250（`opensearch-ccs-node2`）作為協調叢集。

若要取得遠端叢集的 IP 位址，請先找出其容器 ID：

```bash
docker ps
CONTAINER ID    IMAGE                                       PORTS                                                      NAMES
6fe89ebc5a8e    opensearchproject/opensearch:{{site.opensearch_version}}   0.0.0.0:9200->9200/tcp, 0.0.0.0:9600->9600/tcp, 9300/tcp   opensearch-ccs-node1
2da08b6c54d8    opensearchproject/opensearch:{{site.opensearch_version}}   9300/tcp, 0.0.0.0:9250->9200/tcp, 0.0.0.0:9700->9600/tcp   opensearch-ccs-node2
```

接著取得該容器的 IP 位址：

```bash
docker inspect --format='{% raw %}{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}{% endraw %}' 6fe89ebc5a8e
172.31.0.3
```

在協調叢集上，新增遠端叢集名稱及每個「種子節點」的 IP 位址（使用連接埠 9300）。在此範例中，您只有一個種子節點：

```json
curl -k -XPUT -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9250/_cluster/settings' -d '
{
  "persistent": {
    "cluster.remote": {
      "opensearch-ccs-cluster1": {
        "seeds": ["172.31.0.3:9300"]
      }
    }
  }
}'
```
所有 cURL 請求也都可以使用 OpenSearch Dashboards Dev Tools 傳送。
{: .tip }
下圖顯示使用 Dev Tools 傳送 cURL 請求的範例。
![用於設定跨叢集搜尋遠端叢集的 OpenSearch Dashboards Dev Tools 請求]({{site.url}}{{site.baseurl}}/images/ccs-devtools.png)

在遠端叢集上，將一份文件編製索引：

```bash
curl -XPUT -k -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://localhost:9200/books/_doc/1' -d '{"Dracula": "Bram Stoker"}'
```

此時，跨叢集搜尋已可運作。您可以使用 `admin` 使用者進行測試：

```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://localhost:9250/opensearch-ccs-cluster1:books/_search?pretty'
{
  ...
  "hits": [{
    "_index": "opensearch-ccs-cluster1:books",
    "_id": "1",
    "_score": 1.0,
    "_source": {
      "Dracula": "Bram Stoker"
    }
  }]
}
```

若要繼續測試，請在兩個叢集上建立一位新使用者：

```bash
curl -XPUT -k -u 'admin:<custom-admin-password>' 'https://localhost:9200/_plugins/_security/api/internalusers/booksuser' -H 'Content-Type: application/json' -d '{"password":"password"}'
curl -XPUT -k -u 'admin:<custom-admin-password>' 'https://localhost:9250/_plugins/_security/api/internalusers/booksuser' -H 'Content-Type: application/json' -d '{"password":"password"}'
```

接著使用 `booksuser` 執行與先前相同的搜尋：

```json
curl -XGET -k -u booksuser:password 'https://localhost:9250/opensearch-ccs-cluster1:books/_search?pretty'
{
  "error" : {
    "root_cause" : [
      {
        "type" : "security_exception",
        "reason" : "no permissions for [indices:admin/shards/search_shards, indices:data/read/search] and User [name=booksuser, roles=[], requestedTenant=null]"
      }
    ],
    "type" : "security_exception",
    "reason" : "no permissions for [indices:admin/shards/search_shards, indices:data/read/search] and User [name=booksuser, roles=[], requestedTenant=null]"
  },
  "status" : 403
}
```

請留意權限錯誤。在遠端叢集上，建立具有適當權限的角色，並將 `booksuser` 對應至該角色：

```bash
curl -XPUT -k -u 'admin:<custom-admin-password>' -H 'Content-Type: application/json' 'https://localhost:9200/_plugins/_security/api/roles/booksrole' -d '{"index_permissions":[{"index_patterns":["books"],"allowed_actions":["indices:admin/shards/search_shards","indices:data/read/search"]}]}'
curl -XPUT -k -u 'admin:<custom-admin-password>' -H 'Content-Type: application/json' 'https://localhost:9200/_plugins/_security/api/rolesmapping/booksrole' -d '{"users" : ["booksuser"]}'
```

兩個叢集都必須具有使用者角色，但只有遠端叢集需要同時具有角色與對應。在此範例中，協調叢集負責驗證（也就是「此請求是否包含有效的使用者憑證？」），而遠端叢集負責授權（也就是「此使用者是否可以存取此資料？」）。
{: .tip }

最後，再次執行搜尋：

```bash
curl -XGET -k -u booksuser:password 'https://localhost:9250/opensearch-ccs-cluster1:books/_search?pretty'
{
  ...
  "hits": [{
    "_index": "opensearch-ccs-cluster1:books",
    "_id": "1",
    "_score": 1.0,
    "_source": {
      "Dracula": "Bram Stoker"
    }
  }]
}
```

## 裸機/虛擬機器設定範例

如果您在裸機伺服器上執行 OpenSearch 或使用虛擬機器，可以執行相同的命令，並指定 OpenSearch 叢集的 IP (或網域)。
例如，若要為跨叢集搜尋設定遠端叢集，請找出遠端節點的 IP 或遠端叢集的網域，然後執行以下命令：

```json
curl -k -XPUT -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://opensearch-domain-1:9200/_cluster/settings' -d '
{
  "persistent": {
    "cluster.remote": {
      "opensearch-ccs-cluster2": {
        "seeds": ["opensearch-domain-2:9300"]
      }
    }
  }
}'
```
只需指向遠端叢集中其中一個節點的 IP 即可，因為在節點探索過程中會查詢叢集中的所有節點。
{: .tip }

現在您可以跨兩個叢集執行查詢：

```bash
curl -XGET -k -u 'admin:<custom-admin-password>' 'https://opensearch-domain-1:9200/opensearch-ccs-cluster2:books/_search?pretty'
{
  ...
  "hits": [{
    "_index": "opensearch-ccs-cluster2:books",
    "_id": "1",
    "_score": 1.0,
    "_source": {
      "Dracula": "Bram Stoker"
    }
  }]
}
```

## Kubernetes/Helm 設定範例
如果您使用 Kubernetes 叢集部署 OpenSearch，則需要使用 `LoadBalancer` 或 `Ingress` 來設定遠端叢集。以下 [Helm]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/) 範例所建立的 Kubernetes 服務屬於 `ClusterIP` 類型，只能從叢集內部存取；因此，您必須使用可從外部存取的端點：

```bash
curl -k -XPUT -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://opensearch-domain-1:9200/_cluster/settings' -d '
{
  "persistent": {
    "cluster.remote": {
      "opensearch-ccs-cluster2": {
        "seeds": ["ingress:9300"]
      }
    }
  }
}'
```

## Proxy 設定

您可以在位於 proxy 後方的叢集上設定跨叢集搜尋。設定反向 proxy 的方式有很多種，也有各種 proxy 可供選擇。以下範例示範未啟用 TLS 終止的基本 NGINX 反向 proxy 組態，不過仍有許多 proxy 與反向 proxy 可供選擇。若要讓此範例運作，OpenSearch 必須同時啟用傳輸層與 HTTP 的 TLS 加密。如需設定 TLS 加密的更多資訊，請參閱 [設定 TLS 憑證]({{site.url}}{{site.baseurl}}/security/configuration/tls/)。

### 必要條件

若要使用 proxy 模式，請符合以下必要條件：

- 確保來源叢集的節點能夠連線至已設定的 `proxy_address`。
- 確保 proxy 能夠將連線路由至遠端叢集的節點。

### Proxy 組態

以下是適用於 HTTP 與傳輸層通訊的基本 NGINX 組態：

```
stream {
    upstream opensearch-transport {
        server <opensearch>:9300;
    }
    upstream opensearch-http {
        server <opensearch>:9200;
    }
    server {
        listen 8300;
        ssl_certificate /.../{{site.opensearch_version}}/config/esnode.pem;
        ssl_certificate_key /.../{{site.opensearch_version}}/config/esnode-key.pem;
        ssl_trusted_certificate /.../{{site.opensearch_version}}/config/root-ca.pem;
        proxy_pass opensearch-transport;
        ssl_preread on;
    }
    server {
        listen 443;
        listen [::]:443;
        ssl_certificate /.../{{site.opensearch_version}}/config/esnode.pem;
        ssl_certificate_key /.../{{site.opensearch_version}}/config/esnode-key.pem;
        ssl_trusted_certificate /.../{{site.opensearch_version}}/config/root-ca.pem;
        proxy_pass opensearch-http;
        ssl_preread on;
    }
}
```

HTTP 與傳輸層通訊的監聽連接埠分別設定為 `443` 與 `8300`。

### OpenSearch 組態

遠端叢集可以設定為指向 `proxy`，方法是使用以下命令：

```bash
curl -k -XPUT -H 'Content-Type: application/json' -u 'admin:<custom-admin-password>' 'https://opensearch:9200/_cluster/settings' -d '
{
  "persistent": {
    "cluster.remote": {
      "opensearch-remote-cluster": {
        "mode": "proxy",
        "proxy_address": "<remote-cluster-proxy>:8300"
      }
    }
  }
}'
```

請留意 [Proxy 組態]({{site.url}}{{site.baseurl}}/search-plugins/cross-cluster-search/#proxy-configuration) 章節中先前設定的連接埠 `8300`。
