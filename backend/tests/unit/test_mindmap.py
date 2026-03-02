
"""
思维导图功能单元测试
"""
import pytest
from flask import url_for


class TestMindmapRoute:
    """测试思维导图路由功能"""

    def test_mindmap_page_exists(self, client):
        """测试思维导图页面存在"""
        response = client.get('/mindmap')
        assert response.status_code == 200
        assert b'技术学习路线思维导图' in response.data

    def test_mindmap_page_has_correct_title(self, client):
        """测试思维导图页面标题正确"""
        response = client.get('/mindmap')
        assert b'<title>技术学习路线思维导图</title>' in response.data

    def test_mindmap_page_has_zoom_controls(self, client):
        """测试思维导图页面有缩放控制按钮"""
        response = client.get('/mindmap')
        assert b'放大' in response.data
        assert b'缩小' in response.data
        assert b'重置' in response.data

    def test_mindmap_page_has_export_buttons(self, client):
        """测试思维导图页面有导出按钮"""
        response = client.get('/mindmap')
        assert b'导出图片' in response.data
        assert b'导出 PDF' in response.data

    def test_mindmap_page_has_progress_tracking(self, client):
        """测试思维导图页面有进度追踪功能"""
        response = client.get('/mindmap')
        assert b'学习进度追踪' in response.data
        assert b'总进度' in response.data

    def test_mindmap_page_has_legend(self, client):
        """测试思维导图页面有图例说明"""
        response = client.get('/mindmap')
        assert b'图例说明' in response.data
        assert b'基础运维开发阶段' in response.data
        assert b'开发技能阶段' in response.data
        assert b'云原生与 DevOps' in response.data
        assert b'AI/ML 进阶阶段' in response.data

    def test_mindmap_page_has_stage1_topics(self, client):
        """测试思维导图包含阶段 1 主题"""
        response = client.get('/mindmap')
        assert b'Linux/Unix 系统基础' in response.data
        assert b'网络基础' in response.data
        assert b'Shell 脚本编程' in response.data
        assert b'Git 版本控制' in response.data
        assert b'基础容器技术' in response.data

    def test_mindmap_page_has_stage2_topics(self, client):
        """测试思维导图包含阶段 2 主题"""
        response = client.get('/mindmap')
        assert b'编程语言' in response.data
        assert b'Web 开发基础' in response.data
        assert b'数据库基础' in response.data
        assert b'API 设计与开发' in response.data
        assert b'CI/CD 流程' in response.data

    def test_mindmap_page_has_stage3_topics(self, client):
        """测试思维导图包含阶段 3 主题"""
        response = client.get('/mindmap')
        assert b'Kubernetes' in response.data
        assert b'云服务' in response.data
        assert b'监控与日志' in response.data
        assert b'基础设施即代码' in response.data

    def test_mindmap_page_has_stage4_topics(self, client):
        """测试思维导图包含阶段 4 主题"""
        response = client.get('/mindmap')
        assert b'机器学习基础' in response.data
        assert b'深度学习框架' in response.data
        assert b'LLM 应用开发' in response.data
        assert b'AI 工程化实践' in response.data

    def test_mindmap_page_has_modal(self, client):
        """测试思维导图页面有详情弹窗"""
        response = client.get('/mindmap')
        assert b'node-modal' in response.data
        assert b'标记为完成' in response.data
        assert b'标记为学习中' in response.data
        assert b'标记为未开始' in response.data

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
        assert b'技术学习路线思维导图' in response.data
        assert b'立即查看思维导图' in response.data

    def test_mindmap_page_is_valid_html(self, client):
        """测试思维导图页面是有效的 HTML"""
        response = client.get('/mindmap')
        assert response.content_type == 'text/html; charset=utf-8'
        assert response.data.startswith(b'<!DOCTYPE html>')

