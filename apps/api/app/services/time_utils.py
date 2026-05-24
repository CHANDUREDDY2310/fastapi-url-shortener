from datetime import timezone


def normalize_expires_at(expires_at):
    if not expires_at:
        return None

    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    return expires_at.astimezone(timezone.utc)