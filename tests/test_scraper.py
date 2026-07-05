"""
Tests for InstagramPostsDiscovery.

Covers initialization, input handling, query parameters, payload construction,
filtering options, error handling, and timeout behavior.

Run:
    python -m pytest tests/ -v
"""

import pytest
from unittest.mock import patch, MagicMock

from instagram_posts_discovery import (
    InstagramPostsDiscovery,
    InstagramPostsDiscoveryError,
    AuthenticationError,
    InputValidationError,
    DATASET_ID,
)

FAKE_TOKEN = "test_api_token_abc123"
PROFILE_URL = "https://www.instagram.com/meta/"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def scraper():
    """Return a scraper instance with a fake token."""
    return InstagramPostsDiscovery(api_token=FAKE_TOKEN)


@pytest.fixture
def mock_post():
    """Return a mock successful API response."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"url": PROFILE_URL, "likes": 42}]
    mock_resp.raise_for_status.return_value = None
    return mock_resp


# ---------------------------------------------------------------------------
# 1. Initialization
# ---------------------------------------------------------------------------

class TestInit:
    def test_init_with_token(self):
        s = InstagramPostsDiscovery(api_token=FAKE_TOKEN)
        assert s.api_token == FAKE_TOKEN

    def test_init_from_env(self):
        with patch.dict("os.environ", {"BRIGHT_DATA_API_TOKEN": "env_token"}):
            s = InstagramPostsDiscovery()
            assert s.api_token == "env_token"

    def test_init_missing_token_raises(self):
        with patch.dict("os.environ", {}, clear=True):
            with pytest.raises(AuthenticationError, match="API token required"):
                InstagramPostsDiscovery()


# ---------------------------------------------------------------------------
# 2. Single URL string input
# ---------------------------------------------------------------------------

class TestSingleURL:
    def test_single_url_payload(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            call_kwargs = m.call_args
            payload = call_kwargs.kwargs["json"]
            assert payload == {"input": [{"url": PROFILE_URL}]}

    def test_single_url_with_num_of_posts(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, num_of_posts=5)
            payload = m.call_args.kwargs["json"]
            assert payload["input"][0]["num_of_posts"] == 5

    def test_single_url_strips_whitespace(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile("  " + PROFILE_URL + "  ")
            payload = m.call_args.kwargs["json"]
            assert payload["input"][0]["url"] == PROFILE_URL


# ---------------------------------------------------------------------------
# 3. Batch dict input
# ---------------------------------------------------------------------------

class TestBatchDicts:
    def test_list_of_dicts(self, scraper, mock_post):
        profiles = [
            {"url": "https://www.instagram.com/meta/", "num_of_posts": 3},
            {"url": "https://www.instagram.com/google/"},
        ]
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(profiles)
            payload = m.call_args.kwargs["json"]
            assert len(payload["input"]) == 2
            assert payload["input"][0]["num_of_posts"] == 3
            assert "num_of_posts" not in payload["input"][1]

    def test_single_dict_input(self, scraper, mock_post):
        profile = {"url": PROFILE_URL, "num_of_posts": 7}
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(profile)
            payload = m.call_args.kwargs["json"]
            assert len(payload["input"]) == 1
            assert payload["input"][0]["num_of_posts"] == 7

    def test_empty_list_raises(self, scraper):
        with pytest.raises(InputValidationError, match="cannot be empty"):
            scraper.discover_by_profile([])

    def test_dict_missing_url_raises(self, scraper):
        with pytest.raises(InputValidationError, match="must contain a 'url' key"):
            scraper.discover_by_profile({"num_of_posts": 5})


# ---------------------------------------------------------------------------
# 4. Correct query parameters
# ---------------------------------------------------------------------------

class TestQueryParams:
    def test_default_query_params(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            params = m.call_args.kwargs["params"]
            assert params["dataset_id"] == DATASET_ID
            assert params["type"] == "discover_new"
            assert params["discover_by"] == "url"
            assert params["include_errors"] == "true"

    def test_limit_per_input_not_sent_by_default(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            params = m.call_args.kwargs["params"]
            assert "limit_per_input" not in params

    def test_limit_per_input_sent_when_set(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, limit_per_input=25)
            params = m.call_args.kwargs["params"]
            assert params["limit_per_input"] == 25


# ---------------------------------------------------------------------------
# 5. Date filters in payload
# ---------------------------------------------------------------------------

class TestDateFilters:
    def test_start_date_in_payload(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, start_date="01-01-2025")
            record = m.call_args.kwargs["json"]["input"][0]
            assert record["start_date"] == "01-01-2025"

    def test_end_date_in_payload(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, end_date="03-01-2025")
            record = m.call_args.kwargs["json"]["input"][0]
            assert record["end_date"] == "03-01-2025"

    def test_both_dates_in_payload(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(
                PROFILE_URL, start_date="01-01-2025", end_date="03-01-2025"
            )
            record = m.call_args.kwargs["json"]["input"][0]
            assert record["start_date"] == "01-01-2025"
            assert record["end_date"] == "03-01-2025"

    def test_none_dates_excluded(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            record = m.call_args.kwargs["json"]["input"][0]
            assert "start_date" not in record
            assert "end_date" not in record


# ---------------------------------------------------------------------------
# 6. Post type filter
# ---------------------------------------------------------------------------

class TestPostType:
    def test_post_type_post(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, post_type="Post")
            record = m.call_args.kwargs["json"]["input"][0]
            assert record["post_type"] == "Post"

    def test_post_type_reel(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, post_type="Reel")
            record = m.call_args.kwargs["json"]["input"][0]
            assert record["post_type"] == "Reel"

    def test_invalid_post_type_raises(self, scraper):
        with pytest.raises(InputValidationError, match="post_type must be one of"):
            scraper.discover_by_profile(PROFILE_URL, post_type="Story")

    def test_none_post_type_excluded(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            record = m.call_args.kwargs["json"]["input"][0]
            assert "post_type" not in record


# ---------------------------------------------------------------------------
# 7. Posts to exclude
# ---------------------------------------------------------------------------

class TestPostsExclusion:
    def test_posts_to_not_include_in_payload(self, scraper, mock_post):
        exclude = ["C1abc123", "C2def456"]
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL, posts_to_not_include=exclude)
            record = m.call_args.kwargs["json"]["input"][0]
            assert record["posts_to_not_include"] == exclude

    def test_none_exclusion_excluded_from_payload(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            record = m.call_args.kwargs["json"]["input"][0]
            assert "posts_to_not_include" not in record


# ---------------------------------------------------------------------------
# 8. Timeout
# ---------------------------------------------------------------------------

class TestTimeout:
    def test_request_timeout_is_30(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(PROFILE_URL)
            assert m.call_args.kwargs["timeout"] == 30

    def test_timeout_raises_error(self, scraper):
        import requests as req

        with patch(
            "instagram_posts_discovery.requests.post",
            side_effect=req.exceptions.Timeout("timed out"),
        ):
            with pytest.raises(InstagramPostsDiscoveryError, match="timed out"):
                scraper.discover_by_profile(PROFILE_URL)


# ---------------------------------------------------------------------------
# 9. HTTP errors
# ---------------------------------------------------------------------------

class TestHTTPErrors:
    def test_401_raises_auth_error(self, scraper):
        import requests as req

        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.text = "Unauthorized"
        http_err = req.exceptions.HTTPError(response=mock_resp)
        mock_resp.raise_for_status.side_effect = http_err

        with patch("instagram_posts_discovery.requests.post", return_value=mock_resp):
            with pytest.raises(AuthenticationError, match="Invalid API token"):
                scraper.discover_by_profile(PROFILE_URL)

    def test_500_raises_scraper_error(self, scraper):
        import requests as req

        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.text = "Internal Server Error"
        http_err = req.exceptions.HTTPError(response=mock_resp)
        mock_resp.raise_for_status.side_effect = http_err

        with patch("instagram_posts_discovery.requests.post", return_value=mock_resp):
            with pytest.raises(InstagramPostsDiscoveryError, match="HTTP 500"):
                scraper.discover_by_profile(PROFILE_URL)

    def test_connection_error(self, scraper):
        import requests as req

        with patch(
            "instagram_posts_discovery.requests.post",
            side_effect=req.exceptions.ConnectionError("refused"),
        ):
            with pytest.raises(InstagramPostsDiscoveryError, match="Request failed"):
                scraper.discover_by_profile(PROFILE_URL)


# ---------------------------------------------------------------------------
# 10. Input validation edge cases
# ---------------------------------------------------------------------------

class TestInputValidation:
    def test_empty_string_raises(self, scraper):
        with pytest.raises(InputValidationError, match="cannot be empty"):
            scraper.discover_by_profile("")

    def test_whitespace_only_string_raises(self, scraper):
        with pytest.raises(InputValidationError, match="cannot be empty"):
            scraper.discover_by_profile("   ")

    def test_invalid_type_raises(self, scraper):
        with pytest.raises(InputValidationError, match="must be a string, dict, or list"):
            scraper.discover_by_profile(12345)

    def test_dict_with_empty_url_raises(self, scraper):
        with pytest.raises(InputValidationError, match="cannot be empty"):
            scraper.discover_by_profile({"url": ""})

    def test_invalid_post_type_in_dict_raises(self, scraper):
        with pytest.raises(InputValidationError, match="post_type must be one of"):
            scraper.discover_by_profile({"url": PROFILE_URL, "post_type": "IGTV"})


# ---------------------------------------------------------------------------
# 11. Optional fields only when not None
# ---------------------------------------------------------------------------

class TestOptionalFieldsExclusion:
    def test_all_none_kwargs_produce_url_only(self, scraper, mock_post):
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(
                PROFILE_URL,
                num_of_posts=None,
                start_date=None,
                end_date=None,
                post_type=None,
                posts_to_not_include=None,
            )
            record = m.call_args.kwargs["json"]["input"][0]
            assert list(record.keys()) == ["url"]

    def test_dict_with_none_values_excluded(self, scraper, mock_post):
        profile = {
            "url": PROFILE_URL,
            "num_of_posts": None,
            "start_date": None,
            "post_type": None,
        }
        with patch("instagram_posts_discovery.requests.post", return_value=mock_post) as m:
            scraper.discover_by_profile(profile)
            record = m.call_args.kwargs["json"]["input"][0]
            assert list(record.keys()) == ["url"]
