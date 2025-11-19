"""
Mixpanel client for tracking events
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# Import Mixpanel only if token is configured
try:
    from mixpanel import Mixpanel
    mp = Mixpanel(settings.MIXPANEL_TOKEN) if settings.MIXPANEL_TOKEN else None
except Exception as e:
    logger.warning(f"Mixpanel initialization failed: {e}")
    mp = None


def track_event(user_id, event_name, properties=None):
    """
    Track an event in Mixpanel

    Args:
        user_id: User ID (distinct_id in Mixpanel)
        event_name: Name of the event
        properties: Dictionary of event properties
    """
    if not mp:
        logger.debug(f"Mixpanel not configured. Would track: {event_name} for user {user_id}")
        return

    try:
        properties = properties or {}
        mp.track(str(user_id), event_name, properties)
        logger.info(f"Tracked event: {event_name} for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to track event {event_name}: {e}")


def set_user_profile(user_id, properties):
    """
    Set user profile properties in Mixpanel

    Args:
        user_id: User ID
        properties: Dictionary of user properties
    """
    if not mp:
        logger.debug(f"Mixpanel not configured. Would set profile for user {user_id}")
        return

    try:
        mp.people_set(str(user_id), properties)
        logger.info(f"Set profile for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to set user profile: {e}")


def increment_user_property(user_id, property_name, value=1):
    """
    Increment a user property in Mixpanel

    Args:
        user_id: User ID
        property_name: Name of the property to increment
        value: Amount to increment by (default: 1)
    """
    if not mp:
        logger.debug(f"Mixpanel not configured. Would increment {property_name} for user {user_id}")
        return

    try:
        mp.people_increment(str(user_id), {property_name: value})
        logger.info(f"Incremented {property_name} for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to increment user property: {e}")
