"""Shared fixtures for the translation pipeline tests (no model inference)."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[1]
REPO = SCRIPTS.parent
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from translation_pipeline import config  # noqa: E402
from translation_pipeline.protect import TOKEN_RE  # noqa: E402
from translation_pipeline.providers import ModelReply, Provider  # noqa: E402

MATCH_PAGE = """---
layout: default
title: Match query
parent: Full-text queries
grand_parent: Query DSL
nav_order: 10
redirect_from:
  - /old/match/
---

# Match query

Use the `match` query for full-text search on a specific document field. See [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) for details.

```json
GET testindex/_search
{
  "query": { "match": { "title": "wind" } }
}
```
{% include copy-curl.html %}

## Parameters

The following table lists the parameters that the query accepts.

| Parameter | Description |
| :--- | :--- |
| `query` | The query string to use for search. |

For more information, visit https://opensearch.org/docs/latest/.
{: .note}
"""

INDEX_PAGE = """---
layout: default
title: Getting started
nav_order: 1
has_children: true
permalink: /getting-started/
description: "Get started with OpenSearch: core concepts and installation."
next_steps:
  - heading: "Intro to OpenSearch"
    description: "Learn how OpenSearch stores data."
    link: "/getting-started/intro/"
---

# Getting started

OpenSearch is a distributed search and analytics engine that you can run anywhere.
"""

LANDING_PAGE = """---
layout: default
title: Tutorials
has_children: true
nav_order: 5
# Cards rendered by the landing layout.
more_cards:
  - heading: "Vector search"
    description: "Discover <b>semantic</b> search with `knn` at {{site.url}}{{site.baseurl}}/vector-search/"
    link: "/vector-search/"
  - heading: Getting started
    description: Start here
    link: /getting-started/
features:
  - heading: Fast
    description: Low latency
    link: /fast/
    image: /images/fast.png
    image_alt: Fast icon
flows:
  - heading: Agents
    list:
      - "<b>Platform:</b> OpenSearch"
      - "<b>Model:</b> Anthropic Claude"
    link: /agents/
redirect_from:
  - /tutorials/old/
seo:
  type: TechArticle
---

# Tutorials

Browse the tutorials below.
"""

NOTICE = config.MODIFICATION_NOTICE


def zhify(text: str) -> str:
    """Deterministic fake translation: English words -> 譯, tokens untouched."""
    parts = re.split(r"(⟦P\d+⟧)", text)
    return "".join(p if TOKEN_RE.fullmatch(p) else re.sub(r"[A-Za-z][A-Za-z'’-]*", "譯", p) for p in parts)


def request_payload(prompt: str) -> dict:
    return json.loads(prompt.split("INPUT:\n", 1)[1])


def good_translation(prompt: str) -> str:
    payload = request_payload(prompt)
    return json.dumps({"schema": "zh-tw-translation-result/v1",
                       "segments": [{"id": s["id"], "text": zhify(s["text"])} for s in payload["segments"]]},
                      ensure_ascii=False)


def approve(prompt: str) -> str:
    return json.dumps({"approved": True, "issues": []})


class FakeProvider(Provider):
    def __init__(self, name: str, family: str, handler) -> None:
        self.name = name
        self.family = family
        self.model = f"{name}-test-model"
        self.handler = handler
        self.calls: list[str] = []

    def complete(self, system: str, prompt: str) -> ModelReply:
        self.calls.append(prompt)
        result = self.handler(prompt, len(self.calls))
        if isinstance(result, Exception):
            raise result
        return ModelReply(result, self.name, self.model)


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def make_repo(root: Path, pages: dict[str, str]) -> str:
    """Create a small Jekyll-like git repo and return its baseline commit."""
    (root / "_config.yml").write_text(
        "collections:\n"
        "  docs:\n    permalink: /:collection/:path/\n    output: true\n"
        "  getting-started:\n    output: true\n"
        "  hidden:\n    output: false\n", encoding="utf-8")
    for path, text in pages.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    for name in ("glossary.yml", "style-guide.md", "banned-terms.yml"):
        (root / "translation").mkdir(exist_ok=True)
        shutil.copy(REPO / "translation" / name, root / "translation" / name)
    git(root, "init", "-q")
    git(root, "add", "-A")
    git(root, "-c", "user.name=t", "-c", "user.email=t@example.com", "-c", "commit.gpgsign=false",
        "commit", "-q", "-m", "baseline")
    return git(root, "rev-parse", "HEAD")


__all__ = ["config", "FakeProvider", "make_repo", "zhify", "good_translation", "approve",
           "request_payload", "MATCH_PAGE", "INDEX_PAGE", "LANDING_PAGE", "NOTICE", "REPO"]
