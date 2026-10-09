---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證即時擷取元件"
grand_parent: Migration phases
nav_order: 4
parent: Deploy
permalink: /classic/migration-assistant/migration-phases/deploy/verifying-live-capture-components/
---

# 驗證即時擷取元件

使用 Migration Assistant 之前，請採取下列步驟，驗證您的叢集已準備好進行遷移。

### Traffic Replayer

若要停止執行 Traffic Replayer，請使用下列命令：

```bash
console replay stop
```
{% include copy.html %}

### Apache Kafka 

若要清除 Kafka 主題中所有已擷取的流量，您可以執行下列命令。

此命令會導致 Capture Proxy 到目前為止所擷取的所有流量資料遺失，因此應謹慎使用。
{: .warning}

```bash
console kafka delete-topic
```
{% include copy.html %}

### 目標叢集 

若要清除目標叢集中可能因測試而建立的非系統索引，您可以執行下列命令。

此命令會導致目標叢集中的所有資料遺失，因此應謹慎使用。
{: .warning}

```bash
console clusters clear-indexes --cluster target
```

## 切換用戶端流量

Migration Assistant Application Load Balancer 部署時會搭配一個接聽程式，透過 Proxy 服務在來源叢集與目標叢集之間切換流量。Application Load Balancer 應以 **Source Passthrough** 模式啟動。

### 驗證流量切換已完成

請使用下列步驟，驗證流量切換已完成：

1. 在 AWS Management Console 中，瀏覽至 **EC2 > Load Balancers**。
2. 選取 **MigrationAssistant ALB**。
3. 檢查連接埠 `9200` 上的接聽程式，並確認 100% 的流量都導向 **Source Proxy**。
4. 在 AWS Management Console 中，瀏覽至 **Migration ECS Cluster**。
5. 選取 **Target Proxy Service**。
6. 確認服務的所需計數正在執行中：
   * 如果未達到所需計數，請更新服務，將其增加至至少 1，並等待服務啟動。
7. 在 **Health and Metrics** 索引標籤的 **Load balancer health** 下，確認所有目標都回報為健康狀態：
   * 這可確認 Application Load Balancer 可以透過目標 Proxy 連線至目標叢集。
8. (重設) 在 Amazon Elastic Container Service (Amazon ECS) 中，將 **Target Proxy Service** 的所需計數更新回其原始值。

### 修正無法識別的流量模式

將流量切換至目標叢集時，您可能會遇到無法識別的流量模式。為了協助找出這些模式的原因，請使用下列步驟：
* 確認目標叢集允許來自 **Target Proxy security group** 的流量輸入。
* 瀏覽至 **Target Proxy ECS Tasks**，以調查任何失敗的工作。
將 **Filter desired status** 設定為 **Any desired status** 以檢視所有工作，然後瀏覽至任何已停止工作的記錄檔。


## 驗證複寫

部署 Traffic Capture Proxy 之後，請使用下列步驟驗證複寫是否正常運作：


1. 在 AWS Management Console 中，瀏覽至 **Migration ECS Cluster**。
2. 瀏覽至 **Capture Proxy Service**。
3. 確認擷取 Proxy 正在以所需的 Proxy 計數執行中。如果沒有，請更新服務，將其增加至至少 1，並等待啟動。
4. 在 **Health and Metrics** > **Load balancer health** 下，確認所有目標都健康。這表示 Application Load Balancer 可以透過 Capture Proxy 連線至來源叢集。
5. 瀏覽至 **Migration Console Terminal**。
6. 執行 `console kafka describe-topic-records`。等待 30 秒，讓另一個 Application Load Balancer 健康檢查執行。
7. 再次執行 `console kafka describe-topic-records`，並確認兩次執行之間的 RECORDS 數量增加。
8. 執行 `console replay start` 以啟動 Traffic Replayer。
9.  執行 `tail -f /shared-logs-output/traffic-replayer-default/*/tuples/tuples.log  | jq '.targetResponses[]."Status-Code"'`，確認 Kafka 請求已傳送至目標，且目標已如預期回應。如果沒有出現回應：
    * 執行 `./catIndices.sh` 以檢查 Migration Console 能否存取目標叢集，這應會顯示來源與目標中的索引。
    * 確認訊息仍持續記錄至 Kafka。
    * 使用 Amazon CloudWatch 檢查 Traffic Replayer 記錄檔 (`/migration/STAGE/default/traffic-replayer-default`) 中是否有錯誤。
10. (重設) 在 Amazon ECS 中，將 **Capture Proxy Service** 的所需計數更新回其原始值。

### 疑難排解

請使用本指引來排解下列任何複寫驗證問題。

### 健康檢查回應 401/403 狀態碼

如果來源叢集設定為需要驗證，Capture Proxy 將無法驗證複寫，僅能在 Application Load Balancer 健康檢查中收到 401/403 狀態碼。如需詳細資訊，請參閱[失敗模式](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficCaptureProxyServer/README.md#failure-modes)。

### 流量未送達來源叢集 

確認來源叢集允許來自 Capture Proxy security group 的流量輸入。

瀏覽至 **Traffic Capture Proxy ECS**，以尋找失敗的工作。將 **Filter desired status** 變更為 **Any desired status**，以查看所有工作，並瀏覽至已停止工作的記錄檔。

## 遷移前重設

所有驗證完成之後，請先重設所有資源，再使用 Migration Assistant 進行實際遷移。 

下列步驟概述如何在執行實際遷移之前，使用 Migration Assistant 重設資源。此時，預期所有驗證都已完成。這些步驟可以在[存取 Migration Console]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-console/accessing-the-migration-console/) 之後執行。

### Traffic Replayer

若要停止執行 Traffic Replayer，請使用下列命令：

```bash
console replay stop
```
{% include copy.html %}

### Kafka 

若要清除 Kafka 主題中所有已擷取的流量，您可以執行下列命令。

此命令會導致 Capture Proxy 到目前為止所擷取的所有流量資料遺失，因此應謹慎使用。
{: .warning}

```bash
console kafka delete-topic
```
{% include copy.html %}

### 目標叢集 

若要清除目標叢集中可能因測試而建立的非系統索引，您可以執行下列命令。 

此命令會導致目標叢集中的所有資料遺失，因此應謹慎使用。
{: .warning}

```bash
console clusters clear-indexes --cluster target
```
{% include copy.html %}
