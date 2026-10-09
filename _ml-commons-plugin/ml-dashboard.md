---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 OpenSearch Dashboards 中管理機器學習模型"
parent: Integrating ML models
nav_order: 120
redirect_from:
  - /ml-commons-plugin/ml-dashbaord/
---

# 在 OpenSearch Dashboards 中管理機器學習模型
**2.9 版新增**
{: .label .label-purple }

機器學習 (ML) 叢集的管理員可以使用 OpenSearch Dashboards 來管理並檢查叢集內執行中的 ML 模型狀態。這能協助 ML 開發人員佈建節點，以確保其模型有效率地執行。

您只能使用 API 來註冊及部署模型。如需更多資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-serving-framework/)。

## 在 OpenSearch Dashboards 中啟用機器學習

在 OpenSearch 2.6 中，機器學習功能預設為停用。若要啟用，您需要編輯 `opensearch_dashboards.yml` 中的組態，然後重新啟動叢集。

若要啟用此功能：

1. 在您的 OpenSearch 叢集中，前往 Dashboards 主目錄；例如在 Docker 中為 `/usr/share/opensearch-dashboards`。
2. 開啟 Dashboards 組態檔 `opensearch_dashboards.yml` 的本機副本。如果您沒有副本，可以從 GitHub 取得：[`opensearch_dashboards.yml`](https://github.com/opensearch-project/OpenSearch-Dashboards/blob/main/config/opensearch_dashboards.yml)。
3. 將設定 `ml_commons_dashboards.enabled:` 新增至 `opensearch_dashboards.yml`。然後將其設為 `ml_commons_dashboards.enabled: true` 並儲存組態檔。
4. 重新啟動 Dashboards 容器。
5. 啟動 OpenSearch Dashboards，驗證功能組態設定已正確建立及設定。Machine Learning 區段應會出現在 **OpenSearch plugins** 下方。

## 在 OpenSearch Dashboards 中存取機器學習功能

若要在 OpenSearch Dashboards 中存取機器學習功能，請選取 **OpenSearch plugins** > **Machine Learning**。

![OpenSearch Dashboards 中的 Machine Learning 區段]({{site.url}}{{site.baseurl}}/images/ml/ml-dashboard/ml-dashboard.png)

在 Machine Learning 區段中，您現在可以存取 **Deployed models** 儀表板。

## Deployed models 儀表板

Deployed models 儀表板讓管理員能夠檢查儲存在 OpenSearch 叢集中任何模型的狀態。

![Deployed models 檢視畫面。]({{site.url}}{{site.baseurl}}/images/ml/ml-dashboard/deployed-models.png)

儀表板包含下列有關模型的資訊：

- **Name**：上傳時所指定的模型名稱。
- **Status**：模型有回應的節點數量。
   - 當所有節點都有回應時，狀態為 **Green**。
   - 當部分節點有回應時，狀態為 **Yellow**。
   - 當所有節點都無回應時，狀態為 **Red**。
- **Model ID**：模型 ID。
- **Action**：您可以對模型執行的動作。

唯一可用的動作是 **View Status Details**，如下圖所示。

![您可以在動作選單中檢視狀態詳細資訊。]({{site.url}}{{site.baseurl}}/images/ml/ml-dashboard/view-status-details.png)

選取後，會出現 Status Details 面板。

面板內提供下列詳細資訊：

- **Model ID**
- **Model status by node**：模型有回應的節點數量。

節點清單可讓您檢視模型執行所在的每個節點，包括每個節點的 **Node ID** 與狀態，如下圖所示。當您想使用節點的 **Node ID** 來判斷節點為何無回應時，這項功能非常實用。

![執行模型的各節點狀態。]({{site.url}}{{site.baseurl}}/images/ml/ml-dashboard/model-node-details.png)

## 後續步驟

如需如何在 OpenSearch 中管理 ML 模型的更多資訊，請參閱[在 OpenSearch 中使用 ML 模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-serving-framework/)。
