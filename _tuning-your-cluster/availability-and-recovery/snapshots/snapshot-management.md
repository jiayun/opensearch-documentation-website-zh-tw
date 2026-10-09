---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "快照管理"
parent: Snapshots
nav_order: 20
has_children: false
grand_parent: Availability and recovery
redirect_from: 
  - /opensearch/snapshots/snapshot-management/
---

# 快照管理

快照管理 (Snapshot Management, SM) 可讓您自動化[建立快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore#take-snapshots)的流程。若要使用此功能，您必須安裝 [索引管理 (IM) 外掛程式]({{site.url}}{{site.baseurl}}/im-plugin/)。快照只儲存自上次快照以來的增量變更。因此，雖然建立初始快照可能是繁重的作業，但後續快照的負擔極小。若要設定自動快照，您必須以所需的 SM 排程與組態建立 SM 政策。

建立 SM 政策時，其文件 ID 會命名為 `<policy_name>-sm-policy`。因此，SM 政策必須遵守下列規則：

- SM 政策必須有唯一的名稱。

- 政策建立後，您無法更新其名稱。

由 SM 建立的快照名稱格式為 `<policy_name>-<date>-<random number>`。不同政策在同一時間建立的兩個快照，因為 `<policy_name>` 前置詞而必定有不同的名稱。為避免同一政策內發生名稱衝突，每個快照的名稱都包含一個隨機字串後置詞。

每個政策都有儲存政策狀態的相關中繼資料。快照管理會將 SM 政策與中繼資料儲存在系統索引中，並從系統索引讀取。因此，快照管理依賴 OpenSearch 叢集的索引編製與搜尋功能。政策的中繼資料只保留最近一次建立與刪除的資訊。中繼資料會在每次執行排程工作前讀取，讓 SM 能從上一個工作的狀態繼續執行。您可以使用 [explain API]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#explain) 檢視中繼資料。

SM 排程是自訂的 [cron]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/#cron-expressions) 運算式。它由兩部分組成：建立排程與刪除排程。您必須設定指定快照建立頻率與時間的建立排程。此外，您也可以選擇性地設定另一個用於刪除快照的排程。

SM 組態包含快照的索引與儲存庫，並支援您透過 API [建立快照]({{site.url}}{{site.baseurl}}/opensearch/snapshots/snapshot-restore#take-snapshots)時可定義的所有參數。此外，您還可以指定快照名稱中所用日期的格式與時區。


## 效能

一個快照可包含叢集中現有的所有索引。我們預期單一叢集中最多只有數十個 SM 政策，但一個快照儲存庫可以安全地擴充至數千個快照。不過，為了管理其中繼資料，大型儲存庫需要在叢集管理員節點上使用更多記憶體。

快照管理依賴 Job Scheduler 外掛程式來排程定期執行的工作。每個 SM 政策對應一個 SM 排程的工作。排程工作非常輕量，因此 SM 的負擔取決於快照建立頻率以及執行快照作業本身的負擔。

### 儲存庫資料快取
**2.19 版新增**
{: .label .label-purple }

為提升效能，OpenSearch 會將儲存庫中繼資料 (儲存庫資料) 快取在記憶體中，減少在複製、還原與狀態檢查等快照作業期間重複下載這些資料的需求。您可以使用 `snapshot.repository_data.cache.threshold` 設定來控制快取儲存庫資料的大小上限。組態詳細資訊請參閱 [快照設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/availability-recovery/#snapshot-settings)。

如果您的儲存庫中繼資料超過所設定快取閾值的 10 倍，OpenSearch 會記錄一則警告，建議您考慮改用新的儲存庫。大型儲存庫中繼資料可能影響效能，因為下載與處理需要更長時間。如果您遇到此警告，請考慮下列選項：

- 如果您的節點有足夠的堆積記憶體，請提高 `snapshot.repository_data.cache.threshold` 設定。
- 建立新的快照儲存庫以減少中繼資料大小。
- 刪除不再需要的舊快照，以減少儲存庫中繼資料的大小。

## 並行處理

SM 政策不支援並行的快照作業，因為過多此類作業可能會使叢集效能降低。快照作業 (建立或刪除) 是以非同步方式執行。SM 在上一個非同步作業完成之前，不會啟動新的作業。

我們不建議在同一叢集中建立多個排程相同且索引重疊的 SM 政策，因為這會導致在相同索引上並行建立快照，並妨礙效能。
{: .warning }


我們不建議在不同叢集中為多個排程相同的 SM 政策設定同一個儲存庫，因為這可能導致該儲存庫的負擔突然飆升。
{: .warning }

## 失敗管理

如果快照作業失敗，最多會重試三次。失敗訊息會儲存在 `metadata.latest_execution` 中，並在後續快照作業開始時被覆寫。您可以使用 [explain API]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#explain) 檢視失敗訊息。使用 OpenSearch Dashboards 時，您可以在[政策詳細資料頁面]({{site.url}}{{site.baseurl}}/dashboards/admin-ui-index/sm-dashboards#view-edit-or-delete-an-sm-policy)上檢視失敗訊息。可能的失敗原因包括紅色索引狀態與分片重新分配。

## 安全性

Security 外掛程式為快照管理動作提供兩個內建角色：`snapshot_management_full_access` 與 `snapshot_management_read_access`。各角色的說明請參閱 [預先定義的角色]({{site.url}}{{site.baseurl}}/security/access-control/users-roles#predefined-roles)。

下表列出每個快照管理 API 所需的權限。

功能 | API | 權限
:--- | :--- | :---
取得政策 | `GET _plugins/_sm/policies`<br>`GET _plugins/_sm/policies/{policy_name}` | `cluster:admin/opensearch/snapshot_management/policy/get`<br>`cluster:admin/opensearch/snapshot_management/policy/search`
建立/更新政策 | `POST _plugins/_sm/policies/{policy_name}`<br>`PUT _plugins/_sm/policies/{policy_name}?if_seq_no=1&if_primary_term=1` | `cluster:admin/opensearch/snapshot_management/policy/write`
刪除政策 | `DELETE _plugins/_sm/policies/{policy_name}` | `cluster:admin/opensearch/snapshot_management/policy/delete`
Explain | `GET _plugins/_sm/policies/{policy_names}/_explain` | `cluster:admin/opensearch/snapshot_management/policy/explain`
啟動 | `POST _plugins/_sm/policies/{policy_name}/_start` | `cluster:admin/opensearch/snapshot_management/policy/start`
停止 | `POST _plugins/_sm/policies/{policy_name}/_stop` | `cluster:admin/opensearch/snapshot_management/policy/stop`


## API

下表列出所有[快照管理 API]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api/) 功能。

功能 | API | 說明
:--- | :--- | :---
[建立政策]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#create-or-update-a-policy) | `POST _plugins/_sm/policies/{policy_name}` | 建立 SM 政策。
[更新政策]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#create-or-update-a-policy) | `PUT _plugins/_sm/policies/{policy_name}?if_seq_no={sequence_number}&if_primary_term={primary_term}` | 修改 `{policy_name}` 政策。
[取得所有政策]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#get-policies) | `GET _plugins/_sm/policies` | 傳回所有 SM 政策。
[取得政策 `{policy_name}`]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#get-policies) | `GET _plugins/_sm/policies/{policy_name}` | 傳回 `{policy_name}` SM 政策。
[刪除政策]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#delete-a-policy) | `DELETE _plugins/_sm/policies/{policy_name}` | 刪除 `{policy_name}` 政策。
[Explain]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#explain) | `GET _plugins/_sm/policies/{policy_names}/_explain` | 提供 `{policy_names}` 所指定所有政策的啟用/停用狀態與中繼資料。
[啟動政策]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#start-a-policy) | `POST _plugins/_sm/policies/{policy_name}/_start` | 啟動 `{policy_name}` 政策。
[停止政策]({{site.url}}{{site.baseurl}}/opensearch/snapshots/sm-api#stop-a-policy) | `POST _plugins/_sm/policies/{policy_name}/_stop` | 停止 `{policy_name}` 政策。