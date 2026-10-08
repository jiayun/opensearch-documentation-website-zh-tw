---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除索引範本"
parent: Index templates
grand_parent: Index APIs
nav_order: 20
---

# 刪除索引範本 API
**於 1.0 版導入**
{: .label .label-purple }

刪除索引範本 API 會刪除一或多個索引範本。

## 端點

```json
DELETE /_index_template/{template-name}
```

## 路徑參數

參數 | 類型 | 說明
:--- | :--- | :---
`template-name` | 字串 | 索引範本的名稱。您可以在一個請求中以逗號分隔多個範本名稱，一次刪除多個範本。當請求中使用多個範本名稱時，不支援萬用字元。

## 查詢參數

支援下列選用的查詢參數。

參數 | 類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | Time | 等待連線至叢集管理員節點的時間。預設為 `30s`。
`timeout` | Time | 此作業等待回應的時間。預設為 `30s`。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/index_template/delete`。
