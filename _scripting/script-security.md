---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼安全性"
nav_order: 50
---

# 指令碼安全性

指令碼是在 OpenSearch 程序內執行的程式碼，因此叢集的安全性取決於該程式碼的來源，以及它可呼叫的 Java 類別。OpenSearch 透過限制指令碼允許執行的動作，以及限制 OpenSearch 程序本身來保護指令碼功能。組態設定可進一步限制叢集接受的指令碼。

## 限制指令碼允許執行的動作

[Painless]({{site.url}}{{site.baseurl}}/scripting/painless/) 與 [Lucene 運算式語言]({{site.url}}{{site.baseurl}}/scripting/expressions/) 都在沙箱中執行：指令碼只能呼叫 OpenSearch 所提供允許清單中的類別與方法，而該允許清單排除了檔案存取、網路存取、執行緒建立、反射與系統時鐘。Java 代理程式會在 JVM 層級強制執行此允許清單。

允許清單以純文字形式提供於 `lang-painless` 模組中，因此您可以閱讀它來判斷特定類別或方法是否可呼叫。已安裝的外掛程式可以新增項目，這表示邊界取決於存在哪些外掛程式。關於檔案位置與內容，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。

允許清單可限制惡意指令碼造成的損害，但並不表示來自不受信任來源的指令碼就可以安全執行。請將它與下列章節所述的程序與組態限制搭配使用。
{: .warning}

## 限制 OpenSearch 程序

沙箱規範指令碼可以呼叫的內容。本節的兩項防護則規範 OpenSearch 程序本身可以執行的動作，使逃出沙箱的程式碼仍受到侷限。

### 以非特權使用者執行 OpenSearch

切勿以 `root` 使用者執行 OpenSearch。以 `root` 執行的程序若發生沙箱逃逸，會危害整台主機；而以專用服務帳戶執行的程序發生相同的逃逸時，僅侷限於該帳戶可讀寫的範圍。封裝的發行版本會為此建立 `opensearch` 使用者。如需更多資訊，請參閱 [安裝 OpenSearch]({{site.url}}{{site.baseurl}}/install-and-configure/install-opensearch/index/)。

OpenSearch 會自行強制執行此規則。以 `root` 啟動的節點會在啟動程序期間失敗並出現 `can not run opensearch as root`。沒有任何設定可以覆寫這項檢查。

### 在作業系統層級封鎖程序建立

在語言沙箱之下，OpenSearch 會借助作業系統來限制程序本身，使載入 JVM 的原生程式碼也無法啟動新的程式。機制因平台而異：

- 在 Linux 上，透過 `seccomp(2)`（較舊核心則透過 `prctl(2)`）安裝的篩選器會封鎖 `fork`、`vfork`、`execve` 與 `execveat` 系統呼叫。
- 在 macOS 上，`sandbox_init` 會套用 Seatbelt 設定檔 `(version 1) (allow default) (deny process-fork) (deny process-exec)`。
- 在 Windows 上，程序會加入 `ActiveProcessLimit` 為 1 的工作物件，因此無法建立子程序。

此防護由靜態設定 `bootstrap.system_call_filter` 控制，預設為 `true`。請保持啟用。

當設定已啟用但篩選器無法安裝時，OpenSearch 會回報 `system call filters failed to install; check the logs and fix your configuration or disable system call filters at your own risk`。該訊息是否會使節點停止，取決於節點的繫結方式：

- 僅繫結至回環位址，或設定了 `discovery.type: single-node` 的節點，會將該訊息記錄為警告並照常啟動。因此本機開發叢集會在缺少此防護層的情況下執行，且除了該記錄行之外沒有任何跡象。
- 繫結或發布至非回環位址的節點將無法啟動，因為繫結至可連線的位址會使這項檢查變成強制。

請勿將開發叢集成功啟動視為篩選器已安裝的證明。請在啟動記錄檔中搜尋前述訊息，其中會說明原因---例如核心建置時未包含 `CONFIG_SECCOMP_FILTER`---並在將相同組態套用至其他機器可連線的節點之前先修正問題。若要在任何節點上強制執行此檢查，請以 `-Dopensearch.enforce.bootstrap.checks=true` 啟動。
{: .note}

僅在篩選器無法安裝的平台上，才停用 `bootstrap.system_call_filter` 作為因應措施，並將該節點視為少了一層防護。
{: .warning}

## 限制叢集接受的指令碼

組態是您可控的防護。下列章節說明誰可以提交指令碼，以及叢集會執行哪些指令碼。

### 讓叢集遠離公開網路

請勿將 OpenSearch REST API 直接暴露給使用者或網際網路。任何能連線到 API 的用戶端都可以提交指令碼，因此暴露的叢集會讓每位訪客都能在您的搜尋程序內執行程式碼。請將您自己的應用程式置於使用者與 OpenSearch 之間，並由它根據已驗證的輸入建構請求。請勿轉發使用者提供的請求本文。

下列做法可降低您暴露於惡意指令碼的風險：

