"""Static configuration shared by every pipeline module."""

from __future__ import annotations

import os
from pathlib import Path

SCHEMA_VERSION = 1
BASELINE_COMMIT = "55880db68ce90d82cf6d83ac9a44bc0fc86a07a2"
TARGET_LANGUAGE = "zh-TW"

# Root-level pages rendered by Jekyll in addition to the output collections.
ROOT_PAGES = ("index.md", "search.md", "404.md")
DOC_EXTENSIONS = (".md", ".markdown")

# Paths relative to the repository root.
TRANSLATION_DIR = "translation"
MANIFEST_PATH = "translation/manifest.json"
SOURCE_INVENTORY_PATH = "translation/source-inventory.json"
SOURCE_STORE_DIR = "translation/source"
GLOSSARY_PATH = "translation/glossary.yml"
STYLE_GUIDE_PATH = "translation/style-guide.md"
BANNED_TERMS_PATH = "translation/banned-terms.yml"
CACHE_DIR = ".translation-cache"

# Work-item sizing. A page whose body exceeds CHUNK_LIMIT characters is split
# on structural boundaries; review covers the whole page in one request unless
# original + translation exceed REVIEW_LIMIT characters.
CHUNK_LIMIT = 12000
REVIEW_LIMIT = 60000

MAX_WORKERS = 4
MAX_PAGE_ATTEMPTS = 3           # translate/review cycles per page
MAX_CHUNK_TRIES = 3             # tries for a structurally valid chunk output
TRANSPORT_RETRIES = 2           # extra tries after a transport failure

# Front matter fields that are visible text and get translated. Ancestor
# fields stay in baseline English; the site plugin maps them to translated
# titles through manifest.original_front_matter.
TRANSLATABLE_FM_FIELDS = ("title", "description", "summary")
# Inside nested mappings/lists under any other root (card lists, next_steps,
# flows...), string values under these keys are translated, as are the string
# items of a `list` key. Everything else (link, url, image, id, icon...) is kept.
TRANSLATABLE_NESTED_KEYS = frozenset({"heading", "title", "description", "summary", "text", "image_alt", "alt"})
TRANSLATABLE_LIST_KEY = "list"
# Roots never searched for visible text.
STRUCTURAL_FM_ROOTS = frozenset({
    "layout", "parent", "grand_parent", "great_grand_parent", "permalink", "redirect_from",
    "nav_order", "nav_exclude", "has_children", "has_toc", "has_math", "heading_anchors",
    "sitemap", "seo", "datatable", "section", "link", "url", "src", "image", "id", "icon",
    "api", "api_identifier", "apis", "spec_insert", "canonical_url",
})
ORIGINAL_FM_FIELDS = ("title", "parent", "grand_parent", "great_grand_parent")

# Apache-2.0 section 4(b) modification notice, a YAML comment placed on the
# line right after the opening `---` of every translated page.
MODIFICATION_NOTICE = ("# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese "
                       "translation and website adaptations.")

PILOT_PATHS = (
    "_getting-started/index.md",
    "_getting-started/intro.md",
    "_getting-started/quickstart.md",
    "_api-reference/index-apis/create-index.md",
    "_query-dsl/full-text/match.md",
    "_data-prepper/getting-started.md",
    "_benchmark/index.md",
    "_clients/index.md",
)

# ollama-local is opt-in until a pilot run qualifies its output quality.
DEFAULT_TRANSLATORS = ("ollama-cloud-glm", "ollama-cloud",
                       "claude", "codex", "ollama-cloud-glm-backup", "ollama-cloud-gemma", "agy-gpt", "agy", "agy-flash")
DEFAULT_REVIEWERS = ("agy-sonnet", "agy-opus", "codex-review", "agy", "claude")
# Providers whose reviews count as quality-approved for publishing.
REVIEW_APPROVED_PROVIDERS = frozenset({"agy", "agy-sonnet", "agy-opus", "claude", "codex", "codex-review"})

# Existing ChatGPT subscription; modest reasoning effort for bounded translation work.
CODEX_TRANSLATION_MODEL = "gpt-6.1-sol"
CODEX_REVIEW_MODEL = "gpt-6-sol"

OLLAMA_URL = os.environ.get("TRANSLATION_OLLAMA_URL", "http://localhost:11434/api/chat")
OLLAMA_CLOUD_MODEL = "deepseek-v4.1-flash:cloud"
OLLAMA_CLOUD_MODELS = {
    "ollama-cloud": OLLAMA_CLOUD_MODEL,
    "ollama-cloud-glm": "glm-5.3-flash:cloud",
    "ollama-cloud-glm-backup": "glm-5.2:cloud",
    "ollama-cloud-gemma": "gemma4:cloud",
}
TRANSLATION_WEIGHTS = ("ollama-cloud-glm", "ollama-cloud", "ollama-cloud-glm", "ollama-cloud", "claude",
                       "ollama-cloud-glm", "ollama-cloud", "ollama-cloud-glm", "ollama-cloud", "codex")
# Verified against each model's /api/show thinking.values (2026-10-08).
OLLAMA_CLOUD_THINKING = {
    "glm-5.3-flash:cloud": "low",
    "deepseek-v4.1-flash:cloud": False,
    "glm-5.2:cloud": False,
    "gemma4:cloud": False,
}
OLLAMA_LOCAL_MODEL = "gemma4:12b-mlx"
AGY_MODEL = "gemini-3.1-pro-high"
AGY_MODELS = {
    "agy": (AGY_MODEL, "gemini"),
    "agy-flash": ("gemini-3.8-flash-low", "gemini"),
    "agy-sonnet": ("claude-sonnet-5-5-medium", "claude-gpt"),
    "agy-opus": ("claude-opus-5-5-medium", "claude-gpt"),
    "agy-gpt": ("gpt-oss-120b-medium", "claude-gpt"),
}
REVIEW_WEIGHTS = ("agy", "agy", "agy-sonnet", "codex-review")

# Environment variables removed before launching a model CLI so that the CLIs
# authenticate with the signed-in account and never fall back to paid API keys.
SCRUBBED_ENV_VARS = (
    "ANTHROPIC_API_KEY",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDECODE",
    "CLAUDE_CODE_ENTRYPOINT",
    "GEMINI_API_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_GENAI_USE_VERTEXAI",
    "GOOGLE_APPLICATION_CREDENTIALS",
    "OPENAI_API_KEY",
    "CODEX_API_KEY",
)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]
