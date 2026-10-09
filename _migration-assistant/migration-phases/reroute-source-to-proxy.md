---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將用戶端流量重新導向至擷取 Proxy"
nav_order: 30
parent: Migration workflows
permalink: /migration-assistant/migration-phases/reroute-source-to-proxy/
---

# 將用戶端流量重新導向至擷取 Proxy

以下資訊僅適用於使用「擷取與重播」(Capture and Replay) 的零停機遷移。
{: .note }

若您想保留遷移期間發生的寫入，擷取必須在快照回填之前啟動。

## 工作流程建立的資源

當您的工作流程包含 `traffic.proxies` 區段時，Migration Assistant 會建立：

- 擷取 Proxy Pod。
- 位於這些 Pod 前方的 Kubernetes Service 資源。
- Apache Kafka 組態，以便日後重播所擷取的流量。

用戶端流量會傳送至 Proxy 的 Kubernetes Service。Proxy 會將請求轉送至來源叢集，並記錄這些請求以供日後重播。

## Kubernetes 與 EKS 的比較

遷移引擎在 Kubernetes 與 Amazon Elastic Kubernetes Service (EKS) 兩個平台上皆相同。實務上的差異在於 Kubernetes Service 的暴露方式，以及如何整合至您的環境：

- 在**一般 Kubernetes** 上，您需提供將用戶端路由至 Proxy Kubernetes Service 的網路模式。
- 在 **Amazon EKS** 上，Kubernetes Service 可由 AWS 負載平衡器基礎架構支援，且啟動路徑會自動化更多平台組態。

## 在工作流程中設定 Proxy

請一律從目前的範例開始：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

在 Proxy 組態中，重要欄位包括：

- `listenPort`
- `podReplicas`
- 當您需要在 EKS 上對外暴露時，使用 `internetFacing`。
- `tls`
- `setHeader`

## TLS 行為

Proxy 預設為安全。若您未明確設定 TLS，工作流程會為 Proxy 佈建自簽憑證。

若您刻意想使用純文字 HTTP，請將 Proxy TLS 模式設為 `plaintext`。

## 主機與標頭覆寫

若您的來源使用以主機為基礎的路由，請在 Proxy 組態中新增靜態標頭。

使用 `setHeader` 欄位並以 `Header-Name: value` 格式提供項目，例如：

```json
{
  "setHeader": ["Host: source.example.com"]
}
```
{% include copy.html %}

## 尋找 Proxy 端點

提交工作流程後，請檢查 `ma` 命名空間中的 Service，並找出為 Proxy 建立的那一個：

```bash
kubectl get svc -n ma
```
{% include copy.html %}

接著更新您的應用程式、DNS 或負載平衡器，將流量改為傳送至該 Proxy 端點，而非直接傳送至來源。

## 繼續之前先驗證擷取

在您繼續進行中繼資料遷移與回填之前，請確認：

- Proxy Pod 正在執行。
- Kubernetes Service 可連線。
- 應用程式流量正流經 Proxy。
- 工作流程顯示流量元件狀態良好。

實用命令：

```bash
workflow status
workflow manage
```
{% include copy.html %}

## 後續步驟

擷取上線後，請在執行下列步驟期間讓流量持續流經 Proxy：

1. 遷移中繼資料
2. 回填歷史文件
3. 重播所擷取的流量，讓目標趕上進度

{% include migration-phase-navigation.html %}
