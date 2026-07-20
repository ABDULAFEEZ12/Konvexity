import uuid
from datetime import datetime, timezone

from app.extensions import db


def generate_uuid():
    return str(uuid.uuid4())


class TimestampMixin:
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


faculty_programs = db.Table(
    "faculty_programs",
    db.Column("faculty_id", db.String(36), db.ForeignKey("faculty.id", ondelete="CASCADE"), primary_key=True),
    db.Column("program_id", db.String(36), db.ForeignKey("programs.id", ondelete="CASCADE"), primary_key=True),
)


class Faculty(TimestampMixin, db.Model):
    __tablename__ = "faculty"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    credentials = db.Column(db.String(200), nullable=True)
    expertise = db.Column(db.JSON, nullable=False, default=list)
    bio = db.Column(db.Text, nullable=False)
    long_bio = db.Column(db.Text, nullable=True)
    photo_url = db.Column(db.String(500), nullable=True)
    social_links = db.Column(db.JSON, nullable=True, default=dict)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    programs = db.relationship("Program", secondary=faculty_programs, back_populates="faculty_members")
    articles = db.relationship("Post", back_populates="author", foreign_keys="Post.author_id")

    def __repr__(self):
        return f"<Faculty {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def initials(self):
        return f"{self.first_name[0]}{self.last_name[0]}"


