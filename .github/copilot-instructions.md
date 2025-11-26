# SD5913 - Programming for Art and Design

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

This is a Python-based educational repository for Programming for Artists and Designers class, organized by weekly exercises. Each week contains Python scripts, Jupyter notebooks, and projects focusing on web scraping, data visualization, AI/ML, computer vision, and creative applications.

## Working Effectively

### Environment Setup
- Repository uses Python 3.12.3 with system packages already available
- Key available system packages: `requests`, `numpy`, `matplotlib`, `lxml`, `python-dotenv`
- Packages that INSTALL SUCCESSFULLY: `pandas`, `matplotlib`, `numpy`, basic Python libraries
- Docker 28.0.4 and Docker Compose v2.38.2 are available
- Network access is LIMITED - pip installs frequently fail due to SSL/timeout issues
- External API calls (web scraping) will fail due to network restrictions

### Bootstrap and Test Repository
1. **ALWAYS start with basic environment check:**
   ```bash
   python3 --version  # Should show Python 3.12.3
   docker --version   # Should show Docker 28.0.4
   docker compose version  # Should show v2.38.2
   ```

2. **For week-specific work:**
   ```bash
   cd /home/runner/work/pfad/pfad/week##/
   pip3 install -r requirements.txt  # EXPECT FAILURES due to network limitations
   ```

3. **Test basic functionality:**
   ```bash
   # Test matplotlib (works)
   python3 -c "import matplotlib.pyplot as plt; import numpy as np; x=np.linspace(0,10,100); plt.plot(x, np.sin(x)); plt.savefig('/tmp/test.png'); print('Success')"
   
   # Test local modules
   python3 -c "import sys; sys.path.append('.'); import main; print('Module loaded')"
   ```

### Package Installation - CRITICAL LIMITATIONS
- **NETWORK LIMITATIONS**: pip installs FREQUENTLY FAIL due to SSL certificate issues and timeouts
- **NEVER CANCEL**: pip install attempts take 2-5 minutes and often fail. WAIT for completion.
- **Available packages**: Use system packages when possible: `requests`, `numpy`, `matplotlib`, `lxml`, `python-dotenv`
- **Successfully install**: `pandas`, `matplotlib`, `numpy` - these typically work within ~30 seconds
- **Known failures**: `streamlit`, `coqui-tts`, `langgraph`, `langchain`, `weaviate`, AI/ML packages requiring internet
- **Workaround**: Focus on testing code logic with available packages; document expected requirements

### Docker Workflows
- **Docker Compose configuration validation:**
  ```bash
  cd /home/runner/work/pfad/pfad
  docker compose config  # Takes 1-2 seconds, validates YAML
  ```

- **Docker builds WILL FAIL** due to network restrictions during pip install steps:
  ```bash
  cd /home/runner/work/pfad/pfad/week08
  docker build -t test .  # EXPECTED TO FAIL after 20-30 seconds
  ```

- **NEVER CANCEL**: Docker builds take 20-30 seconds before failing. Document the failure pattern.

## Weekly Structure and Validation

### Week 01: Web Scraping & Data Collection
- **Files**: `main.py`, `.env`, `requirements.txt`
- **Dependencies**: `python-dotenv`, `requests`, `lxml` (available)
- **Test command**: `cd week01 && python3 main.py` (WILL FAIL due to network restrictions)
- **Expected behavior**: Network error when trying to fetch HKO tide data
- **Validation**: Code syntax and imports work; network calls fail as expected

### Week 02: Data Visualization & Utilities  
- **Files**: `plot_tides.py`, `scraping_utils.py`, `draw_svg.py`, `week02_notebook.ipynb`, `python_foundations/` subfolder
- **Dependencies**: `python-dotenv`, `requests`, `lxml` (same as week01)
- **Test commands**:
  ```bash
  cd week02
  python3 -c "import scraping_utils; print('Utils work')"
  python3 -c "import matplotlib.pyplot as plt; print('Matplotlib works')"
  ```
- **Validation**: Modules import successfully, plotting works (save to `/tmp/`)
- **Subfolder**: `python_foundations/` contains Jupyter notebooks covering flow control, functions, matplotlib installation, and variable types

