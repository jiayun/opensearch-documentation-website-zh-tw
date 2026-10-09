---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遠端後端儲存"
nav_order: 40
has_children: true
parent: Availability and recovery
redirect_from:
  - /opensearch/remote/
  - /tuning-your-cluster/availability-and-recovery/remote/
  - /tuning-your-cluster/availability-and-recovery/remote-store/
---

# 遠端後端儲存

於 2.10 版推出
{: .label .label-purple }


遠端後端儲存為 OpenSearch 使用者提供了一種新的資料遺失防護方式，會自動為所有索引交易建立備份，並將其傳送至遠端儲存空間。為了啟用此功能，也必須啟用分段複寫。如需詳細資訊，請參閱[分段複寫]({{site.url}}{{site.baseurl}}/opensearch/segment-replication/)。

使用遠端後端儲存時，當寫入請求送達主要分片，該請求只會在主要分片上編製索引至 Lucene。接著，對應的 translog 會上傳至遠端儲存區。OpenSearch 不會將寫入請求傳送至副本，而是執行主要分片任期驗證，以確認請求的來源分片仍是主要分片。主要分片任期驗證可確保作用中的主要分片在遭到隔離且未察覺叢集管理員已選出新的主要分片時失效。

在重新整理、排清及合併流程中於主要分片上建立分段後，這些分段會上傳至遠端分段儲存區，而副本分片則會從同一個遠端分段儲存區取得複本。這可避免主要分片必須執行任何寫入操作。

## 設定遠端後端儲存

遠端後端儲存是叢集層級的設定。只能在對叢集進行啟動載入時啟用。啟動載入完成後，就無法啟用或停用遠端後端儲存。這可在叢集層級提供耐久性。

與所設定遠端叢集的通訊會在 Repository 外掛程式介面中進行。Repository 外掛程式的所有現有實作，例如 Azure Blob Storage、Google Cloud Storage 及 Amazon Simple Storage Service (Amazon S3)，都與遠端後端儲存相容。

請確認叢集中所有節點的遠端儲存區設定方式都相同。若非如此，屬性與所選叢集管理員節點不同的節點將會啟動載入失敗。
{: .note}

若要為特定叢集啟用遠端後端儲存，請在 `opensearch.yml` 中提供遠端儲存區儲存庫詳細資料作為節點屬性，如下列範例所示：

```yml
# Repository name
node.attr.remote_store.segment.repository: my-repo-1
node.attr.remote_store.translog.repository: my-repo-2
node.attr.remote_store.state.repository: my-repo-3

# Segment repository settings
node.attr.remote_store.repository.my-repo-1.type: s3
node.attr.remote_store.repository.my-repo-1.settings.bucket: <Bucket Name 1>
node.attr.remote_store.repository.my-repo-1.settings.base_path: <Bucket Base Path 1>
node.attr.remote_store.repository.my-repo-1.settings.region: us-east-1

# Translog repository settings
node.attr.remote_store.repository.my-repo-2.type: s3
node.attr.remote_store.repository.my-repo-2.settings.bucket: <Bucket Name 2>
node.attr.remote_store.repository.my-repo-2.settings.base_path: <Bucket Base Path 2>
node.attr.remote_store.repository.my-repo-2.settings.region: us-east-1

# Remote cluster state repository settings
node.attr.remote_store.repository.my-repo-3.type: s3
node.attr.remote_store.repository.my-repo-3.settings.bucket: <Bucket Name 3>
node.attr.remote_store.repository.my-repo-3.settings.base_path: <Bucket Base Path 3>
node.attr.remote_store.repository.my-repo-3.settings.region: us-east-1

```
{% include copy-curl.html %}

如需設定遠端叢集狀態設定的詳細資訊，請參閱[遠端叢集狀態]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-cluster-state/)。這是叢集中繼資料能夠保存在遠端儲存區的必要條件。

您不需要為分段、translog 及狀態使用三個不同的遠端儲存區儲存庫。這三個儲存區可以共用同一個儲存庫。

在啟動載入過程中，`opensearch.yml` 中列出的遠端後端儲存庫會自動註冊。使用 `remote_store` 設定建立叢集後，在該叢集中建立的所有索引都會開始將資料上傳至所設定的遠端儲存區。

## 相關叢集設定

您可以使用下列[叢集設定]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/cluster-settings/)來調整遠端後端叢集處理各工作負載的方式。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| cluster.default.index.refresh_interval | 時間單位 | 設定未提供 `index.refresh_interval` 設定時的重新整理間隔。當您想要為叢集中的所有索引設定預設重新整理間隔，同時支援 `searchIdle` 設定時，此設定會很有用。您設定的間隔不能低於 `cluster.minimum.index.refresh_interval` 設定。 |
| cluster.minimum.index.refresh_interval | 時間單位 | 設定最小重新整理間隔，並將其套用至叢集中的所有索引。`cluster.default.index.refresh_interval` 設定應高於此設定的值。若在建立索引期間，`index.refresh_interval` 設定低於最小值，則建立索引會失敗。 |
| cluster.remote_store.translog.buffer_interval | 時間單位 | 執行週期性 translog 更新時所使用的 translog 緩衝區間隔預設值。只有在索引設定 `index.remote_store.translog.buffer_interval` 不存在時，此設定才會生效。 |
| cluster.remote_store.translog.max_readers | 整數 | 設定遠端後端索引可開啟的 translog 檔案數上限。這會限制每個分片的 translog 檔案總數。達到此上限後，遠端儲存區會排清 translog 檔案。預設值為 `1000`。最低需求為 `100`。 |

## 從備份還原

若要從遠端備份還原索引，例如在節點故障時，請使用下列其中一個選項：

**僅還原未指派的分片**

