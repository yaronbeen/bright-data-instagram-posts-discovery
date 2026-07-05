"""
Bright Data Instagram Posts Discovery
Discover Instagram posts from profile URLs with advanced filtering options.

Dataset ID: gd_lk5ns7kz21pck8jpis
Pricing: $0.0015 per record
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE = "https://api.brightdata.com/datasets/v3/scrape"
DATASET_ID = "gd_lk5ns7kz21pck8jpis"
VALID_POST_TYPES = ("Post", "Reel")


class InstagramPostsDiscoveryError(Exception):
    """Base exception for Instagram Posts Discovery errors."""
    pass


class AuthenticationError(InstagramPostsDiscoveryError):
    """Raised when the API token is missing or invalid."""
    pass


class InputValidationError(InstagramPostsDiscoveryError):
    """Raised when input parameters are invalid."""
    pass


class InstagramPostsDiscovery:
    """Discover Instagram posts from profile URLs using Bright Data's dataset API.

    Supports advanced filtering by date range, post type, post count,
    and post exclusion lists.

    Args:
        api_token: Bright Data API token. Falls back to BRIGHT_DATA_API_TOKEN env var.
    """

    def __init__(self, api_token=None):
        self.api_token = api_token or os.getenv("BRIGHT_DATA_API_TOKEN")
        if not self.api_token:
            raise AuthenticationError(
                "API token required. Pass api_token or set BRIGHT_DATA_API_TOKEN env var."
            )

    def _build_input_record(self, profile):
        """Build a single input record from a URL string or dict.

        Args:
            profile: Instagram profile URL string or dict with 'url' and optional filters.

        Returns:
            dict: Validated input record for the API payload.

        Raises:
            InputValidationError: If the input is malformed or missing required fields.
        """
        if isinstance(profile, str):
            if not profile.strip():
                raise InputValidationError("Profile URL cannot be empty.")
            return {"url": profile.strip()}

        if isinstance(profile, dict):
            if "url" not in profile:
                raise InputValidationError("Each profile dict must contain a 'url' key.")
            if not profile["url"] or not profile["url"].strip():
                raise InputValidationError("Profile URL cannot be empty.")

            record = {"url": profile["url"].strip()}

            if "num_of_posts" in profile and profile["num_of_posts"] is not None:
                record["num_of_posts"] = int(profile["num_of_posts"])

            if "start_date" in profile and profile["start_date"] is not None:
                record["start_date"] = profile["start_date"]

            if "end_date" in profile and profile["end_date"] is not None:
                record["end_date"] = profile["end_date"]

            if "post_type" in profile and profile["post_type"] is not None:
                if profile["post_type"] not in VALID_POST_TYPES:
                    raise InputValidationError(
                        f"post_type must be one of {VALID_POST_TYPES}, "
                        f"got '{profile['post_type']}'."
                    )
                record["post_type"] = profile["post_type"]

            if "posts_to_not_include" in profile and profile["posts_to_not_include"] is not None:
                record["posts_to_not_include"] = profile["posts_to_not_include"]

            return record

        raise InputValidationError(
            f"Profile must be a URL string or dict, got {type(profile).__name__}."
        )

    def _make_request(self, params, payload):
        """Send a POST request to the Bright Data scrape API.

        Args:
            params: Query parameters dict.
            payload: JSON body payload (list of input records).

        Returns:
            list | dict: Parsed JSON response from the API.

        Raises:
            InstagramPostsDiscoveryError: On HTTP or network errors.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                API_BASE,
                headers=headers,
                params=params,
                json=payload,
                timeout=30,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else None
            if status == 401:
                raise AuthenticationError("Invalid API token.") from exc
            raise InstagramPostsDiscoveryError(
                f"HTTP {status} error: {exc.response.text if exc.response is not None else exc}"
            ) from exc
        except requests.exceptions.Timeout as exc:
            raise InstagramPostsDiscoveryError("Request timed out after 30s.") from exc
        except requests.exceptions.RequestException as exc:
            raise InstagramPostsDiscoveryError(f"Request failed: {exc}") from exc

    def discover_by_profile(
        self,
        url_or_profiles,
        num_of_posts=None,
        start_date=None,
        end_date=None,
        post_type=None,
        posts_to_not_include=None,
        limit_per_input=None,
    ):
        """Discover Instagram posts from one or more profile URLs.

        Accepts three input styles:
          1. A URL string with optional keyword filters.
          2. A single dict with 'url' and optional filter keys.
          3. A list of dicts, each with 'url' and optional filter keys.

        When url_or_profiles is a string, the keyword arguments (num_of_posts,
        start_date, end_date, post_type, posts_to_not_include) are applied to
        that single profile. When dicts are passed, filters inside each dict
        take precedence and keyword arguments are ignored.

        Args:
            url_or_profiles: Profile URL string, single input dict, or list of input dicts.
            num_of_posts: Max number of posts to return (string input only).
            start_date: Start date filter in MM-DD-YYYY format (string input only).
            end_date: End date filter in MM-DD-YYYY format (string input only).
            post_type: Filter by "Post" or "Reel" (string input only).
            posts_to_not_include: List of post ID strings to exclude (string input only).
            limit_per_input: Max records per input. Only sent when explicitly set.

        Returns:
            list | dict: Discovered posts data from the API.

        Raises:
            InputValidationError: If inputs are invalid.
            AuthenticationError: If the API token is rejected.
            InstagramPostsDiscoveryError: On network / API errors.
        """
        # Build input records
        if isinstance(url_or_profiles, str):
            record = {"url": url_or_profiles.strip()}
            if not record["url"]:
                raise InputValidationError("Profile URL cannot be empty.")

            if num_of_posts is not None:
                record["num_of_posts"] = int(num_of_posts)
            if start_date is not None:
                record["start_date"] = start_date
            if end_date is not None:
                record["end_date"] = end_date
            if post_type is not None:
                if post_type not in VALID_POST_TYPES:
                    raise InputValidationError(
                        f"post_type must be one of {VALID_POST_TYPES}, got '{post_type}'."
                    )
                record["post_type"] = post_type
            if posts_to_not_include is not None:
                record["posts_to_not_include"] = posts_to_not_include

            input_records = [record]

        elif isinstance(url_or_profiles, dict):
            input_records = [self._build_input_record(url_or_profiles)]

        elif isinstance(url_or_profiles, list):
            if not url_or_profiles:
                raise InputValidationError("Profile list cannot be empty.")
            input_records = [self._build_input_record(p) for p in url_or_profiles]

        else:
            raise InputValidationError(
                f"url_or_profiles must be a string, dict, or list, "
                f"got {type(url_or_profiles).__name__}."
            )

        # Query parameters
        params = {
            "dataset_id": DATASET_ID,
            "type": "discover_new",
            "discover_by": "url",
            "include_errors": "true",
        }

        if limit_per_input is not None:
            params["limit_per_input"] = int(limit_per_input)

        payload = {"input": input_records}

        return self._make_request(params, payload)
