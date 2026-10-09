---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: mvcombine
parent: Commands
grand_parent: PPL
nav_order: 30
---

<!-- vale off -->

# mvcombine 命令

<!-- vale on -->

`mvcombine` 命令會將除了指定目標欄位以外，所有欄位都相同的資料列分組，並將該目標欄位的值合併成多重值 (陣列) 欄位。

資料列會依管線中目前除了目標欄位以外的所有欄位進行分組。目標欄位缺少或為 `null` 的資料列，會從合併後的多重值輸出中排除。
{: .note}

## 語法

`mvcombine` 命令的語法如下：

```sql
mvcombine <field>
```

## 參數

`mvcombine` 命令支援下列參數。

| 參數 | 必要/選用 | 說明 |
| --- | --- | --- |
| `<field>` | 必要 | 值會合併成多重值欄位的欄位名稱。 |

<!-- vale off -->

## 範例 1：使用基本 mvcombine

<!-- vale on -->

下列查詢會將資料列收合成單一資料列，並將 `packets_str` 合併成多重值欄位：

```sql
source=mvcombine_data
| where ip='10.0.0.1' and bytes=100 and tags='t1'
| fields ip, bytes, tags, packets_str
| mvcombine packets_str
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| ip | bytes | tags | packets_str |
| --- | --- | --- | --- |
| 10.0.0.1 | 100 | t1 | [10,20,30] |

<!-- vale on -->

## 範例 2：合併多個群組

下列查詢會為每個群組索引鍵產生一個輸出資料列：

```sql
source=mvcombine_data
| where bytes=700 and tags='t7'
| fields ip, bytes, tags, packets_str
| sort ip, packets_str
| mvcombine packets_str
| sort ip
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| ip | bytes | tags | packets_str |
| --- | --- | --- | --- |
| 10.0.0.7 | 700 | t7 | [1,2] |
| 10.0.0.8 | 700 | t7 | [9] |

<!-- vale on -->

## 範例 3：部分資料列缺少目標欄位

缺少目標欄位的資料列不會對合併後的輸出貢獻值：

```sql
source=mvcombine_data
| where ip='10.0.0.3' and bytes=300 and tags='t3'
| fields ip, bytes, tags, packets_str
| mvcombine packets_str
```
{% include copy.html %}

查詢會傳回下列結果：

<!-- vale off -->

| ip | bytes | tags | packets_str |
| --- | --- | --- | --- |
| 10.0.0.3 | 300 | t3 | [5] |

<!-- vale on -->

## 範例 4：缺少欄位

下列查詢嘗試合併目前結構描述中不存在之欄位的值：

```sql
source=mvcombine_data
| mvcombine does_not_exist
```
{% include copy.html %}

查詢會傳回下列錯誤：

```text
{'reason': 'Invalid Query', 'details': 'Field [does_not_exist] not found.', 'type': 'IllegalArgumentException'}
```

## 相關命令

- [`nomv`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/nomv/) -- 將多重值欄位轉換成單一字串值
- [`mvexpand`]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/mvexpand/) -- 將多重值欄位展開成個別資料列
