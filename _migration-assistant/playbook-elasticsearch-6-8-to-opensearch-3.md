---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Elasticsearch 6.8 → OpenSearch 3.5"
nav_order: 1
parent: Playbooks
permalink: /migration-assistant/playbook-elasticsearch-6-8-to-opensearch-3/
redirect_from:
  - /migration-assistant/playbook-elasticsearch-6-8-to-opensearch-3-Kubernetes/
---

# 操作手冊：在 EKS 上從 Elasticsearch 6.8 遷移至 OpenSearch 3.5 (現有 VPC)

本操作手冊將常見的 AWS 遷移模式轉化為一份具體的執行手冊：從執行於 Amazon Elastic Kubernetes Service (EKS) 上的自我管理 Elasticsearch 6.8 叢集，遷移至 Amazon OpenSearch Service 3.5，並將 Migration Assistant 部署到現有的虛擬私人雲端 (VPC) 中。

此模式適用於從具備自我管理外掛程式、自簽憑證及應用程式自有憑證的自我管理搜尋叢集，遷移至具備 VPC 隔離、以 AWS Identity and Access Management (IAM) 為基礎的存取控制，並降低持續維運負擔的受管目標環境。

本操作手冊刻意設計為端對端流程，涵蓋來源準備、EKS 部署、工作流程組態、試驗遷移、完整遷移、驗證、切換及移除。

## 範例預留位置

請將下列預留位置替換為您環境中的實際值。

| 預留位置 | 意義 |
|:------------|:--------|
| `<ACCOUNT_ID>` | 託管遷移環境的 AWS 帳戶 ID |
| `<REGION>` | AWS 區域，例如 `us-east-2` |
| `<STAGE>` | 部署標籤，例如 `dev` 或 `prod` |
| `<YOUR_VPC_ID>` | 部署 Migration Assistant 的現有 VPC |
| `<SUBNET_1>,<SUBNET_2>` | 位於不同可用區的至少兩個子網路 |
| `<SOURCE_ENDPOINT>` | Elasticsearch 端點或 Network Load Balancer 的 DNS 名稱 |
| `<TARGET_DOMAIN_NAME>` | OpenSearch Service 網域名稱 |
| `<TARGET_DOMAIN_ENDPOINT>` | OpenSearch Service 網域端點 |
| `<PILOT_INDEX_NAME>` | 用於試驗執行的小型非關鍵索引 |

## 預估時間

下表提供遷移各個階段的預估持續時間。

| 階段 | 一般持續時間 |
|:------|:-----------------|
| 來源準備 (外掛程式、S3 存取、快照儲存庫) | 15 至 25 分鐘 |
| 在 EKS 上部署 Migration Assistant | 15 至 25 分鐘 |
| 建立組態並測試連線能力 | 5 至 10 分鐘 |
| 試驗遷移 | 15 至 20 分鐘 |
| 僅回填的完整遷移 | 取決於資料量與目標匯入容量 |
| 零停機的完整遷移 | 回填持續時間加上重播追趕時間 |

對於零停機遷移，重播持續時間取決於回填期間累積的流量量，以及為 Replayer 設定的 `speedupFactor`。一般起始值為 `1.5` 至 `2.0`。請監控目標叢集，確認其能夠承受重播速率。

## 開始之前

除了[一般操作手冊先決條件]({{site.url}}{{site.baseurl}}/migration-assistant/playbooks/)之外，請在開始遷移前確認下列事項。如果您的環境有所不同，請據此調整網路與身分組態。

### 來源叢集需求

您的來源叢集必須符合下列所有需求：

- 可從 Migration Assistant 執行所在的 VPC 存取。
- 您知道來源端點。
- 您知道來源驗證方法。
- 可將快照寫入 Amazon S3。
- 已包含 `repository-s3` 外掛程式。

如果來源使用自簽憑證，請規劃在工作流程組態中設定 `allowInsecure: true`。

### 目標叢集需求

您的 Amazon OpenSearch Service 3.5 網域必須符合下列所有需求：

