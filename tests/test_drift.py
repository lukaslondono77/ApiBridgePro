"""
Test schema drift detection
"""
from pydantic import BaseModel

from apibridgepro.drift import validate_response


class UserModel(BaseModel):
    """Example schema for testing"""
    id: int
    name: str
    email: str
    age: int | None = None


class WeatherModel(BaseModel):
    """Weather schema for testing"""
    temp_c: float
    humidity: int
    provider: str


def test_valid_response_passes():
    """Test that valid data passes validation"""
    data = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }

    error = validate_response(UserModel, data)
    assert error is None


def test_valid_response_with_optional_field():
    """Test validation with missing optional fields"""
    data = {
        "id": 2,
        "name": "Jane Doe",
        "email": "jane@example.com"
        # age is optional, so omitting it should work
    }

    error = validate_response(UserModel, data)
    assert error is None


def test_invalid_response_returns_error():
    """Test that invalid data returns error message"""
    data = {
        "id": "not-an-int",  # Should be int
        "name": "John Doe",
        "email": "john@example.com"
    }

    error = validate_response(UserModel, data)
    assert error is not None
    assert "validation error" in error.lower()


def test_missing_required_field_returns_error():
    """Test that missing required fields are detected"""
    data = {
        "id": 1,
        # Missing required 'name' and 'email'
    }

    error = validate_response(UserModel, data)
    assert error is not None
    assert "field required" in error.lower() or "missing" in error.lower()


def test_extra_fields_are_ignored():
    """Test that extra fields don't cause validation errors"""
    data = {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30,
        "extra_field": "should be ignored"  # Extra field
    }

    error = validate_response(UserModel, data)
    # Pydantic by default ignores extra fields
    assert error is None


def test_none_model_returns_none():
    """Test that None model always passes"""
    data = {"any": "data"}
    error = validate_response(None, data)
    assert error is None


def test_weather_unified_schema():
    """Test the actual WeatherUnified schema from the app"""
    # Valid data
    valid_data = {
        "temp_c": 25.5,
        "humidity": 60,
        "provider": "openweather"
    }
    error = validate_response(WeatherModel, valid_data)
    assert error is None

    # Invalid data (humidity as string)
    invalid_data = {
        "temp_c": 25.5,
        "humidity": "sixty",  # Should be int
        "provider": "openweather"
    }
    error = validate_response(WeatherModel, invalid_data)
    assert error is not None