class Program(TimestampMixin, db.Model):
    __tablename__ = "programs"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(300), nullable=True)
    category = db.Column(db.String(50), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    detailed_description = db.Column(db.Text, nullable=True)
    learning_outcomes = db.Column(db.JSON, nullable=True, default=list)
    target_audience = db.Column(db.JSON, nullable=True, default=list)
    duration = db.Column(db.String(100), nullable=True)
    format = db.Column(db.String(100), nullable=True)
    icon = db.Column(db.String(100), nullable=True)
    hero_image = db.Column(db.String(500), nullable=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    solution_id = db.Column(db.String(36), db.ForeignKey("solutions.id", ondelete="SET NULL"), nullable=True)
    solution = db.relationship("Solution", back_populates="programs")
    faculty_members = db.relationship("Faculty", secondary=faculty_programs, back_populates="programs")
    testimonials = db.relationship("Testimonial", back_populates="program")
    applications = db.relationship("Application", back_populates="program")

    def __repr__(self):
        return f"<Program {self.title}>"


class Solution(TimestampMixin, db.Model):
    __tablename__ = "solutions"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    name = db.Column(db.String(200), nullable=False)
    tagline = db.Column(db.String(300), nullable=True)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.JSON, nullable=True, default=list)
    icon = db.Column(db.String(100), nullable=True)
    illustration = db.Column(db.String(500), nullable=True)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    programs = db.relationship("Program", back_populates="solution")

    def __repr__(self):
        return f"<Solution {self.name}>"


class Testimonial(TimestampMixin, db.Model):
    __tablename__ = "testimonials"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    client_name = db.Column(db.String(200), nullable=False)
    client_title = db.Column(db.String(200), nullable=True)
    client_company = db.Column(db.String(200), nullable=True)
    quote = db.Column(db.Text, nullable=False)
    featured = db.Column(db.Boolean, nullable=False, default=False)
    avatar_url = db.Column(db.String(500), nullable=True)
    company_logo_url = db.Column(db.String(500), nullable=True)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    program_id = db.Column(db.String(36), db.ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    program = db.relationship("Program", back_populates="testimonials")

    def __repr__(self):
        return f"<Testimonial {self.client_name}>"


class Client(TimestampMixin, db.Model):
    __tablename__ = "clients"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    company_name = db.Column(db.String(200), nullable=False)
    industry = db.Column(db.String(100), nullable=True)
    logo_url = db.Column(db.String(500), nullable=False)
    case_study_url = db.Column(db.String(500), nullable=True)
    display_order = db.Column(db.Integer, nullable=False, default=0)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        return f"<Client {self.company_name}>"


class Post(TimestampMixin, db.Model):
    __tablename__ = "posts"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slug = db.Column(db.String(300), unique=True, nullable=False, index=True)
    title = db.Column(db.String(300), nullable=False)
    excerpt = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text, nullable=True)
    featured_image_url = db.Column(db.String(500), nullable=True)
    category = db.Column(db.String(100), nullable=True, index=True)
    tags = db.Column(db.JSON, nullable=True, default=list)
    seo_meta = db.Column(db.JSON, nullable=True, default=dict)
    published_at = db.Column(db.DateTime(timezone=True), nullable=True)
    is_published = db.Column(db.Boolean, nullable=False, default=False)

    author_id = db.Column(db.String(36), db.ForeignKey("faculty.id", ondelete="SET NULL"), nullable=True)
    author = db.relationship("Faculty", back_populates="articles", foreign_keys=[author_id])

    def __repr__(self):
        return f"<Post {self.title}>"


class Event(TimestampMixin, db.Model):
    __tablename__ = "events"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slug = db.Column(db.String(300), unique=True, nullable=False, index=True)
    title = db.Column(db.String(300), nullable=False)
    description = db.Column(db.Text, nullable=True)
    event_type = db.Column(db.String(50), nullable=False, default="in_person")
    start_date = db.Column(db.DateTime(timezone=True), nullable=True)
    end_date = db.Column(db.DateTime(timezone=True), nullable=True)
    location = db.Column(db.String(500), nullable=True)
    registration_url = db.Column(db.String(500), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=True)
    featured_image_url = db.Column(db.String(500), nullable=True)
    is_published = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Event {self.title}>"


class ContactInquiry(TimestampMixin, db.Model):
    __tablename__ = "contact_inquiries"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(300), nullable=False, index=True)
    phone = db.Column(db.String(50), nullable=True)
    company = db.Column(db.String(300), nullable=True)
    role = db.Column(db.String(200), nullable=True)
    inquiry_type = db.Column(db.String(50), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    program_interest_id = db.Column(db.String(36), db.ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    is_responded = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<ContactInquiry {self.name} - {self.inquiry_type}>"


class Application(TimestampMixin, db.Model):
    __tablename__ = "applications"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(300), nullable=False, index=True)
    phone = db.Column(db.String(50), nullable=True)
    company = db.Column(db.String(300), nullable=True)
    role = db.Column(db.String(200), nullable=True)
    linkedin_url = db.Column(db.String(500), nullable=True)
    statement_of_interest = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), nullable=False, default="pending")
    reviewed_by = db.Column(db.String(36), nullable=True)
    reviewed_at = db.Column(db.DateTime(timezone=True), nullable=True)

    program_id = db.Column(db.String(36), db.ForeignKey("programs.id", ondelete="SET NULL"), nullable=True)
    program = db.relationship("Program", back_populates="applications")

    def __repr__(self):
        return f"<Application {self.first_name} {self.last_name}>"


class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    email = db.Column(db.String(300), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="learner", index=True)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    email_verified = db.Column(db.Boolean, nullable=False, default=False)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return f"<User {self.email}>"


class Media(TimestampMixin, db.Model):
    __tablename__ = "media"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    filename = db.Column(db.String(500), nullable=False)
    original_filename = db.Column(db.String(500), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    alt_text = db.Column(db.String(300), nullable=True)
    caption = db.Column(db.String(500), nullable=True)
    folder = db.Column(db.String(100), nullable=False, default="general")

    uploaded_by = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    def __repr__(self):
        return f"<Media {self.filename}>"


class Page(TimestampMixin, db.Model):
    __tablename__ = "pages"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    title = db.Column(db.String(300), nullable=False)
    meta_description = db.Column(db.String(500), nullable=True)
    content_blocks = db.Column(db.JSON, nullable=True, default=list)
    is_published = db.Column(db.Boolean, nullable=False, default=False)

    updated_by = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    def __repr__(self):
        return f"<Page {self.title}>"