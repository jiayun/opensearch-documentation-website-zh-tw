---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立或更新快照儲存庫"
parent: Snapshot APIs
nav_order: 10
---

# 建立或更新快照儲存庫 API
**於 1.0 版推出**
{: .label .label-purple }

註冊新的快照儲存庫或更新現有的快照儲存庫。

快照儲存庫可以為下列類型：

* 檔案系統（`fs`）：如需建立 `fs` 儲存庫的詳細資訊，請參閱[註冊儲存庫共用檔案系統]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#shared-file-system)。

* Amazon Simple Storage Service (Amazon S3) 儲存貯體（`s3`）：如需建立 `s3` 儲存庫的詳細資訊，請參閱[註冊儲存庫 Amazon S3]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#amazon-s3)。

* Hadoop Distributed File System (HDFS)（`hdfs`）：如需建立 `hdfs` 儲存庫的詳細資訊，請參閱[註冊 HDFS 儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#hdfs)。

如需建立儲存庫的詳細資訊，請參閱[註冊儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#register-repository)。

若要更新現有的儲存庫，請傳送包含該儲存庫完整定義的請求。新的設定會取代所有現有設定，因此您未包含在請求中的任何設定都會重設為其預設值。

由於快照格式可能會在主要版本之間變更，建議您為每個 OpenSearch 主要版本註冊個別的儲存庫。如需詳細資訊，請參閱[在叢集之間共用儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#sharing-a-repository-between-clusters)。

## 端點

```json
POST /_snapshot/{repository}
PUT /_snapshot/{repository}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | 字串 | 儲存庫名稱。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數都是選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | 時間 | 等待叢集管理員節點回應的時間長度。預設為 `30s`。
`timeout` | 時間 | 等待回應的時間長度。預設為 `30s`。
`verify` | 布林值 | 是否在註冊儲存庫之前，先驗證可從所有叢集管理員與資料節點存取該儲存庫。若為 `false`，OpenSearch 會註冊儲存庫而不進行檢查。若要在稍後驗證儲存庫，請使用[驗證快照儲存庫 API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/verify-snapshot-repository/)。預設為 `true`。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`type` | 字串 | 儲存庫類型。有效值為 `fs`、`s3`、`hdfs`、`azure` 及 `url`。`s3`、`hdfs` 及 `azure` 類型需要對應的儲存庫外掛程式。如需 `azure` 儲存庫的詳細資訊，請參閱 [Microsoft Azure]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#set-up-microsoft-azure-blob-storage)。必要。
`settings` | 物件 | 儲存庫設定。有效設定取決於儲存庫類型，並列於下列各節。必要。

### 一般參數

下表列出可與 `fs` 及 `s3` 儲存庫搭配使用的參數。

請求欄位 | 說明
:--- | :---
`prefix_mode_verification` | 啟用時，會將隨機種子的雜湊值新增至儲存庫驗證的前置字元。對於已啟用遠端儲存的叢集，您可以將 `setting.prefix_mode_verification` 設定新增至所提供儲存庫的節點屬性。此欄位適用於新的與現有的儲存庫。選用。
`shard_path_type` | 控制分片層級 blob 的路徑結構。支援的值為 `FIXED`、`HASHED_PREFIX` 及 `HASHED_INFIX`。如需每個值的詳細資訊，請參閱 [shard_path_type 值](#shard_path_type-values)。預設為 `HASHED_PREFIX`。選用。

<!-- vale off -->
#### shard_path_type 值
<!-- vale on -->

`shard_path_type` 設定支援下列值：

- `FIXED`：以現有的階層方式保留路徑結構，例如 `<ROOT>/<BASE_PATH>/indices/<index-id>/0/<SHARD_BLOBS>`。
- `HASHED_PREFIX`：為每個唯一的分片 ID 在路徑開頭加上雜湊前置字元，例如 `<ROOT>/<HASH-OF-INDEX-ID-AND-SHARD-ID>/<BASE_PATH>/indices/<index-id>/0/<SHARD_BLOBS>`。
- `HASHED_INFIX`：為每個唯一的分片 ID 在基底路徑之後附加雜湊前置字元，例如 `<ROOT>/<BASE-PATH>/<HASH-OF-INDEX-ID-AND-SHARD-ID>/indices/<index-id>/0/<SHARD_BLOBS>`。所使用的雜湊方法為 `FNV_1A_COMPOSITE_1`，其使用 `FNV1a` 雜湊函式並產生自訂編碼的 64 位元雜湊值，可與大多數遠端儲存選項良好搭配。`FNV1a` 取最高有效 6 位元來建立 URL 安全的 Base64 字元，並取接下來 14 位元來建立二進位字串。

<!-- vale off -->
### fs 儲存庫
<!-- vale on -->

下表列出 `fs` 儲存庫的請求欄位。

請求欄位 | 說明
:--- | :---
`location` | 用於快照的檔案系統目錄，例如檔案伺服器或 Samba 共用的掛載目錄。檔案系統必須在所有叢集管理員與資料節點上掛載於相同路徑，且該位置必須列於 `path.repo` 設定中。相對路徑會相對於第一個 `path.repo` 目錄解析。必要。
`chunk_size` | 在快照作業期間將大型檔案分割成區塊（例如 `64mb` 或 `1gb`），這對雲端儲存供應商很重要，對共用檔案系統則較不重要。預設為 `null`（無限制）。選用。
`compress` | 是否壓縮中繼資料檔案。此設定不會影響資料檔案，資料檔案可能已根據您的索引設定進行壓縮。預設為 `false`。選用。
`max_restore_bytes_per_sec` | 每個節點還原快照的最大速率。預設為 `0`（無限制）。還原速率也受 `indices.recovery.max_bytes_per_sec` 限制（預設為 `40mb`）。選用。
`max_snapshot_bytes_per_sec` | 每個節點建立快照的最大速率。預設為每秒 40 MB（`40mb`）。選用。
`remote_store_index_shallow_copy` | 決定是否將遠端儲存索引的快照擷取為淺層複本。預設為 `false`。
`shallow_snapshot_v2` | 決定是否將遠端儲存索引的快照擷取為[淺層複本 v2]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability/#shallow-snapshot-v2)。預設為 `false`。
`readonly` | 儲存庫是否為唯讀。唯讀儲存庫可以列出與還原快照，但無法建立快照。若您在多個叢集上註冊相同的儲存庫，應只有一個叢集寫入該儲存庫，而所有其他叢集應以 `readonly` 設為 `true` 的方式註冊。如需詳細資訊，請參閱[在叢集之間共用儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#sharing-a-repository-between-clusters)。預設為 `false`。選用。

<!-- vale off -->
### s3 儲存庫
<!-- vale on -->

下表列出 `s3` 儲存庫的請求欄位。

| 請求欄位 | 說明 |
| :--- | :--- |
| `base_path` | 儲存快照的儲存貯體內路徑（例如 `my/snapshot/directory`）。請勿包含 `s3://` 前綴。選用。若未指定，快照會儲存在 S3 儲存貯體根目錄。 |
| `bucket` | S3 儲存貯體名稱，不含 `s3://` 前綴。必要。 |
| `region` | S3 儲存貯體所在的 AWS 區域。選用。若缺少此值，則使用 `opensearch.yml` 中 `s3.client.default.region` 的值。 |
| `endpoint` | S3 儲存貯體端點。若未指定，則使用 `opensearch.yml` 中 `s3.client.default.endpoint` 的值。若兩者皆未設定，則從 `region` 決定端點。當您使用 S3 相容的儲存服務或需要特定端點時，請設定此欄位，例如 `us-west-2` 的 `https://s3.us-west-2.amazonaws.com`。選用。 |
| `buffer_size` | 超過此閾值時，區塊（`chunk_size`）會被拆成較小的片段（`buffer_size`），並使用不同的 API 傳送至 S3。預設為兩個值中較小者：100 MB 或 Java 堆積的 5%。有效值介於 `5mb` 與 `5gb` 之間。不建議變更此選項。 |
| `canned_acl` | S3 提供多種[預先定義的 ACL](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl)，`repository-s3` 外掛程式在 S3 中建立物件時可將其加入。預設為 `private`。選用。 |
| `chunk_size` | 在快照作業期間將檔案拆成區塊（例如 `64mb`、`1gb`），這對雲端儲存供應商非常重要，對共用檔案系統則較不重要。預設為 `1gb`。選用。 |
| `client` | 指定用戶端設定時（例如 `s3.client.default.access_key`），您可以使用 `default` 以外的字串（例如 `s3.client.backup-role.access_key`）。若您使用了替代名稱，請將此值變更為相符的名稱。預設值與建議值為 `default`。選用。 |
| `compress` | 是否壓縮中繼資料檔案。此設定不會影響資料檔案；資料檔案可能已依您的索引設定壓縮。預設為 `false`。選用。 |
| `disable_chunked_encoding` | 停用分塊編碼，以與某些儲存服務相容。預設為 `false`。選用。 |
| `max_restore_bytes_per_sec` | 每個節點還原快照的最大速率。預設為 `0`（無限制）。還原速率也受 `indices.recovery.max_bytes_per_sec` 限制（預設為 `40mb`）。選用。 |
| `max_snapshot_bytes_per_sec` | 每個節點建立快照的最大速率。預設為每秒 40 MB（`40mb`）。選用。 |
| `readonly` | 儲存庫是否為唯讀。唯讀儲存庫可以列出與還原快照，但無法建立快照。若您在多個叢集上註冊同一儲存庫，只有一個叢集應寫入該儲存庫，其他所有叢集都應以 `readonly` 設為 `true` 來註冊。如需更多資訊，請參閱[在叢集之間共用儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#sharing-a-repository-between-clusters)。預設為 `false`。選用。 |
| `remote_store_index_shallow_copy` | 決定遠端儲存索引的快照是否以淺層複本擷取。預設為 `false`。
| `s3_async_client_type` | `repository-s3` 外掛程式將資料上傳至此儲存庫時使用的非同步 HTTP 用戶端。有效值為 `crt`（AWS Common Runtime 用戶端）與 `netty`（Netty NIO 用戶端）。如需更多資訊，請參閱 [s3_async_client_type](#s3_async_client_type)。預設為 `crt`。選用。 |
| `shallow_snapshot_v2` | 決定遠端儲存索引的快照是否以[淺層複本 v2]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability/#shallow-snapshot-v2) 擷取。預設為 `false`。
| `storage_class` | 指定快照檔案的 [S3 儲存類別](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html)。預設為 `standard`。請勿使用 `glacier` 與 `deep_archive` 儲存類別。選用。 |
| `server_side_encryption_type` | 指定 S3 伺服器端加密類型。支援的值為 `AES256`（[SSE-S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html)）、`aws:kms`（[SSE-AWS Key Management Service (KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)）與 `bucket_default`（[儲存貯體預設加密](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)）。預設為 `bucket_default`。 |
| `server_side_encryption_kms_key_id` | 指定當透過設定 `aws:kms` 加密類型選取 [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) 時要使用的 AWS KMS 金鑰。若 `aws:kms` 設為 `server_side_encryption_type`，則為必要。 |
| `server_side_encryption_bucket_key_enabled` | 指定使用 [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) 時是否應使用 [S3 Bucket Keys](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)。選用。 |
| `server_side_encryption_encryption_context` | 指定使用 [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) 時應使用的其他[加密內容](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html#encryption-context)。此設定值必須格式化為 JSON 物件。選用。 |
| `expected_bucket_owner` | 指定預期 S3 儲存貯體擁有者的 AWS 帳戶 ID。此設定可用於[驗證儲存貯體擁有權](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-owner-condition.html)。選用。 |

`server_side_encryption` 設定已在 OpenSearch 3.1.0 中移除。S3 會將伺服器端加密套用為所有 S3 儲存貯體的基礎加密層級。由於此加密無法停用，該儲存庫設定已無作用。如需更多資訊，請參閱[使用伺服器端加密保護資料](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html)。
{: .note}

<!-- vale off -->
#### s3_async_client_type
<!-- vale on -->

`s3_async_client_type` 適用於單一儲存庫，因此請在儲存庫的 `settings` 區塊中設定。`repository-s3` 外掛程式也會將 `s3_async_client_type` 註冊為節點設定，因此節點可以在 `opensearch.yml` 中包含此設定而成功啟動，且 [Nodes Info API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/) 會回傳該設定，但外掛程式只會從儲存庫定義讀取該值。未設定 `s3_async_client_type` 的儲存庫會使用 `crt`，即使 `opensearch.yml` 指定為 `netty` 亦然。

若節點的平台上沒有 AWS Common Runtime 原生程式庫，外掛程式會記錄警告並改用 Netty 用戶端。

若要確認儲存庫使用哪個用戶端，請為 `org.opensearch.repositories.s3.S3AsyncService` 記錄器啟用 `DEBUG` 記錄，並尋找 `S3 Http client type` 訊息。

<!-- vale off -->
### hdfs 儲存庫
<!-- vale on -->

下表列出 `hdfs` 儲存庫的請求欄位。

| 請求欄位 | 說明 |
| :--- | :--- |
| `uri` | 採用 `hdfs://<HOST>:<PORT>/` 格式的 HDFS URI。URI 不得包含路徑。請在 `path` 欄位中指定路徑。必要。 |
| `path` | 您要儲存快照的 HDFS 內路徑（例如 `/my/snapshot/directory`）。必要。 |
| `security.principal` | 連線至 HDFS 時要使用的 Kerberos 主體。選用。 |
| `conf.<key>` | 其他 HDFS 用戶端組態設定（例如 `core-site.xml` 或 `hdfs-site.xml`）。選用。 |

<!-- vale off -->
### url 儲存庫
<!-- vale on -->

`url` 儲存庫為唯讀：您可以列出並還原其中的快照，但無法在其中建立快照。使用 `url` 儲存庫可讓叢集以唯讀方式存取另一個叢集寫入共用檔案系統儲存庫的快照。

下表列出 `url` 儲存庫的請求欄位。

請求欄位 | 說明
:--- | :---
`url` | 儲存庫根目錄的 URL。若要提供共用檔案系統儲存庫的唯讀存取權，URL 必須指向該儲存庫的 `location`，而非上層目錄。支援的通訊協定為 `file`、`ftp`、`http`、`https` 及 `jar`。`file` URL 必須指向所有叢集管理員節點與資料節點上 `path.repo` 設定中所列的位置。`ftp`、`http` 或 `https` URL 必須符合 `repositories.url.allowed_urls` 設定中的項目。如需更多資訊，請參閱[節點層級儲存庫設定]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#node-level-repository-settings)。必要。

## 範例請求

以下範例示範如何註冊不同的儲存庫類型。

<!-- vale off -->
### fs
<!-- vale on -->

以下範例使用本機目錄 `/mnt/snapshots` 作為 `location` 來註冊 `fs` 儲存庫：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-fs-repository
body: |
{
  "type": "fs",
  "settings": {
    "location": "/mnt/snapshots"
  }
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-fs-repository
{
  "type": "fs",
  "settings": {
    "location": "/mnt/snapshots"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create_repository(
  repository = "my-fs-repository",
  body =   {
    "type": "fs",
    "settings": {
      "location": "/mnt/snapshots"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<!-- vale off -->
### s3
<!-- vale on -->

以下請求會在名為 `my-open-search-bucket` 的現有儲存貯體中註冊名為 `my-opensearch-repo` 的新 S3 儲存庫。由於請求設定了 `base_path`，快照會儲存在儲存貯體內的 `my/snapshot/directory` 路徑中：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-opensearch-repo
body: |
{
  "type": "s3",
  "settings": {
    "bucket": "my-open-search-bucket",
    "base_path": "my/snapshot/directory"
  }
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-opensearch-repo
{
  "type": "s3",
  "settings": {
    "bucket": "my-open-search-bucket",
    "base_path": "my/snapshot/directory"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create_repository(
  repository = "my-opensearch-repo",
  body =   {
    "type": "s3",
    "settings": {
      "bucket": "my-open-search-bucket",
      "base_path": "my/snapshot/directory"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

以下請求會在名為 `my-open-search-bucket` 的現有儲存貯體中註冊名為 `my-opensearch-repo` 的新 S3 儲存庫。由於請求設定了 `base_path`，快照會儲存在儲存貯體內的 `my/snapshot/directory` 路徑中。此外，此儲存庫已設定為使用 [SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html#encryption-context)，且預期的儲存貯體擁有者 AWS 帳戶 ID 為 `123456789000`：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-opensearch-repo
body: |
{
  "type": "s3",
  "settings": {
    "bucket": "my-open-search-bucket",
    "base_path": "my/snapshot/directory",
    "server_side_encryption_type": "aws:kms",
    "server_side_encryption_kms_key_id": "arn:aws:kms:us-east-1:123456789000:key/kms-key-id",
    "server_side_encryption_encryption_context": "{\"additional-enc-ctx\": \"sample-context\"}",
    "expected_bucket_owner": "123456789000"
  }
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-opensearch-repo
{
  "type": "s3",
  "settings": {
    "bucket": "my-open-search-bucket",
    "base_path": "my/snapshot/directory",
    "server_side_encryption_type": "aws:kms",
    "server_side_encryption_kms_key_id": "arn:aws:kms:us-east-1:123456789000:key/kms-key-id",
    "server_side_encryption_encryption_context": "{\"additional-enc-ctx\": \"sample-context\"}",
    "expected_bucket_owner": "123456789000"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create_repository(
  repository = "my-opensearch-repo",
  body =   {
    "type": "s3",
    "settings": {
      "bucket": "my-open-search-bucket",
      "base_path": "my/snapshot/directory",
      "server_side_encryption_type": "aws:kms",
      "server_side_encryption_kms_key_id": "arn:aws:kms:us-east-1:123456789000:key/kms-key-id",
      "server_side_encryption_encryption_context": "{\"additional-enc-ctx\": \"sample-context\"}",
      "expected_bucket_owner": "123456789000"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<!-- vale off -->
### hdfs
<!-- vale on -->

以下請求會使用 HDFS URI `hdfs://namenode:8020` 與 HDFS 檔案系統路徑 `/opensearch/snapshots` 來註冊新的 HDFS 儲存庫：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-hdfs-repository
body: |
{
  "type": "hdfs",
  "settings": {
    "uri": "hdfs://namenode:8020",
    "path": "/opensearch/snapshots"
  }
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-hdfs-repository
{
  "type": "hdfs",
  "settings": {
    "uri": "hdfs://namenode:8020",
    "path": "/opensearch/snapshots"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create_repository(
  repository = "my-hdfs-repository",
  body =   {
    "type": "hdfs",
    "settings": {
      "uri": "hdfs://namenode:8020",
      "path": "/opensearch/snapshots"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

<!-- vale off -->
### url
<!-- vale on -->

以下請求會為共用檔案系統位置 `/mnt/snapshots` 註冊唯讀的 `url` 儲存庫：

<!-- spec_insert_start
component: example_code
rest: PUT /_snapshot/my-url-repository
body: |
{
  "type": "url",
  "settings": {
    "url": "file:/mnt/snapshots"
  }
}
-->
{% capture step1_rest %}
PUT /_snapshot/my-url-repository
{
  "type": "url",
  "settings": {
    "url": "file:/mnt/snapshots"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create_repository(
  repository = "my-url-repository",
  body =   {
    "type": "url",
    "settings": {
      "url": "file:/mnt/snapshots"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

成功時，會傳回下列 JSON 物件：

```json
{
  "acknowledged": true
}
```

若要驗證儲存庫是否已註冊，請使用 [Get Snapshot Repository API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/)，並將儲存庫名稱作為 `repository` 路徑參數傳入。
{: .note}

## 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/repository/put`。
