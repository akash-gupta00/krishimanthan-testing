# Krishi Manthan — Backend (Django + DRF + PostgreSQL)

Full backend powering the Krishi Manthan agriculture portal. Every piece of
content that used to be hardcoded in the React frontend (news, schemes,
events, resources, ads, announcements, market prices, weather, FAQs,
testimonials, about page, e-paper, site settings, contact/subscribe forms)
is now stored in PostgreSQL and managed from the Django Admin panel.

## Stack

- Python 3.12, Django 5, Django REST Framework
- PostgreSQL 16
- JWT auth (djangorestframework-simplejwt) for the API + Django's built-in
  session auth for the Admin panel
- drf-spectacular → Swagger UI (`/api/docs/`) and Redoc (`/api/redoc/`)
- django-cors-headers, django-filter, Pillow, Whitenoise, Gunicorn
- django-jazzmin — modern, clean, responsive Django Admin theme (no extra setup needed, just `pip install`)

## Project layout

```
config/            settings, root urls, api v1 url aggregator
apps/
  core/             shared abstract models (TimeStamped, Publishable, SEO) + seed_data command
  accounts/         custom User model + JWT login/refresh/me
  sitesettings/     singleton — site identity, contact, social, SEO defaults
  departments/      Agriculture / Cooperation / Panchayat / Forest / Animal Husbandry
  news/             NewsCategory + NewsItem
  schemes/          government schemes
  events/           events — "upcoming" is computed automatically from event_date
  resources/        downloadable PDFs/guides
  ads/              AdSlot + Advertisement (public submission -> admin approval workflow)
  announcements/    top-bar ticker + sidebar govt. announcement widget
  market/           mandi/market prices
  weather/          live weather (OpenWeatherMap) with DB fallback, cached 30 min
  contact/          contact form -> DB + email notification
  subscribers/      newsletter subscribers
  faqs/             FAQ
  testimonials/     testimonials
  about/            About page intro + 3 highlight cards
  epaper/           e-paper issues (PDF + thumbnail)
  searchapi/        unified /api/v1/search/?q= across news/schemes/events/resources
  llmintegration/   provider-agnostic LLM service (Anthropic/OpenAI/None) — scaffold for future AI features
seed_media/         real images/PDF bundled so `seed_data` never leaves the site blank
```

## Setup

```bash
# 1. Create & activate a virtualenv
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# edit .env — at minimum set DJANGO_SECRET_KEY and DATABASE_URL

# 4. Create the PostgreSQL database (adjust to your local setup)
sudo -u postgres psql -c "CREATE USER krishimanthan WITH PASSWORD 'krishimanthan_dev_pass';"
sudo -u postgres psql -c "CREATE DATABASE krishimanthan_db OWNER krishimanthan;"

# 5. Migrate + seed real content so the site isn't blank
python manage.py migrate
python manage.py seed_data

# 6. Create an admin user
python manage.py createsuperuser

# 7. Run
python manage.py runserver
```

- Admin panel: http://localhost:8000/admin/
- API root (v1): http://localhost:8000/api/v1/
- Swagger UI: http://localhost:8000/api/docs/
- Redoc: http://localhost:8000/api/redoc/
- OpenAPI schema (JSON): http://localhost:8000/api/schema/

## Key API endpoints

| Endpoint | Notes |
|---|---|
| `GET /api/v1/news/` | `?category=<slug>&search=&ordering=-published_date` |
| `GET /api/v1/news/<slug>/` | Full article |
| `GET /api/v1/schemes/` | `?department=<slug>&search=` |
| `GET /api/v1/events/?upcoming=true|false` | `is_upcoming` is computed from today's date |
| `GET /api/v1/resources/` | |
| `GET /api/v1/departments/` | |
| `GET /api/v1/announcements/?placement=ticker|sidebar` | |
| `GET /api/v1/market-prices/` | |
| `GET /api/v1/weather/current/` | Live if `WEATHER_API_KEY` set, else DB fallback |
| `GET /api/v1/ads/?slot=sidebar_top` | Only approved, in-date ads |
| `POST /api/v1/ads/submit/` | Public "Post Your Ads" form — always lands as `pending` |
| `POST /api/v1/contact/` | Contact form → DB + email |
| `POST /api/v1/subscribers/` | Subscribe form |
| `GET /api/v1/faqs/` `GET /api/v1/testimonials/` | |
| `GET /api/v1/about/` | Intro + the 3 highlight cards, one call |
| `GET /api/v1/epaper/` | Latest issue first |
| `GET /api/v1/site-settings/` | Global identity/contact/social/SEO defaults |
| `GET /api/v1/search/?q=` | Unified search across news/schemes/events/resources |
| `GET /api/v1/pages/<slug>/` | Static/legal pages — e.g. `/api/v1/pages/privacy-policy/`, `/api/v1/pages/terms-conditions/` (rich-text, admin-editable) |
| `POST /api/v1/auth/login/` `/refresh/` `/me/` | JWT auth for admin-only endpoints |
| `POST /api/v1/llm/summarize/` `/query/` | Admin-only, scaffold for future AI features |

## Admin roles

`apps.accounts.User.role` — `super_admin`, `content_editor`, `ad_manager`,
`viewer`. Combine with Django's built-in `is_staff`/`is_superuser` and
Groups/Permissions in the Admin panel for fine-grained access control.

## FastAPI migration note

Business logic lives in serializers/services (e.g. `apps/weather/services.py`,
`apps/llmintegration/services.py`), not in views — views stay thin. This
keeps a future Django REST → FastAPI migration mechanical: FastAPI routes
would call the same service functions, and Django's ORM can keep serving
data access even under a FastAPI app if migrated incrementally.

## Security

- Every image/PDF upload (news, schemes, events, ads, resources, e-paper, testimonials, site settings) is validated against its **real file signature** — not just the extension — via `apps/core/validators.py`. A file renamed to `.jpg`/`.pdf` but containing something else (script, executable) is rejected with a 400, both in the Django Admin and via the public "Post Your Ads" API.
- Size caps are enforced per file type (5MB images, 20MB PDFs) plus a hard 25MB request-body cap (`DATA_UPLOAD_MAX_MEMORY_SIZE`).
- `media/.htaccess` denies script execution inside the media folder on Apache/cPanel hosting, as defense-in-depth even if a bad file somehow got past validation.
- Rich text (TinyMCE) fields are sanitized again on the frontend with DOMPurify before rendering, so a compromised admin account or stored-XSS attempt can't inject scripts into visitors' browsers.

## Rich text editing

News article body, scheme benefits/eligibility/process, event descriptions, FAQ answers, the About page intro, and static legal pages all use a TinyMCE editor in the Admin — no code changes needed to format text, add links, or bullet lists.

## Production checklist

- Set `DEBUG=False`, a real `DJANGO_SECRET_KEY`, and proper `ALLOWED_HOSTS`
- Serve `MEDIA_ROOT` from S3/Cloud storage instead of local disk. In DEBUG mode, media (e.g. the e-paper PDF) is exempted from `X-Frame-Options` so it can be embedded in an `<iframe>` on the frontend — nginx/S3 in production won't add that header at all, so no extra config is needed there.
- Put Gunicorn behind Nginx; `whitenoise` already serves static files
- Set a real `CORS_ALLOWED_ORIGINS` (your production frontend domain)
- Configure real SMTP `EMAIL_*` settings for contact-form notifications
