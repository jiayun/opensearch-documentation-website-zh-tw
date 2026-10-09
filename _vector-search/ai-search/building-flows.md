---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定 AI 搜尋類型"
parent: Building AI search workflows in OpenSearch Dashboards
grand_parent: AI search
nav_order: 10
---

# 設定 AI 搜尋類型

本頁提供不同 AI 搜尋工作流程類型的範例組態。每個範例示範如何針對特定使用情境調整設定，例如語意搜尋或混合擷取。若要從頭到尾建立工作流程，請依照 [在 OpenSearch Dashboards 中建立 AI 搜尋工作流程]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflow-builder/) 中的步驟，並將您的使用情境組態套用到設定的適當部分。

## 必要條件：佈建機器學習資源

開始之前，請依據您的使用情境選取並佈建必要的機器學習 (ML) 資源。例如，若要實作語意搜尋，您必須在 OpenSearch 叢集中設定文字嵌入模型。有關在本機部署 ML 模型或連線至外部託管模型的更多資訊，請參閱 [整合 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/integrating-ml-models/)。

<details markdown="block">
<summary>
    目錄
</summary>
{: .text-delta }
1. TOC
{:toc}
</details>

<p id="implementation-examples"></p>

## 語意搜尋

此範例示範如何設定語意搜尋。

### ML 資源

