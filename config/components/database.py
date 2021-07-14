DATABASES = {
    "default": {
        "ENGINE": environ.get("DB_ENGINE", "django.db.backends.sqlite3"),
        "NAME": environ.get("DB_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": environ.get("DB_USER", "user"),
        "PASSWORD": environ.get("DB_PASSWORD", "password"),
        "HOST": environ.get("DB_HOST", "localhost"),
        "PORT": environ.get("DB_PORT", "5432"),
    }
}
