---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "產生向量"
nav_order: 40
parent: Synthetic data generation
grand_parent: Additional features
---

# 產生向量

您可以使用 OpenSearch Benchmark 的合成資料產生器，從對應產生合成的密集向量與稀疏向量。

## 密集向量

密集向量（在 OpenSearch 中以 [`knn_vector`]({{site.url}}{{site.baseurl}}/field-types/supported-field-types/knn-vector/) 欄位類型表示）是文字或影像等資料的數值表示法，其大部分或所有維度都具有非零值。這些向量通常包含介於 -1.0 到 1.0 之間的浮點數，每個維度都對整體語意有所貢獻。

單字「dog」的嵌入範例：

```json
{
  "embedding": [0.234, -0.567, 0.123, 0.891, -0.234, 0.456, ..., 0.789]
}
```

## 稀疏向量

稀疏向量（在 OpenSearch 中以 [`sparse_vector`]({{site.url}}{{site.baseurl}}/field-types/supported-field-types/sparse-vector/) 欄位類型表示）是大部分維度皆為零的向量，以非零詞元 ID 及其權重的鍵值對來表示。

範例文字：`Korean jindos are hunting dogs that have a reputation for being loyal, independent, and confident`。

範例文字的稀疏向量表示法：

```json
{
  "5432": 0.85,   // "korean" - very important (specific descriptor)
  "7821": 0.78,   // "jindos" - very important (breed name)
  "2": 0.45,      // "dog" - moderately important (general category)
  "9999": 0.32,   // "loyal" - somewhat important (characteristic)
  "1111": 0.12    // "things" - less important (common word)
}
```
---

## 基本用法

下列範例說明如何僅使用 OpenSearch 索引對應，以最精簡的組態產生向量。

### 產生密集向量

以最精簡的組態產生隨機的 128 維向量。

**1. 建立對應檔案**（`simple-knn-mapping.json`）：

```json
{
  "settings": {
    "index.knn": true
  },
  "mappings": {
    "properties": {
      "title": {"type": "text"},
      "my_embedding": {
        "type": "knn_vector",
        "dimension": 128
      }
    }
  }
}
```
{% include copy.html %}

**2. 產生資料**：

```bash
opensearch-benchmark generate-data \
  --index-name my-vectors \
  --index-mappings simple-knn-mapping.json \
  --output-path ./output \
  --total-size 1
```
{% include copy.html %}

#### 產生的輸出

在每個產生的文件中，`my_embedding` 欄位可能如下所示：

```json
{
  "title": "Sample text 42",
  "my_embedding": [0.234, -0.567, 0.123, ..., 0.891]  // 128 random floats [-1.0, 1.0]
}
```

### 產生稀疏向量

以預設組態（10 個詞元）產生稀疏向量。

**1. 建立對應檔案**（`simple-sparse-mapping.json`）：

```json
{
  "mappings": {
    "properties": {
      "content": {"type": "text"},
      "sparse_embedding": {
        "type": "sparse_vector"
      }
    }
  }
}
```
{% include copy.html %}

**2. 產生資料**（相同的命令模式）：

```bash
opensearch-benchmark generate-data \
  --index-name my-sparse \
  --index-mappings simple-sparse-mapping.json \
  --output-path ./output \
  --total-size 1
```
{% include copy.html %}

#### 產生的輸出

在每個產生的文件中，`sparse_embedding` 欄位可能如下所示：

```json
{
  "content": "Sample text content",
  "sparse_embedding": {
    "1000": 0.3421,
    "1100": 0.5234,
    "1200": 0.7821,
    "1300": 0.1523,
    "1400": 0.9102,
    "1500": 0.4567,
    "1600": 0.2341,
    "1700": 0.6789,
    "1800": 0.8123,
    "1900": 0.3456
  }
}
```

OpenSearch Benchmark 只需使用 OpenSearch 索引對應，即可產生合成的密集向量與稀疏向量。不過，這樣只會產生基本的合成向量。若要獲得更貼近實際的分布與群集，建議您設定下一節所述的參數。

---

## 密集向量（k-NN 向量）參數

