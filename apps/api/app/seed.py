import asyncio

from sqlalchemy import select

from app.database import async_session_maker
from app.models.company import Company
from app.models.user import User
from app.security.security import get_password_hash


async def seed() -> None:
    async with async_session_maker() as session:
        company = await session.scalar(
            select(Company).where(Company.name == "Acmenra Studio (Поставщик)")
        )
        if company is None:
            company = Company(name="Acmenra Studio (Поставщик)")
            session.add(company)
            await session.flush()

        email = "admin@acmenra.ru"
        admin = await session.scalar(select(User).where(User.email == email))
        if admin is None:
            session.add(
                User(
                    email=email,
                    hashed_password=get_password_hash("admin123"),
                    role="provider_admin",
                    company_id=None,
                )
            )

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
