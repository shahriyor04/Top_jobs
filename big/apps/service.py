from django.contrib.auth.models import User
from reportlab.lib.pagesizes import A4


def add_profile_section(c, resume_instance):
    # Profile Section
    w, h = A4
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0, 51, 102)  # Dark blue color
    c.drawString(50, h - 150, "Profile")
    c.setFillColorRGB(0, 0, 0)  # Black color
    c.setFont("Helvetica", 14)
    c.drawString(50, h - 180, f"Phone: {resume_instance.phone_number}")
    c.drawString(50, h - 200, f"Email: {resume_instance.user.email}")
    c.drawString(50, h - 220, f"GitHub: {resume_instance.github}")
    c.drawString(50, h - 260, f"Reside in: {resume_instance.address}")


def add_education_section(c, resume_instance):
    # Education Section
    w, h = A4
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0, 51, 102)  # Dark blue color
    c.drawString(50, h - 340, "Education")
    c.setFillColorRGB(0, 0, 0)  # Black color
    c.setFont("Helvetica", 16)
    c.drawString(50, h - 370, f"School: {resume_instance.school}")
    c.setFont("Helvetica", 14)
    c.drawString(50, h - 390, f"Major: {resume_instance.education_direction}")
    c.drawString(50, h - 410, f"Graduation Date: {resume_instance.education_date}")


#
def add_work_experience_section(c, resume_instance):
    # Work Experience Section
    w, h = A4
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0, 51, 102)  # Dark blue color
    c.drawString(50, h - 450, "Desired position")
    c.setFillColorRGB(0, 0, 0)  # Black color
    c.setFont("Helvetica", 18)
    c.drawString(50, h - 480, f"{resume_instance.job}")
    c.setFont("Helvetica", 14)
    c.drawString(50, h - 500, f"Employment: {resume_instance.working_time}")


def add_skills(c, resume_instance):
    # Work Experience Section
    w, h = A4
    c.setFont("Helvetica-Bold", 18)
    c.setFillColorRGB(0, 51, 102)  # Dark blue color
    c.drawString(50, h - 530, "Skills ")
    c.setFillColorRGB(0, 0, 0)  # Black color
    c.setFont("Helvetica", 16)
    skills_lens = resume_instance.skills.split(', ') and resume_instance.skills.split(',')
    y_coordinate = h - 560
    line_height = 20
    for line in skills_lens:
        c.drawString(50, y_coordinate, line)
        y_coordinate -= line_height
