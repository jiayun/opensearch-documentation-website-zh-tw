---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Migration Assistant 適合您嗎？"
nav_order: 10
permalink: /classic/migration-assistant/is-migration-assistant-right-for-you/
---

# Migration Assistant 適合您嗎
Migration Assistant 是否適合您，取決於您的升級路徑、基礎架構複雜度及營運目標。本頁將協助您評估 Migration Assistant 是否符合您的使用情境。

Migration Assistant 解決了傳統遷移方式的主要限制。舉例來說，如果您要跨越多個主要版本進行升級——例如從 Elasticsearch 6.8 升級至 OpenSearch 2.19——您可以使用 Migration Assistant 以單一步驟完成整個流程。其他方法（例如滾動升級或快照還原）則需要逐一升級每個主要版本，而且通常每個階段都必須重新編製索引。

Migration Assistant 也支援即時流量複寫，可實現零停機遷移。這使其非常適合將服務中斷降至最低至關重要的環境。

## 支援的遷移路徑

下列矩陣顯示哪些來源版本可以直接遷移至哪些 OpenSearch 目標版本：

<!-- Migration matrix rendering logic — excludes Solr (not supported in classic) -->
{% comment %}First, collect all unique target versions (excluding Solr sources){% endcomment %}
{% assign all_targets = "" | split: "" %}
{% for path in site.data.migration-assistant.valid_migrations.migration_paths %}
  {% unless path.source contains "Solr" %}
    {% for target in path.targets %}
      {% assign all_targets = all_targets | push: target %}
    {% endfor %}
  {% endunless %}
{% endfor %}
{% assign unique_targets = all_targets | uniq | sort %}

<table class="migration-matrix" style="border-collapse: collapse; border: 1px solid #ddd;">
  <thead>
    <tr>
      <th style="border: 1px solid #ddd; padding: 8px;">來源版本</th>
      {% for target in unique_targets %}
      <th style="border: 1px solid #ddd; padding: 8px;">{{ target }}</th>
      {% endfor %}
    </tr>
  </thead>
  <tbody>
    {% for path in site.data.migration-assistant.valid_migrations.migration_paths %}
    {% unless path.source contains "Solr" %}
    <tr>
      <th style="border: 1px solid #ddd; padding: 8px;">{{ path.source }}</th>
      {% for target_version in unique_targets %}
      <td style="border: 1px solid #ddd; padding: 8px; text-align: center;">
        {% if path.targets contains target_version %}✓{% endif %}
      </td>
      {% endfor %}
    </tr>
    {% endunless %}
    {% endfor %}
  </tbody>
</table>

## 支援的平台

**來源與目標平台**

- 自行管理（內部部署或由雲端供應商代管）
- Amazon OpenSearch Service（不支援 Amazon OpenSearch Serverless 集合）

**支援的 AWS 區域**

