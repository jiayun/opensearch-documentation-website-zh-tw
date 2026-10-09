---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "預訓練模型"
parent: Using ML models within OpenSearch
grand_parent: Integrating ML models
nav_order: 10
---

# OpenSearch 提供的預訓練模型
**於 2.9 版引入**
{: .label .label-purple }

OpenSearch 提供多種開放原始碼的預訓練模型，可協助處理各種機器學習 (ML) 搜尋與分析使用案例。您可以將任何支援的模型上傳至 OpenSearch 叢集，並在本機使用。

## 支援的預訓練模型

OpenSearch 支援下列模型，並依類型分類。文字嵌入模型來自 [Hugging Face](https://huggingface.co/)。稀疏編碼模型由 OpenSearch 訓練。雖然相同類型的模型會有類似的使用案例，但每個模型的模型大小不同，且會依您的叢集設定而有不同的效能表現。如需部分預訓練模型的效能比較，請參閱 [SBERT 文件](https://www.sbert.net/docs/pretrained_models.html#model-overview)。

不支援在 CentOS 7 作業系統上執行本機模型。此外，並非所有本機模型都能在所有硬體和作業系統上執行。
{: .important}

### 句子轉換器

句子轉換器模型會將句子和段落對應至多維的密集向量空間。向量數量取決於模型類型。您可以將這些模型用於分群或語意搜尋等使用案例。

下表列出句子轉換器模型，以及可用於下載這些模型的成品連結。請注意，您必須在模型名稱前加上 `huggingface/` 前綴，如 **Model name** 欄所示。

**詞元限制與截斷**：文字嵌入模型有最大詞元數限制 (以 BERT 為基礎的模型通常為 512 個詞元)。當文件超過此限制時，模型會自動截斷文字，而被截斷的內容不會呈現在嵌入中。這可能會大幅影響搜尋相關性，因為如果相關內容遭到截斷，文件可能不會出現在搜尋結果中。為避免此問題，請在產生嵌入之前，先將長文件分割成較小的區塊。
{: .warning}

| 模型名稱 | 版本 | 向量維度 | 自動截斷 | TorchScript 成品 | ONNX 成品 |
|:---|:---|:---|:---|:---|:---|
| `huggingface/sentence-transformers/all-distilroberta-v1` | 1.0.2 | 768 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-distilroberta-v1/1.0.2/torch_script/sentence-transformers_all-distilroberta-v1-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-distilroberta-v1/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-distilroberta-v1/1.0.2/onnx/sentence-transformers_all-distilroberta-v1-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-distilroberta-v1/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/all-MiniLM-L6-v2` | 1.0.2 | 384 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L6-v2/1.0.2/torch_script/sentence-transformers_all-MiniLM-L6-v2-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L6-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L6-v2/1.0.2/onnx/sentence-transformers_all-MiniLM-L6-v2-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L6-v2/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/all-MiniLM-L12-v2` | 1.0.2 | 384 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L12-v2/1.0.2/torch_script/sentence-transformers_all-MiniLM-L12-v2-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L12-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L12-v2/1.0.2/onnx/sentence-transformers_all-MiniLM-L12-v2-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-MiniLM-L12-v2/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/all-mpnet-base-v2` | 1.0.2 | 768 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-mpnet-base-v2/1.0.2/torch_script/sentence-transformers_all-mpnet-base-v2-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-mpnet-base-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-mpnet-base-v2/1.0.2/onnx/sentence-transformers_all-mpnet-base-v2-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/all-mpnet-base-v2/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/msmarco-distilbert-base-tas-b` | 1.0.3 | 768 維密集向量空間。針對語意搜尋最佳化。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/msmarco-distilbert-base-tas-b/1.0.3/torch_script/sentence-transformers_msmarco-distilbert-base-tas-b-1.0.3-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/msmarco-distilbert-base-tas-b/1.0.3/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/msmarco-distilbert-base-tas-b/1.0.3/onnx/sentence-transformers_msmarco-distilbert-base-tas-b-1.0.3-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/msmarco-distilbert-base-tas-b/1.0.3/onnx/config.json) |
| `huggingface/sentence-transformers/multi-qa-MiniLM-L6-cos-v1` | 1.0.2 | 384 維密集向量空間。專為語意搜尋設計，並以 2.15 億組問答配對訓練。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-MiniLM-L6-cos-v1/1.0.2/torch_script/sentence-transformers_multi-qa-MiniLM-L6-cos-v1-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-MiniLM-L6-cos-v1/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-MiniLM-L6-cos-v1/1.0.2/onnx/sentence-transformers_multi-qa-MiniLM-L6-cos-v1-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-MiniLM-L6-cos-v1/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/multi-qa-mpnet-base-dot-v1` | 1.0.2 | 768 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-mpnet-base-dot-v1/1.0.2/torch_script/sentence-transformers_multi-qa-mpnet-base-dot-v1-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-mpnet-base-dot-v1/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-mpnet-base-dot-v1/1.0.2/onnx/sentence-transformers_multi-qa-mpnet-base-dot-v1-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/multi-qa-mpnet-base-dot-v1/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2` | 1.0.2 | 384 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2/1.0.2/torch_script/sentence-transformers_paraphrase-MiniLM-L3-v2-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2/1.0.2/onnx/sentence-transformers_paraphrase-MiniLM-L3-v2-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-MiniLM-L3-v2/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | 1.0.2 | 384 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/1.0.2/torch_script/sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/1.0.2/onnx/sentence-transformers_paraphrase-multilingual-MiniLM-L12-v2-1.0.2-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2/1.0.2/onnx/config.json) |
| `huggingface/sentence-transformers/paraphrase-mpnet-base-v2` | 1.0.1 | 768 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-mpnet-base-v2/1.0.1/torch_script/sentence-transformers_paraphrase-mpnet-base-v2-1.0.1-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-mpnet-base-v2/1.0.1/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-mpnet-base-v2/1.0.1/onnx/sentence-transformers_paraphrase-mpnet-base-v2-1.0.1-onnx.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/paraphrase-mpnet-base-v2/1.0.1/onnx/config.json) |
| `huggingface/sentence-transformers/distiluse-base-multilingual-cased-v1` | 1.0.2 | 512 維密集向量空間。 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/distiluse-base-multilingual-cased-v1/1.0.2/torch_script/sentence-transformers_distiluse-base-multilingual-cased-v1-1.0.2-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/sentence-transformers/distiluse-base-multilingual-cased-v1/1.0.2/torch_script/config.json) | 無法使用 |


