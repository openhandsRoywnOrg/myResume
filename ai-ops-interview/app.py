
from flask import Flask, render_template, send_from_directory, jsonify, request
import markdown
import os
import json

app = Flask(__name__)

CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')

def get_categories():
    """Get all categories and their topics"""
    categories = []
    for category in sorted(os.listdir(CONTENT_DIR)):
        category_path = os.path.join(CONTENT_DIR, category)
        if os.path.isdir(category_path):
            topics = []
            for file in sorted(os.listdir(category_path)):
                if file.endswith('.md'):
                    topic_name = file[:-3].replace('-', ' ').title()
                    topics.append({
                        'id': file[:-3],
                        'name': topic_name,
                        'category': category.replace('-', ' ').title()
                    })
            if topics:
                categories.append({
                    'id': category,
                    'name': category.replace('-', ' ').title(),
                    'topics': topics
                })
    return categories

def read_markdown_file(category, topic):
    """Read and convert markdown file to HTML"""
    file_path = os.path.join(CONTENT_DIR, category, f'{topic}.md')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            html = markdown.markdown(content, extensions=['extra', 'codehilite', 'toc'])
            return html
    return None

def extract_mindmap_data(category, topic):
    """Extract mindmap structure from markdown file"""
    file_path = os.path.join(CONTENT_DIR, category, f'{topic}.md')
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

            root = {
                'id': f'{category}/{topic}',
                'text': topic.replace('-', ' ').title(),
                'children': [],
                'link': f'/topic/{category}/{topic}'
            }

            stack = [(root, -1)]  # (node, level)

            for line in lines:
                if line.startswith('#'):
                    level = len(line.split()[0])
                    text = line.lstrip('#').strip()

                    if text:
                        node = {
                            'id': f'{category}/{topic}/{text}',
                            'text': text,
                            'children': [],
                            'link': f'/topic/{category}/{topic}'
                        }

                        # Find parent node
                        while stack and stack[-1][1] >= level:
                            stack.pop()

                        if stack:
                            stack[-1][0]['children'].append(node)
                            stack.append((node, level))

            return root
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/categories')
def api_categories():
    return jsonify(get_categories())

@app.route('/topic/<category>/<topic>')
def topic(category, topic):
    content = read_markdown_file(category, topic)
    mindmap_data = extract_mindmap_data(category, topic)
    if content:
        return render_template('topic.html', content=content, topic=topic.replace('-', ' ').title(), category=category.replace('-', ' ').title(), mindmap_data=mindmap_data)
    return 'Topic not found', 404

@app.route('/api/mindmap/<category>/<topic>')
def api_mindmap(category, topic):
    """API endpoint to get mindmap data"""
    mindmap_data = extract_mindmap_data(category, topic)
    if mindmap_data:
        return jsonify(mindmap_data)
    return 'Topic not found', 404

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/mindmap')
def mindmap():
    return render_template('mindmap.html')

@app.route('/api/search')
def api_search():
    query = request.args.get('q', '').lower()
    results = []
    for category in get_categories():
        for topic in category['topics']:
            file_path = os.path.join(CONTENT_DIR, category['id'], f"{topic['id']}.md")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().lower()
                    if query in content or query in topic['name'].lower():
                        results.append({
                            'category': category['name'],
                            'topic': topic['name'],
                            'id': topic['id'],
                            'category_id': category['id']
                        })
    return jsonify(results)

# ========== AI 应用开发相关路由 ==========

@app.route('/ai-apps/langchain')
def ai_apps_langchain():
    """LangChain 页面"""
    return render_template('langchain.html')

@app.route('/ai-apps/langgraph')
def ai_apps_langgraph():
    """LangGraph 页面"""
    return render_template('content_page.html', 
                         title='🕸️ LangGraph',
                         subtitle='构建状态化 Agent 工作流',
                         content='<p>LangGraph 相关内容正在建设中...</p>')

@app.route('/ai-apps/mcp')
def ai_apps_mcp():
    """MCP 页面"""
    return render_template('content_page.html',
                         title='🔌 MCP (Model Context Protocol)',
                         subtitle='模型上下文协议',
                         content='<p>MCP 相关内容正在建设中...</p>')

@app.route('/ai-apps/agent-collaboration')
def ai_apps_agent_collaboration():
    """多 Agent 协同页面"""
    return render_template('content_page.html',
                         title='👥 多 Agent 协同',
                         subtitle='Agent 间协作与通信',
                         content='<p>多 Agent 协同相关内容正在建设中...</p>')

@app.route('/ai-apps/agent-orchestration')
def ai_apps_agent_orchestration():
    """Agent 编排页面"""
    return render_template('content_page.html',
                         title='🎼 Agent 编排',
                         subtitle='复杂任务调度与管理',
                         content='<p>Agent 编排相关内容正在建设中...</p>')

@app.route('/ai-apps/agent-evaluation')
def ai_apps_agent_evaluation():
    """Agent 评估页面"""
    return render_template('content_page.html',
                         title='📊 Agent 评估',
                         subtitle='性能与效果评估',
                         content='<p>Agent 评估相关内容正在建设中...</p>')

# ========== AI 软件工程相关路由 ==========

@app.route('/ai-se/doc-driven')
def ai_se_doc_driven():
    """文档驱动开发页面"""
    return render_template('doc_driven.html')

@app.route('/ai-se/test-driven')
def ai_se_test_driven():
    """测试驱动开发页面"""
    return render_template('content_page.html',
                         title='✅ 测试驱动开发 (TDD)',
                         subtitle='Test-Driven Development',
                         content='<p>测试驱动开发相关内容正在建设中...</p>')

@app.route('/ai-se/requirement-driven')
def ai_se_requirement_driven():
    """需求驱动开发页面"""
    return render_template('content_page.html',
                         title='🎯 需求驱动开发',
                         subtitle='Requirement-Driven Development',
                         content='<p>需求驱动开发相关内容正在建设中...</p>')

@app.route('/ai-se/ai-workflow')
def ai_se_ai_workflow():
    """AI 工程流程页面"""
    return render_template('content_page.html',
                         title='⚙️ AI 工程流程',
                         subtitle='完整开发工作流',
                         content='<p>AI 工程流程相关内容正在建设中...</p>')

@app.route('/ai-se/code-review')
def ai_se_code_review():
    """AI 代码审查页面"""
    return render_template('content_page.html',
                         title='🔍 AI 代码审查',
                         subtitle='自动化 Code Review',
                         content='<p>AI 代码审查相关内容正在建设中...</p>')

@app.route('/ai-se/continuous-learning')
def ai_se_continuous_learning():
    """持续学习页面"""
    return render_template('content_page.html',
                         title='📚 持续学习',
                         subtitle='知识更新与迭代',
                         content='<p>持续学习相关内容正在建设中...</p>')

if __name__ == '__main__':
    from flask import request
    app.run(host='0.0.0.0', port=51880, debug=False, threaded=True)
