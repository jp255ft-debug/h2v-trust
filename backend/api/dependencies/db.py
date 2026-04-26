from db.database import get_db as get_db_session


def get_db():
    """Dependency to get database session."""
    db_gen = get_db_session()
    try:
        db = next(db_gen)
        yield db
    finally:
        next(db_gen, None)  # Ensure generator is closed

