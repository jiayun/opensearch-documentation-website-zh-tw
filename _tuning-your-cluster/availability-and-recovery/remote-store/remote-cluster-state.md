---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遠端叢集狀態"
nav_order: 5
parent: Remote-backed storage
grand_parent: Availability and recovery
---

# 遠端叢集狀態

於 2.10 版推出
{: .label .label-purple }

遠端後端儲存空間的_遠端叢集狀態_功能可防止因叢集內多數叢集管理員節點永久遺失而導致的任何叢集狀態中繼資料遺失。

_叢集狀態_是一種內部資料結構，包含叢集的中繼資料，其中包括下列項目：
- 索引設定
- 索引對應
- 叢集中分片的作用中副本
- 叢集層級設定
- 資料串流
- 範本

叢集狀態中繼資料由選出的叢集管理員節點管理，對於叢集正常運作至關重要。當叢集永久遺失多數叢集管理員節點時，叢集可能會發生資料遺失，因為現存的叢集管理員節點可能沒有最新的叢集狀態中繼資料。將叢集中所有叢集管理員節點的狀態保存到遠端後端儲存空間，可提供更好的耐久性。

啟用遠端叢集狀態功能後，叢集中繼資料會發布到叢集中設定的遠端儲存庫。
災難復原後啟動新的叢集管理員節點時，這些節點會自動使用遠端儲存庫中儲存的最新中繼資料進行啟動程序。這可提供中繼資料耐久性。

您可以獨立於遠端後端資料儲存空間啟用遠端叢集狀態。
{: .note}

如果您需要資料耐久性，則必須啟用遠端後端資料儲存空間，如[遠端儲存空間文件]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/index/)所述。

## 設定遠端叢集狀態

您可以在啟動叢集時啟用遠端叢集狀態設定。啟用遠端叢集狀態後，您可以更新設定並對所有節點執行輪流重新啟動來停用該功能。

若要為指定的叢集啟用遠端叢集狀態，請將下列叢集層級與儲存庫設定新增至叢集的 `opensearch.yml` 檔案：

```yml
# Enable Remote cluster state cluster setting
cluster.remote_store.state.enabled: true

# Remote cluster state repository settings
node.attr.remote_store.state.repository: my-remote-state-repo
node.attr.remote_store.repository.my-remote-state-repo.type: s3
node.attr.remote_store.repository.my-remote-state-repo.settings.bucket: <Bucket Name 3>
node.attr.remote_store.repository.my-remote-state-repo.settings.base_path: <Bucket Base Path 3>
node.attr.remote_store.repository.my-remote-state-repo.settings.region: <Bucket region>
```
{% include copy-curl.html %}

除了必要的靜態設定外，您也可以根據叢集的需求設定下列動態設定：

設定 | 預設 | 說明
:--- | :--- | :---
`cluster.remote_store.state.index_metadata.upload_timeout` | 20s | 已棄用。請改用 `cluster.remote_store.state.global_metadata.upload_timeout`。
`cluster.remote_store.state.global_metadata.upload_timeout` | 20s | 等待叢集狀態上傳完成的時間長度。
`cluster.remote_store.state.metadata_manifest.upload_timeout` | 20s | 等待資訊清單檔案上傳完成的時間長度。資訊清單檔案包含單一叢集狀態所上傳之每個檔案的詳細資料，包括索引中繼資料檔案與全域中繼資料檔案。
`cluster.remote_store.state.cleanup_interval` | 300s | 非同步遠端狀態清理工作的執行間隔。此工作會刪除任何舊的遠端狀態檔案。


## 限制

遠端叢集狀態功能有下列限制：
- 啟用遠端叢集狀態時，無法執行不安全的啟動程序指令碼。當多數叢集管理員節點遺失且叢集停止運作時，使用者需要更換所有剩餘的叢集管理員節點，並重新設定節點的種子資訊，才能啟動新叢集。

## 遠端叢集狀態發布

叢集管理員節點會處理叢集狀態的更新。接著，它會透過本機傳輸層將更新後的叢集狀態發布給所有追隨者節點。啟用 `remote_store.publication` 功能後，每次狀態更新時，叢集狀態都會備份到遠端儲存空間。追隨者節點接著可以直接從遠端儲存空間擷取狀態，這可減少叢集管理員節點發布的額外負擔。

若要啟用此功能，請在 `opensearch.yml` 中設定下列設定：

```yml
# Enable Remote cluster state publication
cluster.remote_store.publication.enabled: true
```

啟用此設定不會變更發布流程，且追隨者節點在從遠端儲存空間下載更新後的叢集狀態之前，不會將確認傳送回叢集管理員節點。

您必須啟用遠端叢集狀態功能，遠端發布才能運作。若要修改遠端發布行為，可以使用下列路由表儲存庫設定，其中包含遠端叢集狀態中每個索引的分片配置詳細資料：

```yml
# Remote routing table repository settings
node.attr.remote_store.routing_table.repository: my-remote-routing-table-repo
node.attr.remote_store.repository.my-remote-routing-table-repo.type: s3
node.attr.remote_store.repository.my-remote-routing-table-repo.settings.bucket: <Bucket Name 3>
node.attr.remote_store.repository.my-remote-routing-table-repo.settings.region: <Bucket region>
```

您不需要為狀態和路由使用不同的遠端儲存空間儲存庫，因為狀態和路由都可以使用相同的儲存庫設定。

若要設定遠端發布，請使用下列叢集設定。

設定 | 預設 | 說明
:--- |:---| :---
`cluster.remote_store.state.read_timeout` | 20s | 等待追隨者節點上的遠端狀態下載完成的時間長度。
`cluster.remote_store.state.path.prefix` | "" (空字串) | 要新增至 blob 儲存空間中索引中繼資料檔案的固定前置字元。
`cluster.remote_store.index_metadata.path_type` | `HASHED_PREFIX` | 用於在 blob 儲存空間中建立索引中繼資料路徑的路徑類型。有效值為 `FIXED`、`HASHED_PREFIX` 和 `HASHED_INFIX`。
`cluster.remote_store.index_metadata.path_hash_algo` | `FNV_1A_BASE64 ` | 用於在 blob 儲存空間中建構索引中繼資料路徑之前置字元或中置字元的演算法。如果 `cluster.remote_store.index_metadata.path_type` 設定為 `HASHED_PREFIX` 或 `HASHED_INFIX`，則會套用此設定。有效的演算法值為 `FNV_1A_BASE64` 和 `FNV_1A_COMPOSITE_1`。
`cluster.remote_store.routing_table.path.prefix` | "" (空字串) | 要為 blob 儲存空間中索引路由檔案新增的固定前置字元。
  
