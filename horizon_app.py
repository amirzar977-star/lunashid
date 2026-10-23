"""Entry point for the Horizon Properties site.

Development:  flask --app horizon_app:app run --debug --host 0.0.0.0 --port 3000
Production:   gunicorn "horizon_app:app"
"""
from horizon import create_app

app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