### Week 03: Fractals & Mathematical Visualization
- **Files**: `run_examples.py`, fractal scripts (`koch_curve.py`, `mandelbrot.py`, `sierpinksi_matplot_animation.py`), `week03_notebook.ipynb`
- **Dependencies**: `numpy`, `matplotlib`, `pandas` (ALL WORK - install successfully)
- **Topics**: Koch snowflake, Mandelbrot set, recursive algorithms, complex number mathematics
- **Test commands**:
  ```bash
  cd week03
  pip3 install -r requirements.txt  # Installs successfully in ~30 seconds
  python3 run_examples.py  # Generates plots in week03/plots/
  ls plots/  # Should show line_plot.png, multi_series.png, rolling_mean.png, monthly_avg.png
  ```
- **Validation**: Full week03 functionality WORKS - script execution and plot generation succeed
- **Output**: Plots saved to `week03/plots/` directory

### Week 04: Interactive User Interfaces with Streamlit
- **Files**: `1_user_input.py`, `2_user_input_with_history.py`, `3_chat_with_response.py`, `ollama_chatbot.py`, `lmstudio_chatbot.py`, `display_graph.py`, `display_image.py`
- **Dependencies**: `streamlit`, `ollama`, `openai` (INSTALL FAILS)
- **Topics**: Basic user input, chat history, conversational interfaces, Streamlit fundamentals
- **Expected**: Cannot run Streamlit apps due to missing dependencies
- **Validation**: Check code syntax only; document dependency failures

### Week 05: Generative Image Creation
- **Files**: `1_random_image.py`, `2_gen_image.py`, `3_gen_image_lcm.py`, `4_controlnet_canny.py`, `st_tti.py`, `st_controlnet.py`, `python_classes_tutorial.ipynb`
- **Dependencies**: `diffusers`, `transformers`, `PIL`, `torch`, `accelerate` (INSTALL FAILS)
- **Topics**: Random image generation, NumPy array manipulation, RGB color spaces, PIL image handling, diffusion models
- **Expected**: Cannot run image generation due to missing GPU libraries
- **Validation**: Verify code structure and import patterns

### Week 06: Audio Synthesis & Generation
- **Files**: `1_random_audio.py`, `2_gen_audio.py`, `3_synth_audio.py`, `4a_asyncio_loopback.py`, `4b_pyaudio_loopback.py`, `5_spectrogram.py`, `5_waveform.py`, `6a_spectrogram_pygame.py`, `6b_spectrogram.py`
- **Dependencies**: `pyaudio`, `numpy`, `matplotlib`, `pyo`, `pygame` (MIXED - numpy/matplotlib work, audio libraries fail)
- **Topics**: Random audio generation, structured sound patterns, real-time audio streaming, sample rates, audio visualization
- **Expected**: Audio library dependencies fail; numpy/matplotlib portions testable
- **Validation**: Syntax check only for audio portions; test data processing if applicable

### Week 07: AI Agents & LangGraph
- **Files**: `1_langgraph_chat.py`, `2_tool_calling.py`, `3_graph_agent.py`, `processing/` subfolder
- **Dependencies**: `langgraph`, `langchain_ollama` (INSTALL FAILS)
- **Topics**: LangGraph chatbots, tool calling, AI agents, state management, conversation memory
- **Expected**: Cannot run LangGraph agents due to missing dependencies
- **Validation**: Code structure review only

### Week 08: Computer Vision with MediaPipe
- **Files**: `1_face_detection.py`, `2_hand_tracking.py`, `3_pose_estimation.py`, `4_face_mesh.py`, `5_gesture_recognition.py`, `6_holistic_detection.py`, `7_selfie_segmentation.py`, `8_multi_detection.py`, `9_emotion_detection.py`, `camera_utils.py`, `setup_camera.py`
- **Dependencies**: `mediapipe`, `opencv-python` (INSTALL FAILS)
- **Topics**: Face detection, hand tracking, pose estimation, gesture recognition, webcam-based interactive applications
- **Test commands**:
  ```bash
  cd week08
  python3 -m py_compile camera_utils.py  # Syntax check works
  ```
- **Validation**: Code syntax checking; cannot run due to mediapipe dependency