```bash
curl -X POST "https://localhost:9200/_remotestore/_restore" -H 'Content-Type: application/json' -d'
{
  "indices": ["my-index-1", "my-index-2"]
}
'
```

**還原指定索引的所有分片**

```bash
curl -X POST "https://localhost:9200/_remotestore/_restore?restore_all_shards=true" -ku admin:<custom-admin-password> -H 'Content-Type: application/json' -d'
{
  "indices": ["my-index"]
}
'
```

若已啟用 Security 外掛程式，使用者必須具備 `cluster:admin/remotestore/restore` 權限。如需設定使用者權限的資訊，請參閱[存取控制](/security-plugin/access-control/index/)。
{: .note}

## 可能的使用案例

您可以使用遠端後端儲存來：

- 還原紅色叢集或索引。
- 若 `index.translog.durability` 設為 `request`，則不論副本數量為何，都能復原至最後一次已確認寫入為止的所有資料。

## 基準測試

The OpenSearch Project 使用 [OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/index/) 工具中提供的多種工作負載選項來執行遠端儲存區。本節摘要說明下列工作負載的基準測試結果：

- [StackOverflow](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/so)
- [HTTP logs](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/http_logs)
- [NYC taxis](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/nyc_taxis)

每個工作負載都針對多種大量編製索引用戶端組態進行測試，以模擬不同程度的請求並行處理。

您的結果可能會因叢集拓撲、硬體、分片數量及合併設定而有所不同。

### 叢集、分片及測試組態

在這些基準測試中，我們使用了下列叢集、分片及測試組態：

* 節點：三個節點，每個節點都使用 data、ingest 及 cluster manager 角色
* 節點執行個體：Amazon EC2 r6g.xlarge
* OpenSearch Benchmark 主機：單一 Amazon EC2 m5.2xlarge 執行個體
* 分片組態：三個分片，一個副本
* 已安裝 `repository-s3` 外掛程式，並使用預設 S3 設定

### StackOverflow

下表列出 `so` 工作負載在遠端 translog 緩衝區間隔為 250 ms 時的基準測試結果。

|	|	| 8 個大量編製索引用戶端 (預設)	| | | 16 個大量編製索引用戶端	| | | 24 個大量編製索引用戶端	| | |
|---	|---	|---	|---	|---	| --- | --- | --- | --- | --- | --- |
|	|	| 文件複寫	| 已啟用遠端	| 百分比差異	| 文件複寫	| 已啟用遠端	| 百分比差異	| 文件複寫	| 已啟用遠端	| 百分比差異	|
|編製索引輸送量	|Mean	|29582.5	| 40667.4	|37.47	|31154.9	|47862.3	|53.63	|31777.2	|51123.2	|60.88	|
|編製索引輸送量	|P50	|28915.4	|40343.4	|39.52	|30406.4	|47472.5	|56.13	|30852.1	|50547.2	|63.84	|
|編製索引延遲	|P90	|1716.34	|1469.5	|-14.38	|3709.77	|2799.82	|-24.53	|5768.68	|3794.13	|-34.23	|

### HTTP logs

下表列出 `http_logs` 工作負載在遠端 translog 緩衝區間隔為 200 ms 時的基準測試結果。

|	|	| 8 個大量編製索引用戶端 (預設)	| | | 16 個大量編製索引用戶端	| | | 24 個大量編製索引用戶端	| | |
|---	|---	|---	|---	|---	| --- | --- | --- | --- | --- | --- |
|	|	| 文件複寫	| 已啟用遠端	|百分比差異	| 文件複寫	| 已啟用遠端	| 百分比差異	|文件複寫	| 已啟用遠端	| 百分比差異	|
|編製索引輸送量	|Mean	|149062	|82198.7	|-44.86	|134696	|148749	|10.43	|133050	|197239	|48.24	|
|編製索引輸送量	|P50	|148123	|81656.1	|-44.87	|133591	|148859	|11.43	|132872	|197455	|48.61	|
|編製索引延遲	|P90	|327.011	|610.036	|86.55	|751.705	|669.073	|-10.99	|1145.19	|817.185	|-28.64	|

### NYC taxis

下表列出 `http_logs` 工作負載在遠端 translog 緩衝區間隔為 250 ms 時的基準測試結果。

|	|	| 8 個大量編製索引用戶端 (預設)	| | | 16 個大量編製索引用戶端	| | | 24 個大量編製索引用戶端	| | |
|---	|---	|---	|---	|---	| --- | --- | --- | --- | --- | --- |
|	|	| 文件複寫	| 已啟用遠端	|百分比差異	| 文件複寫	| 已啟用遠端	| 百分比差異	|文件複寫	| 已啟用遠端	| 百分比差異	|
|編製索引輸送量	|Mean	|93383.9	|94186.1	|0.86	|91624.8	|125770	|37.27	|93627.7	|132006	|40.99	|
|編製索引輸送量	|P50	|91645.1	|93906.7	|2.47	|89659.8	|125443	|39.91	|91120.3	|132166	|45.05	|
|編製索引延遲	|P90	|995.217	|1014.01	|1.89	|2236.33	|1750.06	|-21.74	|3353.45	|2472	|-26.28	|

如結果所示，在編製索引延遲大於平均遠端上傳時間的情況下，可獲得一致的效能提升。當您增加大量編製索引用戶端的數量時，啟用遠端的組態可提供高達 60--65% 的編製索引輸送量提升。如需更詳細的結果，請參閱 [Issue #9790](https://github.com/opensearch-project/OpenSearch/issues/9790)。

## 後續步驟

若要追蹤遠端後端儲存的未來增強功能，請參閱 [Issue #10181](https://github.com/opensearch-project/OpenSearch/issues/10181)。

