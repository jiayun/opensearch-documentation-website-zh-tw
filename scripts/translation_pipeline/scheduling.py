"""Keep review backlog moving while giving cloud translation regular work."""

def mixed_batch(candidates, entries, limit=25):
    reviews = [page for page in candidates if entries[page].get('status') == 'translated']
    translations = [page for page in candidates if entries[page].get('status') != 'translated']
    selected = []
    review_index = translation_index = 0
    while len(selected) < limit and (review_index < len(reviews) or translation_index < len(translations)):
        for _ in range(3):
            if review_index < len(reviews) and len(selected) < limit:
                selected.append(reviews[review_index])
                review_index += 1
        if translation_index < len(translations) and len(selected) < limit:
            selected.append(translations[translation_index])
            translation_index += 1
    return selected
