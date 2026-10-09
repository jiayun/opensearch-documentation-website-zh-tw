---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 flattened 欄位轉換為 flat_object"
nav_order: 3
parent: Migrate metadata
grand_parent: Migration workflows
permalink: /migration-assistant/migration-phases/migrate-metadata/transform-flattened-flat-object/
---

# 將 flattened 欄位轉換為 flat_object

當來源包含 `flattened` 對應且目標支援 `flat_object` 時，Migration Assistant 會在中繼資料遷移期間自動將 Elasticsearch `flattened` 欄位轉換為 OpenSearch `flat_object` 欄位。如果目標不支援您需要的同等欄位行為，請改為規劃自訂轉換。

## 內建轉換行為

在中繼資料遷移期間，內建轉換會偵測 `flattened` 欄位定義並自動將其改寫為 `flat_object`。不需要手動組態。

## 識別 flattened 欄位

若要確認您的來源是否使用 `flattened` 欄位，請執行下列命令：

```bash
console clusters curl source /_mapping
```
{% include copy.html %}

如果回應包含 `"type":"flattened"`，則自動轉換會在中繼資料遷移期間套用。

## 遷移後驗證

在中繼資料階段之後，請確認目標對應是否正確：

```bash
console clusters curl target /your-index/_mapping
workflow show
```
{% include copy.html %}

另外也請對目標驗證下列項目：

- 具代表性的查詢
- 彙總
- 依賴該欄位的儀表板或視覺化。

## 自訂轉換器

在下列情況下，請使用自訂中繼資料轉換器：

- 目標版本不支援您需要的欄位行為。
- 您想要將 `flattened` 轉換為不同的目標類型。
- 您需要超出內建轉換範圍的額外屬性清理。
