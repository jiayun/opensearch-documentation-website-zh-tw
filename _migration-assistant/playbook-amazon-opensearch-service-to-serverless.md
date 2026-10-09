---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Amazon OpenSearch Service → Amazon OpenSearch Serverless NextGen"
nav_order: 2
parent: Playbooks
permalink: /migration-assistant/playbook-amazon-opensearch-service-to-serverless/
---

# 操作手冊：從 Amazon OpenSearch Service 遷移至 Amazon OpenSearch Serverless NextGen（向量搜尋）

本操作手冊說明如何使用 Migration Assistant，將執行 Elasticsearch 7.10 的 Amazon OpenSearch Service 網域遷移至 Amazon OpenSearch Serverless NextGen 向量搜尋集合。

採用 `VECTORSEARCH` 集合類型的 Amazon OpenSearch Serverless NextGen 提供下列優點：

- **無需叢集管理** -- 無需調整、修補或擴充任何節點。AWS 會自動管理容量。
- **內建向量引擎** -- 專為 k-NN 搜尋、語意搜尋以及檢索增強生成（RAG）工作負載而設計。
- **按用量計費** -- 以 OpenSearch Compute Unit（OCU）為基礎的計費方式，您只需為實際用量付費，而非閒置容量。
- **自動擴充** -- 依需求獨立擴充索引與搜尋容量。
- **內建加密與存取控制** -- 靜態與傳輸中加密，以及細緻的資料存取政策，無需管理安全性外掛程式。

如果您在 Amazon OpenSearch Service 網域上執行向量或 k-NN 工作負載，Serverless NextGen 可免除為這類耗用大量記憶體與運算資源的向量工作負載手動選擇及擴充執行個體類型的需求。
{: .note }

## OpenSearch Service 與 OpenSearch Serverless NextGen 的比較

下表列出 Amazon OpenSearch Service 與 Amazon OpenSearch Serverless NextGen 之間的主要差異。

| 功能 | Amazon OpenSearch Service | Amazon OpenSearch Serverless NextGen |
|:---------|:---------------------------|:----------------------|
| 叢集設定 | 完整的 `_cluster/settings` API | 不支援 |
| 快照/還原 | 支援 | 不支援（請使用 Migration Assistant 回填） |
| ISM/ILM 政策 | 支援 | 不支援 |
| 資料匯入管線 | 支援 | 不支援 |
| 自訂外掛程式 | 支援 | 不支援 |
| 安全性模型 | 細緻存取控制（FGAC） | 資料存取政策（以 IAM 為基礎） |
| 驗證 | 基本驗證、Security Assertion Markup Language（SAML）、IAM | 僅支援 IAM AWS Signature Version 4 |
| 索引範本 | 支援 | 支援（有限制） |
| 別名 | 支援 | 支援 |
| 索引大小上限 | 無硬性限制 | 每個索引 1 TB |

Migration Assistant 僅遷移資料（中繼資料、文件與即時流量）。遷移後，您必須在目標端手動重建 ISM 政策、資料匯入管線與儀表板。
{: .warning }

## 範例預留位置

下表列出本操作手冊使用的範例值。

| 設定 | 值 |
|---------|-------|
| AWS 帳戶 | `111122223333` |
| 區域 | `us-east-2` |
| AWS Identity and Access Management（IAM）角色 | Admin |
| 來源 | Amazon OpenSearch Service 網域（`my-source-domain`，Elasticsearch 7.10） |
| 目標 | Amazon OpenSearch Serverless NextGen 集合（`my-target-collection`，VECTORSEARCH） |
| 部署 | 「Launch into existing virtual private cloud（VPC）」CloudFormation 範本 |
| 階段 | `dev` |

本操作手冊中的帳戶 ID、網域名稱與端點皆為範例。請以您環境中的實際值取代。
{: .note }

## 預估時間

下表提供遷移各階段的預估時間。

| 階段 | 時間 |
|-------|----------|
| 先決條件（Amazon OpenSearch Serverless NextGen 集合、集合群組、政策、IAM、VPC 對等連線） | 15--20 分鐘 |
| 步驟 3：部署 Migration Assistant（CloudFormation + Helm） | 15--25 分鐘 |
| 步驟 4--9：設定並測試連線 | 5--10 分鐘 |
| 步驟 10：試驗性遷移（小型索引） | 15--20 分鐘 |
| 步驟 11：透過變更資料擷取（CDC）進行完整遷移 | 20--30 分鐘 + 追趕重播時間 |
| 端對端總計 | 小型叢集約 90 分鐘 |


## 開始之前

除了[操作手冊的一般先決條件]({{site.url}}{{site.baseurl}}/migration-assistant/playbooks/)之外，開始遷移前請先確認下列事項。

### 來源叢集需求

您的 Amazon OpenSearch Service 網域必須符合下列所有需求：

- 網域執行 Elasticsearch 7.10（或任何[支援的來源版本]({{site.url}}{{site.baseurl}}/migration-assistant/is-migration-assistant-right-for-you/)）。
- 網域位於 VPC 中，且可從您部署 Migration Assistant 的 VPC 存取。
- 您知道網域的 VPC 端點（例如 `https://vpc-my-source-domain-abc123example.us-east-2.es.amazonaws.com`）。
- 若已啟用細緻存取控制（FGAC），請將 Migration Assistant 的 IAM 角色對應為 `MasterUserARN`。

執行下列命令以確認來源網域詳細資訊：

