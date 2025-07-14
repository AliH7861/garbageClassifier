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

Clone the repository:


git clone https://github.com/yourusername/ecobin-ai.git
cd ecobin-ai

## Install dependencies

```bash
pip install -r requirements.txt

## Set up environment variables

1. Copy `.env.example` to `.env`
2. Fill in `DATABASE_URL` (your PostgreSQL URI) and any other required variables

## Prepare the database

1. Create a new PostgreSQL database
2. Run migration scripts (if provided), or let SQLAlchemy auto-create tables on first run

## Run the application

```bash
streamlit run dashboard.py
# OR
python main.py

## Usage

- Sign up or log in.
- Upload an image of your waste item for an instant bin recommendation.
- Edit your bins:
  - Change names/images to fit your home
  - Revert to Durham Region defaults anytime
- Visit your dashboard:
  - See recent submissions, analytics, and personalized charts

**Privacy:**  
Your submissions & customizations are private and visible only to you.

---

## Configuration

- **Bins:**  
  Default bins match Durham Region categories. You can upload your own images and rename bins at any time.

- **Environment Variables:**  
  `DATABASE_URL` (PostgreSQL) required—set this in your `.env` file.

- **Data Storage:**  
  User accounts, submissions, and analytics are stored securely in PostgreSQL. Uploaded images are processed and deleted after 30 minutes for privacy.

---

## Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **AI Model:** ResNet50 (TensorFlow)
- **Frontend/UI:** Streamlit, HTML, CSS, JavaScript
- **Database:** PostgreSQL
- **Dev Environment:** Jupyter Notebook

---

## Contributing

We welcome all contributions!

1. Fork the repository
2. Create a feature branch:
    ```bash
    git checkout -b feature/your-feature
    ```
3. Commit your changes:
    ```bash
    git commit -am "Add new feature"
    ```
4. Push to your branch:
    ```bash
    git push origin feature/your-feature
    ```
5. Open a Pull Request and describe your changes.

---

## Testing

Automated and manual tests for major features are included.