
# LangChain/LangGraph 基础概念

## 1. 什么是 LangChain？

LangChain 是一个用于构建 LLM 应用的开发框架，提供了抽象层和工具来简化与大语言模型交互的过程。

### 核心特点：
- **模块化设计**：组件解耦，易于组合
- **丰富组件**：LLM、Prompt、Memory、Agent、Tool 等
- **生态丰富**：集成多种模型和外部服务

### 核心组件：
1. **LLM Wrappers**：统一接口调用各种大模型
2. **Prompt Templates**：动态构建提示词
3. **Chains**：串联多个组件形成工作流
4. **Agents**：动态决策调用工具
5. **Memory**：保存对话上下文

## 2. LangChain vs LangGraph

| 特性 | LangChain | LangGraph |
|------|-----------|-----------|
| 架构 | 线性链式 | 图结构 |
| 流程控制 | 顺序执行 | 条件分支/循环 |
| 状态管理 | 简单 | 支持复杂状态 |
| 适用场景 | 简单 Pipeline | 多代理/复杂工作流 |

### LangGraph 优势：
- 支持有向无环图（DAG）和循环
- 内置状态管理
- 更好的可视化和调试
- 支持多 Agent 协作

## 3. LangChain 核心组件

### 3.1 LLM 接口

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.7,
    api_key="your-api-key"
)

response = llm.invoke("什么是 LangChain?")
print(response.content)
```

### 3.2 Prompt Templates

```python
from langchain.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template(
    "你是一位{role}专家，请用{style}风格解释{topic}"
)

formatted_prompt = prompt.format(
    role="Python",
    style="简洁",
    topic="装饰器"
)
```

### 3.3 Chains

```python
from langchain.chains import LLMChain

chain = LLMChain(
    llm=llm,
    prompt=prompt
)

result = chain.run(topic="LangChain")
```

### 3.4 Memory

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True,
    memory_key="chat_history"
)

# 添加对话历史
memory.chat_memory.add_user_message("你好")
memory.chat_memory.add_ai_message("有什么可以帮你？")
```

## 4. LangGraph 核心概念

### 4.1 State 和 Node

```python
from typing import TypedDict
from langgraph.graph import StateGraph

# 定义状态
class AgentState(TypedDict):
    messages: list
    next_action: str
    result: str

# 定义节点
def process_node(state: AgentState) -> AgentState:
    return {
        **state,
        "result": "处理完成"
    }

def decision_node(state: AgentState) -> AgentState:
    return {
        **state,
        "next_action": "end"
    }

# 构建图
graph = StateGraph(AgentState)
graph.add_node("process", process_node)
graph.add_node("decide", decision_node)
graph.set_entry_point("process")
graph.add_edge("process", "decide")
```

### 4.2 条件边和循环

```python
from langgraph.graph import END

# 条件边
def should_continue(state: AgentState) -> str:
    if state.get("next_action") == "continue":
        return "process"
    return END

graph.add_conditional_edges(
    "decide",
    should_continue,
    {
        "process": "process",
        END: END
    }
)
```

## 5. Agent 类型

### 5.1 ReAct Agent

```python
from langchain.agents import create_react_agent

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
```

### 5.2 Tool Calling Agent

```python
from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
```

### 5.3 自定义 Agent

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """执行数学计算"""
    return str(eval(expression))

@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果: {query}"

tools = [calculator, search]

# Agent 决策流程
def agent_node(state: AgentState) -> AgentState:
    last_message = state["messages"][-1]
    # 判断是否需要调用工具
    # ...
    return state
```

## 6. 常见面试题

### Q1: LangChain 的核心组件有哪些？

**答案：**
LangChain 五大核心组件：
1. **LLM**：大语言模型封装
2. **Prompt**：提示词模板管理
3. **Chain**：组件串联的工作流
4. **Agent**：动态决策和工具调用
5. **Memory**：对话状态管理

### Q2: LangGraph 与 LangChain 的区别？

**答案：**
- LangChain 采用线性 Chain 结构，适合简单 Pipeline
- LangGraph 采用图结构，支持条件分支和循环
- LangGraph 适合多 Agent 协作和复杂工作流
- LangGraph 内置状态管理，更适合有状态应用

### Q3: 如何在 LangChain 中实现 RAG？

**答案：**
```python
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings

# 1. 文档加载和分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# 2. 向量化存储
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

# 3. 构建 Retriever
retriever = vectorstore.as_retriever()

# 4. 构建 RAG Chain
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

rag_chain = create_retrieval_chain(
    retriever,
    combine_docs_chain
)
```

### Q4: LangGraph 中如何实现多 Agent 协作？

**答案：**
多 Agent 协作通过图的节点和边实现：

```python
# 定义多个 Agent 节点
def agent_a_node(state):
    # Agent A 处理
    return {"result_a": "..."}

def agent_b_node(state):
    # Agent B 处理
    return {"result_b": "..."}

def coordinator_node(state):
    # 协调者决定下一步
    return {"next": "agent_a" if condition else "agent_b"}

# 构建协作图
graph.add_node("agent_a", agent_a_node)
graph.add_node("agent_b", agent_b_node)
graph.add_node("coordinator", coordinator_node)
```

### Q5: LangChain Memory 的类型有哪些？

**答案：**
1. **BufferMemory**：简单对话历史
2. **ConversationBufferMemory**：保留完整消息
3. **ConversationSummaryMemory**：摘要历史
4. **EntityMemory**：实体信息记忆
5. **Graph Knowledge**：知识图谱记忆

### Q6: 如何优化 LangChain 应用性能？

**答案：**
1. **流式输出**：使用 streaming=True
2. **批量处理**：合并多次调用
3. **缓存结果**：使用缓存避免重复调用
4. **异步调用**：async/await 并行处理
5. **减少 token**：优化 Prompt 长度
6. **选择合适模型**：根据任务选择性价比模型
