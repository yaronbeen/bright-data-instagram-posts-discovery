# Bright Data Instagram Posts Discovery

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

Discover Instagram posts from any public profile with advanced filtering. Filter by date range, post type (Post or Reel), post count, and exclude specific posts — all through a single Python class backed by Bright Data's infrastructure.

No headless browsers. No proxies to manage. No CAPTCHAs. Just structured post data at **$0.0015/record**.

> **All Instagram scrapers:** [Profile Scraper](https://github.com/yaronbeen/bright-data-instagram-profile-scraper) · [Profile Discovery](https://github.com/yaronbeen/bright-data-instagram-profile-discovery) · [Posts Scraper](https://github.com/yaronbeen/bright-data-instagram-posts-scraper) · **[Posts Discovery](https://github.com/yaronbeen/bright-data-instagram-posts-discovery)** · [Reels Scraper](https://github.com/yaronbeen/bright-data-instagram-reels-scraper) · [Reels Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-discovery) · [Reels (All) Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-all-discovery) · [Comments Scraper](https://github.com/yaronbeen/bright-data-instagram-comments-scraper)

---

## Features

- **Profile-based discovery** — Get posts from any public Instagram profile URL
- **Date range filtering** — Narrow results to a specific time window (MM-DD-YYYY format)
- **Post type filtering** — Retrieve only Posts or only Reels
- **Post exclusion** — Skip specific post IDs you've already processed
- **Batch requests** — Discover posts from multiple profiles in a single API call
- **Result limiting** — Control max records per input with `limit_per_input`
- **40 output fields** — Full post metadata including likes, comments, hashtags, media URLs, location, and more
- **Built-in error handling** — Typed exceptions for auth, validation, and network errors

## Use Cases

- Pull a brand's latest posts to analyze content strategy
- Track competitor posting frequency within a date range
- Build a content calendar from historical post data
- Filter for only Reels or only Posts from a mixed feed
- Exclude already-processed posts to avoid duplicate work

## Prerequisites

- Python 3.8 or higher
- A Bright Data API token

## Installation

```bash
git clone https://github.com/yaronbeen/bright-data-instagram-posts-discovery.git
cd bright-data-instagram-posts-discovery
pip install -r requirements.txt
```

Set up your API token:

```bash
cp .env.example .env
# Edit .env and add your Bright Data API token
```

Or export it directly:

```bash
export BRIGHT_DATA_API_TOKEN=your_token_here
```

## Quick Start

```python
from instagram_posts_discovery import InstagramPostsDiscovery

scraper = InstagramPostsDiscovery()

# Discover the latest 10 posts from a profile
results = scraper.discover_by_profile(
    "https://www.instagram.com/wild.trail.runs/",
    num_of_posts=10,
)
print(results)
```

## API Reference

### `InstagramPostsDiscovery(api_token=None)`

Creates a new discovery client.

| Parameter | Type | Description |
|-----------|------|-------------|
| `api_token` | `str` | Bright Data API token. Falls back to `BRIGHT_DATA_API_TOKEN` env var. |

### `discover_by_profile(url_or_profiles, **kwargs)`

Discover posts from one or more Instagram profiles.

**Input formats:**

```python
# 1. URL string with keyword filters
scraper.discover_by_profile("https://www.instagram.com/wild.trail.runs/", num_of_posts=10)

# 2. Single dict
scraper.discover_by_profile({"url": "https://www.instagram.com/wild.trail.runs/", "num_of_posts": 10})

# 3. List of dicts (batch)
scraper.discover_by_profile([
    {"url": "https://www.instagram.com/wild.trail.runs/", "num_of_posts": 5},
    {"url": "https://www.instagram.com/ceramics_by_jun/", "num_of_posts": 5},
])
```

**Parameters (keyword args for string input, or dict keys for dict input):**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `url` | `str` | Yes | Instagram profile URL |
| `num_of_posts` | `int` | No | Maximum number of posts to discover |
| `start_date` | `str` | No | Start of date range (`MM-DD-YYYY`) |
| `end_date` | `str` | No | End of date range (`MM-DD-YYYY`) |
| `post_type` | `str` | No | `"Post"` or `"Reel"` |
| `posts_to_not_include` | `list[str]` | No | Post ID strings to exclude |
| `limit_per_input` | `int` | No | Max records per input (query param, only sent when set) |

## Example Output

```json
[
  {
    "url": "https://www.instagram.com/p/C7xK9mNs2Qr/",
    "user_posted": "wild.trail.runs",
    "description": "Summit push at 4am. Worth every frozen step.",
    "hashtags": ["#trailrunning", "#ultramarathon", "#mountains"],
    "num_comments": 87,
    "date_posted": "2025-03-11T06:45:00.000Z",
    "likes": 2341,
    "photos": ["https://instagram.com/trail_summit.jpg"],
    "videos": [],
    "location": "Chamonix, France"
  }
]
```

> Note: This is a representative example. Actual field values and available fields may vary.

## Output Fields

The API returns up to 40 fields per post. Key fields include:

| Field | Type | Description |
|-------|------|-------------|
| `url` | `str` | Direct URL to the post |
| `user_posted` | `str` | Username that posted |
| `description` | `str` | Post caption text |
| `hashtags` | `list` | Hashtags used in the post |
| `num_comments` | `int` | Comment count |
| `date_posted` | `str` | ISO 8601 publish timestamp |
| `likes` | `int` | Like count |
| `photos` | `list` | Photo URLs |
| `videos` | `list` | Video URLs |
| `location` | `str` | Tagged location name |

## Rate Limits

- **Sync mode:** Results returned directly in the response. Best for small batches (1-10 inputs).
- **Async mode:** For larger jobs, use the async API. See [Bright Data API docs](https://docs.brightdata.com/datasets/functions/introduction).
- **No hard rate limit** on API calls, but performance varies with batch size.
- **Pricing:** $0.0015 per record ($1.50 per 1,000 records).

## Why Bright Data?

Bright Data's Instagram datasets handle the hard parts of Instagram data collection so you don't have to:

- **Date range filtering** lets you pull exactly the time window you need
- **Post type filter** separates Posts from Reels in mixed feeds
- **Exclusion lists** prevent re-processing posts you already have
- **Batch multiple profiles** in a single API call for efficient pipeline builds
- **Compliance built in** — data collection follows platform terms and privacy regulations

For full API documentation, see the [Bright Data API Reference](https://docs.brightdata.com/datasets/functions/introduction).

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*This repository is a community project and is not officially affiliated with Instagram or Meta. It uses the Bright Data API to access publicly available data. Some links in this README are affiliate links — if you sign up through them, I may earn a commission at no extra cost to you.*
