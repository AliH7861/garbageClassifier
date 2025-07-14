
# **EcoBin AI**

## Description
EcoBin AI is a smart web application that helps you classify household waste using AI. Simply sign up, upload any image, and our ResNet50 deep learning model predicts the correct Durham Region bin (e.g., Green Bin, Blue Box, Garbage). Your personal dashboard updates in real time track all submissions, fully customize bins (images & names), get analytics, and revert to official defaults with one click.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [Testing](#testing)
- [FAQ](#faq)
- [License](#license)
- [Contact](#contact)

## Features
- **Bin Prediction**  
    Instantly predicts which Durham Region bin (Green Bin, Blue Box, Garbage, etc.) your item belongs to.

- **Customizable Bins**  
    Swap default bin images/names with your own for a personalized experience. Revert to official bins anytime.

- **Live Dashboard**  
    Updates with every submission. Shows:
     * Last 7 submissions (with image previews)
     * Pie chart: today’s classified (bins & classes)
     * Bar chart: bin/submission counts for today
     * Most common bin (today & all-time)
     * Total scan count (today & all-time)
     * Line Chart of daily scans

- **User Accounts**  
    Swap default bin images/names with your own for a personalized experience. Revert to official bins anytime.

## Getting Started
### Dependencies
* Python 3.8+
* pip (Python package manager)
* Visual Studio Code

### Installing
1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo

2. Install required packages:

   ```bash
   pip install -r requirements.txt

### Executing Program
1. Terminal 01: FastAPI Setup

   ```bash
   uvicorn main:app --reload

2. Terminal 02: Frontend Setup

   ```bash
   streamlit run login.py

## Usage