import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
from datetime import datetime, timedelta
import jwt
from uuid import uuid4

from app.main import app
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from app.models.mind_map import MindMap
from app.models.node import Node
from app.models.edge import Edge
from app.models.template import Template

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

# Test data fixtures
@pytest.fixture
def test_user(db):
    user = User(
        id=uuid4(),
        email="test@example.com",
        name="Test User",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def test_mind_map(db, test_user):
    mind_map = MindMap(
        id=uuid4(),
        title="Test Mind Map",
        owner_id=test_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(mind_map)
    db.commit()
    return mind_map

@pytest.fixture
def test_node(db, test_mind_map):
    node = Node(
        id=uuid4(),
        mind_map_id=test_mind_map.id,
        content="Test Node",
        position={"x": 0, "y": 0},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(node)
    db.commit()
    return node

@pytest.fixture
def test_edge(db, test_node):
    target_node = Node(
        id=uuid4(),
        mind_map_id=test_node.mind_map_id,
        content="Target Node",
        position={"x": 100, "y": 100},
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(target_node)
    db.commit()
    
    edge = Edge(
        id=uuid4(),
        source_id=test_node.id,
        target_id=target_node.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(edge)
    db.commit()
    return edge

@pytest.fixture
def test_template(db):
    template = Template(
        id=uuid4(),
        name="Test Template",
        description="Test template description",
        nodes=[{"content": "Root", "position": {"x": 0, "y": 0}}],
        edges=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(template)
    db.commit()
    return template

@pytest.fixture
def test_token(test_user):
    to_encode = {
        "sub": str(test_user.id),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

@pytest.fixture
def auth_headers(test_token):
    return {"Authorization": f"Bearer {test_token}"} 