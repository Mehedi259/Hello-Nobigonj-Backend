# হ্যালো দেশ (Hello Desh) - Enterprise News Portal & Admin Backend

একটি উচ্চ-ক্ষমতাসম্পন্ন, স্কেলেবল এবং ইন্ডাস্ট্রি স্ট্যান্ডার্ড **Python Django REST Framework (DRF)** এবং **PostgreSQL** ব্যাকএন্ড আর্কিটেকচার। এটি একই সাথে **Hello-Desh-News-Website** (পাঠক পোর্টাল) এবং **Hello-Desh-News-Website-Admin-Dashboard** (সম্পাদনা ও নিয়ন্ত্রণ প্যানেল)-এর সকল ডেটা মডেল, এপিআই ও ফিচার পূর্ণাঙ্গভাবে পরিচালনা করে।

---

## 🏛️ আর্কিটেকচার ও ডোমেন ডিজাইন (Clean Modular Architecture)

প্রকল্পটির কাঠামো একজন সিনিয়র সফটওয়্যার ইঞ্জিনিয়ারের ইন্ডাস্ট্রি বেস্ট প্র্যাকটিস মেনে মডুলার আর্কিটেকচারে তৈরি করা হয়েছে:

```
Hello-Desh-News-Website-Backend/
├── manage.py
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── entrypoint.sh
├── README.md
├── core/                           # গ্লোবাল কনফিগারেশন ও সেটিংস
│   ├── settings/
│   │   ├── base.py                 # কোর সেটিংস (JWT, CORS, Apps, REST Framework)
│   │   ├── development.py          # লোকাল ডেভেলপমেন্ট
│   │   └── production.py           # প্রোডাকশন সিকিউরিটি ও হেডার
│   ├── pagination.py               # মেটাডেটা সহ কাস্টম প্যাজিনেশন
│   ├── exceptions.py               # স্ট্যান্ডার্ডাইজড এরর হ্যান্ডলার
│   └── urls.py                     # গ্লোবাল এপিআই রাউটিং ও Swagger UI
└── apps/
    ├── accounts/                   # ইউজার, রোল (SuperAdmin, Editor, Reporter, Reader), JWT Auth
    ├── categories/                 # সংবাদের ৮টি প্রধান বিভাগ ও কাউন্টার
    ├── authors/                    # সাংবাদিক ও ডেস্ক প্রতিবেদকদের প্রোফাইল
    ├── articles/                   # নিউজ আর্টিকেলস (Hero, Breaking, Featured, Popular, Views Counter)
    ├── comments/                   # পাঠকদের মন্তব্য ও মডারেশন (Approve, Pending, Spam)
    ├── media_library/              # মিডিয়া অ্যাসেট আপলোড ও গ্যালারি ফাইল ম্যানেজমেন্ট
    ├── subscribers/                # নিউজলেটার গ্রাহক ও CSV এক্সপোর্ট
    ├── notifications/              # অ্যাডমিন সিস্টেম নোটিফিকেশনস
    ├── analytics/                  # ড্যাশবোর্ড কেপিআই (KPI), ট্রেন্ড চার্ট ও রিপোর্টস
    └── settings_app/               # সাইট সেটিংস, এসইও (SEO) মেটা ও কন্টাক্ট মেসেজ
```

---

## 🚀 টেকনোলজি স্ট্যাক (Tech Stack)

- **Language:** Python 3.12+ / 3.14+
- **Framework:** Django 5.1 & Django REST Framework (DRF) 3.17
- **Database:** PostgreSQL 16 (psycopg 3) / SQLite (লোকাল কুইক টেস্ট)
- **Authentication:** SimpleJWT (Access + Refresh Token, Token Blacklist)
- **API Documentation:** OpenAPI 3.0 via `drf-spectacular` (Swagger UI & Redoc)
- **Containerization:** Docker & Docker Compose
- **Web Server:** Gunicorn & WhiteNoise

---

## ⚡ দ্রুত শুরু করার নির্দেশিকা (Quickstart)

### অপশন ১: ডকার কম্পোজ দিয়ে চালানো (প্রস্তাবিত)

```bash
# ১. রিপোজিটরি ক্লোন করুন
cd /Users/mehedihasanmridul/Backend/Hello-Desh-News-Website-Backend

# ২. ডকার কন্টেইনার বিল্ড ও রান করুন
docker compose up -d --build

# ৩. এপিআই ডকুমেন্টেশন ব্রাউজ করুন
# Swagger UI: http://localhost:8000/api/docs/
# Redoc: http://localhost:8000/api/redoc/
```

### অপশন ২: লোকাল ভার্চুয়াল এনভায়রনমেন্টে চালানো

