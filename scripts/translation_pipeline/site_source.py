"""Create a build-only snapshot without changing the running translator."""
from __future__ import annotations

import copy
from pathlib import Path
import shutil
import subprocess

from . import config
from .checks import provenance_problems, run_check
from .store import Manifest, SourceInventory, SourceStore, atomic_write_json, new_entry, now, sha256_bytes
from .terms import TermRules


def prepare_source(root: Path, destination: Path, mode: str = 'preview') -> dict:
    root, destination = root.resolve(), destination.resolve()
    if mode not in {'preview', 'complete'}:
        raise ValueError('mode must be preview or complete')
    if destination == root or root.is_relative_to(destination):
        raise ValueError('destination must not contain the repository')
    manifest = Manifest.load(root)
    inventory = SourceInventory.load(root)
    if set(manifest.pages) != set(inventory.pages) or manifest.data['baseline_commit'] != inventory.data['baseline_commit']:
        raise ValueError('manifest/source inventory mismatch')
    selected = {}
    snapshot = copy.deepcopy(manifest.data)
    reviewed = 0
    for page, entry in manifest.pages.items():
        if Path(page).is_absolute() or '..' in Path(page).parts:
            raise ValueError(f'unsafe document path: {page}')
        baseline = SourceStore(root).read(page)
        if sha256_bytes(baseline) != inventory.pages[page] or entry['source_sha256'] != inventory.pages[page]:
            raise ValueError(f'baseline hash mismatch: {page}')
        if entry['status'] == 'reviewed':
            data = (root / page).read_bytes()
            problems = provenance_problems(entry, require_review=True)
            if sha256_bytes(data) != entry.get('target_sha256') or problems:
                raise ValueError(f'reviewed page is not verified: {page}: {problems}')
            selected[page] = data
            reviewed += 1
        else:
            if mode == 'complete':
                raise ValueError(f'complete publication requires review: {page}')
            selected[page] = baseline
            replacement = new_entry(entry['source_sha256'], entry['original_front_matter'])
            snapshot['pages'][page] = replacement
    # git enumerates repository files, including new implementation files,
    # while excluding credentials, caches, dependencies and build artifacts.
    result = subprocess.run(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                            cwd=root, capture_output=True, check=True)
    names = sorted(set(result.stdout.decode().split('\0')) - {''})
    if destination.exists():
        owned_default = destination == root / '.translation-cache/site-source'
        recognized = (destination / '_data/translation_preview.json').is_file()
        if not owned_default and not recognized and any(destination.iterdir()):
            raise ValueError('refusing to replace a nonempty directory that is not a site snapshot')
        shutil.rmtree(destination)
    destination.mkdir(parents=True)
    for name in names:
        path = root / name
        if name.startswith(('.git/', '.translation-cache/', '_site/', 'node_modules/', 'vendor/bundle/')):
            continue
        if not path.is_file():
            continue
        if path.is_symlink():
            raise ValueError(f'symlink is not allowed in build source: {name}')
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for page, data in selected.items():
        target = destination / page
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    atomic_write_json(destination / config.MANIFEST_PATH, snapshot)
    report = run_check(destination, TermRules.load(destination / config.BANNED_TERMS_PATH), publish=mode == 'complete')
    if not report.ok:
        raise ValueError('snapshot integrity failed: ' + '; '.join(report.problems[:10]))
    summary = {'mode': mode, 'snapshot_at': now(), 'baseline_commit': manifest.data['baseline_commit'],
               'reviewed': reviewed, 'english': len(selected) - reviewed, 'total': len(selected)}
    atomic_write_json(destination / '_data/translation_preview.json', summary)
    atomic_write_json(destination / '_config.preview.yml', {'translation_preview': mode == 'preview'})
    return summary