### Week 09: FastAPI & WebSockets
- **Files**: `fastapi_example.py`, `websocket_server_echo.py`, `websocket_client_example.py`, `pygame_websocket.py`, `compose.yml`
- **Dependencies**: `fastapi`, `websockets`, `uvicorn` (INSTALL FAILS)
- **Expected**: Cannot run FastAPI/WebSocket servers due to missing dependencies
- **Validation**: Code structure review only

### Week 10: Advanced Streamlit Applications
- **Files**: `handbook_app/`, `login_app/`, `word2vec_example.py`
- **Dependencies**: `qdrant`, `langchain`, `peewee`, `gensim` (INSTALL FAILS)
- **Topics**: PDF processing, vector databases, semantic search, user authentication, session management, multi-page Streamlit apps
- **Services**: Ollama, Qdrant (cannot start due to dependencies)
- **Validation**: Code structure review only

### Week 11: 3D Modeling, NDI & External Tools
- **Files**: `blender/`, `orange/`, `touchdesigner/`, `maxmsp/`, NDI integration (`ndi_hand_tracking.py`, `ndi_utils.py`), OSC (`osc_demo.py`)
- **Dependencies**: External applications (Blender, Orange Data Mining, TouchDesigner, Max/MSP), NDI SDK
- **Topics**: Python scripting for 3D modeling, visual data mining, NDI video streaming, OSC communication
- **Expected**: Integration examples for external creative tools
- **Validation**: Review code structure; cannot execute without external tools

### Week 12: MCP-Powered Streamlit Agents
- **Files**: `app.py`, `bot.py`, `tools.py`, `comfyui-mcp-server/` submodule
- **Dependencies**: `langchain`, `mcp`, `streamlit` (INSTALL FAILS)
- **Topics**: Model Context Protocol (MCP), LangChain agent integration, tool calling, async orchestration, ComfyUI workflow automation
- **Expected**: MCP agent with ComfyUI tool integration
- **Validation**: Review agent loop architecture and MCP tool patterns

### Week 13: Back to Basics – Semester Loop
- **Files**: `semester.py`
- **Dependencies**: None (standard library only)
- **Topics**: `@dataclass` decorator, type annotations with `from __future__ import annotations`, clean control flow, deterministic helper classes
- **Test command**: `cd week13 && python3 semester.py`
- **Validation**: Pure Python - should run successfully

## Common Validation Patterns

### ALWAYS Test These Scenarios After Changes:
1. **Python syntax validation** (completes in <0.1 seconds):
   ```bash
   python3 -m py_compile script_name.py
   ```

2. **Import testing** (completes in <0.2 seconds):
   ```bash
   python3 -c "import script_name; print('Syntax OK')"
   ```

3. **Matplotlib plotting** (completes in ~0.6 seconds):
   ```bash
   python3 -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; import numpy as np; plt.plot([1,2,3]); plt.savefig('/tmp/test.png'); print('Plot created')"
   ```

4. **Docker configuration** (completes in ~0.1 seconds):
   ```bash
   docker compose config  # Should complete in 1-2 seconds
   ```

5. **Comprehensive validation test** (completes in ~2 seconds):
   ```bash
   # Run from repository root
   cd /home/runner/work/pfad/pfad
   python3 --version && docker --version && docker compose version
   pip3 list | grep -E "(requests|numpy|matplotlib|pandas)"
   cd week02 && python3 -c "import scraping_utils; print('✓ Local modules work')"
   python3 -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('/tmp/quick_test.png'); print('✓ Plotting works')"
   cd .. && docker compose config > /dev/null && echo "✓ Docker config works"
   ```

6. **Week03 full validation** (completes in ~1 second after packages installed):
   ```bash
   cd /home/runner/work/pfad/pfad/week03
   pip3 install -r requirements.txt  # First time: ~30 seconds
   python3 run_examples.py && ls plots/*.png && echo "✓ Week03 plots generated"
   ```

### NEVER Do These:
- **NEVER CANCEL** pip installs before 5+ minutes (they often take 2-5 minutes to fail)
- **NEVER CANCEL** Docker builds before 30+ seconds  
- **DO NOT** expect external network calls to work
- **DO NOT** try to run Streamlit apps (will fail due to missing dependencies)

## Timing Expectations - CRITICAL
- **pip install**: 2-5 minutes before timeout/SSL failure - NEVER CANCEL early
- **Docker build**: 20-30 seconds before network failure - NEVER CANCEL early  
- **Python script execution**: Immediate for syntax, fails on network calls
- **Docker compose config**: 1-2 seconds
- **Module imports**: Immediate for available packages

