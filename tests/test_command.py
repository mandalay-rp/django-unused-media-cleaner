import os

import pytest
from django.core.management import call_command


@pytest.mark.django_db
def test_command_dry_run(media_file, capsys):
    call_command("cleanup_unused_media", "--dry-run", verbosity=2)
    out = capsys.readouterr().out
    assert "Dry run" in out
    assert os.path.exists(media_file)  # файл не удалён


@pytest.mark.django_db
def test_command_noinput_deletes_files(media_file):
    call_command("cleanup_unused_media", "--noinput")
    assert not os.path.exists(media_file)


@pytest.mark.django_db
def test_command_exclude(media_file):
    call_command("cleanup_unused_media", "--noinput", exclude=["*.txt"])
    assert os.path.exists(media_file)  # исключён


# @pytest.mark.django_db
# def test_diagnose(media_file, settings, capsys):
#     from django.conf import settings as dj_settings
#     from unused_media_cleaner.cleanup import (
#         get_all_media,
#         get_unused_media,
#         get_used_media,
#     )

#     print("\n=== MEDIA_ROOT =", repr(settings.MEDIA_ROOT))
#     print("=== media_file    =", repr(media_file))
#     print("=== listdir(MR)   =", os.listdir(settings.MEDIA_ROOT))
#     print("=== dj.MEDIA_ROOT =", repr(dj_settings.MEDIA_ROOT))
#     print("=== get_all_media       =", get_all_media())
#     print("=== get_used_media      =", get_used_media())
#     print("=== get_unused_media    =", get_unused_media())

#     call_command("cleanup_unused_media", "--noinput", verbosity=2)
#     print("=== command output =", capsys.readouterr().out)
#     print("=== file exists    =", os.path.exists(media_file))
