---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "擴充功能"
nav_order: 10
---

# OpenSearch 擴充功能

擴充功能是一項實驗性功能。因此，我們不建議在正式環境中使用擴充功能。如需擴充功能進度的最新消息，或想提供有助於改善此功能的意見回饋，請參閱 [GitHub 上的 issue](https://github.com/opensearch-project/OpenSearch/issues/2447)。
{: .warning}

在擴充功能推出之前，外掛程式是擴充 OpenSearch 功能的唯一方式。然而，外掛程式有明顯的缺點：它們需要經常更新，才能與 OpenSearch 核心保持同步；由於它們與 OpenSearch 在同一個處理程序中執行，因此會帶來安全性風險；而且更新或安裝外掛程式需要將整個叢集重新啟動。此外，外掛程式一旦發生故障，可能會對叢集造成致命影響。

擴充功能提供更簡單、更安全的方式來自訂 OpenSearch。擴充功能支援所有外掛程式功能，並可讓您為 OpenSearch 建置更多模組化功能。[OpenSearch SDK for Java](https://github.com/opensearch-project/opensearch-sdk-java/) 提供可用於開發擴充功能的類別與介面程式庫。擴充功能與 OpenSearch 核心分離，不需要經常更新。此外，擴充功能可以在獨立的處理程序中或另一個節點上執行，並可在叢集執行期間安裝。

## 入門

請使用下列文件開始使用擴充功能：

### 步驟 1：了解基本概念

閱讀[設計文件](https://opensearch-project.github.io/opensearch-sdk-java/DESIGN.html)，了解擴充功能的架構及其運作方式。

### 步驟 2：實際試用

依照[開發人員指南的入門章節](https://opensearch-project.github.io/opensearch-sdk-java/DEVELOPER_GUIDE.html#getting-started)中的詳細步驟，嘗試執行 Hello World 範例擴充功能。

### 步驟 3：建立您自己的擴充功能

依照[此教學](https://opensearch-project.github.io/opensearch-sdk-java/CREATE_YOUR_FIRST_EXTENSION.html)中的說明，開發自訂的建立、讀取、更新、刪除 (CRUD) 擴充功能。

### 步驟 4：了解如何部署您的擴充功能

如需建置、測試及執行擴充功能的說明，請參閱[開發人員指南的「開發您自己的擴充功能」章節](https://opensearch-project.github.io/opensearch-sdk-java/DEVELOPER_GUIDE.html#developing-your-own-extension)。

<!-- TODO: add the link after the release
## Extensions Javadoc

For a complete extensions class hierarchy, see the [Javadoc](Link TBD).
-->

## 外掛程式遷移

[Anomaly Detection 外掛程式](https://github.com/opensearch-project/anomaly-detection)現已[以擴充功能的形式實作](https://github.com/opensearch-project/anomaly-detection/tree/feature/extensions)。如需詳細資訊，請參閱[此 GitHub issue](https://github.com/opensearch-project/OpenSearch/issues/3635)。

如需將現有外掛程式遷移為擴充功能的提示，請參閱[外掛程式遷移文件](https://opensearch-project.github.io/opensearch-sdk-java/PLUGIN_MIGRATION.html)。