from sqlalchemy.ext.asyncio import AsyncSession

async def get_user(db: AsyncSession, user_id: int):
    return await db.query(models.User).filter(models.User.id == user_id).first()

async def get_user_by_email(db: AsyncSession, email: str):
    return await db.query(models.User).filter(models.User.email == email).first()

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    return await db.query(models.User).offset(skip).limit(limit).all()

async def create_user(db: AsyncSession, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
