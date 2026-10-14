---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資料匯入管線"
nav_order: 5
nav_exclude: true
has_toc: true
permalink: /ingest-pipelines/
redirect_from:
   - /api-reference/ingest-apis/ingest-pipelines/
   - /ingest-pipelines/index/
---

# 資料匯入管線

_資料匯入管線_ 是一連串的 _處理器_，會在文件匯入索引時套用至文件。管線中的每個[處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)會執行特定工作，例如篩選、轉換或擴充資料。

處理器是可自訂的工作，會依其在請求本文中出現的順序依序執行。這個順序很重要，因為每個處理器都取決於前一個處理器的輸出。套用處理器之後，修改過的文件會出現在您的索引中。

## OpenSearch 資料匯入管線與 Data Prepper 的比較

OpenSearch 資料匯入管線在 OpenSearch 叢集內執行，而 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 是在 OpenSearch 叢集上執行的外部元件。

OpenSearch 資料匯入管線會對索引執行動作，較適合用於涉及預先處理簡單資料集、[機器學習 (ML) 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/) 及[向量嵌入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-image-embedding/) 的使用案例。建議將 OpenSearch 資料匯入管線用於簡單的資料預先處理及小型資料集。

建議將 Data Prepper 用於其支援的任何資料處理工作，尤其是在處理大型資料集及複雜的資料預先處理需求時。它可簡化傳輸及擷取大型資料集的流程，同時為複雜的資料準備與轉換作業提供強大的功能。如需更多資訊，請參閱 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 文件。

OpenSearch 資料匯入管線只能使用 [Ingest API 操作]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/) 來管理。
{: .note}

## 先決條件

以下是使用 OpenSearch 資料匯入管線的先決條件：

- 在生產環境中使用匯入時，您的叢集應至少包含一個節點角色權限設為 `ingest` 的節點。如需在叢集中設定節點角色的相關資訊，請參閱[叢集形成]({{site.url}}{{site.baseurl}}/opensearch/cluster/)。
- 如果已啟用 OpenSearch Security 外掛程式，您必須具備 `cluster_manage_pipelines` 權限才能管理資料匯入管線。

## 定義管線

_管線定義_ 描述資料匯入管線的順序，並可以 JSON 格式撰寫。資料匯入管線包含下列項目：

```json
{
    "description" : "..."
    "processors" : [...]
}
```

#### 請求本文欄位

欄位 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`processors` | 必要 | 處理器物件陣列 | 在資料匯入 OpenSearch 時執行特定資料處理工作的元件。
`description` | 選用 | 字串 | 資料匯入管線的說明。

管線定義會儲存在叢集狀態中。當您將 `include_global_state` 設為 `true` 來建立快照時，快照會包含這些定義。如需更多資訊，請參閱[全域叢集狀態]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#global-cluster-state)。

## 後續步驟

了解如何：

- [建立管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/)。
- [測試管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/simulate-ingest/)。
- [擷取管線的相關資訊]({{site.url}}{{site.baseurl}}/ingest-pipelines/get-ingest/)。
- [刪除管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/delete-ingest/)。
- [在 OpenSearch 中使用匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)
- [使用條件式執行]({{site.url}}{{site.baseurl}}/ingest-pipelines/conditional-execution/)
