

---

Django Project with TailwindCSS

This project is a Django-based web application styled with TailwindCSS. Below are the steps to set up the project on your local machine, including the installation of all necessary dependencies using package.json and setting up a Python virtual environment.

Prerequisites

Make sure you have the following installed:

Python 3.x: Python Installation Guide

Node.js: Node.js Installation Guide

npm (comes with Node.js): Ensure you have npm for managing the frontend dependencies.


Setting Up the Project

1. Clone the Repository

git clone <your-repo-url>
cd <your-project-directory>

2. Set Up Python Virtual Environment

It's recommended to use a virtual environment to manage your Python dependencies.

Create and activate the virtual environment:

On Windows:

python -m venv venv
venv\Scripts\activate

On macOS/Linux:

python3 -m venv venv
source venv/bin/activate


3. Install Python Dependencies

Once the virtual environment is activated, install the Python dependencies listed in requirements.txt:

pip install -r requirements.txt

4. Install Node.js and TailwindCSS Dependencies

After the Python dependencies are installed, run the following command to install the JavaScript dependencies (TailwindCSS and others):

npm install

This will read the package.json file and install the required frontend dependencies.

5. Run TailwindCSS (optional)

To start TailwindCSS and watch for changes in your CSS files, run:

npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

Make sure to adjust the paths according to your project's directory structure.

6. Apply Migrations

Make sure the database is up-to-date by applying migrations:

python manage.py migrate

7. Create a Superuser

To access the Django admin interface, create a superuser:

python manage.py createsuperuser

Follow the prompts to set up the superuser.

8. Run the Development Server

Now you can run the Django development server:

python manage.py runserver

Visit http://127.0.0.1:8000/ in your browser to see the project in action.

Additional Information

Static Files: Make sure to run python manage.py collectstatic if deploying to production.

Environment Variables: Remember to set up any environment variables (such as for the database or secret keys) in a .env file.


License

This project is licensed under the MIT License.


---

