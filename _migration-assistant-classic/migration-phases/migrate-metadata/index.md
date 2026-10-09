---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移中繼資料"
nav_order: 5
parent: Migration phases
has_children: true
has_toc: true
permalink: /classic/migration-assistant/migration-phases/migrate-metadata/
---

# 遷移中繼資料

中繼資料遷移包含建立叢集的快照，然後使用 Migration Console 遷移快照中的中繼資料。

此工具透過快照或對來源叢集發出 HTTP 請求，收集來源叢集的資訊。這些快照與 `Reindex-From-Snapshot`（RFS）情境的回填程序完全相容。

收集來源叢集的資訊後，會與目標叢集進行比較。執行遷移時，會在目標叢集上建立尚不存在的中繼資料項目。

## 命令引數

若要找出下列命令的所有有效引數，請使用 `--help` 執行。

```shell
console metadata evaluate --help
```
{% include copy.html %}

系統會根據 Migration Console 的部署選項，預先填入若干命令。若要檢視這些命令，請以詳細輸出模式執行主控台：

```shell
console -v metadata migrate --help
```
{% include copy.html %}

您應該會收到類似下列內容的回應：

```shell
(.venv) bash-5.2# console -v metadata migrate --help
INFO:console_link.cli:Logging set to INFO
.
.
.
INFO:console_link.models.metadata:Migrating metadata with command: /root/metadataMigration/bin/MetadataMigration --otel-collector-endpoint http://otel-collector:4317 migrate --snapshot-name snapshot_2023_01_01 --target-host https://opensearchtarget:9200 --min-replicas 0 --file-system-repo-path /snapshot/test-console --target-username admin --target-password ******** --target-insecure --help
.
.
.
```


## 使用 evaluate 命令

透過掃描來源叢集的內容、套用篩選及修改，會建立包含所有將遷移項目的清單。執行 migrate 命令時，此輸出中未出現的任何項目都不會遷移至目標叢集。這是在修改目標叢集之前進行的安全檢查。

```shell
console metadata evaluate [...]
```
{% include copy.html %}

您應該會收到類似下列內容的回應：

```bash
Starting Metadata Evaluation
Clusters:
   Source:
      Remote Cluster: OpenSearch 1.3.16 ConnectionContext(uri=http://localhost:33039, protocol=HTTP, insecure=false, compressionSupported=false)

   Target:
      Remote Cluster: OpenSearch 2.14.0 ConnectionContext(uri=http://localhost:33037, protocol=HTTP, insecure=false, compressionSupported=false)


Migration Candidates:
   Index Templates:
      simple_index_template

   Component Templates:
      simple_component_template

   Indexes:
      blog_2023, movies_2023

   Aliases:
      alias1, movies-alias


Results:
   0 issue(s) detected
```


## 使用 migrate 命令

migrate 命令會處理與 evaluate 命令相同的資料，並將所有要遷移的項目套用至目標叢集。重複執行多次時，先前已遷移的項目不會重新建立。如果有任何項目需要重新遷移，請先從目標叢集刪除這些項目，再依序重新執行 evaluate 和 migrate 命令，以確保完成所需的變更。

```shell
console metadata migrate [...]
```
{% include copy.html %}

您應該會收到類似下列內容的回應：

```shell
Starting Metadata Migration

Clusters:
   Source:
      Snapshot: OpenSearch 1.3.16 FileSystemRepo(repoRootDir=/tmp/junit10626813752669559861)

   Target:
      Remote Cluster: OpenSearch 2.14.0 ConnectionContext(uri=http://localhost:33042, protocol=HTTP, insecure=false, compressionSupported=false)


Migrated Items:
   Index Templates:
      simple_index_template

   Component Templates:
      simple_component_template

   Indexes:
      blog_2023, movies_2023

   Aliases:
      alias1, movies-alias


Results:
   0 issue(s) detected
```


## 中繼資料驗證程序

繼續進行其他遷移步驟之前，建議您確認叢集的詳細資訊。視您的組態而定，這可能包括檢查分片策略，或匯入測試文件，以確保索引對應已正確定義。

## 疑難排解

請使用這些指示協助排解下列問題。

### 存取詳細記錄檔

中繼資料遷移會建立詳細記錄檔，其中包含用於疑難排解的低階追蹤資訊。每次執行程式時，都會在 Migration Console 上名為 `shared-logs-output` 的共用磁碟區中建立記錄檔。下列命令會列出所有記錄檔，每次執行命令都會產生一個記錄檔。

