---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移至 OpenSearch Serverless NextGen"
nav_order: 55
permalink: /migration-assistant/amazon-opensearch-serverless/
---

# 遷移至 OpenSearch Serverless NextGen

如果您的目標是 Amazon OpenSearch Serverless NextGen 集合，Serverless NextGen 可作為 Migration Assistant 支援之所有來源的目標：Elasticsearch 1.x--2.x、OpenSearch 1.x--2.x、Amazon OpenSearch Service，以及 Apache Solr 6.x--9.x（僅限回填）。遷移步驟與任何其他 OpenSearch 目標相同。請依照來源的教戰手冊操作，並使用本頁的 Serverless NextGen 目標組態。

| 來源 | 回填 | 擷取與重播 |
|:-------|:--------:|:------------------:|
| 自行管理的 Elasticsearch 5.x--8.x | 是 | 是 |
| Elasticsearch 1.x--2.x | 是 | 否（此來源版本不支援） |
| OpenSearch 1.x--2.x | 是 | 是 |
| Amazon OpenSearch Service 或舊版 Elasticsearch Service（5.x+） | 是 | 是 |
| Apache Solr 6.x--9.x | 是 | 否（Solr 不支援擷取與重播） |

## 集合類型

Amazon OpenSearch Serverless NextGen 支援下列集合類型。Migration Assistant 會自動偵測集合類型並據以調整行為。

| 集合類型 | 文件 ID |
|:---------------|:------------|
| `SEARCH` | 保留來源文件 ID |
| `TIMESERIES` | 伺服器產生的 ID（不保留來源 ID）。NextGen 推出時不支援（Classic 版本提供）。 |
| `VECTORSEARCH` | 伺服器產生的 ID（不保留來源 ID） |

如果您的來源資料依賴特定的文件 ID（例如用於查閱或去除重複），請使用 `SEARCH` 集合。

遷移至 `VECTORSEARCH` 集合時，`knn_vector` 欄位對應會自動轉換為 Faiss HNSW，以與 Serverless NextGen 相容，且 `model_id` 參照會被移除（Amazon OpenSearch Serverless NextGen 不支援訓練 API）。

## 將您的集合連線至 Migration Assistant

Migration Assistant 需要下列組態才能存取您的 Amazon OpenSearch Serverless NextGen 集合：

1. 遷移 IAM 角色必須在其 IAM 政策中具有 `aoss:APIAccessAll`（Amazon Elastic Kubernetes Service (EKS) 部署會自動處理此項）。
2. 遷移 IAM 角色必須在您集合的資料存取政策中列為 `Principal`（您必須自行設定此項）。

### 步驟 1：尋找遷移角色 ARN

EKS 部署會建立名為 `<eks-cluster-name>-migrations-role` 的角色。若要尋找該角色，請執行下列命令：

```bash
aws iam list-roles --query "Roles[?contains(RoleName,'migrations-role')].{Name:RoleName,Arn:Arn}" --output table
```
{% include copy.html %}

### 步驟 2：更新您集合的資料存取政策

將遷移角色新增為您集合資料存取政策中的主體。該角色同時需要集合層級與索引層級的權限。

請在 AWS CLI 中執行下列命令：

```bash
aws opensearchserverless create-access-policy \
  --name migration-access \
  --type data \
  --policy '[{
    "Rules": [
      {
        "ResourceType": "collection",
        "Resource": ["collection/<COLLECTION-NAME>"],
        "Permission": [
          "aoss:CreateCollectionItems",
          "aoss:DeleteCollectionItems",
          "aoss:UpdateCollectionItems",
          "aoss:DescribeCollectionItems"
        ]
      },
      {
        "ResourceType": "index",
        "Resource": ["index/<COLLECTION-NAME>/*"],
        "Permission": [
          "aoss:CreateIndex",
          "aoss:DeleteIndex",
          "aoss:UpdateIndex",
          "aoss:DescribeIndex",
          "aoss:ReadDocument",
          "aoss:WriteDocument"
        ]
      }
    ],
    "Principal": ["<MIGRATION-ROLE-ARN>"]
  }]'
```
{% include copy.html %}

將 `<COLLECTION-NAME>` 取代為您的集合名稱，並將 `<MIGRATION-ROLE-ARN>` 取代為步驟 1 取得的 ARN。

如果您的集合已有資料存取政策，請改用 `update-access-policy` 將遷移角色新增至現有的 Principal 清單。詳情請參閱 [Data access control for Amazon OpenSearch Serverless](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/serverless-data-access.html)。
{: .note }

### 步驟 3：設定工作流程

在工作流程組態中，將您的 Amazon OpenSearch Serverless NextGen 集合設定為目標。與受管理的 OpenSearch Service 目標的主要差異在於 `service: aoss`（而非 `service: es`）：

```bash
workflow configure edit
```
{% include copy.html %}

設定目標叢集：

```json
{
  "targetClusters": {
    "target": {
      "endpoint": "https://<collection-id>.aoss.<region>.on.aws",
      "authConfig": {
        "sigv4": {
          "region": "<region>",
          "service": "aoss"
        }
      }
    }
  }
}
```
{% include copy.html %}

接著依照[使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/getting-started/) 中的步驟操作。

## 各來源的教戰手冊

請選擇符合您來源類型的教戰手冊：

- **自行管理/第三方 Elasticsearch 或 OpenSearch** -- 請依照 [Elasticsearch 6.8 → OpenSearch 3.5 教戰手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-elasticsearch-6-8-to-opensearch-3/)，然後將目標叢集區塊取代為前述的 Serverless NextGen 組態。
- **Amazon OpenSearch Service/舊版 Elasticsearch Service** -- 請依照 [Amazon OpenSearch Service → Amazon OpenSearch Serverless NextGen 教戰手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-amazon-opensearch-service-to-serverless/)。
- **Apache Solr** -- 請依照 [Apache Solr 8.11 → OpenSearch 3.5 教戰手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-solr-8.11-to-opensearch-3/)，然後將目標叢集區塊取代為前述的 Serverless NextGen 組態。
