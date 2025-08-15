<p align="center">
  <img src="https://yourdomain.com/static/icons/snapvibe-logo.png" alt="SnapVibe Logo" width="150"/>
</p>

<h1 align="center">SnapVibe</h1>
<p align="center"><em>Capture. Share. Connect.</em></p>

---

## 🚀 Overview
**SnapVibe** is a **Flask-based social media platform** that lets users **share videos, images, and stories**, connect with others, and interact through **likes, follows, and notifications** — all powered by **Firebase real-time features**.

With **SnapVibe**, you can upload your favorite moments, follow your friends, and enjoy a smooth, modern interface inspired by today’s leading social apps.

---

## ✨ Features

- 👤 **User Authentication** – Secure registration and login via Firebase.  
- 🖼 **Media Uploads** – Share videos and images with ease.  
- 📚 **Stories System** – Upload and view time-limited stories.  
- 🔔 **Real-Time Notifications** – Stay updated instantly.  
- 🤝 **Follow/Unfollow System** – Connect with friends and creators.  
- 💾 **Save Posts & Likes** – Keep your favorite content.  
- 📱 **Responsive Design** – Works on desktops, tablets, and smartphones.  

---

## 🛠 Technologies Used

- **Frontend:** HTML, CSS, Tailwind CSS, JavaScript  
- **Backend:** Python (Flask)  
- **Database & Authentication:** Firebase Realtime Database + Firebase Authentication  

---

## 📷 SnapVibe Screenshots  

<p>
  <a href="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/1.png" target="_blank" rel="noopener noreferrer">
    <img src="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/1.png" alt="SnapVibe Image 1" width="400" style="margin-right:10px;" />
  </a>
  <a href="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/2.png" target="_blank" rel="noopener noreferrer">
    <img src="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/2.png" alt="SnapVibe Image 2" width="400" style="margin-right:10px;" />
  </a>
  <a href="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/3.png" target="_blank" rel="noopener noreferrer">
    <img src="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/3.png" alt="SnapVibe Image 3" width="400" style="margin-right:10px;" />
  </a>
  <a href="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/4.png" target="_blank" rel="noopener noreferrer">
    <img src="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/4.png" alt="SnapVibe Image 4" width="400" />
  </a>
  <a href="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/5.png" target="_blank" rel="noopener noreferrer">
    <img src="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/5.png" alt="SnapVibe Image 5" width="400" />
  </a>
  <a href="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/6.png" target="_blank" rel="noopener noreferrer">
    <img src="https://raw.githubusercontent.com/Abdullah9779/flask-projects/refs/heads/main/SnapVibe%20-%20Social%20Media%20Web%20App/Snapvibe%20Screenshorts/6.png" alt="SnapVibe Image 6" width="400" />
  </a>
</p>

---

# 📜 SnapVibe Firebase Realtime Database Rules

```json
{
  "rules": {
    "users": {
      "$userId": {
        ".read": "auth != null",
        ".write": "auth != null"
      }
    },
    "usernames": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "saved_posts": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "notifications": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "is_new_notification": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    "posts": {
      ".read": "auth != null",
      ".write": "auth != null"
    },
    ".read": "auth != null",
    ".write": "auth != null"
  }
}
```

---

## ⚙️ Configuration Files

### `config.json`

This file contains the Firebase configuration for your SnapVibe client-side application. It includes your app's API keys and identifiers needed to initialize Firebase services like Authentication, Firestore, or Storage.

Example structure:

```json
{
  "apiKey": "YOUR_API_KEY_HERE",
  "authDomain": "your-app.firebaseapp.com",
  "projectId": "your-app",
  "storageBucket": "your-app.appspot.com",
  "messagingSenderId": "YOUR_SENDER_ID",
  "appId": "YOUR_APP_ID"
}
```

### `adminsdk.json`

This file contains the Firebase Admin SDK service account credentials. It is used on your backend server to securely authenticate and interact with Firebase services with full administrative privileges.

> **Warning:** This file holds sensitive private keys. Never expose it publicly or commit it to public repositories.

Example structure:

```json
{
  "type": "service_account",
  "project_id": "snapvibe-demo",
  "private_key_id": "abcdef1234567890abcdef1234567890abcdef12",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEv...YourPrivateKeyHere...IDAQAB\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-demo@snapvibe-demo.iam.gserviceaccount.com",
  "client_id": "123456789012345678901",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-demo%40snapvibe-demo.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
```

## 🌐 Live Deployment Note

Replace all static file URLs like:  
`https://snapvibe.share.zrok.io/static/.....`  
with your own domain:  
`https://yourdomain.com/static/.....`  
This change must be done throughout the project to ensure proper functionality.

---

**LICENSE:** [MIT License](https://github.com/Abdullah9779/flask-projects/blob/main/LICENSE)

