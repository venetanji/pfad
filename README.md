# 🎮 SD5913 - Programming for Art and Design 🎨

Welcome to the repository for SD5913! This repo contains weekly exercises, projects, and examples for the Programming for Artists and Designers class.

## 📂 Repository Structure

The repository is organized by weeks, with each folder containing the code and resources for that week's topics:

```
/week01, /week02, ... - Weekly content and exercises
/extra              - Additional code examples and resources
```

## 🚀 Getting Started

Clone the repo:
```bash
git clone https://github.com/venetanji/pfad
```

Update the repo:
```bash
git pull
```

Install requirements for a specific week:
```bash
cd pfad/week##/
pip install -r requirements.txt
```

## 📅 Weekly Content

### Week 01: Web Scraping & Data Collection 🕸️

In Week 01, we explore the basics of web scraping using Python. The main script connects to the Hong Kong Observatory website to fetch tide data. Key concepts covered include:

- Loading environment variables with `python-dotenv`
- Making HTTP requests with the `requests` library
- Parsing HTML using `lxml`
- Working with XPath to extract specific data from web pages
- File handling for storing and retrieving web content

This week establishes fundamental data collection techniques that will be used throughout the course.

### Week 02: Data Visualization & Utilities 📊

Week 02 focuses on data visualization, basic data processing, and utility scripts in Python. The folder includes:

- `draw_svg.py`: Script for drawing SVG graphics programmatically.
- `multi_city_temp.py`: Handles temperature data for multiple cities, likely involving data parsing and visualization.
- `plot_tides.py`: Plots tide data, building on the data collection from Week 01.
- `scraping_utils.py`: Utility functions for web scraping and data handling.
- `tides_csv.py`: Processes and saves tide data to CSV format.
- `week02_notebook.ipynb`: Jupyter notebook with interactive code and explanations for the week's topics.
- `requirements.txt`: Lists required Python packages for this week's exercises.

There is also a `python_foundations/` subfolder with foundational Jupyter notebooks covering:
- Flow control keywords
- Functions and arguments
- Installing and using matplotlib
- Expanded variable types in Python

These resources help reinforce core Python concepts and introduce data visualization techniques.

### Week 03: Fractals & Mathematical Visualization 🌀

Week 03 explores fractal geometry and mathematical art using Python. Topics include:

- **Koch Snowflake**: Recursive generation of Koch curves using NumPy complex numbers
- **Mandelbrot Set**: Computing and visualizing the famous Mandelbrot fractal
- Mathematical visualization with Matplotlib
- Recursive algorithms and complex number mathematics
- Creating artistic patterns through mathematical formulas

This week demonstrates how code can generate beautiful, complex patterns from simple mathematical rules.

### Week 04: Interactive User Interfaces with Streamlit 💬

Week 04 introduces building interactive applications with Streamlit. The exercises cover:

- **Basic User Input**: Simple chat input interfaces
- **Chat History**: Building conversational interfaces with message persistence
- Streamlit fundamentals for rapid UI development
- Creating interactive web applications without HTML/CSS
- Real-time user interaction patterns

Students learn to create user-facing applications that can accept and respond to user input.

### Week 05: Generative Image Creation 🖼️

Week 05 focuses on programmatic image generation using Python. Topics include:

- **Random Image Generation**: Creating images with NumPy random data
- **Generative Images**: Using algorithms to create structured visual content
- Working with PIL (Python Imaging Library)
- NumPy array manipulation for image data
- Understanding RGB color spaces and pixel manipulation

This week lays the foundation for computational image creation and manipulation.

### Week 06: Audio Synthesis & Generation 🔊

Week 06 explores audio generation and processing with Python. Covered topics:

- **Random Audio**: Generating random audio streams with PyAudio
- **Generative Audio**: Creating structured sound patterns programmatically
- Real-time audio output and streaming
- Understanding audio data formats (sample rates, channels)
- Working with NumPy arrays for audio data

Students learn to create and manipulate audio programmatically, opening possibilities for sound art.

### Week 07: AI Agents & LangGraph 🤖

