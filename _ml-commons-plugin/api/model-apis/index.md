---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模型 API"
parent: ML APIs
has_children: true
nav_order: 10
has_toc: false
redirect_from:
  - /ml-commons-plugin/api/model-apis/
---

# Model APIs

OpenSearch 支援下列模型 API：

- [註冊模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/register-model/)
- [部署模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/deploy-model/)
- [取得模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/get-model/)
- [搜尋模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/search-model/)
- [更新模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/update-model/)
- [取消部署模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/undeploy-model/)
- [刪除模型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/delete-model/)

# Predict API

Predict API 會叫用機器學習 (ML) 模型。OpenSearch 支援下列 Predict API：

- [Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 
- [Predict Stream]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict-stream/) 
- [Batch Predict]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/batch-predict/)

# Train API

使用 Train API 以同步或非同步方式訓練機器學習演算法：

- [Train]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)

若要透過 API 訓練任務，需要三項輸入：

- 演算法名稱：必須是 [FunctionName](https://github.com/opensearch-project/ml-commons/blob/1.3/common/src/main/java/org/opensearch/ml/common/parameter/FunctionName.java)。這會決定機器學習模型執行哪種演算法。若要新增函式，請參閱 [How To Add a New Function](https://github.com/opensearch-project/ml-commons/blob/main/docs/how-to-add-new-function.md)。
- 模型超參數：調整這些參數以提升模型準確度。
- 輸入資料：用於訓練機器學習模型或套用至預測的資料。您可以透過兩種方式輸入資料：對您的索引進行查詢，或使用 data frame。

# 訓練與預測 API

訓練與預測 API 可讓您使用相同的資料集訓練及叫用模型：

- [訓練與預測]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train-and-predict/)

## 模型存取控制考量

對於已啟用模型存取控制的叢集，使用者可以依照下列指定的存取層級，對模型群組中的模型執行 API 操作：

- `public` 模型群組：任何使用者。
- `restricted` 模型群組：僅限模型擁有者，或與該模型群組共用至少一個後端角色的使用者。
- `private` 模型群組：僅限模型擁有者。 

對於已停用模型存取控制的叢集，任何使用者都可以對任何模型群組中的模型執行 API 操作。 

管理員使用者可以對任何模型群組中的模型執行 API 操作。 

如需更多資訊，請參閱[模型存取控制]({{site.url}}{{site.baseurl}}/ml-commons-plugin/model-access-control/)。
