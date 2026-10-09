---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取樣"
parent: Common use cases
nav_order: 45
---

# 取樣

OpenSearch Data Prepper 提供下列取樣功能：

- 時間取樣
- 百分比取樣
- 尾端取樣

## 時間取樣

您可以在 [`aggregate` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/aggregate/) 中使用 `rate_limiter` 動作，以限制每秒可處理的事件數量。您可以選擇捨棄超出的事件，或將其保留至下一個時間週期。

在下列範例中，來自特定 IP 位址且狀態碼為 `200` 的事件，每秒只有 100 個會傳送至接收端。`when_exceeds` 選項設為 `drop`，表示所設定時間範圍內所有超出的事件都會被捨棄。

```json
...
  processor:
   - aggregate:                                                                                                                                          
        identification_keys: ["clientip"]                                                                                                      
        action:                                                                                                                                           
          rate_limiter:                                                                                                                                   
            events_per_second: 100                                                                                                                        
            when_exceeds: drop
        when: "/status == 200"  
...
```

如果您改將 `when_exceeds` 選項設為 `block`，處理器會封鎖管線，直到時間範圍結束。接著它會處理被封鎖的事件。

## 百分比取樣

在 `aggregate` 處理器中使用 `percent_sampler` 動作，以限制傳送至接收端的事件數量。所有超出的事件都會被捨棄。

在下列範例中，來自特定 IP 位址且狀態碼為 `200` 的事件，只有 20% 會傳送至接收端：

```json
...
  processor:
  - aggregate:                                                                                                                                          
        identification_keys: ["clientip"]  
        duration :                                                                                                    
        action:                                                                                                                                           
          percent_sampler:                                                                                                                                   
            percent: 20                                                                                                                        
        when: "/status == 200" 
...
```

## 尾端取樣

在 `aggregate` 處理器中使用 `tail_sampler` 動作，以依據一組已定義的原則取樣事件。此動作會根據所設定的等待期間，等待不同彙總期間的彙總完成。當彙總完成且符合特定錯誤條件時，便會傳送至接收端。否則，只有所設定百分比的事件會傳送至接收端。

下列管線會將所有錯誤條件狀態為 `2` 的 OpenTelemetry 追蹤傳送至接收端。不符合此錯誤條件的追蹤則只有 20% 會傳送至接收端。

```json
...
  processor:
   - aggregate:                                                                                                                                          
        identification_keys: ["traceId"]                                                                                                                   
        action:                                                                                                                                           
          tail_sampler:                                                                                                                                   
            percent: 20                                                                                                                                   
            wait_period: "10s"                                                                                                                            
            condition: "/status == 2"                                                                                                              
          
...
```

如果您將錯誤條件設為 `false` 或未包含該條件，則只有所設定百分比的事件會依機率結果獲准通過。

由於可能難以確切判斷尾端取樣應於何時發生，您可以使用 `wait_period` 選項來測量自上次收到事件以來的閒置時間。
