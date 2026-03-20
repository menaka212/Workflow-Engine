# 🚀 FlowX - Workflow Automation Engine

FlowX is a dynamic workflow automation system built using Django. It allows users to create, manage, and execute workflows with conditional logic, approvals, and execution tracking.

---

## 🔥 Features

- ✅ Create custom workflows
- ✅ Add multiple steps (Task / Approval)
- ✅ Define conditional rules (dynamic decision engine)
- ✅ Execute workflows with real-time input
- ✅ Automatic rule evaluation
- ✅ Approval-based flow pause
- ✅ Execution logs with timeline view
- ✅ Admin panel for managing workflows
- ✅ Search functionality

---

## 🧠 How It Works

1. Create a workflow  
2. Add steps with order  
3. Define rules between steps  
4. Set start step  
5. Execute workflow with input data  
6. System evaluates rules and moves through steps  
7. Logs are generated for each execution  

---

## 📂 Project Structure
# 🚀 FlowX - Workflow Automation Engine

FlowX is a dynamic workflow automation system built using Django. It allows users to create, manage, and execute workflows with conditional logic, approvals, and execution tracking.

---

## 🔥 Features

- ✅ Create custom workflows
- ✅ Add multiple steps (Task / Approval)
- ✅ Define conditional rules (dynamic decision engine)
- ✅ Execute workflows with real-time input
- ✅ Automatic rule evaluation
- ✅ Approval-based flow pause
- ✅ Execution logs with timeline view
- ✅ Admin panel for managing workflows
- ✅ Search functionality

---

## 🧠 How It Works

1. Create a workflow  
2. Add steps with order  
3. Define rules between steps  
4. Set start step  
5. Execute workflow with input data  
6. System evaluates rules and moves through steps  
7. Logs are generated for each execution  

---

## 📂 Project Structure
# 🚀 FlowX - Workflow Automation Engine

FlowX is a dynamic workflow automation system built using Django. It allows users to create, manage, and execute workflows with conditional logic, approvals, and execution tracking.

---

## 🔥 Features

- ✅ Create custom workflows
- ✅ Add multiple steps (Task / Approval)
- ✅ Define conditional rules (dynamic decision engine)
- ✅ Execute workflows with real-time input
- ✅ Automatic rule evaluation
- ✅ Approval-based flow pause
- ✅ Execution logs with timeline view
- ✅ Admin panel for managing workflows
- ✅ Search functionality

---

## 🧠 How It Works

1. Create a workflow  
2. Add steps with order  
3. Define rules between steps  
4. Set start step  
5. Execute workflow with input data  
6. System evaluates rules and moves through steps  
7. Logs are generated for each execution  

---

## 📂 Project Structure
workflow_engine/
│
├── engine/
│ ├── models.py
│ ├── views.py
│ ├── services.py
│ ├── templates/
│ ├── forms.py
│
├── templates/
├── static/
├── db.sqlite3
├── manage.py


---

## ⚙️ Technologies Used

- Python 🐍
- Django 🌐
- SQLite 🗄️
- HTML, CSS, Bootstrap 🎨

---

## 🔄 Workflow Examples

### 1️⃣ Job Application Workflow
- Experience-based filtering  
- HR approval step  

### 2️⃣ Loan Approval Workflow
- Credit score validation  
- Approval / Rejection flow  

### 3️⃣ Fraud Detection Workflow ⭐
- Amount-based risk analysis  
- Country-based validation  
- Manual review for suspicious cases  

---

## 🧪 Sample Inputs

### Fraud Detection Workflow
amount = 15000
country = India


👉 Output:
- Risk Analysis → Manual Review  

---

## 📊 Execution Logs

- Displays step-by-step execution
- Shows rule evaluation results
- Tracks workflow path

---

## 🔐 Admin Panel

Access admin panel:
/admin/


Manage:
- Workflows
- Steps
- Rules
- Executions

---

## 🚀 Deployment

Deployed using **Render**

👉 Live URL:  

 https://workflow-engine-adeg.onrender.com
---
## Screenshots

## 🛠️ Setup Instructions

```bash
git clone https://github.com/your-username/your-repo-name.git
cd workflow_engine
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
⭐ Conclusion

FlowX demonstrates a rule-based workflow engine capable of handling real-world automation scenarios with flexibility and scalability.


---
🎯 Future Enhancements

🔄 Drag & Drop Workflow Builder

🤖 AI-based rule suggestion

📊 Analytics Dashboard

📩 Notification system

👨‍💻 Author

Menaka Manavalan
# 🚀 EXTRA FILES (IMPORTANT FOR RENDER)

## ✅ requirements.txt

Make sure you have:


Django
gunicorn
whitenoise


---

## ✅ build.sh (for Render)

Create file:

```bash
#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
✅ Procfile
web: gunicorn workflow_engine.wsgi