### 稀疏編碼模型
**於 2.11 版導入**
{: .label .label-purple }

稀疏編碼模型會將文字轉換為稀疏向量，並將該向量轉換為 `<token: weight>` 成對清單，代表文字項目及其在稀疏向量中對應的權重。您可以在分群或稀疏神經搜尋等使用情境中使用這些模型。

為獲得最佳效能，我們建議以下組合：

- 在匯入與搜尋時都使用 `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill` 模型。
- 在匯入時使用 `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte` 模型，並在搜尋時使用
`amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1` 斷詞器。

`amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill` 與 `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte` 都以最大值比例 0.1 進行剪枝，在檢索效能與索引大小之間提供更佳的權衡。

如需執行神經稀疏搜尋之上述選項的更多資訊，請參閱[自動產生稀疏向量嵌入]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-with-pipelines/)。

下表列出稀疏編碼模型，以及可用以下載這些模型的成品連結。

| 模型名稱 | 版本 | 自動截斷 | TorchScript 成品 | 說明 |
|:---|:---|:---|:---|:---|
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-v1` | 1.0.1 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-v1/1.0.1/torch_script/neural-sparse_opensearch-neural-sparse-encoding-v1-1.0.1-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-v1/1.0.1/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-v1)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-encoding-v2-distill-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-v2-distill/1.0.0/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-v2-distill)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v1` | 1.0.1 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v1/1.0.1/torch_script/neural-sparse_opensearch-neural-sparse-encoding-doc-v1-1.0.1-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v1/1.0.1/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v1)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-distill` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-distill/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-encoding-doc-v2-distill-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-distill/1.0.0/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v2-distill)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-mini` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-mini/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-encoding-doc-v2-mini-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v2-mini/1.0.0/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v2-mini)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-encoding-doc-v3-distill-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-distill/1.0.0/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v3-distill)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-encoding-doc-v3-gte-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-doc-v3-gte/1.0.0/torch_script/config.json) | 神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-doc-v3-gte)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-encoding-multilingual-v1` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-multilingual-v1/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-encoding-multilingual-v1-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-encoding-multilingual-v1/1.0.0/torch_script/config.json) | 多語言神經稀疏編碼模型。此模型將文字轉換為稀疏向量，識別向量中非零元素的索引，然後將向量轉換為 `<entry, weight>` 成對結構，其中每個項目對應一個非零元素索引。若要使用 transformers 與 PyTorch API 實驗此模型，請參閱 [Hugging Face 文件](https://huggingface.co/opensearch-project/opensearch-neural-sparse-encoding-multilingual-v1)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1` | 1.0.1 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1/1.0.1/torch_script/neural-sparse_opensearch-neural-sparse-tokenizer-v1-1.0.1-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-tokenizer-v1/1.0.1/torch_script/config.json) | 神經稀疏斷詞器。此斷詞器將文字拆分為詞元，並為每個詞元指派預先定義的權重，即該詞元的反向文件頻率 (IDF)。若未提供 IDF 檔案，權重預設為 1。如需更多資訊，請參閱[準備模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/#preparing-a-model)。 |
| `amazon/neural-sparse/opensearch-neural-sparse-tokenizer-multilingual-v1` | 1.0.0 | 是 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-tokenizer-multilingual-v1/1.0.0/torch_script/neural-sparse_opensearch-neural-sparse-tokenizer-multilingual-v1-1.0.0-torch_script.zip)<br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/neural-sparse/opensearch-neural-sparse-tokenizer-multilingual-v1/1.0.0/torch_script/config.json) | 多語言神經稀疏斷詞器。此斷詞器將文字拆分為詞元，並為每個詞元指派預先定義的權重，即該詞元的反向文件頻率 (IDF)。若未提供 IDF 檔案，權重預設為 1。如需更多資訊，請參閱[準備模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/custom-local-models/#preparing-a-model)。 |

### 交叉編碼器模型
**2.12 版新增**
{: .label .label-purple }

交叉編碼器模型支援查詢重新排序。

下表列出交叉編碼器模型及其可用於下載的成品連結。請注意，模型名稱必須加上 `huggingface/cross-encoders` 前綴，如 **Model name** 欄所示。

| 模型名稱 | 版本 | TorchScript 成品 | ONNX 成品 |
|:---|:---|:---|:---|
| `huggingface/cross-encoders/ms-marco-MiniLM-L-6-v2` | 1.0.2 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-6-v2/1.0.2/torch_script/cross-encoders_ms-marco-MiniLM-L-6-v2-1.0.2-torch_script.zip) <br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-6-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-6-v2/1.0.2/onnx/cross-encoders_ms-marco-MiniLM-L-6-v2-1.0.2-onnx.zip) <br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-6-v2/1.0.2/onnx/config.json) |
| `huggingface/cross-encoders/ms-marco-MiniLM-L-12-v2` | 1.0.2 | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-12-v2/1.0.2/torch_script/cross-encoders_ms-marco-MiniLM-L-12-v2-1.0.2-torch_script.zip) <br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-12-v2/1.0.2/torch_script/config.json) | - [model_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-12-v2/1.0.2/onnx/cross-encoders_ms-marco-MiniLM-L-12-v2-1.0.2-onnx.zip) <br>- [config_url](https://artifacts.opensearch.org/models/ml-models/huggingface/cross-encoders/ms-marco-MiniLM-L-12-v2/1.0.2/onnx/config.json)

### 語意句子醒目提示模型
**3.0 版新增**
{: .label .label-purple }

語意句子醒目提示模型專為搭配 [`semantic` 醒目提示器]({{site.url}}{{site.baseurl}}/search-plugins/searching-data/highlight/#the-semantic-highlighter)而設計。這些模型會分析文件文字，並找出與搜尋查詢語意最相關的句子。

如需搭配語意醒目提示器使用這些模型的教學，請參閱[使用語意醒目提示]({{site.url}}{{site.baseurl}}/tutorials/vector-search/semantic-highlighting-tutorial/)。

下表列出語意句子醒目提示模型及其可用於下載的成品連結。請注意，模型名稱必須加上 `opensearch/` 前綴，如 **Model name** 欄所示。

| 模型名稱 | 版本 | TorchScript 成品 | 說明 |
|:---|:---|:---|:---|
| `amazon/sentence-highlighting/opensearch-semantic-highlighter-v1` | 1.0.0 | - [model_url](https://artifacts.opensearch.org/models/ml-models/amazon/sentence-highlighting/opensearch-semantic-highlighter-v1/1.0.0/torch_script/sentence-highlighting_opensearch-semantic-highlighter-v1-1.0.0-torch_script.zip) <br>- [config_url](https://artifacts.opensearch.org/models/ml-models/amazon/sentence-highlighting/opensearch-semantic-highlighter-v1/1.0.0/torch_script/config.json) | 專為找出需醒目提示的語意相關句子而最佳化的模型。 |


## 必要條件

在配備專屬 ML 節點的叢集上，請指定 `"only_run_on_ml_node": "true"` 以提升效能。如需更多資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

此範例使用不含專屬 ML 節點的簡單組態，並允許在非 ML 節點上執行模型。為確保此基本本機組態可正常運作，請指定以下叢集設定：

```json
PUT _cluster/settings
{
  "persistent": {
    "plugins.ml_commons.only_run_on_ml_node": "false",
    "plugins.ml_commons.model_access_control_enabled": "true",
    "plugins.ml_commons.native_memory_threshold": "99"
  }
}
```
{% include copy-curl.html %}

## 步驟 1：註冊模型群組

若要註冊模型，您有以下選項：

- 您可以使用 `model_group_id` 將模型版本註冊到現有的模型群組。
- 若不使用 `model_group_id`，ML Commons 會以新的模型群組建立模型。

若要註冊模型群組，請傳送以下請求：

```json
POST /_plugins/_ml/model_groups/_register
{
  "name": "local_model_group",
  "description": "A model group for local models"
}
```
{% include copy-curl.html %}

回應包含模型群組 ID，您將使用該 ID 將模型註冊到此模型群組：

```json
{
 "model_group_id": "wlcnb4kBJ1eYAeTMHlV6",
 "status": "CREATED"
}
```

若要進一步了解模型群組，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。

## 步驟 2：註冊 OpenSearch 提供的本機模型

若要將 OpenSearch 提供的模型註冊到步驟 1 建立的模型群組，請在以下請求中提供步驟 1 的模型群組 ID。

由於預先訓練模型來自 ML Commons 模型儲存庫，您只需在註冊 API 請求中提供 `name`、`version`、`model_group_id` 和 `model_format`：

```json
POST /_plugins/_ml/models/_register
{
  "name": "huggingface/sentence-transformers/msmarco-distilbert-base-tas-b",
  "version": "1.0.3",
  "model_group_id": "Z1eQf4oB5Vm0Tdw8EIP2",
  "model_format": "TORCH_SCRIPT"
}
```
{% include copy-curl.html %}

OpenSearch 會傳回註冊作業的任務 ID：

```json
{
  "task_id": "cVeMb4kBJ1eYAeTMFFgj",
  "status": "CREATED"
}
```

若要檢查作業狀態，請將任務 ID 提供給 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/)：

```bash
GET /_plugins/_ml/tasks/cVeMb4kBJ1eYAeTMFFgj
```
{% include copy-curl.html %}

當作業完成時，狀態會變為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "XPcXLV7RQoi5m8NI_jEOVQ"
  ],
  "create_time": 1689793598499,
  "last_update_time": 1689793598530,
  "is_async": false
}
```

請記下傳回的 `model_id`，因為部署模型時需要用到它。

## 步驟 3：部署模型

部署作業會從模型索引讀取模型的區塊，然後建立要載入記憶體的模型執行個體。模型越大，被分割成的區塊就越多，載入記憶體所需的時間也越長。

若要部署已註冊的模型，請在以下請求中提供其步驟 3 的模型 ID：

```bash
POST /_plugins/_ml/models/cleMb4kBJ1eYAeTMFFg4/_deploy
```
{% include copy-curl.html %}

回應包含任務 ID，您可用它來檢查部署作業的狀態：

```json
{
  "task_id": "vVePb4kBJ1eYAeTM7ljG",
  "status": "CREATED"
}
```

與上一個步驟相同，透過呼叫 [Get ML Task API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/tasks-apis/get-task/) 檢查作業狀態：

```bash
GET /_plugins/_ml/tasks/vVePb4kBJ1eYAeTM7ljG
```
{% include copy-curl.html %}

當作業完成時，狀態會變為 `COMPLETED`：

```json
{
  "model_id": "cleMb4kBJ1eYAeTMFFg4",
  "task_type": "DEPLOY_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "n-72khvBTBi3bnIIR8FTTw"
  ],
  "create_time": 1689793851077,
  "last_update_time": 1689793851101,
  "is_async": true
}
```

如果叢集或節點重新啟動，您需要重新部署模型。若要了解如何設定自動重新部署，請參閱[模型部署設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/#model-deployment-settings)。
{: .tip} 

## 步驟 4 (選用)：測試模型

使用 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 來測試模型。

### 文字嵌入模型

若為文字嵌入模型，請傳送下列請求：

```json
POST /_plugins/_ml/_predict/text_embedding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs":[ "today is sunny"],
  "return_number": true,
  "target_response": ["sentence_embedding"]
}
```
{% include copy-curl.html %}

回應中包含所提供句子的文字嵌入：

```json
{
  "inference_results" : [
    {
      "output" : [
        {
          "name" : "sentence_embedding",
          "data_type" : "FLOAT32",
          "shape" : [
            768
          ],
          "data" : [
            0.25517133,
            -0.28009856,
            0.48519906,
            ...
          ]
        }
      ]
    }
  ]
}
```

### 稀疏編碼模型或稀疏斷詞器

若為稀疏編碼模型或稀疏斷詞器，請傳送下列請求：

```json
POST /_plugins/_ml/_predict/sparse_encoding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs":[ "today is sunny"]
}
```
{% include copy-curl.html %}

回應中包含擷取出的詞元及其對應的權重：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "output",
          "dataAsMap": {
            "response": [
              {
                "saturday": 0.48336542,
                "week": 0.1034762,
                "mood": 0.09698499,
                "sunshine": 0.5738209,
                "bright": 0.1756877,
                ...
              }
          }
        }
    }
}
```

