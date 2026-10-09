---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立與還原快照"
parent: Snapshots
nav_order: 10
has_toc: false
has_children: false
grand_parent: Availability and recovery
redirect_from: 
  - /opensearch/snapshots/snapshot-restore/
  - /upgrade-to/snapshot-migrate/
  - /opensearch/snapshot-restore/
  - /availability-and-recovery/snapshots/snapshot-restore/
---

# 建立與還原快照

快照並非瞬間完成。它們需要時間才能完成，且不代表叢集的完美時間點檢視。快照進行期間，您仍可將文件編製索引並傳送其他請求至叢集，但新文件及現有文件的更新通常不會包含在快照中。快照包含 OpenSearch 開始建立快照時各主要分片的狀態。視您的快照執行緒集區大小而定，不同分片可能會在略微不同的時間點納入快照。

OpenSearch 快照是增量式的，這表示它們只儲存自上次成功快照以來已變更的資料。頻繁與不頻繁快照之間的磁碟使用量差異通常很小。

換句話說，每小時建立一次快照持續一週（總共 168 個快照）所使用的磁碟空間，可能不會比在週末建立單一快照多太多。此外，您越頻繁建立快照，完成所需的時間就越短。有些 OpenSearch 使用者甚至每 30 分鐘就建立一次快照。

如果您需要刪除快照，請務必使用 OpenSearch API，而不要瀏覽至儲存位置並清除檔案。來自叢集的增量快照通常會共用大量相同的資料；當您使用 API 時，OpenSearch 只會移除沒有其他快照正在使用的資料。
{: .tip }

---

<details markdown="block">
  <summary>
    目錄
  </summary>
  {: .text-delta }
- TOC
{:toc}
</details>

---

## 註冊儲存庫

在您建立快照之前，必須先「註冊」快照儲存庫。快照儲存庫只是一個儲存位置：共用檔案系統、Amazon Simple Storage Service (Amazon S3)、Hadoop Distributed File System (HDFS) 或 Azure Storage。

### 節點層級儲存庫設定

下列節點層級設定會在其各自類型的所有儲存庫之間全域控制儲存庫行為。這些設定是在 `opensearch.yml` 中設定，且需要重新啟動叢集才能修改。

#### 檔案系統儲存庫設定

- `repositories.fs.chunk_size`（靜態，單位：位元組）：設定檔案系統儲存庫在儲存大型 blob 時的預設區塊大小。此設定決定儲存期間大型 blob 檔案如何分割成較小的區塊。較大的區塊大小可改善循序存取的效能，但可能增加記憶體使用量及網路傳輸額外負荷。當儲存庫設定中未明確指定區塊大小時，此設定可作為後備。預設為無限制（不分割區塊）。最小值為 `5` 位元組。

#### URL 儲存庫設定

- `repositories.url.allowed_urls`（靜態，清單）：指定允許用於 URL 儲存庫存取的 URL 模式清單。此安全性設定會限制建立 URL 儲存庫時可使用的 URL，防止存取未經授權或內部網路資源。URL 模式支援萬用字元（例如 `http://snapshot.example.com/*`）。當為空（預設）時，除非已設定 path.repo，否則不允許任何 URL 儲存庫。此設定有助於防止伺服器端請求偽造 (SSRF) 攻擊。預設為 `[]`（空清單）。

- `repositories.url.supported_protocols`（靜態，清單）：定義 URL 儲存庫支援哪些 URL 通訊協定。此設定控制存取 URL 儲存庫時可使用哪些通訊協定配置（例如 HTTP、HTTPS 或 FTP）。限制支援的通訊協定有助於提升安全性，防止透過可能不安全或非預期的通訊協定進行存取。預設為 `["http", "https", "ftp", "file", "jar"]`。


### 共用檔案系統

1. 若要使用共用檔案系統作為快照儲存庫，請將其新增至 `opensearch.yml`：

   ```yml
   path.repo: ["/mnt/snapshots"]
   ```

   在 RPM 和 Debian 安裝中，您接著可以掛載檔案系統。如果您使用 Docker 安裝，請在啟動叢集之前，將檔案系統新增至 `docker-compose.yml` 中的每個節點：

   ```yml
   volumes:
     - /Users/jdoe/snapshots:/mnt/snapshots
   ```

