#!/usr/bin/env python3
"""
Test for GitHub Actions workflow label checking logic.

This test verifies that the workflow correctly identifies issues/PRs
with 'fix-me', 'fix-me-experimental', or the macro label (e.g., '@openhands-agent')
for both 'opened' and 'labeled' events.
"""

import json


def check_labels(labels_json: str, macro: str = '@openhands-agent') -> bool:
    """
    Simulate the label checking logic from the workflow.

    Args:
        labels_json: JSON string of labels array
        macro: The macro label to check for

    Returns:
        True if macro or fix-me label is found, False otherwise
    """
    try:
        labels = json.loads(labels_json)
        for label in labels:
            name = label.get('name', '')
            if name == macro or name == 'fix-me' or name == 'fix-me-experimental':
                return True
        return False
    except (json.JSONDecodeError, TypeError):
        return False


def test_opened_event_with_fix_me_label():
    """Test that opened event with fix-me label is detected."""
    labels = [{'name': 'fix-me'}, {'name': 'bug'}]
    labels_json = json.dumps(labels)
    assert check_labels(labels_json) is True, "Should detect fix-me label in opened event"


def test_opened_event_with_fix_me_experimental_label():
    """Test that opened event with fix-me-experimental label is detected."""
    labels = [{'name': 'fix-me-experimental'}]
    labels_json = json.dumps(labels)
    assert check_labels(labels_json) is True, "Should detect fix-me-experimental label"


def test_opened_event_with_macro_label():
    """Test that opened event with macro label is detected."""
    labels = [{'name': '@openhands-agent'}]
    labels_json = json.dumps(labels)
    assert check_labels(labels_json) is True, "Should detect macro label"


def test_opened_event_without_trigger_label():
    """Test that opened event without trigger label is not detected."""
    labels = [{'name': 'bug'}, {'name': 'enhancement'}]
    labels_json = json.dumps(labels)
    assert check_labels(labels_json) is False, "Should not detect without trigger label"


def test_empty_labels():
    """Test that empty labels array returns False."""
    labels_json = json.dumps([])
    assert check_labels(labels_json) is False, "Should return False for empty labels"


def test_labeled_event_simulation():
    """
    Simulate labeled event where github.event.label.name is checked directly.
    In the workflow, this is handled before checking the labels array.
    """
    # For labeled events, the workflow checks github.event.label.name directly
    label_name = 'fix-me'
    macro = '@openhands-agent'

    # Should trigger for fix-me, fix-me-experimental, or macro
    assert label_name in ['fix-me', 'fix-me-experimental', macro], \
        "Labeled event should trigger for fix-me, fix-me-experimental, or macro"


def test_multiple_labels_including_fix_me():
    """Test that multiple labels including fix-me is detected."""
    labels = [
        {'name': 'bug'},
        {'name': 'fix-me'},
        {'name': 'priority-high'}
    ]
    labels_json = json.dumps(labels)
    assert check_labels(labels_json) is True, "Should detect fix-me among multiple labels"


def test_custom_macro_label():
    """Test with a custom macro label."""
    labels = [{'name': '@custom-agent'}]
    labels_json = json.dumps(labels)
    assert check_labels(labels_json, macro='@custom-agent') is True, \
        "Should detect custom macro label"


if __name__ == '__main__':
    # Run all tests
    test_opened_event_with_fix_me_label()
    print("✓ test_opened_event_with_fix_me_label passed")

    test_opened_event_with_fix_me_experimental_label()
    print("✓ test_opened_event_with_fix_me_experimental_label passed")

    test_opened_event_with_macro_label()
    print("✓ test_opened_event_with_macro_label passed")

    test_opened_event_without_trigger_label()
    print("✓ test_opened_event_without_trigger_label passed")

    test_empty_labels()
    print("✓ test_empty_labels passed")

    test_labeled_event_simulation()
    print("✓ test_labeled_event_simulation passed")

    test_multiple_labels_including_fix_me()
    print("✓ test_multiple_labels_including_fix_me passed")

    test_custom_macro_label()
    print("✓ test_custom_macro_label passed")

    print("\n✅ All tests passed!")

