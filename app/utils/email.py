from smtplib import SMTP
from email.mime.text import MIMEText
from app.core.config import settings

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_SENDER_EMAIL}>"
    msg["To"] = to_email

    with SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        smtp.sendmail(settings.SMTP_SENDER_EMAIL, to_email, msg.as_string())

def otp_email_body(username, otp):
    return f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #000000; line-height: 1.5;">
            <p style="color: #000000;">Hello <b>{username}</b>,</p>
            <p style="color: #000000;">We received a request to reset your password. Please use the following OTP to proceed:</p>
            <p style="font-family: monospace; border: 1px solid #ccc; padding: 10px; display: inline-block; color: #000000;">
                <b>OTP: {otp}</b>
            </p>
            <p style="color: #000000;">This OTP is valid for <b>15 minutes</b>. Please do not share it with anyone.</p>
            <p style="color: #000000;">If you did not request this, please ignore this email or contact our support team.</p>
            <br>
            <p style="color: #000000;">Best regards,<br>
                <b>The {settings.PROJECT_NAME} Team</b>
            </p>
        </body>
        </html>
    """


def verify_email_body(username, otp):
    return f"""
        <html>
        <body style="font-family: Arial, sans-serif; color: #000000; line-height: 1.5;">
            <p style="color: #000000;">Hello <b>{username}</b>,</p>
            <p style="color: #000000;">We received a request to verify your email address. Please use the following verification code to proceed:</p>
            <p style="font-family: monospace; border: 1px solid #ccc; padding: 10px; display: inline-block; color: #000000;">
                <b>Verification Code: {otp}</b>
            </p>
            <p style="color: #000000;">This code is valid for <b>15 minutes</b>. Please do not share it with anyone.</p>
            <p style="color: #000000;">If you did not request this, please ignore this email or contact our support team.</p>
            <br>
            <p style="color: #000000;">Best regards,<br>
                <b>The {settings.PROJECT_NAME} Team</b>
            </p>
        </body>
        </html>
    """
