---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行分散式負載"
nav_order: 32
redirect_from:
  - /benchmark/user-guide/optimizing-benchmarks/distributed-load/
  - /benchmark/user-guide/distributed-load/
---

# 執行分散式負載

OpenSearch Benchmark 負載一律在啟動基準測試的同一部機器上執行。不過，您可以使用多個負載驅動程式來產生額外的基準測試負載，特別適用於分布在多部機器上的大型叢集。本教學說明如何將基準測試負載分散到單一叢集中的多部機器上。

## 系統架構

以下教學使用三節點架構，每個節點皆在 [Amazon Elastic Compute Cloud (Amazon EC2)](https://docs.aws.amazon.com/ec2/?nc2=h_ql_doc_ec2) 中產生：

- **Node 1**：Node 1 擔任_協調節點_，負責啟用其他兩個節點之間的分配與通訊。
- **Node 2** 與 **Node 3**：叢集中其餘的節點用於產生基準測試的負載。

所有節點都必須安裝 OpenSearch Benchmark。如需安裝說明，請參閱[安裝 OpenSearch Benchmark]({{site.url}}{{site.baseurl}}/benchmark/user-guide/installing-benchmark/)。

請記下每個節點的 IP 位址。本教學使用下列 IP 位址：

- **Node 1 -- 協調節點**：192.0.1.0
- **Node 2 -- 工作節點**：198.52.100.0
- **Node 3 -- 工作節點**：198.53.100.0

## 步驟 1：啟用節點通訊

請務必為每個節點啟用通訊。在 AWS Management Console 中：

1. 前往該節點的 EC2 主機。
2. 選取 **Security**，然後選取與該節點相關聯的安全性群組。
3. 根據叢集的連接埠範圍與流量類型，使用 **Add inbound rules** 開放流向該節點的流量。

## 步驟 2：在每個節點上執行常駐程式

在每個節點上啟動 OpenSearch Benchmark，先使用 `--node-ip` 在節點本身初始化 OpenSearch Benchmark，再使用 `--coordinator-ip` 將每個節點連線至協調節點。

對於 **Node 1**，下列命令會將該節點識別為協調節點：

```
opensearch-benchmarkd start --node-ip=192.0.1.0 --coordinator-ip=192.0.1.0
```

下列命令可讓 **Node 2** 與 **Node 3** 監聽協調節點傳來的負載產生指示。

**Node 2**

```
opensearch-benchmarkd start --node-ip=198.52.100.0 --coordinator-ip=192.0.1.0
```

**Node 3**

```
opensearch-benchmarkd start --node-ip=198.53.100.0 --coordinator-ip=192.0.1.0
```

當三個節點上都在執行 OpenSearch Benchmark，且工作節點已設定為監聽協調節點後，您就可以執行基準測試了。

## 步驟 3：執行基準測試

在 **Node 1** 上執行基準測試，並將 `worker-ips` 設為工作節點的 IP 位址，如下列範例所示：

```
opensearch-benchmark run --pipeline=benchmark-only --workload=eventdata --worker-ips=198.52.100.0,198.53.100.0 --target-hosts=<DOMAIN_ENDPOINT> --client-options=<STANDARD_CLIENT_OPTIONS> --kill-running-processes
```

測試完成後，測試所產生的記錄檔會出現在您的工作節點上。

