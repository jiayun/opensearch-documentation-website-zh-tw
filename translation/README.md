# zh-TW translation pipeline

This directory holds the state of the Taiwan Traditional Chinese (zh-TW)
translation of the OpenSearch documentation on branch `3.9-zh-tw`. The
pipeline is `scripts/translation.py`.

The source inventory contains 1,870 pages. Translation and independent review run in batches; use
`python3 scripts/translation.py status` for live completion, pending work and errors.

## Layout

| Path | Tracked | Purpose |
| --- | --- | --- |
| `translation/manifest.json` | yes | Per-page state, hashes and provenance |
| `translation/source-inventory.json` | yes | Page set and source hashes pinned by `init`; never written by `run` |
| `translation/source/<page>` | yes | Immutable baseline content, byte-identical to the baseline commit (plain files) |
| `translation/glossary.yml` | yes | zh-TW terminology; included in every prompt |
| `translation/style-guide.md` | yes | zh-TW style rules; included in every prompt |
| `translation/banned-terms.yml` | yes | Mainland China terms and simplified characters, with exceptions |
| `translation/schemas/*.json` | yes | JSON Schemas for the model request/result formats |
| `.translation-cache/` | no (ignored) | Validated chunk results, approved reviews, commit journal, run logs |

Baseline commit: `ea8f887557c3a673bbb1200837e750ca0d02de7a`. Pages are all
`output: true` collections in the baseline `_config.yml` (files with front
matter) plus `index.md`, `search.md` and `404.md`. `translation/` (including
the inventory and source store) is excluded from the Jekyll build by
`_config.zh-tw.yml`.

## Requirements

- Python 3.10+ and `pip install -r requirements-translation.txt` (PyYAML).
- `git` (only for `init`).
- For `run`: signed-in `claude` and `agy` CLIs, and optionally Ollama on
  `localhost:11434`. `init`, `status`, `check` and the tests make no model
  calls.

## Commands

```sh
python3 scripts/translation.py init                  # store baseline, create/extend manifest (idempotent)
python3 scripts/translation.py status [--pilot | --paths a,b] [-v] [--json]
python3 scripts/translation.py run --pilot --dry-run  # show the plan, no model calls or writes
python3 scripts/translation.py run --pilot            # translate + review the 8 pilot pages
python3 scripts/translation.py run --paths _clients/index.md,_benchmark/index.md
python3 scripts/translation.py run --limit 20 --workers 2 --stop-on-quota
python3 scripts/translation.py check                  # publish gate (same as --complete)
python3 scripts/translation.py check --allow-incomplete   # integrity of the work done so far
python3 scripts/translation.py check --pilot          # pilot pages must be reviewed (not the publish gate)
```

`--pilot` and `--paths` are mutually exclusive in `status`, `run` and `check`.
`check --pilot` / `check --paths` require the selected pages to be reviewed
(add `--allow-incomplete` for integrity only); the page set is always checked
in full against the inventory. `check --complete` (used by the deploy
workflow) refuses `--pilot`/`--paths`.

`run` options:

- `--pilot`, `--paths a,b` (repeatable), `--limit N`: selection. Pages that are
  reviewed and current are skipped. Pages out of attempts are skipped unless
  `--reset-attempts`.
- `--workers 1..4`: pages processed in parallel (maximum 4).
- `--translator ollama-cloud-glm,ollama-cloud,claude,codex,ollama-cloud-glm-backup,ollama-cloud-gemma,agy-gpt,agy,agy-flash`: translator chain (default shown).
  `ollama-local` is opt-in until a pilot run qualifies its output.
- `--reviewer agy-sonnet,agy-opus,codex-review,agy,claude|none`: reviewer chain (default shown). 每份譯文使用不同模型家族校對，Codex 可立即分攤工作。
- `--stop-on-quota` (alias `--run-stop-on-quota`): stop starting new pages as
  soon as any provider reports a quota limit.
- `--claude-model NAME`: pass `--model` to `claude` (default: account default).

