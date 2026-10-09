---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預設動作群組"
parent: Access control
nav_order: 80
redirect_from:
 - /security-plugin/access-control/default-action-groups/
---

# 預設動作群組

本頁列出所有預設動作群組。建立新動作群組時，最連貫的方式通常是將這些預設群組與[個別權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)結合使用。


## 一般

| 動作群組 | 說明 | 權限 |
| :--- | :--- | :--- |
| unlimited | 授予動作群組的完整存取權。可用於 `cluster-` 或 `index-` 層級。等同於「*」。 | `*` |



## 叢集層級

| 動作群組 | 說明 | 權限 |
| :--- | :--- | :--- |
| cluster_all | 授予所有叢集權限。等同於 `cluster:*`。 | `cluster:*` |
| cluster_monitor | 授予所有叢集監控權限。等同於 `cluster:monitor/*`。 | `cluster:monitor/*` |
| cluster_composite_ops_ro | 授予執行 `mget`、`msearch` 或 `mtv` 等請求的唯讀權限，以及查詢別名的權限。 | `indices:data/read/mget` `indices:data/read/msearch` `indices:data/read/mtv` `indices:admin/aliases/exists*` `indices:admin/aliases/get*` `indices:data/read/scroll` `indices:admin/resolve/index` |
| cluster_composite_ops | 與 `CLUSTER_COMPOSITE_OPS_RO` 相同，但另外授予大量操作 (bulk) 權限與所有別名權限。 | `indices:data/write/bulk` `indices:admin/aliases*` `indices:data/write/reindex` `indices:data/read/mget` `indices:data/read/msearch` `indices:data/read/mtv` `indices:admin/aliases/exists*` `indices:admin/aliases/get*` `indices:data/read/scroll` `indices:admin/resolve/index` |
| manage_snapshots | 授予管理快照與儲存庫的權限。 | `cluster:admin/snapshot/*` `cluster:admin/repository/*` |
| cluster_manage_pipelines | 授予管理資料匯入管線的權限。 | `cluster:admin/ingest/pipeline/*` |
| cluster_manage_index_templates | 授予管理索引範本的權限。 | `indices:admin/template/*` `indices:admin/index_template/*` `cluster:admin/component_template/*` |


## 索引層級

| 動作群組 | 說明 | 權限 |
| :--- | :--- | :--- |
| indices_all | 授予索引的所有權限。等同於 `indices:*`。 | `indices:*` |
| get | 授予使用 `get` 與 `mget` 動作的權限。 | `indices:data/read/get*` `indices:data/read/mget*` |
| read | 授予索引的讀取權限，例如 `search`、`get` 欄位對應、`get` 與 `mget`。 | `indices:data/read*` `indices:admin/mappings/fields/get*` `indices:admin/resolve/index` |
| write | 授予在現有索引內建立與更新文件的權限。 | `indices:data/write*` `indices:admin/mapping/put` |
| delete | 授予刪除文件的權限。 | `indices:data/write/delete*` |
| crud | 結合 read、write 與 delete 動作群組。包含於 `data_access` 動作群組中。 | `indices:data/read*` `indices:admin/mappings/fields/get*` `indices:admin/resolve/index` `indices:data/write*` `indices:admin/mapping/put` |
| search | 授予搜尋文件的權限，包括 Suggest API。 | `indices:data/read/search*` `indices:data/read/msearch*` `indices:admin/resolve/index` `indices:data/read/suggest*` |
| suggest | 授予使用 Suggest API 的權限。包含於 `read` 動作群組中。 | `indices:data/read/suggest*` |
| create_index | 授予建立索引與對應的權限。 | `indices:admin/create` `indices:admin/mapping/put` |
| indices_monitor | 授予執行所有索引監控動作的權限，例如 `recovery`、`segments_info`、`index_stats` 與 `status`)。 | `indices:monitor/*` |
| index | write 動作群組的限制較嚴格版本。 | `indices:data/write/index*` `indices:data/write/update*` `indices:admin/mapping/put` `indices:data/write/bulk*` |
| data_access | 將 CRUD 動作群組與 `indices:data/*` 結合。 | `indices:data/*` `indices:data/read*` `indices:admin/mappings/fields/get*` `indices:admin/resolve/index` `indices:data/write*` `indices:admin/mapping/put` |
| manage_aliases | 授予管理別名的權限。 | `indices:admin/aliases*` |
| manage | 授予索引的所有監控與管理權限。 | `indices:monitor/*` `indices:admin/*` |
