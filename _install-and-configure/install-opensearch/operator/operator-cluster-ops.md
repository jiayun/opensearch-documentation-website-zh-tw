---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "叢集操作"
parent: OpenSearch Kubernetes Operator
grand_parent: Installing OpenSearch
nav_order: 50
---

# 叢集操作

Operator 可自動化叢集生命週期中的常見管理任務，包括故障復原、滾動升級、組態變更以及磁碟區擴充。

## 叢集復原

Operator 會自動處理常見的故障情境並重新啟動崩潰的 pod。通常情況下，Operator 會逐一重新啟動 pod，以維持法定人數 (quorum) 和叢集穩定性。

如果 Operator 同時偵測到某個節點池有多個崩潰或遺失的 pod，它會切換到特殊的復原模式，一次啟動所有 pod 並允許叢集形成新的法定人數。這種平行復原模式是實驗性的，且僅適用於基於 PVC 的儲存，因為它使用現有 PVC 的數量來確定遺失 pod 的數量。

復原是透過暫時變更每個節點池底層的 `StatefulSet` 並將 `podManagementPolicy` 設定為 `Parallel` 來完成的。如果您遇到問題，請透過重新部署 Operator 並在 `values.yaml` 中加入 `manager.parallelRecoveryEnabled: false` 來停用平行復原。請透過在 Operator 專案中開啟 GitHub issue 來回報任何問題。

如果您刪除了叢集但保留了 PVC，然後重新安裝叢集，也會啟動復原模式。

如果每個節點池都使用 `emptyDir` 儲存，Operator 會在以下故障情境中啟動復原：

1. 超過一半的叢集管理員節點遺失或崩潰，導致法定人數中斷。
2. 所有資料節點遺失或崩潰，導致沒有可用的資料節點。

由於 `emptyDir` 儲存是暫時性的，當 pod 被刪除時，資料會遺失且無法復原。在這種情境下，Operator 會刪除並重新建立整個 OpenSearch 叢集。

## 滾動升級

Operator 支援自動滾動版本升級。要進行升級，請變更叢集 `spec` 中的 `general.version` 並重新套用：

```yaml
spec:
  general:
    version: 3.0.0
```
{% include copy.html %}

接著 Operator 會執行滾動升級，逐一重新啟動節點，並在每個節點重新啟動後等待叢集穩定並達到綠色狀態。根據節點數量和儲存資料的大小，這可能需要一些時間。

不支援降級以及跨越多個主版本的升級，因為這會使 OpenSearch 叢集處於不支援的狀態。如果您為資料節點使用 `emptyDir` 儲存，請將 `general.drainDataNodes` 設定為 `true` 以避免資料遺失。

## 組態變更

如果您在已安裝的叢集上變更 OpenSearch 組態，Operator 會偵測到變更並對所有叢集節點執行滾動重新啟動，以套用新組態。有關新增 OpenSearch 組態的更多資訊，請參閱 [Configuring opensearch.yml]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/operator/operator-opensearch-config/#configuring-opensearchyml)。這同樣適用於節點池特定的組態，例如 `resources`、`annotations` 或 `labels`。

## 磁碟區擴充

如果您的底層儲存支援線上磁碟區擴充，Operator 可以為您協調該操作。

要增加磁碟區大小，請將節點池的 `diskSize` 設定為所需值，並重新套用叢集 `spec` YAML。此操作沒有停機時間，叢集將保持運作狀態。

增加磁碟大小時請考慮以下事項：

- 這僅適用於基於 PVC 的持久化儲存。
- 在擴充叢集磁碟之前，請備份磁碟區和資料，以便在發生任何故障時能透過還原備份來復原。
- 在套用新 `diskSize` 之前，請確保叢集儲存類別 (storage class) 具有 `allowVolumeExpansion: true`。更多資訊請參閱 [Kubernetes storage classes](https://kubernetes.io/docs/concepts/storage/storage-classes/).
- 在驗證儲存類別組態後，將具有新 `diskSize` 值的叢集 YAML 套用到所有節點池或單一節點池。
- 請勿在執行磁碟區擴充的同時對叢集套用任何其他變更。
- 確保大小單位一致。例如，如果 `diskSize` 為 `30G`，請使用 `G` 進行擴充（例如 `50G`）。在擴充過程中請勿在 `G` 和 `Gi` 之間切換。

要將 `diskSize` 單位從 `G` 變更為 `Gi` 或反之，請先備份資料並計算正確的轉換值，使底層磁碟區大小保持不變。然後重新套用叢集 YAML。這可確保 `StatefulSet` 以 `VolumeClaimTemplates` 中的正確值重新建立。此操作沒有停機時間。
{: .note}
