---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "選擇工作負載"
nav_order: 15
redirect_from:
  - /benchmark/user-guide/understanding-workloads/choosing-a-workload/
---

# 選擇工作負載

[`opensearch-benchmark-workloads`](https://github.com/opensearch-project/opensearch-benchmark-workloads) 儲存庫包含可用於執行基準測試的工作負載清單。使用與您叢集使用案例相似的工作負載，可在評估叢集效能時節省時間與精力。 

例如，假設您是共乘公司的系統架構師。身為共乘公司，您會收集並儲存行程時間、地點，以及與每趟共乘行程相關的其他資料。建立自訂工作負載並使用您自己的資料需要額外的時間、精力與成本，因此您可以使用 [nyc_taxis](https://github.com/opensearch-project/opensearch-benchmark-workloads/tree/main/nyc_taxis) 工作負載對叢集進行基準測試，因為此工作負載中的資料與您收集的資料相似。 

## 選擇工作負載的準則

決定哪個工作負載最適合用於叢集基準測試時，請考量下列準則：

- 叢集的使用案例與規模。小型叢集通常包含 1--10 個節點，適合開發環境。中型叢集通常包含 11--50 個節點，用於更接近正式環境叢集的測試環境。 
- 叢集使用的資料類型與工作負載中文件的資料結構之間的比較。每個工作負載都包含一份範例文件，供您比較資料類型，您也可以在 `index.json` 檔案中檢視索引對應與資料類型。
- 叢集中最常使用的查詢類型。`operations/default.json` 檔案包含查詢類型與工作負載操作的相關資訊。如需常見操作清單，請參閱[常見操作]({{site.url}}{{site.baseurl}}/benchmark/common-operations/)。

## 後續步驟

- 如需各個預先封裝工作負載的資料、叢集需求與查詢類型，請參閱[工作負載類型]({{site.url}}{{site.baseurl}}/benchmark/workload-types/)。
- 如果您找不到符合需求的官方工作負載，可以建立自訂工作負載。如需詳細資訊，請參閱[建立自訂工作負載]({{site.url}}{{site.baseurl}}/benchmark/creating-custom-workloads/)。
