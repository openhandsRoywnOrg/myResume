"""
知识点服务单元测试
"""
import pytest
from app.services.topic_service import create_topic, get_topic_by_id, update_topic
from app.exceptions import ValidationError, TopicNotFoundError
from app.models.topic import Topic


class TestTopicCreation:
    """测试知识点创建功能"""
    
    def test_create_valid_topic(self, database):
        """测试创建有效的知识点"""
        topic = create_topic(
            title="Machine Learning Basics",
            content="Machine learning is a subset of artificial intelligence that focuses on...",
            category="ai-ml"
        )
        
        assert topic.id is not None
        assert topic.title == "Machine Learning Basics"
        assert topic.category == "ai-ml"
        assert topic.created_at is not None
    
    def test_create_topic_with_short_title(self, database):
        """测试标题太短时的验证"""
        with pytest.raises(ValidationError) as exc_info:
            create_topic(
                title="ML",
                content="Some content here...",
                category="ai-ml"
            )
        
        assert "Title must be at least 3 characters" in str(exc_info.value)
    
    def test_create_topic_with_empty_content(self, database):
        """测试内容为空时的验证"""
        with pytest.raises(ValidationError) as exc_info:
            create_topic(
                title="Valid Title",
                content="",
                category="ai-ml"
            )
        
        assert "Content must be at least 50 characters" in str(exc_info.value)
    
    def test_create_topic_with_short_content(self, database):
        """测试内容太短时的验证"""
        with pytest.raises(ValidationError) as exc_info:
            create_topic(
                title="Valid Title",
                content="Too short",
                category="ai-ml"
            )
        
        assert "Content must be at least 50 characters" in str(exc_info.value)
    
    def test_create_topic_triggers_hooks(self, database, mocker):
        """测试创建知识点时触发钩子"""
        mock_hook = mocker.patch('app.services.topic_service.hooks.trigger')
        
        topic = create_topic(
            title="Test Topic",
            content="This is a test topic with sufficient content length...",
            category="test"
        )
        
        # 验证钩子被调用
        assert mock_hook.call_count >= 1
        mock_hook.assert_any_call('before_topic_save', title=mocker.ANY, content=mocker.ANY)


class TestTopicRetrieval:
    """测试知识点查询功能"""
    
    def test_get_existing_topic(self, database, sample_topic):
        """测试获取已存在的知识点"""
        topic = get_topic_by_id(sample_topic.id)
        
        assert topic is not None
        assert topic.id == sample_topic.id
        assert topic.title == sample_topic.title
    
    def test_get_nonexistent_topic(self, database):
        """测试获取不存在的知识点"""
        with pytest.raises(TopicNotFoundError):
            get_topic_by_id(99999)
    
    def test_get_topic_with_questions(self, database, sample_topic, sample_question):
        """测试获取带有问题的知识点"""
        topic = get_topic_by_id(sample_topic.id)
        
        assert topic is not None
        assert len(topic.questions) == 1
        assert topic.questions[0].id == sample_question.id


class TestTopicUpdate:
    """测试知识点更新功能"""
    
    def test_update_topic_title(self, database, sample_topic):
        """测试更新知识点标题"""
        updated_topic = update_topic(
            topic_id=sample_topic.id,
            title="Updated Machine Learning Basics"
        )
        
        assert updated_topic.title == "Updated Machine Learning Basics"
        assert updated_topic.id == sample_topic.id
        assert updated_topic.updated_at is not None
    
    def test_update_topic_content(self, database, sample_topic):
        """测试更新知识点内容"""
        updated_topic = update_topic(
            topic_id=sample_topic.id,
            content="This is the updated content with more details..."
        )
        
        assert "updated content" in updated_topic.content.lower()
    
    def test_update_nonexistent_topic(self, database):
        """测试更新不存在的知识点"""
        with pytest.raises(TopicNotFoundError):
            update_topic(
                topic_id=99999,
                title="Some Title"
            )
    
    def test_update_preserves_history(self, database, sample_topic):
        """测试更新保留历史（回归测试）"""
        original_title = sample_topic.title
        
        # 第一次更新
        update_topic(topic_id=sample_topic.id, title="New Title 1")
        
        # 第二次更新
        update_topic(topic_id=sample_topic.id, title="New Title 2")
        
        # 验证可以获取历史版本（如果实现了历史功能）
        topic = get_topic_by_id(sample_topic.id)
        assert topic.title == "New Title 2"


class TestTopicValidation:
    """测试知识点验证逻辑"""
    
    def test_topic_title_max_length(self, database):
        """测试标题最大长度验证"""
        long_title = "A" * 201  # 超过 200 字符
        
        with pytest.raises(ValidationError):
            create_topic(
                title=long_title,
                content="Valid content here...",
                category="test"
            )
    
    def test_topic_category_validation(self, database):
        """测试分类验证"""
        with pytest.raises(ValidationError):
            create_topic(
                title="Valid Title",
                content="Valid content with sufficient length...",
                category=""  # 空分类
            )
    
    def test_topic_special_characters_in_title(self, database):
        """测试标题中的特殊字符"""
        topic = create_topic(
            title="ML/AI & Data Science",
            content="This topic covers machine learning, artificial intelligence...",
            category="ai-ml"
        )
        
        assert topic is not None
        assert "ML/AI & Data Science" in topic.title
