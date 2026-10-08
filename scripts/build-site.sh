#!/bin/bash
set -euo pipefail

rm -rf _site

# Snapshot only reviewed Chinese; pending/rejected pages use immutable English.
SITE_MODE="${SITE_MODE:-preview}"
python3 scripts/prepare-site-source.py --mode "$SITE_MODE"
site_source=".translation-cache/site-source"
JEKYLL_ENV=production bundle exec jekyll build -q --source "$site_source" \
  --config "$site_source/_config.yml,$site_source/_config.zh-tw.yml,$site_source/_config.preview.yml" -d _site/3.9

# Generate root redirect to 3.9/
cat << 'INDEXEOF' > _site/index.html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="utf-8">
<title>重新導向中…</title>
<link rel="canonical" href="https://jiayun.github.io/opensearch-documentation-website-zh-tw/3.9/">
<meta http-equiv="refresh" content="0; url=/opensearch-documentation-website-zh-tw/3.9/">
<meta name="robots" content="noindex">
</head>
<body>
<h1>重新導向中…</h1>
<a href="/opensearch-documentation-website-zh-tw/3.9/">如果沒有自動導向，請點選此處。</a>
</body>
</html>
INDEXEOF

# Ensure 404 is usable at root
cp _site/3.9/404.html _site/404.html

# Share the identical navigation tree across pages before generating search.
python3 scripts/share-navigation.py --site _site/3.9

# Repair the shared trees once instead of rechecking them in every page.
python3 scripts/repair-built-links.py --site _site/3.9

# Run Pagefind
node_modules/.bin/pagefind --site "_site/3.9" \
  --output-path "_site/3.9/pagefind" \
  --root-selector "[data-pagefind-body]" \
  --include-characters "_"
