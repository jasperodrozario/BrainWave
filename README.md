

---

# **A Simple Django Project with TailwindCSS**

This project is a Django-based web application styled with TailwindCSS. You may follow the steps below to run it on your local machine

## **Prerequisites**

Make sure you have the following installed:

- **Python 3.x**
- **Node.js - npm (comes with Node.js), ensure you have it installed for managing the frontend dependencies**

## **Setup Instructions**

### **Step 1: Clone the Repository**
First, clone this repository to your local machine:

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

### **Step 2: Set Up Python Virtual Environment**

It's recommended to use a virtual environment to manage your Python dependencies.

*Create and activate the virtual environment:*

Go to the project's root directory

**On Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```
**On macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Python Dependencies**

Once the virtual environment is activated, install the Python dependencies listed in requirements.txt:

```bash
pip install -r requirements.txt
```

### **4. Install Node.js and TailwindCSS Dependencies**

After the Python dependencies are installed, run the following command to install the JavaScript dependencies (TailwindCSS and others):

```bash
npm install
```

*This will read the package.json file and install the required frontend dependencies.*

### **5. Run TailwindCSS (optional)**

To start TailwindCSS and watch for changes in your CSS files, run:

```bash
npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch
```

*Make sure to adjust the paths according to your project's directory structure.*

### **6. Apply Migrations**

Make sure the database is up-to-date by applying migrations:

```bash
python manage.py migrate
```

### **7. Create a Superuser (optional)**

To access the Django admin interface, create a superuser:

```bash
python manage.py createsuperuser
```
Follow the prompts to set up the superuser.

### **8. Run the Development Server**

Finally, run the Django development server:

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser to see the project in action.

For running the development server on a custom port:

```bash
python manage.py runserver your-custom-port-number
```

---
