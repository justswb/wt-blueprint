import pytest
from pydantic import ValidationError

from .git_ref import GitRef


def test_pr_zero_rejected():
    with pytest.raises(ValidationError):
        GitRef('feat/a', 0)


def test_pr_negative_rejected():
    with pytest.raises(ValidationError):
        GitRef('feat/a', -1)


def test_pr_one_accepted():
    assert GitRef('feat/a', 1).pr == 1


def test_merge_commit_39_chars_rejected():
    with pytest.raises(ValidationError):
        GitRef('feat/a', None, 'a' * 39)


def test_merge_commit_41_chars_rejected():
    with pytest.raises(ValidationError):
        GitRef('feat/a', None, 'a' * 41)


def test_merge_commit_non_hex_rejected():
    with pytest.raises(ValidationError):
        GitRef('feat/a', None, 'g' * 40)


def test_merge_commit_uppercase_stored_lowercase():
    assert GitRef('feat/a', None, 'ABCDEF' + '0' * 34).merge_commit == 'abcdef' + '0' * 34


def test_empty_branch_rejected():
    with pytest.raises(ValidationError):
        GitRef('')


def test_whitespace_branch_rejected():
    with pytest.raises(ValidationError):
        GitRef('   ')


def test_none_pr_and_merge_commit_accepted():
    ref = GitRef('feat/a', None, None)
    assert ref.pr is None
    assert ref.merge_commit is None