請參閱[支援的 AWS 區域](https://docs.aws.amazon.com/solutions/latest/migration-assistant-for-amazon-opensearch-service/plan-your-deployment.html#supported-aws-regions)以取得完整的支援區域清單。

## 支援的功能

在開始升級或遷移之前，請考量要納入的叢集功能。下表列出可使用 Migration Assistant 遷移的項目、目前是否支援，以及如何處理每個元件的建議。

| 功能 | 支援 | 建議   |
| :--- |:----------| :--- |
| **文件**  | 是       | 使用 RFS 遷移現有資料；使用 Capture and Replay 遷移即時流量。 |
| **索引設定**  | 是       | 使用 `Metadata-Migration-Tool` 遷移。 |
| **索引對應**  | 是       | 使用 `Metadata-Migration-Tool` 遷移。  |
| **索引範本**   | 是       | 使用 `Metadata-Migration-Tool` 遷移。 |
| **元件範本**  | 是       | 使用 `Metadata-Migration-Tool` 遷移。  |
| **別名**   | 是       | 使用 `Metadata-Migration-Tool` 遷移。  |
| **Index State Management (ISM) 原則**  | 否        | 使用 API 手動遷移。如需 ISM 支援的詳細資訊，請參閱 [issue #944](https://github.com/opensearch-project/opensearch-migrations/issues/944)。 |
| **Elasticsearch Kibana 儀表板** | 否        | 若要將儀表板視覺化從 Elasticsearch Kibana 遷移至 OpenSearch Dashboards，請從 Kibana 匯出 JSON 檔案，再匯入 OpenSearch Dashboards。針對具有 X-Pack 視覺化（例如 Canvas 和 Lens）的 Elasticsearch 7.10.2--7.17 版本，請使用 [`dashboardsSanitizer`](https://github.com/opensearch-project/opensearch-migrations/tree/main/dashboardsSanitizer) 工具預先處理匯出的 JSON 檔案再匯入，因為這些視覺化可能需要修改以確保與 OpenSearch 相容。|
| **安全性建構**   | 否        | 根據雲端供應商的建議設定角色與權限。例如，若使用 AWS，請使用 AWS Identity and Access Management (IAM) 以強化安全性管理。 |
| **外掛程式**  | 否        | 檢查外掛程式相容性：部分 Elasticsearch 外掛程式可能沒有直接對應的 OpenSearch 版本。 |

## 檢查清單

使用此檢查清單判斷 Migration Assistant 是否適合您的遷移：

- 您是否要以單一步驟跨越一個或多個主要版本進行遷移——例如從 Elasticsearch 5 遷移至 OpenSearch 3？
- 您是否正在升級，但希望能安全地回復，以降低資料遺失或服務中斷的風險？
- 您是否需要維持高服務可用性，並將停機時間降至最低或為零？
- 您是否需要在切換之前驗證新的 OpenSearch 叢集——並具備復原能力？
- 您是否在尋找可遷移索引設定及其他中繼資料的工具？
- 您是否需要重新設定目標叢集——例如變更分片策略並重新編製索引？
- 您是否要跨區域遷移、從內部部署遷移，或從其他雲端供應商遷移？
- 您是否需要高效能的回填解決方案，能夠可靠地重新編製索引文件——並支援暫停、繼續或檢查點復原？

如果您對上述大多數問題的回答都是「是」，那麼 Migration Assistant 很可能就是適合您遷移的解決方案。

## Migration Assistant 的假設與限制

使用 Migration Assistant 之前，請先檢閱下列假設與限制。

### 網路與環境

必須能夠連線至 AWS 服務並具備對外網際網路存取，才能建置及部署 Migration Assistant。需求會因您要部署至新的或現有的虛擬私有雲端 (VPC) 而有所不同。

#### 來源與目標連線能力

為符合連線能力需求，請確保下列事項：

- 您必須在下列項目之間建立連線：
  - 來源叢集及/或 Amazon Simple Storage Service (Amazon S3)（用於快照，可能只需要更新儲存貯體政策）與 Migration Assistant。
  - 目標叢集與 Migration Assistant。
- 如果來源或目標位於沒有網際網路存取的私有 VPC 中，請使用下列其中一種方式連線：
  - VPC 端點
  - VPC 對等互連
  - AWS Transit Gateway

#### 部署至新的 VPC

部署至新的 VPC 時，請考量下列事項：

- Migration Assistant 會佈建具有必要元件（例如 NAT 閘道、子網路）的新 VPC。
- 您必須建立從此 VPC 到來源與目標叢集的網路存取。

#### 部署至現有的 VPC

部署至現有的 VPC 時，請考量下列事項：

- 如果將 Migration Assistant 部署至現有的 VPC（例如與來源或目標相同的 VPC），您可能需要設定與目標 VPC 外部任何叢集的連線。
  - 例如，如果 Migration Assistant 部署至來源 VPC，您可能需要 VPC 端點或對等互連才能連線至目標。

- 確保 Migration Assistant 元件可以連線至所有必要的 AWS 服務。

  - 如果 VPC 使用具有 NAT 閘道的私有子網路或具有網際網路閘道的公有子網路來進行對外存取，則不需要 VPC 介面端點。


  - 如果使用沒有對外存取的隔離子網路，您必須設定 VPC 介面端點或路由至下列服務：

    - **Application Load Balancer**（僅限 Capture and Replay）– 用於在遷移期間選擇性地將用戶端流量從來源重新路由至目標。
    - **Amazon CloudWatch** – 發佈遷移指標。
    - **Amazon CloudWatch Logs** – 匯入 Amazon Elastic Container Service (Amazon ECS) 任務記錄檔。
    - **Amazon Elastic Compute Cloud (Amazon EC2)** – 用於啟動 Migration Assistant。使用 AWS CloudFormation 部署時，啟動 EC2 執行個體需要對外網際網路存取（使用 NAT 閘道或網際網路閘道）才能從 GitHub 下載最新版本。
    - **Amazon Elastic Block Store (Amazon EBS)** – 提供暫存磁碟儲存空間。
    - **Amazon Elastic Container Registry (Amazon ECR)** – 提取容器映像。
    - **Amazon ECS** – 協調容器工作負載。
    - **Amazon Elastic File System (Amazon EFS)** – 儲存持續性記錄檔。
    - **Amazon Managed Streaming for Apache Kafka (Amazon MSK)**（僅限 Capture and Replay）– 用作持久儲存空間，以擷取及重播即時 HTTP 流量。
    - **Amazon S3** – 儲存及擷取快照與成品。
    - **Elastic Load Balancing**（僅限 Capture and Replay）– 由 Migration Console 用來連線至 Application Load Balancer。
    - **AWS Secrets Manager** – 在來源或目標使用基本驗證時，安全地儲存認證。
    - **AWS Systems Manager Parameter Store** – 儲存組態參數。
    - **AWS Systems Manager Session Manager** – 啟用對 ECS 任務（例如 Migration Console）的安全殼層存取。
    - **AWS X-Ray** – 支援分散式追蹤。
    - **Amazon Virtual Private Cloud (Amazon VPC)** – 確保適當的路由、DNS 解析及端點組態。

### Reindex-from-Snapshot

若要使用 `Reindex-from-Snapshot` (RFS)，請確保下列事項：

- 所有要遷移的索引都必須啟用 `_source` 欄位。請參閱[來源]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/source/)。
- 來源叢集必須安裝 Amazon S3 外掛程式。
- 如果您選擇自備快照（亦即不是由 Migration Assistant 建立的快照），則建立快照時必須套用下列設定：
  - `include_global_state: true` – 確保包含全域叢集狀態。
  - `compress: false` – 停用中繼資料壓縮，這是與 RFS 相容所必需的。
- 預設支援最大 **80 GiB** 的分片。您可以設定更大的分片大小，**但 AWS GovCloud (US) 除外**，其上限為 80 GiB。
- 在 OpenSearch 2.9 及更新版本中，不支援使用 `zstd` 或 zstd_no_dict 編解碼器的索引快照。如果您需要使用 `Reindex-from-Snapshot` 遷移這些索引，您必須先在來源叢集上使用 `default` 或 `best_compression` 重新編製索引，然後再建立新的快照供 RFS 使用。

### Capture and Replay

Capture and Replay 有下列需求：

- 必須部署 Traffic Capture Proxy 以攔截用戶端流量。
- 即時擷取僅建議用於來源叢集傳入流量 **< 4 TB/天** 的工作負載。
- 自動產生的文件 ID 在重播期間**不會保留**。用戶端必須為 `index` 和 `update` 操作明確提供文件 ID。
- 從 Elasticsearch 1.x 或 Elasticsearch 2.x 遷移時，Migration Assistant 不保證透過即時流量 Capture and Replay 達成零停機遷移。