Exit codes: `0` success, `1` some pages failed (or check failed), `2` usage
error, `3` stopped because no translator was available or a quota stop was
requested.

Output is aggregate only (`progress 3/8: reviewed=2 failed=1`), followed by a
per-provider `usage` line. Details are in
`.translation-cache/logs/run-<UTC timestamp>.jsonl`.

## Pilot pages

`_getting-started/index.md`, `_getting-started/intro.md`,
`_getting-started/quickstart.md`, `_api-reference/index-apis/create-index.md`,
`_query-dsl/full-text/match.md`, `_data-prepper/getting-started.md`,
`_benchmark/index.md`, `_clients/index.md`. All exist at the baseline. If a
requested path is missing, `run` resolves it to a same-topic page in the same
directory and prints a `note:`; it aborts before any model call when nothing
matches.

## Manifest

`translation/manifest.json` has `schema_version`, `baseline_commit`,
`target_language`, `source_store`, and `pages`, keyed by source path:

| Field | Meaning |
| --- | --- |
| `source_sha256` | SHA-256 of the baseline file (`translation/source/<page>`) |
| `original_front_matter` | Baseline `title`, `parent`, `grand_parent`, `great_grand_parent` (only keys present) |
| `status` | `pending`, `translated` (written, not reviewed) or `reviewed` |
| `attempts` | Completed translation passes (maximum 3) |
| `target_sha256` | SHA-256 of the translated file as committed |
| `translated_source_sha256` | Source hash the translation was made from |
| `translator` | `providers` (provider, model, family, chunks), `prompt_version`, `at` |
| `reviewer` | provider, model, family, `approved`, `issues`, `target_sha256` reviewed, `prompt_version`, `at` |
| `last_error` | Last failure for this page, if any |

The site uses `original_front_matter` to map English `parent` /
`grand_parent` / `great_grand_parent` labels to translated titles, and reads
`translation/source/<page>` to keep English heading IDs.

## How a page is translated

1. **Work item**: one page; every page must have front matter. Visible
   front matter text is sent for translation: root `title`, `description`,
   `summary`, and, inside nested mappings/lists under any other
   non-structural root (`more_cards`, `next_steps`, `features`, `flows`, ...),
   string values under `heading`, `title`, `description`, `summary`, `text`
   plus the string items of `list`. Segment IDs are paths such as
   `fm.more_cards.0.heading` or `fm.flows.1.list.2`; keys containing dots or
   other characters outside `[A-Za-z0-9_-]` are never translated. `parent`
   and other ancestors, `permalink`, `redirect_from`, nav keys, `seo`, and
   nested `link`, `url`, `image`, `image_alt`, `id`, `icon` stay baseline
   English. Only the top-level keys holding a changed field are rewritten
   (scalars as one quoted line, nested roots with `yaml.safe_dump`); other
   lines and comments are kept, and the result must parse to exactly the
   baseline mapping except for the translated values. HTML, Liquid, inline
   code and URLs inside these strings are placeholders like in the body.
2. **Protection**: fenced code blocks, Liquid `raw`/`comment`/`capture`
   blocks, Liquid tags and `{{ }}` output, HTML comments, `$$` math, inline
   code, link and image destinations, reference labels and definitions,
   autolinks, bare URLs, kramdown attribute lists (`{: .note}`, `{#id}`),
   footnote markers, HTML tags, and copyright/SPDX/license/permission
   notice lines become unique placeholders such as `⟦P12⟧`. A path written
   directly after Liquid output (`{{site.url}}{{site.baseurl}}/x/`) is part of
   the Liquid placeholder.
3. **Chunking**: a body over 12,000 characters (measured on the original
   text) is split at blank-line boundaries, preferring a heading boundary; an
   oversized single block falls back to line boundaries. Protected blocks are
   never split. Segments without any letters (for example a chunk that is a
   single code block) are passed through without a model call.
4. **Model call**: the request (`translation/schemas/translation-request.schema.json`)
   lists segments with IDs (`fm.title`, `body.000`, ...) and metadata (page,
   source hash, chunk index, prompt version). The reply must be a JSON object
   whose `segments` list has exactly the same segment IDs, each once; a
   repeated ID is a validation problem.