Week 07 introduces AI-powered applications using LangGraph and Ollama. Topics covered:

- **LangGraph Chatbots**: Building conversational AI with state management
- **Tool Calling**: Enabling AI agents to use external tools and functions
- Working with local LLMs using Ollama
- State management and conversation memory
- Creating AI agents that can perform actions

This week demonstrates how to build intelligent, interactive AI systems.

### Week 08: Computer Vision with MediaPipe 👁️

Week 08 explores real-time computer vision using MediaPipe. Content includes:

- **Face Detection**: Detecting and tracking faces in webcam feeds
- **Hand Tracking**: Real-time hand landmark detection and gesture recognition
- Working with OpenCV for video capture and display
- MediaPipe solutions for computer vision tasks
- Building camera-based interactive applications

Students learn to create applications that understand and respond to visual input.

### Week 09: Web APIs with FastAPI 🌐

Week 09 introduces building web APIs using FastAPI. Topics covered:

- FastAPI fundamentals and routing
- Request/response models with Pydantic
- RESTful API design patterns
- Creating endpoints for data exchange
- Running web servers with Uvicorn

This week teaches how to create backend services that can be consumed by web and mobile applications.

### Week 10: Advanced Streamlit Applications 📱

Week 10 builds on Streamlit knowledge with more complex applications:

- **Handbook App**: PDF processing with Qdrant vector database for semantic search
- **Login App**: User authentication and session management
- Integrating vector databases for AI-powered search
- Multi-page Streamlit applications
- Working with Docker Compose for service orchestration

Students learn to build production-ready applications with databases and user management.

### Week 11: 3D Modeling & Data Mining 🎨

Week 11 explores two powerful tools for artists and data scientists:

- **Blender**: Python scripting for 3D modeling and dataset generation
- **Orange**: Visual programming for data mining and machine learning workflows
- Automating 3D content creation with Python
- Visual data analysis and machine learning pipelines
- Integration of 3D tools with data processing

This week bridges the gap between 3D art and data science.

### Week 12: MCP-Powered Streamlit Agents 🎯

Week 12 ties Streamlit, LangChain, and the Model Context Protocol (MCP) together:

- `app.py` hosts a Streamlit chat UI that streams updates from a LangChain `create_agent` graph.
- `bot.py` targets a local OpenAI-compatible endpoint (LM Studio, Ollama, etc.) so you can drive lightweight models without cloud calls.
- `tools.py` shows how `MultiServerMCPClient` connects to the provided `comfyui-mcp-server/`, letting the agent trigger remote ComfyUI image workflows as tools.
- Async orchestration keeps the UI responsive while the agent reasons, calls MCP tools, and reports tool responses back into chat history.

This week is all about wiring creative tools into an agent loop rather than focusing on UI polish.

### Week 13: Back to Basics – Semester Loop ♻️

Week 13 strips things down to a single `semester.py` script that replays the original pseudo-code loop with a tiny harness:

- `from __future__ import annotations` postpones evaluation of type hints so factory/class methods can annotate `Problem` before Python knows the class itself; this keeps the file Python 3.12-friendly without using string literal annotations everywhere.
- The `@dataclass` decorator builds the `Problem` boilerplate (`__init__`, `__repr__`, comparisons) automatically, so you only declare the fields that matter (difficulty, solved flag, attempts).
- Deterministic helper classes (`SemesterClock`, `Student`, `Code`) keep control flow safe while random checks mimic the original chaotic semester narrative.
- Fresh print statements surface each attempt, state change, skill upgrade, and panic cool-down so you can observe the loop without stepping through a debugger.

It is a quick reminder that solid fundamentals—clean dataclasses, future-ready annotations, and small test doubles—make bigger creative projects easier to reason about.

## 🧪 Extra Resources

The `/extra` folder contains additional code examples and experimental projects that might be helpful for your assignments:

- Various computer vision examples with OpenCV and diffusion models
- Nake code examples
- Y-R-we-here project samples

Feel free to explore these examples for inspiration or as starting points for your own projects!

