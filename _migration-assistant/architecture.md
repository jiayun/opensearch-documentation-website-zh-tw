---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "架構"
nav_order: 15
permalink: /migration-assistant/architecture/
redirect_from:
  - /migration-assistant/overview/architecture/
---

# Migration Assistant 架構

Migration Assistant 採用下列運作模型：

1. 您在工作流程組態中描述遷移作業。
2. Workflow CLI 將該組態提交至 Kubernetes。
3. Kubernetes 與 Argo Workflows 建立各階段所需的 Pod 與服務。
4. 您觀察進度、核准需經審核的步驟、驗證結果，並將流量切換至目標。

在內部，工作流程由 [Argo Workflows](https://argoproj.github.io/workflows/) 執行，但您透過 Migration Console 與 Workflow CLI 操作 Migration Assistant，而非直接透過 Argo 操作。

下圖說明在 Amazon Elastic Kubernetes Service（EKS）上的典型部署。其他 Kubernetes 發行版採用相同的邏輯遷移模型，但 EKS 額外提供 AWS 專屬的身分、網路、映像檔與可觀測性整合。

![EKS 上的 Migration Assistant 架構]({{site.url}}{{site.baseurl}}/images/migration-assistant/eks-architecture.svg)

## 系統層

Migration Assistant 將職責分為兩層。您只需描述一次遷移作業，平台便會將其作為受管理的工作負載執行：

- 管理遷移工作流程的 **控制平面**。
- 執行實際快照、中繼資料、回填、擷取與重播工作的 **資料平面**。

## 控制平面

下表列出控制平面元件。

| 元件 | 說明 |
|:----------|:------------|
| **Migration Console** | 您執行 `console` 與 `workflow` 命令的 Pod |
| **Workflow CLI** | 用於組態設定、提交、核准與狀態查詢的主要介面 |
| **Argo Workflows** | 依序執行任務、重試失敗的任務並追蹤狀態的工作流程引擎 |
| **Kubernetes** | 排程 Pod、建立服務、管理 Secret 並清理資源的平台 |

## 資料平面

下表列出資料平面元件。

| 元件 | 說明 |
|:----------|:------------|
| **Reindex-from-Snapshot（RFS）** | 高效能回填引擎，從快照讀取 Lucene 分段，而非透過來源叢集 API 讀取文件 |
| **中繼資料遷移** | 傳輸索引設定、對應、範本與別名 |
| **Capture Proxy** | 在零停機遷移期間，將即時流量記錄至 Apache Kafka |
| **Traffic Replayer** | 對目標叢集重播擷取的流量，使其追上最新狀態 |
| **Strimzi** | 為 Capture and Replay 工作流程管理 Kafka |
| **可觀測性堆疊** | 與 Prometheus 相容的指標、記錄檔與儀表板；在 EKS 上，這些功能延伸至 CloudWatch |

## 遷移程序概觀

架構圖中每個編號節點都對應遷移程序中的一個步驟。

### 步驟 1：將用戶端流量導向現有叢集

用戶端流量如常流向來源叢集。如果您使用 Capture and Replay 執行零停機遷移，Kubernetes Service 會將流量路由經過擷取代理伺服器群組，該群組會將請求轉送至來源，同時將請求記錄至 Kafka。

### 步驟 2：擷取代理伺服器將流量複製至 Kafka

擷取代理伺服器將流量轉送至來源叢集，同時將原始請求／回應串流複製至 Kafka（由 Strimzi 管理）。這會為遷移期間的所有寫入作業提供持久的記錄。此步驟不適用於僅執行回填的遷移。

### 步驟 3：透過 Reindex-from-Snapshot 建立快照並回填

在持續擷取流量的機制就緒後（或暫停寫入後），您從 Migration Console 提交遷移工作流程。工作流程會建立來源叢集在特定時間點的快照、遷移中繼資料（索引、範本、別名），然後啟動 Reindex-from-Snapshot（RFS）工作程序，直接從 Amazon S3 中的快照讀取資料，並將文件批次編製索引至目標叢集。

### 步驟 4：Traffic Replayer 使目標追上最新狀態

回填完成後，Traffic Replayer 會從 Kafka 讀取擷取的流量，並對目標叢集重播，視需要轉換請求（驗證、索引名稱）。Replayer 使目標追上即時狀態，消除快照時間點與目前狀態之間的差距。

### 步驟 5：驗證與比較

透過檢視記錄檔、指標與文件數量，分析路由至來源與目標叢集的流量效能及行為。使用 `console clusters curl` 對兩個叢集執行比較查詢。在一般 Kubernetes 上，這通常會使用您叢集的記錄與指標堆疊；在 EKS 上，初始設定流程也會整合 CloudWatch 儀表板與記錄檔。

### 步驟 6：重新導向流量並停用來源

確認目標叢集的功能符合預期後，透過更新 DNS 記錄、負載平衡器組態或應用程式連線字串，將用戶端重新導向新的目標。保留來源叢集作為備援（建議保留 24--72 小時），然後停用來源並移除 Migration Assistant 基礎架構。

## 錯誤復原

以下列出常見的錯誤復原徵兆與解決方式。

### 工作流程失敗

如果工作流程步驟失敗，請執行下列步驟：

1. 使用 `workflow status` 與 `workflow log all` 檢查錯誤。
2. 修正根本問題，例如連線、權限或組態問題。
3. 透過工作流程模型重試或重新提交，而非手動修補 Pod。

### 恢復 RFS 回填

RFS 會自動追蹤進度。如果回填中斷，會採取下列行為：
- RFS 重新啟動時，會自動從上一個檢查點恢復。
- 已遷移的分片會略過。
- 不會產生重複資料。

## 元件詳細資訊

下列元件構成 Migration Assistant 架構。

### Reindex-from-Snapshot

RFS 採用與傳統遷移工具根本不同的方法。它不會透過來源叢集的 HTTP API 讀取文件，而是：

1. 建立來源叢集的 **一次性快照**（這是唯一會存取來源的時機）
2. 直接從儲存空間（S3）中的快照讀取 **原始 Lucene 分段檔案**
3. 擷取文件、套用轉換，並 **在目標上批次編製索引**

此方法 **不會持續對來源造成負載**、**沒有版本相容性限制**（適用於任何受支援的版本差距）、支援 **平行處理**（每個分片使用一個工作程序），並且能夠 **從中斷處恢復**（重試失敗的分片，無須重新開始）。

{% include migration-phase-navigation.html %}
