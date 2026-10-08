---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: download
nav_order: 30
parent: Command reference
grand_parent: Reference
redirect_from:
  - /benchmark/commands/download/
---

<!-- vale off -->
# download 命令
<!-- vale on -->

使用 `download` 命令來選擇要下載的 OpenSearch 發行版本。

## 使用方式

下列範例會下載 OpenSearch 2.7.0 版：

```
opensearch-benchmark download --distribution-version=2.7.0
```

接著 Benchmark 會傳回 OpenSearch 產製品的位置：

```
{
  "opensearch": "/Users/.benchmark/benchmarks/distributions/opensearch-2.7.0.tar.gz"
}
```

## 選項

使用下列選項來自訂 OpenSearch Benchmark 下載 OpenSearch 的方式：

- `--cluster-config-repository`：定義 OpenSearch Benchmark 從中載入 `cluster-configs` 與 `cluster-config-instances` 的儲存庫。
- `--cluster-config-revision`：定義 OpenSearch Benchmark 應在 `cluster-config` 中使用的特定 Git 修訂版本。
- `--cluster-config-path`：定義 `--cluster-config-instance` 的路徑，以及要使用的任何 OpenSearch 外掛程式組態。
- `--distribution-version`：根據版本編號下載指定的 OpenSearch 發行版。如需已發行 OpenSearch 版本的清單，請參閱[版本歷程]({{site.url}}{{site.latesturl}}/version-history/)。
- `--distribution-repository`：定義應從中下載 OpenSearch 發行版的儲存庫。預設為 `release`。
- `--cluster-config-instance`：定義要使用的 `--cluster-config-instance`。您可以使用 `opensearch-benchmark list cluster-config-instances` 命令來檢視可能的組態執行個體。
- `--cluster-config-instance-params`：以逗號分隔的索引鍵-值組清單，會逐字插入作為 `cluster-config-instance` 的變數。
- `--target-os`：應下載 OpenSearch 產製品的目標作業系統。預設為目前的作業系統。
- `--target-arch`：應下載產製品的 CPU 架構名稱。