1. 然後使用 REST API 註冊儲存庫：

   ```json
   PUT /_snapshot/my-fs-repository
   {
     "type": "fs",
     "settings": {
       "location": "/mnt/snapshots"
     }
   }
   ```
  {% include copy-curl.html %}

您很可能不需要指定任何參數，除了 `location` 之外。如需允許的請求參數，請參閱[註冊或更新快照儲存庫 API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/)。

### Amazon S3

1. 若要使用 Amazon S3 儲存貯體作為快照儲存庫，請在所有節點上安裝 `repository-s3` 外掛程式：

   ```bash
   sudo ./bin/opensearch-plugin install repository-s3
   ```

   如果您使用 Docker 安裝，請參閱[使用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#working-with-plugins)。您的 `Dockerfile` 應類似於下列內容：

   ```
   FROM opensearchproject/opensearch:{{site.opensearch_version}}

   ENV AWS_ACCESS_KEY_ID <access-key>
   ENV AWS_SECRET_ACCESS_KEY <secret-key>

   # Optional
   ENV AWS_SESSION_TOKEN <optional-session-token>

   RUN /usr/share/opensearch/bin/opensearch-plugin install --batch repository-s3
   RUN /usr/share/opensearch/bin/opensearch-keystore create

   RUN echo $AWS_ACCESS_KEY_ID | /usr/share/opensearch/bin/opensearch-keystore add --stdin s3.client.default.access_key
   RUN echo $AWS_SECRET_ACCESS_KEY | /usr/share/opensearch/bin/opensearch-keystore add --stdin s3.client.default.secret_key

   # Optional
   RUN echo $AWS_SESSION_TOKEN | /usr/share/opensearch/bin/opensearch-keystore add --stdin s3.client.default.session_token
   ```

   Docker 叢集啟動後，請跳至步驟 7。

   如果您使用 [AWS IAM 執行個體設定檔](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) 來允許 AWS EC2 執行個體上的 OpenSearch 節點在授予 AWS S3 儲存貯體存取權時繼承政策角色，請跳至步驟 8。

1. 將您的 AWS 存取金鑰與私密金鑰新增至 OpenSearch 金鑰儲存庫：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.access_key
   sudo ./bin/opensearch-keystore add s3.client.default.secret_key
   ```

1. （選用）如果您使用自訂 S3 端點（例如 MinIO），請停用 Amazon EC2 中繼資料連線：

   ```bash
   export AWS_EC2_METADATA_DISABLED=true
   ```

   如果您使用 Helm 安裝 OpenSearch，請在您的 values 檔案中更新下列設定：

   ```yml
   extraEnvs:
     - name: AWS_EC2_METADATA_DISABLED
       value: "true"
   ```

1. （選用）如果您使用臨時憑證，請新增您的工作階段權杖：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.session_token
   ```

1. （選用）如果您透過代理伺服器連線至網際網路，請新增那些憑證：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.proxy.username
   sudo ./bin/opensearch-keystore add s3.client.default.proxy.password
   ```

1. （選用）將其他設定新增至 `opensearch.yml`：

   ```yml
   s3.client.default.endpoint: s3.amazonaws.com # S3 has alternate endpoints, but you probably don't need to change this value.
   s3.client.default.max_retries: 3 # number of retries if a request fails
   s3.client.default.path_style_access: false # whether to use the deprecated path-style bucket URLs.
   # You probably don't need to change this value, but for more information, see https://docs.aws.amazon.com/AmazonS3/latest/dev/VirtualHosting.html#path-style-access.
   s3.client.default.protocol: https # http or https
   s3.client.default.proxy.host: my-proxy-host # the hostname for your proxy server
   s3.client.default.proxy.port: 8080 # port for your proxy server
   s3.client.default.read_timeout: 50s # the S3 connection timeout
   s3.client.default.use_throttle_retries: true # whether the client should wait a progressively longer amount of time (exponential backoff) between each successive retry
   s3.client.default.region: us-east-2 # AWS region to use. For non-AWS S3 storage, this value is required but has no effect.
   ```

1. （選用）如果您不想使用 AWS 存取金鑰與私密金鑰，您可以設定 S3 外掛程式，讓服務帳戶使用 AWS Identity and Access Management (IAM) 角色：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.role_arn
   sudo ./bin/opensearch-keystore add s3.client.default.role_session_name
   ```

   如果您不想設定 AWS 存取金鑰與私密金鑰，請修改下列 `opensearch.yml` 設定。請確定該檔案可由 `repository-s3` 外掛程式存取：
   
   ```yml
   s3.client.default.identity_token_file: /usr/share/opensearch/plugins/repository-s3/token
   ```

   如果無法複製，您可以在 `${OPENSEARCH_PATH_CONFIG}` 資料夾中建立指向 Web 身分權杖檔案的符號連結：

   ```
   ln -s $AWS_WEB_IDENTITY_TOKEN_FILE "${OPENSEARCH_PATH_CONFIG}/aws-web-identity-token-file"
   ```

   您可以在下列 `opensearch.yml` 設定中參照 Web 身分權杖檔案，方法是指定相對於 `${OPENSEARCH_PATH_CONFIG}` 解析的相對路徑：

   ```yaml
   s3.client.default.identity_token_file: aws-web-identity-token-file
   ```

   IAM 角色需要至少一個上述設定。其他設定將取自環境變數（若有）：`AWS_ROLE_ARN`、`AWS_WEB_IDENTITY_TOKEN_FILE`、`AWS_ROLE_SESSION_NAME`。

1. 如果您變更了 `opensearch.yml`，則必須重新啟動叢集中的每個節點。否則，您只需要重新載入安全叢集設定：

   ```
   POST /_nodes/reload_secure_settings
   ```
  {% include copy-curl.html %}

1. 如果您還沒有 S3 儲存貯體，請建立一個。若要建立快照，您需要存取該儲存貯體的權限。下列 IAM 政策是這些權限的範例：

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Action": [
           "s3:GetBucketLocation",
           "s3:ListBucket",
           "s3:ListBucketMultipartUploads",
           "s3:ListBucketVersions"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:s3:::your-bucket"
         ]
       },
       {
         "Action": [
           "s3:AbortMultipartUpload",
           "s3:DeleteObject",
           "s3:GetObject",
           "s3:ListMultipartUploadParts",
           "s3:PutObject"
         ],
         "Effect": "Allow",
         "Resource": [
           "arn:aws:s3:::your-bucket/*"
         ]
       }
     ]
   }
   ```

1. 使用 REST API 註冊儲存庫：

   ```json
   PUT /_snapshot/my-s3-repository
   {
     "type": "s3",
     "settings": {
       "bucket": "my-s3-bucket",
       "base_path": "my/snapshot/directory"
     }
   }
   ```
   {% include copy-curl.html %}

您很可能不需要指定任何參數，除了 `bucket` 和 `base_path` 之外。如需允許的請求參數，請參閱[註冊或更新快照儲存庫 API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/)。

### HDFS

若要使用 Hadoop Distributed File System (HDFS) 作為快照儲存庫，請依照下列步驟操作：

1. 為快照建立一個 HDFS 目錄（例如 `/opensearch/repositories/searchable_snapshots`），並確保 OpenSearch 使用者對該目錄具有讀取與寫入權限。

1. 在所有節點上安裝 `repository-hdfs` 外掛程式：

   ```bash
   sudo ./bin/opensearch-plugin install repository-hdfs
   ```

   如果您使用的是 Docker 安裝，請參閱[使用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#working-with-plugins)。您的 `Dockerfile` 應類似如下：

   ```
   FROM opensearchproject/opensearch:{{site.opensearch_version}}

   RUN /usr/share/opensearch/bin/opensearch-plugin install --batch repository-hdfs
   ```

1. （選用）如果您的 HDFS 叢集使用 Kerberos，您可能需要將 keytab 檔案分發到所有節點，並確保 OpenSearch 使用者具有讀取權限。

1. 重新啟動 OpenSearch 叢集中的所有節點。

1. 使用 OpenSearch Snapshot API 註冊儲存庫：

    不使用 HDFS 驗證：

    ```json
    PUT _snapshot/searchable_snapshots
    {
      "type": "hdfs",
      "settings": {
        "uri": "hdfs://namenode:8020/",
        "path": "/opensearch/repositories/searchable_snapshots",
        "conf.<key>": "<value>"
      }
    }
    ```
    {% include copy-curl.html %}

    使用 HDFS 驗證：

    ```json
    PUT _snapshot/searchable_snapshots
    {
      "type": "hdfs",
      "settings": {
        "uri": "hdfs://namenode:8020/",
        "path": "/opensearch/repositories/searchable_snapshots",
        "security.principal": "opensearch@YOURREALM",
        "conf.<key>": "<value>"
      }
    }
    ```
    {% include copy-curl.html %}

### 使用 Helm 註冊 Microsoft Azure 儲存體帳戶

請依照下列步驟，為使用 Helm 部署的 OpenSearch 叢集註冊以 Azure 儲存體帳戶為後端的快照儲存庫。

1. 建立 Azure 儲存體帳戶。接著在該儲存體帳戶中建立一個容器。如需更多資訊，請參閱 [Azure Storage 簡介](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction)。

1. 使用 bash 指令碼建立 OpenSearch keystore 檔案。若要建立 bash 指令碼，請將下列範例的內容複製到名為 `create-keystore.sh` 的檔案中：

   ```bash
   #!/bin/bash

   /usr/share/opensearch/bin/opensearch-keystore create
   echo $AZURE_SNAPSHOT_STORAGE_ACCOUNT | /usr/share/opensearch/bin/opensearch-keystore add --stdin azure.client.default.account
   echo $AZURE_SNAPSHOT_STORAGE_ACCOUNT_KEY | /usr/share/opensearch/bin/opensearch-keystore add --stdin azure.client.default.key
   cp /usr/share/opensearch/config/opensearch.keystore /tmp/keystore/opensearch.keystore
   ```

1. 建立 Docker 檔案。此檔案包含您的 keystore、OpenSearch 執行個體以及 Azure 儲存庫的詳細資訊。若要建立此檔案，請複製下列範例並將其儲存為 `Dockerfile`：

   ```docker
   FROM opensearchproject/opensearch:{{site.opensearch_version}}

   RUN /usr/share/opensearch/bin/opensearch-plugin install --batch repository-azure
   COPY --chmod=0775 create-keystore.sh create-keystore.sh
   ```

1. 使用下列 `docker build` 命令，從您的 Dockerfile 建置 OpenSearch 映像：

   ```
   docker build -t opensearch-custom:{{site.opensearch_version}} -f Dockerfile .
   ```

1. 使用下列資訊清單與命令，建立包含 Azure 儲存體帳戶金鑰的 Kubernetes secret：

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: opensearch
   data:
     azure-snapshot-storage-account-key: ### Insert base64 encoded key
   ```

