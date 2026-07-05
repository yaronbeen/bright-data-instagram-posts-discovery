# Bright Data Instagram Posts Discovery

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

Discover Instagram posts from any public profile with advanced filtering. Filter by date range, post type (Post or Reel), post count, and exclude specific posts — all through a single Python class backed by Bright Data's infrastructure.

No headless browsers. No proxies to manage. No CAPTCHAs. Just structured post data at **$0.0015/record** with ~1 second response times.

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

## Prerequisites

- Python 3.8 or higher
- A Bright Data API token — [Get one here](https://get.brightdata.com/1tndi4600b25)

## Installation

```bash
git clone https://github.com/nicobailon/bright-data-instagram-posts-discovery.git
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
    "https://www.instagram.com/meta/",
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
scraper.discover_by_profile("https://www.instagram.com/meta/", num_of_posts=10)

# 2. Single dict
scraper.discover_by_profile({"url": "https://www.instagram.com/meta/", "num_of_posts": 10})

# 3. List of dicts (batch)
scraper.discover_by_profile([
    {"url": "https://www.instagram.com/meta/", "num_of_posts": 5},
    {"url": "https://www.instagram.com/google/", "num_of_posts": 5},
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
    "url": "https://www.instagram.com/p/ABC123/",
    "user_posted": "meta",
    "description": "Introducing our latest AI tools for creators...",
    "hashtags": ["#AI", "#Creators", "#Meta"],
    "num_comments": 1523,
    "date_posted": "2025-02-15T14:30:00.000Z",
    "likes": 48210,
    "photos": ["https://instagram.com/photo1.jpg"],
    "videos": [],
    "location": "Menlo Park, California"
  }
]
```

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

## Why Bright Data?

Bright Data's Instagram datasets handle the hard parts of Instagram data collection so you don't have to:

- **No infrastructure to manage** — Skip the headless browsers, proxy pools, and CAPTCHA solvers
- **Reliable at scale** — Battle-tested infrastructure handles rate limits and blocks automatically
- **Structured data** — Get clean, typed JSON instead of parsing raw HTML
- **Compliance built in** — Data collection follows platform terms and privacy regulations
- **Pay per record** — $0.0015/record with no minimum commitment

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## Running Tests

```bash
pip install pytest
python -m pytest tests/ -v
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*This project uses Bright Data's Instagram datasets. [Sign up for a free trial](https://get.brightdata.com/1tndi4600b25) to get your API token.*
