from django.urls import NoReverseMatch
from difflib import SequenceMatcher
from django.urls import reverse
from .models import Websites
import logging
import random
import unicodedata

logger = logging.getLogger(__name__)

def resolve_target(website:Websites):
    """
    失效路由处理
    """
    try:
        return website.get_target_url() or None
    except NoReverseMatch:
        logger.warning(
            "route is valid: id=%s, route_name=%s",
            website.pk,
            website.route_name
        )
        return None

def get_random_websites(limit=3)-> list[dict]:

    websites = Websites.objects.filter(
        is_active=True,
        show_in_random=True,
    ).order_by("pk")

    unique_targets = {}

    for website in websites:

        target_url = resolve_target(website)

        if not target_url:
            continue
        if target_url in unique_targets:
            continue

        unique_targets[target_url] = {
            "name": website.name,
            "description": website.description,
            "url":target_url,
        }

    pool = list(unique_targets.values())

    return random.sample(
        pool,
        k=min(len(pool), limit)
    )

def normalize_search(value):
        return (
            unicodedata.normalize("NFKC", value)
            .casefold()
            .strip()
            .strip("/")
            .strip()
        )

def match_target_url(raw_query):

    fallback_url = reverse("index:index")
    query = normalize_search(raw_query)

    if not query:
        return fallback_url

    websites = Websites.objects.filter(
        is_active=True,
        search_enabled=True,
    ).exclude(
        route_name=''
    ).order_by("search_order","pk")

    best_url = fallback_url
    best_score = -1.0

    for website in websites:

        target_url = resolve_target(website)

        if not target_url:
            continue

        aliases = website.search_aliases

        if not isinstance(aliases, list):
            aliases = []

        raw_terms = [
            website.name,
            target_url,
            *aliases,
        ]

        terms = [
            normalize_search(term)
            for term in raw_terms
            if isinstance(term,str)
        ]

        score = max(
            (
                SequenceMatcher(
                    None,
                    query,
                    term,
                    autojunk=False
                ).ratio()
                for term in terms
                if term
            ),
            default=0.0
        )

        if score > best_score:
            best_score = score
            best_url = target_url

    return best_url