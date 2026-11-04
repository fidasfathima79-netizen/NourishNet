# NourishNet –  Food Donation & Distribution Management System

A Django web application that connects **food donors** with **NGOs / food banks** so surplus food reaches people in need instead of going to waste. Donors list surplus food (quantity, type, location, use-by time); NGOs search and reserve it; administrators oversee everything from a central dashboard.

## Features

| Guideline requirement | Implementation |
|---|---|
| User authentication | Register, login, logout (custom `User` model) |
| Role-based access control | **Admin**, **Donor** (staff-level: manages own records), **NGO** (customer-level: browses and reserves) |
| CRUD | Donations: create, view, edit, delete (donor-owned) |
| Database + migrations + foreign keys | SQLite; `Donation.donor → User`, `Reservation.ngo → User`, `Reservation.donation ↔ Donation` |
| Reports / dashboard | Separate Admin, Donor and NGO dashboards with live statistics |
| Responsive UI | HTML, CSS, Bootstrap 5, media queries |
| Django admin | `User`, `Donation`, `Reservation` registered |
| Search | NGO dashboard search by food / location / donor, plus food-type filter |
| File uploads | Food photo upload on donations |
| REST-style API | `GET /api/donations/?q=&food_type=` (JSON; NGO and Admin only) |

### Roles

| Role | Can do |
|---|---|
| **Admin** | Manage users (activate/deactivate), view all donations and reservations, admin dashboard, Django admin panel |
| **Donor** | Create, edit and delete own donations, view reservations, mark pickups as collected |
| **NGO** | Search available donations, reserve them, track own reservations |

All protected pages require login, and Admin-only pages are restricted by role.

## Project structure

```
nourishnet/
├── manage.py
├── requirements.txt
├── build.sh              # deployment build script (Render)
├── config/               # settings.py, urls.py, wsgi.py, asgi.py
├── core/                 # models, views, forms, urls, admin, migrations
│   └── management/commands/seed_demo.py
├── templates/            # accounts/, admin/, donor/, ngo/, donations/
├── static/               # css, images
└── media/                # uploaded food images (not committed)
```

## Setup (local)

```bash
git clone <your-github-repo-url>
cd nourishnet

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py seed_demo      # creates the demo accounts below
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Login credentials (created by `seed_demo`)

| Role | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin@12345` |
| Donor | `demo_donor` | `Donor@12345` |
| NGO | `demo_ngo` | `Ngo@12345` |

The Django admin panel is at `/admin/` (use the `admin` account).
Change these passwords before using the app with real data.

## Commands

```bash
python manage.py runserver        # run the development server
python manage.py migrate          # apply migrations
python manage.py seed_demo        # create/reset demo accounts
python manage.py test             # run the tests
python manage.py createsuperuser  # optional: create another admin
```

## Deployment (PythonAnywhere)

1. Push the project to GitHub.
2. Log in to PythonAnywhere.
3. Open a Bash console.
4. Clone the GitHub repository.
5. Create a Python virtual environment.
6. Install dependencies using `pip install -r requirements.txt`.
7. Configure the Django web app using Manual Configuration.
8. Configure environment variables and static files.
9. Run database migrations and create an administrator.
10. Reload the web application.

## Submission

- GitHub link: _add here_
- Deploy link: _add here_
