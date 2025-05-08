from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME="your@gmail.com",
    MAIL_PASSWORD="your-password-or-app-password",
    MAIL_FROM="your@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
) # SMTP 설정

async def send_reset_email(to_email: str, reset_token: str):
    message = MessageSchema(
        subject="비밀번호 재설정",
        recipients=[to_email],
        body=f"<a href='https://yourapp.com/reset-password?token={reset_token}'>비밀번호 재설정</a>",
        subtype="html"
    )
    fm = FastMail(conf)
    await fm.send_message(message)