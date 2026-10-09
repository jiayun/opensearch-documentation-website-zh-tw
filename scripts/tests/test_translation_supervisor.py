"""Exercise the real coordinator with isolated tasks, never model CLIs."""
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest import mock
from test_translation_helpers import REPO, FakeProvider


class SupervisorTests(unittest.TestCase):
    def test_explicit_retry_resets_only_pending_pages_and_preserves_quota_cooldown(self):
        spec = importlib.util.spec_from_file_location('supervisor_retry_test', REPO / 'scripts/translation-overnight.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        manifest = SimpleNamespace(pages={
            'done': {'status': 'reviewed', 'attempts': 2},
            'pending': {'status': 'pending', 'attempts': module.config.MAX_PAGE_ATTEMPTS}},
            lock=threading.RLock(), save=lambda: None)
        providers = {name: FakeProvider(name, family, lambda p, n: '{}') for name, family in
                     [('claude', 'claude'), ('codex-review', 'codex:gpt-6-sol'), ('agy', 'gemini')]}
        class FakeRunner:
            def __init__(self, *args, **kwargs): pass
            def is_up_to_date(self, page): return manifest.pages[page]['status'] == 'reviewed'
            def select(self, pages, limit):
                return [p for p in pages if manifest.pages[p]['attempts'] < module.config.MAX_PAGE_ATTEMPTS]
            def _guarded(self, page):
                if manifest.pages[page]['attempts'] != 0:
                    raise AssertionError('explicit retry did not reset attempt limit')
                manifest.pages[page]['status'] = 'reviewed'
                return 'reviewed'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = root / '.translation-cache'
            cache.mkdir()
            quota_reset = time.time()+10000
            (cache / 'overnight-state.json').write_text(json.dumps({
                'prompt_version': 'test', 'next_quality_retry': quota_reset,
                'page_retry_after': {'pending': quota_reset},
                'disabled': {'agy': 'quota'}, 'disabled_until': {'agy': quota_reset}}))
            with mock.patch.object(module, '__file__', str(root / 'scripts/translation-overnight.py')), \
                 mock.patch.object(module.Manifest, 'load', return_value=manifest), \
                 mock.patch.object(module.PromptContext, 'load', return_value=SimpleNamespace(version='test')), \
                 mock.patch.object(module.TermRules, 'load', return_value=SimpleNamespace()), \
                 mock.patch.object(module, 'build_providers', return_value=providers), \
                 mock.patch.object(module, 'Runner', FakeRunner), \
                 mock.patch.object(module.os, 'chdir'), \
                 mock.patch.object(module.signal, 'signal'), mock.patch('builtins.print'):
                module.main(retry_now=True)
            state = json.loads((cache / 'overnight-state.json').read_text())
            self.assertEqual(state['status'], 'translation_complete_needs_final_validation')
            self.assertEqual(state['disabled']['agy'], 'quota')
            self.assertEqual(state['disabled_until']['agy'], quota_reset)
            self.assertEqual(manifest.pages['done']['attempts'], 2)

    def test_coordinator_refills_and_stops_with_atomic_checkpoint(self):
        spec = importlib.util.spec_from_file_location('supervisor_test', REPO / 'scripts/translation-overnight.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        release_slow, third_started = threading.Event(), threading.Event()
        registrations = {}
        errors = []
        manifest = SimpleNamespace(pages={p: {'status': 'pending', 'attempts': 0}
                                          for p in ['a-slow', 'b-fast', 'c-third']},
                                   lock=threading.RLock(), save=lambda: None)
        class FakeRunner:
            def __init__(self, *args, **kwargs):
                pass
            def is_up_to_date(self, page):
                return manifest.pages[page]['status'] == 'reviewed'
            def select(self, pages, limit):
                return [p for p in pages if not self.is_up_to_date(p)]
            def _guarded(self, page):
                if page == 'a-slow' and not release_slow.wait(5):
                    raise AssertionError('slow task never released')
                if page == 'c-third':
                    third_started.set()
                manifest.pages[page]['status'] = 'reviewed'
                return 'reviewed'
        providers = {name: FakeProvider(name, family, lambda p, n: '{}')
                     for name, family in [('claude', 'claude'), ('agy', 'gemini')]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            def run():
                try:
                    module.main()
                except BaseException as error:
                    errors.append(error)
            with mock.patch.object(module, '__file__', str(root / 'scripts/translation-overnight.py')), \
                 mock.patch.object(module.Manifest, 'load', return_value=manifest), \
                 mock.patch.object(module.PromptContext, 'load', return_value=SimpleNamespace(version='test')), \
                 mock.patch.object(module.TermRules, 'load', return_value=SimpleNamespace()), \
                 mock.patch.object(module, 'build_providers', return_value=providers), \
                 mock.patch.object(module, 'Runner', FakeRunner), \
                 mock.patch.object(module, 'MAX_ACTIVE', 2), \
                 mock.patch.object(module.os, 'chdir'), \
                 mock.patch.object(module.signal, 'signal', side_effect=lambda sig, handler: registrations.update({sig: handler})), \
                 mock.patch('builtins.print'):
                thread = threading.Thread(target=run)
                thread.start()
                try:
                    self.assertTrue(third_started.wait(5), 'third page must start before the slow page finishes')
                    self.assertFalse(release_slow.is_set())
                    registrations[module.signal.SIGTERM]()
                finally:
                    release_slow.set()
                    thread.join(5)
                self.assertFalse(thread.is_alive())
                self.assertFalse(errors, errors)
            state = json.loads((root / '.translation-cache/overnight-state.json').read_text())
            self.assertEqual(state['status'], 'stopped')
            self.assertEqual(state['active_pages'], [])
            self.assertEqual(state['reviewed'], 3)
            self.assertEqual(state['remaining'], 0)