5. **Validation per chunk**: all segment IDs present; the placeholder
   multiset is identical; block placeholders stay on their own lines in the
   same order; heading levels and table row counts are unchanged; prose is
   actually translated; the reply is not much shorter than the source; no
   banned terms. Invalid or truncated replies are retried with the problems
   listed (up to 3 tries per chunk).
6. **Page assembly and checks**: placeholders are restored and the page is
   compared with the baseline: fenced code byte-for-byte, the same protected
   code/Liquid/URL/legal regions, heading count and levels, front matter
   structure (links, images, list lengths and card order) and protected
   regions per front matter field, and terminology.
   The modification notice (below) is inserted before these checks and
   before the target hash is computed.
7. **Review**: a reviewer from a different provider family sees the full
   original and translated text, aligned by heading sections
   (`review-request.schema.json`), and returns `{approved, issues}`. Pages
   whose original + translation exceed 60,000 characters are reviewed in
   consecutive parts by the same reviewer; all parts must approve. An
   approval that lists a `major` issue counts as a rejection.
8. **Fix loop**: on rejection, the affected chunks (mapped from the issue's
   section ID) are retranslated with the findings. At most 3 translation
   passes per page; after that the page stays `pending` (or `translated`) and
   the file is not changed. The rejected text is kept in the cache.
9. **Commit**: the coordinator writes a journal entry, writes the file
   atomically (temp file, fsync, rename), saves the manifest atomically, then
   clears the journal.

