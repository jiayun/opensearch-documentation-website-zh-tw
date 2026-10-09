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

_資料匯入管線_ (ingest pipeline) 是一連串的_處理器_ (processor)，在文件匯入索引時套用於文件。管線中的每個[處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)執行特定任務，例如篩選、轉換或充實資料。

處理器是可自訂的任務，依照請求本文中出現的順序依序執行。此順序非常重要，因為每個處理器都依賴前一個處理器的輸出。處理器套用完成後，修改過的文件就會出現在您的索引中。

## OpenSearch 資料匯入管線與 Data Prepper 的比較

OpenSearch 資料匯入管線在 OpenSearch 叢集內執行，而 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 則是在 OpenSearch 叢集上執行的外部元件。

OpenSearch 資料匯入管線對索引執行動作，適合用於簡單資料集的預先處理、[機器學習 (ML) 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/sparse-encoding/)以及[向量嵌入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/text-image-embedding/)等使用情境。建議在簡單的資料預先處理和小型資料集使用 OpenSearch 資料匯入管線。

Data Prepper 則建議用於其支援的任何資料處理任務，尤其是處理大型資料集和複雜的資料預先處理需求時。它能簡化大型資料集的傳輸與擷取流程，同時提供強大的功能來執行複雜的資料準備與轉換作業。如需更多資訊，請參閱 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/) 文件。

OpenSearch 資料匯入管線只能透過 [Ingest API 操作]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/index/)來管理。
{: .note}

## 必要條件

以下是使用 OpenSearch 資料匯入管線的必要條件：

- 在正式環境中使用匯入功能時，您的叢集應至少包含一個節點角色權限設定為 `ingest` 的節點。如需在叢集內設定節點角色的相關資訊，請參閱 [叢集形成]({{site.url}}{{site.baseurl}}/opensearch/cluster/)。
- 若已啟用 OpenSearch Security 外掛程式，您必須具備 `cluster_manage_pipelines` 權限才能管理資料匯入管線。

## 定義管線

_管線定義_ (pipeline definition) 描述資料匯入管線的順序，可以使用 JSON 格式撰寫。資料匯入管線包含下列項目：

```json
{
    "description" : "..."
    "processors" : [...]
}
```

#### 請求本文欄位

欄位 | 必要性 | 類型 | 說明
:--- | :--- | :--- | :---
`processors` | 必要 | 處理器物件的陣列 | 在資料匯入 OpenSearch 時執行特定資料處理任務的元件。
`description` | 選用 | 字串 | 資料匯入管線的描述。

## 後續步驟

了解如何：

- [建立管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/)。
- [測試管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/simulate-ingest/)。
- [擷取管線資訊]({{site.url}}{{site.baseurl}}/ingest-pipelines/get-ingest/)。
- [刪除管線]({{site.url}}{{site.baseurl}}/ingest-pipelines/delete-ingest/)。
- [在 OpenSearch 中使用匯入處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/index-processors/)
- [使用條件式執行]({{site.url}}{{site.baseurl}}/ingest-pipelines/conditional-execution/)
