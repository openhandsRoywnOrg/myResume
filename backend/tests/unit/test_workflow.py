
"""
测试 OpenHands Workflow 配置

验证 GitHub Actions workflow 的逻辑正确性
"""
import os


def test_label_consistency():
    """
    测试 check-labels 和 setup-repository 的标签检查是否一致

    修复后：两个步骤都使用 OPENHANDS_MACRO 变量
    """
    # 读取 workflow 文件
    workflow_path = '/workspace/.github/workflows/openhands-resolver.yml'
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow_content = f.read()

    # 检查 check-labels 步骤
    check_labels_section = workflow_content.split('check-labels:')[1].split('setup-repository:')[0]
    assert 'OPENHANDS_MACRO' in check_labels_section or '@openhands-agent' in check_labels_section, \
        "check-labels 应该检查 OPENHANDS_MACRO 或 @openhands-agent"

    # 检查 setup-repository 步骤 - 修复后应该使用 check-labels 的输出
    setup_repo_section = workflow_content.split('setup-repository:')[1].split('call-openhands-resolver:')[0]
    assert 'needs.check-labels.outputs.has-macro-label' in setup_repo_section, \
        "setup-repository 应该使用 check-labels 的输出 (has-macro-label)"

    # 验证不再硬编码 fix-me
    assert 'fix-me' not in setup_repo_section, \
        "setup-repository 不应该硬编码 fix-me 标签，应该使用 OPENHANDS_MACRO"


def test_workflow_dependencies():
    """测试 workflow 依赖关系"""
    workflow_path = '/workspace/.github/workflows/openhands-resolver.yml'
    with open(workflow_path, 'r', encoding='utf-8') as f:
        workflow_content = f.read()

    # call-openhands-resolver 应该依赖 setup-repository
    assert 'needs: [check-permissions, setup-repository]' in workflow_content, \
        "call-openhands-resolver 应该依赖 setup-repository"


def test_workflow_file_exists():
    """测试 workflow 文件存在"""
    workflow_path = '/workspace/.github/workflows/openhands-resolver.yml'
    assert os.path.exists(workflow_path), f"Workflow 文件不存在：{workflow_path}"


def test_workflow_has_required_jobs():
    """测试 workflow 包含必要的 job"""
    workflow_path = '/workspace/.github/workflows/openhands-resolver.yml'
    with open(workflow_path, 'r', encoding='utf-8') as f:
        content = f.read()

    required_jobs = [
        'check-permissions',
        'check-labels',
        'setup-repository',
        'call-openhands-resolver'
    ]

    for job in required_jobs:
        assert f'{job}:' in content, f"Workflow 缺少必要的 job: {job}"


if __name__ == '__main__':
    import sys
    print("Running workflow tests...")

    tests = [
        test_label_consistency,
        test_workflow_dependencies,
        test_workflow_file_exists,
        test_workflow_has_required_jobs,
    ]

    failed = 0
    for test in tests:
        try:
            test()
            print(f"✓ {test.__name__}")
        except AssertionError as e:
            print(f"✗ {test.__name__}: {e}")
            failed += 1

    if failed == 0:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print(f"\n{failed} test(s) failed")
        sys.exit(1)