1. 使用下列額外值[透過 Helm 部署 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/)。在 `AZURE_SNAPSHOT_STORAGE_ACCOUNT` 環境變數中指定儲存體帳戶的值：

   ```yaml
   extraInitContainers:
   - name: keystore-generator
     image: opensearch-custom:{{site.opensearch_version}}
     command: ["/bin/bash", "-c"]
     args: ["bash create-keystore.sh"]
     env:
     - name: AZURE_SNAPSHOT_STORAGE_ACCOUNT
       value: ### Insert storage account name
     - name: AZURE_SNAPSHOT_STORAGE_ACCOUNT_KEY
       valueFrom:
         secretKeyRef:
           name: opensearch
           key: azure-snapshot-storage-account-key
     volumeMounts:
     - name: keystore
       mountPath: /tmp/keystore

   extraVolumeMounts:
   - name: keystore
     mountPath: /usr/share/opensearch/config/opensearch.keystore
     subPath: opensearch.keystore
  
   extraVolumes:
   - name: keystore
     emptyDir: {}

   image:
     repository: "opensearch-custom"
     tag: {{site.opensearch_version}}
   ```

1. 使用 Snapshot API 註冊儲存庫。將 `snapshot_container` 替換為您在步驟 1 中指定的名稱，如下列命令所示：
   ```json
   PUT /_snapshot/my-azure-snapshot
   {
     "type": "azure",
     "settings": {
       "client": "default",
       "container": "snapshot_container"
     }
   }
   ```

