---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Min hash
parent: Token filters
nav_order: 270
---

# Min hash 詞元篩選器

`min_hash` 詞元篩選器會根據 [MinHash](https://en.wikipedia.org/wiki/MinHash) 近似演算法為詞元產生雜湊值，可用於偵測文件之間的相似度。`min_hash` 詞元篩選器會為一組詞元（通常來自經過分析的欄位）產生雜湊值。

## 參數

`min_hash` 詞元篩選器可以使用下列參數進行設定。

參數 | 必要/選用 | 資料類型 | 說明
:--- | :--- | :--- | :--- 
`hash_count` | 選用 | 整數 | 為每個詞元產生的雜湊值數量。增加此值通常可提高相似度估算的準確性，但會增加運算成本。預設值為 `1`。
`bucket_count` | 選用 | 整數 | 要使用的雜湊桶 (bucket) 數量。這會影響雜湊的細緻度。桶的數量越多，細緻度越高，雜湊衝突也越少，但需要更多記憶體。預設值為 `512`。
`hash_set_size` | 選用 | 整數 | 每個桶中要保留的雜湊值數量。這可能會影響雜湊品質。較大的集合大小可能帶來更好的相似度偵測效果，但會耗用更多記憶體。預設值為 `1`。
`with_rotation` | 選用 | 布林值 | 設為 `true` 時，若 `hash_set_size` 為 `1`，篩選器會以循環方向往右找到的第一個非空桶的值，填入空的桶。若 `bucket_count` 引數超過 `1`，此設定會自動預設為 `true`；否則預設為 `false`。

## 範例

下列範例請求會建立名為 `minhash_index` 的新索引，並設定一個使用 `min_hash` 篩選器的分析器：

```json
PUT /minhash_index
{
  "settings": {
    "analysis": {
      "filter": {
        "minhash_filter": {
          "type": "min_hash",
          "hash_count": 3,
          "bucket_count": 512,
          "hash_set_size": 1,
          "with_rotation": false
        }
      },
      "analyzer": {
        "minhash_analyzer": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": [
            "minhash_filter"
          ]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 產生的詞元

使用下列請求來檢視使用此分析器產生的詞元：

```json
POST /minhash_index/_analyze
{
  "analyzer": "minhash_analyzer",
  "text": "OpenSearch is very powerful."
}
```
{% include copy-curl.html %}

回應中包含產生的詞元（這些詞元代表雜湊值，因此人類無法直接閱讀）：

```json
{
  "tokens" : [
    {
      "token" : "\u0000\u0000㳠锯ੲ걌䐩䉵",
      "start_offset" : 0,
      "end_offset" : 27,
      "type" : "MIN_HASH",
      "position" : 0
    },
    {
      "token" : "\u0000\u0000㳠锯ੲ걌䐩䉵",
      "start_offset" : 0,
      "end_offset" : 27,
      "type" : "MIN_HASH",
      "position" : 0
    },
    ...
```

為了展示 `min_hash` 詞元篩選器的用處，您可以使用下列 Python 指令碼，透過先前建立的分析器比較這兩個字串：

```python
from opensearchpy import OpenSearch
from requests.auth import HTTPBasicAuth

# Initialize the OpenSearch client with authentication
host = 'https://localhost:9200'  # Update if using a different host/port
auth = ('admin', 'admin')  # Username and password

# Create the OpenSearch client with SSL verification turned off
client = OpenSearch(
    hosts=[host],
    http_auth=auth,
    use_ssl=True,
    verify_certs=False,  # Disable SSL certificate validation
    ssl_show_warn=False  # Suppress SSL warnings in the output
)

# Analyzes text and returns the minhash tokens
def analyze_text(index, text):
    response = client.indices.analyze(
        index=index,
        body={
            "analyzer": "minhash_analyzer",
            "text": text
        }
    )
    return [token['token'] for token in response['tokens']]

# Analyze two similar texts
tokens_1 = analyze_text('minhash_index', 'OpenSearch is a powerful search engine.')
tokens_2 = analyze_text('minhash_index', 'OpenSearch is a very powerful search engine.')

# Calculate Jaccard similarity
set_1 = set(tokens_1)
set_2 = set(tokens_2)
shared_tokens = set_1.intersection(set_2)
jaccard_similarity = len(shared_tokens) / len(set_1.union(set_2))

print(f"Jaccard Similarity: {jaccard_similarity}")
```

回應中應包含 Jaccard 相似度分數：

```yaml
Jaccard Similarity: 0.8571428571428571
```