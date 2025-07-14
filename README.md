
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


##  Tech Stack

**Programming Language**
- Python 3.11 – used across backend, ML logic, and frontend scripting

**Frontend**
- **Streamlit** – interactive UI for users to upload images, track bin predictions, and view analytics
- **Plotly** – used to render beautiful pie, bar, and line charts dynamically
- **Pandas** – for data manipulation and display in tables
- **Matplotlib** – additional plotting support
- **Custom CSS + Google Fonts** – for styling and UI polish (`Poppins`, `Montserrat`, `Open Sans`)
- **streamlit-cookies-manager** – manages login sessions with encrypted cookies
- **streamlit_autorefresh** – auto-refreshes dashboard every 10 seconds

**Backend**
- **FastAPI** – serves predictions and API endpoints
- **SQLAlchemy** – ORM for PostgreSQL
- **dotenv** – for loading env variables
- **requests** – makes API calls from Streamlit to FastAPI backend
- **hashlib** – for password hashing and user auth

**Machine Learning**
- **TensorFlow / Keras** – loads and runs ResNet50 image classification model
- **PIL (Pillow)** – reads and resizes images
- **NumPy** – handles array transformations for model input/output

**Database**
- **PostgreSQL** – stores user accounts, image submissions, prediction results, and analytics
- **Railway** – cloud hosting for the PostgreSQL database and optionally the backend

**Other Features**
- **EncryptedCookieManager** – keeps login sessions persistent without exposing raw credentials
- **Image Upload + Customization** – users can replace bin images with personal ones
- **Modular Routing** – app split across multiple Streamlit pages (`login.py`, `dashboard.py`, `pictures.py`, etc.)

## Contributing

We welcome contributions to improve this project! To contribute:

1. Fork this repository
2. Create a new branch (`git checkout -b feature-name`)
3. Commit your changes (`git commit -m "Add feature"`)
4. Push to your branch (`git push origin feature-name`)
5. Create a pull request

Please make sure your code follows our style and includes relevant tests/documentation.

## Testing
Before pushing any changes, please test your code:

For backend (FastAPI):
```bash
# Example with pytest
pytest tests/
```

## FAQ

**Q: What images can I upload?**  
A: You can upload any image that is less than 200MB and in JPG, JPEG, or PNG format.

---


**Q: How do I reset my bins to default?**  
A: Use the **“Return Original”** button on the Pictures page to restore the official Durham Region bin images.

---


**Q: Is this app only for Durham Region?**  
A: No! You can fully customize the bin categories and images to match any region or your personal needs.

---

**Q: How is my data stored?**  
A: Each user’s account, bin customizations, and analytics are stored securely in a PostgreSQL database.  
Personal bin images are **temporarily stored** during processing and deleted automatically within 30 minutes.

## License
This project is licensed under the [MIT License](LICENSE).

You are free to use, modify, and distribute this software for personal or commercial purposes,  
provided that you include the original license file in any redistributed versions.