- 已經存在。
- 可從同一個 VPC 存取，或可從該 VPC 路由連線。
- 您知道網域端點。
- 如果已啟用細微存取控制，Migration Assistant IAM 角色已對應具備足夠的權限。

### 基礎架構需求

需要下列基礎架構：

- 現有的 VPC ID。
- 位於不同可用區的至少兩個子網路。
- AWS CLI v2 與 `kubectl`，或 AWS CloudShell。
- 部署 EKS、AWS CloudFormation、IAM、S3 及 OpenSearch 資源的權限。

## 步驟 1：選擇遷移方式

在設定工作流程之前，請選擇下列其中一種遷移方式。

### 選項 A：計畫性停機

若採用計畫性停機遷移，請遵循下列步驟：

1. 暫停對 Elasticsearch 的寫入。
2. 建立快照。
3. 遷移中繼資料。
4. 回填文件。
5. 驗證目標。
6. 將用戶端指向 OpenSearch。

如果您不確定該選擇哪種方式，請使用計畫性停機，因為它涉及的元件較少且風險較低。
{: .note }

### 選項 B：零停機

若採用零停機遷移，請遵循下列步驟：

1. 啟動擷取。
2. 將用戶端路由至 capture proxy。
3. 建立快照。
4. 遷移中繼資料。
5. 回填文件。
6. 重播擷取的流量，直到目標追趕上為止。
7. 驗證目標。
8. 將用戶端切換至 OpenSearch。

如果您的應用程式依賴自動產生的文件 ID，請在選擇零停機方式之前徹底測試 Capture 與 Replay。自動產生的 ID 在重播期間不會保留。

## 步驟 2：準備來源叢集

準備來源叢集，包括安裝 `repository-s3` 外掛程式及註冊快照儲存庫。

### 安裝 repository-s3 外掛程式

Migration Assistant 使用快照進行回填，因此來源必須支援 S3 快照。有關 `repository-s3` 外掛程式的一般資訊，請參閱[快照與還原]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/snapshot-restore/#amazon-s3)。

驗證目前的外掛程式狀態：

```bash
curl -sk -u <SOURCE_USERNAME>:<SOURCE_PASSWORD> https://<SOURCE_ENDPOINT>:9200/_cat/plugins?v
```
{% include copy.html %}

如果缺少 `repository-s3`，且您的來源執行於 Kubernetes 中，常見的做法是使用 init container 進行安裝，使其在 pod 重新啟動後仍持續存在：

```bash
kubectl patch statefulset elasticsearch-master -n elasticsearch --type=strategic -p '{
  "spec": {
    "template": {
      "spec": {
        "initContainers": [
          {
            "name": "install-plugins",
            "image": "docker.elastic.co/elasticsearch/elasticsearch:6.8.22",
            "command": ["sh", "-c", "bin/elasticsearch-plugin install --batch repository-s3 && cp -r /usr/share/elasticsearch/plugins/* /plugins/"],
            "volumeMounts": [{"name": "plugins", "mountPath": "/plugins"}]
          }
        ],
        "containers": [
          {
            "name": "elasticsearch",
            "volumeMounts": [
              {"name": "plugins", "mountPath": "/usr/share/elasticsearch/plugins"}
            ]
          }
        ],
        "volumes": [
          {"name": "plugins", "emptyDir": {}}
        ]
      }
    }
  }
}'
```
{% include copy.html %}

然後等待部署完成：

```bash
kubectl rollout status statefulset/elasticsearch-master -n elasticsearch --timeout=300s
```
{% include copy.html %}

驗證外掛程式已載入：

```bash
curl -sk -u <SOURCE_USERNAME>:<SOURCE_PASSWORD> https://<SOURCE_ENDPOINT>:9200/_cat/plugins?v
```
{% include copy.html %}

### 授予來源叢集 S3 存取權限

來源叢集需要 AWS 憑證才能寫入快照。

對於 EKS 中的自我管理 Elasticsearch 叢集，請執行下列步驟來設定 S3 存取：