```shell
ls -al /shared-logs-output/migration-console-default/*/metadata/
```
{% include copy.html %}

若要在主控台中檢查檔案，請使用 `cat`、`tail` 和 `grep` 命令列工具。查看此記錄檔中的警告、錯誤和例外狀況，有助於瞭解失敗的原因，或至少有助於在此專案中建立問題。

```shell
tail /shared-logs-output/migration-console-default/*/metadata/*.log
```
{% include copy.html %}

### 警告與錯誤

當回應中出現 `WARN` 或 `ERROR` 元素時，會附上一則簡短訊息，例如 `WARN - my_index already exists`。您可以在與該警告或錯誤相關的詳細記錄檔中找到更多資訊。

### OpenSearch 以相容模式執行

您可能會遇到無法更新 ES 7.10.2 叢集的錯誤。當 OpenSearch 叢集啟用相容模式時，可能會發生此錯誤。請停用相容模式以繼續，請參閱[啟用相容模式](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/rename.html#rename-upgrade)。


### 重大變更相容性

中繼資料遷移需要將資料從來源版本修改為目標版本的格式，以重新建立項目。有時這些功能已不再受支援，並已從目標版本移除。有時目標版本未提供這些功能，降級時尤其如此。雖然此工具旨在簡化此程序，但其支援範圍並未涵蓋所有情況。若在遷移時遇到相容性問題或缺少重要功能，請[搜尋問題並在現有問題中留言](https://github.com/opensearch-project/opensearch-migrations/issues)，或在找不到相關問題時[建立新問題](https://github.com/opensearch-project/opensearch-migrations/issues/new/choose)。

如需處理特定欄位類型相容性問題的資訊，請參閱：
- [轉換類型對應]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-type-mapping-deprecation/) -- 處理 Elasticsearch 6.x 中已棄用的對應類型。
- [轉換欄位類型]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/) -- 設定自訂欄位類型轉換。
- [將 `flattened` 欄位轉換為 `flat_object` 欄位]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/transform-flattened-flat-object/) -- 自動將 `flattened` 欄位轉換為 `flat_object` 欄位。
- [將 `string` 欄位轉換為 `text` 或 `keyword` 欄位]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/transform-string-text-keyword/) -- 自動將 `string` 欄位轉換為 `text` 或 `keyword` 欄位。
- [將 `dense_vector` 欄位轉換為 `knn_vector` 欄位]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/transform-dense-vector-knn-vector/) -- 自動將 `dense_vector` 欄位轉換為 `knn_vector` 欄位。

#### 對應類型的棄用

Elasticsearch 6.8 中的對應類型功能在 Elasticsearch 7.0 及更新版本中已停止使用，這使得遷移至較新版本的 Elasticsearch 和 OpenSearch 更加複雜，請[瞭解更多](https://www.elastic.co/guide/en/elasticsearch/reference/7.17/removal-of-types.html) ↗。

由於中繼資料遷移支援從 ES 6.8 遷移至最新版本的 OpenSearch，因此會透過移除對應中的類型，並重新整理範本或索引屬性來處理此情境。請注意，截至本文撰寫時，尚不支援多個類型對應，請參閱[追蹤任務](https://opensearch.atlassian.net/browse/MIGRATIONS-1778) ↗。


**包含對應類型 foo 的起始狀態範例（ES 6）：**

```json
{
  "mappings": [
    {
      "foo": {
        "properties": {
          "field1": { "type": "text" },
          "field2": { "type": "keyword" }
        }
      }
    }
  ]
}
```
{% include copy.html %}

**移除 foo 後的最終狀態範例（ES 7）：**

```json
{
  "mappings": {
    "properties": {
      "field1": { "type": "text" },
      "field2": { "type": "keyword" },
    }
  }
}
```
{% include copy.html %}

如需其他技術詳細資訊，請[檢視類型對應清理的原始碼](https://github.com/opensearch-project/opensearch-migrations/blob/main/transformation/transformationPlugins/jsonMessageTransformers/jsonTypeMappingsSanitizationTransformer/src/main/java/org/opensearch/migrations/transform/TypeMappingsSanitizationTransformer.java)。

{% include migration-phase-navigation.html %}
