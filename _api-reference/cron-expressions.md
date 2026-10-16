---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Cron 運算式"
nav_order: 165
redirect_from:
  - /monitoring-plugins/alerting/cron/
  - /observing-your-data/alerting/cron/
---

# Cron 運算式

多項 OpenSearch 功能接受以 cron 運算式進行排程，包括 [Index State Management]({{site.url}}{{site.baseurl}}/im-plugin/ism/policies/)、[警示]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/monitors/) 和 [異常偵測]({{site.url}}{{site.baseurl}}/observing-your-data/ad/index/)。OpenSearch 使用標準 UNIX cron 語法。所有排程時間均為 UTC。

cron 運算式的格式如下：

```
<minutes> <hours> <day_of_month> <month> <day_of_week>
```

下表說明各個欄位。

| 欄位 | 值 | 特殊字元 |
| :--- | :--- | :--- |
| 分鐘 | 0--59 | `, - * /` |
| 小時 | 0--23 | `, - * /` |
| 每月第幾天 | 1--31 | `, - * /` |
| 月份 | 1--12 或 JAN--DEC（不分大小寫） | `, - * /` |
| 每週第幾天 | 0--7（0 和 7 都代表星期日）或 SUN--SAT（不分大小寫） | `, - * /` |

下表說明特殊字元。

| 字元 | 說明 |
| :--- | :--- |
| `*` | 符合所有值。例如，月份欄位中的 `*` 會符合每個月。 |
| `-` | 範圍。例如，`day_of_week` 中的 `1-5` 會符合週一到週五。 |
| `,` | 多個值。例如，`day_of_week` 中的 `1,3,5` 代表週一、週三和週五。 |
| `/` | 增量。例如，分鐘欄位中的 `0/15` 代表從第 0 分鐘開始每 15 分鐘一次。 |

有兩個欄位可指定日期：`day_of_month` 和 `day_of_week`。如果您在兩個欄位中都使用非萬用字元的值，則只要其中任一欄位符合時間，排程就會執行。例如，`15 2 1,15 * 1` 會在每月第一天、每月第 15 天以及每週一的 UTC 上午 2:15 執行。若要排定單一天，請設定其中一個欄位，並將另一個欄位保留為 `*`。

## 範例

| 運算式 | 說明 |
| :--- | :--- |
| `5 9 * * *` | 每天 UTC 上午 9:05 |
| `0/15 9 * * *` | UTC 上午 9:00 到 9:45 之間每 15 分鐘 |
| `5 9 * * 1-5` | UTC 上午 9:05，週一到週五 |
| `5 9 * * MON-FRI` | UTC 上午 9:05，週一到週五（使用具名星期） |
| `45 13 1-31/2 * *` | UTC 下午 1:45，每隔一天 |
| `0/10 * * * 6-7` | 週六和週日每 10 分鐘 |
| `0 0-23/3 1 1-12/2 *` | 每隔一個月的第一天每 3 小時 |

## 相關文件

- [常見 REST 參數]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/)
- [索引名稱語法]({{site.url}}{{site.baseurl}}/api-reference/index-name-syntax/)
- [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)
