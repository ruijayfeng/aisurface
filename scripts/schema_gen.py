"""Generate and validate Schema.org JSON-LD for OSS projects."""
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
