---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "安全性修補與更新"
nav_order: 30
permalink: /classic/migration-assistant/security-patching-and-updating/
---

# 安全性修補與更新

本頁面說明如何安全地更新 **bootstrap box** (用於建置與執行 Migration Assistant 元件的 Amazon Elastic Compute Cloud [Amazon EC2] 執行個體)、清理 Docker 快取，以及重建 Migration Assistant 容器映像。

> **建議頻率**：僅在 Migration Assistant 未執行時執行這些步驟。

---

## 步驟 1：修補 bootstrap box 上的作業系統

```shell
sudo dnf upgrade --refresh -y
```
{% include copy.html %}

> **注意**：如果核心或核心程式庫已更新，通常需要重新開機。

如有需要，請重新開機：

```shell
sudo reboot
```
{% include copy.html %}

機器重新啟動後，重新連線並繼續。


## 步驟 2：清除 Docker 建置與下載快取

清除 Docker 建置與下載快取會移除**所有**未使用的映像、容器、網路與儲存區 (volume)，以釋放磁碟空間並確保重建時的乾淨狀態：

```shell
docker system prune -a --volumes
```
{% include copy.html %}


## 步驟 3：清理先前的 Gradle 輸出

從儲存庫根目錄執行下列命令，以清理先前的 Gradle 輸出：

```shell
./gradlew clean
```
{% include copy.html %}


## 步驟 4：重建 Migration Assistant 映像

重建 Migration Assistant 使用的 Docker 映像：

```shell
./gradlew :buildDockerImages -x test
```
{% include copy.html %}


## 步驟 5：重新部署 Migration Assistant

重新部署 Migration Assistant，以最新建置的版本取代現有的容器映像：

```shell
cd deployment/cdk/opensearch-service-migration
./deploy.sh <contextId>
```
{% include copy.html %}

> **警告**：重新部署會中斷任何執行中的遷移工作 (例如 Capture Proxy、Traffic Replayer 或 Reindex-from-Snapshot)。
> **請勿**在遷移進行中重新部署，否則可能導致資料遺失或狀態不一致。
{: .warning}


## 疑難排解

* **`toomanyrequests: Rate exceeded`**：
  重試最後一個建置命令。部分下游容器映像有速率限制，且可能隨時間變更。

* **無法提取基礎映像**：
  確認執行個體具有網際網路對外連線 (NAT/IGW)，並視需要可存取 Docker Hub/Amazon Elastic Container Registry (Amazon ECR)。

* **Gradle 快取損毀**：
  如果在 `./gradlew clean` 之後問題仍然存在，請一併移除 `~/.gradle/caches` 後重試。