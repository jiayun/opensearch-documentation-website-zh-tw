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

快照並非即時完成。它們需要時間才能完成，且不代表叢集完美的時間點檢視。快照進行中時，您仍然可以為文件編製索引並向叢集傳送其他請求，但新文件與對現有文件的更新通常不會包含在快照中。快照包含 OpenSearch 啟動快照時主要分片當時的狀態。視快照執行緒集區的大小而定，不同分片可能會在稍微不同的時間點被納入快照。

在為分片建立快照之前，OpenSearch 會先[排清]({{site.url}}{{site.baseurl}}/api-reference/index-apis/flush/)該分片，然後複製所產生 Lucene commit 的檔案。因此，分片的快照包含排清之前已編製索引到該分片的所有作業，包括尚未重新整理且尚不可搜尋的文件。

OpenSearch 快照是漸進式的，也就是說它們只儲存自上次成功快照以來變更的資料。頻繁與不頻繁快照之間的磁碟用量差異通常很小。

換句話說，持續一週每小時建立一次快照（總計 168 個快照）所使用的磁碟空間，可能不會比在週末只建立一個快照多多少。此外，建立快照的頻率越高，完成所需的時間就越短。有些 OpenSearch 使用者每 30 分鐘就建立一次快照。

如果您需要刪除快照，請務必使用 OpenSearch API，而不是前往儲存位置並清除檔案。來自叢集的漸進式快照通常共用許多相同的資料；使用 API 時，OpenSearch 只會移除沒有其他快照使用的資料。
{: .tip }

請勿透過複製節點的資料目錄來備份叢集。資料目錄的複本不是一致的備份，從這種複本還原可能會失敗或無聲地遺失資料。快照是備份叢集唯一可靠的方式。
{: .warning }

若要依排程建立快照並自動刪除舊快照，請使用 [Snapshot Management]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-management/)。

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

在建立快照之前，您必須「註冊」快照儲存庫。快照儲存庫只是一個儲存位置：共用檔案系統、Amazon Simple Storage Service (Amazon S3)、Hadoop Distributed File System (HDFS) 或 Azure Storage。

### 節點層級的儲存庫設定

下列節點層級的設定會全域控制其各自類型所有儲存庫的行為。這些設定在 `opensearch.yml` 中組態，且需要重新啟動叢集才能修改。

#### 檔案系統儲存庫設定

- `repositories.fs.chunk_size`（靜態，位元組單位）：設定檔案系統儲存庫在儲存大型 blob 時的預設區塊大小。此設定決定儲存時大型 blob 檔案如何分割成較小的區塊。較大的區塊大小可以改善循序存取的效能，但可能會增加記憶體用量與網路傳輸負擔。當儲存庫設定中未明確指定區塊大小時，此設定可作為後備值。預設為無限制（不分割區塊）。最小值為 `5` 位元組。

#### URL 儲存庫設定

- `repositories.url.allowed_urls`（靜態，清單）：指定允許用於 URL 儲存庫存取的 URL 樣式清單。此安全性設定限制建立 URL 儲存庫時可使用的 URL，防止存取未經授權或內部網路資源。URL 樣式支援萬用字元（例如 `http://snapshot.example.com/*`）。當為空（預設）時，除非設定了 path.repo，否則不允許任何 URL 儲存庫。此設定有助於防止伺服器端請求偽造 (SSRF) 攻擊。預設為 `[]`（空清單）。

- `repositories.url.supported_protocols`（靜態，清單）：定義 URL 儲存庫支援哪些 URL 通訊協定。此設定控制存取 URL 儲存庫時可使用的通訊協定方案（例如 HTTP、HTTPS 或 FTP）。限制支援的通訊協定有助於防止透過可能不安全或非預期的通訊協定進行存取，以增強安全性。預設為 `["http", "https", "ftp", "file", "jar"]`。

### 共用檔案系統

1. 若要使用共用檔案系統作為快照儲存庫，請將它加入 `opensearch.yml`：

   ```yml
   path.repo: ["/mnt/snapshots"]
   ```

   檔案系統必須在所有叢集管理員節點與資料節點上掛載於相同的路徑。在 RPM 與 Debian 安裝上，您接著可以掛載檔案系統。如果您使用 Docker 安裝，請在啟動叢集之前，將檔案系統加入 `docker-compose.yml` 中的每個節點：

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