1. 將內嵌 S3 政策新增至 IAM 角色：

   ```bash
   aws iam put-role-policy \
     --role-name <ES_EKS_NODE_ROLE_NAME> \
     --policy-name es-snapshot-s3-access \
     --policy-document '{
       "Version": "2012-10-17",
       "Statement": [
         {
           "Effect": "Allow",
           "Action": ["s3:ListBucket", "s3:GetBucketLocation"],
           "Resource": "arn:aws:s3:::migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION>"
         },
         {
           "Effect": "Allow",
           "Action": ["s3:GetObject", "s3:PutObject", "s3:DeleteObject"],
           "Resource": "arn:aws:s3:::migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION>/*"
         }
       ]
     }'
   ```
   {% include copy.html %}

1. 建立暫時性輔助 pod：

   ```bash
   kubectl apply -f - <<'EOF'
   apiVersion: v1
   kind: Pod
   metadata:
     name: creds-helper
     namespace: elasticsearch
   spec:
     hostNetwork: true
     containers:
     - name: helper
       image: amazon/aws-cli:latest
       command: ["sh", "-c", "sleep 300"]
     restartPolicy: Never
   EOF

   kubectl wait --for=condition=ready pod/creds-helper -n elasticsearch --timeout=60s
   ```
   {% include copy.html %}

1. 擷取暫時性憑證：

   ```bash
   ACCESS_KEY=$(kubectl exec creds-helper -n elasticsearch -- \
     sh -c 'TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"); ROLE=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/); curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE" | python3 -c "import json,sys; print(json.load(sys.stdin)[\"AccessKeyId\"])"')

   SECRET_KEY=$(kubectl exec creds-helper -n elasticsearch -- \
     sh -c 'TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"); ROLE=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/); curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE" | python3 -c "import json,sys; print(json.load(sys.stdin)[\"SecretAccessKey\"])"')

   SESSION_TOKEN=$(kubectl exec creds-helper -n elasticsearch -- \
     sh -c 'TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"); ROLE=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/iam/security-credentials/); curl -s -H "X-aws-ec2-metadata-token: $TOKEN" "http://169.254.169.254/latest/meta-data/iam/security-credentials/$ROLE" | python3 -c "import json,sys; print(json.load(sys.stdin)[\"Token\"])"')
   ```
   {% include copy.html %}

1. 將憑證載入每個 pod 上的 Elasticsearch keystore：

   ```bash
   for pod in elasticsearch-master-0 elasticsearch-master-1 elasticsearch-master-2; do
     kubectl exec $pod -n elasticsearch -c elasticsearch -- \
       sh -c "echo '${ACCESS_KEY}' | bin/elasticsearch-keystore add -f s3.client.default.access_key"
     kubectl exec $pod -n elasticsearch -c elasticsearch -- \
       sh -c "echo '${SECRET_KEY}' | bin/elasticsearch-keystore add -f s3.client.default.secret_key"
     kubectl exec $pod -n elasticsearch -c elasticsearch -- \
       sh -c "echo '${SESSION_TOKEN}' | bin/elasticsearch-keystore add -f s3.client.default.session_token"
   done
   ```
   {% include copy.html %}

1. 重新載入安全設定：

   ```bash
   curl -sk -X POST -u <SOURCE_USERNAME>:<SOURCE_PASSWORD> \
     "https://<SOURCE_ENDPOINT>:9200/_nodes/reload_secure_settings"
   ```
   {% include copy.html %}

1. 移除輔助 pod：

   ```bash
   kubectl delete pod creds-helper -n elasticsearch --force
   ```
   {% include copy.html %}

對於正式環境的永久設定，建議為來源叢集採用持久性身分識別方式，而非暫時性憑證注入。
{: .note }

### 註冊快照儲存庫

在來源叢集上註冊一個儲存庫，並為此次遷移使用專用的 `base_path`：

```bash
curl -sk -X PUT -u <SOURCE_USERNAME>:<SOURCE_PASSWORD> \
  "https://<SOURCE_ENDPOINT>:9200/_snapshot/migration-repo" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "s3",
    "settings": {
      "bucket": "migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION>",
      "region": "<REGION>",
      "base_path": "es68-snapshots"
    }
  }'
```
{% include copy.html %}

