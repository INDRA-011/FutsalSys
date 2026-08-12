# Futsal Booking System

Django app where players request futsal court bookings and a manager approves or rejects them.

## Setup (everyone runs this after cloning)

```bash
git clone <your-github-repo-url>
cd FutsalSys

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# generate a key and paste into .env as SECRET_KEY=...
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

python manage.py migrate
python manage.py createsuperuser
python manage.py seed_slots
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`. Register a player account, or log in with your superuser as manager.

**Note:** Login uses email, not username.

## Branches

| Branch | Owner | Files | Task |
|---|---|---|---|
| `feature/browse-slots` | | `bookings/views.py` (browse_slots, request_booking), `templates/bookings/player_home.html` | Player browses & requests slots |
| `feature/my-bookings` | | `bookings/views.py` (my_bookings, cancel_booking), `templates/bookings/my_bookings.html` | Player views/cancels own bookings |
| `feature/manager-dashboard` | | `bookings/views.py` (manager_dashboard, approve_booking, reject_booking), `templates/bookings/manager_dashboard.html` | Manager approves/rejects |
| `feature/all-bookings-polish` | | `bookings/views.py` (all_bookings), `templates/bookings/all_bookings.html`, `static/css/style.css` | History view + styling |

Each view function has a `TODO` docstring. Don't edit `urls.py` or `models.py`.

## Git workflow

```bash
git checkout main
git pull origin main
git checkout -b feature/your-branch-name
# ...work...
git add .
git commit -m "message"
git push origin feature/your-branch-name
```
Then open a Pull Request into `main` on GitHub.