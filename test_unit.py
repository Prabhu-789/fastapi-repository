import pytest
from unittest.mock import MagicMock
from schemas import RegisteredUserCreate
from services import UserService
import bcrypt
from models import RegisteredUser

@pytest.fixture
def mock_db():
    return MagicMock()

def test_register_user(mock_db):
    # Mock user data
    Ruser = RegisteredUserCreate(name="testuser", password="testpassword")

    # Mock the db session and UserService
    user_service = UserService(mock_db)

    # Mock bcrypt hash
    mock_hashed_password = bcrypt.hashpw(Ruser.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Mock RegisteredUser object
    mock_user = RegisteredUser(name=Ruser.name, hashed_password=mock_hashed_password)

    # Simulate the database operations
    mock_db.add.return_value = None
    mock_db.commit.return_value = None
    mock_db.refresh.return_value = mock_user

    # Call the register_user method
    result = user_service.register_user(Ruser)

    # Assertions
    assert result.name == Ruser.name
    assert bcrypt.checkpw(Ruser.password.encode('utf-8'), result.hashed_password.encode('utf-8'))

    # Check that mock_db.add was called with a user object with the correct attributes
    added_user = mock_db.add.call_args[0][0]  # get the user object passed to add()
    assert added_user.name == Ruser.name
    assert bcrypt.checkpw(Ruser.password.encode('utf-8'), added_user.hashed_password.encode('utf-8'))

    mock_db.commit.assert_called_once()


def test_get_all_registered_users(mock_db):
    # Mock UserService and RegisteredUser data
    user_service = UserService(mock_db)
    
    # Create mock user list
    mock_users = [RegisteredUser(name="user1", hashed_password="password1"), 
                  RegisteredUser(name="user2", hashed_password="password2")]
    
    # Simulate DB query
    mock_db.query().all.return_value = mock_users
    
    # Call the method
    result = user_service.get_all_registered_users()
    
    # Assertions
    assert len(result) == 2
    assert result[0].name == "user1"
    assert result[1].name == "user2"
