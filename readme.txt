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

WEBSITE:
Open website/index.html directly in Chrome

OUTPUTS:
See the outputs/ folder for screenshots and accuracy results

ACCURACY: 97.3% test accuracy, 97.1% cross-validated accuracy
DATASET:  UCI Phishing Websites Dataset — 11,055 URLs, 30 features