```bash
aws opensearch describe-domain \
  --region us-east-2 \
  --domain-name my-source-domain \
  --query 'DomainStatus.{EngineVersion:EngineVersion,Endpoint:Endpoints.vpc,VPC:VPCOptions.VPCId,Subnets:VPCOptions.SubnetIds,SGs:VPCOptions.SecurityGroupIds,FGAC:AdvancedSecurityOptions.Enabled}' \
  --output table
```
{% include copy.html %}

預期輸出：

```
-----------------------------------------------------------
|                     DescribeDomain                      |
+-----------------+---------------------------------------+
| EngineVersion   | Elasticsearch_7.10                    |
| Endpoint        | vpc-my-source-domain-...    |
| FGAC            | True                                  |
| VPC             | vpc-009ea0f461cc426c6                 |
+-----------------+---------------------------------------+
```

### 目標集合需求

目標 Amazon OpenSearch Serverless NextGen 集合必須依下列方式設定：

- **類型** -- 本操作手冊使用 `VECTORSEARCH`。若是其他工作負載，請使用 `SEARCH`。上市時 NextGen 不支援 `TIMESERIES`（Classic 版本可用）。
- **加密政策** -- 至少一個涵蓋該集合的加密政策。
- **網路政策** -- 依您的需求選擇公用或 VPC 存取。
- **資料存取政策** -- 授權 Migration Assistant 的 IAM 角色完整的索引讀寫權限。

