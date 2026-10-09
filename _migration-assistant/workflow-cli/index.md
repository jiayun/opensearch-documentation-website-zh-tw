---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Workflow CLI
nav_order: 50
has_children: true
has_toc: false
permalink: /migration-assistant/workflow-cli/
---

# Workflow CLI

Workflow CLI 是 Migration Assistant 的操作介面。它提供可重複執行遷移的方式，無需手動串接個別基礎架構命令。

Migration Assistant 將每個遷移作為 [Argo Workflows](https://argo-workflows.readthedocs.io/en/latest/) 工作執行。Argo 是 Kubernetes 原生的工作流程引擎，會將每個步驟（快照、中繼資料遷移、回填、重播、驗證）排程為一個 pod 並追蹤其狀態。您不需要了解 Argo 也能操作 Migration Assistant；Workflow CLI 就是您互動的層級。

## 設計原則

Migration Assistant 使用 Kubernetes 與工作流程來達成以下目標：

- 一次描述遷移，而不是輸入一次性的命令。
- 讓平台協調長時間執行的步驟。
- 讓進度清晰可見。
- 在需要人工驗證時於核准關卡暫停。
- 在組態變更後安全地重新提交工作流程，而無需重建環境。

## 標準操作流程

大多數遷移都遵循相同的模式：

1. 開啟 Migration Console。
2. 執行 `console --version` 以確認安裝的版本。
3. 執行 `workflow configure sample --load` 載入與版本相符的範例組態。
4. 只編輯描述您的環境與遷移路徑的欄位。
5. 執行 `console clusters connection-check` 驗證連線能力。
6. 提交試驗工作流程。
7. 執行 `workflow manage` 觀察進度與核准事項。
8. 驗證試驗結果，然後執行完整遷移。

## 核心命令

Workflow CLI 將命令分為以下幾個區段。

### Console 命令

`console` CLI 依元件將操作分組。`workflow` CLI 負責協調完整遷移；`console` CLI 則是您在驗證與疑難排解期間用來檢視或手動驅動單一元件的工具。

#### 叢集檢查命令

<table>
<thead>
<tr><th>命令</th><th>說明</th></tr>
</thead>
<tbody>
<tr><td><code>console --version</code></td><td>確認您的 console 正在執行的結構描述與行為。</td></tr>
<tr><td><code>console clusters connection-check</code></td><td>驗證 console 能連線並對來源與目標叢集完成驗證。</td></tr>
<tr><td><code>console clusters connection-check --cluster source|target|proxy</code></td><td>將檢查限制在單一叢集。</td></tr>
<tr><td><code>console clusters cat-indices [--refresh] [--cluster source|target|proxy]</code></td><td>列出單一或兩個叢集上的索引。</td></tr>
<tr><td><code>console clusters curl source /_cat/indices?v</code></td><td>對指定叢集直接發出 API 請求（路徑為位置參數）。</td></tr>
<tr><td><code>console clusters curl target /_search -X POST --json '{"query":{"match_all":{}}}'</code></td><td>傳送帶有 JSON 本文的 <code>POST</code> 請求。</td></tr>
<tr><td><code>console clusters clear-indexes --cluster target --acknowledge-risk</code></td><td><strong>破壞性操作</strong>。刪除指定叢集上的所有索引。</td></tr>
</tbody>
</table>

#### 指標與 Apache Kafka 命令

| 群組 | 命令 |
|:------|:---------|
| `console metrics` | `list`, `get-data` |
| `console kafka` | `create-topic`, `list-topics`, `delete-topic`, `describe-consumer-group`, `list-consumer-groups`, `describe-topic-records` |

### 組態命令

| 命令 | 用途 |
|:--------|:---------------|
| `workflow configure sample` | 顯示您安裝版本的範例結構描述 |
| `workflow configure sample --load` | 載入該範例作為起點 |
| `workflow configure edit` | 在您的編輯器中開啟工作流程組態（`$EDITOR`，預設為 `vi`） |
| `workflow configure edit --stdin` | 從 `stdin` 讀取 YAML 而不是開啟編輯器---適用於指令碼與 CI |
| `workflow configure view` | 顯示目前的組態 |
| `workflow configure clear` | 清除目前的組態，讓您重新開始 |

### 執行與監控命令

<table>
<thead>
<tr><th>命令</th><th>說明</th></tr>
</thead>
<tbody>
<tr><td><code>workflow submit</code></td><td>啟動遷移工作流程（會自動停止並取代同名的工作流程）。</td></tr>
<tr><td><code>workflow submit --wait --timeout 300</code></td><td>提交並封鎖直到工作流程完成或達到逾時時間。</td></tr>
<tr><td><code>workflow manage</code></td><td>監控、核准與記錄檔的主要介面（互動式 TUI）。</td></tr>
<tr><td><code>workflow status</code></td><td>以非互動形式顯示目前的工作流程樹。</td></tr>
<tr><td><code>workflow status --all</code></td><td>顯示執行中與已完成的工作流程。</td></tr>
<tr><td><code>workflow status --live-status</code></td><td>為每個節點新增即時快照／回填狀態檢查。</td></tr>
<tr><td><code>workflow log all</code></td><td>顯示工作流程各 pod 的記錄檔（使用 pod 標籤來尋找）。</td></tr>
<tr><td><code>workflow log all --follow</code></td><td>即時串流記錄檔（內部使用 <code>stern</code>）。</td></tr>
<tr><td><code>workflow log filter -l source=src,target=tgt</code></td><td>依標籤選擇器篩選。</td></tr>
<tr><td><code>workflow approve step &lt;PATTERN&gt; [&lt;PATTERN&gt; ...]</code></td><td>核准符合確切名稱或 glob 模式的待處理關卡（例如 <code>*.evaluateMetadata</code>）。</td></tr>
<tr><td><code>workflow reset</code></td><td>列出遷移 CRD 並讓您安全地刪除它們。請使用此命令而非 <code>kubectl delete workflow ...</code>。</td></tr>
<tr><td><code>workflow reset --all</code></td><td>刪除所有遷移 CRD（擷取代理程式預設受到保護；新增 <code>--include-proxies</code> 可一併移除）。</td></tr>
<tr><td><code>workflow reset &lt;NAME&gt; --cascade</code></td><td>刪除特定資源及其相依項目。</td></tr>
<tr><td><code>workflow util completions &lt;bash|zsh|fish&gt;</code></td><td>產生 shell 自動完成指令碼。</td></tr>
</tbody>
</table>

## workflow manage 命令

`workflow manage` 命令會開啟全螢幕終端機使用者介面（TUI），用於監控與管理工作流程執行。它提供以下功能：

- 檢視逐步的工作流程狀態（等待中、執行中或失敗）。
- 無需切換工具即可開啟記錄檔。
- 在關卡步驟就緒時予以核准。

## 核准關卡

並非每個遷移步驟都應在沒有人工審核的情況下執行。核准關卡讓工作流程在有意義的檢查點停止，讓您能在繼續之前進行驗證。

典型的核准點包括中繼資料遷移之後的轉換、回填里程碑，以及對切換敏感的步驟。若要檢視與核准關卡，請執行以下命令：

```bash
workflow manage
workflow approve step <STEP_NAME>
```
{% include copy.html %}

## 狀態符號

下表說明工作流程狀態輸出中顯示的符號。

| 符號 | 意義 |
|:-------|:--------|
| `✓` | 成功 |
| `▶` | 執行中 |
| `○` | 擱置中 |
| `✗` | 失敗 |
| `⟳` | 等待核准 |

## 版本相符的範例組態

工作流程結構描述會隨版本而變動。請務必載入與您安裝版本相符的範例組態，而不是手動撰寫組態。若要載入範例並加以編輯，請執行以下命令：

```bash
console --version
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}


## 結構描述感知編輯

每個版本都會發布 `workflowMigration.schema.json` 資產。console 也會在本機保留作用中的結構描述，讓您的編輯器與驗證能與安裝的版本保持一致。

在 Migration Console 上，結構描述位於：

```text
/root/.workflowUser.schema.json
```

CLI 在編輯與驗證組態時會自動使用此結構描述，因此無需另外下載。

若要以互動方式參考所有可用欄位及其類型、預設值與說明，請參閱 [Migration Assistant Schema Viewer](https://opensearch-project.github.io/opensearch-migrations/)。

## 相關文件

| 主題 | 連結 |
|:------|:-----|
| 第一個工作流程 | [使用 Workflow CLI]({{site.url}}{{site.baseurl}}/migration-assistant/workflow-cli/getting-started/) |
| 部署選擇 | [選擇您的部署方式]({{site.url}}{{site.baseurl}}/migration-assistant/migration-phases/deploy/) |
| Elasticsearch 6.8 至 OpenSearch 3.5 | [Playbook]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-elasticsearch-6-8-to-opensearch-3/) |
| Amazon OpenSearch Service 至 Serverless NextGen | [Playbook]({{site.url}}{{site.baseurl}}/migration-assistant/playbook-amazon-opensearch-service-to-serverless/) |
| 互動式結構描述參考 | [Migration Assistant Schema Viewer](https://opensearch-project.github.io/opensearch-migrations/) |
