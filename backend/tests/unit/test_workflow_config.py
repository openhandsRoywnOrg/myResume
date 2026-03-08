
"""
Test to verify the workflow configuration.
Specifically tests that the 'if' condition has been removed from call-openhands-resolver job.
"""
import os
import sys
import yaml

# Add the parent directory to the path to avoid conftest.py issues
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


def test_call_openhands_resolver_has_no_if_condition():
    """
    Test that the call-openhands-resolver job does not have an 'if' condition.
    This verifies the fix for: 测试移除 if 条件
    """
    # Get the path to the workflow file
    workflow_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        '..',
        '.github',
        'workflows',
        'openhands-resolver.yml'
    )

    # Load the workflow file
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)

    # Get the call-openhands-resolver job
    jobs = workflow.get('jobs', {})
    call_openhands_resolver = jobs.get('call-openhands-resolver', {})

    # Verify that the 'if' condition is not present
    assert 'if' not in call_openhands_resolver, \
        "The 'if' condition should be removed from call-openhands-resolver job"


def test_call_openhands_resolver_has_required_needs():
    """
    Test that the call-openhands-resolver job has the required 'needs' dependencies.
    """
    workflow_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        '..',
        '.github',
        'workflows',
        'openhands-resolver.yml'
    )

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get('jobs', {})
    call_openhands_resolver = jobs.get('call-openhands-resolver', {})

    # Verify that the job has the required needs
    needs = call_openhands_resolver.get('needs', [])
    assert 'check-permissions' in needs, \
        "call-openhands-resolver should need check-permissions"
    assert 'check-labels' in needs, \
        "call-openhands-resolver should need check-labels"
    assert 'setup-repository' in needs, \
        "call-openhands-resolver should need setup-repository"


def test_call_openhands_resolver_uses_correct_workflow():
    """
    Test that the call-openhands-resolver job uses the correct workflow.
    """
    workflow_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        '..',
        '.github',
        'workflows',
        'openhands-resolver.yml'
    )

    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow = yaml.safe_load(f)

    jobs = workflow.get('jobs', {})
    call_openhands_resolver = jobs.get('call-openhands-resolver', {})

    # Verify that the job uses the correct workflow
    uses = call_openhands_resolver.get('uses', '')
    assert 'OpenHands/OpenHands/.github/workflows/openhands-resolver.yml@main' in uses, \
        "call-openhands-resolver should use the correct OpenHands workflow"