驗證儲存庫：

```bash
curl -sk -X POST -u <SOURCE_USERNAME>:<SOURCE_PASSWORD> \
  "https://<SOURCE_ENDPOINT>:9200/_snapshot/migration-repo/_verify?pretty"
```
{% include copy.html %}

雖然此工作流程支援外部管理的快照，但對於正式環境遷移，建議的做法是讓 Migration Assistant 建立快照。這可確保快照建立、中繼資料遷移與回填保持在單一可重複的工作流程中，並具有一致的核准、驗證與復原步驟。外部管理的快照適合用於測試遷移、疑難排解或復原情境。
{: .note }

## 步驟 3：蒐集您的 VPC 資訊

尋找您的 VPC：

```bash
aws ec2 describe-vpcs \
  --region <REGION> \
  --query "Vpcs[*].{VpcId:VpcId,Name:Tags[?Key=='Name']|[0].Value,CidrBlock:CidrBlock}" \
  --output table
```
{% include copy.html %}

若要尋找 VPC 中的子網路，請執行以下命令：

```bash
aws ec2 describe-subnets \
  --region <REGION> \
  --filters "Name=vpc-id,Values=<YOUR_VPC_ID>" \
  --query "Subnets[*].{SubnetId:SubnetId,AZ:AvailabilityZone,CidrBlock:CidrBlock,Name:Tags[?Key=='Name']|[0].Value}" \
  --output table
```
{% include copy.html %}

請選擇位於不同可用區域中的至少兩個子網路。

## 步驟 4：在 EKS 上部署 Migration Assistant

下載 bootstrap 指令碼：

```bash
curl -sL -o aws-bootstrap.sh \
  "https://github.com/opensearch-project/opensearch-migrations/releases/latest/download/aws-bootstrap.sh" \
  && chmod +x aws-bootstrap.sh
```
{% include copy.html %}

將 Migration Assistant 部署到現有的 VPC：

```bash
./aws-bootstrap.sh \
  --deploy-import-vpc-cfn \
  --stack-name MA \
  --stage <STAGE> \
  --vpc-id <YOUR_VPC_ID> \
  --subnet-ids <SUBNET_1>,<SUBNET_2> \
  --region <REGION>
```
{% include copy.html %}

<details markdown="block">
<summary><strong>適用於隔離的子網路</strong></summary>

如果子網路沒有直接的網際網路對外連線，請新增 VPC 端點旗標：

```bash
./aws-bootstrap.sh \
  --deploy-import-vpc-cfn \
  --stack-name MA \
  --stage <STAGE> \
  --vpc-id <YOUR_VPC_ID> \
  --subnet-ids <SUBNET_1>,<SUBNET_2> \
  --create-vpc-endpoints \
  --region <REGION>
```
{% include copy.html %}

</details>

驗證部署：

```bash
aws eks update-kubeconfig --region <REGION> --name migration-eks-cluster-<STAGE>-<REGION>
kubectl get pods -n ma
```
{% include copy.html %}

所有核心 pod 都應處於執行中狀態。

## 步驟 5：確認輸出並對應目標存取權

讀取 CloudFormation 輸出：

```bash
aws cloudformation describe-stacks \
  --region <REGION> \
  --stack-name MA \
  --query "Stacks[0].Outputs[?contains(OutputKey,'MigrationsExportString')].OutputValue" \
  --output text
```
{% include copy.html %}

輸出包含以下值：

- EKS 叢集名稱
- 快照角色 ARN
- 遷移 IAM 角色資訊
- EKS 叢集安全群組

如果您的目標網域使用細微存取控制，請將 Migration Assistant IAM 角色對應到具有足夠權限的角色。其中一種做法是將其設定為 `MasterUserARN`：

```bash
aws opensearch update-domain-config \
  --region <REGION> \
  --domain-name <TARGET_DOMAIN_NAME> \
  --advanced-security-options '{
    "Enabled": true,
    "MasterUserOptions": {
      "MasterUserARN": "arn:aws:iam::<ACCOUNT_ID>:role/migration-eks-cluster-<STAGE>-<REGION>-migrations-role"
    }
  }'
```
{% include copy.html %}

