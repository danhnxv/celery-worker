from celery_config import celery
from app.services.email_service import send_mail
from app.database import connect
from app.repository.user import user_repository
from celery import group

mail_data = {
    "subject": "Let's order",
    "body": "Purchase items that bring you joy"
}

@celery.task(ignore_result=True)
def send_welcome_email_task(mail_to: str, mail_data: dict):
    try:
        print("Mail is sending...")
        send_mail(mail_to, mail_data)
        print("Mail has been sent!!!")
    except Exception as e:
        print(f"Send email failed!: {str(e)}")

@celery.task(ignore_result=True)
def send_reminder_order_email_task():
    try:
        # Connecting db
        connect()

        # Handle send email
        non_buying_customers = user_repository.get_user_has_not_order()
        chunk_customers_data = []
        chunk_size = 10
        for i in range(0, len(non_buying_customers), 10):
            chunk_customers_data.append(non_buying_customers[i:i + chunk_size])

        for chunk_customers_item in chunk_customers_data:
            email_tasks = [
                send_welcome_email_task.s(mail_to=customer.email, mail_data=mail_data)
                for customer in chunk_customers_item
            ]
            group(email_tasks).apply_async()
        
    except Exception as e:
        print(f"Send email failed!: {str(e)}")