如果 `location` 是相對路徑，OpenSearch 會根據第一個 `path.repo` 目錄來解析它。例如，使用 `path.repo: ["/mnt/snapshots"]` 時，位置 `my-backups` 會解析為 `/mnt/snapshots/my-backups`。

您很可能不需要指定 `location` 以外的任何參數。如需允許的請求參數，請參閱 [Create or Update Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/)。

### URL 儲存庫

URL 儲存庫提供對儲存在 URL 的快照的唯讀存取，例如另一個叢集寫入的共用檔案系統儲存庫。下列請求為共用檔案系統位置註冊一個 URL 儲存庫。`file:` URL 必須指向 `path.repo` 中列出的位置：

```json
PUT /_snapshot/my-url-repository
{
  "type": "url",
  "settings": {
    "url": "file:/mnt/snapshots"
  }
}
```
{% include copy-curl.html %}

您可以列出並還原 URL 儲存庫中的快照，但無法在其中建立快照。

### Amazon S3

1. 若要使用 Amazon S3 儲存貯體作為快照儲存庫，請在所有節點上安裝 `repository-s3` 外掛程式：

   ```bash
   sudo ./bin/opensearch-plugin install repository-s3
   ```

   如果您使用 Docker 安裝，請參閱[使用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#working-with-plugins)。您的 `Dockerfile` 應類似如下：

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

   Docker 叢集啟動後，跳至步驟 7。

   如果您使用 [AWS IAM 執行個體設定檔](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) 讓 AWS EC2 執行個體上的 OpenSearch 節點在授予 AWS S3 儲存貯體存取權時繼承政策的角色，請跳至步驟 8。

1. 將您的 AWS 存取金鑰與私密金鑰加入 OpenSearch keystore：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.access_key
   sudo ./bin/opensearch-keystore add s3.client.default.secret_key
   ```

1. （選用）如果您使用自訂 S3 端點（例如 MinIO），請停用 Amazon EC2 中繼資料連線：

   ```bash
   export AWS_EC2_METADATA_DISABLED=true
   ```

   如果您使用 Helm 安裝 OpenSearch，請更新 values 檔案中的下列設定：

   ```yml
   extraEnvs:
     - name: AWS_EC2_METADATA_DISABLED
       value: "true"
   ```

1. （選用）如果您使用臨時憑證，請加入您的工作階段權杖：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.session_token
   ```

1. （選用）如果您透過 Proxy 連線到網際網路，請加入那些憑證：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.proxy.username
   sudo ./bin/opensearch-keystore add s3.client.default.proxy.password
   ```

1. （選用）將其他設定加入 `opensearch.yml`：

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

1. （選用）如果您不想使用 AWS 存取金鑰與私密金鑰，可以設定 S3 外掛程式，讓服務帳戶使用 AWS Identity and Access Management (IAM) 角色：

   ```bash
   sudo ./bin/opensearch-keystore add s3.client.default.role_arn
   sudo ./bin/opensearch-keystore add s3.client.default.role_session_name
   ```

   如果您不想設定 AWS 存取金鑰與私密金鑰，請修改下列 `opensearch.yml` 設定。請確保 `repository-s3` 外掛程式可以存取該檔案：
   
   ```yml
   s3.client.default.identity_token_file: /usr/share/opensearch/plugins/repository-s3/token
   ```

   如果無法複製，您可以在 `${OPENSEARCH_PATH_CONFIG}` 資料夾中建立指向網頁身分權杖檔案的符號連結：

   ```
   ln -s $AWS_WEB_IDENTITY_TOKEN_FILE "${OPENSEARCH_PATH_CONFIG}/aws-web-identity-token-file"
   ```

   您可以在下列 `opensearch.yml` 設定中參照網頁身分權杖檔案，方式是指定相對於 `${OPENSEARCH_PATH_CONFIG}` 解析的相對路徑：

   ```yaml
   s3.client.default.identity_token_file: aws-web-identity-token-file
   ```

   IAM 角色至少需要上述其中一項設定。其他設定將取自環境變數（如果可用）：`AWS_ROLE_ARN`、`AWS_WEB_IDENTITY_TOKEN_FILE`、`AWS_ROLE_SESSION_NAME`。

1. 如果您變更了 `opensearch.yml`，必須重新啟動叢集中的每個節點。否則，您只需要重新載入安全叢集設定：

   ```
   POST /_nodes/reload_secure_settings
   ```
  {% include copy-curl.html %}

1. 如果您還沒有 S3 儲存貯體，請先建立一個。若要建立快照，您需要存取該儲存貯體的權限。下列 IAM 政策是這些權限的範例：

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

您很可能不需要指定任何參數，除了 `bucket` 和 `base_path`。關於允許的請求參數，請參閱 [Create or Update Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/)。

### HDFS

若要使用 Hadoop Distributed File System (HDFS) 作為快照儲存庫，請依照下列步驟操作：

1. 為快照建立一個 HDFS 目錄（例如 `/opensearch/repositories/searchable_snapshots`），並確認 OpenSearch 使用者對其具有讀取和寫入權限。

1. 在所有節點上安裝 `repository-hdfs` 外掛程式：

   ```bash
   sudo ./bin/opensearch-plugin install repository-hdfs
   ```

   如果您使用 Docker 安裝，請參閱[使用外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/docker/#working-with-plugins)。您的 `Dockerfile` 應類似於下列內容：

   ```
   FROM opensearchproject/opensearch:{{site.opensearch_version}}

   RUN /usr/share/opensearch/bin/opensearch-plugin install --batch repository-hdfs
   ```

1. （選用）如果您的 HDFS 叢集使用 Kerberos，您可能需要將 keytab 檔案散布到所有節點，並確認 OpenSearch 使用者具有讀取權限。

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

請使用下列步驟，為使用 Helm 部署的 OpenSearch 叢集註冊由 Azure 儲存體帳戶支援的快照儲存庫。

1. 建立 Azure 儲存體帳戶。然後在儲存體帳戶內建立容器。如需詳細資訊，請參閱 [Azure 儲存體簡介](https://learn.microsoft.com/en-us/azure/storage/common/storage-introduction)。

1. 使用 bash 指令碼建立 OpenSearch keystore 檔案。若要建立 bash 指令碼，請將下列範例的內容複製到名為 `create-keystore.sh` 的檔案中：

   ```bash
   #!/bin/bash

   /usr/share/opensearch/bin/opensearch-keystore create
   echo $AZURE_SNAPSHOT_STORAGE_ACCOUNT | /usr/share/opensearch/bin/opensearch-keystore add --stdin azure.client.default.account
   echo $AZURE_SNAPSHOT_STORAGE_ACCOUNT_KEY | /usr/share/opensearch/bin/opensearch-keystore add --stdin azure.client.default.key
   cp /usr/share/opensearch/config/opensearch.keystore /tmp/keystore/opensearch.keystore
   ```

1. 建立 Docker 檔案。此檔案包含您的 keystore、OpenSearch 執行個體和 Azure 儲存庫的詳細資料。若要建立該檔案，請複製下列範例並將其儲存為 `Dockerfile`：

   ```docker
   FROM opensearchproject/opensearch:{{site.opensearch_version}}

   RUN /usr/share/opensearch/bin/opensearch-plugin install --batch repository-azure
   COPY --chmod=0775 create-keystore.sh create-keystore.sh
   ```

1. 使用下列 `docker build` 命令，從您的 Dockerfile 建置 OpenSearch 映像：

   ```
   docker build -t opensearch-custom:{{site.opensearch_version}} -f Dockerfile .
   ```

1. 使用下列 manifest 和命令，建立包含 Azure 儲存體帳戶金鑰的 Kubernetes secret：

   ```yaml
   apiVersion: v1
   kind: Secret
   metadata:
     name: opensearch
   data:
     azure-snapshot-storage-account-key: ### Insert base64 encoded key
   ```

1. [使用 Helm 部署 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/helm/)，並搭配下列額外值。在 `AZURE_SNAPSHOT_STORAGE_ACCOUNT` 環境變數中指定儲存體帳戶的值：

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

1. 使用 Snapshot API 註冊儲存庫。將 `snapshot_container` 取代為您在步驟 1 中指定的名稱，如下列命令所示：
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
1. 使用下列命令，在所有節點上安裝 `repository-azure` 外掛程式：

   ```bash
   ./bin/opensearch-plugin install repository-azure
   ```

1. 安裝 `repository-azure` 外掛程式後，請在初始化節點之前定義您的 Azure Blob Storage 設定。首先使用下列安全設定定義您的 Azure 儲存體帳戶名稱：

   ```bash
   ./bin/opensearch-keystore add azure.client.default.account
   ```

請選擇下列其中一個選項，來設定您的 Azure Blob Storage 驗證認證。

#### 使用 Azure Blob Storage 帳戶金鑰
   
使用下列設定來指定您的 Azure 儲存體帳戶金鑰：
   
```bash 
./bin/opensearch-keystore add azure.client.default.key
```

#### 共用存取簽章
   
使用共用存取簽章 (SAS) 存取 Azure 時，請使用下列設定：
         
```bash
./bin/opensearch-keystore add azure.client.default.sas_token      
```

#### Azure 權杖憑證 

您可以在 `opensearch.yml` 中設定權杖憑證驗證流程。此方法與連接字串驗證不同，連接字串驗證需要 SAS 或帳戶金鑰。

如果您選擇使用權杖憑證驗證，則必須選擇權杖憑證類型。雖然 Azure 提供多種權杖憑證類型，但僅支援[受控識別](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview)。

若要使用受控識別，請使用 `managed` 或 `managed_identity` 值，將您的權杖憑證類型新增至 `opensearch.yml`。這表示正在使用受控識別來執行權杖憑證驗證：

```yml
azure.client.default.token_credential_type: "managed_identity"
``` 

使用 Azure 權杖憑證時，請注意下列事項：

- 權杖憑證支援在 `opensearch.yml` 中預設為停用。
- 當設定多個選項時，權杖憑證優先於 Azure 儲存體帳戶金鑰或 SAS。 

## 在叢集之間共用儲存庫

您可以在多個叢集上註冊相同的儲存庫，例如，將快照從生產叢集還原至測試叢集。只有一個叢集應寫入儲存庫。在其他每個叢集上，註冊儲存庫時將 `readonly` 設定設為 `true`。唯讀儲存庫可以列出及還原快照，但無法建立快照。如果多個叢集寫入相同的儲存庫，儲存庫內容可能會損毀：

```json
PUT /_snapshot/my-fs-repository
{
  "type": "fs",
  "settings": {
    "location": "/mnt/snapshots",
    "readonly": true
  }
}
```
{% include copy-curl.html %}

由於快照格式可能會在主要版本之間變更，我們建議為每個 OpenSearch 主要版本使用個別的儲存庫。

## 維護儲存庫

使用下列 API 來維護快照儲存庫：

- [Verify Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/verify-snapshot-repository/)：檢查所有節點是否都能存取儲存庫。當您註冊儲存庫時，OpenSearch 會驗證儲存庫。若要略過此檢查，請在註冊請求中新增 `?verify=false`，然後稍後使用 `POST /_snapshot/<repository>/_verify` 驗證儲存庫。
- [Cleanup Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/cleanup-snapshot-repository/)：移除任何快照不再參照的資料，例如失敗的快照作業所留下的資料。
- [Delete Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/delete-snapshot-repository/)：從叢集移除儲存庫註冊。儲存庫中的快照不會被刪除。若要再次使用它們，請重新註冊儲存庫。

## 建立快照

建立快照時，您需指定兩項資訊：

- 快照儲存庫的名稱
- 快照的名稱

下列快照包含所有索引和叢集狀態：

```json
PUT /_snapshot/my-repository/snapshot-1
```
{% include copy-curl.html %}

您也可以新增請求本文，以包含或排除特定索引，或指定其他設定。`metadata` 物件會將自訂資訊 (例如由誰建立快照及原因) 與快照一併儲存：

```json
PUT /_snapshot/my-repository/snapshot-2
{
  "indices": "opensearch_dashboards*,my-index*,-my-index-2016",
  "ignore_unavailable": true,
  "include_global_state": false,
  "partial": false,
  "metadata": {
    "taken_by": "ops-team",
    "reason": "Backup before upgrading to 3.9"
  }
}
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Create Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-snapshot/)。