If no quality-approved reviewer is available (quota, auth, unavailable, or
only the translator's own family is left), the page is committed as
`translated`. A later `run` reviews it without retranslating.

## Modification notice (Apache-2.0 section 4)

Every translated page gets one YAML comment as the first line after the
opening `---`:

```yaml
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
```

It is inserted idempotently by the pipeline (not by the model), adds no YAML
data key and no body comment, and is required by `check` for every
`translated`/`reviewed` page. A recorded translation without it is
retranslated instead of reviewed. Existing copyright, SPDX and license
notices are protected verbatim; prompts tell the translator and reviewer that
this English legal text is intentional, and that source text (including any
mention of attribution or licenses) is content, never instructions.

## Providers and failure policy

| Name | Role | How it is called |
| --- | --- | --- |
| `claude` | first translator; reviewer for non-Claude translations | `claude -p --tools '' --output-format json --no-session-persistence --system-prompt …`, prompt on stdin |
| `agy` | second translator; first reviewer | `agy --model gemini-3.1-pro-high --mode plan --output-format json --disable-slash-commands --print=<prompt>` (one argv element, empty stdin) |
| `ollama-cloud` | third translator | HTTP `POST localhost:11434/api/chat`, model `gemma4:cloud` |
| `ollama-local` | opt-in translator (not a default until a pilot qualifies it) | same, model `gemma4:12b-mlx` |

The reviewer is always a different provider family from every translator of
the page (a Claude translation is reviewed by `agy` and vice versa).

- CLIs run with `shell=False` in a fresh temporary directory outside the
  repository; model workers only return text. Only the coordinator writes
  files.
- `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `GOOGLE_API_KEY`, `OPENAI_API_KEY`
  and similar variables are removed from the child environment so the CLIs use
  the signed-in account. The pipeline never uses paid API keys.
- Failures are classified as `quota`, `auth`, `unavailable`, `transport`, or
  invalid/truncated replies. Only `quota`/`auth`/`unavailable` disable a
  provider for the rest of the run and move on to the next provider in the
  chain. `transport` failures are retried twice on the same provider, then the
  page fails for this run (no attempt is consumed). Invalid or truncated
  replies are retried as validation problems.
- The `agy` JSON envelope is nested; the parser looks for the answer text
  under common keys (`response`, `result`, `text`, `candidates[].content.parts`,
  assistant `messages`) and treats `finishReason`/`stop_reason` values such as
  `MAX_TOKENS` as truncation.
- Logs store provider, purpose, timing, sizes, error kind and a redacted error
  excerpt. `usage` holds only token counters the provider reported itself
  (Claude `usage`, agy `usage`/`usageMetadata`, Ollama `prompt_eval_count` /
  `eval_count`); none are invented when a provider reports nothing. CLI-side
  estimates such as Claude's `total_cost_usd` are logged separately as
  `estimated` and printed as "CLI estimate (not billed usage)". API keys, bearer tokens and similar strings are redacted; prompts
  and environment variables are not logged.

## Cache, resume and invalidation

- Validated chunk results are cached under a key that includes the page,
  `source_sha256`, prompt version (hash of the prompt template, glossary,
  style guide and banned terms), chunk content and findings. Editing the
  glossary or style guide, or a new source hash, invalidates the cache.
- Approved reviews are cached by translated text hash; rejections are not.
- A run interrupted mid-page resumes from the chunks already validated. A
  crash between writing the file and saving the manifest is recovered from
  the journal on the next run.
- A page whose file differs from both the baseline and the recorded
  translation is never overwritten (`refusing to overwrite`).

## Publish check

`check` (alias `check --complete`) fails unless, for every page:

- `translation/source-inventory.json` exists, names the baseline commit, and
  the manifest and the source store list exactly its pages, with
  `source_sha256` equal to its hashes (so removing a page's blob and manifest
  entry together still fails; no git history is needed);
- the baseline file exists and matches `source_sha256`;
- `status` is `reviewed`, the current file matches `target_sha256`, and the
  translation was made from the current `source_sha256`;
- translator and reviewer provenance are complete, the reviewer is `agy` or
  `claude`, approved this exact `target_sha256`, and is a different provider
  family from every translator of the page;
- content checks pass: modification notice, front matter structure and
  per-field protected regions, fenced code, protected regions, headings, no
  leftover placeholders and no banned terms in prose.

`check --allow-incomplete` applies the same checks to `translated` and
`reviewed` pages and requires `pending` files to equal the baseline.

## Terminology check

`banned-terms.yml` lists Mainland China terms with their Taiwan equivalents.
Only prose is scanned: code, inline code, Liquid, URLs and other protected
regions are ignored. `error` terms and any simplified-only character fail the
translation and the publish check. `warning` terms (words with legitimate
Taiwan usages, such as 設置 or 數據) are reported only. An occurrence inside
an `exceptions` phrase (for example 支持向量機, 在線上, 用戶端) is ignored.

## Known limitations

- Nested front matter `image_alt` text is kept in English (not in the
  visible-key list). Reordering the plain-text items of a `list` cannot be
  detected structurally; only the reviewer can catch it.
- Indented (four-space) code blocks are not protected; the docs use fenced
  code.
- The `agy` envelope parsing was written from the CLI help and unit-tested
  against assumed envelope shapes (and usage keys); it has not yet been
  exercised against a live `agy` run.
- `agy --mode plan` may still offer the model read-only tools despite the
  prompt rules. It runs in an empty temporary directory outside the
  repository with the prompt as its only input, so it has no workspace to
  read; `claude` runs with `--tools ''`. No permission-bypass flags are used.
- An upstream sync needs a deliberate re-baseline under the runner's exclusive
  lock; `init` does not migrate an existing baseline. Verify and back up the old
  sources and translations, compare the two Git revisions, and reset only pages
  whose source bytes changed. Preserve identical-source translations and their
  review records. Update the source store, manifest, inventory, config, license
  baseline, and validated navigation pins together. Retranslate and independently
  review changed pages, then run the complete publication checks.

## Tests

```sh
python3 -m unittest discover -s scripts/tests -p 'test_translation*.py'
```

The tests use fake providers and temporary git repositories; they make no
model calls.

## 已完成中文與英文回退的公開預覽

使用者已授權先發布部分完成的 3.9 預覽。`SITE_MODE=preview ./scripts/build-site.sh` 會建立獨立建置快照：僅使用 `reviewed`、通過獨立校對且雜湊一致的中文，其餘文件使用 `translation/source/` 的固定上游英文。工作中的譯文及進度清單不被覆寫，網站標示預覽狀態與快照完成數。

GitHub Actions 以 repo 變數 `PUBLISH_39_PREVIEW=true` 啟用此預覽部署，仍檢查快照完整性、連結、搜尋及授權。正式全文中文版維持 `SITE_MODE=complete`／`PUBLISH_39=true` 的全部校對要求；`check --complete` 不因預覽模式而放寬。

## 配額切換與 Codex 分攤工作

agy 的模型與配額分開管理，使用 `agy models` 查到的識別字，不改動使用者互動介面的預設選項：

| 來源名稱 | 指定模型 | agy 配額群組 | 用途 |
| --- | --- | --- | --- |
| `agy-sonnet` | `claude-sonnet-5-5-medium` | Claude／GPT | 一般校對優先 |
| `agy-opus` | `claude-opus-5-5-medium` | Claude／GPT | 超過 45,000 字元的校對提示優先 |
| `agy-gpt` | `gpt-oss-120b-medium` | Claude／GPT | 翻譯備援，尚未列入正式校對來源 |
| `agy` | `gemini-3.1-pro-high` | Gemini | 主動分攤獨立校對 |
| `agy-flash` | `gemini-3.8-flash-low` | Gemini | 翻譯後備 |

每個群組內的模型共享停用與 CLI 回報的重置時間，另一組仍可用；不把 agy 的 Claude／GPT 配額與獨立 Claude CLI 公司帳號配額混在一起。校對獨立性則看模型家族：agy Claude 與獨立 Claude CLI 都屬於 `claude`，不得互相校對同一譯文。數字百分比不由本程式估算，實際配額不足以服務回覆判定。

一般校對的輪替為 Gemini Pro、Gemini Pro、Sonnet、Codex；跳過冷卻中或與譯文同家族的來源。Gemini 群組可用時會實際分到工作，不必等 Codex 不可用才接手；Claude／GPT 群組冷卻時，Gemini Pro 約承擔三分之二的一般校對呼叫。

Claude 的 `You've hit your session limit · resets 3am (Asia/Taipei)` 會歸類為配額耗盡，立即停用該次執行的 Claude，不做連線重試。其他執行緒也會跳過已停用來源。CLI 明確回報重置時間與時區時，批次會等到該時間後一分鐘再恢復 Claude 優先順序；未回報重置時間則不自行猜測。

夜間排程讓可用工具分攤呼叫，約 80% 新翻譯呼叫交給 Ollama Cloud：`glm-5.3-flash:cloud` 約 40%、`deepseek-v4.1-flash:cloud` 約 40%，`glm-5.2:cloud`／`gemma4:cloud` 備援；Cloud 同時最多 2 個請求。依使用者指示，Kimi K3 消耗過大，排除於翻譯、備援及試跑。模型退役或不可用時切換其他來源；帳號配額耗盡時一併暫停 Cloud 模型，不逐一重試相同配額。明確的並行請求上限屬於暫時容量，不能誤判為五小時配額耗盡。Codex 可立即加入，使用既有 ChatGPT 登入配額，翻譯採 `gpt-6.1-sol`／low，獨立校對採 `gpt-6-sol`／medium；皆在獨立暫存目錄使用 read-only sandbox。每份譯文仍由不同模型校對，額外付費 API 不自動接替。

無可用獨立校對模型的頁面保存為 `translated`，後續續跑只需補校對；原有 `reviewed` 頁面不會重做。
# 夜間續跑與配額保留

`python3 -u scripts/translation-overnight.py` 使用持續補工排程，最多 4 頁同時處理，待校對與新翻譯交錯派發；任一頁完成即補入下一頁，避免校對佇列讓 Cloud 翻譯一直閒置。Claude、agy、Ollama、Codex 立即分攤工作，翻譯與校對維持不同模型，沿用完整發布門檻。執行期間不要另開 `translation.py run` 或手動改寫 manifest；兩種 runner 使用同一個排他鎖。

Claude 配額在服務明示的重置時間後重新探測；其他未知重置時間每 5 小時最多探測一次。品質失敗保留待處理，冷卻後再試，不降低校對要求。

依 `/api/show` 支援值，GLM 5.3 Flash 翻譯使用 `think: low`，DeepSeek v4.1 Flash／GLM 5.2／Gemma 使用 `think: false`。兩個主力 Cloud 模型已用相同短文件驗證格式、程式碼與用語，正式產出仍需不同模型獨立校對。

Codex 每次工作前透過 app-server 讀取已登入帳號的實際週用量；週剩餘 ≤25% 就停止翻譯／校對，保留使用者要求的 20% 及 5 個百分點緩衝。用量未知時停止 Codex 工作，5 分鐘後再查詢；讀取失敗不能當成帳號五小時配額耗盡，重新派工前仍需確認用量。這是本 repo 的派工限制，無法限制使用者在其他 Codex 工作階段的消耗，也無法保證單次請求的實際扣額。

即時記錄：`.translation-cache/overnight-console.log`、`.translation-cache/overnight-state.json`、`.translation-cache/overnight.pid`。停止時可向 pid 傳送 SIGTERM，讓正在處理的頁面完成存檔。全部頁面完成時排程停止，仍需執行網站、搜尋、導覽與授權的最終驗證才能發布。

使用者要求立即重試退件文件時，先讓現有 runner 完成停機並釋放排他鎖，再執行 `python3 -u scripts/translation-overnight.py --retry-now`。這只重設未完成頁面的有限嘗試與品質重試等待，不清除 Claude、agy、Ollama 或 Codex 的實際配額限制，也不降低獨立審查要求。

退件草稿會另外保存於 `.translation-cache/pending-repairs/`，包含來源雜湊、譯文、完整模型來源與審查問題；它不表示審查通過。續跑先驗證草稿的結構與來源，再進行局部修補和整頁獨立審查。提示版本改變時先以新規則重審草稿，避免套用失效的段落編號。缺少可信模型來源、程式碼有變動或來源不同的草稿不會被採用。

`translation/source-errata.json` 記錄少量上游 Markdown 格式錯誤的修正，例如缺少程式碼圍欄或錯誤的反引號。每項修正限定原始全文 SHA-256，並要求精確替換文字只出現一次；來源更新後不會默默沿用。`translation/source/` 與來源清單維持原始英文，翻譯、結構檢查和網站英文錨點重建在記憶體中套用相同格式修正，保留 API、程式碼內容與範例值。

導覽對應先比對完整的上游階層；上游省略祖先欄位時，只採用同集合中唯一的原始標題，跨集合則要求唯一且完整的階層相符。已改名的父頁使用 `translation/navigation-aliases.json` 明確指定來源頁面，並核對基準版本、原始標題與來源雜湊；子頁採用該父頁的實際階層。名稱有歧義、來源變動或父頁不存在時，全文建置仍會失敗，須修正資料後才能發布。


## 退件修補與持續補工

校對退件時，能定位到段落的重大問題使用既有中文做局部修補。模型只收到受影響段落的原文、既有中文與校對問題，其餘段落保持逐位元相同；語意修補優先使用可用的 Claude／Codex。每次修補仍經完整結構檢查與整篇獨立校對。全域問題、未知段落或保護內容無法可靠對齊時，保守退回完整重翻。`repairs` 快取依原文、既有譯文、問題與提示版本識別，不能當作校對通過。

夜間排程最多維持 4 個進行中的頁面，一個完成立即補工；慢頁不會擋住其餘空位。30 秒心跳與每次完成均更新 `.translation-cache/overnight-state.json`，包含 active_pages、完成／待處理數及各來源冷卻時間。失敗有冷卻與次數上限，提示規則或術語更新才開啟新的有限重試，不重做已完成文件。暫停停止補工，既有任務完成後保存一致的進度。
