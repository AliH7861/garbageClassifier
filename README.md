# **EcoBin AI** 
## **Description** 
**EcoBin AI** is a smart web application that helps users classify household waste using AI. Sign up to upload any image—our ResNet50 deep learning model instantly predicts the correct Durham Region bin (e.g., Green Bin, Blue Box, Garbage). The real-time dashboard tracks all user submissions, allows for full bin customization (images and names), personal analytics, and one-click reversion to the official defaults. 
## **Table of Contents** 
- Features 
- Getting Started 
- Usage 
- Configuration 
- Tech Stack 
- Contributing 
- Testing 
- FAQ 
- License 
- Contact 
## **Features** 
- **Bin Prediction** 

  ` `Instantly predicts which Durham Region bin your scanned item belongs to (e.g., Green Bin, Blue Box, Garbage, etc.). 

- **Customizable Bins** 

  ` `Swap default bin images and names with your own, for a fully personalized experience. Revert to official bins anytime. 

- **Live Dashboard** 

  ` `The dashboard updates with every submission, showing: 

- Last 7 submissions (with image previews) 
- Pie chart: today’s classified bins 
- Bar chart: bin/submission counts for today 
- Most common bin (today & all-time) 
- Total scan count (today & all-time) 
- **User Accounts** 

  ` `Sign up, log in/out, and enjoy a personalized dashboard. Each user’s submissions and bin settings are kept separate and private. 
## **Getting Started** 
### **Prerequisites** 
- Python 3.8+ 
- [PostgreSQL ](https://www.postgresql.org/)
- pip (Python package manager) 
### **Installation** 
**Clone the repository:**  bash 

CopyEdit 

git clone https://github.com/yourusername/ecobin-ai.git cd ecobin-ai 

 

**Install dependencies:** 

` `bash 

CopyEdit 

pip install -r requirements.txt 

 
2. **Set up environment variables:** 
- Copy .env.example to .env 
- Fill in DATABASE\_URL (your PostgreSQL URI) and any other necessary variables. 
4. **Prepare the database:** 
- Create a new PostgreSQL database. 
- Run the migration scripts if provided, or let SQLAlchemy create tables on first run. 

**Run the application:** 

` `bash CopyEdit 

streamlit run dashboard.py # OR python main.py 


## **Usage** 
1. **Sign up or log in.** 
1. **Upload an image** of your waste item to get an instant bin recommendation. 
1. **View and edit your bins:** 
- Change names and images to fit your home setup. 
- Revert to Durham Region defaults with one click. 
4. **Visit your dashboard:** 
- See recent submissions, analytics, and personalized charts. 
5. **Your data, your way:** 
- All submissions and customizations are private to your account. !
## **Configuration** 
- **Bins:** 

  ` `Default bins match Durham Region weekly categories. You can upload your own images and rename bins at any time. 

- **Environment Variables:** 
- DATABASE\_URL (PostgreSQL) is required. 
- Place all variables in your .env file. 
- **Data Storage:** 
- User accounts, submissions, and analytics are stored securely in PostgreSQL. 
- Uploaded images are processed and deleted after 30 minutes for privacy. 
## **Tech Stack** 
- **Backend:** Python, FastAPI, SQLAlchemy 
- **AI Model:** ResNet50 (TensorFlow) 
- **Frontend/UI:** Streamlit, HTML, CSS, JavaScript 
- **Database:** PostgreSQL 
- **Dev Environment:** Jupyter Notebook 
## **Contributing** 
We welcome contributions of all kinds! 

1\.  **Fork the repository** 

**Create your feature branch:** 

` `bash CopyEdit 

git checkout -b feature/your-feature 2.  

**Commit your changes:** 

` `bash CopyEdit 

git commit -am 'Add new feature' 3.  

**Push to your branch:** 

` `bash 

CopyEdit 

git push origin feature/your-feature 

 
4. **Open a Pull Request** and describe your changes. 
## **Testing **
- Automated and manual tests for major features are included. 

To run tests: 

` `bash CopyEdit pytest 

 
- Check the /tests folder for more info, or add your own tests! 
## **FAQ** 
**Q: What if my item isn’t recognized?** 

` `A: You can re-upload, choose the closest bin, or request more bins in future releases. 

**Q: Can I reset my custom bins?** 

` `A: Yes—there’s a “Revert to Defaults” button in your dashboard. 

**Q: Are my uploads private?** 

` `A: Yes, all uploads and analytics are only visible to your account. Images are deleted after 30 minutes. 

**Q: Can I use EcoBin AI outside Durham Region?** 

` `A: Yes, you can fully customize bin names and images to fit any local waste system. 
## **License** 
This project is licensed under the MIT License. See LICENSE for details. 
## **Contact** 
For questions, bug reports, or feature requests:[ ](https://github.com/yourusername)

- **Email:** alihusen2k27@gmail.com 

*EcoBin AI – Smarter, Greener, Cleaner!* 