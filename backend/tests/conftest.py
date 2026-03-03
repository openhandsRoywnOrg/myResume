"""
pytest 配置和共享 fixtures
"""
import pytest
from app import create_app, db
from app.models.user import User
from flask import Flask
from flask.testing import FlaskClient


@pytest.fixture(scope='session')
def app():
    """创建测试应用实例"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture(scope='function')
def database(app):
    """为每个测试创建干净的数据"""
    with app.app_context():
        # 开始事务
        db.session.begin_nested()
        yield db
        # 回滚事务，清理数据
        db.session.rollback()


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """创建 Flask 测试客户端"""
    return app.test_client()


@pytest.fixture
def auth_client(client: FlaskClient, database) -> FlaskClient:
    """创建已认证的测试客户端"""
    # 创建测试用户
    user = User(
        username='testuser',
        email='test@example.com',
        role='user'
    )
    user.set_password('password123')
    database.session.add(user)
    database.session.commit()
    
    # 登录获取 token
    response = client.post('/api/v1/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    
    token = response.get_json()['access_token']
    
    # 添加认证头
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client


@pytest.fixture
def admin_client(client: FlaskClient, database) -> FlaskClient:
    """创建管理员认证的测试客户端"""
    # 创建管理员用户
    admin = User(
        username='admin',
        email='admin@example.com',
        role='admin'
    )
    admin.set_password('admin123')
    database.session.add(admin)
    database.session.commit()
    
    # 登录获取 token
    response = client.post('/api/v1/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    token = response.get_json()['access_token']
    
    # 添加认证头
    client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
    return client


@pytest.fixture
def sample_topic(database):
    """创建示例知识点"""
    from app.models.topic import Topic
    
    topic = Topic(
        title='Machine Learning Basics',
        content='Machine learning is a subset of artificial intelligence...',
        category='ai-ml'
    )
    database.session.add(topic)
    database.session.commit()
    return topic


@pytest.fixture
def sample_question(database, sample_topic):
    """创建示例面试题"""
    from app.models.question import Question
    
    question = Question(
        topic_id=sample_topic.id,
        question_text='What is machine learning?',
        answer_hint='ML is a subset of AI...',
        difficulty='easy'
    )
    database.session.add(question)
    database.session.commit()
    return question
