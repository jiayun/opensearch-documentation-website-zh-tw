---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "可搜尋快照"
parent: Snapshots
nav_order: 40
grand_parent: Availability and recovery
redirect_from: 
  - /opensearch/snapshots/searchable_snapshot/
---

# 可搜尋快照

可搜尋快照索引會在搜尋時即時依需求從[快照儲存庫]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/#register-repository)讀取資料，而不是在還原時將所有索引資料下載到叢集儲存空間。由於索引資料在儲存庫中仍保持快照格式，可搜尋快照索引本質上是唯讀的。任何寫入可搜尋快照索引的嘗試都會導致錯誤。

可搜尋快照功能採用多種技術，例如在叢集節點中快取常用的資料分段，並從叢集節點中移除最少使用的資料分段，以騰出空間給常用的資料分段。從區塊儲存上的快照下載的資料分段，會與叢集節點的一般索引存放在一起。因此，叢集節點的運算能力會在編製索引、本機搜尋，以及位於低成本物件儲存（例如 Amazon Simple Storage Service (Amazon S3)）上的快照資料分段之間共用。雖然叢集節點資源的使用效率大幅提升，但大量的工作會導致快照搜尋速度較慢、耗時較長。節點的本機儲存空間也會用於快取快照資料。

## 設定節點以使用可搜尋快照

使用可搜尋快照功能的節點必須具備 `warm` 節點角色。在 OpenSearch 2.x 中，這些節點使用 `search` 角色。
{: .important}

若要設定可搜尋快照功能，請在您的 `opensearch.yml` 檔案中建立一個節點，並將節點角色定義為 `warm`。此外，您也可以選擇性地為該節點設定 `cache.size` 屬性。

`warm` 節點會保留儲存空間作為快取，以執行可搜尋快照查詢。對於專屬搜尋節點（即節點僅具有 `warm` 角色），此值預設為可用儲存空間的固定百分比（80%）。在其他情況下，則需要使用 `node.search.cache.size` 設定來設定此值。

參數 | 類型 | 說明
:--- | :--- | :---
`node.search.cache.size` | 字串 | 以絕對位元組大小（例如 `7kb` 或 `6gb`）或總磁碟空間的百分比（例如 `10%`）指定快取大小。如需位元組大小單位的詳細資訊，請參閱[支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)。

## 可搜尋快照索引設定

下列索引層級設定由 OpenSearch 自動為可搜尋快照索引管理。這些設定屬於內部設定，通常不由使用者直接設定，但可以在索引中繼資料中檢視：

| 設定 | 類型 | 說明 |
|---------|------|-------------|
| `index.searchable_snapshot.repository` | 字串 | 指定儲存可搜尋快照的儲存庫。此設定會在建立可搜尋快照索引時自動設定。 |
| `index.searchable_snapshot.snapshot_id.uuid` | 字串 | 建立可搜尋快照索引所依據之快照的 UUID。 |
| `index.searchable_snapshot.snapshot_id.name` | 字串 | 建立可搜尋快照索引所依據之快照的名稱。 |
| `index.searchable_snapshot.index.id` | 字串 | 快照中用於可搜尋快照索引的原始索引 ID。 |.


```yaml
node.name: snapshots-node
node.roles: [ warm ]
node.search.cache.size: 50gb
```

如果您使用 Docker，可以在 `docker-compose.yml` 檔案中加入 `- node.roles=warm` 這一行，以建立具有 `warm` 節點角色的節點：

```yaml
version: '3'
services:
  opensearch-node1:
    image: opensearchproject/opensearch:3.0.0
    container_name: opensearch-node1
    environment:
      - cluster.name=opensearch-cluster
      - node.name=opensearch-node1
      - node.roles=warm
      - node.search.cache.size=50gb
```

- k-NN 索引支援 NMSLIB 與 Faiss 引擎的可搜尋快照。

## 建立可搜尋快照索引

可搜尋快照索引是透過[還原快照 API]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/#restore-snapshots) 指定 `remote_snapshot` 儲存類型來建立。

請求欄位 | 說明
:--- | :---
`storage_type` | `local` 表示所有快照中繼資料與索引資料都會下載到本機儲存空間。<br /><br > `remote_snapshot` 表示快照中繼資料會下載到叢集，但遠端儲存庫仍是索引資料的權威儲存位置。系統會視需要下載並快取資料以服務查詢。若要使用 `remote_snapshot` 類型還原快照，叢集中至少必須有一個節點設定為 `warm` 節點角色。<br /><br > 預設值為 `local`。

#### 範例請求

下列請求將快照 `my-snapshot` 中的索引 `my-index` 還原為可搜尋快照：

````json
POST /_snapshot/my-repository/my-snapshot/_restore
{
  "storage_type": "remote_snapshot",
  "indices": "my-index"
}
````

與所有快照還原請求一樣，您可以包含或排除特定索引，或指定其他快照設定。如需詳細資訊，請參閱[還原快照 API]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore/#restore-snapshots)。


## 列出索引

若要判斷索引是否為可搜尋快照索引，請尋找值為 `remote_snapshot` 的儲存類型：

```
GET /my-index/_settings?pretty
```

```json
{
  "my-index": {
    "settings": {
      "index": {
        "store": {
          "type": "remote_snapshot"
        }
      }
    }
  }
}
```

## 潛在使用案例

以下是可搜尋快照功能的潛在使用案例：

- 能夠將索引從叢集儲存空間卸載，同時保留搜尋這些索引的能力。
- 能夠在低成本的媒體上擁有大量可搜尋的索引。

## 已知限制

以下是可搜尋快照功能的已知限制：

- 從遠端儲存庫存取資料比本機磁碟讀取慢，因此搜尋查詢的延遲會較高。
- 許多遠端物件儲存會按請求收取擷取費用，因此使用者應密切監控所產生的任何成本。
- 搜尋遠端資料可能會影響同一節點上執行之其他查詢的效能。我們建議對效能關鍵的應用程式佈建具有 `warm` 角色的專屬節點。
- 為了獲得更好的搜尋效能，請考慮在取得快照之前先[強制合併]({{site.url}}{{site.baseurl}}/api-reference/index-apis/force-merge/)索引為較少數量的分段。若要達到最佳效能（代價是在取得快照前使用運算資源），請將索引強制合併為一個分段。
- 我們建議使用 `cluster.filecache.remote_data_ratio` 設定來設定遠端資料與本機磁碟快取大小的最大比例。對大多數工作負載而言，比例 5 是確保良好查詢效能的良好起點。如果比例過大，磁碟空間可能不足以處理搜尋工作負載。如需遠端資料最大比例的詳細資訊，請參閱議題 [#11676](https://github.com/opensearch-project/OpenSearch/issues/11676)。
