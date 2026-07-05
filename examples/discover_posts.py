"""
Examples: Discover Instagram posts from profiles using Bright Data.

Demonstrates single profile lookups, batch requests, date filtering,
post type filtering, and post exclusion.

Usage:
    export BRIGHT_DATA_API_TOKEN=your_token
    python examples/discover_posts.py
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from instagram_posts_discovery import InstagramPostsDiscovery


def example_single_profile():
    """Discover recent posts from a single Instagram profile."""
    print("=" * 60)
    print("Example 1: Single profile - latest 10 posts")
    print("=" * 60)

    scraper = InstagramPostsDiscovery()
    results = scraper.discover_by_profile(
        "https://www.instagram.com/meta/",
        num_of_posts=10,
    )
    print(json.dumps(results, indent=2, default=str))


def example_batch_profiles():
    """Discover posts from multiple profiles in a single request."""
    print("\n" + "=" * 60)
    print("Example 2: Batch - multiple profiles")
    print("=" * 60)

    scraper = InstagramPostsDiscovery()
    profiles = [
        {"url": "https://www.instagram.com/meta/", "num_of_posts": 5},
        {"url": "https://www.instagram.com/google/", "num_of_posts": 5},
        {"url": "https://www.instagram.com/openai/", "num_of_posts": 3},
    ]
    results = scraper.discover_by_profile(profiles)
    print(json.dumps(results, indent=2, default=str))


def example_date_filtering():
    """Discover posts within a specific date range."""
    print("\n" + "=" * 60)
    print("Example 3: Date range filter (Jan-Mar 2025)")
    print("=" * 60)

    scraper = InstagramPostsDiscovery()
    results = scraper.discover_by_profile(
        "https://www.instagram.com/meta/",
        num_of_posts=20,
        start_date="01-01-2025",
        end_date="03-01-2025",
    )
    print(json.dumps(results, indent=2, default=str))


def example_post_type_filter():
    """Discover only Reels from a profile."""
    print("\n" + "=" * 60)
    print("Example 4: Filter by post type (Reels only)")
    print("=" * 60)

    scraper = InstagramPostsDiscovery()
    results = scraper.discover_by_profile(
        "https://www.instagram.com/meta/",
        num_of_posts=5,
        post_type="Reel",
    )
    print(json.dumps(results, indent=2, default=str))


def example_exclude_posts():
    """Discover posts while excluding specific post IDs."""
    print("\n" + "=" * 60)
    print("Example 5: Exclude specific posts")
    print("=" * 60)

    scraper = InstagramPostsDiscovery()
    results = scraper.discover_by_profile(
        "https://www.instagram.com/meta/",
        num_of_posts=10,
        posts_to_not_include=["C1abc123", "C2def456"],
    )
    print(json.dumps(results, indent=2, default=str))


def example_combined_filters():
    """Use multiple filters together with batch profiles."""
    print("\n" + "=" * 60)
    print("Example 6: Combined filters in batch mode")
    print("=" * 60)

    scraper = InstagramPostsDiscovery()
    profiles = [
        {
            "url": "https://www.instagram.com/meta/",
            "num_of_posts": 10,
            "start_date": "01-01-2025",
            "end_date": "06-01-2025",
            "post_type": "Post",
        },
        {
            "url": "https://www.instagram.com/google/",
            "num_of_posts": 5,
            "post_type": "Reel",
            "posts_to_not_include": ["CxYz789"],
        },
    ]
    results = scraper.discover_by_profile(profiles, limit_per_input=10)
    print(json.dumps(results, indent=2, default=str))


if __name__ == "__main__":
    print("Bright Data Instagram Posts Discovery - Examples\n")
    print("Set BRIGHT_DATA_API_TOKEN env var before running.\n")

    examples = [
        example_single_profile,
        example_batch_profiles,
        example_date_filtering,
        example_post_type_filter,
        example_exclude_posts,
        example_combined_filters,
    ]

    for fn in examples:
        try:
            fn()
        except Exception as exc:
            print(f"  Error: {exc}")
