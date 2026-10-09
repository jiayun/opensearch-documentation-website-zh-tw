---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "常見問題"
nav_order: 1000
parent: Learning to Rank
grand_parent: Optimizing search quality
has_children: false
---

# 常見問題

為了充分發揮 Learning to Rank (LTR) 的效益，請參考這些實用的見解。

## 負分數

Lucene 不允許負的查詢分數。如果您的原始特徵包含負值，這可能會造成問題。為了解決這個問題，請在訓練模型 _之前_ 確認您的特徵為非負值。您可以建立將各數值減去最小值的正規化欄位，或將分數傳入會產生大於或等於 `0` 之值的函式，來達成此目的。

## 錯誤

如果您在使用此外掛程式時遇到錯誤，可以在 [`opensearch-learning-to-rank-base` 儲存庫](https://github.com/opensearch-project/opensearch-learning-to-rank-base/issues) 中開啟問題。專案團隊會定期調查並解決問題。如果您需要一般支援，該問題可能會被關閉，並將您導向相關的支援管道。

## 進一步協助

如果您需要進一步協助，請加入 [Relevance Slack Community](https://opensourceconnections.com/slack) 並參與 `#opensearch-learn-to-rank` 頻道，以獲得社群的指引與支援。
