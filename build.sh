#!/usr/bin/env bash
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.

host="localhost"

if [[ "$DOCKER_BUILD" == "true" ]]; then
    host="0.0.0.0"
fi

JEKYLL_LINK_CHECKER=internal bundle exec jekyll serve --host ${host} --port 4000 --incremental --livereload --open-url --trace