請等待網域處理回傳 `false` 後再繼續。若要驗證狀態，請執行以下命令：

```bash
aws opensearch describe-domain \
  --region <REGION> \
  --domain-name <TARGET_DOMAIN_NAME> \
  --query "DomainStatus.Processing"
```
{% include copy.html %}

若要保留現有的 `MasterUserARN` 組態，請將該角色對應到適當的後端角色，而不是取代它。
{: .warning }

## 步驟 6：允許網路存取

尋找 EKS 叢集安全群組：

```bash
aws eks describe-cluster \
  --region <REGION> \
  --name migration-eks-cluster-<STAGE>-<REGION> \
  --query "cluster.resourcesVpcConfig.clusterSecurityGroupId" \
  --output text
```
{% include copy.html %}

然後新增輸入規則，讓 Migration Assistant 可以連線來源與目標叢集：

```bash
aws ec2 authorize-security-group-ingress \
  --region <REGION> \
  --group-id <SOURCE_CLUSTER_SG> \
  --protocol tcp \
  --port 9200 \
  --source-group <MA_EKS_CLUSTER_SG>

aws ec2 authorize-security-group-ingress \
  --region <REGION> \
  --group-id <TARGET_DOMAIN_SG> \
  --protocol tcp \
  --port 443 \
  --source-group <MA_EKS_CLUSTER_SG>
```
{% include copy.html %}

如果來源與目標叢集位於不同的 VPC 中，請確認路由與安全性政策允許跨 VPC 通訊。

## 步驟 7：連線至 Migration Console 並建立 Kubernetes Secret

開啟 Migration Console：

```bash
kubectl exec -it migration-console-0 -n ma -- /bin/bash
```
{% include copy.html %}

驗證已安裝的版本：

```bash
console --version
```
{% include copy.html %}

如果來源使用基本驗證，請建立 Kubernetes Secret：

```bash
kubectl create secret generic source-credentials \
  --from-literal=username=<SOURCE_USERNAME> \
  --from-literal=password='<SOURCE_PASSWORD>' \
  -n ma
```
{% include copy.html %}

對於使用 AWS Signature Version 4 的 OpenSearch Service 目標，您不需要目標憑證的 Secret。Migration Assistant 的 pod 會使用 AWS 身分。

## 步驟 8：建置試驗工作流程組態

從目前的 schema 範例開始：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