- 只將使用者輸入的查詢文字傳送至您的應用程式，並在伺服器端據此建構 OpenSearch 請求。
- 將指令碼儲存在叢集中並以識別碼參照，讓用戶端從已審核的指令碼集合中選擇，且只提供 `params`。如需更多資訊，請參閱 [使用儲存的指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/#working-with-stored-scripts)。
- 使用 `cluster:admin/script/put` 權限限制誰可以建立儲存的指令碼。如需更多資訊，請參閱 [權限]({{site.url}}{{site.baseurl}}/security/access-control/permissions/)。
- 驗證並限制您在 `params` 中傳遞的值，如同對待其他使用者輸入一樣。

下列做法會使叢集暴露於風險：

- 讓 REST API 可從網際網路或不受信任的網路連線。
- 接受來自用戶端的搜尋請求本文並原樣傳遞，讓用戶端能提供任意的內嵌指令碼。
- 將使用者輸入插入指令碼 `source` 字串中，這是指令碼注入：輸入會變成程式碼而非資料。

### 限制允許的指令碼類型

`script.allowed_types` 設定控制叢集是否接受內嵌指令碼、儲存的指令碼，或兩者皆可。可將其設為 `inline`、`stored` 或 `none`。

預設為空清單，表示允許兩種類型。若只接受儲存的指令碼，使每個使用中的指令碼都經過管理員審核並儲存，請在 `opensearch.yml` 中加入以下內容：

```yaml
script.allowed_types: stored
```
{% include copy.html %}

若要完全停用指令碼功能，請將值設為 `none`：

```yaml
script.allowed_types: none
```
{% include copy.html %}

### 限制允許的情境

`script.allowed_contexts` 設定控制叢集接受哪些指令碼情境。每個情境對應一項會執行指令碼的功能，例如 `score` 用於相關性評分、`update` 用於文件更新，以及 `ingest` 用於資料匯入管線處理器。

預設為空清單，表示允許所有情境。若只允許計算分數與排序值的指令碼，請在 `opensearch.yml` 中加入以下內容：

```yaml
script.allowed_contexts: score, number_sort, string_sort
```
{% include copy.html %}

設定此設定後，在任何其他情境中提交的指令碼---包括更新指令碼或資料匯入處理器指令碼---都會被拒絕。

`script.allowed_types` 與 `script.allowed_contexts` 都是靜態設定。請在每個節點的 `opensearch.yml` 中設定，並重新啟動節點。
{: .note}

## 驗證目前的限制

若要確認叢集目前接受的內容，請使用 [Get Script Languages API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-language/)：

```json
GET _script_language
```
{% include copy-curl.html %}

`types_allowed` 欄位會回報 `script.allowed_types` 的效果，並列出每種語言在套用 `script.allowed_contexts` 後可執行的情境：

<details open markdown="block">
<summary>
  回應
</summary>

```json
{
  "types_allowed": [
    "inline",
    "stored"
  ],
  "language_contexts": [
    {
      "language": "expression",
      "contexts": [
        "aggregation_selector",
        "aggs",
        "bucket_aggregation",
        "field",
        "filter",
        "number_sort",
        "score",
        "terms_set"
      ]
    },
    {
      "language": "knn",
      "contexts": [
        "score"
      ]
    },
    {
      "language": "mustache",
      "contexts": [
        "template"
      ]
    },
    {
      "language": "opensearch_compounded_script",
      "contexts": [
        "aggs",
        "filter"
      ]
    },
    {
      "language": "painless",
      "contexts": [
        "aggregation_selector",
        "aggs",
        "aggs_combine",
        "aggs_init",
        "aggs_map",
        "aggs_reduce",
        "analysis",
        "bucket_aggregation",
        "context_aware_grouping",
        "derived_field",
        "field",
        "filter",
        "ingest",
        "interval",
        "moving-function",
        "number_sort",
        "painless_test",
        "processor_conditional",
        "ranklib",
        "score",
        "script_heuristic",
        "search",
        "similarity",
        "similarity_weight",
        "string_sort",
        "template",
        "terms_set",
        "trigger",
        "update"
      ]
    },
    {
      "language": "ranklib",
      "contexts": [
        "ranklib"
      ]
    }
  ]
}
```
</details>

此回應來自兩項設定皆保持預設值的標準發行版本，因此會顯示所有類型與所有情境。確切清單取決於安裝了哪些外掛程式，因為每個外掛程式都可以註冊自己的語言與情境。在收緊任一設定後，回應會顯示縮減後的集合，這可直接驗證您的組態是否已生效。

## 限制指令碼可消耗的資源

即使指令碼被允許且正確無誤，仍可能耗用大量資源。有兩項設定可限制指令碼功能消耗的資源：

- `script.painless.regex.enabled` 與 `script.painless.regex.limit-factor` 限制正規表示式可執行的工作量，防止單一指令碼使節點停擺。如需更多資訊，請參閱 [控制正規表示式]({{site.url}}{{site.baseurl}}/scripting/painless/#controlling-regular-expressions)。
- 編譯速率限制會限制新指令碼的編譯頻率，防止大量唯一指令碼在編譯時耗盡節點的 CPU。如需更多資訊，請參閱 [指令碼編譯設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/script-and-resource-settings/#script-compilation-settings)。

## 其他安全層

指令碼設定只是保護叢集的一部分。請同時設定以下項目：

- [驗證與授權]({{site.url}}{{site.baseurl}}/security/authentication-backends/authc-index/)，讓只有已知的用戶端可以傳送請求。
- REST 與傳輸層上的 [TLS]({{site.url}}{{site.baseurl}}/security/configuration/tls/)，讓請求與叢集流量經過加密。
- [細微存取控制]({{site.url}}{{site.baseurl}}/security/access-control/index/)，讓用戶端只能存取其所需的索引與操作。
- 在叢集前方設置 IP 篩選器或防火牆，讓 API 只能從您的應用程式層連線。

如需完整說明，請參閱 [OpenSearch 的安全性]({{site.url}}{{site.baseurl}}/security/index/)。

## 相關文件

- [如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/)
- [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)
- [Get Script Languages API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/get-script-language/)
