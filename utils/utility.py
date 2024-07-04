import random

from app.models import User


class Utility:

    @classmethod
    async def generate_four_digit_number(cls):
        return random.randint(1000, 9999)

    @classmethod
    async def get_jwt_payload(cls, user: User) -> dict:
        user_data = user.__dict__
        return dict(
            sub=user_data['id'],
            username=user_data['username'],
        )

    @classmethod
    async def send_code_email(cls, email, code):
        subject = "Soff.uz"
        body = render_to_string('email.html', {'code': code})
        em = EmailMessage()
        em['Message-ID'] = str(uuid.uuid4())
        em['From'] = EMAIL
        em['To'] = email
        em['Subject'] = subject
        em.set_content(body, subtype='html')
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(EMAIL_HOST, 465, context=context) as smtp:
            smtp.login(EMAIL, EMAIL_PASSWORD)
            smtp.sendmail(EMAIL, email, em.as_string())


UTILITY = Utility()