如需所有可用欄位、其類型、預設值與描述的互動式參考，請參閱 [Migration Assistant Schema Viewer](https://opensearch-project.github.io/opensearch-migrations/)。

使用類似以下的試驗組態：

```json
{
  "sourceClusters": {
    "source": {
      "endpoint": "https://<SOURCE_ENDPOINT>:9200",
      "allowInsecure": true,
      "version": "ES 6.8",
      "authConfig": {
        "basic": {
          "secretName": "source-credentials"
        }
      },
      "snapshotInfo": {
        "repos": {
          "migration-repo": {
            "awsRegion": "<REGION>",
            "s3RepoPathUri": "s3://migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION>/es68-snapshots"
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
      "endpoint": "https://<TARGET_DOMAIN_ENDPOINT>",
      "authConfig": {
        "sigv4": {
          "region": "<REGION>",
          "service": "es"
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
              "indexAllowlist": ["<PILOT_INDEX_NAME>"],
              "multiTypeBehavior": "UNION"
            },
            "documentBackfillConfig": {
              "indexAllowlist": ["<PILOT_INDEX_NAME>"],
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

此範例中值得注意的組態細節如下：

- 來源使用 HTTPS 與 `allowInsecure: true`，因為 EKS 上的自我管理 Elasticsearch 通常使用自簽憑證。
- 來源版本為 `ES 6.8`。
- 目標使用 AWS Signature Version 4，服務為 `es`。
- 將 `multiTypeBehavior` 設定為 `UNION` 是 Elasticsearch 6.8 來源的實用起點。
- 試驗會將快照建立、中繼資料遷移與回填限制在一個小型索引。

## 步驟 9：測試連線

執行內建的連線測試：

```bash
console clusters connection-check
console clusters curl source /
console clusters curl target /
```
{% include copy.html %}

來源與目標叢集都應成功連線。如果目標叢集回傳 `403`，表示目標 IAM 對應尚未完成。

## 步驟 10：執行試驗遷移

提交工作流程：

```bash
workflow submit
workflow manage
```
{% include copy.html %}

使用 `workflow manage` 作為主要介面。如果出現核准項目，請驗證並核准輸出，或直接使用 CLI：

```bash
workflow approve step "*.evaluateMetadata"
workflow approve step "*.migrateMetadata"
```
{% include copy.html %}

試驗完成後，請驗證目標叢集：

```bash
console clusters curl target /_cat/indices?v
console clusters curl target /<PILOT_INDEX_NAME>/_mapping
console clusters curl target /<PILOT_INDEX_NAME>/_count
console clusters curl target /<PILOT_INDEX_NAME>/_search?size=5&pretty
```
{% include copy.html %}

在試驗結果看起來沒有問題之前，請勿開始完整遷移。
{: .note }

## 步驟 11：執行完整遷移

若要將遷移擴展到所有索引，請編輯工作流程組態：

```bash
workflow configure edit
```
{% include copy.html %}

若要進行僅回填的整叢集遷移，請依照下列方式更新組態：

```json
"config": {
  "createSnapshotConfig": {
    "indexAllowlist": [],
    "includeGlobalState": true
  }
}
```
{% include copy.html %}

```json
"metadataMigrationConfig": {
  "indexAllowlist": [],
  "multiTypeBehavior": "UNION"
}
```
{% include copy.html %}

```json
"documentBackfillConfig": {
  "indexAllowlist": [],
  "podReplicas": 4
}
```
{% include copy.html %}

中繼資料或 RFS 的 `indexAllowlist` 為空時，表示選取快照中所有符合條件的索引。

下列章節說明各種遷移方式的步驟。請依照您在步驟 1 中選擇的方式，閱讀對應的章節。

### 計劃性停機路徑

若採用計劃性停機遷移，請依照下列步驟：

1. 停止寫入 Elasticsearch。
2. 提交工作流程。
3. 視需要監視並核准關卡。
4. 驗證目標。
5. 重建 Migration Assistant 未自動搬移的項目，例如安全性組態、ISM 或 ILM、儀表板、管線，以及叢集調校。
6. 將用戶端指向目標。
7. 恢復寫入。

### 零停機路徑

若採用零停機遷移，請在工作流程組態中加入流量區段。此區段會設定 capture proxy 與 Replayer：

```json
"traffic": {
  "proxies": {
    "capture": {
      "source": "source",
      "proxyConfig": {
        "listenPort": 9200,
        "podReplicas": 2,
        "internetFacing": false
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

若要在 VPC 外公開 proxy，請在提交前於工作流程組態中將 `internetFacing` 設為 `true`。提交後請勿修改 Kubernetes Service 資源。

然後依照下列步驟：

1. 提交工作流程。
2. 等待 capture proxy Kubernetes Service 變為可用。
3. 在快照與回填時段開始前，將用戶端路由至 proxy。
4. 等待快照、中繼資料遷移與回填完成。
5. 等待重播追上最新流量。
6. 驗證目標。
7. 將用戶端從 proxy 切換到目標端點。

尋找 proxy 端點：

```bash
kubectl get svc -n ma
```
{% include copy.html %}

重播所需時間取決於回填期間累積的流量，以及設定的 `speedupFactor`。

## 步驟 12：驗證並切換流量

切換流量之前，請驗證下列項目：

- 目標叢集健康狀態。
- 目標索引清單。
- 文件數量。
- 具代表性的搜尋結果。
- 已遷移多類型資料的對應行為。

若要驗證，請執行下列命令：

```bash
console clusters curl source /_cat/indices?v
console clusters curl target /_cat/indices?v
console clusters curl target /_cat/aliases?v
console clusters curl target /_cluster/health
```
{% include copy.html %}

<details markdown="block">
<summary><strong>選用：EKS 上的進階驗證</strong></summary>

在 EKS 上，您可以在 Amazon CloudWatch 中檢視額外的重播與比較遙測資料。請檢查下列項目：

- 重播心跳記錄檔，以確認重播持續進行。
- `tupleComparison` 指標，用於比較來源與目標的回應行為。
- 目標端的錯誤，以找出寫入不一致的情況。

此驗證對零停機遷移尤其重要，因為這類遷移需要比僅比較文件數量更徹底的驗證。

</details>

驗證確認目標正確後，請將用戶端重新導向至 OpenSearch Service 網域端點。

## 步驟 13：保留來源作為備援

切換流量後請勿立即移除來源叢集。在確認下列事項之前，請保留來源可用：

- 生產流量在目標上運作穩定。
- 應用程式錯誤率在預期範圍內。
- 儀表板與維運工具正常運作。
- 所有用戶端都已重新導向，不再使用 capture proxy。

建議保留 24 至 72 小時的回復時限。

## 步驟 14：移除遷移基礎架構

只有在回復時限過後才能移除基礎架構。

移除 Helm release 與命名空間：

```bash
helm uninstall -n ma ma
kubectl -n ma delete pvc --all
kubectl delete namespace ma --timeout=120s
```
{% include copy.html %}

刪除 CloudFormation 堆疊：

```bash
aws cloudformation delete-stack --region <REGION> --stack-name MA
aws cloudformation wait stack-delete-complete --region <REGION> --stack-name MA
```
{% include copy.html %}

這會移除 Migration Assistant 的 EKS 環境。它不會自動移除您的來源叢集、目標網域或快照資料。

如果不再需要快照儲存桶，請執行下列命令將其刪除：

```bash
aws s3 rb s3://migrations-default-<ACCOUNT_ID>-<STAGE>-<REGION> --force
```
{% include copy.html %}

## 疑難排解

以下是常見問題及其解決方法。

### CloudFormation 期間啟動程序失敗

若要確認 CloudFormation 堆疊狀態，請執行下列命令：

```bash
aws cloudformation describe-stacks --region <REGION> --stack-name MA --query "Stacks[0].StackStatus"
```
{% include copy.html %}

如果堆疊狀態為 `ROLLBACK_COMPLETE` 或 `CREATE_FAILED`，請刪除堆疊並重新執行啟動程序指令碼。

### CloudFormation 之後、Helm 部署之前啟動程序失敗

重新執行啟動程序指令碼：

```bash
./aws-bootstrap.sh --skip-cfn-deploy --stage <STAGE> --region <REGION>
```
{% include copy.html %}

### 目標回傳 403

Migration Assistant 的 IAM 角色在目標網域上沒有足夠的權限。請在目標叢集的安全性組態中，將該角色對應至適當的後端角色。

### 快照建立失敗，出現 ExpiredToken

來源叢集上的暫時 S3 憑證已過期。更新憑證並重新載入安全設定：

```bash
curl -sk -X POST -u <SOURCE_USERNAME>:<SOURCE_PASSWORD> \
  "https://<SOURCE_ENDPOINT>:9200/_nodes/reload_secure_settings"
```
{% include copy.html %}

### 從主控台執行試行作業成功，但工作流程失敗

此問題表示主控台 Pod 與工作流程執行器 Pod 的存取權限有所差異。在 EKS 上，請確認工作流程執行器的服務帳戶具備必要的 AWS 身分與網路存取權限。

## 相關文件

如需詳細資訊，請參閱下列資源：

- [選擇您的部署方式]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/)
- [使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/getting-started/)
- [疑難排解]({{site.url}}{{site.baseurl}}/migration-assistant/troubleshooting/)
- [遷移中繼資料]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/migrate-metadata/)
- [Migration Assistant 結構描述檢視器](https://opensearch-project.github.io/opensearch-migrations/)
