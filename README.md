# Smart-USB-Forensics-Tool

![image alt](https://github.com/Rishi-0040/Smart-USB-Forensics-Tool/blob/b9b34e2f3fe4134b866e9b9c10c851e4fe62cc80/App_icon.png)

# 🔥 Smart USB Activity Forensics Tool

## AI-Powered USB Threat Detection & Digital Forensics Platform

An advanced cybersecurity and digital forensics project developed using Python that monitors USB activities in real time, collects forensic evidence, detects suspicious behavior using AI/ML, and provides both desktop and web-based threat intelligence dashboards.

---

# 🚀 Features

## 🔍 Real-Time USB Monitoring

* Detects file creation, deletion, and modification events
* Monitors suspicious USB activity automatically

## 🧠 AI-Powered Threat Detection

* Uses Isolation Forest Machine Learning algorithm
* Detects anomalous and suspicious behaviors

## 🔐 SHA256 Forensic Hashing

* Generates cryptographic hashes for evidence integrity verification

## 📊 Threat Intelligence Dashboard

* Displays:

  * High-risk events
  * Dangerous file extensions
  * Threat analytics
  * Event summaries

## 🖥️ Desktop GUI Dashboard

* Built using PyQt5
* Real-time forensic visualization

## 🌐 Web Dashboard

* Flask-based browser monitoring interface
* Login authentication system

## 📁 Device Fingerprinting

* Tracks:

  * USB device name
  * Vendor ID
  * Product ID
  * Trusted device status

## ☁️ SIEM-Compatible Architecture

* Supports JSON exports for:

  * Wazuh
  * Splunk
  * Elastic Stack

---

# 🛠️ Technologies Used

| Technology   | Purpose           |
| ------------ | ----------------- |
| Python       | Core Development  |
| PyQt5        | Desktop GUI       |
| Flask        | Web Dashboard     |
| SQLite       | Database          |
| Watchdog     | File Monitoring   |
| Scikit-learn | Machine Learning  |
| Matplotlib   | Analytics         |
| PyInstaller  | Desktop Packaging |

---

# 📂 Project Structure

```text
Smart-USB-Forensics-Tool/
│
├── gui/
├── forensic/
├── analytics/
├── alerts/
├── database/
├── ml_model/
├── siem/
├── web_dashboard/
├── screenshots/
│
├── README.md
├── requirements.txt
├── usb_forensics.db
```

---

# ▶️ Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/Smart-USB-Forensics-Tool.git
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Desktop Dashboard

```bash
python gui/dashboard.py
```

---

## Run Web Dashboard

```bash
cd web_dashboard

python app.py
```

---

# 📸 Screenshots

(Add screenshots here later)

---

# 🚀 Future Enhancements

* Advanced behavioral AI
* Malware sandbox analysis
* Cloud synchronization
* Multi-system monitoring
* Live websocket updates
* Enterprise SIEM integrations

---

# 👨‍💻 Developer

MSc Digital Forensics and Cybersecurity Student

Project focused on:

* Digital Forensics
* Threat Intelligence
* Cybersecurity Analytics
* AI-based Monitoring

---

# ⭐ Project Goals

This project was developed to explore:

* USB forensic investigations
* AI-driven threat detection
* Threat intelligence visualization
* Security event monitoring
* DFIR workflows

---

# 📜 License

MIT License
