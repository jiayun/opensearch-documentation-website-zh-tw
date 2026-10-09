---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遠端索引建置"
nav_order: 72
has_children: false
---

# 使用 GPU 遠端建置向量索引
於 3.0 版導入 
{: .label .label-purple }

OpenSearch 支援使用 GPU 加速的遠端索引建置服務來建置向量索引。使用 GPU 可大幅縮短索引建置時間並降低成本。基準測試結果請參閱[這篇網誌文章](https://opensearch.org/blog/GPU-Accelerated-Vector-Search-OpenSearch-New-Frontier/)。

## 支援的組態

遠端索引建置服務支援使用 `hnsw` 方法的 [Faiss]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-methods-engines/#faiss-engine) 索引。對於這些索引，該服務支援下列向量類型：

- 預設的 32 位元浮點數 (`FP32`) 向量
- 16 位元浮點數 (`FP16`)、位元組與二進位向量，適用於所有壓縮層級 (`2x`、`8x`、`16x` 與 `32x`)
- [`half_float` 向量]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-memory-optimized/#half-float-vectors)，適用於 `1x` 與 `16x` 壓縮層級

不支援使用 [`bf16` 編碼器類型]({{site.url}}{{site.baseurl}}/vector-search/optimizing-storage/faiss-scalar-quantization/#the-bf16-encoder) 量化的向量，使用該編碼器的索引一律在本機建置。

## 先決條件

在設定遠端索引建置設定之前，請確認您符合下列先決條件。有關更新動態設定的更多資訊，請參閱[動態設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index/#dynamic-settings)。

### 步驟 1：啟用遠端索引建置服務

只有當叢集層級設定 `knn.remote_index_build.enabled` 與索引層級設定 `index.knn.remote_index_build.enabled` 都設為 `true` 時，OpenSearch 才會遠端建置索引。叢集層級設定預設為 `false`，因此請為叢集啟用它：

```json
PUT /_cluster/settings
{
  "persistent": {
    "knn.remote_index_build.enabled": true
  }
}
```
{% include copy-curl.html %}

索引層級設定預設為 `true`，因此僅在要將個別索引排除於遠端索引建置之外時，才將它設為 `false`。有關這兩項設定的說明，請參閱[遠端索引建置設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#remote-index-build-settings)。

### 步驟 2：建立並註冊遠端向量儲存庫

遠端向量儲存庫充當 OpenSearch 叢集與遠端建置服務之間的中介物件儲存空間。叢集會將向量與文件 ID 上傳至儲存庫。遠端建置服務會擷取該資料、在外部建置索引，並將完成的結果上傳回儲存庫。

若要建立並註冊儲存庫，請依照[註冊儲存庫]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#register-repository)中的步驟操作。然後將 `knn.remote_index_build.repository` 動態設定設為已註冊儲存庫的名稱。

遠端建置服務僅支援 Amazon Simple Storage Service (Amazon S3) 儲存庫。
{: .note}

### 步驟 3：設定遠端向量索引建置器

在 k-NN 設定中，將 `knn.remote_index_build.service.endpoint` 設為執行中的[遠端向量索引建置器](https://github.com/opensearch-project/remote-vector-index-builder) 執行個體，以設定遠端端點。有關設定遠端服務的說明，請參閱[使用者指南](https://github.com/opensearch-project/remote-vector-index-builder/blob/main/USER_GUIDE.md)。

## 設定遠端索引建置設定

遠端索引建置服務支援數個額外的選用設定。有關設定其餘遠端索引建置設定的資訊，請參閱[遠端索引建置設定]({{site.url}}{{site.baseurl}}/vector-search/settings/#remote-index-build-settings)。

## 使用遠端索引建置服務

遠端索引建置服務設定完成後，任何符合下列要求的分段排清與合併作業都會透明地使用 GPU 建置路徑：

- 索引使用其中一種[支援的組態](#supported-configurations)。
- 分段大小大於 `index.knn.remote_index_build.size.min` 且小於 `knn.remote_index_build.size.max`。

您可以呼叫 k-NN Stats API 並檢視[遠端索引建置統計資料]({{site.url}}{{site.baseurl}}/vector-search/api/knn/#remote-index-build-stats)來監控遠端索引建置工作。
