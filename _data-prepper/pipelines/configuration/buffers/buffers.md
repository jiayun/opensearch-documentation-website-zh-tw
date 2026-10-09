---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "緩衝區"
parent: Pipelines
has_children: true
nav_order: 30
---

# Data Prepper 緩衝區

`buffer` 元件在 OpenSearch Data Prepper 管線中扮演 `source` 與 `sink` 元件之間的中介層。它做為事件的暫存空間，將 `source` 與下游的處理器和接收器解耦。緩衝區可以是記憶體內或磁碟式。

若未在管線組態中明確指定，Data Prepper 會使用預設的 `bounded_blocking` 緩衝區，這是一個以可儲存事件數量為上限的記憶體內佇列。當事件量和處理速率在可用記憶體限制內可控時，`bounded_blocking` 緩衝區是方便的選項。 


