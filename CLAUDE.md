# AI Assistant Guide for SmolAgents Examples

**Last Updated:** 2025-11-17
**For:** Claude Code, Cursor, Copilot, and other AI coding assistants
**Project:** SmolAgents Multi-Agent Tutorial Repository

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Codebase Structure](#codebase-structure)
3. [Key Conventions](#key-conventions)
4. [Development Workflows](#development-workflows)
5. [Architecture Patterns](#architecture-patterns)
6. [Testing Strategy](#testing-strategy)
7. [Common Tasks](#common-tasks)
8. [What to Avoid](#what-to-avoid)
9. [Troubleshooting](#troubleshooting)
10. [Quick Reference](#quick-reference)

---

## Project Overview

### Purpose
This is an **educational repository** demonstrating multi-agent systems using Hugging Face's SmolAgents library. It provides 8 progressive examples for a YouTube tutorial, ranging from basic agents to complex multi-agent orchestration.

### Goals
- Teach multi-agent system development
- Demonstrate LLM provider integrations
- Show best practices for agent coordination
- Provide reusable patterns and tools

### Target Audience
Developers learning SmolAgents, AI engineers, tutorial followers

### Current State
**Status:** Educational/Demo - Functional but Incomplete
- ✅ All 8 examples working
- ⚠️ Testing infrastructure incomplete (0% coverage)
- ⚠️ requirements.txt missing version numbers
- ❌ CI/CD not implemented

**See UPDATES.md for detailed status report**

---

## Codebase Structure

### Directory Layout

```
smolagents_examples/
│
├── Core Example Scripts (8 files)
│   ├── smolagent_basic.py          # 1. Foundation: Basic CodeAgent
│   ├── smol_toolcalling_agent.py   # 2. Tool integration basics
│   ├── smol_ollama.py              # 3. Local Ollama models
│   ├── smol_claude.py              # 4. Anthropic Claude integration
│   ├── smolagent_gemini.py         # 5. Google Gemini integration
│   ├── smol_gradio.py              # 6. UI creation with Gradio
│   ├── smol_multiagent.py          # 7. Multi-agent coordination
│   └── smol_blogwriter.py          # 8. Complex 4-agent pipeline
│
├── smoltools/                      # Custom tool implementations
│   ├── __init__.py                 # Package initializer (empty)
│   ├── jinaai.py                   # Jina AI scraping/search tools
│   ├── visitwebpage.py             # HTTP scraper (currently unused)
│   └── test_visitwebpage.py        # Unit tests (incomplete)
│
├── tests/                          # Integration tests
│   ├── __init__.py                 # Package initializer (empty)
│   └── test_smolagent_basic.py     # Basic agent tests (incomplete)
│
├── Configuration & Documentation
│   ├── requirements.txt            # Python dependencies (no versions!)
│   ├── .env.example                # API key template
│   ├── .gitignore                  # Standard Python gitignore
│   ├── README.md                   # Setup & usage guide
│   ├── UPDATES.md                  # Status report (this sprint)
│   └── CLAUDE.md                   # This file - AI assistant guide
│
└── Generated Files (gitignored)
    ├── .env                        # Local API keys (never commit!)
    ├── venv/                       # Python virtual environment
    └── blog_post.md                # Output from blogwriter example
```

### File Purpose Reference

| File | Lines | Purpose | Dependencies | Status |
|------|-------|---------|--------------|--------|
| smolagent_basic.py | 40 | Introduction to CodeAgent | HF API | ✅ Complete |
| smol_toolcalling_agent.py | 15 | ToolCallingAgent basics | HF API | ✅ Complete |
| smol_ollama.py | 45 | Local model integration | Ollama | ✅ Complete |
| smol_claude.py | 50 | Claude integration | Anthropic API | ✅ Complete |
| smolagent_gemini.py | 45 | Gemini integration | Google API | ✅ Complete |
| smol_gradio.py | 20 | UI creation | HF API | ✅ Complete |
| smol_multiagent.py | 60 | Agent coordination | OpenAI API | ✅ Complete |
| smol_blogwriter.py | 107 | Complex pipeline | OpenAI API | ✅ Complete (minor typo) |
| smoltools/jinaai.py | 40 | Web tools | Jina API | ✅ Complete |
| smoltools/visitwebpage.py | 30 | HTTP scraper | None | ⚠️ Unused |
| smoltools/test_visitwebpage.py | 50 | Unit tests | - | ❌ Stub only |
| tests/test_smolagent_basic.py | 30 | Integration tests | - | ❌ Stub only |

---

## Key Conventions

### Code Style

#### 1. Import Organization
**Standard pattern across all files:**

```python
# Standard library imports first
import os
from typing import Optional

# Third-party imports
from smolagents import CodeAgent, ToolCallingAgent, LiteLLMModel
from dotenv import load_dotenv

# Local imports last
from smoltools.jinaai import scrape_page_with_jina_ai
```

#### 2. Environment Variable Loading
**Always at module level, after imports:**

```python
from dotenv import load_dotenv
import os

load_dotenv()  # This loads .env file

# Then access variables
api_key = os.getenv("SOME_API_KEY")
```

#### 3. Agent Initialization Pattern

**For single agents:**
```python
# 1. Define model
model = LiteLLMModel(model_id="gpt-4o-mini")

# 2. Define tools (if needed)
tools = [DuckDuckGoSearchTool(), custom_tool]

# 3. Create agent
agent = ToolCallingAgent(
    tools=tools,
    model=model,
    max_steps=10
)

# 4. Run agent
result = agent.run("Your task here")
```

**For multi-agent systems:**
```python
# 1. Create base agents
research_agent = ToolCallingAgent(tools=[...], model=model)

# 2. Wrap in ManagedAgent
managed_research = ManagedAgent(
    agent=research_agent,
    name="researcher",  # Used in orchestration
    description="What this agent does"  # Manager uses this
)

# 3. Create manager
manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_research, ...]
)

# 4. Run manager (it coordinates sub-agents)
result = manager.run("Complex multi-step task")
```

### 4. Tool Creation Pattern

**Using @tool decorator:**
```python
from smolagents import tool

@tool
def my_custom_tool(query: str) -> str:
    """
    Brief description of what the tool does.

    Args:
        query: What the parameter means

    Returns:
        What the tool returns
    """
    # Implementation
    return result
```

**Key rules:**
- Always use type hints
- Always include docstring
- Keep tools focused (single responsibility)
- Handle errors gracefully
- Return strings (agents work with text)

### 5. Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Example scripts | `smol_<name>.py` | `smol_claude.py` |
| Agent variables | `<purpose>_agent` | `research_agent` |
| Managed agents | `managed_<purpose>_agent` | `managed_research_agent` |
| Tools | `<action>_<object>` | `scrape_page_with_jina_ai` |
| Models | `model` | `model = LiteLLMModel(...)` |
| Test files | `test_<module>.py` | `test_smolagent_basic.py` |

### 6. Documentation Standards

**Every example script should have:**
- File-level docstring explaining purpose
- Inline comments for complex logic
- Example usage (usually at bottom)

**Example:**
```python
"""
SmolAgent Claude Integration Example

Demonstrates:
- Using Anthropic Claude with SmolAgents
- Creating custom tools with @tool decorator
- Both ToolCallingAgent and CodeAgent patterns

Requirements:
- ANTHROPIC_API_KEY in .env
- litellm package installed
"""

# ... code ...

if __name__ == "__main__":
    # Example usage
    result = agent.run("What's the weather like?")
    print(result)
```

---

## Development Workflows

### Adding a New Example Script

**Follow this checklist:**

1. **Choose a name:** `smol_<integration>.py`

2. **Start with template:**
```python
"""
Brief description of what this example demonstrates

Requirements:
- List API keys needed
- List special dependencies
"""

from smolagents import <needed imports>
from dotenv import load_dotenv
import os

load_dotenv()

# Configuration
api_key = os.getenv("YOUR_API_KEY")
if not api_key:
    raise ValueError("YOUR_API_KEY not found in environment")

# Model initialization
model = LiteLLMModel(model_id="model-name")

# Agent setup
agent = ToolCallingAgent(
    tools=[],
    model=model
)

# Example usage
if __name__ == "__main__":
    result = agent.run("Example task")
    print(result)
```

3. **Update README.md:**
   - Add to list of examples
   - Document any new API keys needed
   - Update .env.example if needed

4. **Test manually:**
```bash
python smol_<name>.py
```

5. **Create integration test:**
   - Add `tests/test_smol_<name>.py`
   - Follow existing test patterns
   - Mock API calls

6. **Update documentation:**
   - Add to UPDATES.md (What's Been Done)
   - Update this file if new patterns introduced

### Adding a Custom Tool

**Follow this pattern:**

1. **Decide location:**
   - General utility → `smoltools/<name>.py`
   - Example-specific → inline in script

2. **Implement with @tool:**
```python
# smoltools/my_tool.py

from smolagents import tool
import requests

@tool
def fetch_data(url: str) -> str:
    """
    Fetches data from a URL and returns formatted text.

    Args:
        url: The URL to fetch data from

    Returns:
        Formatted text content from the URL
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching data: {str(e)}"
```

3. **Create unit test:**
```python
# smoltools/test_my_tool.py

import unittest
from unittest.mock import patch, Mock
from smoltools.my_tool import fetch_data

class TestMyTool(unittest.TestCase):
    @patch('smoltools.my_tool.requests.get')
    def test_successful_fetch(self, mock_get):
        mock_response = Mock()
        mock_response.text = "Test content"
        mock_get.return_value = mock_response

        result = fetch_data("http://example.com")
        self.assertEqual(result, "Test content")

    @patch('smoltools.my_tool.requests.get')
    def test_error_handling(self, mock_get):
        mock_get.side_effect = requests.RequestException("Network error")

        result = fetch_data("http://example.com")
        self.assertIn("Error fetching data", result)
```

4. **Use in example:**
```python
from smoltools.my_tool import fetch_data

agent = ToolCallingAgent(
    tools=[fetch_data, ...],
    model=model
)
```

### Implementing Tests

**Current state:** Tests are stubs only (0% coverage)

**When implementing tests:**

1. **Unit tests** (`smoltools/test_*.py`):
   - Test individual tools in isolation
   - Mock all external dependencies
   - Use `unittest.mock`
   - Test success and failure cases

2. **Integration tests** (`tests/test_*.py`):
   - Test agent execution flows
   - Mock LLM API responses
   - Test end-to-end examples
   - May need refactoring of example scripts

**Test execution:**
```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest smoltools/test_visitwebpage.py

# Run with coverage
pip install coverage
coverage run -m unittest discover
coverage report
```

### Setting Up Development Environment

**Standard setup (document for contributors):**

```bash
# 1. Clone repository
git clone <repo-url>
cd smolagents_examples

# 2. Create virtual environment
python -m venv venv

# 3. Activate (macOS/Linux)
source venv/bin/activate
# Or Windows: .\venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure API keys
cp .env.example .env
# Edit .env with your keys

# 6. Test setup
python smolagent_basic.py
```

---

## Architecture Patterns

### Pattern 1: Basic CodeAgent

**Use case:** Simple tasks that may need code execution

**Structure:**
```python
model = HfApiModel(token=os.getenv("HF_TOKEN"))
agent = CodeAgent(tools=[], model=model)
result = agent.run("Calculate the cube of 2")
```

**When to use:**
- Mathematical calculations
- Data processing tasks
- When agent might need to write code

**Examples:** smolagent_basic.py:1-40

### Pattern 2: ToolCallingAgent

**Use case:** Tasks requiring external tools/APIs

**Structure:**
```python
model = LiteLLMModel(model_id="claude-3-5-sonnet-20241022")
agent = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool(), custom_tool],
    model=model
)
result = agent.run("Search for latest news")
```

**When to use:**
- Web searches needed
- API integrations required
- Predefined tools sufficient

**Examples:** smol_toolcalling_agent.py, smol_claude.py, smolagent_gemini.py

### Pattern 3: Local Model Integration

**Use case:** Privacy, cost reduction, offline operation

**Structure:**
```python
model = LiteLLMModel(
    model_id="ollama/llama2",
    api_base="http://localhost:11434"
)
agent = ToolCallingAgent(tools=[custom_tool], model=model)
```

**When to use:**
- Sensitive data (can't use cloud APIs)
- Cost optimization
- Offline requirements

**Examples:** smol_ollama.py:1-45

### Pattern 4: Multi-Agent Coordination

**Use case:** Complex tasks needing specialization

**Structure:**
```python
# Create specialized agents
specialist_agent = ToolCallingAgent(tools=[...], model=model)
managed_specialist = ManagedAgent(
    agent=specialist_agent,
    name="specialist",
    description="What this agent does"
)

# Create manager to coordinate
manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_specialist, ...]
)

result = manager.run("Complex multi-step task")
```

**When to use:**
- Task has distinct phases
- Different tools needed at different stages
- Need for verification/validation steps

**Examples:** smol_multiagent.py, smol_blogwriter.py

### Pattern 5: Agent Pipeline

**Use case:** Sequential processing with validation

**Example from smol_blogwriter.py:**
```
1. Research Agent → Gather information
2. Research Checker → Validate relevance
3. Writer Agent → Create draft
4. Copy Editor → Polish content
5. Manager → Coordinate flow & save output
```

**When to use:**
- Content creation workflows
- Quality assurance needed
- Multi-stage transformations

**Examples:** smol_blogwriter.py:1-107

### Pattern 6: UI Integration

**Use case:** Interactive agent interfaces

**Structure:**
```python
from smolagents import GradioUI

agent = ToolCallingAgent(tools=[...], model=model)
GradioUI(agent).launch()  # Creates web interface
```

**When to use:**
- Demos and presentations
- User-facing applications
- Rapid prototyping

**Examples:** smol_gradio.py:1-20

---

## Testing Strategy

### Current Implementation Status

**Unit Tests:** ❌ Not implemented (stubs only)
- smoltools/test_visitwebpage.py - 0% complete
- Need: Mock HTTP requests, test conversions

**Integration Tests:** ❌ Not implemented (stubs only)
- tests/test_smolagent_basic.py - 0% complete
- Need: Mock LLM APIs, test agent flows

**Overall Coverage:** 0%

### Target Testing Approach

#### Unit Tests (Tools)

**What to test:**
- Individual tool functions
- Input validation
- Error handling
- Output formatting

**How to test:**
```python
import unittest
from unittest.mock import patch, Mock

class TestMyTool(unittest.TestCase):
    @patch('requests.get')  # Mock external calls
    def test_success_case(self, mock_get):
        # Arrange
        mock_get.return_value.text = "expected"

        # Act
        result = my_tool("input")

        # Assert
        self.assertEqual(result, "expected")
```

#### Integration Tests (Agents)

**What to test:**
- Agent initialization
- Task execution
- Error propagation
- Multi-agent coordination

**How to test:**
```python
@patch('smolagents.HfApiModel')
def test_agent_execution(self, mock_model):
    # Mock the LLM response
    mock_instance = Mock()
    mock_instance.generate.return_value = "response"
    mock_model.return_value = mock_instance

    # Test agent
    agent = CodeAgent(tools=[], model=mock_instance)
    result = agent.run("task")

    # Verify
    self.assertIsNotNone(result)
```

### Testing Challenges

**Known Issues:**
1. **Examples not designed for testing:**
   - Most logic at module level (runs on import)
   - Need refactoring into functions

2. **API dependencies:**
   - Need comprehensive mocking
   - Consider VCR.py for recording responses

3. **Non-deterministic outputs:**
   - LLM responses vary
   - Test for patterns, not exact matches

**Recommended Solutions:**
1. Refactor examples to use `if __name__ == "__main__":`
2. Extract core logic into testable functions
3. Use fixtures for common mocks
4. Test behavior, not implementation

---

## Common Tasks

### Task: Add Support for New LLM Provider

**Example: Adding Mistral AI**

1. **Create new example file:**
```python
# smol_mistral.py

from smolagents import ToolCallingAgent, LiteLLMModel
from dotenv import load_dotenv
import os

load_dotenv()

# Validate API key
mistral_key = os.getenv("MISTRAL_API_KEY")
if not mistral_key:
    raise ValueError("MISTRAL_API_KEY not found in environment")

# Initialize model
model = LiteLLMModel(model_id="mistral/mistral-large-latest")

# Create agent
agent = ToolCallingAgent(
    tools=[],
    model=model,
    system_prompt="You are a helpful AI assistant."
)

# Example usage
if __name__ == "__main__":
    result = agent.run("Explain quantum computing briefly")
    print(result)
```

2. **Update .env.example:**
```bash
# Add to .env.example
MISTRAL_API_KEY=your_mistral_api_key_here
```

3. **Update requirements.txt:**
```
# Ensure litellm is present (supports Mistral)
litellm==<version>
```

4. **Update README.md:**
```markdown
5. SmolMistralAgent - Working with Mistral AI
```

5. **Create test:**
```python
# tests/test_smol_mistral.py
# Follow existing test patterns
```

### Task: Debug Agent Execution Issues

**Common problems and solutions:**

1. **"API key not found"**
   ```bash
   # Check .env file exists
   ls -la .env

   # Verify variable name matches
   cat .env | grep YOUR_KEY

   # Test loading
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('YOUR_KEY'))"
   ```

2. **"Model not responding"**
   ```python
   # Add debug logging
   import logging
   logging.basicConfig(level=logging.DEBUG)

   # Check model initialization
   print(f"Model ID: {model.model_id}")
   ```

3. **"Tool not being called"**
   ```python
   # Verify tool registration
   print(f"Tools: {agent.tools}")

   # Check tool description
   print(f"Tool desc: {my_tool.description}")
   ```

4. **"Import errors"**
   ```bash
   # Verify virtual environment active
   which python

   # Check package installation
   pip list | grep smolagents

   # Reinstall if needed
   pip install --upgrade smolagents
   ```

### Task: Update Dependencies

**Process:**

1. **Generate version pins:**
```bash
# Activate virtual environment
source venv/bin/activate

# Create frozen requirements
pip freeze > requirements-frozen.txt

# Review and selectively copy to requirements.txt
# Keep only project dependencies, not sub-dependencies
```

2. **Test with fresh install:**
```bash
# Create new environment
python -m venv test-venv
source test-venv/bin/activate

# Install from requirements.txt
pip install -r requirements.txt

# Run examples
python smolagent_basic.py
python smol_multiagent.py
```

3. **Document versions:**
```
# requirements.txt
smolagents==1.2.3  # Multi-agent framework
litellm==0.8.5     # LLM provider abstraction
# ... etc
```

---

## What to Avoid

### ❌ Anti-Patterns

#### 1. Don't Commit API Keys
```python
# ❌ NEVER do this
api_key = "sk-1234567890abcdef"

# ✅ Always use environment variables
api_key = os.getenv("API_KEY")
```

#### 2. Don't Skip Error Handling
```python
# ❌ Will crash on missing key
model = LiteLLMModel(model_id="gpt-4")

# ✅ Validate first
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found")
model = LiteLLMModel(model_id="gpt-4")
```

#### 3. Don't Mix Agent Types Unnecessarily
```python
# ❌ CodeAgent when tools would work
agent = CodeAgent(tools=[search_tool], model=model)

# ✅ Use appropriate type
agent = ToolCallingAgent(tools=[search_tool], model=model)
```

#### 4. Don't Create Orphaned Tools
```python
# ❌ Tool that's never used (like visitwebpage.py currently)
@tool
def unused_tool(x: str) -> str:
    return x

# ✅ Either use it or delete it
```

#### 5. Don't Ignore Test Coverage
```python
# ❌ Stub tests that never get implemented
def test_something(self):
    pass  # TODO: Implement this

# ✅ Either implement or remove
def test_something(self):
    result = function_under_test()
    self.assertEqual(result, expected)
```

### ⚠️ Known Issues to Avoid

1. **visitwebpage.py is not integrated**
   - Don't reference it in new code
   - Use jinaai.py instead
   - Or help complete/integrate it properly

2. **requirements.txt has no versions**
   - Don't assume specific versions available
   - Pin versions when you update
   - Test with fresh installs

3. **Tests are incomplete**
   - Don't assume test coverage exists
   - Manually test all changes
   - Consider implementing tests when modifying code

4. **gradio not in requirements.txt**
   - Add it if you work on smol_gradio.py
   - Document this issue if encountered

5. **Typo in smol_blogwriter.py:51**
   - "checkedresearch" should be "checked research"
   - Fix if you're editing that file

---

## Troubleshooting

### Environment Issues

**Problem:** "No module named 'smolagents'"
```bash
# Solution:
pip install -r requirements.txt

# Or specifically:
pip install smolagents
```

**Problem:** "dotenv not loading .env"
```python
# Solution: Check file location
import os
from pathlib import Path

print(f"Current dir: {os.getcwd()}")
print(f".env exists: {Path('.env').exists()}")

# Ensure .env is in project root
# Or specify path:
load_dotenv(dotenv_path="/path/to/.env")
```

### API Issues

**Problem:** "Rate limit exceeded"
```python
# Solution: Add retry logic
import time
from functools import wraps

def retry_on_rate_limit(max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except RateLimitError:
                    if attempt < max_retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise
        return wrapper
    return decorator
```

**Problem:** "Invalid API key"
```bash
# Solution: Verify key format and validity
echo $YOUR_API_KEY  # Check if set

# Test key with curl
curl https://api.provider.com/test \
  -H "Authorization: Bearer $YOUR_API_KEY"
```

### Agent Issues

**Problem:** "Agent not calling tools"
```python
# Solution: Verify tool is properly decorated and registered
print(agent.tools)  # Should show your tools

# Check tool description is clear
@tool
def my_tool(query: str) -> str:
    """
    CLEAR description of what tool does and when to use it.
    Be specific about inputs and outputs.
    """
    pass
```

**Problem:** "Multi-agent coordination failing"
```python
# Solution: Check ManagedAgent descriptions
# Manager uses these to decide which agent to call

managed_agent = ManagedAgent(
    agent=agent,
    name="clear_name",
    description="SPECIFIC description of when to use this agent"
)

# Also check manager has access to managed agents
print(manager.managed_agents)
```

### Development Issues

**Problem:** "Example runs on import"
```python
# Current problem in some files:
# Code executes immediately when imported

# Solution: Use main guard
if __name__ == "__main__":
    # Move execution code here
    result = agent.run("task")
    print(result)
```

**Problem:** "Can't test due to module-level execution"
```python
# Solution: Refactor into functions
def create_agent():
    model = LiteLLMModel(...)
    return ToolCallingAgent(...)

def run_query(query: str) -> str:
    agent = create_agent()
    return agent.run(query)

if __name__ == "__main__":
    result = run_query("task")
    print(result)

# Now testable:
def test_agent_creation(self):
    agent = create_agent()
    self.assertIsNotNone(agent)
```

---

## Quick Reference

### Agent Types Quick Guide

| Agent Type | When to Use | Code Example |
|------------|-------------|--------------|
| CodeAgent | Math, data processing, code execution | `CodeAgent(tools=[], model=model)` |
| ToolCallingAgent | API calls, searches, predefined tools | `ToolCallingAgent(tools=[search], model=model)` |
| ManagedAgent | Wrapper for coordination | `ManagedAgent(agent=agent, name="x", description="...")` |

### Model Providers Quick Reference

| Provider | Model ID Example | API Key | Example File |
|----------|------------------|---------|--------------|
| HuggingFace | "Qwen/Qwen2.5-Coder-32B-Instruct" | HF_TOKEN | smolagent_basic.py |
| Anthropic | "claude-3-5-sonnet-20241022" | ANTHROPIC_API_KEY | smol_claude.py |
| Google | "gemini/gemini-2.0-flash-exp" | GEMINI_API_KEY | smolagent_gemini.py |
| OpenAI | "gpt-4o-mini" | OPENAI_API_KEY | smol_multiagent.py |
| Ollama | "ollama/llama2" | None (local) | smol_ollama.py |

### Common Import Patterns

```python
# Basic agent setup
from smolagents import CodeAgent, ToolCallingAgent, HfApiModel

# LLM providers
from smolagents import LiteLLMModel

# Multi-agent
from smolagents import ManagedAgent

# Built-in tools
from smolagents import DuckDuckGoSearchTool, Tool

# UI
from smolagents import GradioUI

# Custom tools
from smolagents import tool

# Environment
from dotenv import load_dotenv
import os
```

### File Locations Cheat Sheet

| Need to... | File/Directory |
|------------|----------------|
| Add new example | `smol_<name>.py` (root) |
| Add custom tool | `smoltools/<name>.py` |
| Add unit test | `smoltools/test_<name>.py` |
| Add integration test | `tests/test_<name>.py` |
| Update dependencies | `requirements.txt` |
| Document API keys | `.env.example` |
| Update setup instructions | `README.md` |
| Check current status | `UPDATES.md` |
| Reference this guide | `CLAUDE.md` |

### Command Cheat Sheet

```bash
# Setup
python -m venv venv
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env

# Running
python smolagent_basic.py          # Single example
python smol_blogwriter.py          # Multi-agent

# Testing
python -m unittest discover        # All tests
python -m unittest tests/test_smolagent_basic.py  # Specific test

# Development
pip freeze > requirements-frozen.txt  # Capture versions
pip list | grep smolagents           # Check installation
which python                         # Verify venv active
```

---

## Examples Gallery

### Minimal Working Example

```python
"""Simplest possible SmolAgent"""
from smolagents import CodeAgent, HfApiModel
import os

model = HfApiModel(token=os.getenv("HF_TOKEN"))
agent = CodeAgent(tools=[], model=model)
result = agent.run("What is 2 + 2?")
print(result)
```

### Tool Creation Example

```python
"""Custom tool with error handling"""
from smolagents import tool
import requests

@tool
def fetch_weather(city: str) -> str:
    """
    Fetches current weather for a city.

    Args:
        city: Name of the city

    Returns:
        Weather description or error message
    """
    try:
        # Implementation
        return f"Weather in {city}: Sunny, 72°F"
    except Exception as e:
        return f"Error: {str(e)}"
```

### Multi-Agent Example Pattern

```python
"""Two-agent system: researcher + writer"""
from smolagents import (
    ToolCallingAgent,
    ManagedAgent,
    CodeAgent,
    LiteLLMModel,
    DuckDuckGoSearchTool
)

model = LiteLLMModel(model_id="gpt-4o-mini")

# Specialist 1: Researcher
researcher = ToolCallingAgent(
    tools=[DuckDuckGoSearchTool()],
    model=model
)
managed_researcher = ManagedAgent(
    agent=researcher,
    name="researcher",
    description="Researches topics using web search"
)

# Specialist 2: Writer
writer = ToolCallingAgent(tools=[], model=model)
managed_writer = ManagedAgent(
    agent=writer,
    name="writer",
    description="Writes content based on research"
)

# Manager: Coordinates workflow
manager = CodeAgent(
    tools=[],
    model=model,
    managed_agents=[managed_researcher, managed_writer]
)

# Execute
result = manager.run("Research AI trends and write a summary")
```

---

## Contributing Guidelines

### Before Making Changes

1. **Read current state:**
   - Review UPDATES.md for known issues
   - Check if issue already documented
   - Understand current architecture

2. **Discuss significant changes:**
   - Open issue first for major features
   - Get feedback on approach
   - Ensure alignment with project goals

3. **Set up properly:**
   - Use virtual environment
   - Install all dependencies
   - Copy .env.example to .env

### While Making Changes

1. **Follow conventions:**
   - Use existing patterns
   - Match naming conventions
   - Keep code style consistent

2. **Test thoroughly:**
   - Manual testing required (tests incomplete)
   - Try with different API providers if applicable
   - Test error cases

3. **Document changes:**
   - Update relevant example files
   - Add comments for complex logic
   - Update README if adding features

### Before Committing

1. **Check your changes:**
   - No API keys in code
   - No .env file committed
   - requirements.txt updated if needed

2. **Update documentation:**
   - Update UPDATES.md if significant
   - Update this file for new patterns
   - Update README for user-facing changes

3. **Consider tests:**
   - Add tests if infrastructure improves
   - Document testing approach if complex
   - Note test coverage gaps

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-11-17 | Initial creation - comprehensive guide |

---

## Additional Resources

### SmolAgents Documentation
- [Official Docs](https://huggingface.co/docs/smolagents)
- [GitHub Repository](https://github.com/huggingface/smolagents)

### Tutorial Resources
- [YouTube Tutorial](https://youtu.be/XHijkFRd2TU)
- This repository's examples

### LLM Provider Docs
- [Anthropic Claude](https://docs.anthropic.com/)
- [Google Gemini](https://ai.google.dev/)
- [OpenAI](https://platform.openai.com/docs)
- [Ollama](https://ollama.ai/)
- [LiteLLM](https://docs.litellm.ai/)

### Related Tools
- [Jina AI](https://jina.ai/)
- [Gradio](https://gradio.app/)
- [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/)

---

**Last Updated:** 2025-11-17
**Maintained By:** Repository contributors
**Questions?** Open an issue or check UPDATES.md