上述範例使用預設的 `lexical` 輸出格式，會以字串作為鍵傳回。您可以將 `parameters.sparse_embedding_format` 設為 `lexical` (傳回字串詞元) 或 `token_id` (傳回整數詞元 ID)，來控制輸出鍵的格式。下列範例將 `sparse_embedding_format` 設為 `token_id`：

```json
POST /_plugins/_ml/_predict/sparse_encoding/cleMb4kBJ1eYAeTMFFg4
{
  "text_docs": ["hello world"],
  "parameters": {
    "sparse_embedding_format": "token_id"
  }
}
```
{% include copy-curl.html %}

回應中包含詞元 ID 及其對應的詞元權重：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "dataAsMap": {
            "response": [
              {
                "2088": 3.4208686,
                "7592": 6.9377565
              }
            ]
          }
        }
      ]
    }
  ]
}
```

### 交叉編碼器模型

若為交叉編碼器模型，請傳送下列請求：

```json
POST _plugins/_ml/models/{model_id}/_predict
{
    "query_text": "today is sunny",
    "text_docs": [
        "how are you",
        "today is sunny",
        "today is july fifth",
        "it is winter"
    ]
}
```
{% include copy-curl.html %}

模型會計算 `query_text` 與 `text_docs` 中每份文件的相似度分數，並依文件在 `text_docs` 中提供的順序，傳回每份文件的分數清單：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            -6.077798
          ],
          "byte_buffer": {
            "array": "Un3CwA==",
            "order": "LITTLE_ENDIAN"
          }
        }
      ]
    },
    {
      "output": [
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            10.223609
          ],
          "byte_buffer": {
            "array": "55MjQQ==",
            "order": "LITTLE_ENDIAN"
          }
        }
      ]
    },
    {
      "output": [
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            -1.3987057
          ],
          "byte_buffer": {
            "array": "ygizvw==",
            "order": "LITTLE_ENDIAN"
          }
        }
      ]
    },
    {
      "output": [
        {
          "name": "similarity",
          "data_type": "FLOAT32",
          "shape": [
            1
          ],
          "data": [
            -4.5923924
          ],
          "byte_buffer": {
            "array": "4fSSwA==",
            "order": "LITTLE_ENDIAN"
          }
        }
      ]
    }
  ]
}
```

文件分數越高，代表相似度越高。在上述回應中，各文件相對於查詢文字 `today is sunny` 的分數如下：

文件文字 | 分數
:--- | :---
`how are you` | -6.077798
`today is sunny` | 10.223609
`today is july fifth` | -1.3987057
`it is winter` | -4.5923924

與查詢文字相同的文件分數最高，其餘文件則依文字相似度計分。

## 步驟 5：使用模型進行搜尋

若要了解如何設定向量索引，並使用文字嵌入模型進行搜尋，請參閱[語意搜尋]({{site.url}}{{site.baseurl}}/search-plugins/semantic-search/)。

若要了解如何設定向量索引，並使用稀疏編碼模型進行搜尋，請參閱[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/search-plugins/neural-sparse-search/)。

若要了解如何使用交叉編碼器模型進行重新排序，請參閱[重新排序搜尋結果]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/reranking-search-results/)。

