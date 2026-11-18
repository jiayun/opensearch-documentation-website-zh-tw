"""Reuse reviewed prose only when the upstream delta is structural URL metadata.

This module does not approve a migration. Its result still needs a separate
metadata review, with the earlier content review retained as provenance.
"""
from __future__ import annotations

import copy
import json
import re

from . import config
from .frontmatter import (_top_level_span, has_modification_notice, split_document,
                          structural_problems, translatable_fields)
from .protect import legal_notice_lines
from .store import sha256_bytes

URL_METADATA = frozenset({'canonical_url', 'redirect_from', 'redirect_to'})
METADATA_REVIEW_SCOPE = 'URL metadata delta plus retained full content review'


class MetadataOnlyError(ValueError):
    pass


def _without_metadata(doc):
    lines = doc.raw.split(doc.newline)
    for key in URL_METADATA:
        span = _top_level_span(lines, key)
        if span:
            del lines[span[0]:span[1]]
    return doc.newline.join(lines)


def migrate_url_metadata(old_source: str, new_source: str, translation: str) -> str:
    """Copy exact upstream URL fields while keeping translated prose verbatim.

    Any body, translatable field, other YAML field, or non-metadata comment
    change requires ordinary translation/review instead of this shortcut.
    """
    old, new, target = map(split_document, (old_source, new_source, translation))
    if not all(doc.has_front_matter for doc in (old, new, target)):
        raise MetadataOnlyError('front matter is required')
    if not has_modification_notice(target):
        raise MetadataOnlyError('the existing translation lacks its modification notice')
    if (old.body != new.body or old.opening != new.opening or old.closing != new.closing
            or translatable_fields(old.data) != translatable_fields(new.data)):
        raise MetadataOnlyError('upstream content or translatable fields changed')
    changed = {key for key in old.data.keys() | new.data.keys()
               if key not in old.data or key not in new.data or old.data[key] != new.data[key]}
    if not changed <= URL_METADATA or _without_metadata(old) != _without_metadata(new):
        raise MetadataOnlyError('upstream delta is not limited to URL metadata')
    legal_comments = re.compile(r'^.*#.*\b(?:Copyright|SPDX-License-Identifier)\b.*$', re.I | re.M)
    if (legal_notice_lines(old_source) != legal_notice_lines(new_source)
            or legal_comments.findall(old.raw) != legal_comments.findall(new.raw)):
        raise MetadataOnlyError('upstream legal notices changed')
    if structural_problems(old.data, target.data):
        raise MetadataOnlyError('the existing translation has different structural metadata')

    expected = copy.deepcopy(target.data)
    lines = target.raw.split(target.newline)
    source_lines = new.raw.split(new.newline)
    for key in sorted(changed):
        span = _top_level_span(lines, key)
        source_span = _top_level_span(source_lines, key) if key in new.data else None
        if key in new.data and source_span is None:
            raise MetadataOnlyError(f'cannot locate upstream URL metadata: {key}')
        replacement = source_lines[source_span[0]:source_span[1]] if source_span else []
        if span:
            lines[span[0]:span[1]] = replacement
        else:
            lines.extend(replacement)
        if key in new.data:
            expected[key] = new.data[key]
        else:
            expected.pop(key, None)

    result = target.render(raw=target.newline.join(lines))
    migrated = split_document(result)
    if (migrated.data != expected or migrated.body != target.body
            or translatable_fields(migrated.data) != translatable_fields(target.data)):
        raise MetadataOnlyError('metadata migration changed reviewed content')
    return result


def metadata_continuation_problems(entry: dict, source: str | None = None,
                                   target: str | None = None) -> list[str]:
    """Require a hash-bound prior content approval for a metadata-only review.

    A later metadata update may retain an earlier metadata review. Each link
    must preserve the same prose fingerprints and lead to a full review.
    """
    review = entry.get('reviewer') or {}
    if review.get('scope') != METADATA_REVIEW_SCOPE:
        return []
    migration = (entry.get('translator') or {}).get('metadata_migration') or {}
    families = {p.get('family') for p in (entry.get('translator') or {}).get('providers', [])}
    fingerprints = {}
    try:
        for name, text in [('source', source), ('target', target)]:
            if text is not None:
                doc = split_document(text)
                fingerprints[name + '_body_sha256'] = sha256_bytes(doc.body.encode())
                fields = json.dumps(translatable_fields(doc.data), ensure_ascii=False, sort_keys=True)
                fingerprints[name + '_visible_fields_sha256'] = sha256_bytes(fields.encode())
    except ValueError:
        return ['cannot validate metadata continuation documents']
    for _ in range(64):
        retained = review.get('retained_content_review') or {}
        previous = retained.get('review') or {}
        digests = ['old_source_sha256', 'old_target_sha256', 'source_body_sha256',
                   'target_body_sha256', 'source_visible_fields_sha256', 'target_visible_fields_sha256']
        if any(not re.fullmatch(r'[0-9a-f]{64}', str(migration.get(key, ''))) for key in digests):
            return ['metadata continuation lacks complete prose fingerprints']
        if not re.fullmatch(r'[0-9a-f]{64}', str(review.get('metadata_request_sha256', ''))):
            return ['metadata continuation lacks its independent metadata request hash']
        if (retained.get('source_sha256') != migration['old_source_sha256']
                or retained.get('target_sha256') != migration['old_target_sha256']
                or previous.get('target_sha256') != migration['old_target_sha256']):
            return ['metadata continuation is not bound to the retained content review']
        if (previous.get('approved') is not True
                or previous.get('provider') not in config.REVIEW_APPROVED_PROVIDERS
                or not previous.get('model') or not previous.get('at')
                or not previous.get('family') or previous['family'] in families
                or any(i.get('severity') == 'major' for i in previous.get('issues', []))):
            return ['metadata continuation lacks a valid independent prior content review']
        if any(migration.get(key) != value for key, value in fingerprints.items()):
            return ['metadata-only review cannot cover changed prose or visible fields']
        if previous.get('scope') != METADATA_REVIEW_SCOPE:
            return []
        review, migration = previous, retained.get('metadata_migration') or {}
    return ['metadata continuation review chain is too deep']
