
#!/usr/bin/env python3
"""
Test script to validate the GitHub Actions workflow label checking logic.
This simulates the shell script logic that will run in GitHub Actions.
"""

import json
import subprocess
import sys
import tempfile
import os


def simulate_check_labels_script(event_name, event_data):
    """
    Simulate the shell script logic from the GitHub Actions workflow.
    Returns True if has-macro-label would be set to true, False otherwise.
    """
    # Create a temporary script file
    script_content = f"""#!/bin/bash
set -e

# Mock GitHub environment variables
export GITHUB_EVENT_NAME="{event_name}"
export GITHUB_OUTPUT_FILE=$(mktemp)

# Mock event data
EVENT_JSON='{json.dumps(event_data)}'

# Function to write to GITHUB_OUTPUT
write_output() {{
    echo "$1" >> "$GITHUB_OUTPUT_FILE"
}}

echo "Event name: $GITHUB_EVENT_NAME"

# For labeled event, check the added label directly
if [ "$GITHUB_EVENT_NAME" = "labeled" ]; then
    LABEL_NAME=$(echo "$EVENT_JSON" | jq -r '.label.name // ""')
    echo "Labeled event, label name: $LABEL_NAME"
    if [ "$LABEL_NAME" = "fix-me" ] || [ "$LABEL_NAME" = "fix-me-experimental" ]; then
        write_output "has-macro-label=true"
        cat "$GITHUB_OUTPUT_FILE"
        exit 0
    fi
fi

# For opened/reopened events, github.event.issue.labels should be available
if [ "$GITHUB_EVENT_NAME" = "opened" ] || [ "$GITHUB_EVENT_NAME" = "reopened" ]; then
    LABELS_JSON=$(echo "$EVENT_JSON" | jq -c '.issue.labels // []')
    echo "Opened event, labels JSON: $LABELS_JSON"
    if echo "$LABELS_JSON" | jq -e '.[] | select(.name == "fix-me" or .name == "fix-me-experimental")' > /dev/null 2>&1; then
        write_output "has-macro-label=true"
        cat "$GITHUB_OUTPUT_FILE"
        exit 0
    fi
fi

# For PR events
if [ "$GITHUB_EVENT_NAME" = "pull_request" ]; then
    LABELS_JSON=$(echo "$EVENT_JSON" | jq -c '.pull_request.labels // []')
    echo "PR event, labels JSON: $LABELS_JSON"
    if echo "$LABELS_JSON" | jq -e '.[] | select(.name == "fix-me" or .name == "fix-me-experimental")' > /dev/null 2>&1; then
        write_output "has-macro-label=true"
        cat "$GITHUB_OUTPUT_FILE"
        exit 0
    fi
fi

write_output "has-macro-label=false"
cat "$GITHUB_OUTPUT_FILE"
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False) as f:
        f.write(script_content)
        script_path = f.name

    try:
        # Make script executable
        os.chmod(script_path, 0o755)

        # Run the script
        result = subprocess.run(
            ['bash', script_path],
            capture_output=True,
            text=True,
            timeout=10
        )

        output = result.stdout
        has_macro = 'has-macro-label=true' in output

        return has_macro, output
    finally:
        # Clean up
        os.unlink(script_path)


def test_labeled_with_fix_me():
    """Test labeled event with fix-me label"""
    event = {"label": {"name": "fix-me"}}
    has_macro, output = simulate_check_labels_script("labeled", event)
    assert has_macro, f"Should detect fix-me label. Output: {output}"
    print("✓ test_labeled_with_fix_me passed")


def test_labeled_with_fix_me_experimental():
    """Test labeled event with fix-me-experimental label"""
    event = {"label": {"name": "fix-me-experimental"}}
    has_macro, output = simulate_check_labels_script("labeled", event)
    assert has_macro, f"Should detect fix-me-experimental label. Output: {output}"
    print("✓ test_labeled_with_fix_me_experimental passed")


def test_labeled_with_other_label():
    """Test labeled event with non-macro label"""
    event = {"label": {"name": "bug"}}
    has_macro, output = simulate_check_labels_script("labeled", event)
    assert not has_macro, f"Should not detect macro label. Output: {output}"
    print("✓ test_labeled_with_other_label passed")


def test_opened_with_fix_me():
    """Test opened event with fix-me label"""
    event = {
        "issue": {
            "labels": [
                {"name": "bug"},
                {"name": "fix-me"},
                {"name": "priority-high"}
            ]
        }
    }
    has_macro, output = simulate_check_labels_script("opened", event)
    assert has_macro, f"Should detect fix-me label. Output: {output}"
    print("✓ test_opened_with_fix_me passed")


def test_opened_with_fix_me_experimental():
    """Test opened event with fix-me-experimental label"""
    event = {
        "issue": {
            "labels": [
                {"name": "bug"},
                {"name": "fix-me-experimental"}
            ]
        }
    }
    has_macro, output = simulate_check_labels_script("opened", event)
    assert has_macro, f"Should detect fix-me-experimental label. Output: {output}"
    print("✓ test_opened_with_fix_me_experimental passed")


def test_opened_without_macro():
    """Test opened event without macro label"""
    event = {
        "issue": {
            "labels": [
                {"name": "bug"},
                {"name": "priority-high"}
            ]
        }
    }
    has_macro, output = simulate_check_labels_script("opened", event)
    assert not has_macro, f"Should not detect macro label. Output: {output}"
    print("✓ test_opened_without_macro passed")


def test_reopened_with_fix_me():
    """Test reopened event with fix-me label"""
    event = {
        "issue": {
            "labels": [{"name": "fix-me"}]
        }
    }
    has_macro, output = simulate_check_labels_script("reopened", event)
    assert has_macro, f"Should detect fix-me label. Output: {output}"
    print("✓ test_reopened_with_fix_me passed")


def test_pr_with_fix_me():
    """Test pull_request event with fix-me label"""
    event = {
        "pull_request": {
            "labels": [
                {"name": "enhancement"},
                {"name": "fix-me"}
            ]
        }
    }
    has_macro, output = simulate_check_labels_script("pull_request", event)
    assert has_macro, f"Should detect fix-me label. Output: {output}"
    print("✓ test_pr_with_fix_me passed")


def test_pr_with_fix_me_experimental():
    """Test pull_request event with fix-me-experimental label"""
    event = {
        "pull_request": {
            "labels": [
                {"name": "enhancement"},
                {"name": "fix-me-experimental"}
            ]
        }
    }
    has_macro, output = simulate_check_labels_script("pull_request", event)
    assert has_macro, f"Should detect fix-me-experimental label. Output: {output}"
    print("✓ test_pr_with_fix_me_experimental passed")


def test_pr_without_macro():
    """Test pull_request event without macro label"""
    event = {
        "pull_request": {
            "labels": [
                {"name": "enhancement"},
                {"name": "bug"}
            ]
        }
    }
    has_macro, output = simulate_check_labels_script("pull_request", event)
    assert not has_macro, f"Should not detect macro label. Output: {output}"
    print("✓ test_pr_without_macro passed")


def test_empty_labels():
    """Test event with empty labels array"""
    event = {"issue": {"labels": []}}
    has_macro, output = simulate_check_labels_script("opened", event)
    assert not has_macro, f"Should not detect macro label. Output: {output}"
    print("✓ test_empty_labels passed")


def test_no_labels_field():
    """Test event with no labels field"""
    event = {"issue": {}}
    has_macro, output = simulate_check_labels_script("opened", event)
    assert not has_macro, f"Should not detect macro label. Output: {output}"
    print("✓ test_no_labels_field passed")


def main():
    """Run all tests"""
    print("Testing GitHub Actions workflow label checking logic...\n")

    tests = [
        test_labeled_with_fix_me,
        test_labeled_with_fix_me_experimental,
        test_labeled_with_other_label,
        test_opened_with_fix_me,
        test_opened_with_fix_me_experimental,
        test_opened_without_macro,
        test_reopened_with_fix_me,
        test_pr_with_fix_me,
        test_pr_with_fix_me_experimental,
        test_pr_without_macro,
        test_empty_labels,
        test_no_labels_field,
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
        print("\nThe workflow correctly handles:")
        print("  • labeled events (checking github.event.label.name)")
        print("  • opened/reopened events (checking github.event.issue.labels)")
        print("  • pull_request events (checking github.event.pull_request.labels)")
        print("  • Both 'fix-me' and 'fix-me-experimental' labels")
        return 0
    else:
        print(f"{failed}/{len(tests)} tests failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

