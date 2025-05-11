# AppVendasAndroid

A **mobile-first sales management app** built with **Python, Kivy/KivyMD, and Firebase**.  
AppVendasAndroid lets individual sellers record sales, track their performance, and gives managers a real-time view of overall company revenue—all from an Android device (or any desktop that can run Kivy).

---
## ✨ Core features

| Area | Functionality |
|------|---------------|
| **Authentication** | 🔐 Email/Password sign-in & persistent sessions via Firebase Refresh Tokens |
| **Sales capture**  | 📝 Register new sales with amount, product, client, and optional notes |
| **Personal dashboard** | 📊 View your total sales and recent transactions |
| **Company dashboard**  | 💼 Aggregate sales metrics across all sellers |
| **Team monitor**  | 👀 Lookup other sellers by unique ID to compare performance |
| **Profile** | 🖼️ Update avatar, change password, tweak preferences |
| **Offline-aware UI** | 🔄 Local state caching & graceful error alerts when connectivity drops |

---
## 🗂️ Project layout

```
appvendasandroid/
├─ kv/                  # .kv layout files (one per Screen)
│   ├─ loginpage.kv
│   ├─ homepage.kv
│   └─ ...
├─ icones/              # PNG/JPG assets used by the UI
│   ├─ logo.png
│   └─ ...
├─ botoes.py            # Reusable KivyMD button classes
├─ bannervenda.py       # Widget that renders a single sale card
├─ bannervendedor.py    # Widget that renders a seller card
├─ telas.py             # All Screen classes & navigation logic
├─ main.kv              # Root KV file that wires ScreenManager + global styles
├─ myfirebase.py        # Tiny wrapper around Pyrebase v3 for auth & DB ops
├─ main.py              # App entry-point
└─ refreshtoken.txt     # Stores the Firebase refresh token (auto-generated)
```

---
## 🚀 Getting started

### 1. Clone & install deps
```bash
git clone https://github.com/pcarpes/appvendasandroid.git
cd appvendasandroid
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt  # Kivy, KivyMD, Pyrebase, requests, etc.
```

### 2. Configure Firebase
1. Create a project at <https://console.firebase.google.com>.
2. Enable **Email/Password** sign-in under **Authentication → Sign-in method**.
3. Create a **Realtime Database** (or Firestore) in *test mode*.
4. Copy your **API key**, **project URL**, and **storage bucket**.
5. Open `myfirebase.py` and paste the values in the `firebaseConfig` dict.

> **Never commit secrets!** Consider using environment variables or `dotenv` in production.

### 3. Run on desktop
```bash
python main.py
```
The Kivy window should open; log in with a user created in Firebase Auth to explore the app.

### 4. Build the Android APK (optional)
```bash
# Inside WSL or a Linux host
pip install buildozer cython
buildozer init          # generates buildozer.spec
buildozer -v android debug
# The unsigned APK will be in bin/AppVendasAndroid-0.1-debug.apk
```
For detailed instructions see the [Buildozer docs](https://buildozer.readthedocs.io).

---
## 🧩 Tech stack
* **Python 3.11**
* **Kivy** & **KivyMD** for the UI layer
* **Firebase** (Authentication + Realtime Database + Storage)
* **Pyrebase** for Firebase REST calls
* **Buildozer** & **Gradle** for Android packaging

---
## 🛠️ Extending the app
* **Switch to Firestore** – swap the REST endpoints in `myfirebase.py`.
* **Add product images** – use Firebase Storage and store the download URL with each sale.
* **Offline sync** – integrate `kivy.storage.jsonstore` for local queuing.
* **Dark mode** – add a secondary KivyMD theme and expose a toggle in Settings.

---
## 🗒️ Roadmap
- [ ] Unit tests with `pytest` + `pytest-mock`
- [ ] CI workflow (GitHub Actions) that lints and runs tests
- [ ] Internationalisation (i18n) for 🇧🇷🇨🇦 Portuguese & English
- [ ] Push notifications when a seller beats their monthly target

---
## 🤝 Contributing
Pull requests are welcome! Please open an issue first to discuss your proposed change.

1. Fork the repo & create your branch: `git checkout -b feature/awesome`  
2. Commit your changes: `git commit -m 'Add some awesome'`  
3. Push to the branch: `git push origin feature/awesome`  
4. Open a PR.

Be sure to run `flake8 .` and keep commits granular.

---
## 📜 License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
