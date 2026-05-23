from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime, timezone
from urllib.parse import urlparse

ALLOWED_SCHEMES = {"http", "https"}
BLOCKED_SCHEMES = {"javascript", "data"}

MAX_TAGS = 10
MAX_TAG_LENGTH = 30


class CreateLinkRequest(BaseModel):
    long_url: str
    expires_at: Optional[datetime] = None
    tags: Optional[List[str]] = None

    @field_validator("long_url")
    @classmethod
    def validate_long_url(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("URL cannot be empty")

        if any(ord(char) < 32 for char in value):
            raise ValueError("Control characters are not allowed")

        parsed = urlparse(value)

        if parsed.username or parsed.password:
            raise ValueError("Userinfo in URLs is not allowed")

        scheme = parsed.scheme.lower()

        if scheme in BLOCKED_SCHEMES:
            raise ValueError("Dangerous URL scheme blocked")

        if scheme not in ALLOWED_SCHEMES:
            raise ValueError("Only http and https URLs are allowed")

        if not parsed.netloc:
            raise ValueError("Hostname is required")

        return value

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, tags):
        if tags is None:
            return tags

        if len(tags) > MAX_TAGS:
            raise ValueError("Too many tags")

        cleaned_tags = []

        for tag in tags:
            tag = tag.strip()

            if not tag:
                raise ValueError("Empty tags are not allowed")

            if len(tag) > MAX_TAG_LENGTH:
                raise ValueError("Tag is too long")

            cleaned_tags.append(tag)

        return cleaned_tags

    @field_validator("expires_at")
    @classmethod
    def validate_expiration(cls, value):
        if value is None:
            return value

        now = datetime.now(timezone.utc)

        if value <= now:
            raise ValueError("expires_at must be in the future")

        return value