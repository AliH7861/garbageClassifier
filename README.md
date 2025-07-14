# EcoBin AI

## Description
EcoBin AI is a smart web application that helps you classify household waste using AI. Simply sign up, upload any image, and our ResNet50 deep learning model predicts the correct Durham Region bin (e.g., Green Bin, Blue Box, Garbage). Your personal dashboard updates in real time—track all submissions, fully customize bins (images & names), get analytics, and revert to official defaults with one click.

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
  - Last 7 submissions (with image previews)
  - Pie chart: today’s classified bins
  - Bar chart: bin/submission counts for today
  - Most common bin (today & all-time)
  - Total scan count (today & all-time)

- **User Accounts**  
  Sign up, log in/out. Each user’s submissions & bin settings are separate and private.

## Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL
- pip (Python package manager)

### Installation

First, make sure you have Python 3.8+ installed on your machine. Then, install all the required packages by running:

```bash
pip install -r requirements.txt

First, make sure you have Python 3.8+ installed on your machine. Then, install all the required packages by running:

```bash
pip install -r requirements.txt
