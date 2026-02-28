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
- **Languages:** Python, JavaScript, HTML, CSS
- **Libraries:** Django REST Framework, Axios, Vue Router, Pinia, ReportLab (PDF generation)
- **Tools:** VS Code, Git, Postman, pip, npm
- **Security:** AES Encryption for all vault data, document-verified death confirmation

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
git clone https://github.com/your-username/endura.git
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

![WhatsApp Image 2026-02-28 at 9 39 17 PM (1)](https://github.com/user-attachments/assets/89645d86-5186-4ce9-9cd0-77cd75ad6010)
![WhatsApp Image 2026-02-28 at 9 39 17 PM](https://github.com/user-attachments/assets/e8510cc8-32eb-44e2-88e8-605854af11a5)
![WhatsApp Image 2026-02-28 at 9 39 16 PM (2)](https://github.com/user-attachments/assets/38b325f9-d698-47d1-bd16-672fb59888dc)
![WhatsApp Image 2026-02-28 at 9 39 16 PM (1)](https://github.com/user-attachments/assets/8f93de07-a09f-4129-b5e7-548c5f70df3d)
![WhatsApp Image 2026-02-28 at 9 39 16 PM](https://github.com/user-attachments/assets/13ac82fc-1a30-49f6-82d6-3e26ce9d587e)
![WhatsApp Image 2026-02-28 at 9 39 15 PM (1)](https://github.com/user-attachments/assets/d5c9f4ff-a077-42a7-bd46-8fbe45f72631)
![WhatsApp Image 2026-02-28 at 9 39 15 PM](https://github.com/user-attachments/assets/b68ee457-fa65-4d2c-afbf-cdfd99e745e4)

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

https://github.com/user-attachments/assets/66205ea5-550b-4197-96cb-3369426b0d6f

---

## Team Contributions

- Sherya Shajalan: Builded main features and other features
- Elna Susan: UI/UX designing and basic implementaion of it and other features

---

## License

This project is licensed under the [LICENSE_NAME] License - see the [LICENSE](LICENSE) file for details.

**Common License Options:**
- MIT License (Permissive, widely used)
- Apache 2.0 (Permissive with patent grant)
- GPL v3 (Copyleft, requires derivative works to be open source)

---

Made with ❤️ at TinkerHub
