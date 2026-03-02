
"""
思维导图功能单元测试
"""
import pytest
import sys
import os

# Add the ai-ops-interview directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


@pytest.fixture
def client():
    """创建 Flask 测试客户端"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestMindmapRoute:
    """测试思维导图路由功能"""

    def test_mindmap_page_exists(self, client):
        """测试思维导图页面存在"""
        response = client.get('/mindmap')
        assert response.status_code == 200
        assert '技术学习路线思维导图'.encode('utf-8') in response.data

    def test_mindmap_page_has_correct_title(self, client):
        """测试思维导图页面标题正确"""
        response = client.get('/mindmap')
        assert '<title>技术学习路线思维导图</title>'.encode('utf-8') in response.data

    def test_mindmap_page_has_zoom_controls(self, client):
        """测试思维导图页面有缩放控制按钮"""
        response = client.get('/mindmap')
        assert '放大'.encode('utf-8') in response.data
        assert '缩小'.encode('utf-8') in response.data
        assert '重置'.encode('utf-8') in response.data

    def test_mindmap_page_has_export_buttons(self, client):
        """测试思维导图页面有导出按钮"""
        response = client.get('/mindmap')
        assert '导出图片'.encode('utf-8') in response.data
        assert '导出 PDF'.encode('utf-8') in response.data

    def test_mindmap_page_has_progress_tracking(self, client):
        """测试思维导图页面有进度追踪功能"""
        response = client.get('/mindmap')
        assert '学习进度追踪'.encode('utf-8') in response.data
        assert '总进度'.encode('utf-8') in response.data

    def test_mindmap_page_has_legend(self, client):
        """测试思维导图页面有图例说明"""
        response = client.get('/mindmap')
        assert '图例说明'.encode('utf-8') in response.data
        assert '基础运维开发阶段'.encode('utf-8') in response.data
        assert '开发技能阶段'.encode('utf-8') in response.data
        assert '云原生与 DevOps'.encode('utf-8') in response.data
        assert 'AI/ML 进阶阶段'.encode('utf-8') in response.data

    def test_mindmap_page_has_stage1_topics(self, client):
        """测试思维导图包含阶段 1 主题"""
        response = client.get('/mindmap')
        assert 'Linux/Unix 系统基础'.encode('utf-8') in response.data
        assert '网络基础'.encode('utf-8') in response.data
        assert 'Shell 脚本编程'.encode('utf-8') in response.data
        assert 'Git 版本控制'.encode('utf-8') in response.data
        assert '基础容器技术'.encode('utf-8') in response.data

    def test_mindmap_page_has_stage2_topics(self, client):
        """测试思维导图包含阶段 2 主题"""
        response = client.get('/mindmap')
        assert '编程语言'.encode('utf-8') in response.data
        assert 'Web 开发基础'.encode('utf-8') in response.data
        assert '数据库基础'.encode('utf-8') in response.data
        assert 'API 设计与开发'.encode('utf-8') in response.data
        assert 'CI/CD 流程'.encode('utf-8') in response.data

    def test_mindmap_page_has_stage3_topics(self, client):
        """测试思维导图包含阶段 3 主题"""
        response = client.get('/mindmap')
        assert 'Kubernetes'.encode('utf-8') in response.data
        assert '云服务'.encode('utf-8') in response.data
        assert '监控与日志'.encode('utf-8') in response.data
        assert '基础设施即代码'.encode('utf-8') in response.data

    def test_mindmap_page_has_stage4_topics(self, client):
        """测试思维导图包含阶段 4 主题"""
        response = client.get('/mindmap')
        assert '机器学习基础'.encode('utf-8') in response.data
        assert '深度学习框架'.encode('utf-8') in response.data
        assert 'LLM 应用开发'.encode('utf-8') in response.data
        assert 'AI 工程化实践'.encode('utf-8') in response.data

    def test_mindmap_page_has_modal(self, client):
        """测试思维导图页面有详情弹窗"""
        response = client.get('/mindmap')
        assert b'node-modal' in response.data
        assert '标记为完成'.encode('utf-8') in response.data
        assert '标记为学习中'.encode('utf-8') in response.data
        assert '标记为未开始'.encode('utf-8') in response.data

    def test_mindmap_page_loads_css(self, client):
        """测试思维导图页面加载 CSS 文件"""
        response = client.get('/mindmap')
        assert b'mindmap.css' in response.data

    def test_mindmap_page_has_svg_container(self, client):
        """测试思维导图页面有 SVG 容器"""
        response = client.get('/mindmap')
        assert b'<svg id="mindmap"' in response.data


class TestMindmapIntegration:
    """测试思维导图集成功能"""

    def test_homepage_links_to_mindmap(self, client):
        """测试首页有思维导图链接"""
        response = client.get('/')
        assert b'/mindmap' in response.data
        assert '技术学习路线思维导图'.encode('utf-8') in response.data
        assert '立即查看思维导图'.encode('utf-8') in response.data

    def test_mindmap_page_is_valid_html(self, client):
        """测试思维导图页面是有效的 HTML"""
        response = client.get('/mindmap')
        assert response.content_type == 'text/html; charset=utf-8'
        assert response.data.strip().startswith(b'<!DOCTYPE html>')

