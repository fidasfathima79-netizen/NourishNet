# NourishNet – Food Donation & Distribution Management System

**NourishNet** is a Django-based web application that connects food donors with NGOs to reduce food waste and improve food distribution. It allows donors to share surplus food and enables NGOs to reserve and collect available donations.

🌐 **Live Demo:** https://fidasfathima12.pythonanywhere.com/  
💻 **GitHub Repository:** https://github.com/fidasfathima79-netizen/NourishNet

---

## Key Features

- User registration, login and logout
- Role-based access control
- Separate dashboards for Admin, Donor and NGO
- Food donation management
- Donation reservation by NGOs
- Donation collection status management
- Search and filter available donations
- Admin user management
- Admin donation and reservation monitoring
- Food donation image uploads
- Responsive user interface

## User Roles

| Role | Permissions |
|---|---|
| Admin | Manage users, monitor donations and reservations, access admin dashboard |
| Donor | Create, view and manage own donations; view reservations |
| NGO | Browse available donations, search and filter, reserve donations and view reservations |

## Screenshots
### Homepage

![NourishNet Homepage](screenshots/homepage.png)

### Login and Registration

![Login Demo](screenshots/login-demo.png)

![Login Empty](screenshots/login-empty.png)

![Registration](screenshots/registration.png)

### Admin Dashboard

![Admin Dashboard](screenshots/admin-dashboard.png)

### Donor Dashboard

![Donor Dashboard](screenshots/donor-dashboard.png)

### NGO Dashboard

![NGO Dashboard](screenshots/ngo-dashboard.png)

### Donation List and Reservation

![Donation List](screenshots/donation-list.png)

![Reservation](screenshots/reservation.png)

## Technologies Used

- **Backend:** Python, Django
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite
- **Image Handling:** Pillow
- **Static Files:** WhiteNoise
- **Deployment:** PythonAnywhere
- **Version Control:** Git and GitHub

## Project Structure

```text
NourishNet/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── migrations/
│   ├── management/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── tests.py
│
├── screenshots/
│   ├── admin-dashboard.png
│   ├── donation-list.png
│   ├── donor-dashboard.png
│   ├── login-demo.png
│   ├── login-empty.png
│   ├── ngo-dashboard.png
│   ├── registration.png
│   └── reservation.png
│
├── static/
├── templates/
├── manage.py
├── requirements.txt
├── build.sh
├── .gitignore
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/fidasfathima79-netizen/NourishNet.git
cd NourishNet
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**Linux / Ubuntu:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create an Admin Account

Create the administrator account using Django's built-in command:

```bash
python manage.py createsuperuser
```

Enter the required username, email address and password when prompted.

### 6. Run the Development Server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

### 7. Create Donor and NGO Accounts

Donor and NGO accounts can be created directly through the website registration page.

1. Open the application.
2. Click **Join NourishNet**.
3. Register as a Donor or NGO.
4. Log in using the registered credentials.

## Demo Login Credentials

The following credentials are for the demo accounts created by the local `seed_demo` command.

| Role | Username | Password |
|---|---|---|
| Admin | admin | sana@5911 |
| Donor | donor@123 | sana@1234# |
| NGO | ngo@123 | sana@123# |

Account Creation:

Admin: Created using Django's createsuperuser command.

Donor: Registered through the website registration page.

NGO: Registered through the website registration page.


## Testing

Run the Django test suite using:

```bash
python manage.py test
```

Check the project configuration using:

```bash
python manage.py check
```

## Deployment

The application is deployed using PythonAnywhere.

**Live Application:** https://fidasfathima12.pythonanywhere.com/

## Future Enhancements

- Email and SMS notifications
- Advanced donation analytics
- Interactive dashboard charts
- Location-based donation discovery
- Food expiry reminders
- Improved reporting features

## Author

**Developed as an academic final project**

**Project:** NourishNet – Food Donation & Distribution Management System  
**Framework:** Django  
**Repository:** [GitHub – NourishNet](https://github.com/fidasfathima79-netizen/NourishNet)  
**Live Demo:** [NourishNet](https://fidasfathima12.pythonanywhere.com/)

---

*Reducing food waste. Connecting communities. Nourishing lives.*
