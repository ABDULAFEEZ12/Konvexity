# app/blueprints/public/routes.py

from flask import flash, redirect, render_template, request, url_for

from app.blueprints.public import public_bp


@public_bp.route("/")
def home():
    seo = {
        "title": "Konvexity \u2014 Where Clarity Meets Growth",
        "description": "Premium leadership, organizational transformation, and human performance consulting. Helping founders, executives, and institutions achieve sustainable growth.",
        "canonical_url": url_for("public.home", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/home.html", seo=seo)


@public_bp.route("/about")
def about():
    seo = {
        "title": "About Konvexity \u2014 Where Clarity Meets Growth",
        "description": "Konvexity is a premium leadership and organizational transformation institution. We help organizations build clarity, drive growth, and achieve sustainable excellence.",
        "canonical_url": url_for("public.about", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/about.html", seo=seo)


@public_bp.route("/solutions")
def solutions():
    seo = {
        "title": "Solutions \u2014 Konvexity",
        "description": "Explore our premium solutions: Leadership Lab, Professional Accelerator, ADI Performance Model, and Konvexity Clarity Room.",
        "canonical_url": url_for("public.solutions", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/solutions.html", seo=seo)


@public_bp.route("/solutions/<slug>")
def solution_detail(slug):
    seo = {
        "title": "Solution Details \u2014 Konvexity",
        "description": "Detailed information about our solutions.",
        "canonical_url": url_for("public.solution_detail", slug=slug, _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/solution_detail.html", seo=seo, solution_slug=slug)


@public_bp.route("/programs")
def programs():
    seo = {
        "title": "Programs \u2014 Konvexity",
        "description": "Explore our comprehensive leadership development, professional acceleration, and organizational transformation programs.",
        "canonical_url": url_for("public.programs", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/programs.html", seo=seo)


@public_bp.route("/programs/<slug>")
def program_detail(slug):
    seo = {
        "title": "Program Details \u2014 Konvexity",
        "description": "Detailed information about our programs.",
        "canonical_url": url_for("public.program_detail", slug=slug, _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/program_detail.html", seo=seo, program_slug=slug)


@public_bp.route("/faculty")
def faculty():
    seo = {
        "title": "Faculty \u2014 Konvexity",
        "description": "Meet our multidisciplinary faculty of experts in leadership, governance, finance, AI, digital transformation, behavioral psychology, and organizational development.",
        "canonical_url": url_for("public.faculty", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/faculty.html", seo=seo)


@public_bp.route("/faculty/<slug>")
def faculty_detail(slug):
    seo = {
        "title": "Faculty Profile \u2014 Konvexity",
        "description": "Detailed profile of our faculty member.",
        "canonical_url": url_for("public.faculty_detail", slug=slug, _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/faculty_detail.html", seo=seo, faculty_slug=slug)


@public_bp.route("/founder")
def founder():
    seo = {
        "title": "Dr. Tioluwalogo Olakunbi-Black \u2014 Founder, Konvexity",
        "description": "Dr. Tioluwalogo Olakunbi-Black is a Performance Architect, founder of TechTrybe Africa, and one of Africa\u2019s leading experts on leadership and organizational transformation.",
        "canonical_url": url_for("public.founder", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/founder.html", seo=seo)


@public_bp.route("/clients")
def clients():
    seo = {
        "title": "Clients \u2014 Konvexity",
        "description": "We are privileged to work with leading organizations, institutions, and enterprises across Africa and beyond.",
        "canonical_url": url_for("public.clients", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/clients.html", seo=seo)


@public_bp.route("/contact", methods=["GET", "POST"])
def contact():
    seo = {
        "title": "Contact \u2014 Konvexity",
        "description": "Start a conversation with Konvexity. Inquire about our programs, solutions, or how we can support your organization\u2019s transformation journey.",
        "canonical_url": url_for("public.contact", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()
        if not name or not email or not message:
            flash("Please complete all required fields.", "error")
            return render_template("public/contact.html", seo=seo)
        flash("Thank you for your message. We will respond within 24 hours.", "success")
        return redirect(url_for("public.contact"))
    return render_template("public/contact.html", seo=seo)


@public_bp.route("/resources")
def resources():
    seo = {
        "title": "Resources \u2014 Konvexity",
        "description": "Explore articles, research papers, frameworks, and insights from Konvexity\u2019s faculty and research center.",
        "canonical_url": url_for("public.resources", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/resources.html", seo=seo)


@public_bp.route("/blog")
def blog():
    seo = {
        "title": "Blog \u2014 Konvexity",
        "description": "Insights, perspectives, and thought leadership from Konvexity\u2019s faculty on leadership, organizational transformation, and human performance.",
        "canonical_url": url_for("public.blog", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/blog.html", seo=seo)


@public_bp.route("/events")
def events():
    seo = {
        "title": "Events \u2014 Konvexity",
        "description": "Upcoming workshops, masterclasses, speaking engagements, and programs from Konvexity.",
        "canonical_url": url_for("public.events", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/events.html", seo=seo)


@public_bp.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": url_for("public.home", _external=True), "priority": "1.0"},
        {"loc": url_for("public.about", _external=True), "priority": "0.8"},
        {"loc": url_for("public.solutions", _external=True), "priority": "0.9"},
        {"loc": url_for("public.programs", _external=True), "priority": "0.8"},
        {"loc": url_for("public.faculty", _external=True), "priority": "0.7"},
        {"loc": url_for("public.founder", _external=True), "priority": "0.8"},
        {"loc": url_for("public.clients", _external=True), "priority": "0.6"},
        {"loc": url_for("public.contact", _external=True), "priority": "0.7"},
        {"loc": url_for("public.resources", _external=True), "priority": "0.6"},
    ]
    sitemap_xml = render_template("public/sitemap.xml", pages=pages)
    return sitemap_xml, 200, {"Content-Type": "application/xml"}