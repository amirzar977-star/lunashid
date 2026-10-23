"""Routes for the Horizon Properties site."""
import re

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)

from . import data, db

bp = Blueprint("site", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[A-Za-z]{2,}$")


@bp.app_context_processor
def inject_site():
    return {"site": data.SITE, "nav": data.NAV}


def wants_json():
    return (
        request.is_json
        or request.accept_mimetypes.best == "application/json"
        or request.headers.get("X-Requested-With") == "fetch"
    )


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------

@bp.route("/")
def home():
    return render_template(
        "index.html",
        page_title=f"{data.SITE['name']} — Exceptional homes & investments",
        page_description=data.SITE["description"],
        hero=data.HERO_IMAGE,
        featured=data.featured_properties(),
        services=data.SERVICES,
        values=data.VALUES,
        stats=data.STATS,
        team=data.team_members(),
        about_images=data.ABOUT_IMAGES,
    )


@bp.route("/properties")
def properties():
    items, meta = data.filter_properties(request.args)
    return render_template(
        "properties.html",
        page_title=f"Properties — {data.SITE['name']}",
        page_description=(
            "Browse the Horizon Properties portfolio: architect-designed homes, "
            "waterfront residences and prime investment property."
        ),
        properties=items,
        meta=meta,
        locations=data.locations(),
        types=data.property_types(),
        price_ranges=data.PRICE_RANGES,
        bed_options=data.BED_OPTIONS,
        bath_options=data.BATH_OPTIONS,
        sort_options=data.SORT_OPTIONS,
        filters={
            "q": request.args.get("q", ""),
            "location": request.args.get("location", ""),
            "type": request.args.get("type", ""),
            "beds": request.args.get("beds", ""),
            "baths": request.args.get("baths", ""),
            "price": request.args.get("price", ""),
            "sort": meta["sort"],
        },
    )


@bp.route("/properties/<slug>")
def property_detail(slug):
    prop = data.get_property(slug)
    if prop is None:
        abort(404)
    return render_template(
        "property.html",
        page_title=f"{prop['name']}, {prop['city']} — {data.SITE['name']}",
        page_description=prop["summary"],
        property=prop,
        agent=data.get_agent(prop["agent"]),
        similar=data.similar_properties(prop),
        viewing_sent=request.args.get("viewing") == "1",
    )


@bp.route("/about")
def about():
    return render_template(
        "about.html",
        page_title=f"About us — {data.SITE['name']}",
        page_description=(
            "Horizon Properties is a boutique brokerage for exceptional homes "
            "and considered investments."
        ),
        values=data.VALUES,
        stats=data.STATS,
        team=data.team_members(),
        about_images=data.ABOUT_IMAGES,
    )


@bp.route("/services")
def services():
    return render_template(
        "services.html",
        page_title=f"Services — {data.SITE['name']}",
        page_description=(
            "Sales, investment, marketing, advisory, valuation and relocation "
            "services for prime residential property."
        ),
        services=data.SERVICES,
        stats=data.STATS,
    )


@bp.route("/team")
def team():
    return render_template(
        "team.html",
        page_title=f"Team — {data.SITE['name']}",
        page_description=(
            "Meet the advisors at Horizon Properties: sales, investment and "
            "client services."
        ),
        team=data.team_members(),
        stats=data.STATS,
    )


@bp.route("/contact")
def contact():
    return render_template(
        "contact.html",
        page_title=f"Contact — {data.SITE['name']}",
        page_description=(
            "Talk to a Horizon Properties advisor about buying, selling or "
            "investing."
        ),
        sent=request.args.get("sent") == "1",
        services=data.SERVICES,
    )


@bp.route("/saved")
def saved():
    return render_template(
        "saved.html",
        page_title=f"Saved properties — {data.SITE['name']}",
        page_description="Properties you have saved while browsing Horizon Properties.",
        properties=data.all_properties(),
    )


@bp.route("/favicon.ico")
def favicon():
    return redirect(url_for("static", filename="img/favicon.svg"))


# ---------------------------------------------------------------------------
# Form endpoints (progressive enhancement: JSON for fetch, redirect without JS)
# ---------------------------------------------------------------------------

@bp.post("/api/contact")
def api_contact():
    payload = request.get_json(silent=True) or request.form
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    phone = (payload.get("phone") or "").strip()
    message = (payload.get("message") or "").strip()
    interest = (payload.get("interest") or "").strip()

    errors = {}
    if len(name) < 2:
        errors["name"] = "Please tell us your name."
    if not EMAIL_RE.match(email):
        errors["email"] = "Please enter a valid email address."
    if len(message) < 10:
        errors["message"] = "Please add a short message (at least 10 characters)."

    if errors:
        if wants_json():
            return jsonify(ok=False, errors=errors), 400
        flash("Please check the highlighted fields and try again.", "error")
        return redirect(url_for("site.contact"))

    db.add_enquiry(
        "contact", name=name, email=email, phone=phone,
        message=message + (f"\n\nInterest: {interest}" if interest else ""),
    )
    notice = "Thank you — an advisor will reply within one business day."
    if wants_json():
        return jsonify(ok=True, message=notice)
    flash(notice, "success")
    return redirect(url_for("site.contact", sent=1))


@bp.post("/api/viewing")
def api_viewing():
    payload = request.get_json(silent=True) or request.form
    name = (payload.get("name") or "").strip()
    email = (payload.get("email") or "").strip()
    phone = (payload.get("phone") or "").strip()
    message = (payload.get("message") or "").strip()
    slug = (payload.get("property") or "").strip()
    preferred_date = (payload.get("date") or "").strip()
    preferred_time = (payload.get("time") or "").strip()
    intent = (payload.get("intent") or "viewing").strip()

    prop = data.get_property(slug) if slug else None

    errors = {}
    if len(name) < 2:
        errors["name"] = "Please tell us your name."
    if not EMAIL_RE.match(email):
        errors["email"] = "Please enter a valid email address."
    if intent == "viewing" and not preferred_date:
        errors["date"] = "Please choose a preferred date."

    if errors:
        if wants_json():
            return jsonify(ok=False, errors=errors), 400
        flash("Please check the highlighted fields and try again.", "error")
        return redirect(url_for("site.property_detail", slug=slug) if prop else url_for("site.contact"))

    db.add_enquiry(
        intent,
        name=name,
        email=email,
        phone=phone,
        message=message,
        property_slug=slug,
        preferred_date=preferred_date,
        preferred_time=preferred_time,
    )

    if intent == "viewing":
        notice = "Your viewing request is in — we will confirm the time by email shortly."
    else:
        notice = "Thank you — the listing advisor will contact you shortly."

    if wants_json():
        return jsonify(ok=True, message=notice)
    flash(notice, "success")
    return redirect(
        url_for("site.property_detail", slug=slug, viewing=1) if prop else url_for("site.contact", sent=1)
    )


@bp.post("/api/subscribe")
def api_subscribe():
    payload = request.get_json(silent=True) or request.form
    email = (payload.get("email") or "").strip()
    if not EMAIL_RE.match(email):
        if wants_json():
            return jsonify(ok=False, errors={"email": "Please enter a valid email address."}), 400
        flash("Please enter a valid email address.", "error")
        return redirect(request.referrer or url_for("site.home"))

    created = db.add_subscriber(email)
    notice = (
        "You are on the list — new listings will arrive by email."
        if created
        else "You are already subscribed — thank you."
    )
    if wants_json():
        return jsonify(ok=True, created=created, message=notice)
    flash(notice, "success")
    return redirect(request.referrer or url_for("site.home"))