### 設定 Microsoft Azure Blob Storage

若要使用 Azure Blob Storage 作為快照儲存庫，請依照下列步驟操作：
1. 使用下列命令在所有節點上安裝 `repository-azure` 外掛程式：

   ```bash
   ./bin/opensearch-plugin install repository-azure
   ```

1. 安裝 `repository-azure` 外掛程式後，請在初始化節點之前定義您的 Azure Blob Storage 設定。首先使用下列安全設定定義您的 Azure Storage 帳戶名稱：

   ```bash
   ./bin/opensearch-keystore add azure.client.default.account
   ```

請從下列選項中選擇一種，以設定您的 Azure Blob Storage 驗證憑證。

#### 使用 Azure Blob Storage 帳戶金鑰
   
使用下列設定來指定您的 Azure Storage 帳戶金鑰：
   
```bash 
./bin/opensearch-keystore add azure.client.default.key
```

#### 共用存取簽章
   
使用共用存取簽章 (SAS) 存取 Azure 時，請使用下列設定：
         
```bash
./bin/opensearch-keystore add azure.client.default.sas_token      
```

#### Azure 權杖憑證

您可以在 `opensearch.yml` 中設定權杖憑證驗證流程。此方法不同於需要 SAS 或帳戶金鑰的連接字串驗證。

