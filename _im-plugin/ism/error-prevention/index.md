---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "ISM 錯誤預防"
parent: Index State Management
nav_order: 40
has_children: true
has_toc: false
redirect_from:
  - /im-plugin/ism/error-prevention/
---

# ISM 錯誤預防

錯誤預防會在執行索引狀態管理（ISM）動作之前驗證這些動作，以防止動作失敗。它也會在 [Index Explain API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/#explain-index) 的回應中輸出動作驗證結果的其他資訊。以下各節列出各動作的驗證規則與疑難排解方式。

---

#### 目錄
1. 目錄
{:toc}


---

## 輪替 

若索引符合下列任一條件，ISM 就不會對該索引執行 `rollover` 動作： 

- [索引不是寫入索引]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#the-index-is-not-the-write-index)。
- [索引沒有別名]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#the-index-does-not-have-an-alias)。
- [輪替政策未包含 rollover_alias 索引設定]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#the-rollover-policy-misses-rollover_alias-index-setting)。
- [輪替動作已遭略過]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#skipping-rollover-action-is-true)。
- [索引已使用別名成功輪替]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#this-index-has-already-been-rolled-over-successfully)。

## 刪除 

若索引符合下列任一條件，ISM 就不會對該索引執行 `delete` 動作： 

- 索引不存在。
- 索引名稱無效。
- 索引是資料串流的寫入索引。

## 強制合併

若索引的資料集過大且超過閾值，ISM 就不會對該索引執行 `force_merge` 動作。

## 副本數量

若索引符合下列任一條件，ISM 就不會對該索引執行 `replica_count` 動作： 

- 資料量超過閾值。
- 分片數量超過上限。

## 開啟

若索引符合下列任一條件，ISM 就不會對該索引執行 `open` 動作： 

- 索引遭到封鎖。
- 分片數量超過上限。

## 唯讀

若索引符合下列任一條件，ISM 就不會對該索引執行 `read_only` 動作： 

- 索引遭到封鎖。
- 資料量超過閾值。

## 讀寫 

若索引遭到封鎖，ISM 就不會對該索引執行 `read_write` 動作。


## 關閉

若索引符合下列任一條件，ISM 就不會對該索引執行 `close` 動作：

- 索引不存在。
- 索引名稱無效。

## 索引優先順序

若索引沒有 `read-only-allow-delete` 權限，ISM 就不會對該索引執行 `index_priority` 動作。

## 快照

若索引符合下列任一條件，ISM 就不會對該索引執行 `snapshot` 動作：

- 索引不存在。
- 索引名稱無效。

## 僅供搜尋

若索引符合下列任一條件，ISM 就不會對該索引執行 `search_only` 動作：

- 索引不存在。
- 叢集[未啟用遠端儲存]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#remote-store-is-not-enabled)。
- 索引[未啟用分段複寫]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#segment-replication-is-not-enabled)。
- 索引[未設定搜尋副本]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/resolutions/#no-search-replicas-configured)。

## 轉換 

若索引符合下列任一條件，ISM 就不會對該索引執行 `transition` 動作：

- 索引不存在。
- 索引名稱無效。