import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.team import add_member, search_member, get_team_member_count, format_greeting

def test_add_member_success():
    members = []
    added, message = add_member(members, "Henrique", "henrique111")
    assert added is True
    assert len(members) == 1
    assert members[0]["name"] == "Henrique"

def test_add_member_duplicate():
    members = [{"name": "Henrique", "github_username": "henrique111"}]
    added, message = add_member(members, "Henrique", "henrique111")
    assert added is False
    assert len(members) == 1


def test_search_member_found():
    members = [
        {"name": "Vitalii", "github_username": "vitalii111"},
        {"name": "Ummay", "github_username": "ummay111"},
    ]
    results = search_member(members, "Vitalii")
    assert len(results) == 1
    assert results[0]["name"] == "Vitalii"


def test_search_member_not_found():
    members = [{"name": "Vitalii", "github_username": "vitalii111"}]
    results = search_member(members, "Daniel")
    assert results == []

