"""Horizon Properties — application factory.

A small server-rendered Flask site for a boutique real-estate brokerage.
"""
import os

from flask import Flask, render_template

from . import db
from .views import bp


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get("SECRET_KEY", "horizon-properties-development-key"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        JSON_SORT_KEYS=False,
        TEMPLATES_AUTO_RELOAD=True,
    )

    db.init_db()
    app.register_blueprint(bp)

    @app.errorhandler(404)
    def not_found(error):
        return (
            render_template(
                "404.html",
                page_title="Page not found — Horizon Properties",
                page_description="We could not find the page you were looking for.",
            ),
            404,
        )

    return app
