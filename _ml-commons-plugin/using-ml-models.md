---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "在 OpenSearch 中使用機器學習模型"
parent: Integrating ML models
has_children: true
has_toc: false
nav_order: 50
redirect_from:
   - /ml-commons-plugin/model-serving-framework/
   - /ml-commons-plugin/ml-framework/
models:
- heading: OpenSearch 提供的預先訓練模型
  link: /ml-commons-plugin/pretrained-models/
  description: 探索 OpenSearch 為 AI 應用程式即用而最佳化的機器學習模型系列
- heading: 自訂模型
  link: /ml-commons-plugin/custom-local-models/
  description: 了解如何在 OpenSearch 中上傳及提供您自己的機器學習模型，以滿足特殊使用情境
gpu:
- heading: GPU 加速
  link: /ml-commons-plugin/gpu-acceleration/
  description: 利用 ML 節點上的 GPU 加速來提升效能
---

# 在 OpenSearch 中使用機器學習模型
**於 2.9 版導入**
{: .label .label-purple }

若要將機器學習 (ML) 模型整合到您的 OpenSearch 叢集中，您可以在本機上傳及提供這些模型。請選擇下列其中一個選項。

{% include cards.html cards=page.models %}

在正式環境中，請在專用的 ML 節點上執行本機模型，而不是在資料節點上執行。如需詳細資訊，請參閱[節點選取設定]({{site.url}}{{site.baseurl}}/ml-commons-plugin/cluster-settings/#node-selection-settings)。
{: .important}

不支援在 CentOS 7 作業系統上執行本機模型。此外，並非所有本機模型都能在所有硬體與作業系統上執行。
{: .important}

{% include cards.html cards=page.gpu %}
