# app/blueprints/public/routes.py

from flask import abort, render_template, request, url_for

from app.blueprints.public import public_bp
from app.blueprints.public.forms import ScheduleConsultationForm, WorkWithKonvexityForm
from app.extensions import db, limiter
from app.models import ConsultationBooking, Lead
from app.models.crm import SERVICE_CHOICES, ActivityLog
from app.utils.identifiers import next_identifier


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


@public_bp.route("/pricing")
def pricing():
    seo = {
        "title": "The Investment Menu \u2014 Konvexity",
        "description": "Transparent, tiered pricing across every Konvexity solution \u2014 Leadership Lab, ADI Performance Model, Professional Accelerator, and Konvexity Clarity Room.",
        "canonical_url": url_for("public.pricing", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/pricing.html", seo=seo)


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


@public_bp.route("/signature-platforms")
def signature_platforms():
    seo = {
        "title": "Signature Platforms | Konvexity",
        "description": "Konvexity's flagship initiatives: Konvexity Entrepreneurship, a community for founders and business builders, and AR\u00c1K\u00d9NRIN, Konvexity's male formation platform.",
        "canonical_url": url_for("public.signature_platforms", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/signature_platforms.html", seo=seo)


BRAND_PORTFOLIO_ITEMS = {
    "gesai": {
        "name": "GESAI",
        "full_name": "Green Economy & Sustainability African Institute",
        "tagline": "Building Africa’s Green Economy.",
        "overview": "A Konvexity initiative advancing sustainability, green enterprise, and practical solutions for Africa’s economic future.",
        "logo": "images/logos/gesai-logo-light.png",
        "logo_dark": "images/logos/gesai-logo-dark.png",
        "image": "images/platforms/gesai-solar-eswatini.webp",
        "image_alt": "Solar panels installed on a rural landscape in Eswatini",
        "intro": (
            "The Green Economy & Sustainability African Institute (GESAI) works to help African "
            "people and organisations understand the changing green economy and find practical "
            "ways to participate in it."
        ),
        "intro_extra": [
            "Our work covers professional training, corporate sustainability, business advisory, "
            "applied research and green enterprise development. We focus on the knowledge and "
            "skills that businesses need to adapt, while helping entrepreneurs identify "
            "opportunities in emerging green industries.",
            "GESAI brings this work into Konvexity’s wider focus on strategy, capability "
            "development and execution. We want sustainability to inform the way organisations "
            "make decisions, build their businesses and prepare for the future.",
        ],
        "sections": [
            {
                "type": "text",
                "title": "Why GESAI?",
                "image": "images/platforms/gesai-farmer-crops.webp",
                "image_alt": "An African farmer inspecting crops in a field",
                "paragraphs": [
                    "Africa’s green transition is creating new demands across industries. "
                    "Businesses are under growing pressure to improve their environmental "
                    "practices, while entrepreneurs are exploring opportunities in clean energy, "
                    "electric mobility and resource recovery. Meeting these demands requires "
                    "people who understand the issues and know how to respond. GESAI aims to help "
                    "close that gap by connecting sustainability knowledge with business practice.",
                ],
            },
            {
                "type": "grid",
                "title": "What We Do",
                "cards": [
                    {
                        "title": "Professional and Corporate Sustainability",
                        "text": (
                            "We help professionals and businesses build the skills needed to "
                            "integrate sustainability into their work. Our areas of focus include "
                            "ESG, sustainability reporting readiness, climate risk, carbon "
                            "accounting and sustainable procurement."
                        ),
                    },
                    {
                        "title": "Green Enterprise Development",
                        "text": (
                            "We support the development of businesses that respond to "
                            "environmental challenges and emerging market needs. This includes "
                            "green business models, circular economy solutions, waste-to-value "
                            "opportunities and support for small and medium-sized enterprises."
                        ),
                    },
                    {
                        "title": "Mobility and Clean Energy Enterprise",
                        "text": (
                            "The shift towards cleaner energy and transport presents "
                            "opportunities for new businesses. GESAI focuses on areas such as "
                            "electric mobility, renewable energy, charging infrastructure, "
                            "battery services and green logistics, with an emphasis on "
                            "entrepreneurship and commercial viability."
                        ),
                    },
                    {
                        "title": "Research, Policy and Advisory",
                        "text": (
                            "Good decisions depend on reliable information and a clear "
                            "understanding of the problem. We work towards supporting "
                            "organisations and stakeholders through sustainability assessments, "
                            "strategic roadmaps, sector research and impact evaluation."
                        ),
                    },
                ],
            },
            {
                "type": "text",
                "title": "Our Approach",
                "paragraphs": [
                    "GESAI takes a practical approach to sustainability. We focus on helping "
                    "people apply what they learn, understand the business implications of their "
                    "decisions and identify opportunities they can act on.",
                    "We also recognise the importance of collaboration. Working with industry "
                    "practitioners, academic institutions, financial organisations and "
                    "development partners can help ensure that our programmes respond to real "
                    "needs. Where possible, we will assess progress through clear indicators, "
                    "including skills gained, business development and the results of "
                    "sustainability initiatives.",
                ],
            },
            {
                "type": "text",
                "title": "Who We Work With",
                "paragraphs": [
                    "Our work is intended for professionals looking to develop their "
                    "sustainability expertise, companies seeking to improve their practices, and "
                    "entrepreneurs interested in green business opportunities.",
                    "We also seek to engage graduates, public institutions, researchers, "
                    "investors and development organisations that share an interest in Africa’s "
                    "green economy.",
                ],
            },
            {
                "type": "text",
                "title": "From Knowledge to Practice",
                "paragraphs": [
                    "GESAI is being developed around a clear idea: people and businesses need "
                    "the right capabilities to respond to changes in the economy.",
                    "Through training, advisory services and enterprise development, we aim to "
                    "help bridge the gap between understanding sustainability and putting it "
                    "into practice.",
                    "As part of Konvexity’s commitment to unlocking potential through clarity, "
                    "strategy, and execution, GESAI focuses on making sustainability practical, "
                    "commercially relevant, and responsive to Africa’s development priorities.",
                ],
            },
        ],
        "cta_label": "Explore GESAI Opportunities",
    },
    "tab": {
        "name": "TAB",
        "full_name": "TakeABreak",
        "tagline": "Work hard. Live well.",
        "overview": "Curated short getaways for professionals to reset, unwind, and connect.",
        "logo": "images/logos/tab-logo-light.png",
        "logo_dark": "images/logos/tab-logo-dark.png",
        "image": "images/platforms/tab-zanzibar-beachfront.webp",
        "image_alt": "Scenic beachfront view from a boat in Zanzibar",
        "intro": (
            "TakeABreak is Konvexity’s curated getaway and experience brand, created for "
            "working professionals, entrepreneurs and anyone who wants to step away from the "
            "daily routine. We bring people together for short escapes filled with good "
            "company, comfortable stays, local experiences and time to relax."
        ),
        "intro_extra": [
            "From the destination to the activities, we handle the planning so you can focus "
            "on enjoying the experience.",
        ],
        "sections": [
            {
                "type": "text",
                "title": "More Than a Getaway",
                "paragraphs": [
                    "A good trip is about more than where you go. It is also about the people "
                    "you meet, the things you try and the memories you bring home.",
                    "With TakeABreak, you can explore new places, share experiences with people "
                    "you might never have met otherwise, and return to your routine feeling "
                    "refreshed.",
                ],
            },
            {
                "type": "text",
                "title": "Who Is It For?",
                "image": "images/platforms/tab-eswatini-hikers.webp",
                "image_alt": "A group of friends hiking together on a scenic trail in Eswatini",
                "paragraphs": [
                    "TakeABreak is for busy professionals, entrepreneurs, young executives and "
                    "anyone who wants to travel, unwind and connect with new people.",
                    "You can come with friends or come on your own. There is room to meet "
                    "people, try something different and enjoy a change of pace.",
                ],
            },
            {
                "type": "grid",
                "title": "What to Expect",
                "cards": [
                    {
                        "title": "Curated Getaways",
                        "text": (
                            "Enjoy thoughtfully planned 2 to 3-day trips, usually scheduled for "
                            "weekends or public holidays so you never have to worry about the "
                            "work day."
                        ),
                    },
                    {
                        "title": "Comfort and Convenience",
                        "text": (
                            "We coordinate the key details, including accommodation, activities "
                            "and the overall experience, so you spend less time planning and "
                            "more time enjoying yourself."
                        ),
                    },
                    {
                        "title": "Local Experiences and Adventure",
                        "text": (
                            "Discover destinations through local food, cultural activities, "
                            "sightseeing, social events and optional adventures."
                        ),
                    },
                    {
                        "title": "Good Company",
                        "text": (
                            "Meet new people, make connections and enjoy the freedom of "
                            "travelling with a group without having to organise one yourself."
                        ),
                    },
                    {
                        "title": "Take Time for Yourself",
                        "text": (
                            "You do not have to wait for a long holiday to get away. Sometimes, "
                            "a well-planned weekend is enough to give you a different "
                            "perspective. TakeABreak by Konvexity makes it easier to step out of "
                            "your routine and make time for experiences beyond work."
                        ),
                    },
                ],
            },
            {
                "type": "text",
                "title": None,
                "paragraphs": [
                    "As part of Konvexity’s commitment to unlocking potential through clarity, "
                    "strategy, and execution, TakeABreak creates intentional experiences that "
                    "help individuals and teams recharge, reconnect, and return with renewed "
                    "energy and perspective.",
                ],
            },
        ],
        "cta_label": "Plan Your Getaway",
    },
    "lwb": {
        "name": "LWB",
        "full_name": "Leadership Without Borders",
        "tagline": "Leadership. Exposure. Opportunity.",
        "overview": "Connecting African leaders to global markets, networks, and growth opportunities.",
        "logo": "images/logos/lwb-logo-light.png",
        "logo_dark": "images/logos/lwb-logo-dark.png",
        "image": "images/platforms/lwb-lagos-meeting.webp",
        "image_alt": "A diverse team in a business meeting at a Lagos office",
        "intro": (
            "Leadership Without Borders (LWB) is a curated international leadership and "
            "business-immersion experience connecting African leaders, entrepreneurs and "
            "executives with global perspectives, new markets and meaningful professional "
            "relationships."
        ),
        "intro_extra": [
            "Moving beyond conventional conferences and business travel, LWB combines "
            "executive learning, company visits, market exploration, peer exchange and "
            "strategic networking to help participants discover new possibilities and "
            "translate what they learn into practical action.",
            "We believe leadership grows when perspectives expand. By stepping into different "
            "business environments, engaging with industry practitioners and experiencing new "
            "ways of thinking and working, participants gain insights that can shape their "
            "leadership, strengthen their organisations and open doors to new opportunities.",
            "Every LWB experience is intentionally curated around a purpose, bringing together "
            "the right people, places and conversations to make international exposure "
            "meaningful.",
        ],
        "sections": [
            {
                "type": "grid",
                "title": None,
                "columns": 3,
                "cards": [
                    {
                        "title": "Leadership Immersions",
                        "text": (
                            "Explore leadership practices, organisational culture, strategy and "
                            "performance through executive learning, peer exchange and "
                            "real-world exposure."
                        ),
                    },
                    {
                        "title": "Business & Market Expeditions",
                        "text": (
                            "Discover emerging markets, explore business ecosystems, engage with "
                            "industry leaders and identify opportunities for growth, "
                            "collaboration and cross-border expansion."
                        ),
                    },
                    {
                        "title": "Private Corporate Experiences",
                        "text": (
                            "Purpose-built international experiences for companies, executive "
                            "teams, boards and institutions seeking leadership development, "
                            "strategic exchange or a fresh perspective on collaboration and "
                            "growth."
                        ),
                    },
                ],
            },
            {
                "type": "grid",
                "title": "Five Destinations. New Perspectives.",
                "intro": (
                    "Our initial destination portfolio spans five markets, each offering a "
                    "distinct lens through which to explore leadership, enterprise and "
                    "opportunity."
                ),
                "columns": 3,
                "cards": [
                    {
                        "title": "Mauritius",
                        "text": "Digital Business & International Enterprise",
                        "image": "images/platforms/lwb-mauritius.jpg",
                        "image_alt": "Port Louis, Mauritius skyline",
                    },
                    {
                        "title": "Ghana",
                        "text": "West African Business & Regional Expansion",
                        "image": "images/platforms/lwb-ghana.jpg",
                        "image_alt": "Accra, Ghana skyline",
                    },
                    {
                        "title": "Rwanda",
                        "text": "Innovation & Institutional Effectiveness",
                        "image": "images/platforms/lwb-rwanda.jpg",
                        "image_alt": "Kigali, Rwanda skyline",
                    },
                    {
                        "title": "Dubai, UAE",
                        "text": "Global Trade, Capital & Business Growth",
                        "image": "images/platforms/lwb-dubai.jpg",
                        "image_alt": "Dubai, UAE skyline with the Burj Khalifa",
                    },
                    {
                        "title": "London, UK",
                        "text": "Global Leadership, Finance & Innovation",
                        "image": "images/platforms/lwb-london.jpg",
                        "image_alt": "London, UK financial district skyline",
                    },
                ],
                "outro": [
                    "Each programme will be shaped by its destination, participant objectives "
                    "and the opportunities available through local business, institutional and "
                    "learning networks.",
                ],
            },
            {
                "type": "text",
                "title": "Designed for Leaders Ready to Think Beyond.",
                "image": "images/platforms/lwb-nairobi-skyline.webp",
                "image_alt": "Aerial view of Nairobi's skyscrapers",
                "paragraphs": [
                    "LWB is for founders, business owners, corporate executives, senior "
                    "managers, institutional leaders and professionals seeking fresh "
                    "perspectives, valuable relationships and new possibilities for growth.",
                    "Whether the goal is to strengthen an organisation, explore a new market, "
                    "develop as a leader or build cross-border relationships, every experience "
                    "is designed to connect exposure with purposeful action.",
                ],
            },
            {
                "type": "text",
                "title": "The Experience Doesn’t End at the Border.",
                "image": "images/platforms/lwb-lagos-office-chat.webp",
                "image_alt": "Colleagues in a casual office conversation in Lagos, Nigeria",
                "paragraphs": [
                    "From curated engagements and peer learning to facilitated reflection and "
                    "practical action planning, LWB is designed to make insights count long "
                    "after the journey ends.",
                    "Participants are encouraged to translate their experience into clear "
                    "30-, 60- and 90-day actions, helping turn new perspectives into meaningful "
                    "progress.",
                ],
            },
            {
                "type": "text",
                "title": None,
                "paragraphs": [
                    "As part of Konvexity’s commitment to unlocking potential through clarity, "
                    "strategy, and execution, Leadership Without Borders connects African "
                    "leaders to global perspectives, meaningful relationships, and practical "
                    "opportunities for growth.",
                ],
            },
        ],
        "cta_label": "Explore LWB Experiences",
    },
}


@public_bp.route("/brand-portfolio")
def brand_portfolio():
    seo = {
        "title": "Brand Portfolio — Konvexity",
        "description": "The platforms and brands Konvexity is building: ARÁKÙNRIN, GESAI, TAB, and LWB.",
        "canonical_url": url_for("public.brand_portfolio", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/brand_portfolio.html", seo=seo, brands=BRAND_PORTFOLIO_ITEMS)


@public_bp.route("/brand-portfolio/<slug>")
def brand_portfolio_detail(slug):
    brand = BRAND_PORTFOLIO_ITEMS.get(slug)
    if brand is None:
        abort(404)
    seo = {
        "title": f"{brand['name']} — Konvexity Brand Portfolio",
        "description": f"{brand['full_name']}: {brand['tagline']}",
        "canonical_url": url_for("public.brand_portfolio_detail", slug=slug, _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/brand_portfolio_detail.html", seo=seo, brand=brand, slug=slug)


@public_bp.route("/arakunrin")
def arakunrin():
    seo = {
        "title": "AR\u00c1K\u00d9NRIN \u2014 The Institute for Male Formation | Konvexity",
        "description": "AR\u00c1K\u00d9NRIN is Konvexity's male formation platform, intentionally developing males across every stage of life through Boys Today. Men Tomorrow. and AR\u00c1K\u00d9NRIN tracks.",
        "canonical_url": url_for("public.arakunrin", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/arakunrin.html", seo=seo)


@public_bp.route("/ken")
def ken():
    seo = {
        "title": "Konvexity Entrepreneurs Network (KEN) \u2014 Konvexity",
        "description": "KEN is Konvexity's entrepreneurial community, equipping founders, entrepreneurs, and SME leaders with practical knowledge, strategic connections, and growth experiences.",
        "canonical_url": url_for("public.ken", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    return render_template("public/ken.html", seo=seo)


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
@limiter.limit("10 per hour", methods=["POST"])
def contact():
    seo = {
        "title": "Contact \u2014 Konvexity",
        "description": "Start a conversation with Konvexity. Enquire about our solutions, brands, or how we can support your organization\u2019s transformation journey.",
        "canonical_url": url_for("public.contact", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }

    valid_types = {key for key, _ in SERVICE_CHOICES}
    requested_type = request.args.get("type", "")
    form = WorkWithKonvexityForm(service_interest=requested_type if requested_type in valid_types else None)
    request_id = None

    if form.validate_on_submit():
        request_id = next_identifier(scope="lead", prefix="KVX")

        lead = Lead(
            request_id=request_id,
            full_name=form.full_name.data.strip(),
            email=form.email.data.strip().lower(),
            whatsapp_number=(form.whatsapp_number.data or "").strip(),
            company=(form.company.data or "").strip() or None,
            job_title=(form.job_title.data or "").strip() or None,
            country=(form.country.data or "").strip() or None,
            service_interest=form.service_interest.data,
            message=(form.message.data or "").strip() or None,
        )
        db.session.add(lead)
        db.session.flush()

        ActivityLog.record(
            entity_type="lead",
            entity_id=lead.id,
            action="submitted",
            description=f"New enquiry {lead.request_id} submitted via Contact.",
        )
        db.session.commit()

        return render_template("public/contact.html", seo=seo, form=WorkWithKonvexityForm(formdata=None), request_id=request_id, submitted=True)

    return render_template("public/contact.html", seo=seo, form=form, request_id=request_id, submitted=False)


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


# --- Lead capture: replaces the old wa.me deep links -----------------------

@public_bp.route("/work-with-konvexity", methods=["GET", "POST"])
@limiter.limit("10 per hour", methods=["POST"])
def work_with_konvexity():
    seo = {
        "title": "Work With Konvexity",
        "description": "Tell us about your project and a Konvexity consultant will be in touch within 24 hours.",
        "canonical_url": url_for("public.work_with_konvexity", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    form = WorkWithKonvexityForm()
    request_id = None

    if form.validate_on_submit():
        request_id = next_identifier(scope="lead", prefix="KVX")

        lead = Lead(
            request_id=request_id,
            full_name=form.full_name.data.strip(),
            email=form.email.data.strip().lower(),
            whatsapp_number=form.whatsapp_number.data.strip(),
            company=(form.company.data or "").strip() or None,
            job_title=(form.job_title.data or "").strip() or None,
            country=(form.country.data or "").strip() or None,
            service_interest=form.service_interest.data,
            message=(form.message.data or "").strip() or None,
        )
        db.session.add(lead)
        db.session.flush()

        ActivityLog.record(
            entity_type="lead",
            entity_id=lead.id,
            action="submitted",
            description=f"New lead {lead.request_id} submitted via Work With Konvexity.",
        )
        db.session.commit()

        return render_template("public/work_with_konvexity.html", seo=seo, form=WorkWithKonvexityForm(formdata=None), request_id=request_id, submitted=True)

    return render_template("public/work_with_konvexity.html", seo=seo, form=form, request_id=request_id, submitted=False)


@public_bp.route("/schedule-consultation", methods=["GET", "POST"])
@limiter.limit("10 per hour", methods=["POST"])
def schedule_consultation():
    seo = {
        "title": "Schedule a Consultation",
        "description": "Book time with a Konvexity consultant to talk through your organization's goals.",
        "canonical_url": url_for("public.schedule_consultation", _external=True),
        "og_type": "website",
        "og_image": url_for("static", filename="images/brand/konvexity-og.jpg", _external=True),
    }
    form = ScheduleConsultationForm()
    booking_id = None

    if form.validate_on_submit():
        booking_id = next_identifier(scope="consultation", prefix="KVX-MTG")

        booking = ConsultationBooking(
            booking_id=booking_id,
            full_name=form.full_name.data.strip(),
            email=form.email.data.strip().lower(),
            whatsapp_number=form.whatsapp_number.data.strip(),
            company=(form.company.data or "").strip() or None,
            meeting_goal=(form.meeting_goal.data or "").strip() or None,
            preferred_platform=form.preferred_platform.data,
            preferred_date=form.preferred_date.data.strip(),
            preferred_time=form.preferred_time.data.strip(),
        )
        db.session.add(booking)
        db.session.flush()

        ActivityLog.record(
            entity_type="consultation_booking",
            entity_id=booking.id,
            action="submitted",
            description=f"New consultation request {booking.booking_id} submitted.",
        )
        db.session.commit()

        return render_template("public/schedule_consultation.html", seo=seo, form=ScheduleConsultationForm(formdata=None), booking_id=booking_id, submitted=True)

    return render_template("public/schedule_consultation.html", seo=seo, form=form, booking_id=booking_id, submitted=False)


@public_bp.route("/sitemap.xml")
def sitemap():
    pages = [
        {"loc": url_for("public.home", _external=True), "priority": "1.0"},
        {"loc": url_for("public.about", _external=True), "priority": "0.8"},
        {"loc": url_for("public.solutions", _external=True), "priority": "0.9"},
        {"loc": url_for("public.pricing", _external=True), "priority": "0.8"},
        {"loc": url_for("public.programs", _external=True), "priority": "0.8"},
        {"loc": url_for("public.faculty", _external=True), "priority": "0.7"},
        {"loc": url_for("public.founder", _external=True), "priority": "0.8"},
        {"loc": url_for("public.signature_platforms", _external=True), "priority": "0.8"},
        {"loc": url_for("public.brand_portfolio", _external=True), "priority": "0.8"},
        {"loc": url_for("public.brand_portfolio_detail", slug="gesai", _external=True), "priority": "0.6"},
        {"loc": url_for("public.brand_portfolio_detail", slug="tab", _external=True), "priority": "0.6"},
        {"loc": url_for("public.brand_portfolio_detail", slug="lwb", _external=True), "priority": "0.6"},
        {"loc": url_for("public.arakunrin", _external=True), "priority": "0.6"},
        {"loc": url_for("public.ken", _external=True), "priority": "0.6"},
        {"loc": url_for("public.clients", _external=True), "priority": "0.6"},
        {"loc": url_for("public.contact", _external=True), "priority": "0.7"},
        {"loc": url_for("public.work_with_konvexity", _external=True), "priority": "0.9"},
        {"loc": url_for("public.schedule_consultation", _external=True), "priority": "0.9"},
        {"loc": url_for("public.resources", _external=True), "priority": "0.6"},
    ]
    sitemap_xml = render_template("public/sitemap.xml", pages=pages)
    return sitemap_xml, 200, {"Content-Type": "application/xml"}
