---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "註冊快照儲存庫"
parent: Snapshot APIs
nav_order: 1
---

# 註冊或更新快照儲存庫 API
**於 1.0 版推出**
{: .label .label-purple }


您可以使用快照 API 註冊新的儲存庫來儲存快照，或更新現有儲存庫的資訊。

快照儲存庫可以是下列類型：

* 檔案系統（`fs`）：如需建立 `fs` 儲存庫的指示，請參閱[註冊共用檔案系統儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#shared-file-system)。

* Amazon Simple Storage Service（Amazon S3）儲存桶（`s3`）：如需建立 `s3` 儲存庫的指示，請參閱[註冊 Amazon S3 儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#amazon-s3)。

* Hadoop Distributed File System（HDFS）（`hdfs`）：如需建立 `hdfs` 儲存庫的指示，請參閱[註冊 HDFS 儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#hdfs)。

如需建立儲存庫的指示，請參閱[註冊儲存庫]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/#register-repository)。

## 端點

```json
POST /_snapshot/{repository}/ 
PUT /_snapshot/{repository}/
```

## 路徑參數

參數 | 資料類型 | 說明
:--- | :--- | :---
`repository` | 字串 | 儲存庫名稱 |

## 請求參數

請求參數取決於儲存庫的類型：
  - `fs`
  - `s3`
  - `hdfs`

### 共用參數

下表列出可同時用於 `fs` 與 `s3` 儲存庫的參數。

請求欄位 | 說明
:--- | :---
`prefix_mode_verification` | 啟用時，會將隨機種子的雜湊值加入儲存庫驗證所用的前綴。對於已啟用遠端儲存的叢集，您可以將 `setting.prefix_mode_verification` 設定加入所提供儲存庫的節點屬性。此欄位適用於新儲存庫與現有儲存庫。選用。
`shard_path_type` | 控制分片層級 blob 的路徑結構。支援的值為 `FIXED`、`HASHED_PREFIX` 與 `HASHED_INFIX`。如需各個值的詳細資訊，請參閱 [shard_path_type 值](#shard_path_type-values)。預設為 `HASHED_PREFIX`。選用。

<!-- vale off -->
#### shard_path_type 值
<!-- vale on -->

`shard_path_type` 設定支援下列值：

- `FIXED`：以現有的階層方式保留路徑結構，例如 `<ROOT>/<BASE_PATH>/indices/<index-id>/0/<SHARD_BLOBS>`。
- `HASHED_PREFIX`：針對每個唯一的分片 ID，在路徑開頭加上雜湊前綴，例如 `<ROOT>/<HASH-OF-INDEX-ID-AND-SHARD-ID>/<BASE_PATH>/indices/<index-id>/0/<SHARD_BLOBS>`。
- `HASHED_INFIX`：針對每個唯一的分片 ID，在基底路徑後附加雜湊前綴，例如 `<ROOT>/<BASE-PATH>/<HASH-OF-INDEX-ID-AND-SHARD-ID>/indices/<index-id>/0/<SHARD_BLOBS>`。使用的雜湊方法為 `FNV_1A_COMPOSITE_1`，此方法使用 `FNV1a` 雜湊函式，並產生採用自訂編碼的 64 位元雜湊值，可良好地因應大多數遠端儲存選項的規模擴充。`FNV1a` 取最高有效的 6 個位元來建立 URL 安全的 Base64 字元，再取接下來的 14 個位元來建立二進位字串。

<!-- vale off -->
### fs 儲存庫
<!-- vale on -->

請求欄位 | 說明
:--- | :---
`location` | 用於儲存快照的檔案系統目錄，例如從檔案伺服器掛載的目錄或 Samba 共用目錄。所有節點都必須能夠存取。必要。
`chunk_size` | 在快照作業期間將大型檔案分割成區塊（例如 `64mb`、`1gb`），這對雲端儲存服務供應商很重要，但對共用檔案系統的重要性則低得多。預設為 `null`（無限制）。選用。
`compress` | 是否壓縮中繼資料檔案。此設定不影響資料檔案；視您的索引設定而定，資料檔案可能已經壓縮。預設為 `false`。選用。
`max_restore_bytes_per_sec` | 還原快照的最大速率。預設為 `0`（無限制）。還原速率也受 `indices.recovery.max_bytes_per_sec` 限制（預設為 `40mb`）。選用。
`max_snapshot_bytes_per_sec` | 建立快照的最大速率。預設為每秒 40 MB（`40mb`）。選用。
`remote_store_index_shallow_copy` | 決定是否以淺層複製方式擷取遠端儲存索引的快照。預設為 `false`。
`shallow_snapshot_v2` | 決定是否以[淺層複製 v2]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability/#shallow-snapshot-v2) 方式擷取遠端儲存索引的快照。預設為 `false`。
`readonly` | 儲存庫是否為唯讀。從一個叢集（註冊時使用 `"readonly": false`）遷移至另一個叢集（註冊時使用 `"readonly": true`）時很有用。選用。


<!-- vale off -->
### s3 儲存庫
<!-- vale on -->

| 請求欄位                               | 說明                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|:--------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `base_path` | 您要儲存快照的儲存貯體內路徑（例如，`my/snapshot/directory`）。請勿包含 `s3://` 前置詞。選用。若未指定，快照會儲存在 S3 儲存貯體的根目錄。 |
| `bucket` | S3 儲存貯體的名稱，不含 `s3://` 前置詞。必要。 |
| `region` | S3 儲存貯體所在的 AWS 區域。選用。若未提供，會使用 `opensearch.yml` 中的 `s3.client.default.region` 值。 |
| `endpoint` | S3 儲存貯體端點。選用。在 OpenSearch 2.9 及更新版本中，若已設定 `region`，則為必要。例如，對於 `us-west-2`，請使用 `https://s3.us-west-2.amazonaws.com`。若未提供，會使用 `opensearch.yml` 中的 `s3.client.default.endpoint` 值。 |
| `buffer_size` | 超過此門檻時，區塊（大小為 `chunk_size`）應拆分成片段（大小為 `buffer_size`），並使用不同的 API 傳送至 S3。預設為下列兩個值中較小的值：100 MB 或 Java 堆積的 5%。有效值介於 `5mb` 與 `5gb` 之間。我們不建議變更此選項。 |
| `canned_acl` | S3 提供數種[預先定義的 ACL](https://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html#canned-acl)，`repository-s3` 外掛程式可在 S3 中建立物件時，將這些 ACL 新增至物件。預設為 `private`。選用。 |
| `chunk_size` | 在快照作業期間將檔案拆分成區塊（例如，`64mb`、`1gb`），這對雲端儲存空間供應商很重要，但對共用檔案系統的重要性低得多。預設為 `1gb`。選用。 |
| `client` | 指定用戶端設定（例如，`s3.client.default.access_key`）時，您可以使用 `default` 以外的字串（例如，`s3.client.backup-role.access_key`）。若您使用其他名稱，請將此值變更為相符的名稱。預設及建議值為 `default`。選用。 |
| `compress` | 是否壓縮中繼資料檔案。此設定不會影響資料檔案；視您的索引設定而定，資料檔案可能已經過壓縮。預設為 `false`。選用。 |
| `disable_chunked_encoding` | 停用分塊編碼，以相容於部分儲存服務。預設為 `false`。選用。 |
| `max_restore_bytes_per_sec` | 還原快照的最大速率。預設為 `0`（無限制）。還原速率也受 `indices.recovery.max_bytes_per_sec` 限制（預設為 `40mb`）。選用。 |
| `max_snapshot_bytes_per_sec` | 建立快照的最大速率。預設為每秒 40 MB（`40mb`）。選用。 |
| `readonly` | 儲存庫是否為唯讀。從一個叢集（註冊時設為 `"readonly": false`）遷移至另一個叢集（註冊時設為 `"readonly": true`）時很實用。選用。 |
| `remote_store_index_shallow_copy` | 決定是否以淺層複本的形式擷取遠端儲存空間索引的快照。預設為 `false`。
| `s3_async_client_type` | `repository-s3` 外掛程式將資料上傳至此儲存庫時使用的非同步 HTTP 用戶端。有效值為 `crt`（AWS Common Runtime 用戶端）及 `netty`（Netty NIO 用戶端）。如需詳細資訊，請參閱 [s3_async_client_type](#s3_async_client_type)。預設為 `crt`。選用。 |
| `shallow_snapshot_v2` | 決定是否以[淺層複本 v2]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/snapshot-interoperability/#shallow-snapshot-v2) 的形式擷取遠端儲存空間索引的快照。預設為 `false`。
| `storage_class` | 指定快照檔案的 [S3 儲存類別](https://docs.aws.amazon.com/AmazonS3/latest/dev/storage-class-intro.html)。預設為 `standard`。請勿使用 `glacier` 和 `deep_archive` 儲存類別。選用。                                                                                                                                                                                                                  |
| `server_side_encryption_type` | 指定 S3 伺服器端加密類型。支援的值為 `AES256`（[SSE-S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingServerSideEncryption.html)）、`aws:kms`（[SSE-AWS Key Management Service (KMS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html)）及 `bucket_default`（[儲存貯體預設加密](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-encryption.html)）。預設為 `bucket_default`。 |
| `server_side_encryption_kms_key_id` | 指定將加密類型設為 `aws:kms` 以選取 [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) 時要使用的 AWS KMS 金鑰。若將 `server_side_encryption_type` 設為 `aws:kms`，則為必要。                                                                                                                                                                                               |
| `server_side_encryption_bucket_key_enabled` | 指定使用 [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) 時是否應使用 [S3 儲存貯體金鑰](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-key.html)。選用。                                                                                                                                                                                                              |
| `server_side_encryption_encryption_context` | 指定使用 [S3 SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html) 時應使用的任何額外[加密內容](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html#encryption-context)。此設定值必須採用 JSON 物件格式。選用。                                                                                                            |
| `expected_bucket_owner` | 指定預期的 S3 儲存貯體擁有者的 AWS 帳戶 ID。此設定可用於[驗證儲存貯體擁有權](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucket-owner-condition.html)。選用。                                                                                                                                                                                                                              |

`server_side_encryption` 設定已在 OpenSearch 3.1.0 中移除。S3 對所有 S3 儲存貯體套用伺服器端加密，作為基本加密層級。由於無法停用此加密，該儲存庫設定並無作用。如需詳細資訊，請參閱[使用伺服器端加密保護資料](https://docs.aws.amazon.com/AmazonS3/latest/userguide/serv-side-encryption.html)。
{: .note}

<!-- vale off -->
#### s3_async_client_type
<!-- vale on -->

`s3_async_client_type` 僅套用於單一儲存庫，因此請在儲存庫的 `settings` 區塊中設定。`repository-s3` 外掛程式也會將 `s3_async_client_type` 註冊為節點設定，因此在 `opensearch.yml` 中加入此設定時節點仍可成功啟動，且 [Nodes Info API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/nodes-info/) 也會傳回此設定，但外掛程式只會從儲存庫定義中讀取該值。未設定 `s3_async_client_type` 的儲存庫會使用 `crt`，即使 `opensearch.yml` 指定了 `netty` 也是如此。

若節點的平台上無法使用 AWS Common Runtime 原生程式庫，外掛程式會記錄一則警告，並使用 Netty 用戶端。

若要確認儲存庫使用哪個用戶端，請為 `org.opensearch.repositories.s3.S3AsyncService` 記錄器啟用 `DEBUG` 記錄，並尋找 `S3 Http client type` 訊息。

<!-- vale off -->
### hdfs 儲存庫
<!-- vale on -->

| 請求欄位        | 說明                                                                                                 |
|:---------------------|:------------------------------------------------------------------------------------------------------------|
| `uri` | 採用 `hdfs://<HOST>:<PORT>/path/to/backup` 格式的 HDFS URI。必要。 |
| `path` | HDFS 中用於儲存快照的路徑（例如 `/my/snapshot/directory`）。必要。 |
| `security.principal` | 連線至 HDFS 時使用的 Kerberos 主體。選用。 |
| `conf.<key>` | 其他 HDFS 用戶端組態設定（例如 `core-site.xml` 或 `hdfs-site.xml`）。選用。 |



## 範例請求

以下範例示範如何註冊不同類型的儲存庫。

### `fs`

以下範例使用本機目錄 `/mnt/snapshots` 作為 `location`，註冊一個 `fs` 儲存庫：

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

### `s3`


以下請求會在名為 `my-open-search-bucket` 的現有儲存貯體中，註冊名為 `my-opensearch-repo` 的新 S3 儲存庫。根據預設，所有快照都會儲存在 `my/snapshot/directory` 中：

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


以下請求會在名為 `my-open-search-bucket` 的現有儲存貯體中，註冊名為 `my-opensearch-repo` 的新 S3 儲存庫。根據預設，所有快照都會儲存在 `my/snapshot/directory` 中。此外，此儲存庫已設定為使用 [SSE-KMS](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingKMSEncryption.html#encryption-context)，且預期的儲存貯體擁有者 AWS 帳戶 ID 為 `123456789000`。

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
    "expected_bucket_owner": "123456789000",
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
    "expected_bucket_owner": "123456789000",
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.snapshot.create_repository(
  repository = "my-opensearch-repo",
  body = '''
{
  "type": "s3",
  "settings": {
    "bucket": "my-open-search-bucket",
    "base_path": "my/snapshot/directory",
    "server_side_encryption_type": "aws:kms",
    "server_side_encryption_kms_key_id": "arn:aws:kms:us-east-1:123456789000:key/kms-key-id",
    "server_side_encryption_encryption_context": "{\"additional-enc-ctx\": \"sample-context\"}",
    "expected_bucket_owner": "123456789000",
  }
}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### `hdfs`

以下請求使用 HDFS URI `hdfs://namenode:8020` 和 HDFS 檔案系統路徑 `/opensearch/snapshots`，註冊一個新的 HDFS 儲存庫：
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

## 範例回應

成功時，會傳回下列 JSON 物件：

```json
{
  "acknowledged": true
}
```

若要確認儲存庫已註冊，請使用 [取得快照儲存庫]({{site.url}}{{site.baseurl}}/api-reference/snapshots/get-snapshot-repository/) API，並將儲存庫名稱作為 `repository` 路徑參數傳入。
{: .note}

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/repository/put`。
