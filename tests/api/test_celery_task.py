import pytest
from app.celery_tasks.send_email import send_welcome_email_task, send_reminder_order_email_task


@pytest.fixture
def mocked_send_welcome_email_task(mocker):
    return mocker.patch("app.celery_tasks.send_email.send_welcome_email_task.delay", return_value=None)


def test_send_welcome_email_task(mocked_send_welcome_email_task):

    mail_to = "test@gmail.com"
    mail_data = {
        "subject": "Test Subject",
        "body": "Test Body"
    }

    result = send_welcome_email_task.delay(mail_to, mail_data)


    mocked_send_welcome_email_task.assert_called_once_with(mail_to, mail_data)

    assert result == None


@pytest.fixture
def mocked_send_reminder_email(mocker):
    return mocker.patch("app.celery_tasks.send_email.send_reminder_order_email_task.delay)", return_value=None)

def test_send_reminder_email_task(mocked_send_reminder_email):
    result = send_reminder_order_email_task.delay()


    mocked_send_reminder_email.assert_called_once_with(None)

    assert result == None