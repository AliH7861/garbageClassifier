**EcoBin AI**
=============

**Description**
---------------

**EcoBin AI** is a smart web application that helps you classify household waste using AI. Simply sign up, upload any image, and our ResNet50 deep learning model predicts the correct Durham Region bin (e.g., Green Bin, Blue Box, Garbage). Your personal dashboard updates in real time—track all submissions, fully customize bins (images & names), get analytics, and revert to official defaults with one click.

**Table of Contents**
---------------------

*   [Features](#features)
    
*   [Getting Started](#getting-started)
    
*   Usage
    
*   Configuration
    
*   Tech Stack
    
*   Contributing
    
*   Testing
    
*   FAQ
    
*   License
    
*   Contact
    

**Features**
------------

*   **Bin Prediction:**Instantly predicts which Durham Region bin (Green Bin, Blue Box, Garbage, etc.) your item belongs to.
    
*   **Customizable Bins:**Swap default bin images/names with your own for a personalized experience. Revert to official bins anytime.
    
*   **Live Dashboard:**Updates with every submission. Shows:
    
    *   Last 7 submissions (with image previews)
        
    *   Pie chart: today’s classified bins
        
    *   Bar chart: bin/submission counts for today
        
    *   Most common bin (today & all-time)
        
    *   Total scan count (today & all-time)
        
*   **User Accounts:**Sign up, log in/out. Each user’s submissions & bin settings are separate and private.
    

**Getting Started**
-------------------

### **Prerequisites**

*   Python 3.8+
    
*   [PostgreSQL](https://www.postgresql.org/)
    
*   pip (Python package manager)
    

### **Installation**

1.  bashCopyEditgit clone https://github.com/yourusername/ecobin-ai.gitcd ecobin-ai
    
2.  bashCopyEditpip install -r requirements.txt
    
3.  **Set up environment variables:**
    
    *   Copy .env.example to .env
        
    *   Fill in DATABASE\_URL (your PostgreSQL URI) and any other required variables
        
4.  **Prepare the database:**
    
    *   Create a new PostgreSQL database
        
    *   Run migration scripts (if provided), or let SQLAlchemy auto-create tables on first run
        
5.  bashCopyEditstreamlit run dashboard.py# ORpython main.py
    

**Usage**
---------

1.  **Sign up or log in.**
    
2.  **Upload an image** of your waste item for an instant bin recommendation.
    
3.  **Edit your bins:**
    
    *   Change names/images to fit your home
        
    *   Revert to Durham Region defaults anytime
        
4.  **Visit your dashboard:**
    
    *   See recent submissions, analytics, and personalized charts
        
5.  **Privacy:**
    
    *   Your submissions & customizations are private and visible only to you
        

**Configuration**
-----------------

*   **Bins:**Default bins match Durham Region categories. You can upload your own images and rename bins at any time.
    
*   **Environment Variables:**
    
    *   DATABASE\_URL (PostgreSQL) **required**—set this in your .env file.
        
*   **Data Storage:**
    
    *   User accounts, submissions, and analytics are stored securely in PostgreSQL.
        
    *   Uploaded images are processed and deleted after 30 minutes for privacy.
        

**Tech Stack**
--------------

*   **Backend:** Python, FastAPI, SQLAlchemy
    
*   **AI Model:** ResNet50 (TensorFlow)
    
*   **Frontend/UI:** Streamlit, HTML, CSS, JavaScript
    
*   **Database:** PostgreSQL
    
*   **Dev Environment:** Jupyter Notebook
    

**Contributing**
----------------

We welcome all contributions!

1.  **Fork the repository**
    
2.  bashCopyEditgit checkout -b feature/your-feature
    
3.  bashCopyEditgit commit -am "Add new feature"
    
4.  bashCopyEditgit push origin feature/your-feature
    
5.  **Open a Pull Request** and describe your changes.
    

**Testing**
-----------

Automated and manual tests for major features are included.

To run tests:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   bashCopyEditpytest   `

See the /tests folder for details or add your own tests!

**FAQ**
-------

**Q: What if my item isn’t recognized?**A: You can re-upload, choose the closest bin, or request more bins in future releases.

**Q: Can I reset my custom bins?**A: Yes—just click “Revert to Defaults” in your dashboard.

**Q: Are my uploads private?**A: Yes. All uploads and analytics are visible only to your account. Images are deleted after 30 minutes.

**Q: Can I use EcoBin AI outside Durham Region?**A: Yes! You can fully customize bin names and images to fit any local waste system.

**License**
-----------

This project is licensed under the MIT License. See LICENSE for details.

**Contact**
-----------

For questions, bug reports, or feature requests:

*   **Email:** alihusen2k27@gmail.com
    
*   **GitHub Issues:** [Open an issue](https://github.com/yourusername/ecobin-ai/issues)
    

_EcoBin AI – Smarter, Greener, Cleaner!_