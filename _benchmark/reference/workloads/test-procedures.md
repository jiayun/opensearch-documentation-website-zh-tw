---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: test_procedures
parent: Anatomy of a workload
nav_order: 50
---

<!-- vale off -->
# test_procedures 元素
<!-- vale on -->

測試程序是單一基準測試情境。每個測試程序都封裝一個 [`schedule`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/schedule/)，並新增名稱和說明等屬性。當工作負載定義多個情境時，請使用 `test_procedures` 元素。當工作負載僅定義一個情境時，請改在 `workload.json` 的最上層指定 `schedule`，並省略 `test_procedures`。

測試程序可以參照 [`operations`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/operations/) 元素中定義的所有操作。每個測試程序都支援下列參數。

參數 | 是否必要 | 資料類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 測試程序的名稱。為測試程序命名時，請勿使用空格；這可確保您能輕鬆在命令列輸入名稱。
`description` | 否 | 字串 |  以易於閱讀的格式描述測試程序。
`user-info` | 否 | 字串 | 在測試開始時輸出訊息，通知您與測試相關的重要資訊，例如棄用事項。
`default` | 否 | 布林值 | 設為 `true` 時，若您未在命令列指定測試程序，便會選取預設測試程序。如果工作負載僅定義一個測試程序，系統會自動將其選為預設值。否則，您必須僅在一個挑戰中定義 `"default": true`。
[`schedule`]({{site.url}}{{site.baseurl}}/benchmark/reference/workloads/schedule/) | 是 | 陣列 | 定義工作負載任務的執行順序。
