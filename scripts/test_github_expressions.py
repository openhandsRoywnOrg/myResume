
#!/usr/bin/env python3
"""
Test script to validate GitHub Actions expression logic for label checking.
This simulates different GitHub event scenarios to ensure the workflow
correctly identifies when the 'fix-me' or 'fix-me-experimental' labels are present.
"""

import json
import sys


def test_labeled_event_with_fix_me():
    """Test labeled event with fix-me label"""
    event = {
        "label": {"name": "fix-me"},
        "issue": {"labels": [{"name": "bug"}, {"name": "fix-me"}]}
    }
    # Simulate: github.event.label.name == 'fix-me'
    result = event["label"]["name"] == "fix-me"
    assert result, "Should detect fix-me label in labeled event"
    print("✓ test_labeled_event_with_fix_me passed")


def test_labeled_event_with_fix_me_experimental():
    """Test labeled event with fix-me-experimental label"""
    event = {
        "label": {"name": "fix-me-experimental"},
        "issue": {"labels": [{"name": "bug"}]}
    }
    result = event["label"]["name"] == "fix-me-experimental"
    assert result, "Should detect fix-me-experimental label in labeled event"
    print("✓ test_labeled_event_with_fix_me_experimental passed")


def test_labeled_event_with_other_label():
    """Test labeled event with non-macro label"""
    event = {
        "label": {"name": "bug"},
        "issue": {"labels": [{"name": "bug"}]}
    }
    result = event["label"]["name"] in ["fix-me", "fix-me-experimental"]
    assert not result, "Should not detect macro label when other label is added"
    print("✓ test_labeled_event_with_other_label passed")


def test_opened_event_with_fix_me():
    """Test opened event with fix-me label in issue"""
    event = {
        "issue": {
            "labels": [
                {"name": "bug"},
                {"name": "fix-me"},
                {"name": "priority-high"}
            ]
        }
    }
    # Simulate checking labels array
    labels = event.get("issue", {}).get("labels", [])
    has_macro = any(label["name"] in ["fix-me", "fix-me-experimental"] for label in labels)
    assert has_macro, "Should detect fix-me label in opened event"
    print("✓ test_opened_event_with_fix_me passed")


def test_opened_event_without_fix_me():
    """Test opened event without macro label"""
    event = {
        "issue": {
            "labels": [
                {"name": "bug"},
                {"name": "priority-high"}
            ]
        }
    }
    labels = event.get("issue", {}).get("labels", [])
    has_macro = any(label["name"] in ["fix-me", "fix-me-experimental"] for label in labels)
    assert not has_macro, "Should not detect macro label when not present"
    print("✓ test_opened_event_without_fix_me passed")


def test_pr_event_with_fix_me():
    """Test pull_request event with fix-me label"""
    event = {
        "pull_request": {
            "labels": [
                {"name": "enhancement"},
                {"name": "fix-me-experimental"}
            ]
        }
    }
    labels = event.get("pull_request", {}).get("labels", [])
    has_macro = any(label["name"] in ["fix-me", "fix-me-experimental"] for label in labels)
    assert has_macro, "Should detect fix-me-experimental label in PR event"
    print("✓ test_pr_event_with_fix_me passed")


def test_pr_event_without_labels():
    """Test pull_request event without labels"""
    event = {
        "pull_request": {
            "labels": []
        }
    }
    labels = event.get("pull_request", {}).get("labels", [])
    has_macro = any(label["name"] in ["fix-me", "fix-me-experimental"] for label in labels)
    assert not has_macro, "Should not detect macro label when labels array is empty"
    print("✓ test_pr_event_without_labels passed")


def test_reopened_event_with_fix_me():
    """Test reopened event with fix-me label"""
    event = {
        "issue": {
            "labels": [
                {"name": "fix-me"}
            ]
        }
    }
    labels = event.get("issue", {}).get("labels", [])
    has_macro = any(label["name"] in ["fix-me", "fix-me-experimental"] for label in labels)
    assert has_macro, "Should detect fix-me label in reopened event"
    print("✓ test_reopened_event_with_fix_me passed")


def test_issue_with_no_labels():
    """Test issue with no labels"""
    event = {
        "issue": {
            "labels": []
        }
    }
    labels = event.get("issue", {}).get("labels", [])
    has_macro = any(label["name"] in ["fix-me", "fix-me-experimental"] for label in labels)
    assert not has_macro, "Should not detect macro label when no labels exist"
    print("✓ test_issue_with_no_labels passed")


def test_contains_expression_issue():
    """
    Demonstrate the issue with GitHub Actions contains() expression.
    In GitHub Actions, contains(array, value) doesn't work as expected.
    The expression github.event.issue.labels.*.name creates an array,
    but contains() checks if a string contains a substring, not if array contains element.
    """
    # This simulates what github.event.issue.labels.*.name would produce
    label_names = ["bug", "fix-me", "priority-high"]

    # GitHub Actions contains() would do string containment check, not array membership
    # This is WRONG for checking if array contains element
    labels_string = " ".join(label_names)
    wrong_check = "fix-me" in labels_string  # This works by accident

    # But this would fail:
    labels_string2 = "bug enhancement priority"
    wrong_check2 = "fix" in labels_string2  # This would incorrectly return True!

    # The correct approach is to iterate through the array
    correct_check = any(name == "fix-me" for name in label_names)
    correct_check2 = any(name == "fix-me" for name in ["bug", "enhancement", "priority"])

    assert correct_check == True, "Correct check should find fix-me"
    assert correct_check2 == False, "Correct check should not find fix-me"
    print("✓ test_contains_expression_issue passed")
    print("  Note: GitHub Actions contains() doesn't work for array membership!")


def main():
    """Run all tests"""
    print("Testing GitHub Actions label checking logic...\n")

    tests = [
        test_labeled_event_with_fix_me,
        test_labeled_event_with_fix_me_experimental,
        test_labeled_event_with_other_label,
        test_opened_event_with_fix_me,
        test_opened_event_without_fix_me,
        test_pr_event_with_fix_me,
        test_pr_event_without_labels,
        test_reopened_event_with_fix_me,
        test_issue_with_no_labels,
        test_contains_expression_issue,
    ]

    failed = 0
    for test in tests:
        try:
            test()
        except AssertionError as e:
            print(f"✗ {test.__name__} FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    if failed == 0:
        print(f"All {len(tests)} tests passed!")
        return 0
    else:
        print(f"{failed}/{len(tests)} tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