建立並部署 [Amazon Bedrock 上的 Amazon Titan Text Embedding 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#amazon-bedrock-titan-text-embedding)。

### 索引

請確保索引設定包含 `index.knn: true`，且您的索引在對應中包含 `knn_vector` 欄位，如下所示：

```json
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "<embedding_field_name>": {
        "type": "knn_vector",
        "dimension": "<embedding_size>"
      }
    }
  }
}
```

{% include copy.html %}

### 資料匯入管線

設定單一 ML 推論處理器。將您的輸入文字對應到 `inputText` 模型輸入欄位。您可以選擇性地將輸出 `embedding` 對應到新的文件欄位。

### 搜尋管線

設定單一 ML 推論搜尋請求處理器。將包含輸入文字的查詢欄位對應到 `inputText` 模型輸入欄位。您可以選擇性地將輸出 `embedding` 對應到新欄位。覆寫查詢以包含 `knn` 查詢，例如：

```json
{
    "_source": {
        "excludes": [
            "<embedding_field>"
        ]
    },
    "query": {
        "knn": {
            "<embedding_field>": {
                "vector": ${embedding},
                "k": 10
            }
        }
    }
}
```

{% include copy.html %}

---

## 混合搜尋

混合搜尋結合關鍵字搜尋與向量搜尋。此範例示範如何設定混合搜尋。

### ML 資源

建立並部署 [Amazon Bedrock 上的 Amazon Titan Text Embedding 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#amazon-bedrock-titan-text-embedding)。

### 索引

請確保索引設定包含 `index.knn: true`，且您的索引在對應中包含 `knn_vector` 欄位，如下所示：

```json
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "<embedding_field_name>": {
        "type": "knn_vector",
        "dimension": "<embedding_size>"
      }
    }
  }
}
```

{% include copy.html %}

### 資料匯入管線

設定單一 ML 推論處理器。將您的輸入文字對應到 `inputText` 模型輸入欄位。您可以選擇性地將輸出 `embedding` 對應到新的文件欄位。

### 搜尋管線

設定一個 ML 推論搜尋請求處理器和一個標準化處理器。

**對於 ML 推論處理器**，將包含輸入文字的查詢欄位對應到 `inputText` 模型輸入欄位。您可以選擇性地將輸出 `embedding` 對應到新欄位。覆寫查詢使其包含 `hybrid` 查詢。請務必指定 `embedding_field`、`text_field` 和 `text_field_input`：

```json
{
    "_source": {
        "excludes": [
            "<embedding_field>"
        ]
    },
    "query": {
        "hybrid": {
            "queries": [
                {
                    "match": {
                        "<text_field>": {
                            "query": "<text_field_input>"
                        }
                    }
                },
                {
                    "knn": {
                        "<embedding_field>": {
                            "vector": ${embedding},
                            "k": 10
                        }
                    }
                }
            ]
        }
    }
}
```

{% include copy.html %}

**對於標準化處理器**，為每個子查詢設定權重。更多資訊請參閱 [混合搜尋標準化處理器範例]({{site.url}}{{site.baseurl}}/search-plugins/hybrid-search/#step-3-configure-a-search-pipeline)。

---

## 基本 RAG (文件摘要)

此範例示範如何設定基本檢索增強生成 (RAG)。

以下範例顯示 [Claude v1 messages API](https://docs.anthropic.com/en/api/messages) 的簡化連接器藍圖。雖然連接器藍圖和模型介面可能隨時間演進，但此範例示範如何將複雜的 API 互動抽象化為單一 `prompt` 欄位輸入。

範例輸入可能如下所示，其中預留位置代表動態擷取的結果：

```json
{
  "prompt": "Human: You are a professional data analyst. You are given a list of document results. You will analyze the data and generate a human-readable summary of the results. If you don't know the answer, just say I don't know.\n\n Results: ${parameters.results.toString()}\n\n Human: Please summarize the results.\n\n Assistant:"
}
```

### ML 資源

建立並部署 [Amazon Bedrock 上的 Anthropic Claude 3 Sonnet 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#claude-3-sonnet-hosted-on-amazon-bedrock)。

### 搜尋管線

依照下列步驟設定 ML 推論搜尋回應處理器：

1. 選取 **Template** 作為 `prompt` 輸入欄位的轉換類型。
2. 選取 **Configure** 以開啟範本組態。
3. 選擇預設範本以簡化設定。
4. 建立輸入變數以擷取評論清單 (例如 `review`)。
5. 複製該變數並貼到範本中，將其注入提示詞。
6. 選取 **Run preview** 以驗證轉換後的提示詞正確納入範例動態資料。
7. 選取 **Save** 以套用變更並結束。

---

## 多模態搜尋

多模態搜尋以文字和影像進行搜尋。此範例示範如何設定多模態搜尋。

### ML 資源

建立並部署 [Amazon Bedrock 上的 Amazon Titan Multimodal Embedding 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#amazon-bedrock-titan-multimodal-embedding)。

### 索引

請確保索引設定包含 `index.knn: true`，且您的索引在對應中包含 `knn_vector` 欄位 (用於保存產生的嵌入) 和 `binary` 欄位 (用於保存影像二進位資料)，如下所示：

```json
{
    "settings": {
        "index": {
            "knn": true
        }
    },
    "mappings": {
        "properties": {
            "image_base64": {
                "type": "binary"
            },
            "image_embedding": {
                "type": "knn_vector",
                "dimension": <dimension>
            }
        }
    }
}
```

{% include copy.html %}

### 資料匯入管線

設定單一 ML 推論處理器。將您的輸入文字欄位與輸入圖片欄位分別對應至 `inputText` 與 `inputImage` 模型輸入欄位。若同時需要文字與圖片輸入，請確保兩者皆已對應。或者，若單一輸入即足以產生嵌入，您也可以只對應其中一個輸入（文字或圖片）。

您也可以選擇將輸出 `embedding` 對應至新的文件欄位。

### 搜尋管線

設定單一 ML 推論搜尋請求處理器。將查詢中的輸入文字欄位與輸入圖片欄位分別對應至 `inputText` 與 `inputImage` 模型輸入欄位。若同時需要文字與圖片輸入，請確保兩者皆已對應。或者，若單一輸入即足以產生嵌入，您也可以只對應其中一個輸入（文字或圖片）。

覆寫查詢，使其包含 `knn` 查詢，並納入嵌入輸出：

```json
{
    "_source": {
        "excludes": [
            "<embedding_field>"
        ]
    },
    "query": {
        "knn": {
            "<embedding_field>": {
                "vector": ${embedding},
                "k": 10
            }
        }
    }
}
```

{% include copy.html %}

---

## 具名實體辨識

此範例示範如何設定具名實體辨識 (NER)。

### ML 資源

建立並部署 [Amazon Comprehend Entity Detection 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#amazon-comprehend---entity-detection)。

### 資料匯入管線

設定單一 ML 推論處理器。將您的輸入文字欄位對應至 `text` 模型輸入欄位。若要將辨識出的實體與每份文件一併保存，請轉換輸出（實體陣列）並將其儲存於 `entities_found` 欄位。請參考下列 `output_map` 設定：

```json
"output_map": [
    {
        "entities_found": "$.response.Entities[*].Type"
    }
],
```

{% include copy.html %}

此設定會將擷取出的實體對應至 `entities_found` 欄位，確保它們與每份文件一併儲存。

---

## 語言偵測與分類

下列範例示範如何設定語言偵測與分類。

### ML 資源

建立並部署 [Amazon Comprehend Language Detection 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#amazon-comprehend---language-detection)。

### 資料匯入管線

設定單一 ML 推論處理器。將您的輸入文字欄位對應至 `text` 模型輸入欄位。若要為每份文件儲存偵測到最相關或最可能的語言，請轉換輸出（語言陣列）並將其保存於 `detected_dominant_language` 欄位。請參考下列 `output_map` 設定：

```json
"output_map": [
    {
              "detected_dominant_language": "response.Languages[0].LanguageCode"
    }
],
```

{% include copy.html %}

---

## 重新排序結果

重新排序可依所用模型的能力，以多種方式實作。模型通常至少需要兩個輸入：原始查詢，以及要指派相關性分數的資料。有些模型支援批次處理，可在單次推論呼叫中處理多筆結果，而其他模型則需要逐一為每筆結果評分。

在 OpenSearch 中，這會產生兩種常見的重新排序模式：

1. **已啟用批次處理**

   1. 收集所有搜尋結果。
   1. 將批次結果傳遞至單一 ML 處理器進行評分。
   1. 傳回排名前 **n** 的結果。

2. **已停用批次處理**
   1. 收集所有搜尋結果。
   1. 將每筆結果傳遞至 ML 處理器，以指派新的相關性分數。
   1. 將所有已更新分數的結果傳送至重新排序處理器進行排序。
   1. 傳回排名前 **n** 的結果。

下列範例示範 **模式 2（已停用批次處理）**，以突顯重新排序處理器。不過請注意，此範例所使用的 **Cohere Rerank** 模型**確實支援批次處理**，因此您也可以使用此模型實作**模式 1**。

### ML 資源

建立並部署 [Cohere Rerank 模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#cohere-rerank)。

### 搜尋管線

設定 ML 推論**搜尋回應**處理器，接著設定重新排序**搜尋回應**處理器。若要在停用批次處理的情況下進行重新排序，請使用 ML 處理器為擷取到的結果產生新的相關性分數，然後套用重新排序器據以排序。

請使用下列 ML 處理器設定：

1. 將包含要用於比較之資料的文件欄位對應至模型的 `documents` 欄位。
2. 將原始查詢對應至模型的 `query` 欄位。
3. 使用 JSONPath 存取查詢 JSON，並在前面加上 `_request.query`。

請參考下列 `input_map` 設定：

```json
"input_map": [
   {
      "documents": "description",
      "query": "$._request.query.term.value"
   }
],
```

{% include copy.html %}

您也可以選擇將模型輸出中重新評分後的結果儲存於新欄位。您也可以只擷取並保存相關性分數，如下所示：

```json
"input_map": [
   {
      "new_score": "results[0].relevance_score"
   }
],
```

{% include copy.html %}

請使用下列重新排序處理器設定：在 **target_field** 下，選取模型分數欄位（在此範例中為 `new_score`）。

---

## 使用自訂 CLIP 模型進行多模態搜尋（文字或圖片）

下列範例使用託管於 Amazon SageMaker 的自訂 CLIP 模型。此模型會動態匯入文字或圖片 URL 作為輸入，並傳回向量嵌入。

### ML 資源

建立並部署 [自訂 CLIP 多模態模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#custom-clip-multimodal-embedding)。

### 索引

請確保索引設定包含 `index.knn: true`，且您的索引在對應中包含 `knn_vector` 欄位，如下所示：

```json
{
  "settings": {
    "index": {
      "knn": true
    }
  },
  "mappings": {
    "properties": {
      "<embedding_field_name>": {
        "type": "knn_vector",
        "dimension": "<embedding_size>"
      }
    }
  }
}
```

{% include copy.html %}

### 資料匯入管線

設定單一 ML 推論處理器。視您匯入並保存於索引中的資料類型而定，將您的圖片欄位對應至 `image_url` 模型輸入欄位，或將您的文字欄位對應至 `text` 模型輸入欄位。例如，若您要建置可依據文字或圖片輸入傳回相關圖片的應用程式，您將需要保存圖片，並應將圖片欄位對應至 `image_url` 欄位。

### 搜尋管線

設定單一 ML 推論搜尋請求處理器。將查詢中的輸入圖片欄位或輸入文字欄位分別對應至 `image_url` 或 `text` 模型輸入欄位。CLIP 模型可靈活處理其中任一者，因此請選擇最適合您使用案例的選項。

覆寫查詢，使其包含 `knn` 查詢，並納入嵌入輸出：

```json
{
    "_source": {
        "excludes": [
            "<embedding_field>"
        ]
    },
    "query": {
        "knn": {
            "<embedding_field>": {
                "vector": ${embedding},
                "k": 10
            }
        }
    }
}
```

{% include copy.html %}


---

## 神經稀疏搜尋

此範例示範如何設定神經稀疏搜尋。

### 機器學習資源

建立並部署[神經稀疏編碼模型](https://github.com/opensearch-project/dashboards-flow-framework/blob/main/documentation/models.md#neural-sparse-encoding)。

### 索引

確保索引對應包含 `rank_features` 欄位：

```
"<embedding_field_name>": {
    "type": "rank_features"
}
```
{% include copy.html %}

### 資料匯入管線

設定單一機器學習推論處理器。將您的輸入文字對應至 `text_doc` 模型輸入欄位。您也可以選擇將輸出 `response` 對應至新的文件欄位。如有需要，使用 JSONPath 運算式轉換回應。 


### 搜尋管線

設定單一機器學習推論搜尋請求處理器。將包含輸入文字的查詢欄位對應至 `text_doc` 模型輸入欄位。您也可以選擇將輸出 `response` 對應至新欄位。如有需要，使用 JSONPath 運算式轉換回應。加入神經稀疏查詢：

```
{
    "_source": {
        "excludes": [
            "<embedding_field>"
        ]
    },
    "query": {
        "neural_sparse": {
            "<embedding_field>": {
                "query_tokens": ${response},
            }
        }
    }
}
```
{% include copy.html %}