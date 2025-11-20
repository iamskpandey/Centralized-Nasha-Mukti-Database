# Centralized Nasha Mukti Database

Centralized Nasha Mukti Database is a Django-based web application that collects, organizes, and exposes information about addiction-recovery (nasha mukti) centers, resources, and related services. The project provides a simple interface to add, search, and manage records so stakeholders can find support services more easily.

Key features

- Centralized listing of recovery centers and resources
- Create, read, update, and delete (CRUD) operations for records
- Search and filtering of entries (name, location, service type)
- Simple, responsive HTML/CSS frontend powered by Django views and templates

Tech stack

- Python, Django
- HTML, CSS
- SQLite (default) or other Django-supported databases

Getting started (local development)

1. Clone the repository:

   git clone https://github.com/iamskpandey/Centralized-Nasha-Mukti-Database.git
   cd Centralized-Nasha-Mukti-Database

2. Create and activate a virtual environment:

   python -m venv venv
   source venv/bin/activate   # macOS / Linux
   venv\Scripts\activate    # Windows

3. Install dependencies:

   pip install -r requirements.txt

4. Apply migrations and create a superuser:

   python manage.py migrate
   python manage.py createsuperuser

5. Run the development server:

   python manage.py runserver

Open http://127.0.0.1:8000/ in your browser.

Notes

- If requirements.txt is missing, install Django and other dependencies manually (e.g., pip install django).
- Adjust database settings in settings.py for production use.

Contributing

Contributions are welcome. Please open an issue to discuss major changes or submit a pull request with clear commit messages and tests where applicable.

License

If this repository already contains a LICENSE file, refer to it for licensing details. If there is no license, all rights are reserved by the repository owner.

Contact

Created and maintained by @iamskpandey. For questions or help, open an issue or contact the maintainer.