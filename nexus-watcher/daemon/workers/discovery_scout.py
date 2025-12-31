"""Discovery scout worker for finding new AI/AGI APIs."""

import asyncio
import aiohttp
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta

from .base_worker import BaseWorker
from ..database.models import DiscoveredAPI, DiscoverySource
from ..utils.helpers import timestamp_iso, validate_url


class DiscoveryScoutWorker(BaseWorker):
    """Worker that discovers new AI/AGI APIs."""

    def __init__(self, *args, **kwargs):
        super().__init__("discovery_scout", *args, **kwargs)

    async def _search_github(self, session: aiohttp.ClientSession) -> List[DiscoveredAPI]:
        """
        Search GitHub for AI/AGI related repositories.

        Args:
            session: aiohttp session

        Returns:
            List of discovered APIs
        """
        discovered = []
        github_token = self.config.get('discovery_scout.github_token')

        if not github_token:
            self.logger.warning("No GitHub token configured, skipping GitHub search")
            return discovered

        headers = {
            'Authorization': f'token {github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Search queries for AI/AGI APIs
        search_queries = [
            'ai api',
            'machine learning api',
            'llm api',
            'artificial intelligence api',
            'neural network api',
            'gpt api',
            'chatbot api',
            'vision api',
            'speech api',
            'embeddings api',
        ]

        max_results = self.config.get('discovery_scout.max_results_per_scan', 50)
        per_query_limit = max(5, max_results // len(search_queries))

        for query in search_queries:
            try:
                url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_query_limit}"

                async with session.get(url, headers=headers) as response:
                    if response.status != 200:
                        self.logger.warning(f"GitHub API returned {response.status} for query: {query}")
                        continue

                    data = await response.json()
                    items = data.get('items', [])

                    for repo in items:
                        # Extract API info
                        name = repo.get('full_name', '')
                        description = repo.get('description', '')
                        homepage = repo.get('homepage', '')
                        stars = repo.get('stargazers_count', 0)
                        language = repo.get('language', '')

                        # Calculate confidence score
                        confidence = self._calculate_confidence(
                            name, description, stars, language, homepage
                        )

                        threshold = self.config.get('discovery_scout.confidence_threshold', 0.7)
                        if confidence < threshold:
                            continue

                        # Use homepage as endpoint if available, otherwise repo URL
                        endpoint = homepage if homepage and validate_url(homepage) else repo.get('html_url', '')

                        if not endpoint:
                            continue

                        discovered.append(DiscoveredAPI(
                            url=endpoint,
                            name=name,
                            description=description,
                            source=DiscoverySource.GITHUB.value,
                            confidence_score=confidence,
                            discovered_at=timestamp_iso(),
                            metadata={
                                'stars': stars,
                                'language': language,
                                'repo_url': repo.get('html_url', ''),
                                'query': query
                            }
                        ))

                # Rate limiting
                await asyncio.sleep(1)

            except Exception as e:
                self.logger.error(f"GitHub search error for query '{query}': {e}")
                continue

        self.logger.info(f"Discovered {len(discovered)} APIs from GitHub")
        return discovered

    async def _search_product_hunt(self, session: aiohttp.ClientSession) -> List[DiscoveredAPI]:
        """
        Search Product Hunt for AI tools.

        Args:
            session: aiohttp session

        Returns:
            List of discovered APIs
        """
        # Product Hunt API requires OAuth, which is complex to set up
        # For now, this is a placeholder for future implementation
        self.logger.debug("Product Hunt search not yet implemented")
        return []

    async def _search_hacker_news(self, session: aiohttp.ClientSession) -> List[DiscoveredAPI]:
        """
        Search Hacker News for AI/AGI API announcements.

        Args:
            session: aiohttp session

        Returns:
            List of discovered APIs
        """
        discovered = []

        try:
            # Search Algolia HN API
            search_terms = ['ai api', 'llm api', 'gpt api', 'machine learning api']

            for term in search_terms:
                url = f"https://hn.algolia.com/api/v1/search?query={term}&tags=story&hitsPerPage=20"

                async with session.get(url) as response:
                    if response.status != 200:
                        continue

                    data = await response.json()
                    hits = data.get('hits', [])

                    for hit in hits:
                        title = hit.get('title', '')
                        url_link = hit.get('url', '')
                        points = hit.get('points', 0)

                        if not url_link or not validate_url(url_link):
                            continue

                        # Simple confidence based on points and title keywords
                        confidence = min(0.5 + (points / 500), 0.9)

                        # Check for API-related keywords
                        api_keywords = ['api', 'endpoint', 'service', 'platform']
                        if any(kw in title.lower() for kw in api_keywords):
                            confidence += 0.1

                        threshold = self.config.get('discovery_scout.confidence_threshold', 0.7)
                        if confidence < threshold:
                            continue

                        discovered.append(DiscoveredAPI(
                            url=url_link,
                            name=title,
                            description=f"HN Story: {title}",
                            source=DiscoverySource.HACKER_NEWS.value,
                            confidence_score=min(confidence, 1.0),
                            discovered_at=timestamp_iso(),
                            metadata={
                                'points': points,
                                'hn_id': hit.get('objectID'),
                                'search_term': term
                            }
                        ))

                await asyncio.sleep(1)

        except Exception as e:
            self.logger.error(f"Hacker News search error: {e}")

        self.logger.info(f"Discovered {len(discovered)} APIs from Hacker News")
        return discovered

    def _calculate_confidence(
        self,
        name: str,
        description: str,
        stars: int,
        language: str,
        homepage: str
    ) -> float:
        """
        Calculate confidence score for a discovered API.

        Args:
            name: Repository name
            description: Description
            stars: Star count
            language: Programming language
            homepage: Homepage URL

        Returns:
            Confidence score between 0 and 1
        """
        score = 0.0

        # Keywords that indicate AI/AGI API
        ai_keywords = [
            'ai', 'ml', 'llm', 'gpt', 'chatbot', 'neural', 'deep learning',
            'machine learning', 'artificial intelligence', 'vision', 'speech',
            'nlp', 'embeddings', 'transformers', 'api', 'sdk', 'client'
        ]

        text = f"{name} {description}".lower()

        # Keyword matching (max 0.4)
        keyword_matches = sum(1 for kw in ai_keywords if kw in text)
        score += min(keyword_matches * 0.05, 0.4)

        # Star count (max 0.3)
        if stars > 1000:
            score += 0.3
        elif stars > 500:
            score += 0.2
        elif stars > 100:
            score += 0.1

        # Has homepage (0.1)
        if homepage and validate_url(homepage):
            score += 0.1

        # Popular languages (0.1)
        popular_languages = ['Python', 'JavaScript', 'TypeScript', 'Go', 'Java']
        if language in popular_languages:
            score += 0.1

        # Has "api" in name or description (0.1)
        if 'api' in text:
            score += 0.1

        return min(score, 1.0)

    async def run_iteration(self):
        """Execute one discovery iteration."""
        sources = self.config.get('discovery_scout.sources', [])

        if not sources:
            self.logger.warning("No discovery sources configured")
            return

        all_discovered: List[DiscoveredAPI] = []

        async with aiohttp.ClientSession() as session:
            if 'github_api_search' in sources:
                github_apis = await self._search_github(session)
                all_discovered.extend(github_apis)

            if 'product_hunt' in sources:
                ph_apis = await self._search_product_hunt(session)
                all_discovered.extend(ph_apis)

            if 'hacker_news' in sources:
                hn_apis = await self._search_hacker_news(session)
                all_discovered.extend(hn_apis)

        # Save to database (will ignore duplicates)
        new_discoveries = 0
        for api in all_discovered:
            try:
                await self.db.save_discovered_api(api)
                new_discoveries += 1
            except Exception as e:
                self.logger.debug(f"Failed to save discovered API (likely duplicate): {e}")

        self.logger.info(
            f"Discovery complete: {new_discoveries} new APIs found "
            f"(total candidates: {len(all_discovered)})"
        )

        # Update stats
        await self.db.set_state('last_discovery_scan', timestamp_iso())

    def get_interval(self) -> int:
        """Get scan interval from config."""
        return self.config.get('discovery_scout.scan_interval', 3600)
