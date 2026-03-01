<p align="center">
  <img src="./img.png" alt="Project Banner" width="100%">
</p>

# Endura 🎯

## Basic Details

### Team Name: Quackroach

### Team Members
- Member 1: Shreya Sajalan - Albertian Institute of Science and Technology
- Member 2: Elna Susan - Albertian Institute of Science and Technology

### Hosted Project Link
https://endura-phi.vercel.app/

### Project Description
Endura is a private, encrypted digital legacy platform that helps individuals securely store their financial assets, digital accounts, legal documents, and personal wishes — and ensures they're handed over to the right person at the right time, automatically.

### The Problem statement
In India, millions of families are left in chaos after an unexpected loss — bank accounts, LIC policies, PPF/EPF, and property documents remain unknown or inaccessible to loved ones. With no centralized record and no designated person to act, wealth disappears into paperwork and families are left with confusion instead of closure.

### The Solution
Endura gives users a secure, guided vault to document all their assets, accounts, and final wishes in one place. A trusted executor is assigned in advance but sees nothing while the user is alive. A smart check-in system monitors activity — and only upon verified death is the vault unlocked, delivering a structured PDF report, legacy letters, and a clear action checklist. No chaos. Just closure.

---

## Technical Details

### Technologies/Components Used

**For Software:**
- **Libraries:** Django REST Framework, Axios, Vue Router, Pinia, ReportLab (PDF generation)
- **Tools:** VS Code, Git, Postman, pip, npm
- **Security:** AES Encryption for all vault data, document-verified death confirmation
- **Frontend**: Vue.js
- **Backend**: Django + Django REST Framework
- **Crypto**: Web Crypto API (browser native)
- **Key Derivation**: PBKDF2 (250k+ iterations) or Argon2 (preferred)
- **Encryption Mode**: AES-256-GCM
- **Transport**: HTTPS only


---

## Features

- Encrypted Vault: Store personal info, financial assets, digital accounts, physical assets, legacy letters, and dependent details — all AES encrypted.
- Executor System: Assign one trusted person who has zero vault access while you're alive. They're only notified and granted access after verified death.
- Smart Check-In: Automated 6-month email check-ins. If 3 consecutive reminders go unanswered over 30 days, the executor is alerted.
- Verified Handover: Executor uploads a death verification document. Once confirmed, they receive a structured PDF report, legacy letters, and a step-by-step action checklist.
- Completion Score: A live progress tracker shows users what's filled and what's still missing in their vault.

---

## Implementation

### For Software:

#### Installation
```
# Clone the repository
git clone https://github.com/shreya-sajalan/endura.git
cd endura

# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate

# Frontend setup
cd ../frontend
npm install
```

#### Run
```
# Start Django backend
cd backend
python manage.py runserver

# Start Vue.js frontend (separate terminal)
cd frontend
npm run dev
```

> Backend runs on `http://localhost:8000` | Frontend on `http://localhost:5173`

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

![endura 1](https://github.com/user-attachments/assets/d5f0521f-f037-480f-bcd1-0c65d04edb5c)
![endura 2](https://github.com/user-attachments/assets/230b98dd-71a5-4f83-b48a-50a65a0a7ada)
![endura 3](https://github.com/user-attachments/assets/82469e78-ca48-4318-a0f2-d0114a69ad0e)
![endura 4](https://github.com/user-attachments/assets/cbc6cd0f-5afc-4f54-b7fb-9ad4edffa5d6)
![endura 5](https://github.com/user-attachments/assets/e44fec4a-5db2-440b-ab06-fe1a40689d09)
![endura 6](https://github.com/user-attachments/assets/ab0758d6-93a0-4765-ba53-6b0ece116fbc)
![endura 7](https://github.com/user-attachments/assets/28c6e1f2-d1de-41ad-a186-efbd65c5daba)
![endura 8](https://github.com/user-attachments/assets/707a3497-6a21-42f3-8fad-9a8ecac1fec6)
![endura 9](https://github.com/user-attachments/assets/2295b4fe-8351-4b69-bac5-1dea19964560)
![endura 10](https://github.com/user-attachments/assets/e1f59852-b390-466b-b276-a6f116291b2c)

---

## Additional Documentation

### For Web Projects with Backend:

#### API Documentation

**Base URL:** `http://localhost:8000/api/`

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/auth/register/` | Register a new user |
| `POST` | `/auth/login/` | Authenticate and receive token |
| `GET` | `/vault/` | Fetch the authenticated user's vault |
| `PUT` | `/vault/update/` | Update vault section data |
| `POST` | `/executor/assign/` | Assign a trusted executor |
| `POST` | `/checkin/` | Log a user check-in response |
| `POST` | `/executor/verify/` | Executor submits death verification document |
| `GET` | `/executor/handover/` | Retrieve unlocked vault report (post-verification) |

---
## Project Demo

### Video

https://github.com/user-attachments/assets/53e36349-01c7-44d2-b8c7-f14b007c1ff8

---

## Team Contributions

- Shreya Sajalan:  UI/UX designing and documentation
- Elna Susan: Builded main features like Backend and Frontend
---

Made with ❤️ at TinkerHub
