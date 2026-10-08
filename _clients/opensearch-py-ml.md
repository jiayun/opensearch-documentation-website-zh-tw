---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Python ML 用戶端"
parent: Python client
nav_order: 10
---

# Python 機器學習用戶端

Python 機器學習 (ML) 用戶端 (`opensearch-py-ml`) 是一個 Python 程式庫，可與 [Python 用戶端]({{site.url}}{{site.baseurl}}/clients/python-low-level/) (`opensearch-py`) 搭配使用。它提供下列工具：

- 代表 OpenSearch 索引並支援類似 pandas 操作的 DataFrame，讓您能分析儲存在 OpenSearch 中的資料。
- 用於將 ML 模型上傳至 ML Commons 外掛程式並加以管理的方法。

## 安裝 Python ML 用戶端

最新版本的用戶端 `opensearch-py-ml` 1.3.0 需要 Python 3.11 或更新版本。若要將用戶端加入您的專案，請使用 [pip](https://pip.pypa.io/) 安裝：

```bash
pip install opensearch-py-ml
```
{% include copy.html %}

安裝 `opensearch-py-ml` 也會一併安裝 Python 用戶端 (`opensearch-py`)，您可用它連線至 OpenSearch。

## 連線至 OpenSearch

若要連線至 OpenSearch，請建立一個 Python 用戶端物件並匯入 `opensearch_py_ml`。如果您使用 Security 外掛程式，請在啟用 SSL 的情況下建立用戶端物件。將 `<custom-admin-password>` 替換為安裝 OpenSearch 時設定的管理員密碼：

```python
from opensearchpy import OpenSearch
import opensearch_py_ml as oml

host = 'localhost'
port = 9200
auth = ('admin', '<custom-admin-password>') # For testing only. Don't store credentials in code.
ca_certs_path = '/full/path/to/root-ca.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False,
    ca_certs = ca_certs_path
)
```
{% include copy.html %}

如果您未使用 Security 外掛程式，請在停用 SSL 的情況下建立用戶端物件：

```python
from opensearchpy import OpenSearch
import opensearch_py_ml as oml

host = 'localhost'
port = 9200

# Create the client with SSL/TLS and hostname verification disabled.
client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True, # enables gzip compression for request bodies
    use_ssl = False,
    verify_certs = False,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)
```
{% include copy.html %}

如需更多連線選項，包括連線至 Amazon OpenSearch Service，請參閱 [Python 用戶端]({{site.url}}{{site.baseurl}}/clients/python-low-level/)。

## 使用 DataFrame 分析資料

`opensearch-py-ml` DataFrame 代表一個 OpenSearch 索引。當您在 DataFrame 中選取、篩選或彙總資料時，用戶端會將該操作轉換為 OpenSearch 請求，因此資料會保留在索引中，直到您需要結果為止。

首先，使用 Python 用戶端將範例文件編製索引至 `students` 索引：

```python
docs = [
    {"firstName": "John", "lastName": "Doe", "gpa": 3.89, "gradDate": "2022-05-15"},
    {"firstName": "Paulo", "lastName": "Santos", "gpa": 3.93, "gradDate": "2021-05-20"},
    {"firstName": "Shirley", "lastName": "Rodriguez", "gpa": 3.91, "gradDate": "2019-05-10"},
]

for doc_id, doc in enumerate(docs, start=1):
    client.index(index="students", id=doc_id, body=doc, refresh=True)
```
{% include copy.html %}

接著為 `students` 索引建立 DataFrame 並顯示其前幾列：

```python
df = oml.DataFrame(client, "students")
print(df.head())
```
{% include copy.html %}

輸出內容包含每份文件一列，並以文件 ID 作為索引：

```
  firstName   gpa   gradDate   lastName
1      John  3.89 2022-05-15        Doe
2     Paulo  3.93 2021-05-20     Santos
3   Shirley  3.91 2019-05-10  Rodriguez

[3 rows x 4 columns]
```

若要計算數值欄位的摘要統計資料，請使用 `describe` 方法：

```python
print(df.describe())
```
{% include copy.html %}

輸出內容包含 `gpa` 欄位的統計資料：

```
            gpa
count  3.000000
mean   3.910000
std    0.024495
min    3.890000
25%    3.890000
50%    3.910000
75%    3.930000
max    3.930000
```

若要篩選文件並選取欄位，請使用 pandas 語法。下列範例會傳回 GPA 大於 3.9 的學生姓名與 GPA：

```python
print(df[df["gpa"] > 3.9][["firstName", "lastName", "gpa"]])
```
{% include copy.html %}

輸出內容包含兩位符合條件的學生：

```
  firstName   lastName   gpa
2     Paulo     Santos  3.93
3   Shirley  Rodriguez  3.91

[2 rows x 3 columns]
```

若要將 DataFrame 轉換為 pandas DataFrame，請使用 `to_pandas` 方法。此方法會從 OpenSearch 擷取所有符合條件的文件。

如需所有 DataFrame 方法，請參閱 [`opensearch-py-ml` DataFrame 參考文件](https://opensearch-project.github.io/opensearch-py-ml/reference/dataframe.html)。

## 上傳預先訓練模型

使用 `MLCommonClient` 類別來註冊並部署 OpenSearch 提供的其中一個[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。

預設情況下，ML Commons 只會在專用的 ML 節點上執行模型。如果您的叢集沒有專用的 ML 節點，請允許模型在資料節點上執行：

```python
client.cluster.put_settings(body={
    "persistent": {
        "plugins.ml_commons.only_run_on_ml_node": "false"
    }
})
```
{% include copy.html %}

如需更多資訊，請參閱 [ML Commons 叢集設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/)。

下列範例會註冊並部署 `huggingface/sentence-transformers/all-MiniLM-L6-v2` 模型。此方法會等待模型部署完成，並傳回模型 ID：

```python
from opensearch_py_ml.ml_commons import MLCommonClient

ml_client = MLCommonClient(client)

model_id = ml_client.register_pretrained_model(
    model_name="huggingface/sentence-transformers/all-MiniLM-L6-v2",
    model_version="1.0.2",
    model_format="TORCH_SCRIPT",
    deploy_model=True,
    wait_until_deployed=True
)
```
{% include copy.html %}

此方法會列印模型 ID 與部署工作 ID：

```
Model was registered successfully. Model Id:  oVMj-aABo6RnaVqceH5b
oVMj-aABo6RnaVqceH5b
Task ID: olMj-aABo6RnaVqcuX7E
Model deployed successfully
```

由於範例未指定模型群組，ML Commons 會為該模型建立一個模型群組。若要將模型註冊到現有的模型群組，請在 `model_group_id` 參數中傳入模型群組 ID。

若要使用已部署的模型產生嵌入，請將文字傳送至模型：

```python
response = ml_client.generate_model_inference(
    model_id,
    {"text_docs": ["Paulo Santos graduated in 2021."], "target_response": ["sentence_embedding"]}
)
embedding = response["inference_results"][0]["output"][0]
print(embedding["shape"])
print(embedding["data"][:3])
```
{% include copy.html %}

模型會傳回 384 維的嵌入。輸出內容包含嵌入的維度與前三個值：

```
[384]
[-0.0007759315, 0.018069174, 0.014426488]
```

當您不再需要該模型時，請將其取消部署並刪除，連同其模型群組一併刪除：

```python
model_group_id = ml_client.get_model_info(model_id)["model_group_id"]
ml_client.undeploy_model(model_id)
ml_client.delete_model(model_id)
ml_client.model_access_control.delete_model_group(model_group_id)
```
{% include copy.html %}

## 相關文件

- 如需完整的用戶端文件，請參閱 [`opensearch-py-ml` 文件](https://opensearch-project.github.io/opensearch-py-ml/index.html)。
- 如需用戶端 API 參考文件，請參閱 [`opensearch-py-ml` API 參考文件](https://opensearch-project.github.io/opensearch-py-ml/reference/index.html)。
- 如需 Jupyter notebook 範例，請參閱 [`opensearch-py-ml` 範例](https://opensearch-project.github.io/opensearch-py-ml/examples/index.html)。
- 如需用戶端原始碼，請參閱 [`opensearch-py-ml` GitHub 儲存庫](https://github.com/opensearch-project/opensearch-py-ml)。
- 如需預先訓練模型的更多資訊，請參閱[預先訓練模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/pretrained-models/)。