如果您選擇使用權杖憑證驗證，則必須選擇一種權杖憑證類型。雖然 Azure 提供多種權杖憑證類型，但僅支援[受控識別](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)。

若要使用受控識別，請使用 `managed` 或 `managed_identity` 值，將您的權杖憑證類型新增至 `opensearch.yml`。這表示正在使用受控識別來執行權杖憑證驗證：

```yml
azure.client.default.token_credential_type: "managed_identity"
``` 

使用 Azure 權杖憑證時，請注意下列事項：

- 權杖憑證支援在 `opensearch.yml` 中預設為停用。
- 當設定多個選項時，權杖憑證的優先順序高於 Azure Storage 帳戶金鑰或 SAS。 

## 建立快照

建立快照時，您需要指定兩項資訊：

- 快照儲存庫的名稱
- 快照的名稱

下列快照包含所有索引與叢集狀態：

```json
PUT /_snapshot/my-repository/snapshot-1
```
{% include copy-curl.html %}

您也可以新增請求本文，以包含或排除特定索引，或指定其他設定：

```json
PUT /_snapshot/my-repository/snapshot-2
{
  "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
  "ignore_unavailable": true,
  "include_global_state": false,
  "partial": false
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Create Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/)。

如果您在建立快照後立即請求該快照，可能會看到類似以下的內容：

```json
GET /_snapshot/my-repository/snapshot-2
{
  "snapshots": [{
    "snapshot": "snapshot-2",
    "version": "6.5.4",
    "indices": [
      "opensearch_dashboards_sample_data_ecommerce",
      "my-index",
      "opensearch_dashboards_sample_data_logs",
      "opensearch_dashboards_sample_data_flights"
    ],
    "include_global_state": false,
    "state": "IN_PROGRESS",
    ...
  }]
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Get Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/)。

請注意，快照仍在進行中。如果您想在繼續之前等待快照完成，請在請求中新增 `wait_for_completion` 參數。快照可能需要一段時間才能完成，因此請考慮此選項是否符合您的使用情境：

```
PUT _snapshot/my-repository/snapshot-3?wait_for_completion=true
```
{% include copy-curl.html %}

快照具有下列狀態：

