---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "整合 ML 模型"
nav_order: 10
has_children: true
more_cards:
- heading: 開始使用 AI 搜尋
  description: 了解如何在 OpenSearch 中實作語意與混合搜尋
  link: /vector-search/tutorials/neural-search-tutorial/
local_model:
- heading: OpenSearch 提供的預先訓練模型
  link: /ml-commons-plugin/pretrained-models/
  description: 只需最少的設定，並可省去訓練自訂模型所需的時間與心力
- heading: 自訂模型
  link: /ml-commons-plugin/custom-local-models/
  description: 針對您的特定使用案例提供自訂功能
external_model:
- heading: 外部託管的模型
  link: /ml-commons-plugin/remote-models/
  description: 了解如何為託管於第三方平台的模型建立連接器
---

# 整合 ML 模型

OpenSearch 支援機器學習 (ML) 模型，您可以搭配 k-NN 搜尋使用這些模型來擷取語意相似的文件。此語意搜尋功能可改善您應用程式的搜尋相關性。

開始之前，您需要[設定]({{site.url}}{{site.baseurl}}/quickstart/)並[保護]({{site.url}}{{site.baseurl}}/security/index/)您的叢集。
{: .tip}

## 選擇模型

若要將 ML 模型整合至您的搜尋工作流程，請選擇下列其中一個選項。

### 本機模型

將模型上傳至 OpenSearch 叢集並在本機使用。此選項可讓您在 OpenSearch 叢集中提供模型，但可能需要大量的系統資源。

{% include cards.html cards=page.local_model %}

### 外部託管的模型

連線至託管於第三方平台的模型。這需要更多設定，但可讓您使用已託管於 OpenSearch 以外服務上的模型。
    
{% include cards.html cards=page.external_model %}    

在 OpenSearch 2.9 版及更新版本中，您可以在單一叢集內同時整合本機與外部模型。
{: .note}

## 教學

{% include cards.html cards=page.more_cards %}

## 使用模型

您可以使用下列其中一種方式來使用 ML 模型：

- [叫用模型進行推論](#invoking-a-model-for-inference)。
- [使用模型進行搜尋](#using-a-model-for-search)。

### 叫用模型進行推論

您可以呼叫 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 來叫用您的模型。例如，測試文字嵌入模型可讓您查看它們產生的向量嵌入。

透過 ML Commons 外掛程式[訓練]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train/)的模型支援以模型為基礎的演算法，例如 k-means。在您將模型訓練至符合您的精確度需求後，即可使用這類模型進行推論。或者，您可以使用 [Train and Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/train-and-predict/) 來測試您的模型，而不必評估模型的效能。

### 使用模型進行搜尋

OpenSearch 支援多種可與 ML 模型整合的搜尋方法。如需詳細資訊，請參閱 [AI 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/)。

## 停用模型

當您不想取消部署或刪除模型時，可以暫時停用模型。呼叫 [Update Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/update-model/) 並將 `is_enabled` 設定為 `false` 即可停用模型。當您停用模型時，該模型將無法用於 [Predict API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/train-predict/predict/) 請求。如果您停用已取消部署的模型，該模型在部署後仍會保持停用狀態。您需要啟用它才能用於推論。

## 限制推論呼叫的速率

為您的 ML 模型設定 Predict API 呼叫的速率限制，可讓您降低模型推論成本。您可以在下列層級設定 Predict API 呼叫次數的速率限制：

- **模型層級**：呼叫 Update Model API 並指定 `rate_limiter`，為模型的所有使用者設定速率限制。如需詳細資訊，請參閱 [Update Model API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/model-apis/update-model/)。
- **使用者層級**：建立控制器，為模型的特定一或多位使用者設定速率限制。模型可能由多位使用者共用；您可以設定控制器，為不同使用者設定不同的速率限制。如需詳細資訊，請參閱 [Create Controller API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/controller-apis/create-controller/)。

模型層級的速率限制適用於模型的所有使用者。如果您同時指定模型層級速率限制與使用者層級速率限制，整體速率限制會設為兩者中較嚴格者。例如，如果模型層級限制為每分鐘 2 個請求，而使用者層級限制為每分鐘 4 個請求，則整體限制將設為每分鐘 2 個請求。

若要設定速率限制，您必須提供兩項輸入：請求數上限與時間範圍。OpenSearch 會使用這些輸入，將速率限制計算為請求數上限除以時間範圍。例如，如果您將限制設為每分鐘 4 個請求，則速率限制為 `4 requests / 1 minute`，即 `1 request / 0.25 minutes`，或 `1 request / 15 seconds`。OpenSearch 會依先到先服務的順序處理預測請求，並將這些請求限制為每 15 秒 1 個請求。假設有兩位使用者 Alice 與 Bob 針對同一個速率限制為每 15 秒 1 個請求的模型呼叫 Predict API。如果 Alice 呼叫 Predict API，而 Bob 緊接著也呼叫 Predict API，OpenSearch 會處理 Alice 的預測請求並拒絕 Bob 的請求。一旦距離 Alice 的請求已過 15 秒，Bob 即可再次傳送請求，而此請求將會被處理。 