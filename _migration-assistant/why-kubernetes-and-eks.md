---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "為什麼選擇 Kubernetes 和 EKS？"
nav_order: 12
permalink: /migration-assistant/why-kubernetes-and-eks/
---

# 為什麼選擇 Kubernetes 和 EKS

Migration Assistant 以一個平台無關的遷移工具取代了傳統的 ECS 部署模型，該工具可以在任何地方執行、更容易重複使用與維運，並且符合現代平台團隊的需求。

新版 Migration Assistant 遵循三項原則：

1. **在 workflow 組態中宣告一次遷移**，而不是手動串接長期存在的基礎架構。
2. **讓 Kubernetes 執行工作**，使遷移任務可以像一般的平台工作負載一樣建立、重試、擴展和清理。
3. **使用 Amazon EKS 作為建議的 AWS 生產環境路徑**，因為它會設定您通常無論如何都需要的 AWS 服務和權限。

## 與傳統 Migration Assistant 的差異

下表比較了傳統與新版 Migration Assistant 模型。

| 傳統 (ECS) | 新版 Migration Assistant |
|:--------------|:------------------------|
| 專注於固定的 AWS 部署模型 | 在 Kubernetes 上使用相同的 workflow 模型，並以 Amazon EKS 作為建議的 AWS 路徑 |
| 預先設定並保留較多基礎架構 | 僅在需要時才將遷移工作建立為 Kubernetes 工作負載 |
| 除了遷移思維之外，還需要更多平台思維 | 您主要只需思考 workflow 組態、核准、驗證和切換 |
| AWS 專屬的部署細節塑造了心智模型 | 現在的心智模型是：宣告、提交、觀察、核准、驗證，然後將流量切換到目標 |

## Kubernetes 的優點

Kubernetes 作為平台層，讓 Migration Assistant 更可預測。在 Kubernetes 上執行 Migration Assistant 提供下列優點：

- **可重複執行**：在組態或環境變更後，可以再次執行相同的 workflow。
- **短生命週期的遷移工作者**：回填、重播、驗證和支援元件以 pod 的形式執行，而不是永久管理的服務。
- **更好的故障復原**：Kubernetes 和 Argo Workflows 可以重新啟動工作、保留狀態，並以一致的方式讓故障可見。
- **清楚的關注點分離**：您定義遷移，而平台管理 pod 排程、服務網路、記錄檔和資源生命週期。
- **可攜性**：相同的遷移引擎可以在本機開發叢集、自行管理的 Kubernetes 或 Amazon EKS 上執行。

## 為什麼遷移需要部署基礎架構

生產環境遷移是長時間執行、有狀態的作業，需要持久性的基礎架構。Migration Assistant 部署的基礎架構可支援大規模資料搬移的需求：

- **檢查點與續傳**：如果回填工作者在處理期間失敗，它會從最後一個檢查點續傳，而不是從頭重新開始。
- **核准關卡**：生產環境遷移需要在階段之間有人為決策點，例如在開始回填之前驗證中繼資料，或在切換流量之前確認文件數量。workflow 引擎會在這些關卡之間無限期地保留狀態。
- **具協調機制的平行工作者**：Reindex-from-Snapshot 會將工作分配給多個工作者。Kubernetes 會自動管理排程、擴展和重新啟動失敗的工作者。
- **持續的流量擷取**：零停機遷移需要 Kafka 在擷取代理程式與 Replayer 之間持續緩衝即時流量。這無法暫時性地執行。
- **內建可觀測性**：當遷移第四天發生問題時，記錄檔、指標和 workflow 狀態無需額外設定即可用於診斷。
- **可重複性**：執行試驗遷移所使用的相同 Helm chart 和 workflow 組態，無需手動重新設定即可執行生產環境遷移。

對於從頭重新開始可以接受的小型資料集，較簡單的方法可能就足夠了。對於有正常執行時間要求的生產環境遷移，正是這些基礎架構將脆弱的手動流程轉變為可以在無人值守下執行並自動從故障中復原的作業。

## 為什麼 Amazon EKS 是建議的 AWS 路徑

如果您使用 AWS 並想要生產環境部署，Amazon EKS 能以最少的平台工作提供最大的價值。

EKS 路徑不只是「在 AWS 上執行 Kubernetes」。它為 AWS 上的 Migration Assistant 提供了現成的維運模型：

- **Bootstrap 自動化**：使用 bootstrap 指令碼部署到新的 VPC 或現有的 VPC。
- **AWS 身分組態**：為需要 AWS 存取權的服務帳戶設定 pod 身分。
- **私有映像檔支援**：bootstrap 路徑可以將映像檔和 chart 鏡像到私有 ECR，以用於隔離的環境。
- **快照輔助工具**：部署提供預設的儲存貯體組態和快照角色組態。
- **AWS 原生可觀測性**：記錄檔、指標和 CloudWatch 儀表板已整合到部署中。
- **AWS 感知排程預設值**：Karpenter 節點集區和 EBS 支援的儲存空間預設值已為平台預先設定。

對於 AWS 部署而言，這代表花在建置支援基礎架構的時間更少，而花在驗證遷移本身的時間更多。

## 一般 Kubernetes

在下列情況下，一般 Kubernetes 是有效的選項：

- 您已經有一個由您的團隊維運的非 EKS Kubernetes 平台。
- 您不使用 AWS。
- 您正在進行本機開發或評估。
- 您想要自備記錄、儲存空間、登錄檔和工作負載身分模型。

兩種選項都使用相同的遷移引擎。在一般 Kubernetes 上，您需要自行設定平台整合。在 EKS 上，bootstrap 工具會為您設定這些整合。

## 相關文件

- 如果您要尋找較舊的 ECS 模型，請參閱[傳統 Migration Assistant 文件]({{site.url}}{{site.baseurl}}/classic/migration-assistant/)。