若要在快照名稱中包含日期，請在名稱中使用[日期數學]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#date-math)並進行 URL 編碼。例如，下列請求會建立名為 `nightly-` 後接目前日期的快照，例如 `nightly-2026.10.12`。未編碼的名稱為 `<nightly-{now/d}>`：

```json
PUT /_snapshot/my-repository/%3Cnightly-%7Bnow%2Fd%7D%3E
```
{% include copy-curl.html %}

若要在開始快照後立即檢查，請傳送下列請求：

```json
GET /_snapshot/my-repository/snapshot-2
```
{% include copy-curl.html %}

回應顯示快照仍在進行中：

```json
{
  "snapshots": [{
    "snapshot": "snapshot-2",
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

如需更多資訊，請參閱 [Get Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot/)。

如果您想要等待快照完成後再繼續，請在請求中新增 `wait_for_completion` 參數。快照可能需要一段時間才能完成，因此請考量此選項是否符合您的使用情境：

```json
PUT _snapshot/my-repository/snapshot-3?wait_for_completion=true
```
{% include copy-curl.html %}

快照具有下列狀態：

狀態 | 說明
:--- | :---
SUCCESS | 快照成功儲存所有分片。
`IN_PROGRESS` | 快照目前正在執行中。
PARTIAL | 至少有一個分片無法成功儲存。只有在建立快照時將 `partial` 設為 `true` 才會發生。
FAILED | 快照發生錯誤，且未儲存任何資料。
INCOMPATIBLE | 快照與此叢集上執行的 OpenSearch 版本不相容。請參閱[衝突與相容性](#conflicts-and-compatibility)。

若要檢查所有執行中快照的狀態，請傳送下列請求：

```json
GET /_snapshot/_status
```
{% include copy-curl.html %}

若要檢視特定快照中每個分片的進度，請包含儲存庫和快照名稱。即使快照已完成，此請求仍會傳回詳細資訊：

```json
GET /_snapshot/my-repository/snapshot-2/_status
```
{% include copy-curl.html %}

如需更多資訊，請參閱 [Get Snapshot Status API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-status/)。快照執行期間，Get Snapshot API 的回應可能會很慢，因為它與快照作業使用相同的執行緒集區，因此請使用 Get Snapshot Status API 來監視進度。

當分片被納入快照時，它無法重新配置到其他節點。因此，執行中的快照可能會延遲分片重新平衡及分片配置篩選的效果。
{: .note}

### 全域叢集狀態

當 `include_global_state` 為 `true` (建立快照時的預設值) 時，快照會儲存全域叢集狀態。全域狀態包含下列叢集中繼資料：

- 持續性叢集設定。不包含暫時性叢集設定。
- 索引範本、可組合索引範本及元件範本。
- 資料匯入管線和搜尋管線。
- 已儲存的指令碼。
- 持續性工作。外掛程式會使用持續性工作來執行長時間執行的工作，這些工作必須在節點重新啟動後繼續執行，例如跨叢集複寫工作。

全域狀態不包含快照儲存庫註冊。無論 `include_global_state` 值為何，快照中包含的資料串流都會儲存其資料串流定義。

全域狀態不包含任何索引。`indices` 參數決定快照中包含哪些索引，系統索引和隱藏索引的處理方式與其他任何索引相同。如果您省略 `indices`，快照會包含所有開啟的索引，包括系統索引和隱藏索引。儲存在系統索引中的外掛程式組態 (例如 `.opendistro-ism-config` 索引中的 Index State Management (ISM) 原則) 只有在這些索引包含於快照中時才會備份。

## 還原快照

還原快照的第一步是擷取現有的快照。若要檢視所有快照儲存庫，請傳送以下請求：

```json
GET /_snapshot/_all
```
{% include copy-curl.html %}

若要檢視儲存庫中的所有快照，請傳送以下請求：

```json
GET /_snapshot/my-repository/_all
```
{% include copy-curl.html %}

接著還原快照，請傳送以下請求：

```json
POST /_snapshot/my-repository/snapshot-2/_restore
```
{% include copy-curl.html %}

與建立快照時一樣，您可以加入請求本文，以包含或排除特定索引，或指定其他設定：

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

還原快照時，`include_global_state` 預設為 `false`。若將其設為 `true`，OpenSearch 會還原儲存在快照中的全域叢集狀態，包括持續性叢集設定、可組合與元件索引範本、資料匯入與搜尋管線、儲存的指令碼，以及持續性任務。還原的中繼資料會取代叢集中對應的中繼資料。例如，存在於叢集中但不在快照中的持續性任務會被移除，而快照中的索引範本會覆寫同名的現有範本。暫時性叢集設定與已註冊的快照儲存庫不包含在快照中，因此不會被還原。如需全域狀態所包含之中繼資料的清單，請參閱[全域叢集狀態](#global-cluster-state)。

### 監視還原作業

當索引的主要分片正在還原時，索引健康狀態為 `yellow`，且索引沒有作用中的主要分片。當主要分片還原完成後，OpenSearch 會配置副本分片，並在所有副本配置完成後，索引健康狀態變為 `green`。若要監視還原進度，請使用 [CAT Recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/) 或 [Index Recovery API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/recover/)。從快照還原中的分片，其還原類型為 `snapshot`。


### 在使用遠端儲存後端的叢集之間還原快照

使用遠端儲存後端時，OpenSearch 會自動將索引分段與交易記錄備份到遠端儲存庫（通常是 Amazon S3）。如果您要在**皆使用遠端儲存後端**但遠端儲存庫不同的叢集之間還原快照，必須指定來源叢集的遠端儲存庫。

此程序僅適用於已啟用遠端儲存後端的叢集。對於未使用遠端儲存後端的標準 OpenSearch 叢集，請使用標準快照還原程序，不需這些額外參數。
{: .note}

以下程序將快照從叢集 A 還原到叢集 B，兩個叢集都使用遠端儲存後端，但 Amazon S3 儲存庫不同。

#### 必要條件

開始之前，請確認您已符合以下必要條件：

- 兩個叢集執行相同的 OpenSearch 版本。
- 您已從來源叢集的遠端儲存組態取得 Amazon S3 儲存貯體名稱、基礎路徑、AWS Key Management Service (KMS) 金鑰的 Amazon Resource Name (ARN)，以及網域 ARN。

#### 步驟

若要將快照從來源叢集還原到目標叢集，請完成以下步驟：

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

4. 確認您可以列出來源快照儲存庫中的快照：

   ```json
   GET /_snapshot/source-cluster-snapshots/_all
   ```
   {% include copy-curl.html %}

5. 還原快照，同時指定來源分段與交易記錄儲存庫：

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

如果您在還原時遇到索引名稱衝突，可以使用 `rename_pattern` 與 `rename_replacement` 參數重新命名索引，或在還原前刪除衝突的索引。
{: .tip}

### 將快照還原到不同的叢集

快照並未與建立它的叢集綁定。若要將快照還原到另一個叢集，請在該叢集上將快照儲存庫註冊為唯讀，然後照常還原快照。如需更多資訊，請參閱[在叢集之間共用儲存庫](#sharing-a-repository-between-clusters)。目標叢集的大小或拓撲可以與來源叢集不同。請留意以下考量事項：

- 如果目標叢集較小，請確認它有足夠的儲存空間容納還原的索引。若要降低所需的容量，可以使用 `indices` 參數僅還原部分索引，或使用 `index_settings` 參數減少副本數量，例如 `"index_settings": {"index.number_of_replicas": 0}`。
- 分片配置篩選設定（例如 `index.routing.allocation.require.*`）會隨每個索引一起還原。如果目標叢集中沒有節點符合這些設定，還原的分片將保持未配置狀態。若要配置它們，可以使用 `index_settings` 覆寫這些設定，或使用 `ignore_index_settings` 移除它們。
- 如果快照的持續性叢集設定與目標叢集不相容，還原叢集狀態將會失敗。在此情況下，請將 `include_global_state` 設為 `false`，在不包含叢集狀態的情況下還原快照。

如需還原參數的更多資訊，請參閱 [Restore Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/restore-snapshot/)。

### 衝突與相容性

在還原索引時，避免索引命名衝突的一種方式是使用 `rename_pattern` 和 `rename_replacement` 選項。之後如有需要，您可以使用 `_reindex` API 將兩者合併。不過，在從快照還原之前先刪除造成衝突的索引，可能更為簡單。

同樣地，若要還原含有別名的索引時避免別名命名衝突，您可以使用 `rename_alias_pattern` 和 `rename_alias_replacement` 選項。

您可以使用 `_close` API 在從快照還原之前關閉現有的索引，但快照中的索引必須與現有索引具有相同數量的分片。

我們建議在從快照還原之前，先停止對叢集的寫入請求，這有助於避免以下情況：

1. 您刪除了某個索引，這也會一併刪除其別名。
1. 對現已刪除的別名發出寫入請求，會建立一個與該別名同名的新索引。
1. 快照中的別名因為與新索引發生命名衝突而還原失敗。

相容性取決於建立快照中每個索引的 OpenSearch 版本，而不是建立快照的版本。每個索引都必須由目前的主要版本或前一個主要版本所建立。如果快照中有任何索引不相容，您就無法還原該快照。不支援將快照還原到較舊版本的 OpenSearch。

快照僅向前相容一個主要版本。由較早 OpenSearch 版本建立的快照，即使在版本升級之後，仍可繼續由最初建立該快照的 OpenSearch 版本還原。例如，由 OpenSearch 2.11 或更早版本建立的快照，即使在升級至 2.12 之後，仍可繼續由 2.11 叢集還原。

如果您有從較早主要 OpenSearch 版本取得的舊快照，您可以將其還原到比快照版本新一個主要版本的中間叢集、重新編製所有索引的索引、建立新的快照，並重複此流程，直到達到您想要的主要版本，但您可能會發現手動將資料編製索引到新叢集更為容易。

## 取消快照與還原作業

若要取消進行中的快照，請將其刪除。OpenSearch 會停止快照並移除已寫入儲存庫的資料：

```json
DELETE _snapshot/my-repository/my-snapshot
```
{% include copy-curl.html %}

還原作業會使用標準的分片復原程序，從快照復原每個索引。若要取消進行中的還原，請刪除正在還原的索引。這會刪除已還原到這些索引的所有資料：

```json
DELETE restored-index
```
{% include copy-curl.html %}

若要尋找正在還原的索引，請使用 [CAT Recovery API]({{site.url}}{{site.baseurl}}/api-reference/cat/cat-recovery/) 並搭配 `active_only` 參數。從快照還原的分片，其復原類型為 `snapshot`：

```json
GET _cat/recovery?active_only=true&v&h=index,shard,type,stage,snapshot,bytes_percent
```
{% include copy-curl.html %}

## 叢集封鎖的影響

叢集封鎖（例如由 `cluster.blocks.read_only` 設定所設定的封鎖）會影響會修改叢集中繼資料的快照與還原作業。在唯讀叢集封鎖存在的情況下，下列作業會受到影響：

- 註冊或刪除儲存庫會失敗，因為它會寫入叢集中繼資料。
- 還原快照會失敗，因為它會寫入叢集中繼資料。
- 建立快照會成功，因為它只會讀取叢集中繼資料。
- 列出及刪除已註冊儲存庫中的快照會成功，因為儲存庫內容不屬於叢集中繼資料的一部分。

索引封鎖（例如 `index.blocks.write`）會儲存在索引設定中，並會隨索引一併還原。若要移除已還原的封鎖，請在還原後更新索引設定，或使用 `ignore_index_settings` 參數排除該設定。

## 安全性考量

如果您使用 Security 外掛程式，快照會有一些額外的限制：

- 若要執行快照與還原作業，使用者必須具有內建的 `manage_snapshots` 角色。
- 您無法還原包含全域狀態或 `.opendistro_security` 索引的快照。

如果快照包含全域狀態，您在執行還原時必須將其排除。如果您的快照也包含 `.opendistro_security` 索引，請將其排除，或列出您想包含的所有其他索引：

```json
POST /_snapshot/my-repository/snapshot-3/_restore
{
  "indices": "-.opendistro_security",
  "include_global_state": false
}
```
{% include copy-curl.html %}

`.opendistro_security` 索引包含機敏資料，因此我們建議在建立快照時將其排除。如果您確實需要從快照還原該索引，則必須在請求中包含管理員憑證：

```bash
curl -k --cert ./kirk.pem --key ./kirk-key.pem -XPOST 'https://localhost:9200/_snapshot/my-repository/snapshot-3/_restore?pretty'
```
{% include copy.html %}

我們強烈建議不要使用管理員憑證還原 `.opendistro_security`，因為這麼做可能會改變整個叢集的安全性態勢。請參閱[注意事項]({{site.url}}{{site.baseurl}}/security-plugin/configuration/security-admin/#a-word-of-caution)，了解備份與還原 Security 外掛程式組態的建議程序。
{: .warning}

## 索引編解碼器考量

關於索引編解碼器的考量，請參閱[索引編解碼器]({{site.url}}{{site.baseurl}}/im-plugin/index-codecs/#snapshots)。

## 相關文件

- [快照 API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/)
