---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "淺層快照"
nav_order: 15
parent: Remote-backed storage
grand_parent: Availability and recovery
---

# 淺層快照

淺層複製快照讓您能夠參照整個以遠端儲存空間為後端的儲存庫中的資料，而不必將分段的所有資料儲存在快照儲存庫中。這使得存取分段資料比使用一般快照更快，因為分段資料不會儲存在快照儲存庫中。

## 啟用淺層快照

使用 [Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/create-repository/) 並將 `remote_store_index_shallow_copy` 儲存庫設定設為 `true`，即可啟用淺層快照複製，如下列範例所示：

```bash
PUT /_snapshot/snap_repo
{
        "type": "s3",
        "settings": {
            "bucket": "test-bucket",
            "base_path": "daily-snaps",
            "remote_store_index_shallow_copy": true
        }
    }
```
{% include copy-curl.html %}

啟用後，所有使用 [Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/index/) 的請求對所有快照而言都維持不變。因此，啟用淺層快照設定後請勿停用，因為停用該設定可能會影響資料的耐久性。

## 注意事項

使用淺層複製快照之前，請考慮下列事項：

- 淺層複製快照僅適用於以遠端儲存空間為後端的索引。
- 叢集中的所有節點都必須使用 OpenSearch 2.10 或更新版本，才能利用淺層複製快照。
- 使用淺層複製快照時，目前快照與上一個快照之間的 `incremental` 檔案數量與大小為 `0`。
- 淺層複製快照內不支援可搜尋快照。

## 淺層快照 v2 

從 OpenSearch 2.17 開始，淺層快照功能提供名為 `shallow snapshot v2` 的改良版本，透過引入下列強化功能，旨在讓快照作業更有效率且更具擴充性：

* 確定性的快照作業：淺層快照 v2 讓快照作業更具確定性，確保行為一致且可預測。
* 將叢集狀態更新降至最低：淺層快照 v2 將快照作業期間所需的叢集狀態更新次數降至最低，減少額外負擔並提升效能。
* 擴充性：淺層快照 v2 讓快照作業的規模可獨立於叢集中的分片數量擴充，為大型資料集帶來更好的效能與效率。

淺層快照 v2 必須與淺層複製分開啟用。

### 啟用淺層快照 v2

若要啟用淺層快照 v2，請啟用下列儲存庫設定：

- `remote_store_index_shallow_copy: true`
- `shallow_snapshot_v2: true`

下列範例請求會建立淺層快照 v2 儲存庫：

```bash
PUT /_snapshot/snap_repo
{
"type": "s3",
"settings": {
"bucket": "test-bucket",
"base_path": "daily-snaps",
"remote_store_index_shallow_copy": true,
"shallow_snapshot_v2": true
}
}
```
{% include copy-curl.html %}

### 限制 

淺層快照 v2 有下列限制：

* 淺層快照 v2 僅支援以遠端儲存空間為後端的索引。
* 叢集中的所有節點都必須使用 OpenSearch 2.17 或更新版本，才能利用淺層快照 v2。