## Key Repository Areas

### Most Important Directories:
- `/week01/` - Basic web scraping foundation (network calls fail)
- `/week02/` - Data visualization with matplotlib (WORKS) + Python foundations notebooks
- `/week03/` - Fractals & mathematical visualization (FULLY WORKS - pandas, matplotlib, numpy)
- `/week04/` - Streamlit UI applications (dependencies fail)
- `/week05/` - Generative image creation (dependencies fail)
- `/week06/` - Audio synthesis & processing (partial - numpy/matplotlib work)
- `/week07/` - LangGraph AI agents (dependencies fail)
- `/week08/` - MediaPipe computer vision (dependencies fail)
- `/week09/` - FastAPI & WebSockets (dependencies fail)
- `/week10/` - Advanced Streamlit with vector databases (dependencies fail)
- `/week11/` - Third-party tool integrations (Blender, Orange, TouchDesigner, NDI)
- `/week12/` - MCP-powered Streamlit agents (dependencies fail)
- `/week13/` - Back to basics (WORKS - pure Python)
- `/extra/` - Additional examples: opencv-diffusers, nake, Y-R-we-here projects

### Common Commands Reference:
```bash
# Repository navigation
cd /home/runner/work/pfad/pfad/week##/

# Basic testing
python3 --version
pip3 list | grep -E "(requests|numpy|matplotlib)"

# Dependency installation (expect failures)
pip3 install -r requirements.txt  # 2-5 minutes, often fails

# Docker operations  
docker compose config              # Works quickly
docker build .                     # Fails after 20-30 seconds

# Safe plotting test
python3 -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('/tmp/test.png')"
```

### Expected File Output Locations:
- Plots: Save to `/tmp/` directory (e.g., `/tmp/test_plot.png`)
- Cached web pages: Week directories (e.g., `crawled-page-2023.html`)
- Generated images: Week-specific subdirectories or `/tmp/`

**REMEMBER**: This environment has significant network limitations. Focus on code structure validation, syntax checking, and testing with available system packages. Document when network-dependent features cannot be tested.

## Course Patterns & Best Practices

### Recurring Weekly Patterns
1. **Numbered file progression**: Files often follow `1_`, `2_`, `3_` naming to indicate learning progression (e.g., `1_random_image.py` → `2_gen_image.py`)
2. **requirements.txt per week**: Each week has isolated dependencies
3. **Jupyter notebooks**: Most weeks include `week##_notebook.ipynb` for interactive exploration
4. **Streamlit apps**: Weeks 04, 05, 10, 12 use Streamlit for UI (`st_*.py` prefix common)

### Technology Progression Through Course
- **Weeks 01-03**: Foundation (web scraping → visualization → generative art)
- **Week 04**: Interactive UI introduction (Streamlit basics)
- **Weeks 05-06**: Media generation (images → audio)
- **Week 07**: AI integration (LangGraph, tool calling)
- **Week 08**: Computer vision (MediaPipe)
- **Week 09**: Web services (FastAPI, WebSockets)
- **Week 10**: Production patterns (authentication, vector databases)
- **Week 11**: External tool integration (Blender, TouchDesigner, NDI)
- **Week 12**: Advanced AI agents (MCP, LangChain)
- **Week 13**: Review & fundamentals (dataclasses, annotations)

### Common Code Patterns
- **Environment variables**: Use `python-dotenv` for API keys and configuration
- **Type annotations**: Modern Python with `from __future__ import annotations`
- **Dataclasses**: Clean data structures with `@dataclass` decorator
- **Async patterns**: AsyncIO for concurrent operations (audio, websockets, agents)
- **Streamlit state**: `st.session_state` for conversation history and user data

### Creative Applications Focus
The course emphasizes practical creative applications:
- **Data visualization**: matplotlib for artistic visualizations
- **Generative content**: Fractals, random images, synthesized audio
- **Real-time interaction**: Webcam, audio streaming, WebSocket communication
- **AI assistance**: Chatbots, tool-calling agents, image generation
- **Tool integration**: Connecting Python with Blender, TouchDesigner, ComfyUI