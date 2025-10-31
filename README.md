# 🎬 Netflix Clone

A Netflix-style streaming web application built in Django, featuring user authentication, dynamic movie browsing, personalized lists, and cloud-hosted media.
This project showcases backend engineering, database design, and API integration following modern full-stack best practices.

⚠️ Note on Live Demo:
The live demo on Render may return a 502 Bad Gateway due to memory limits on the free Render plan. 
For a fully stable experience, I would highly recommend cloning the project and running it locally - there are instructions for how to achieve this below.
This has been one of my most ambitious projects yet, and currently I do not have the budge to host it on a paid plan to extend the memory limits.

[🌐 Live Demo](https://https://netflix-clone-fhwh.onrender.com/)

---

## 📸 Screenshot

![Netflix Clone Screenshot](screenshot.JPG)

---

## 🎯 Features

- 🔐 User Authentication — Secure signup, login, and logout system
- 🎞️ Dynamic Movie Catalog — Browse all movies with cover art, details, and trailers
- 🧠 Search Functionality — Search by title or genre
- 💾 My List — Add or remove movies to your personal watch list
- 🧩 Genre Filtering — Browse movies by category
- ⚙️ API Endpoints:
- /api/movies/ → Returns JSON of all movie data
- /api/my-list/ → Returns user’s saved movie UUIDs
- 🖥️ Watch Page — Stream videos directly in the browser
- 🧱 Responsive UI — Built with TailwindCSS for a clean, adaptive layout
---

## 🛠️ Tech Stack

- **Django** - Backend framework
- **PostgreSQL (AWS RDS)** - Database
- **AWS S3 (for media and static files)** - Cloud Storage
- **HTML, CSS3, TailwindCSS, JavaScript (AJAX)** - Frontend structure and styling
- **Render** - Hosting

---

## 🚀 Getting Started

To run this app locally:

### 1. Clone the repository

git clone https://github.com/zandernh/netflix-clone.git

cd netflix-clone

### 2. Set up a viritual enviornment

python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Apply database migrations

python manage.py migrate

### 5. Create a superuser to access the admin panel

python manage.py createsuperuser

### 6. Run the development server

python manage.py runserver

### 7. Access the app at:

http://127.0.0.1:8000

---

## 🧠 How It Works

- Users log in to browse or manage their personalized movie list.
- Each movie entry contains title, description, genres, release date, runtime, image URL, and video URL.
- The “Add to My List” button uses AJAX to toggle items without reloading the page.
- Genres are stored via a Many-to-Many relationship in Django, allowing flexible categorization.
- AWS S3 securely hosts all static and media assets, which are served via signed URLs for efficient loading.
- The app exposes clean REST API endpoints for integration or testing.

---

## ☁️ Cloud Setup and Architecture

To follow production best practices, media files (images and videos) are not stored directly in the database.
Instead, I configured AWS S3 as external object storage, referencing each media file’s URL in the Django models.

This approach:

- Reduces database size and improves query performance
- Mimics real-world scalability used in large-scale streaming platforms
- Separates static/media handling from core backend logic

I also set up AWS RDS (PostgreSQL) for the relational database layer.
Because I’m using the AWS free tier, the nearest available server region was Stockholm, which can occasionally introduce mild latency during media playback — a known trade-off for free-tier cloud resources.

---

## 📂 File Structure

![Netflix Clone File Structure](filestructure.JPG)

---

⚠️ Known Limitations

- Some movies may display null or missing genres due to incomplete or inconsistent Many-to-Many data.
- Minor latency may occur when loading images or video streams, caused by AWS S3’s free-tier region distance (Stockholm).
- Currently optimized for desktop; mobile responsiveness is partial but functional.

---

## 📦 Deployment

The app is deployed on Render using a production-ready Django configuration.

- **Database**: AWS RDS (PostgreSQL)
- **Static & Media Files**: AWS S3
- **Environment Variables**: Managed securely on Render

---

## 📄 License

This project is open-source and free to use under the MIT Licence

---

## 🙋‍♂️ Author

Built with ❤️ and curiosity by Zander Harding
