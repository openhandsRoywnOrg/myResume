
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/categories')
def api_categories():
    return jsonify(get_categories())

@app.route('/topic/<category>/<topic>')
def topic(category, topic):
    content = read_markdown_file(category, topic)
    if content:
        return render_template('topic.html', content=content, topic=topic.replace('-', ' ').title(), category=category.replace('-', ' ').title())
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

if __name__ == '__main__':
    from flask import request
    app.run(host='0.0.0.0', port=51880, debug=False, threaded=True)
