---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "支援的單位"
nav_order: 150
redirect_from:
  - /opensearch/units/
---

# 支援的單位

OpenSearch 在所有 REST 操作中支援下列單位。

## 時間單位

下表列出所有支援的時間單位。

單位 | 指定方式
:--- | :---
天 | `d`
小時 | `h`
分鐘 | `m`
秒 | `s`
毫秒 | `ms`
微秒 | `micros`
奈秒 | `nanos`

## 位元組大小單位

下表列出所有支援的位元組大小單位。單位不區分大小寫。位元組大小單位以 2 為基底，因此 `1kb` 等於 1,024 位元組，`1mb` 等於 1,048,576 位元組。

單位 | 指定方式
:--- | :---
位元組 | `b`
二進位千位元組 | `kb` 或 `k`
二進位百萬位元組 | `mb` 或 `m`
二進位十億位元組 | `gb` 或 `g`
二進位兆位元組 | `tb` 或 `t`
二進位千兆位元組 | `pb` 或 `p`

## 距離單位

下表列出所有支援的距離單位。

單位 | 指定方式
:--- | :---
英里 | `mi` 或 `miles`
碼 | `yd` 或 `yards`
英尺 | `ft` 或 `feet`
英吋 | `in` 或 `inch`
公里 | `km` 或 `kilometers`
公尺 | `m` 或 `meters`
公分 | `cm` 或 `centimeters`
公釐 | `mm` 或 `millimeters`
海浬 | `NM`、`nmi` 或 `nauticalmiles`

## 無單位的數量

對於沒有單位的大型數值，例如文件數量，請使用下列字尾。例如，`5k` 等於 5,000。

字尾 | 倍數
:--- | :---
`k` | 千（1,000）
`m` | 百萬（1,000,000）
`g` | 十億（1,000,000,000）
`t` | 兆（1,000,000,000,000）
`p` | 千兆（1,000,000,000,000,000）

## 相關文件

- [常用 REST 參數]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/)
