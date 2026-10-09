---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "現有叢集的 IAM 與安全性群組"
nav_order: 2
grand_parent: Migration phases
parent: Deploy
permalink: /classic/migration-assistant/migration-phases/deploy/iam-and-security-groups-for-existing-clusters/
---

# 現有叢集的 IAM 與安全性群組

本頁說明搭配現有叢集使用遷移工具時的安全性情境，包括為確保彼此之間能正確通訊所需的任何組態變更。

## 匯入 Amazon OpenSearch Service

請對 Amazon OpenSearch Service 使用下列組態。

### OpenSearch Service

對於 OpenSearch 網域，通常需要兩項主要組態，以確保遷移解決方案能正常運作：

1. **安全性群組組態**

   該網域應具有安全性群組，允許適用的遷移服務（Traffic Replayer、Migration Console、`Reindex-from-Snapshot`）進行通訊。CDK 會自動建立 `osClusterAccessSG` 安全性群組，並將其套用至遷移服務。使用者接著應將此安全性群組新增至其現有網域，以允許存取。

2. **存取原則組態** 應為下列其中一項：
   - 允許所有存取的開放式存取原則。
   - 設定為允許至少適用遷移服務（Traffic Replayer、Migration Console、`Reindex-from-Snapshot`）的 AWS Identity and Access Management (IAM) 任務角色存取該網域。
  
### 受管服務角色對應（跨受管叢集遷移）

在兩個受管叢集之間遷移時，例如當兩個網域都是使用 Amazon OpenSearch Service 建立時，請為 Migration Assistant 元件提供足夠的權限，以修改來源叢集和目標叢集。

請使用下列步驟授予所需權限：

1. 在 AWS Management Console 中，瀏覽至 **CloudFormation** > **Stacks**。
2. 找到開頭為 `OSMigrations-<stage>-<region>` 的堆疊（於 CDK 部署期間建立）。
3. 前往 **Resources** 索引標籤，並找到下列 IAM 角色：

   ```bash
   arn:aws:iam::****:role/OSMigrations-<stage>-<region>-migration-console-task
   arn:aws:iam::****:role/OSMigrations-<stage>-<region>-reindex-from-snapshot-task
   arn:aws:iam::****:role/OSMigrations-<stage>-<region>-traffic-replayer-default-task
   ```
   
4. 在來源叢集和目標叢集中，使用下列步驟將使用者對應至每個 Amazon Resource Name (ARN)：
    A. 存取 OpenSearch Dashboards。如果您使用 Elasticsearch，請存取 Kibana。
    B. 瀏覽至 **Security -> Roles -> all_access**。
    C. 在「Mapped users」區段中，將每個 ARN 新增為後端角色。
    D. 儲存您的變更。