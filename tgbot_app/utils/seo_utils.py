import re
from collections import Counter

from django.conf import settings
from pymystem3 import Mystem


async def normalize_text(raw_text: str) -> str:
    mystem = Mystem()
    lemmas = mystem.lemmatize(raw_text)
    return ''.join(lemmas).strip()


async def get_word_frequencies(raw_text: str) -> list:
    limit = settings.KEYWORDS_LIMIT
    pos_filter = settings.KEYWORDS_FILTER
    mystem = Mystem()

    normalized_text = await normalize_text(raw_text)
    words = re.findall(r'\b\w+\b', normalized_text)

    filtered_words = []

    for word in words:
        if len(word) <= 2:
            continue
        analysis = mystem.analyze(word)
        if analysis and 'analysis' in analysis[0] and analysis[0]['analysis']:
            pos = analysis[0]['analysis'][0]['gr'].split(',')[0].split('=')[0]
            if pos in pos_filter:
                filtered_words.append(word)

    word_count = Counter(filtered_words)
    sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
    word_list = [word for word, _ in sorted_word_count[:limit]]

    return word_list


async def get_seo_dictionary(queryset):
    seo_dict = {}
    async for item in queryset:
        original_words = item.phrase.split()
        lemmas = item.lemmas.split()
        for i, lemma in enumerate(lemmas):
            if len(lemma) > 3 and not lemma.isdigit():
                frequency = item.frequency
                if lemma not in seo_dict or seo_dict[lemma][1] < frequency:
                    seo_dict[lemma] = (original_words[i], frequency)
    return [word for word, _ in seo_dict.values()][:settings.SEO_DICT_LIMIT]
