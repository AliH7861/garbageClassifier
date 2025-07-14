# EcoBin AI

## Description
EcoBin AI is a smart web application where users can sign up, log in, and use a powerful AI (ResNet50 deep learning model) to classify household waste. Upload any image, and the AI predicts the correct Durham Region bin. The dashboard updates in real-time, tracking all user submissions. Users can customize default bins (with their own pictures and names), see their personal analytics, and revert to original bin images whenever they want.

---

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

---

## Features

- **Bin Prediction:** Get instant output of which bin (e.g., Green Bin, Blue Box, Garbage) your scanned item belongs to.
- **Customizable Bins:** Change default Durham Region bins to your own custom bins (names & pictures). Easily revert back if needed.
- **Live Dashboard:** Dashboard updates with every submission—showing:
  - Last 7 submissions (visualized)
  - Pie chart of today’s classes and bins
  - Bar graph of bins/submissions for today
  - Most common bin (all-time & today)
  - Total scan count (today/all-time)
- **User Accounts:** Sign up, log in/out, and get a personalized dashboard for each user.

---

## Getting Started

1. **Clone the repository:**  
   ```bash
   git clone https://github.com/yourusername/ecobin-ai.git
   cd ecobin-ai
