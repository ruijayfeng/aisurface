from scripts.schema_gen import (
    build_breadcrumb_list,
    build_faq_page,
    build_organization,
    build_software_application,
    build_website,
    validate_schema,
)


def test_build_software_application_minimal():
    schema = build_software_application(
        name="my-tool",
        description="A test tool",
        url="https://example.com",
    )
    assert schema["@context"] == "https://schema.org"
    assert schema["@type"] == "SoftwareApplication"
    assert schema["name"] == "my-tool"
    assert schema["url"] == "https://example.com"


def test_build_software_application_with_optional():
    schema = build_software_application(
        name="my-tool",
        description="d",
        url="https://example.com",
        application_category="DeveloperApplication",
        operating_system="Cross-platform",
        offers={"price": "0", "priceCurrency": "USD"},
    )
    assert schema["applicationCategory"] == "DeveloperApplication"
    assert schema["operatingSystem"] == "Cross-platform"
    assert schema["offers"]["price"] == "0"


def test_build_faq_page():
    schema = build_faq_page(
        questions=[
            {"q": "What is X?", "a": "X is a tool."},
            {"q": "How to use?", "a": "pip install x"},
        ]
    )
    assert schema["@type"] == "FAQPage"
    assert len(schema["mainEntity"]) == 2
    assert schema["mainEntity"][0]["name"] == "What is X?"
    assert "acceptedAnswer" in schema["mainEntity"][0]


def test_build_organization():
    schema = build_organization(
        name="Acme",
        url="https://acme.com",
        logo="https://acme.com/logo.png",
        same_as=["https://github.com/acme"],
    )
    assert schema["@type"] == "Organization"
    assert schema["name"] == "Acme"
    assert schema["sameAs"] == ["https://github.com/acme"]


def test_build_website_minimal():
    schema = build_website(name="my-site", url="https://example.com")
    assert schema["@context"] == "https://schema.org"
    assert schema["@type"] == "WebSite"
    assert schema["name"] == "my-site"
    assert schema["url"] == "https://example.com"
    assert "description" not in schema


def test_build_website_with_description():
    schema = build_website(
        name="my-site",
        url="https://example.com",
        description="A test site",
    )
    assert schema["description"] == "A test site"


def test_build_breadcrumb_list():
    schema = build_breadcrumb_list(
        items=[
            {"name": "Home", "item": "https://example.com"},
            {"name": "Docs", "item": "https://example.com/docs"},
        ]
    )
    assert schema["@type"] == "BreadcrumbList"
    assert len(schema["itemListElement"]) == 2
    assert schema["itemListElement"][0]["position"] == 1
    assert schema["itemListElement"][0]["name"] == "Home"
    assert schema["itemListElement"][0]["@type"] == "ListItem"
    assert schema["itemListElement"][1]["position"] == 2


def test_validate_schema_valid():
    schema = build_software_application(
        name="x", description="d", url="https://x.com"
    )
    assert validate_schema(schema) == []


def test_validate_schema_missing_required():
    errors = validate_schema({"@type": "SoftwareApplication", "name": "x"})
    assert len(errors) > 0


def test_validate_schema_website_missing_url():
    errors = validate_schema({"@type": "WebSite", "name": "x"})
    assert any("url" in e for e in errors)


def test_validate_schema_breadcrumb_list_missing_items():
    errors = validate_schema({"@type": "BreadcrumbList", "name": "x"})
    assert any("itemListElement" in e for e in errors)
