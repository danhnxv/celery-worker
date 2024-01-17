from celery_config import celery
from app.services.send_email import send_mail
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
        # Sending mail
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

        page_size = 100
        chunk_size = 10

        total_users_count = user_repository.get_total_non_buying_users()

        total_pages = (total_users_count + page_size - 1) // page_size
        
        for x in range(0, total_pages):
            chunk_customers_data = []

            non_buying_customers = user_repository.get_users_has_not_order(page_index=x+1, page_size=page_size)

            serialized_non_buying_customers_list = [customer.to_dict() for customer in non_buying_customers]

            chunk_customers_data = [serialized_non_buying_customers_list[i:i + chunk_size] for i in range(0, len(serialized_non_buying_customers_list), chunk_size)]
    
            chunk_customer_email_tasks = [
                group(
                    send_reminder_order_email_to_chunk_customers_task.s(chunks_customer)
                    for chunks_customer in chunk_customers_data
                )
            ]
            group(chunk_customer_email_tasks).apply_async()

        
    except Exception as e:
        print(f"Send email failed!: {str(e)}")


@celery.task(ignore_result=True)
def send_reminder_order_email_to_chunk_customers_task(chunk_customers: list[dict]):
    try:
        customer_email_tasks = [
            group(
                send_welcome_email_task.s(mail_to=customer['email'], mail_data=mail_data)
                for customer in chunk_customers
            )
        ]
        group(customer_email_tasks).apply_async()
    except Exception as e:
        print(f"Send email failed!: {str(e)}")