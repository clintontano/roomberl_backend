from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class EmailService:
    @staticmethod
    def send_email(
        subject="",
        body="",
        to_emails=None,
        attachments=None,
        *args,
        **kwargs,
    ):
        if to_emails is None:
            to_emails = []

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to_emails,
        )
        email.content_subtype = "html"

        if attachments:
            for attachment in attachments:
                email.attach(
                    attachment["filename"],
                    attachment["file_content"],
                    "application/octet-stream",
                )

        try:
            email.send()
        except Exception as e:
            print(f"Error sending email: {e}")


class CoreService:
    @staticmethod
    def send_email(
        subject="",
        template_path="",
        to_emails=list,
        template_context=None,
        attachments=None,
        **kwargs,
    ):
        """SEND EMAIL"""

        # if settings.DEBUG:
        #     print(f"Sending email to {to_emails}")
        #     return

        html_content = render_to_string(template_path, template_context)

        EmailService.send_email(
            subject=subject,
            body=html_content,
            to_emails=to_emails,
            attachments=attachments,
        )
