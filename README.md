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

## 🧪 Extra Resources

The `/extra` folder contains additional code examples and experimental projects that might be helpful for your assignments:

- Various computer vision examples with OpenCV and diffusion models
- Nake code examples
- Y-R-we-here project samples

Feel free to explore these examples for inspiration or as starting points for your own projects!

