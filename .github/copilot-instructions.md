# SD5913 - Programming for Art and Design

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

This is a Python-based educational repository for Programming for Artists and Designers class, organized by weekly exercises. Each week contains Python scripts, Jupyter notebooks, and projects focusing on web scraping, data visualization, AI/ML, computer vision, and creative applications.

## Working Effectively

### Environment Setup
- Repository uses Python 3.12.3 with system packages already available
- Key available system packages: `requests`, `numpy`, `matplotlib`, `lxml`, `python-dotenv`
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
- **Known failures**: `streamlit`, `coqui-tts`, `langgraph`, `langchain`, AI/ML packages requiring internet
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
- **Files**: `plot_tides.py`, `scraping_utils.py`, `draw_svg.py`, `week02_notebook.ipynb`
- **Dependencies**: Adds `matplotlib` (works)
- **Test commands**:
  ```bash
  cd week02
  python3 -c "import scraping_utils; print('Utils work')"
  python3 -c "import matplotlib.pyplot as plt; print('Matplotlib works')"
  ```
- **Validation**: Modules import successfully, plotting works (save to `/tmp/`)

### Week 04: Streamlit Apps & AI Integration
- **Files**: `ollama_chatbot.py`, `lmstudio_chatbot.py`, `wav_talker.py`
- **Dependencies**: `streamlit`, `ollama`, `openai` (INSTALL FAILS)
- **Expected**: Cannot run Streamlit apps due to missing dependencies
- **Validation**: Check code syntax only; document dependency failures

### Week 05: Computer Vision & Diffusion
- **Files**: `st_tti.py`, `st_controlnet.py`, various image generation scripts
- **Dependencies**: `diffusers`, `transformers`, `opencv-python` (INSTALL FAILS)
- **Expected**: Cannot run image generation due to missing GPU libraries
- **Validation**: Verify code structure and import patterns

### Week 08: Docker & LangGraph Bots
- **Files**: `Dockerfile`, `compose.yml`, `src/app.py`, `src/bot.py`
- **Dependencies**: `langgraph`, `langchain_ollama` (INSTALL FAILS)
- **Docker build time**: 20-30 seconds before SSL failure
- **Test commands**:
  ```bash
  cd week08
  docker compose config  # Works - validates YAML
  docker build .  # FAILS after 20-30 seconds - EXPECTED
  ```

### Week 10: Vector Databases & User Management
- **Files**: `app.py`, `model.py`, `weaviate_store.py`, `compose.yml`
- **Dependencies**: `weaviate`, `langchain`, `peewee` (INSTALL FAILS)
- **Services**: Ollama, Weaviate (cannot start due to GPU requirements)
- **Validation**: Code structure review only

### Week 12: ComfyUI Integration
- **Files**: `app.py`, `workflows/workflow_api.json`
- **Dependencies**: Complex Streamlit + ComfyUI setup (INSTALL FAILS)
- **Expected**: Multi-page Streamlit app with ComfyUI and structured output
- **Validation**: Review navigation structure and API integration patterns

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
   pip3 list | grep -E "(requests|numpy|matplotlib)"
   cd week02 && python3 -c "import scraping_utils; print('✓ Local modules work')"
   python3 -c "import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.savefig('/tmp/quick_test.png'); print('✓ Plotting works')"
   cd .. && docker compose config > /dev/null && echo "✓ Docker config works"
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
- `/week02/` - Data visualization with matplotlib (WORKS)
- `/week04/` - Streamlit applications (dependencies fail)
- `/week08/` - Docker containerization (build fails, config works)
- `/extra/` - Additional examples and computer vision projects

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