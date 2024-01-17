from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from app.models.user import User as UserModel
from app.schema.user import UserBase, UserInDB, UserBase
from fastapi import Body
from app.repository.user import UserRepository
from app.celery_tasks.send_email import send_welcome_email_task

router = APIRouter()

mail_data = {
    "subject": "Welcome to my store",
    "body": "Welcome!!!!"
}

@router.get("", response_model=List[UserInDB])
async def get_users(page_index: Optional[int] = 1, page_size: Optional[int] = 100, user_repository: UserRepository = Depends(UserRepository)):
    try:
        existing_user = user_repository.get_users_has_not_order(page_index=page_index, page_size=page_size)
        return existing_user
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"Error": str(e)}

@router.post("")
async def create_user(user: UserBase = Body(...), user_repository: UserRepository = Depends(UserRepository)):
    try:
        # Creating user
        existing_user = user_repository.get_user_by_email(email=user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
        
        new_user = UserInDB(**user.model_dump())
        user = user_repository.create(obj_in=new_user)

        # Running send email task
        send_welcome_email_task.delay(mail_to=user.email, mail_data=mail_data)

        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        return {"Error": str(e)}