狀態 | 說明
:--- | :---
SUCCESS | 快照已成功儲存所有分片。
`IN_PROGRESS` | 快照目前正在執行中。
PARTIAL | 至少有一個分片儲存失敗。只有在建立快照時將 `partial` 設為 `true` 才會發生。
FAILED | 快照發生錯誤，且未儲存任何資料。
INCOMPATIBLE | 快照與此叢集上執行的 OpenSearch 版本不相容。請參閱[衝突與相容性](#conflicts-and-compatibility)。

如果目前已有快照正在進行中，您就無法建立快照。若要檢查狀態：

```
GET /_snapshot/_status
```
{% include copy-curl.html %}


## 還原快照

還原快照的第一步是擷取現有的快照。若要查看所有快照儲存庫：

```
GET /_snapshot/_all
```
{% include copy-curl.html %}

若要查看儲存庫中的所有快照：

```
GET /_snapshot/my-repository/_all
```
{% include copy-curl.html %}

接著還原快照：

```
POST /_snapshot/my-repository/snapshot-2/_restore
```
{% include copy-curl.html %}

如同建立快照時，您可以新增請求本文，以包含或排除特定索引，或指定其他設定：

```json
POST /_snapshot/my-repository/snapshot-2/_restore
{
  "indices": "opensearch_dashboards*,my-index*",
  "ignore_unavailable": true,
  "include_global_state": false,
  "include_aliases": false,
  "partial": false,
  "rename_pattern": "opensearch_dashboards(.+)",
  "rename_replacement": "restored_opensearch_dashboards$1",
  "index_settings": {
    "index.blocks.read_only": false
  },
  "ignore_index_settings": [
    "index.refresh_interval"
  ]
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Restore Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/restore-snapshot/)。

### 跨遠端後端叢集還原快照

使用遠端後端儲存空間時，OpenSearch 會自動將索引分段與交易記錄備份至遠端儲存庫 (通常是 Amazon S3)。如果您要在**兩者皆使用遠端後端儲存空間**但遠端儲存庫不同的叢集之間還原快照，您必須指定來源叢集的遠端儲存庫。

此程序僅適用於已啟用遠端後端儲存空間的叢集。對於未使用遠端後端儲存空間的標準 OpenSearch 叢集，請使用標準快照還原程序，不需這些額外參數。
{: .note}

下列程序會將快照從叢集 A 還原至叢集 B，其中兩個叢集皆使用遠端後端儲存空間，但使用不同的 Amazon S3 儲存庫。

#### 先決條件

開始之前，請確認您已符合下列先決條件：

- 兩個叢集執行相同的 OpenSearch 版本。
- 您已從來源叢集的遠端儲存庫組態取得 Amazon S3 儲存貯體名稱、基礎路徑、AWS Key Management Service (KMS) 金鑰 Amazon Resource Name (ARN) 及網域 ARN。

#### 步驟

若要將快照從來源叢集還原至目標叢集，請完成下列步驟：

1. 在目標叢集上將來源叢集的快照儲存庫註冊為唯讀：

   ```json
   PUT /_snapshot/source-cluster-snapshots
   {
     "type": "s3",
     "settings": {
       "bucket": "source-snapshot-bucket",
       "base_path": "snapshots",
       "region": "us-east-1",
       "readonly": true
     }
   }
   ```
   {% include copy-curl.html %}

2. 在目標叢集上將來源叢集的遠端分段儲存庫註冊為唯讀：

   ```json
   PUT /_snapshot/source-remote-segment-repo
   {
     "type": "s3",
     "settings": {
       "bucket": "source-segment-bucket",
       "base_path": "remote-store/segments",
       "region": "us-east-1",
       "amazon_es_kms_enc_ctx": "domainARN=arn:aws:es:us-east-1:123456789012:domain/source-cluster",
       "amazon_es_kms_key_arn": "arn:aws:kms:us-east-1:123456789012:key/abcd1234-56ef-78gh-90ij-klmnopqrstuv",
       "amazon_es_encryption": "true",
       "remote_store_index_shallow_copy": "true",
       "readonly": true
     }
   }
   ```
   {% include copy-curl.html %}

3. 在目標叢集上將來源叢集的遠端交易記錄儲存庫註冊為唯讀：

   ```json
   PUT /_snapshot/source-remote-translog-repo
   {
     "type": "s3",
     "settings": {
       "bucket": "source-translog-bucket",
       "base_path": "remote-store/translogs",
       "region": "us-east-1",
       "amazon_es_kms_enc_ctx": "domainARN=arn:aws:es:us-east-1:123456789012:domain/source-cluster",
       "amazon_es_kms_key_arn": "arn:aws:kms:us-east-1:123456789012:key/abcd1234-56ef-78gh-90ij-klmnopqrstuv",
       "amazon_es_encryption": "true",
       "remote_store_index_shallow_copy": "true",
       "readonly": true
     }
   }
   ```
   {% include copy-curl.html %}

4. 確認您可以在來源快照儲存庫中列出快照：

   ```json
   GET /_snapshot/source-cluster-snapshots/_all
   ```
   {% include copy-curl.html %}

5. 還原快照，並同時指定來源分段與交易記錄儲存庫：

   ```json
   POST /_snapshot/source-cluster-snapshots/snapshot-1/_restore
   {
     "indices": "my-index",
     "source_remote_store_repository": "source-remote-segment-repo",
     "source_remote_translog_repository": "source-remote-translog-repo"
   }
   ```
   {% include copy-curl.html %}

目標叢集會從快照儲存庫還原索引，並將還原的索引設定為從來源叢集的遠端儲存庫讀取其遠端分段與交易記錄。

如果您在還原期間遇到索引名稱衝突，請使用 `rename_pattern` 與 `rename_replacement` 參數重新命名索引，或在還原前刪除衝突的索引。
{: .tip}

### 衝突與相容性

在還原索引時避免索引命名衝突的方法之一，是使用 `rename_pattern` 與 `rename_replacement` 選項。必要時，您之後可以使用 `_reindex` API 將兩者合併。不過，在從快照還原之前，先刪除造成衝突的索引可能會更簡單。

同樣地，為了在還原帶有別名的索引時避免別名命名衝突，您可以使用 `rename_alias_pattern` 與 `rename_alias_replacement` 選項。

您可以使用 `_close` API 在從快照還原之前關閉現有索引，但快照中的索引必須與現有索引具有相同的分片數量。

我們建議在從快照還原之前，先停止對叢集的寫入請求，這有助於避免以下情境：

1. 您刪除了一個索引，同時也刪除了它的別名。
1. 對這個已刪除別名的寫入請求，建立了一個與該別名同名的新索引。
1. 快照中的別名因為與新索引命名衝突而無法還原。

快照僅向前相容一個主要版本。由較舊的 OpenSearch 版本所建立的快照，即使在版本升級之後，仍可繼續由原本建立快照的 OpenSearch 版本還原。例如，由 OpenSearch 2.11 或更早版本建立的快照，即使在升級至 2.12 之後，仍可繼續由 2.11 叢集還原。

如果您有從較早的主要 OpenSearch 版本建立的舊快照，您可以將它還原到比快照版本新一個主要版本的中繼叢集，重新為所有索引編製索引，建立新的快照，並重複此程序，直到達到您想要的主要版本；但您可能會發現，直接在新叢集中手動為資料編製索引會更容易。

## 安全性考量

如果您使用 Security 外掛程式，快照會有一些額外的限制：

- 若要執行快照與還原作業，使用者必須具備內建的 `manage_snapshots` 角色。
- 您無法還原包含全域狀態或 `.opendistro_security` 索引的快照。

如果快照包含全域狀態，您必須在執行還原時將其排除。如果您的快照也包含 `.opendistro_security` 索引，請將其排除，或列出所有您想包含的其他索引：

```json
POST /_snapshot/my-repository/snapshot-3/_restore
{
  "indices": "-.opendistro_security",
  "include_global_state": false
}
```
{% include copy-curl.html %}

`.opendistro_security` 索引包含敏感性資料，因此我們建議在建立快照時將其排除。如果您確實需要從快照還原該索引，您必須在請求中包含管理員憑證：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem -XPOST 'https://localhost:9200/_snapshot/my-repository/snapshot-3/_restore?pretty'
```
{% include copy.html %}

我們強烈建議不要使用管理員憑證還原 `.opendistro_security`，因為這樣做可能會改變整個叢集的安全性態勢。請參閱 [注意事項]({{site.url}}{{site.baseurl}}/security-plugin/configuration/security-admin/#a-word-of-caution)，以了解備份與還原 Security 外掛程式組態的建議程序。
{: .warning}

## 索引編解碼器考量

關於索引編解碼器的考量，請參閱 [索引編解碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#snapshots)。

## 相關文件

- [快照 API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/)
