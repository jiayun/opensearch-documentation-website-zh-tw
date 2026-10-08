#!/usr/bin/env python3
"""Build a verified Chinese/English preview snapshot or require full review."""
import argparse
import json
from pathlib import Path
from translation_pipeline.site_source import prepare_source

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
parser.add_argument('--destination', type=Path, default=Path('.translation-cache/site-source'))
parser.add_argument('--mode', choices=['preview', 'complete'], default='preview')
args = parser.parse_args()
try:
    print(json.dumps(prepare_source(args.root, args.destination, args.mode), ensure_ascii=False))
except (ValueError, OSError) as error:
    parser.exit(1, f'prepare-site-source: {error}\n')
