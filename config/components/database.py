DATABASES = {
    "default": {
        "ENGINE": environ.get("SQL_ENGINE", "django.db.backends.sqlite3"),
        "NAME": environ.get("SQL_DATABASE", BASE_DIR / "db.sqlite3"),
        "USER": environ.get("SQL_USER", "user"),
        "PASSWORD": environ.get("SQL_PASSWORD", "password"),
        "HOST": environ.get("SQL_HOST", "localhost"),
        "PORT": environ.get("SQL_PORT", "5432"),
    }
}
