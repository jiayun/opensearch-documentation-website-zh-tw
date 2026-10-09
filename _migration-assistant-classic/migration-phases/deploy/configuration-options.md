---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "組態選項"
nav_order: 1
grand_parent: Migration phases
parent: Deploy
permalink: /classic/migration-assistant/migration-phases/deploy/configuration-options/
---

# 組態選項

本頁說明三種主要遷移情境的組態選項：

1. **中繼資料遷移**
2. **使用 `Reindex-from-Snapshot` (RFS) 的回填遷移**
3. **使用 Capture and Replay (C&R) 的即時擷取遷移**

這些遷移各自依賴快照或擷取代理程式。下列範例 `cdk.context.json` 組態由 AWS Cloud Development Kit (AWS CDK) 用來部署及設定 Migration Assistant for OpenSearch，並依各遷移類型分別顯示為獨立區塊。如果您執行的遷移適用於多個情境，可以合併這些選項。


如需完整的組態選項清單，請參閱 [`opensearch-migrations-options.md`](https://github.com/opensearch-project/opensearch-migrations/blob/main/deployment/cdk/opensearch-service-migration/options.md)。如果您需要的組態選項未出現在本頁，請在 [OpenSearch Migrations 儲存庫](https://github.com/opensearch-project/opensearch-migrations/issues) 中建立議題。
{: .tip }

您應設定來源叢集端點、目標叢集端點及現有虛擬私有雲端 (VPC) 的選項，遷移工具才能有效運作。

## 共用組態選項

每個遷移組態都共用下列選項。


| 名稱 | 範例  | 說明   |
| :--- | :--- | :--- |
| `sourceClusterEndpoint` | `"https://source-cluster.elb.us-east-1.endpoint.com"`  | 來源叢集的端點。  |
| `targetClusterEndpoint` | `"https://vpc-demo-opensearch-cluster-cv6hggdb66ybpk4kxssqt6zdhu.us-west-2.es.amazonaws.com:443"`   | 目標叢集的端點。如果使用現有目標叢集進行遷移，而非建立新的目標叢集，則為必要。 |
| `vpcId` | `"vpc-123456789abcdefgh"`  | 將儲存遷移資源的現有 VPC ID。該 VPC 必須至少有兩個私人子網路，且橫跨兩個可用區域。 |


## 使用 RFS 的回填遷移

下列 CDK 會使用 RFS 執行回填遷移：

```json
{
  "backfill-migration": {
    "stage": "dev",
    "vpcId": <VPC_ID>,
    "sourceCluster": {
        "endpoint": <SOURCE_CLUSTER_ENDPOINT>,
        "version": "ES 7.10",
        "auth": {"type": "none"}
    },
    "targetCluster": {
        "endpoint": <TARGET_CLUSTER_ENDPOINT>,
        "auth": {
            "type": "basic",
            "userSecretArn": <SECRET_WITH_USERNAME_AND_PASSWORD_KEYS>
        }
    },
    "reindexFromSnapshotServiceEnabled": true,
    "reindexFromSnapshotExtraArgs": "",
    "artifactBucketRemovalPolicy": "DESTROY"
  }
}
```
{% include copy.html %}

執行 RFS 回填遷移需要現有快照。 


RFS 組態使用下列選項。所有選項皆為選用。 

| 名稱  | 範例 | 說明 |
| :--- | :--- | :--- |
| `reindexFromSnapshotServiceEnabled` | `true` | 啟用 RFS ECS 服務的部署與組態。 |
| `reindexFromSnapshotExtraArgs` | `"--target-aws-region us-east-1 --target-aws-service-signing-name es"` | Document Migration 命令的額外引數，以空格分隔。如需詳細資訊，請參閱 [RFS 額外引數](https://github.com/opensearch-project/opensearch-migrations/blob/main/DocumentsFromSnapshotMigration/README.md#arguments)。您可以傳遞 `--no-insecure` 以移除 `--insecure` 旗標。 |

如要檢視 `reindexFromSnapshotExtraArgs` 的所有可用引數，請參閱 [快照遷移 `README`](https://github.com/opensearch-project/opensearch-migrations/blob/main/DocumentsFromSnapshotMigration/README.md#arguments)。在最基本的情況下，可能不需要任何額外引數。

## 使用 C&R 的即時擷取遷移 

下列範例 CDK 會使用 C&R 執行即時擷取遷移：

```json
{
  "live-capture-migration": {
    "stage": "dev",
    "vpcId": <VPC_ID>,
    "sourceCluster": {
        "endpoint": <SOURCE_CLUSTER_ENDPOINT>,
        "version": "ES 7.10",
        "auth": {"type": "none"}
    },
    "targetCluster": {
        "endpoint": <TARGET_CLUSTER_ENDPOINT>,
        "auth": {
            "type": "basic",
            "userSecretArn": <SECRET_WITH_USERNAME_AND_PASSWORD_KEYS>
        }
    },

    "// settingsForCaptureAndReplay": "Enable the following services for live traffic Capture and Replay:",
    "trafficReplayerServiceEnabled": true,

    "// help trafficReplayerExtraArgs": "Increase the speedup factor to replay requests at a faster rate in order to catch up.",
    "trafficReplayerExtraArgs": "--speedup-factor 1.5",

    "// help capture/target proxy pt. 1 of 2": "captureProxyService and targetClusterProxyService deployment will fail without network access to clusters.",
    "// help capture/target proxy pt. 2 of 2": "In most cases, keep the desired count setting at `0` until you verify connectivity in the Migration Console. After verifying connectivity, you can redeploy with a higher desired count.",
    "captureProxyServiceEnabled": true,
    "captureProxyDesiredCount": 3,
    "targetClusterProxyServiceEnabled": true,
    "targetClusterProxyDesiredCount": 3

  }
}
```
{% include copy.html %}

執行即時擷取遷移需要設定 Capture Proxy，以擷取傳入流量並使用 Traffic Replayer 服務將其傳送至目標叢集。如需 `captureProxyExtraArgs` 中可用的引數，請參閱[這裡](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficCaptureProxyServer/src/main/java/org/opensearch/migrations/trafficcapture/proxyserver/CaptureProxy.java)的 `@Parameter` 欄位。如需 `trafficReplayerExtraArgs`，請參閱[這裡](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficReplayer/src/main/java/org/opensearch/migrations/replay/TrafficReplayer.java)的 `@Parameter` 欄位。在最基本的情況下，可能不需要任何額外引數。


| 名稱  | 範例                                                                | 說明   |
| :--- |:-----------------------------------------------------------------------| :--- |
| `captureProxyServiceEnabled`    | `true`                                                                 | 使用 AWS CloudFormation 堆疊啟用 Capture Proxy 服務部署。  |
| `captureProxyExtraArgs`  | `"--suppressCaptureForHeaderMatch user-agent .*elastic-java/7.17.0.*"` | Capture Proxy 命令的額外引數，包括 [Capture Proxy](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficCaptureProxyServer/src/main/java/org/opensearch/migrations/trafficcapture/proxyserver/CaptureProxy.java) 指定的選項。  |
| `captureProxyDesiredCount`  | `0`                                                                    |  設定 Capture Proxy Amazon Elastic Container Service (Amazon ECS) 任務的數量。在大多數情況下，請將此設定保持為 `0`，直到您在 Migration Console 中驗證來源與目標叢集之間的連線為止。部署後，您可以修改網路設定，以允許從遷移安全性群組傳入現有叢集安全性群組。  |
| `trafficReplayerServiceEnabled` | `true`                                                                 | 使用 CloudFormation 堆疊啟用 Traffic Replayer 服務部署。  |
| `trafficReplayerExtraArgs`      | `"--sigv4-auth-header-service-region es,us-east-1 --speedup-factor 5"` | Traffic Replayer 命令的額外引數，包括驗證標頭選項及 [Traffic Replayer](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficReplayer/src/main/java/org/opensearch/migrations/replay/TrafficReplayer.java) 指定的其他參數。 |
| `targetClusterProxyServiceEnabled` | `true`                                                                 | 使用 CloudFormation 堆疊啟用目標叢集代理服務部署。 |
| `targetClusterProxyDesiredCount`  | `0`                                                                    | 設定目標叢集代理 Amazon ECS 任務的數量。在大多數情況下，請將此設定保持為 `0`，直到您在 Migration Console 中驗證來源與目標叢集之間的連線為止。部署後，您可以修改網路設定，以允許從遷移安全性群組傳入現有叢集安全性群組。  |

如需 `captureProxyExtraArgs` 中可用的引數，請參閱 [`CaptureProxy.java`](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficCaptureProxyServer/src/main/java/org/opensearch/migrations/trafficcapture/proxyserver/CaptureProxy.java) 中的 `@Parameter` 欄位。如需 `trafficReplayerExtraArgs`，請參閱 [`TrafficReplayer.java`](https://github.com/opensearch-project/opensearch-migrations/blob/main/TrafficCapture/trafficReplayer/src/main/java/org/opensearch/migrations/replay/TrafficReplayer.java) 中的 `@Parameter` 欄位。


## 叢集驗證選項

來源叢集與目標叢集皆可使用無驗證、僅限 VPC 的驗證、以使用者名稱與密碼進行的基本驗證，或限定於某個使用者或角色的 AWS Signature Version 4。

### 無驗證

```json
    "sourceCluster": {
        "endpoint": <SOURCE_CLUSTER_ENDPOINT>,
        "version": "ES 7.10",
        "auth": {"type": "none"}
    }
```
{% include copy.html %}

### 基本驗證

```json
    "sourceCluster": {
        "endpoint": <SOURCE_CLUSTER_ENDPOINT>,
        "version": "ES 7.10",
        "auth": {
            "type": "basic",
            "userSecretArn": <SECRET_WITH_USERNAME_AND_PASSWORD_KEYS>
        }
    }
```
{% include copy.html %}

### AWS Signature Version 4 驗證

```json
    "sourceCluster": {
        "endpoint": <SOURCE_CLUSTER_ENDPOINT>,
        "version": "ES 7.10",
        "auth": {
            "type": "sigv4",
            "region": "us-east-1",
            "serviceSigningName": "es"
        }
    }
```
{% include copy.html %}

`serviceSigningName` 可以是 `es`，適用於 Elasticsearch 或 OpenSearch 網域。

所有這些驗證選項皆同時適用於來源與目標叢集。

## 快照選項

下列組態選項可用於自訂從快照進行遷移的程序。

### 受管理服務來源的快照

如果您的來源叢集位於 Amazon OpenSearch Service 上，您需要設定額外的 AWS Identity and Access Management (IAM) 角色，並在建立快照的呼叫中傳遞該角色，如 [AWS 文件](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html) 所述。Migration Assistant 可以自動管理此程序。OpenSearch Service 快照僅與 AWS Signature Version 4 驗證相容。下列參數可確保建立並傳遞額外的 IAM 角色。

| 名稱  | 範例 | 說明 |
| :--- | :--- | :--- |
| `managedServiceSourceSnapshotEnabled` | `true` | 為 OpenSearch Service 來源叢集建立快照所需的必要角色與信任關係。此功能僅與 AWS Signature Version 4 驗證相容。|

### 自備快照

您可以使用現有的 Amazon Simple Storage Service (Amazon S3) 快照來執行[中繼資料]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/)與[回填]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/backfill/)遷移，而不使用 Migration Assistant 建立快照：

```json
    "snapshot": {
        "snapshotName": "my-snapshot-name",
        "snapshotRepoName": "my-snapshot-repo",
        "s3Uri": "s3://my-s3-bucket-name/my-bucket-path-to-snapshot-repo",
        "s3Region": "us-east-2"
    }
```
{% include copy.html %}

所提供快照組態中使用的叢集版本應與來源叢集版本一致。需要來源叢集版本，才能確保所提供的快照能被正確解析。如果監控與驗證不需要存取來源叢集，可以依照下列方式停用：
```json
    "sourceCluster": {
        "disabled": true,
        "version": "ES 7.10"
    }
```
{% include copy.html %}

預設情況下，Amazon S3 儲存貯體會自動允許同一 AWS 帳戶中的角色（具備適當的 `s3:*` 權限）存取 S3 儲存貯體，無論儲存貯體位於哪個 AWS 區域。如果外部 S3 儲存貯體與 Migration Assistant 部署位於同一個 AWS 帳戶中，則不需要額外的 IAM 組態即可存取該儲存貯體。

如果您在 Amazon S3 中使用自訂權限模型，任何存取控制清單 (ACL) 或自訂儲存貯體政策都應允許 RFS 與 Migration Console 的 Migration Assistant 任務角色從 S3 儲存貯體讀取資料。

如果 S3 儲存貯體與 Migration Assistant 部署位於不同的 AWS 帳戶中，您需要類似下列的自訂儲存貯體政策，以允許 Migration Assistant 存取：

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowExternalAccountReadAccessToBucket",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<ACCOUNT_ID>:root"
      },
      "Action": [
        "s3:GetObject",
        "s3:ListBucket",
        "s3:GetBucketLocation"
      ],
      "Resource": [
        "arn:aws:s3:::my-s3-bucket-name",
        "arn:aws:s3:::my-s3-bucket-name/*"
      ]
    }
  ]
}
```
{% include copy.html %}

## 網路組態

遷移工具預期來源叢集、目標叢集與遷移資源位於同一個 VPC 中。如果情況並非如此，可能需要在本文件之外手動設定網路。

{% include migration-phase-navigation.html %}
