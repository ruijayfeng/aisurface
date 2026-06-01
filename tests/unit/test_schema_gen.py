from scripts.schema_gen import (
    build_faq_page,
    build_organization,
    build_software_application,
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


def test_validate_schema_valid():
    schema = build_software_application(
        name="x", description="d", url="https://x.com"
    )
    assert validate_schema(schema) == []


def test_validate_schema_missing_required():
    errors = validate_schema({"@type": "SoftwareApplication", "name": "x"})
    assert len(errors) > 0
