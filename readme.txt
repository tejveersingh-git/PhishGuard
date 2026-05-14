PROJECT: PhishGuard — A Machine Learning Based Phishing Website Detection System
STUDENT: Tejveersingh Pathi
REG NO:  2022BCS128
GUIDE:   Prof. S.M. Bansode
COLLEGE: SGGSIET Nanded, Dept. of CSE
YEAR:    2025-26

HOW TO RUN:
1. Install Python 3.10 or above
2. Open terminal in the backend/ folder
3. Run: pip install -r requirements.txt
4. Run: python model_train.py   (only once — generates model.pkl)
5. Run: python app.py           (keep this terminal open)
6. Open Chrome → go to chrome://extensions
7. Enable Developer Mode (top right toggle)
8. Click Load Unpacked → select the extension/ folder
9. Click the PhishGuard icon in the toolbar to use

## Live Demo

Frontend:
phish-guard-git-main-tejveersingh-gits-projects.vercel.app
Backend API:
https://phishguard-3jam.onrender.com

WEBSITE:
Open website/index.html directly in Chrome

OUTPUTS:
See the outputs/ folder for screenshots and accuracy results

ACCURACY: 97.3% test accuracy, 97.1% cross-validated accuracy
DATASET:  UCI Phishing Websites Dataset — 11,055 URLs, 30 features

# PhishGuard 🛡️

PhishGuard is a real-time phishing website detection system powered by Machine Learning.

It uses a Random Forest classifier trained on the UCI Phishing Websites Dataset to classify URLs as safe or phishing in real time.

## Features

- Real-time phishing detection
- Chrome Extension support
- Flask REST API
- Feature extraction pipeline
- Confidence score prediction
- Website interface
- Zero-day phishing detection

## Tech Stack

- Python
- Flask
- Scikit-learn
- BeautifulSoup
- JavaScript
- Chrome Extension (Manifest V3)

## Model Performance

- Accuracy: 97.3%
- Cross Validation: 97.1%
- Random Forest Classifier

## System Architecture

[Add architecture screenshot here]

## Installation

```bash
pip install -r requirements.txt
python app.py

Future Scope
QR code phishing detection
Mobile app support
Federated learning
PhishTank API integration
