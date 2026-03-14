from __future__ import annotations

from playwright.sync_api import Locator, Page, expect


class UiWaits:
    DEFAULT_TIMEOUT_MS = 10_000

    @classmethod
    def visible(cls, locator: Locator, timeout_ms: int | None = None) -> Locator:
        expect(locator).to_be_visible(timeout=timeout_ms or cls.DEFAULT_TIMEOUT_MS)
        return locator

    @classmethod
    def hidden(cls, locator: Locator, timeout_ms: int | None = None) -> Locator:
        expect(locator).to_be_hidden(timeout=timeout_ms or cls.DEFAULT_TIMEOUT_MS)
        return locator

    @classmethod
    def enabled(cls, locator: Locator, timeout_ms: int | None = None) -> Locator:
        expect(locator).to_be_enabled(timeout=timeout_ms or cls.DEFAULT_TIMEOUT_MS)
        return locator

    @classmethod
    def contains_text(cls, locator: Locator, text: str, timeout_ms: int | None = None) -> Locator:
        expect(locator).to_contain_text(text, timeout=timeout_ms or cls.DEFAULT_TIMEOUT_MS)
        return locator

    @classmethod
    def has_count(cls, locator: Locator, count: int, timeout_ms: int | None = None) -> Locator:
        expect(locator).to_have_count(count, timeout=timeout_ms or cls.DEFAULT_TIMEOUT_MS)
        return locator

    @classmethod
    def url_contains(cls, page: Page, value: str, timeout_ms: int | None = None) -> Page:
        page.wait_for_url(
            f"**{value}**",
            timeout=timeout_ms or cls.DEFAULT_TIMEOUT_MS,
            wait_until="domcontentloaded",
        )
        return page