如果您已有集合，請直接前往[步驟 5：對應 Migration Assistant 的 IAM 角色](#step-5-map-the-migration-assistant-iam-role)。否則，請[建立集合](#prerequisite-create-a-collection)。

### 基礎架構需求

需要下列基礎架構：

- 您擁有來源網域所在 VPC 的 VPC ID，以及至少兩個子網路 ID（各自位於不同的可用區）。
- 子網路具有 NAT 閘道存取權（否則您將使用 `--create-vpc-endpoints` 旗標）。
- 您已安裝 AWS CLI 2.x 與 `kubectl`，或您正在使用 AWS CloudShell。
- 您的 AWS 憑證在帳戶 `111122223333` 中具有 Admin 權限。

若上述任一項尚未就緒，請先完成準備工作再繼續。
{: .warning }

## 先決條件：建立集合

完成下列步驟以建立集合。

### 步驟 1：建立加密政策

若要建立加密政策，請執行下列命令：

```bash
aws opensearchserverless create-security-policy \
  --region us-east-2 \
  --name vector-search-enc \
  --type encryption \
  --policy '{
    "Rules": [
      {
        "ResourceType": "collection",
        "Resource": ["collection/my-target-collection"]
      }
    ],
    "AWSOwnedKey": true
  }'
```
{% include copy.html %}

### 步驟 2：建立網路政策

本操作手冊使用公開存取。在正式環境中，請考慮使用 VPC 存取。若要建立網路政策，請執行下列命令：

```bash
aws opensearchserverless create-security-policy \
  --region us-east-2 \
  --name vector-search-net \
  --type network \
  --policy '[{
    "Rules": [
      {
        "ResourceType": "collection",
        "Resource": ["collection/my-target-collection"]
      },
      {
        "ResourceType": "dashboard",
        "Resource": ["collection/my-target-collection"]
      }
    ],
    "AllowFromPublic": true
  }]'
```
{% include copy.html %}

### 步驟 3：建立資料存取政策

此政策會授予帳戶根使用者、Admin 角色及 Migration Assistant 角色存取集合的權限。若要建立資料存取政策，請執行下列命令：

```bash
aws opensearchserverless create-access-policy \
  --region us-east-2 \
  --name vector-search-access \
  --type data \
  --policy '[{
    "Rules": [
      {
        "ResourceType": "collection",
        "Resource": ["collection/my-target-collection"],
        "Permission": [
          "aoss:CreateCollectionItems",
          "aoss:DeleteCollectionItems",
          "aoss:UpdateCollectionItems",
          "aoss:DescribeCollectionItems"
        ]
      },
      {
        "ResourceType": "index",
        "Resource": ["index/my-target-collection/*"],
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
    "Principal": [
      "arn:aws:iam::111122223333:role/Admin",
      "arn:aws:iam::111122223333:root"
    ]
  }]'
```
{% include copy.html %}

### 步驟 4：建立集合群組

NextGen 集合必須隸屬於某個集合群組。若要建立一個，請執行下列命令：

```bash
aws opensearchserverless create-collection-group \
  --region us-east-2 \
  --name vector-search-group \
  --generation NEXTGEN \
  --standby-replicas ENABLED
```
{% include copy.html %}

### 步驟 5：建立集合

若要建立集合，請執行下列命令：

```bash
aws opensearchserverless create-collection \
  --region us-east-2 \
  --name my-target-collection \
  --type VECTORSEARCH \
  --collection-group-name vector-search-group
```
{% include copy.html %}

等待集合變成 ACTIVE（約 2--3 分鐘）：

```bash
watch -n 10 "aws opensearchserverless batch-get-collection \
  --region us-east-2 \
  --names my-target-collection \
  --query 'collectionDetails[0].{Status:status,Endpoint:collectionEndpoint}' \
  --output table"
```
{% include copy.html %}

當 `Status` 顯示 `ACTIVE` 時，請記錄端點。下列範例顯示本操作手冊的預期輸出：

```
https://3nbrhts7rv9jxatilz9e.aoss.us-east-2.on.aws
```

### 步驟 6：驗證您能否連線至集合

如果您尚未安裝 `awscurl`，請執行下列命令來安裝： 

```bash
pip install awscurl
```
{% include copy.html %} 

若要驗證您能否連線至集合，請執行下列命令：

```bash
awscurl --service aoss --region us-east-2 \
  "https://3nbrhts7rv9jxatilz9e.aoss.us-east-2.on.aws/"
```
{% include copy.html %}

您應該會看到包含 OpenSearch 版本的 JSON 回應。

## 步驟 1：選擇遷移方式

在設定工作流程之前，請先選取下列其中一種遷移方式。

### 選項 A：計畫性停機

若採用計畫性停機遷移，請依照下列步驟進行：

1. 停止對來源網域的寫入。
2. 建立快照。
3. 遷移中繼資料。
4. 回填文件。
5. 驗證目標。
6. 將用戶端指向 Serverless NextGen 集合端點。

如果您不確定該選取哪種方式，請使用計畫性停機，因為它涉及的元件較少且風險較低。
{: .note }

### 選項 B：零停機

若採用零停機遷移，請依照下列步驟進行：

1. 先開始擷取。
2. 將用戶端路由至擷取代理。
3. 建立快照。
4. 遷移中繼資料。
5. 回填文件。
6. 重播擷取的流量，直到目標趕上進度。
7. 驗證目標。
8. 將用戶端切換至 Serverless NextGen 集合端點。

如果您選擇此選項，您的用戶端必須為索引與更新作業傳送**明確的文件 ID**。如果您的應用程式依賴自動產生的 ID，請勿使用 Capture and Replay。
{: .warning }


## 步驟 2：收集您的 VPC 資訊

收集 Migration Assistant 部署會重複使用的 VPC 與子網路資訊。

尋找來源網域的 VPC：

```bash
aws opensearch describe-domain \
  --region us-east-2 \
  --domain-name my-source-domain \
  --query 'DomainStatus.VPCOptions.{VPCId:VPCId,SubnetIds:SubnetIds,SecurityGroupIds:SecurityGroupIds}' \
  --output json
```
{% include copy.html %}

記錄 VPC ID（`vpc-009ea0f461cc426c6`）與子網路 ID。

尋找子網路詳細資料：

```bash
aws ec2 describe-subnets \
  --region us-east-2 \
  --filters "Name=vpc-id,Values=vpc-009ea0f461cc426c6" \
  --query "Subnets[*].{SubnetId:SubnetId,AZ:AvailabilityZone,CidrBlock:CidrBlock,Name:Tags[?Key=='Name']|[0].Value}" \
  --output table
```
{% include copy.html %}

請至少選取兩個私有子網路，且每個子網路位於不同的可用區域。將它們記錄為以逗號分隔的字串。

您可以將 Migration Assistant 部署到與來源網域**相同的 VPC**，或使用 VPC 對等互連部署到**不同的 VPC**。將 Migration Assistant 部署到相同的 VPC 所需的組態較少。如果您部署到不同的 VPC，請參閱[疑難排解章節](#source-and-target-are-in-different-vpcs)。
{: .note }


## 步驟 3：在 EKS 上部署 Migration Assistant

此步驟會使用啟動指令碼將 Migration Assistant 部署到 Amazon Elastic Kubernetes Service (EKS)。

下載啟動指令碼：

```bash
curl -sL -o aws-bootstrap.sh \
  "https://github.com/opensearch-project/opensearch-migrations/releases/latest/download/aws-bootstrap.sh" \
  && chmod +x aws-bootstrap.sh
```
{% include copy.html %}

部署到與來源網域**相同的 VPC**：

```bash
./aws-bootstrap.sh \
  --deploy-import-vpc-cfn \
  --stack-name MA \
  --stage dev \
  --vpc-id vpc-009ea0f461cc426c6 \
  --subnet-ids subnet-055497d9551cc298a,subnet-0a776b7d7724f22ae \
  --region us-east-2
```
{% include copy.html %}

這會部署 CloudFormation 堆疊，建立 Amazon EKS 叢集、Amazon Elastic Container Registry (Amazon ECR) 儲存庫、IAM 角色，然後安裝 Migration Assistant Helm chart。部署約需 15--25 分鐘。

<details>
<summary><strong>適用於隔離子網路（無 NAT 閘道／無網際網路）</strong></summary>

新增 `--create-vpc-endpoints` 旗標：

```bash
./aws-bootstrap.sh \
  --deploy-import-vpc-cfn \
  --stack-name MA \
  --stage dev \
  --vpc-id vpc-009ea0f461cc426c6 \
  --subnet-ids subnet-055497d9551cc298a,subnet-0a776b7d7724f22ae \
  --create-vpc-endpoints \
  --region us-east-2
```
{% include copy.html %}

</details>

驗證部署：

```bash
aws eks update-kubeconfig --region us-east-2 --name migration-eks-cluster-dev-us-east-2
kubectl get pods -n ma
```
{% include copy.html %}

所有 Pod 都應顯示 `Running`，且 `1/1` 就緒。


## 步驟 4：確認 CloudFormation 輸出

若要確認 CloudFormation 輸出，請執行下列命令：

```bash
aws cloudformation describe-stacks \
  --region us-east-2 \
  --stack-name MA \
  --query "Stacks[0].Outputs[?contains(OutputKey,'MigrationsExportString')].OutputValue" \
  --output text
```
{% include copy.html %}

下表列出主要的輸出值。

| 變數 | 預期值 |
|----------|---------------|
| `MIGRATIONS_EKS_CLUSTER_NAME` | `migration-eks-cluster-dev-us-east-2` |
| `SNAPSHOT_ROLE` | `arn:aws:iam::111122223333:role/migration-eks-cluster-dev-us-east-2-snapshot-role` |
| `EKS_CLUSTER_SECURITY_GROUP` | 新 EKS 叢集的安全群組 ID |

預設的 Amazon Simple Storage Service (Amazon S3) 儲存貯體為 `s3://migrations-default-111122223333-dev-us-east-2`。


## 步驟 5：對應 Migration Assistant IAM 角色

部署後，請完成下列步驟，將來源與目標的存取權授予 Migration Assistant IAM 角色。

### 步驟 1：更新 Amazon OpenSearch Serverless NextGen 資料存取原則

部署 Migration Assistant 後，將 `migrations-role` 和 `snapshot-role` 新增至 Amazon OpenSearch Serverless NextGen 資料存取原則：

```bash
# Get the current policy version
POLICY_VERSION=$(aws opensearchserverless get-access-policy \
  --region us-east-2 \
  --name vector-search-access \
  --type data \
  --query 'accessPolicyDetail.policyVersion' \
  --output text)

aws opensearchserverless update-access-policy \
  --region us-east-2 \
  --name vector-search-access \
  --type data \
  --policy-version "$POLICY_VERSION" \
  --policy '[{
    "Rules": [
      {
        "ResourceType": "collection",
        "Resource": ["collection/my-target-collection"],
        "Permission": [
          "aoss:CreateCollectionItems",
          "aoss:DeleteCollectionItems",
          "aoss:UpdateCollectionItems",
          "aoss:DescribeCollectionItems"
        ]
      },
      {
        "ResourceType": "index",
        "Resource": ["index/my-target-collection/*"],
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
    "Principal": [
      "arn:aws:iam::111122223333:role/Admin",
      "arn:aws:iam::111122223333:root",
      "arn:aws:iam::111122223333:role/migration-eks-cluster-dev-us-east-2-migrations-role",
      "arn:aws:iam::111122223333:role/migration-eks-cluster-dev-us-east-2-snapshot-role"
    ]
  }]'
```
{% include copy.html %}

### 步驟 2：在來源網域上對應 Migration Assistant 角色

如果來源網域已啟用精細存取控制 (FGAC)，則必須將 Migration Assistant 角色設定為 `MasterUserARN`：

```bash
aws opensearch update-domain-config \
  --region us-east-2 \
  --domain-name my-source-domain \
  --advanced-security-options '{
    "Enabled": true,
    "MasterUserOptions": {
      "MasterUserARN": "arn:aws:iam::111122223333:role/migration-eks-cluster-dev-us-east-2-migrations-role"
    }
  }'
```
{% include copy.html %}

等待網域更新完成：

```bash
watch -n 10 "aws opensearch describe-domain \
  --region us-east-2 \
  --domain-name my-source-domain \
  --query 'DomainStatus.Processing'"
```
{% include copy.html %}

當 `Processing` 傳回 `False` 時，表示網域已就緒。

這會取代任何現有的 `MasterUserARN`。如果您需要保留現有的組態，請改為透過 OpenSearch Security API 將 Migration Assistant 角色對應至 `all_access` 後端角色。
{: .warning }


## 步驟 6：設定安全群組存取

尋找 Migration Assistant EKS 叢集安全群組：

```bash
MA_SG=$(aws eks describe-cluster \
  --region us-east-2 \
  --name migration-eks-cluster-dev-us-east-2 \
  --query "cluster.resourcesVpcConfig.clusterSecurityGroupId" \
  --output text)
echo "MA EKS Security Group: $MA_SG"
```
{% include copy.html %}

新增輸入規則，讓 Migration Assistant 可以透過連接埠 443 連線至來源網域：

```bash
aws ec2 authorize-security-group-ingress \
  --region us-east-2 \
  --group-id sg-07dcc2b6423c745a0 \
  --protocol tcp \
  --port 443 \
  --source-group "$MA_SG"
```
{% include copy.html %}

目標是具備公開網路存取權的 Amazon OpenSearch Serverless NextGen 集合，因此目標不需要安全群組規則。如果您為該集合設定了 VPC 存取，請同時為該集合的 VPC 端點安全群組新增輸入規則。
{: .note }


## 步驟 7：連線至 Migration Console

連線至 Migration Console：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

確認已安裝的版本：

```bash
console --version
```
{% include copy.html %}

預期輸出：`Migration Assistant 3.1.1` (或更新版本)。

### 在來源網域上註冊 Amazon S3 快照儲存庫

Amazon OpenSearch Service 需要 `snapshot-role` 才能寫入 Amazon S3。請使用 CloudFormation 輸出中的 `snapshot-role` 註冊儲存庫：

```bash
console clusters curl source /_snapshot/migration-repo \
  -XPUT -H "Content-Type: application/json" \
  -d '{
    "type": "s3",
    "settings": {
      "bucket": "migrations-default-111122223333-dev-us-east-2",
      "region": "us-east-2",
      "role_arn": "arn:aws:iam::111122223333:role/migration-eks-cluster-dev-us-east-2-snapshot-role",
      "base_path": "aos-to-aoss-snapshots"
    }
  }'
```
{% include copy.html %}

確認儲存庫：

```bash
console clusters curl source /_snapshot/migration-repo/_verify?pretty
```
{% include copy.html %}

所有節點都應出現在輸出中。

與自行管理的 Elasticsearch 不同，Amazon OpenSearch Service 使用 IAM `role_arn` 來存取 Amazon S3，而非使用金鑰庫憑證。`snapshot-role` 必須具有信任原則，允許 OpenSearch Service `Principal` (`es.amazonaws.com`) 擔任該角色。
{: .note }


## 步驟 8：建立工作流程組態

若要載入版本相符的範例並開啟編輯器，請執行下列命令：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

如需所有可用欄位、其類型、預設值與說明的互動式參考，請參閱 [Migration Assistant Schema Viewer](https://opensearch-project.github.io/opensearch-migrations/)。

將工作流程組態檔案的內容取代為下列組態。將 `<PILOT_INDEX_NAME>` 取代為一個小型且非關鍵索引的名稱 (例如 `test-index`)：

```json
{
  "sourceClusters": {
    "source": {
      "endpoint": "https://vpc-my-source-domain-abc123example.us-east-2.es.amazonaws.com",
      "allowInsecure": false,
      "version": "ES 7.10",
      "authConfig": {
        "sigv4": {
          "region": "us-east-2",
          "service": "es"
        }
      },
      "snapshotInfo": {
        "repos": {
          "migration-repo": {
            "awsRegion": "us-east-2",
            "s3RepoPathUri": "s3://migrations-default-111122223333-dev-us-east-2/aos-to-aoss-snapshots",
            "s3RoleArn": "arn:aws:iam::111122223333:role/migration-eks-cluster-dev-us-east-2-snapshot-role"
          }
        },
        "snapshots": {
          "migration-snapshot": {
            "repoName": "migration-repo",
            "config": {
              "createSnapshotConfig": {
                "indexAllowlist": ["<PILOT_INDEX_NAME>"],
                "includeGlobalState": true
              }
            }
          }
        }
      }
    }
  },
  "targetClusters": {
    "target": {
      "endpoint": "https://3nbrhts7rv9jxatilz9e.aoss.us-east-2.on.aws",
      "allowInsecure": false,
      "authConfig": {
        "sigv4": {
          "region": "us-east-2",
          "service": "aoss"
        }
      }
    }
  },
  "snapshotMigrationConfigs": [
    {
      "fromSource": "source",
      "toTarget": "target",
      "perSnapshotConfig": {
        "migration-snapshot": [
          {
            "metadataMigrationConfig": {
              "indexAllowlist": ["<PILOT_INDEX_NAME>"]
            },
            "documentBackfillConfig": {
              "podReplicas": 4
            }
          }
        ]
      }
    }
  ]
}
```
{% include copy.html %}

以下是與網域對網域遷移的主要差異：

- **來源**使用 `sigv4` 搭配 `service: "es"`：Amazon OpenSearch Service 使用 IAM 驗證，而非基本驗證。
- **目標**使用 `sigv4` 搭配 `service: "aoss"`：Amazon OpenSearch Serverless NextGen 需要 `aoss` 服務名稱，才能進行 AWS Signature Version 4 簽署。
- **必須要有 `s3RoleArn`**：Amazon OpenSearch Service 需要 IAM 角色才能將快照寫入 Amazon S3 (與使用金鑰庫憑證的自行管理 Elasticsearch 不同)。
- **沒有 `multiTypeBehavior`**：Elasticsearch 7.10 已使用單一類型索引，因此不需要類型對應轉換。

確認組態：

```bash
workflow configure view
```
{% include copy.html %}


## 步驟 9：測試連線

若要驗證 Migration Console 是否能連線至來源與目標，請執行以下命令：

```bash
console clusters connection-check
```
{% include copy.html %}

來源與目標都應顯示 `Successfully connected!`。

如果來源回傳連線逾時，請驗證以下項目：

1. Migration Assistant 已部署在與來源網域相同的 VPC 中（或已設定 VPC 對等連線）。
2. 來源網域的安全性群組允許來自 Migration Assistant EKS 叢集安全性群組的 TCP 443 入站流量。

如果目標回傳 403，請驗證以下項目：

1. Amazon OpenSearch Serverless NextGen 資料存取政策包含 Migration Assistant 的 migrations 角色。
2. 網路政策允許來自 Migration Assistant pod 的存取。

若要手動測試連線，請執行以下命令：

```bash
console clusters curl source /
console clusters curl target /
```
{% include copy.html %}


## 步驟 10：執行試驗遷移

在遷移所有索引之前，先在一個小型索引上執行試驗遷移。

提交工作流程：

```bash
workflow submit
workflow manage
```
{% include copy.html %}

`workflow manage` 命令會開啟互動式文字使用者介面 (TUI)。請使用它來監控進度、檢視記錄檔，以及核准關卡。

當工作流程在核准關卡暫停時（顯示為 `⟳`），請檢閱並核准輸出：

```bash
# Approve metadata evaluation
workflow approve step "*.evaluatemetadata"

# Approve metadata migration
workflow approve step "*.migratemetadata"
```
{% include copy.html %}

關卡名稱為**小寫**。您也可以直接在 `workflow manage` TUI 中核准關卡。
{: .note }

工作流程完成後，請驗證中繼資料與文件：

```bash
console clusters curl target /_cat/indices?v
console clusters curl target /<PILOT_INDEX_NAME>/_mapping
console clusters curl target /<PILOT_INDEX_NAME>/_count
console clusters curl target /<PILOT_INDEX_NAME>/_search?size=5&pretty
```
{% include copy.html %}

請確認來源與目標上的文件數量一致。

如果試驗遷移失敗，請編輯組態並重新提交：

```bash
workflow configure edit
workflow submit
workflow manage
```
{% include copy.html %}

在試驗遷移成功完成之前，請勿開始完整遷移。
{: .note }


## 步驟 11：執行完整遷移

編輯組態以擴充允許清單：

```bash
workflow configure edit
```
{% include copy.html %}

將 `indexAllowlist` 設為空陣列以遷移所有索引：

```json
"metadataMigrationConfig": {
  "indexAllowlist": []
}
```
{% include copy.html %}

更新 `createSnapshotConfig`：

```json
"createSnapshotConfig": {
  "indexAllowlist": [],
  "includeGlobalState": true
}
```
{% include copy.html %}

以下章節說明各種遷移方式的步驟。請依照您在步驟 1 中所選方式對應的章節操作。

### 計劃性停機路徑

若採用計劃性停機遷移，請依照以下步驟：

1. **停止對來源網域的寫入。**
2. 提交工作流程：

   ```bash
   workflow submit
   workflow manage
   ```
   {% include copy.html %}

3. 在驗證每個階段後核准關卡。
4. 回填完成後，驗證目標：

   ```bash
   console clusters curl target /_cat/indices?v
   console clusters curl target /_cat/aliases?v
   ```
   {% include copy.html %}

5. 檢閱 Migration Assistant 不會遷移的元件（ISM 或 ILM 政策、資料匯入管線、儀表板、叢集設定）。Amazon OpenSearch Serverless NextGen 不支援這些功能。在繼續之前，請判斷您的工作負載是否需要替代方案。
6. 將用戶端指向 Serverless NextGen 集合端點：`https://3nbrhts7rv9jxatilz9e.aoss.us-east-2.on.aws`。
7. 將用戶端驗證從基本驗證或使用 `service: es` 的 IAM AWS Signature Version 4，更新為使用 `service: aoss` 的 IAM AWS Signature Version 4。

### 零停機路徑

若採用零停機遷移，請依序完成以下章節。

#### 步驟 1：設定 traffic 區段

若要在工作流程組態中新增 `traffic` 區段，請開啟編輯器：

```bash
workflow configure edit
```
{% include copy.html %}

在與 `sourceClusters`、`targetClusters` 和 `snapshotMigrationConfigs` 相同的層級新增以下 `traffic` 區塊：

```json
"traffic": {
  "proxies": {
    "capture": {
      "source": "source",
      "proxyConfig": {
        "listenPort": 443,
        "podReplicas": 2
      }
    }
  },
  "replayers": {
    "replay": {
      "fromProxy": "capture",
      "toTarget": "target",
      "dependsOnSnapshotMigrations": [
        {
          "source": "source",
          "snapshot": "migration-snapshot"
        }
      ],
      "replayerConfig": {
        "podReplicas": 2,
        "speedupFactor": 2.0
      }
    }
  }
}
```
{% include copy.html %}

將 `indexAllowlist` 設為空陣列以遷移所有索引：

```json
"metadataMigrationConfig": {
  "indexAllowlist": []
}
```
{% include copy.html %}

#### 步驟 2：提交工作流程

若要提交工作流程並開啟監控介面，請執行以下命令：

```bash
workflow submit
workflow manage
```
{% include copy.html %}

工作流程會建立五條平行軌道：Apache Kafka 叢集、擷取代理程式、快照、快照遷移，以及 Traffic Replayer。快照會等待擷取代理程式就緒後才繼續。

#### 步驟 3：尋找擷取代理程式端點

擷取代理程式使用來源網域的連接埠（Amazon OpenSearch Service 為 443）。若要尋找端點，請執行以下命令：

```bash
kubectl get svc capture -n ma
```
{% include copy.html %}

`EXTERNAL-IP` 欄位會顯示 Network Load Balancer 端點。請將您的應用程式用戶端重新導向至此端點。

擷取代理程式會將所有請求轉送至來源網域，並同時將其記錄到 Kafka 以供重播。擷取代理程式使用 AWS Signature Version 4 對來源進行驗證，因此您的用戶端可以繼續使用其現有的驗證方式。
{: .note }

#### 步驟 4：核准工作流程步驟

若要執行核准動作，請執行以下命令：

```bash
workflow approve step "*.evaluatemetadata"
workflow approve step "*.migratemetadata"
```
{% include copy.html %}

#### 步驟 5：監控重播進度

回填完成後，Replayer 會開始處理擷取的流量：

```bash
kubectl logs deployment/capture-target-replay -n ma --tail=5
```
{% include copy.html %}

找出 `ReplayHeartbeat` 一行：

```log
ReplayHeartbeat - tasksOutstanding=437 schedulingLag=1s lastCompletedSourceTime=2026-05-03T16:01:16.565Z targetResponses={}
```

下表說明心跳輸出中的欄位。

| 欄位 | 意義 |
|-------|---------|
| `tasksOutstanding` | 仍在重播中的已擷取請求。應逐漸減少至 0。 |
| `lastCompletedSourceTime` | 最近重播之請求的時間戳記。應接近目前時間。 |
| `targetResponses` | 來自目標的 HTTP 回應碼。空的 `{}` 表示尚未重播任何寫入請求。 |
| `schedulingLag` | Replayer 與即時流量之間的延遲。重播完成時應接近 0。 |

#### 步驟 6：驗證文件數量是否相符

若要比較來源與目標之間的文件數量，請執行下列命令：

```bash
console clusters curl source /_cat/indices?v
console clusters curl target /_cat/indices?v
```
{% include copy.html %}

重播完成後，目標上的文件數量應與來源相符。

#### 步驟 7：將流量切換至目標

當重播完成且驗證確認目標正確後，請將應用程式用戶端從擷取代理程式直接切換至 Serverless NextGen 集合端點：

```
https://3nbrhts7rv9jxatilz9e.aoss.us-east-2.on.aws
```

將用戶端的 AWS Signature Version 4 簽署從 `service: es` 更新為 `service: aoss`。


## 步驟 12：保留來源作為備援

切換後請勿立即刪除來源網域。請保留來源至少 24 至 72 小時，同時觀察目標集合健康狀態、應用程式錯誤率及作業工具。


## 步驟 13：移除遷移基礎設施

移除 Migration Assistant 之前，請確認下列所有事項：

1. 所有用戶端流量都直接指向 Serverless NextGen 集合，不再指向擷取代理程式。
2. 不再需要擷取代理程式與 Replayer。
3. 您已保留來源網域作為備援至少 24--72 小時。
4. 目標集合健康狀態良好，且應用程式錯誤率正常。

若有任何用戶端仍將流量傳送至擷取代理程式端點，當您移除 Migration Assistant 時，該流量將會遺失。繼續進行之前，請確認所有用戶端都已重新導向至目標。
{: .warning }

### 步驟 1：移除 Helm release 與命名空間

若要移除 Migration Assistant Helm release 並刪除命名空間，請執行下列命令：

```bash
helm uninstall -n ma ma
kubectl -n ma delete pvc --all
kubectl delete namespace ma --timeout=120s
```
{% include copy.html %}

### 步驟 2：刪除 CloudFormation 堆疊

若要刪除 CloudFormation 堆疊及所有相關資源，請執行下列命令：

```bash
aws cloudformation delete-stack --region us-east-2 --stack-name MA
aws cloudformation wait stack-delete-complete --region us-east-2 --stack-name MA
```
{% include copy.html %}

這會刪除 Migration Assistant 所建立的 Amazon EKS 叢集、Amazon ECR 儲存庫、IAM 角色及 VPC 端點。它**不會**刪除來源網域、Serverless NextGen 集合或 Amazon S3 快照儲存貯體。

### 步驟 3 (選用)：刪除快照儲存貯體

若要刪除快照儲存貯體，請執行下列命令：

```bash
aws s3 rb s3://migrations-default-111122223333-dev-us-east-2 --force
```
{% include copy.html %}

### 步驟 4 (選用)：刪除 Amazon OpenSearch Serverless NextGen 集合

若您為了測試而建立該集合，且不再需要它，請執行下列命令：

```bash
aws opensearchserverless delete-collection \
  --region us-east-2 \
  --id 3nbrhts7rv9jxatilz9e
```
{% include copy.html %}

接著移除政策：

```bash
aws opensearchserverless delete-access-policy \
  --region us-east-2 --name vector-search-access --type data

aws opensearchserverless delete-security-policy \
  --region us-east-2 --name vector-search-net --type network

aws opensearchserverless delete-security-policy \
  --region us-east-2 --name vector-search-enc --type encryption
```
{% include copy.html %}


## 驗證

工作流程完成後，請從三個層級驗證遷移。

### 層級 1：文件數量比較

針對每個使用者索引，比較來源與目標之間的文件數量：

```bash
console clusters curl source /_cat/indices?v
console clusters curl target /_cat/indices?v
```
{% include copy.html %}

針對每個使用者索引，驗證數量是否相符：

```bash
console clusters curl source /<INDEX_NAME>/_count
console clusters curl target /<INDEX_NAME>/_count
```
{% include copy.html %}

### 層級 2：狀態碼比較 (tuple 指標)

若您使用了零停機路徑，Replayer 會將 `tupleComparison` 指標寫入 CloudWatch：

```bash
aws logs start-query \
  --region us-east-2 \
  --log-group-name "/metrics/OpenSearchMigrations" \
  --start-time $(date -u -v-3H +%s) \
  --end-time $(date -u +%s) \
  --query-string 'fields @message
    | filter @message like /tupleComparison/
    | parse @message /\"method\":\"(?<method>[^\"]+)\".*\"sourceStatusCode\":\"(?<srcCode>[^\"]+)\".*\"statusCodesMatch\":\"(?<match>[^\"]+)\".*\"targetStatusCode\":\"(?<tgtCode>[^\"]+)\"/
    | stats count() as requests by method, srcCode, tgtCode, match
    | sort requests desc'
```
{% include copy.html %}

等待幾秒鐘，然後擷取結果：

```bash
aws logs get-query-results --region us-east-2 --query-id <QUERY_ID>
```
{% include copy.html %}

請調查涉及 `POST` 或 `PUT` 方法的任何不相符情形---這些是寫入作業，若不相符可能代表資料遺失。

### 層級 3：範例查詢比較

在兩個叢集上執行具代表性的查詢並比較結果：

```bash
console clusters curl source /<INDEX_NAME>/_search?size=5&pretty
console clusters curl target /<INDEX_NAME>/_search?size=5&pretty
```
{% include copy.html %}

### 對應驗證

驗證索引對應是否已正確遷移：

```bash
console clusters curl target /<INDEX_NAME>/_mapping
```
{% include copy.html %}

## 重新連線至 Migration Console

若您需要在新的 shell 工作階段中重新連線至 Migration Console，請執行下列命令：

```bash
aws eks update-kubeconfig --region us-east-2 --name migration-eks-cluster-dev-us-east-2
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

## 疑難排解

以下是常見問題及其解決方式。

### 目標傳回 403 forbidden

Migration Assistant IAM 角色未包含在 Amazon OpenSearch Serverless NextGen 資料存取政策中。請更新政策：

```bash
POLICY_VERSION=$(aws opensearchserverless get-access-policy \
  --region us-east-2 --name vector-search-access --type data \
  --query 'accessPolicyDetail.policyVersion' --output text)

echo "Current policy version: $POLICY_VERSION"
```
{% include copy.html %}

接著使用正確的政策版本，從[步驟 5：對應 Migration Assistant IAM 角色](#step-5-map-the-migration-assistant-iam-role)重新執行 `update-access-policy` 命令。

### 來源傳回連線逾時

1. 驗證 Migration Assistant 與來源網域位於相同的 VPC：

   ```bash
   aws eks describe-cluster \
     --region us-east-2 \
     --name migration-eks-cluster-dev-us-east-2 \
     --query 'cluster.resourcesVpcConfig.vpcId' \
     --output text
   ```
   {% include copy.html %}

2. 驗證來源網域的安全群組允許 Migration Assistant EKS 叢集安全群組在連接埠 443 上進行連線。

### 來源與目標位於不同的 VPC

若 Migration Assistant 與來源網域位於不同的 VPC，請建立 VPC 對等互連連線：

```bash
PEERING_ID=$(aws ec2 create-vpc-peering-connection \
  --region us-east-2 \
  --vpc-id <MA_VPC_ID> \
  --peer-vpc-id <SOURCE_VPC_ID> \
  --query "VpcPeeringConnection.VpcPeeringConnectionId" \
  --output text)

aws ec2 accept-vpc-peering-connection \
  --region us-east-2 \
  --vpc-peering-connection-id "$PEERING_ID"

# Add routes in both directions
aws ec2 create-route \
  --region us-east-2 \
  --route-table-id <MA_PRIVATE_ROUTE_TABLE> \
  --destination-cidr-block <SOURCE_VPC_CIDR> \
  --vpc-peering-connection-id "$PEERING_ID"

aws ec2 create-route \
  --region us-east-2 \
  --route-table-id <SOURCE_ROUTE_TABLE> \
  --destination-cidr-block <MA_VPC_CIDR> \
  --vpc-peering-connection-id "$PEERING_ID"
```
{% include copy.html %}

接著將 Migration Assistant EKS 叢集安全群組新增至來源網域的安全群組輸入規則 ([步驟 6：設定安全群組存取](#step-6-configure-security-group-access))。請使用 Migration Assistant VPC CIDR 而非安全群組參照，因為跨 VPC 安全群組參照需要對等互連連線。

### 快照儲存庫註冊失敗

對於 Amazon OpenSearch Service，快照角色必須：
1. 包含允許對快照儲存貯體執行 `s3:ListBucket`、`s3:GetObject`、`s3:PutObject`、`s3:DeleteObject` 的 IAM 政策。
2. 包含允許 `es.amazonaws.com` 擔任該角色的信任政策。
3. 透過 `role_arn` 設定傳遞給 `_snapshot` API。

驗證快照角色的信任政策：

```bash
aws iam get-role \
  --role-name migration-eks-cluster-dev-us-east-2-snapshot-role \
  --query 'Role.AssumeRolePolicyDocument' \
  --output json
```
{% include copy.html %}

### 重新提交時的一致性防護錯誤

首先，刪除過期的自訂資源：

```bash
kubectl delete snapshotmigration --all -n ma
kubectl delete datasnapshot --all -n ma
kubectl delete capturedtraffic --all -n ma
kubectl delete captureproxy --all -n ma
kubectl delete trafficreplay --all -n ma
kubectl delete kafkacluster --all -n ma
```
{% include copy.html %}

然後重新提交工作流程：

```bash
workflow submit
```
{% include copy.html %}

### Amazon OpenSearch Serverless NextGen 錯誤

下列錯誤是 Amazon OpenSearch Serverless NextGen 目標特有的。

#### 目標上發生 Index not found 例外

Amazon OpenSearch Serverless NextGen 不支援 `_cluster/settings` API，也不像 Amazon OpenSearch Service 那樣支援透過範本自動建立索引。請在回填之前確認中繼資料遷移已成功完成：

```bash
console clusters curl target /_cat/indices?v
```
{% include copy.html %}

#### 發生安全性例外與權限錯誤

Amazon OpenSearch Serverless NextGen 資料存取政策缺少權限。請確保該政策同時包含 Migration Assistant 角色的集合層級與索引層級權限。

#### 大量編製索引傳回 413：請求過大

Amazon OpenSearch Serverless NextGen 有 10 MB 的請求承載限制。如果您的文件很大，請在工作流程組態中減少大量批次大小：

```json
"documentBackfillConfig": {
  "podReplicas": 4,
  "maxBulkSizeBytes": 5242880
}
```
{% include copy.html %}



## 相關文件

如需更多資訊，請參閱下列資源：

- [Migration Assistant 是否適合您？]({{site.url}}{{site.baseurl}}/migration-assistant/is-migration-assistant-right-for-you/)
- [遷移至 OpenSearch Serverless NextGen]({{site.url}}{{site.baseurl}}/migration-assistant/amazon-opensearch-serverless/)
- [部署至 EKS]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/deploying-to-eks/)
- [使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/getting-started/)
- [回填]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/backfill/)
- [移除 Migration Assistant]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/remove-migration-infrastructure/)
- [Elasticsearch 6.8 → OpenSearch 3.5 操作手冊]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-elasticsearch-6-8-to-opensearch-3/)
- [Migration Assistant Schema Viewer](https://opensearch-project.github.io/opensearch-migrations/)