以下是您可以加入合成資料產生組態檔案（YAML 組態）中的參數，用於微調密集向量的產生方式。這些參數會在 `field_overrides` 區段中搭配 `generate_knn_vector` 產生器使用。如需完整的組態詳細資訊，請參閱[進階組態](/benchmark/features/synthetic-data-generation/mapping-sdg/#advanced-configuration)。

<!-- vale off -->
#### dimension
<!-- vale on -->

此參數指定向量的維度數。選用。

**指定方式**：`dimension` 必須定義在您的 OpenSearch 索引對應檔案中。您可以選擇在 YAML 組態中使用 `field_overrides` 內的 `dimension` 參數覆寫此值。

**影響**：
- **記憶體**：維度越高 = 需要越多儲存空間
  - 128 維 ≈ 每個向量 0.5 KB
  - 768 維 ≈ 每個向量 3 KB
  - 1536 維 ≈ 每個向量 6 KB
- **效能**：維度越多 = 編製索引與搜尋越慢
- **品質**：必須與您實際使用的嵌入模型輸出相符

下表列出常見的維度值及其典型使用情境。

| 維度 | 使用情境 | 範例模型 |
|-----------|----------|----------------|
| 128 | 輕量、自訂模型 | 自訂嵌入、快速搜尋 |
| 384 | 一般用途 | sentence-transformers/all-MiniLM-L6-v2 |
| 768 | 標準 NLP | BERT-Base, DistilBERT, MPNet |
| 1,024 | 高品質 NLP | BERT-Large |
| 1,536 | OpenAI 標準 | text-embedding-ada-002, text-embedding-3-small |
| 3,072 | OpenAI 進階 | text-embedding-3-large |

**範例**：

```yaml
field_overrides:
  my_embedding:
    generator: generate_knn_vector
    params:
      dimension: 768  # Override mapping dimension if needed
```
{% include copy.html %}

**最佳做法**：此參數必須與您的嵌入模型維度相符。

---

#### sample_vectors

此參數提供基礎向量，產生器會在這些向量上加入雜訊，以建立貼近實際的變化與群集。選用，但強烈建議使用。

若未提供範例向量，OpenSearch Benchmark 的合成資料產生器會在整個空間中產生均勻分布的隨機向量，這樣既不貼近實際，搜尋品質也很差。提供範例向量可讓 OpenSearch Benchmark 的合成資料產生器建立更貼近實際且自然的群集。

準備好範例向量清單後，請將其插入為**清單的清單**，其中每個內部清單都是一個完整的向量。下列範例在合成資料產生組態檔案中提供範例向量：

```yaml
field_overrides:
  product_embedding:
    generator: generate_knn_vector
    params:
      dimension: 768
      sample_vectors:
        - [0.12, -0.34, 0.56, ..., 0.23]  # Vector 1 (768 values)
        - [-0.23, 0.45, -0.12, ..., -0.15]  # Vector 2 (768 values)
        - [0.34, 0.21, -0.45, ..., 0.42]  # Vector 3 (768 values)
```
{% include copy.html %}

請依照下列準則決定要提供的向量數量：

- **最少**：3--5 個，用於基本群集
- **建議**：5--10 個，以獲得貼近實際的分布
- **最多**：20 個以上，用於複雜的多群集情境

**如何取得範例向量**：

**選項 1（建議）：使用您領域中的實際嵌入**：使用您領域中代表不同語意群集的實際嵌入。在沒有範例向量的情況下隨機產生的資料並不貼近實際，不適合用於搜尋品質測試。

**選項 2：在 Python 中使用 sentence-transformers**：

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# Create representative texts from different categories
texts = [
    "Electronics and gadgets",
    "Clothing and fashion",
    "Home and kitchen appliances",
    "Books and literature",
    "Sports and outdoor equipment"
]

embeddings = model.encode(texts)
print(embeddings.tolist())  # Copy to your synthetic data generation configuration file (YAML config)
```
{% include copy.html %}

---

#### distribution_type

此參數指定雜訊分佈的類型。選用。預設值為 `gaussian`。

**有效值**：
- `gaussian`：常態分佈 N(0, `noise_factor`)
  - 最為逼真（自然變異並偶爾出現離群值）
  - 產生平滑的叢集
  - 部分數值可能超出預期範圍

- `uniform`：均勻分佈 [-`noise_factor`, +`noise_factor`]
  - 變異有界（無極端離群值）
  - 結果較可預測
  - 整個範圍內機率均勻

**組態**：
```yaml
field_overrides:
  realistic_embedding:
    generator: generate_knn_vector
    params:
      sample_vectors: [...]
      noise_factor: 0.1
      distribution_type: gaussian  # More realistic

  controlled_embedding:
    generator: generate_knn_vector
    params:
      sample_vectors: [...]
      noise_factor: 0.1
      distribution_type: uniform   # More predictable
```
{% include copy.html %}

**最佳實務**：在類似正式環境的基準測試中使用 `gaussian`。

---

<!-- vale off -->
#### noise_factor
<!-- vale on -->

此參數控制加入基礎向量的雜訊量：
- 對於 `gaussian`：常態分佈的標準差
- 對於 `uniform`：均勻分佈的範圍（±`noise_factor`）

選用。預設值為 `0.1`。

下表顯示不同的 `noise_factor` 值對產生資料的影響。

| `noise_factor` | 效果 | 使用情境 |
|--------------|--------|----------|
| 0.01--0.05 | 緊密叢集，變異極小 | 重複偵測、近似完全相符 |
| 0.1--0.2 | 主題內的自然變異 | 一般語意搜尋、推薦 |
| 0.3--0.5 | 廣泛離散，概念多樣 | 廣泛主題比對、探索 |
| > 0.5 | 非常分散，叢集重疊 | 測試邊界情況、壓力測試 |

**組態**：

```yaml
field_overrides:
  tight_clustering:
    generator: generate_knn_vector
    params:
      sample_vectors: [...]
      noise_factor: 0.05  # Tight clusters

  diverse_results:
    generator: generate_knn_vector
    params:
      sample_vectors: [...]
      noise_factor: 0.2   # More variation
```
{% include copy.html %}

**最佳實務**：先從 `0.1` 開始，再依據搜尋召回率或精確度需求進行調整。

---

<!-- vale off -->
#### normalize
<!-- vale on -->

此參數在加入雜訊後對向量進行正規化，使其大小（長度）恰好為 `1.0`。選用。預設值為 `false`。

下表顯示根據您的索引組態，何時應將 `normalize` 設為 `true`。

| 索引對應中的 `space_type` | `normalize` 值 | 說明                                                                                                                                             |
| --------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `cosinesimil`                     | `true`            | 餘弦相似度僅取決於向量方向。預先正規化可提升效能，因為點積可直接代表餘弦相似度。 |
| `l2`                              | `false`           | L2 距離依賴向量大小。正規化會移除大小資訊並降低準確度。                                                 |
| `innerproduct`                    | `false`           | 內積會將向量大小納入相似度分數，因此正規化會改變預期的評分行為。                     |

**實際模型指引**：

* **OpenAI embeddings**：這些向量已預先正規化，因此請將 `normalize` 設為 `true`。
* **sentence-transformers**：許多模型會輸出已正規化的向量。請查閱模型文件；在大多數情況下，`normalize` 應設為 `true`。
* **BERT (raw output)**：原始 BERT 嵌入未經正規化。請將 `normalize` 設為 `false`，並視需要依靠索引組態執行正規化。

**組態**：

```yaml
field_overrides:
  # For cosine similarity search
  cosine_embedding:
    generator: generate_knn_vector
    params:
      dimension: 384
      sample_vectors: [...]
      normalize: true  # Required for accurate cosine similarity

  # For L2 distance search
  l2_embedding:
    generator: generate_knn_vector
    params:
      dimension: 768
      sample_vectors: [...]
      normalize: false  # Keep original magnitudes
```
{% include copy.html %}

**最佳實務**：與您 OpenSearch 索引的 `space_type` 設定保持一致。

---

## 稀疏向量參數

以下是您可新增至合成資料產生組態檔的參數，用於微調稀疏向量的產生方式。這些參數用於 `field_overrides` 區段搭配 `generate_sparse_vector` 產生器。如需完整組態細節，請參閱[進階組態](/benchmark/features/synthetic-data-generation/mapping-sdg/#advanced-configuration)。

<!-- vale off -->
#### num_tokens
<!-- vale on -->

此參數指定每個向量要產生的詞元-權重配對數量。選用。預設值為 `10`。

**影響**：
- **低 (5--10)**：非常稀疏，搜尋快速；可能遺漏部分相關文件
- **中 (10--25)**：效能與召回率均衡
- **高 (50--100)**：稠密的稀疏表示；內容完整但速度較慢

下表顯示不同模型與方法的典型 `num_tokens` 值。

| 模型/方法 | 典型 `num_tokens` | 使用情境 |
|----------------|-------------------|----------|
| SPLADE v1 | 10--15 | 標準稀疏神經搜尋 |
| SPLADE v2 | 15--25 | 改進的召回率 |
| DeepImpact | 8--12 | 高效率稀疏搜尋 |
| Custom/Hybrid | 20--50 | 豐富的表示方式 |

**組態**：

```yaml
field_overrides:
  sparse_standard:
    generator: generate_sparse_vector
    params:
      num_tokens: 15  # Standard SPLADE-like

  sparse_rich:
    generator: generate_sparse_vector
    params:
      num_tokens: 30  # Richer representation
```
{% include copy.html %}

**最佳實務**：先從 `10--15` 開始；若召回率不足再增加。

---

<!-- vale off -->
#### min_weight 與 max_weight
<!-- vale on -->

這些參數定義詞元重要性權重的範圍。選用。`min_weight` 預設值為 `0.01`；`max_weight` 預設值為 `1.0`。

**影響**：
- `min_weight`：在產生時排除低重要性詞元。權重低於此值的詞元不會被納入。
- `max_weight`：限制詞元影響力的上限，防止任何單一詞元主導整個向量。

下表顯示常見的權重範圍組態及其使用情境。

| 組態 | `min_weight` | `max_weight` | 使用情境 |
|---------------|-----|-----|----------|
| 標準 SPLADE | `0.01` | `1.0` | 預設，重要性均衡 |
| 窄範圍 | `0.1` | `0.9` | 重要性較均勻 |
| 寬範圍 | `0.01` | `2.0` | 強烈的重要性訊號 |
| 高門檻 | `0.05` | `1.0` | 篩選低信心詞元 |

**組態**：

```yaml
field_overrides:
  sparse_balanced:
    generator: generate_sparse_vector
    params:
      num_tokens: 15
      min_weight: 0.01
      max_weight: 1.0

  sparse_uniform:
    generator: generate_sparse_vector
    params:
      num_tokens: 20
      min_weight: 0.2   # Higher minimum
      max_weight: 0.8   # Lower maximum
```
{% include copy.html %}

**限制**：
- `min_weight` 必須 > `0.0`（OpenSearch 要求權重為正值）。
- `max_weight` 必須 > `min_weight`。
- 權重會四捨五入至 `4` 位小數。

**最佳實務**：將 `min_weight` 保持較小（`0.01--0.05`），以允許細緻的權重調整。

---

<!-- vale off -->
#### token_id_start 與 token_id_step
<!-- vale on -->

這些參數定義在產生向量期間如何指派詞元 ID：

- `token_id_start`：設定產生序列中的起始詞元 ID。預設為 `1000`。

- `token_id_step`：指定每個連續詞元 ID 之間套用的增量。預設為 `100`。

**產生的序列**：`start, start+step, start+2*step, ...`

**範例**，使用 `start=1000`、`step=100`、`num_tokens=5`：

```json
{
  "1000": 0.3421,  // token_id_start
  "1100": 0.5234,  // start + 1*step
  "1200": 0.7821,  // start + 2*step
  "1300": 0.1523,  // start + 3*step
  "1400": 0.9102   // start + 4*step
}
```
{% include copy.html %}

下表顯示不同的詞元 ID 組態及其使用情境。

| 組態 | `token_id_start` | `token_id_step` | 使用情境 |
| --------------------------- | ----------------- | --------------- | ------------------------------------------------------------------ |
| 預設測試 | `1000` | `100` | 有助於在視覺上區分產生的詞元範圍。 |
| 真實詞彙 | `0` | `1` | 使詞元 ID 與真實模型的詞彙索引對齊。 |
| 多欄位產生 | `1000`, `5000`, `10000` | `1` | 讓不同欄位的詞元 ID 範圍彼此分開。 |
| 大型詞彙模擬 | `0` | `1` | 支援詞彙量達 `50,000` 個以上詞元的產生情境。 |

**組態**：

```yaml
field_overrides:
  # Default: easy debugging
  sparse_debug:
    generator: generate_sparse_vector
    params:
      num_tokens: 10
      token_id_start: 1000
      token_id_step: 100

  # Realistic: actual vocab indices
  sparse_realistic:
    generator: generate_sparse_vector
    params:
      num_tokens: 15
      token_id_start: 0
      token_id_step: 1

  # Multiple fields: separate ranges
  sparse_field1:
    generator: generate_sparse_vector
    params:
      token_id_start: 1000

  sparse_field2:
    generator: generate_sparse_vector
    params:
      token_id_start: 5000
```
{% include copy.html %}

**注意**：產生資料中的詞元 ID 是連續的。在真實的稀疏向量中，ID 可能會根據實際詞彙而為非連續。此差異不會影響 OpenSearch 的索引編製或搜尋功能。

**最佳實務**：偵錯時使用較大的 `token_id_step`（例如 `100`），而對於模擬正式環境的資料，請將 `token_id_step` 設為 `1`。

---

## 選擇簡單或複雜的產生方式

下表根據您的測試目標，概述何時使用簡單產生方式，以及何時使用更複雜、可設定的方式。

| 情境 | 建議方式 | 理由 |
| ------------------------- | ----------------------------------------------- | --------------------------------------------------------------------------------------------- |
| 學習或快速測試 | 簡單產生（無額外組態） | 設定最快速，足以進行基本驗證。 |
| 負載測試 | 簡單產生 | 優先考量資料量與輸送量，而非向量的真實性。 |
| 貼近實際的基準測試 | 複雜產生（搭配組態） | 需要貼近實際的向量群集與分佈，以反映真實世界的行為。 |
| 正式環境模擬 | 複雜產生 | 需要與實際嵌入模型所產生之向量特性高度相符的向量。 |
| 搜尋品質測試 | 複雜產生 | 需要有意義的向量群集，才能準確評估召回率與精確率。 |


**建議**：若要進行搜尋品質測試或演算法比較，請使用包含範例向量的複雜組態，以確保資料分佈貼近實際情況。