```bash
# ১. ভার্চুয়াল এনভায়রনমেন্ট তৈরি ও সক্রিয় করুন
python3 -m venv venv
source venv/bin/activate

# ২. ডিপেন্ডেন্সি ইনস্টল করুন
pip install -r requirements.txt

# ৩. মাইগ্রেশন রান করুন
python manage.py migrate

# ৪. প্রাথমিক ডেমো ডেটা (আর্টিকেল, ক্যাটাগরি, লেখক, মন্তব্য) সিড করুন
python manage.py seed_hellodesh_data

# ৫. ডেভেলপমেন্ট সার্ভার চালু করুন
python manage.py runserver 0.0.0.0:8000
```

---

## 🔐 প্রাক-কনফিগার করা অ্যাডমিন ও ইউজার ক্রেডেনশিয়াল (Default Credentials)

ডেটাবেস সিড করার পর নিচের অ্যাকাউন্টগুলো স্বয়ংক্রিয়ভাবে তৈরি হয়ে যায়:

| ভূমিকা (Role) | ইমেইল (Email) | পাসওয়ার্ড (Password) | সুবিধা |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@hellodesh.com` | `adminpassword123` | ফুল সিস্টেম ও ইউজার কন্ট্রোল, সেটিংস |
| **Editor** | `editor@hellodesh.com` | `editorpassword123` | সংবাদ সম্পাদনা, ক্যাটাগরি ও মন্তব্য অনুমোদন |
| **Reporter** | `reporter@hellodesh.com` | `reporterpassword123` | নতুন সংবাদ ও মিডিয়া আপলোড |

---

## 📡 এপিআই এন্ডপয়েন্ট ক্যাটালগ (API Endpoints Catalogue)

### ১. অথেনটিকেশন ও অ্যাকাউন্টস (`/api/v1/auth/`)
- `POST /api/v1/auth/login/` - ইমেইল ও পাসওয়ার্ড দিয়ে JWT টোকেন গ্রহণ (প্রোফাইল ও রোল রিটার্ন করে)
- `POST /api/v1/auth/token/refresh/` - রিফ্রেশ টোকেন দিয়ে নতুন অ্যাক্সেস টোকেন প্রাপ্তি
- `POST /api/v1/auth/register/` - নতুন রিডার অ্যাকাউন্ট তৈরি
- `GET /api/v1/auth/me/` - বর্তমান লগইনকৃত ইউজারের প্রোফাইল
- `GET /api/v1/auth/users/` - অ্যাডমিনদের জন্য টিম মেম্বারদের তালিকা ও ব্যবস্থাপনা
- `GET /api/v1/auth/activities/` - সাম্প্রতিক সিস্টেম অ্যাক্টিভিটি লগ

### ২. সংবাদ ও আর্টিকেলস (`/api/v1/articles/`)
- `GET /api/v1/articles/` - সকল প্রকাশিত খবরের ফিল্টার ও প্যাজিনেটেড তালিকা
  - কুয়েরি প্যারামিটার: `?category=politics`, `?search=নির্বাচন`, `?page=1`, `?page_size=10`
- `GET /api/v1/articles/{slug}/` - সংবাদের বিস্তারিত ভিউ (পূর্ববর্তী ও পরবর্তী খবরের লিংকসহ)
- `POST /api/v1/articles/{slug}/view/` - সংবাদের পাঠক সংখ্যা (View count) ইনক্রিমেন্ট
- `GET /api/v1/articles/hero/` - প্রধান লিড নিউজ (Hero Banner)
- `GET /api/v1/articles/breaking/` - ব্রেকিং নিউজ তালিকা
- `GET /api/v1/articles/featured/` - নির্বাচিত বিশেষ সংবাদ তালিকা
- `GET /api/v1/articles/popular/` - সর্বাধিক পঠিত জনপ্রিয় সংবাদ
- `GET /api/v1/articles/latest/` - সর্বশেষ সংবাদ ফিড
- `POST /api/v1/articles/` - নতুন সংবাদ পোস্ট (রিপোর্টার/এডিটর)
- `PUT / PATCH /api/v1/articles/{slug}/` - সংবাদ হালনাগাদ
- `DELETE /api/v1/articles/{slug}/` - সংবাদ অপসারণ
- `POST /api/v1/articles/bulk_action/` - একাধিক সংবাদ একসাথে পাবলিশ/ড্রাফট/ডিলিট

### ৩. বিভাগসমূহ (`/api/v1/categories/`)
- `GET /api/v1/categories/` - ৮টি সক্রিয় বিভাগ ও রিয়েল-টাইম সংবাদের সংখ্যা
- `POST /api/v1/categories/` - নতুন ক্যাটাগরি তৈরি
- `GET /api/v1/categories/{slug}/` - বিভাগের বিস্তারিত তথ্য

### ৪. লেখক ও সাংবাদিকবৃন্দ (`/api/v1/authors/`)
- `GET /api/v1/authors/` - সকল সাংবাদিক ও প্রতিবেদকদের তালিকা
- `POST /api/v1/authors/` - নতুন সাংবাদিক প্রোফাইল যুক্তকরণ

### ৫. মন্তব্য ও পাঠক মতামত (`/api/v1/comments/`)
- `GET /api/v1/comments/?article__slug={slug}` - নির্দিষ্ট সংবাদের অনুমোদিত মন্তব্য
- `POST /api/v1/comments/` - পাঠকদের নতুন মন্তব্য গ্রহণ
- `POST /api/v1/comments/{id}/like/` - মন্তব্যে লাইক প্রদান
- `POST /api/v1/comments/{id}/approve/` - অ্যাডমিন কর্তৃক মন্তব্য অনুমোদন
- `POST /api/v1/comments/{id}/mark_spam/` - মন্তব্যকে স্প্যাম চিহ্নিতকরণ

### ৬. মিডিয়া লাইব্রেরি (`/api/v1/media/`)
- `GET /api/v1/media/` - আপলোডকৃত মিডিয়া ফাইল ও ছবির তালিকা
- `POST /api/v1/media/` - নতুন ছবি ও ডকুমেন্ট আপলোড (অটোমেটিক ডাইমেনশন ও সাইজ ডিটেকশন)

### ৭. নিউজলেটার গ্রাহক (`/api/v1/subscribers/`)
- `POST /api/v1/subscribers/` - পাঠকদের সাবস্ক্রিপশন গ্রহণ
- `GET /api/v1/subscribers/` - অ্যাডমিনদের জন্য গ্রাহক তালিকা
- `GET /api/v1/subscribers/export_csv/` - গ্রাহক তালিকা CSV ফরম্যাটে ডাউনলোড

### ৮. ড্যাশবোর্ড অ্যানালিটিক্স ও রিপোর্টস (`/api/v1/analytics/`)
- `GET /api/v1/analytics/dashboard/` - অ্যাডমিন ড্যাশবোর্ডের যাবতীয় KPI (মোট ভিউ, আজ ভিউ, অ্যাক্টিভ ইউজার, পেন্ডিং কমেন্টস, ক্যাটাগরি ডিস্ট্রিবিউশন চার্ট, ডিভাইস ব্রেকডাউন)
- `GET /api/v1/analytics/reports/articles/csv/` - সংবাদের পূর্ণাঙ্গ রিপোর্ট CSV ফরম্যাটে ডাউনলোড

### ৯. নোটিফিকেশনস (`/api/v1/notifications/`)
- `GET /api/v1/notifications/` - অ্যাডমিন নোটিফিকেশন তালিকা
- `POST /api/v1/notifications/{id}/mark-read/` - নোটিফিকেশন পঠিত হিসেবে চিহ্নিত
- `POST /api/v1/notifications/mark-all-read/` - সব একসাথে পড়া
- `POST /api/v1/notifications/clear-all/` - নোটিফিকেশন ক্লিয়ার

### ১০. ওয়েবসাইট সেটিংস (`/api/v1/settings/`)
- `GET /api/v1/settings/` - ওয়েবসাইটের সাধারণ সেটিংস, লোগো, এসইও মেটা ও সোশ্যাল মিডিয়া লিংক
- `PUT /api/v1/settings/` - সেটিংস হালনাগাদ (সুপার অ্যাডমিন)
- `POST /api/v1/settings/contact/` - পাঠকদের যোগাযোগ ও বার্তা প্রেরণ

---

## 🧪 স্বয়ংক্রিয় টেস্ট পরিচালনা (Automated Tests)

ব্যাকএন্ডের নির্ভরযোগ্যতা নিশ্চিত করতে টেস্ট স্যুট রান করুন:

```bash
./venv/bin/python manage.py test apps.articles.test_articles apps.accounts.test_accounts
```
*ফলাফল:* `Ran 7 tests in 0.95s - OK`

---

## 🔗 ফ্রন্টএন্ড ইন্টিগ্রেশন সহায়িকা (Frontend Integration)

### News Portal (`Hello-Desh-News-Website`) এর সাথে সংযোগ:
React অ্যাপ্লিকেশনের `.env` অথবা এপিআই ক্লায়েন্টে বেস ইউআরএল যুক্ত করুন:
```ts
export const API_BASE_URL = 'http://localhost:8000/api/v1';

// উদাহরণ: নিউজ ফিড কল
export const fetchLatestNews = async () => {
  const res = await fetch(`${API_BASE_URL}/articles/latest/`);
  return res.json();
};
```

### Admin Dashboard (`Hello-Desh-News-Website-Admin-Dashboard`) এর সাথে সংযোগ:
```ts
// উদাহরণ: অ্যাডমিন লগইন ও JWT স্টোরেজ
export const adminLogin = async (email, password) => {
  const res = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  const data = await res.json();
  localStorage.setItem('access_token', data.access);
  return data;
};
```
