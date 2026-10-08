---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "組態與系統設定"
parent: Configuring OpenSearch
nav_order: 10
---

# 組態與系統設定

如需建立 OpenSearch 叢集的概觀及組態設定範例，請參閱[建立叢集]({{site.url}}{{site.baseurl}}/tuning-your-cluster/index/)。若要了解如何套用這些設定，請參閱[設定 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/)。

## 叢集與節點識別設定

以下是識別叢集與節點所需的基本設定：

- `cluster.name`（靜態，字串）：叢集名稱。預設值為 `opensearch`。

- `node.name`（靜態，字串）：節點的描述性名稱。必要。

- `node.roles`（靜態，清單）：為 OpenSearch 節點定義一個或多個角色。有效值為 `cluster_manager`、`data`、`ingest`、`search`、`ml`、`remote_cluster_client` 和 `coordinating_only`。預設值為 `cluster_manager,data,ingest,remote_cluster_client`。

- `node.id.seed`（靜態，long）：提供種子值，用於決定節點持久保存的唯一 UUID。節點首次啟動時，此種子值有助於產生唯一的節點識別碼。如果節點的磁碟上已存有先前啟動時持久保存的 UUID，則會忽略此種子值並重複使用現有的 UUID。此設定有助於在自動化部署中確保節點識別的一致性。預設值為 `0`。接受任何 long 值，包括負數。

## 路徑設定

路徑設定定義 OpenSearch 安裝與資料儲存的目錄位置：

- `path.home`（靜態，字串）：指定 OpenSearch 安裝的主目錄路徑。這是安裝 OpenSearch 的根目錄，其中包含 bin、config、lib 及其他安裝目錄。此設定通常會在安裝期間自動設定，但必要時也可以明確設定。沒有預設值，必須在啟動時指定。

- `path.data`（靜態，字串）：儲存資料的目錄路徑。多個位置請以逗號分隔。預設值為 `$OPENSEARCH_HOME/data`。

- `path.logs`（靜態，字串）：記錄檔的路徑。預設值為 `$OPENSEARCH_HOME/logs`。

- `path.shared_data`（靜態，字串）：指定可供多個節點存取的共用資料目錄路徑。在多節點部署中，若叢集內的節點之間需要共用特定資料，此設定就很實用。指定的目錄必須可供所有需要共用資料的節點存取。沒有預設值，僅在需要共用資料功能時才設定。

## 記憶體與儲存空間設定

控制 OpenSearch 如何使用系統記憶體與儲存空間的設定：

- `bootstrap.memory_lock`（靜態，布林值）：在啟動時鎖定記憶體。建議將堆積大小設為系統可用記憶體的一半左右，並允許處理程序的擁有者使用此限制。當系統正在置換記憶體時，OpenSearch 的效能會不佳。預設值為 `false`。

- `node.store.allow_mmap`（靜態，布林值）：控制索引儲存作業是否允許使用記憶體對應檔案存取。啟用時，OpenSearch 可以使用記憶體對應（`mmapfs` 和 `hybridfs` 儲存類型），將檔案直接對應至虛擬記憶體，以提升 I/O 效能。停用此設定會強制使用不需要記憶體對應的替代儲存實作；在有記憶體對應限制或虛擬位址空間有限的環境中，可能必須這麼做。預設值為 `true`。

- `node.local_storage`（靜態，布林值）：控制節點是否可以將資料儲存在其本機檔案系統上。啟用時，節點可以將索引資料、叢集狀態及其他持久性資訊寫入本機磁碟。停用時，節點會以無狀態節點的形式運作，不會在本機持久保存任何資料。此設定適用於建立不儲存分片資料的專用協調節點。預設值為 `true`。

## 啟動程序與系統安全性設定

控制系統層級安全性與啟動程序行為的設定：

- `bootstrap.system_call_filter`（靜態，布林值）：控制 OpenSearch 是否要求作業系統封鎖建立新處理程序的系統呼叫。只有在無法安裝篩選器的平台上，才將其設為 `false`。如需各平台所使用的機制，以及安裝失敗時會停止節點的條件，請參閱[在作業系統層級封鎖處理程序建立]({{site.url}}{{site.baseurl}}/scripting/script-security/#blocking-process-creation-at-the-operating-system-level)。預設值為 `true`。

- `bootstrap.ctrlhandler`（靜態，布林值）：控制 OpenSearch 是否在 Windows 系統上啟用控制處理常式，以進行正常關閉。啟用時，OpenSearch 可以回應系統關閉訊號並執行清理作業。此設定主要與 Windows 部署相關，有助於確保正確的關閉行為。預設值為 `true`。

## 處理程序管理設定

適用於外部監控與處理程序管理工具的設定：

- `node.portsfile`（靜態，布林值）：控制 OpenSearch 是否將節點的連接埠資訊寫入磁碟上的檔案。啟用時，節點會建立一個包含其接聽中連接埠的檔案，這對外部監控與自動化工具很有用。此檔案通常會寫入節點的資料目錄，並在節點正常關閉時移除。預設值為 `false`。

- `node.pidfile`（靜態，字串）：指定 OpenSearch 寫入其處理程序 ID（PID）檔案的路徑。PID 檔案包含執行中 OpenSearch 節點的處理程序 ID，系統管理員與處理程序管理工具通常會使用它來追蹤及管理 OpenSearch 處理程序。此檔案會在節點啟動時建立，並在節點正常關閉時移除。指定的路徑應可供 OpenSearch 處理程序寫入。沒有預設值，除非指定此設定，否則不會建立 PID 檔案。
