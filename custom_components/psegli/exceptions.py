"""Exceptions for the PSEG Long Island integration."""

from homeassistant.exceptions import HomeAssistantError


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class CannotConnect(InvalidAuth):
    """Error to indicate MyMeter could not be reached.

    Subclasses InvalidAuth so existing handlers keep treating it as before, while
    callers that care can tell a network failure from an expired session.
    """


class PSEGLIError(HomeAssistantError):
    """Base exception for PSEG Long Island integration.""" 