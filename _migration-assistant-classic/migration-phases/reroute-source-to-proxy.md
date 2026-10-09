---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "重新路由用戶端流量"
nav_order: 3
parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/reroute-source-to-proxy/
---

# 將用戶端流量重新路由至 Traffic Capture Proxy

**注意**：本頁面僅適用於您在遷移期間使用 Capture and Replay 以避免停機的情況。如果您只執行回填遷移，可以略過此步驟。
{: .note}

## Capture Proxy 資料複寫

如果您想在遷移期間擷取即時流量，Migration Assistant 內建一個 Application Load Balancer，用於將流量路由至 Capture Proxy 與目標叢集。上游的用戶端流量必須經過 Capture Proxy 路由，才能在之後重播請求。使用 Capture Proxy 之前，請記住以下幾點：

* Application Load Balancer 的上游層必須與 Application Load Balancer 監聽器的憑證相容，無論其對象是用戶端還是 Network Load Balancer。可能需要提供 `cdk.context.json` 中的 `albAcmCertArn`，以確保用戶端信任 Application Load Balancer 憑證。
* 如果在 Application Load Balancer 的正上游使用 Network Load Balancer，則必須使用 TLS 監聽器。
* 上游資源與安全群組必須允許網路存取 Migration Assistant Application Load Balancer。

若要設定 Capture Proxy，請前往 AWS Management Console，並導覽至 **EC2 > Load Balancers > Migration Assistant Application Load Balancer**。複製 Application Load Balancer URL。複製 URL 後，您可以使用下列其中一種選項。



### Network Load Balancer → Application Load Balancer → 叢集

1. 確認已直接為 Capture Proxy 的 Application Load Balancer 提供傳入存取。
2. 在連接埠 `9200` 上為 Migration Assistant Application Load Balancer 建立目標群組，並將健康檢查設為 `HTTPS`。
3. 在新的監聽器上，將此目標群組與您現有的 Network Load Balancer 建立關聯以進行測試。
4. 確認健康檢查成功，並透過新的監聽器連接埠對一些用戶端執行煙霧測試。
5. 當您準備好遷移所有用戶端時，將 Migration Assistant Application Load Balancer 目標群組從測試用的 Network Load Balancer 監聽器卸離，並修改現有的 Network Load Balancer 監聽器，將流量導向此目標群組。
6. 現在用戶端請求將會透過代理程式路由（一旦建立新連線）。請驗證應用程式指標。

### Network Load Balancer → 叢集

如果您不想修改應用程式邏輯，請在叢集前面加入一個 Application Load Balancer，並遵循 **Network Load Balancer → Application Load Balancer → Cluster** 步驟。否則：

1. 在連接埠 `9200` 上為 Application Load Balancer 建立目標群組，並將健康檢查設為 `HTTPS`。
2. 在新的監聽器上，將此目標群組與您現有的 Network Load Balancer 建立關聯。
3. 確認健康檢查成功，並透過新的監聽器連接埠對一些用戶端執行煙霧測試。
4. 當您準備好遷移所有用戶端時，部署變更，讓用戶端連向新的監聽器。
   

### 不使用 Network Load Balancer

如果您只使用回填作為遷移技術，請變更用戶端/DNS，將用戶端路由至連接埠 `9200` 上的 Migration Assistant Application Load Balancer。


### Apache Kafka 連線

根據您的使用案例路由用戶端之後，請依照下列步驟，檢查記錄是否隨 HTTP 請求增加。

在 Migration Console 中，執行以下命令：

```bash
console kafka describe-topic-records
```
{% include copy.html %}
   
記下 logging 主題中的記錄。
   
經過一段短時間後，再次執行相同的命令，並將增加的記錄數量與預期的 HTTP 請求數進行比較。

## 疑難排解

下列章節可能有助於診斷常見問題。

### Host 標頭路由組態

某些系統（例如 Elastic Cloud 與其他託管的 Elasticsearch 服務）使用 `Host` 標頭將流量路由至適當的叢集。在這些系統上使用 Capture Proxy 時，您必須設定代理程式，以來源叢集的網域名稱覆寫 `Host` 標頭。如果設定不正確，用戶端可能會傳送指向代理程式位址而非原始網域的 `Host` 標頭，這可能會干擾路由與驗證。

**重要**：Elastic Cloud 部署以及任何使用 `Host` 標頭路由的系統都需要此組態。如果此設定配置不當，請求將在 Elastic Cloud 中失敗並收到類似 `{"ok":false,"message":"Unknown resource."}` 的錯誤回應，或在其他系統中被錯誤路由。
{: .important}

若要設定 `Host` 標頭，請在您的 `cdk.context.json` 檔案中加入 `captureProxyExtraArgs` 參數：

```json
{
  "captureProxyExtraArgs": "--setHeader Host <domain-host-without-protocol>"
}
```
{% include copy.html %}

例如，如果您的 Elastic Cloud 網域為 `https://my-cluster.es.us-east-1.aws.example.com`，請如下設定 `captureProxyExtraArgs`：

```json
{
  "captureProxyExtraArgs": "--setHeader Host my-cluster.es.us-east-1.aws.example.com"
}
```
{% include copy.html %}

**提示**：`Host` 標頭值應只包含網域名稱，不含通訊協定（`https://`）或連接埠號碼。
{: .tip}

#### 驗證組態

在使用 Capture Proxy 路由正式環境流量之前，請直接向代理程式傳送測試請求，以驗證代理程式是否已正確設定。您可以使用 cURL 驗證連線：

```bash
curl -k https://<capture-proxy-endpoint>:9200/
```
{% include copy.html %}

如果 `Host` 標頭組態正確，您應該會收到來源叢集傳回的成功回應或驗證失敗回應。如果您收到類似 `{"ok":false,"message":"Unknown resource."}` 的錯誤，請確認：
- `captureProxyExtraArgs` 參數已在您的 `cdk.context.json` 中正確設定。
- `Host` 標頭值與您來源叢集的網域完全一致。
- 您在進行組態變更後已重新部署 Capture Proxy 服務。

{% include migration-phase-navigation.html %}
