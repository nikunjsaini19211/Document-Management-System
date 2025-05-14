from setuptools import setup, find_packages

setup(
    name="document-management-system",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "python-multipart",
        "alembic",
        "psycopg2-binary",
        "python-dotenv",
        "pytest",
        "httpx",
        "email-validator",
        "pytest-asyncio"
    ],
) 