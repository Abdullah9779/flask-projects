# 📸 SnapVide – Flask Social Video Sharing Web App

SnapVide is a feature-rich **Flask-based social media platform** where users can register, upload videos or images, view stories, follow other users, and interact through likes and notifications — inspired by modern social apps.

> 🔐 Firebase is used for **authentication, database**, and **real-time features**.

---

## 🚀 Features

- User registration and login  
- Profile editing with profile image  
- Image and video post uploads  
- Stories system (view/upload)  
- Real-time notifications  
- Follow/unfollow system  
- Save posts and view likes  
- Firebase-powered backend
- and more

---

## 🌐 Live Deployment Note

Replace all static file URLs like:  
`https://snapvibe.share.zrok.io/static/.....`  
with your own domain:  
`https://yourdomain.com/static/.....`  
This change must be done throughout the project to ensure proper functionality.

---

## Firebase Rules

Set the following rules in your Firebase Console under Realtime Database → Rules:

```JSON
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

## Firebase Setup

- Replace the **adminsdk.json** file with your own Firebase Admin SDK credentials from the Firebase Console.

- Update the Firebase config object in your **app.py** in line no 24 with your Firebase project details.

