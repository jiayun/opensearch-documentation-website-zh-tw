---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 string 欄位轉換為 text/keyword"
nav_order: 4
parent: Migrate metadata
grand_parent: Migration workflows
permalink: /migration-assistant/migration-phases/migrate-metadata/transform-string-text-keyword/
---

# 將 string 欄位轉換為 text/keyword

較舊的 Elasticsearch 版本使用 `string` 作為主要的文字欄位類型。現代 Elasticsearch 與 OpenSearch 則改用 `text` 與 `keyword`。Migration Assistant 會在遷移中介資料時，自動將舊版的 `string` 欄位轉換為現代的 `text` 或 `keyword` 對應。

## 內建轉換行為

Migration Assistant 會依據原始 `string` 欄位的設定方式來選擇目標欄位類型：

- 經過分析的 string 行為會轉換為 `text`。
- 未經分析或完全相符的 string 行為會轉換為 `keyword`。

此轉換也會視需要移除或正規化不相容的舊版對應屬性。

## 辨識 string 欄位

若要確認您的來源是否使用 `string` 欄位，請執行下列命令：

```bash
console clusters curl source /_mapping
```
{% include copy.html %}

如果來源對應包含 `"type":"string"`，就可能適用此內建轉換。

## 遷移後驗證

遷移中介資料之後，請驗證目標對應：

```bash
console clusters curl target /your-index/_mapping
workflow show
```
{% include copy.html %}

接著驗證相依於這些欄位的應用程式行為，尤其是：

- 詞彙查詢
- 彙總
- 排序
- 區分大小寫的完全相符邏輯

## 自訂轉換器

如果內建的 `string` 轉換不足以滿足您應用程式的語意，例如在下列情況，請使用自訂欄位類型轉換器：

- 您需要自訂的多欄位行為。
- 您想要同時重新命名欄位。
- 您需要特別清理欄位屬性。

