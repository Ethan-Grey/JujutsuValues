# Jujutsu Infinite Values

Value hub for the Roblox game **Jujutsu Infinite**. Players can browse trade values for items, titles, game passes, and event exclusives. Only admins can edit data; everyone else has a clean, mobile-friendly viewer inspired by community value sites.

## Features
- Item list with search, filters (category, rarity, type, trend, min/max value), and sorting.
- Detail pages with badges, demand/trend, acquisition source, and notes.
- Responsive UI with Bootstrap + custom styling, ready for mobile.
- Admin-only create/update/delete via Django admin.
- Sample data seeded automatically for a working demo after migrations.

## Project layout
- `values/` – models, views, URLs for the value directory.
- `templates/` – base layout plus list/detail pages.
- `static/` – shared styles.
- `values/migrations/0002_sample_data.py` – demo content.

## Prerequisites
- Python 3.13+ (venv already included at `venv/`).

## Setup & run
From PowerShell:
```pwsh
# inside project root
& ".\venv\Scripts\Activate.ps1"
cd .\JJI
python manage.py migrate   # already run, safe to rerun
python manage.py createsuperuser  # set admin credentials
python manage.py runserver
```
Open http://127.0.0.1:8000/ for the site, http://127.0.0.1:8000/admin/ for admin.

## Admin workflow
- Sign in at `/admin/` with your superuser.
- Manage `Categories` and `Items` (slug auto-fills). Only admins can edit.

## Future scope
- Player trading forums and offers.
- Value history charts and snapshots.
- Authenticated profiles with wishlists/watchlists.
- API endpoints for bots and Discord integrations.

## Notes
- Demo data provides immediate UI proof; replace with live data in admin.
- `ALLOWED_HOSTS` is open for local testing—tighten for production.

