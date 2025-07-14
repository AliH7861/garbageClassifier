
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

1. Sign up and create your own account

2. Use the username and password to login

3. Upload an Image of a household waste item

4. Click the Submit Button to let an AI model predict the correct bin (e.g., Green Bin, Blue Box, Garbage).

5. View your personalized dashboard for:
   - Recent submissions
   - Analytics (pie charts, total scans)

6. Customize bins (rename or change image) or revert to defaults.   

## Configuration
Before running the app, make sure to set up the required environment variables.

1. **Create a `.env` file** in the root directory (you can copy from `.env.example`).

2. **Set your environment variables**, especially:

``` env
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<dbname>
```
3. **Custom Bin Pictures**  
   You can replace the default bin images with your own by submitting pictures through the `picture.py` script.

   - This allows you to personalize how each bin looks when the AI model predicts.
   - You can revert back to the default Durham Region images anytime.

   > Make sure the uploaded image names match the category keys or update the logic in `picture.py` accordingly.

