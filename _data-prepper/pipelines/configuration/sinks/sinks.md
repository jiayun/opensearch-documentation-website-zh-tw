---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "接收器"
parent: Pipelines
has_children: true
nav_order: 25
---

# Data Prepper 接收器

`sink` 是一種輸出元件，用來指定 OpenSearch Data Prepper 管線將事件發佈至的目的地。接收器目的地可以是 OpenSearch、Amazon Simple Storage Service (Amazon S3) 等服務，甚至是另一個 Data Prepper 管線，藉此串接多個管線。接收器元件具有下列可設定的選項，您可以用來自訂目的地類型。

## 設定選項

下表說明您可以用來設定 `sinks` 接收器的選項。

選項 | 必要 | 類型        | 說明
:--- | :--- |:------------| :---
`routes` | 否 | 字串清單 | 接收器適用的路由清單。若未提供，接收器會接收所有事件。如需詳細資訊，請參閱[條件式路由]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/pipelines#conditional-routing)。
`tags_target_key` | 否 | 字串   | 指定時，會將事件標籤納入輸出中，並置於提供的索引鍵之下。
`include_keys` | 否 | 字串清單 | 指定時，只會將列出的索引鍵納入傳送至接收器的資料中。部分轉碼器和接收器可能不支援此欄位。 
`exclude_keys` | 否 | 字串清單 | 指定時，會從傳送至接收器的資料中排除列出的索引鍵。部分轉碼器和接收器可能不支援此欄位。


