import pytest
from django.apps import apps
from unused_media_cleaner.utils import get_file_fields


@pytest.mark.django_db
def test_get_file_fields_returns_file_fields():
    fields = get_file_fields()
    assert len(fields) > 0
    for field in fields:
        assert field.__class__.__name__ in ("FileField", "ImageField")
