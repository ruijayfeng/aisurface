"""
 * [INPUT]: Depends on `typing.Any` (stdlib).
 * [OUTPUT]: Provides `build_software_application(name, description, url, *, application_category, operating_system, offers, author) -> dict[str, Any]`; `build_faq_page(questions) -> dict[str, Any]`.
 * [POS]: Schema.org JSON-LD builder. Used by the audit verb's check #5 (to test if a schema file exists) and by `fix/schema_org.py` to produce `index.schema.json`.
 * [PROTOCOL]: Update this header when changed, then check CLAUDE.md

Generate and validate Schema.org JSON-LD for OSS projects.
"""
from __future__ import annotations

from typing import Any


def build_software_application(
    name: str,
    description: str,
    url: str,
    *,
    application_category: str | None = None,
    operating_system: str | None = None,
    offers: dict | None = None,
    author: dict | None = None,
) -> dict[str, Any]:
    """Build a SoftwareApplication schema.org object."""
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": name,
        "description": description,
        "url": url,
    }
    if application_category:
        schema["applicationCategory"] = application_category
    if operating_system:
        schema["operatingSystem"] = operating_system
    if offers:
        schema["offers"] = offers
    if author:
        schema["author"] = author
    return schema


def build_faq_page(questions: list[dict[str, str]]) -> dict[str, Any]:
    """Build a FAQPage schema from [{q, a}] pairs."""
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"],
                },
            }
            for item in questions
        ],
    }


def build_organization(
    name: str,
    url: str,
    *,
    logo: str | None = None,
    same_as: list[str] | None = None,
) -> dict[str, Any]:
    """Build an Organization schema."""
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": name,
        "url": url,
    }
    if logo:
        schema["logo"] = logo
    if same_as:
        schema["sameAs"] = same_as
    return schema


def build_website(name: str, url: str, description: str | None = None) -> dict[str, Any]:
    """Build a WebSite schema.org entity."""
    schema: dict[str, Any] = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": name,
        "url": url,
    }
    if description:
        schema["description"] = description
    return schema


def build_breadcrumb_list(items: list[dict[str, str]]) -> dict[str, Any]:
    """Build a BreadcrumbList schema. Each item: {name, item}."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": idx + 1,
                "name": item["name"],
                "item": item["item"],
            }
            for idx, item in enumerate(items)
        ],
    }


# Minimal required-field checks for v0.1's 5 types
REQUIRED_FIELDS = {
    "SoftwareApplication": ["name", "description", "url"],
    "FAQPage": ["mainEntity"],
    "Organization": ["name", "url"],
    "WebSite": ["name", "url"],
    "BreadcrumbList": ["itemListElement"],
}


def validate_schema(schema: dict[str, Any]) -> list[str]:
    """Return list of validation errors. Empty = valid."""
    errors: list[str] = []
    schema_type = schema.get("@type")
    if not schema_type:
        return ["Missing @type"]
    if "@context" not in schema:
        errors.append("Missing @context")
    required = REQUIRED_FIELDS.get(schema_type, [])
    for field in required:
        if field not in schema:
            errors.append(f"Missing required field '{field}' for {schema_type}")
    return errors
