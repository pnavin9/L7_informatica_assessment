"""Pytest configuration and fixtures."""

import os
import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db

# Import after to avoid triggering main app initialization
from app.db.database import Base


@pytest.fixture(scope="session")
def engine():
    """Create a test database engine."""
    # Create a temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    TEST_DATABASE_URL = f"sqlite:///{db_path}"

    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

    yield engine

    # Cleanup
    engine.dispose()
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def db_session(engine):
    """Create a fresh database for each test."""
    from app.db.seed_data import seed_database

    # Create all tables
    Base.metadata.create_all(bind=engine)

    # Create session
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    # Seed the test database
    try:
        seed_database(session)
    except Exception:
        session.rollback()

    yield session

    # Cleanup
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database."""
    from app.main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def empty_db(engine):
    """Create an empty database for testing edge cases."""
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)
