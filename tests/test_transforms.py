"""
Test JMESPath transformation functionality
"""
from apibridgepro.transforms import apply_transform_jmes


def test_simple_jmespath_transform():
    """Test basic JMESPath transformation"""
    data = {
        "temperature": 25.5,
        "humidity": 60,
        "location": "Bogota"
    }
    meta = {"provider": "test", "status": 200}

    expr = "{temp: temperature, place: location, source: meta.provider}"
    result = apply_transform_jmes(data, expr, meta)

    assert result == {
        "temp": 25.5,
        "place": "Bogota",
        "source": "test"
    }


def test_transform_with_no_expression():
    """Test that no expression returns original data"""
    data = {"field": "value"}
    meta = {}

    result = apply_transform_jmes(data, None, meta)
    assert result == data

    result = apply_transform_jmes(data, "", meta)
    assert result == data


def test_transform_provider_unification():
    """Test unifying responses from different providers"""
    # OpenWeatherMap format
    owm_data = {
        "main": {
            "temp": 298.15,  # Kelvin
            "humidity": 65
        },
        "name": "Bogota"
    }

    # Simpler transform that actually works with JMESPath
    owm_expr = """{
        "temp_c": main.temp,
        "humidity": main.humidity,
        "city": name
    }"""

    meta = {"provider": "openweather"}
    owm_result = apply_transform_jmes(owm_data, owm_expr, meta)
    assert owm_result["temp_c"] == 298.15
    assert owm_result["humidity"] == 65
    assert owm_result["city"] == "Bogota"

    # WeatherAPI format
    weatherapi_data = {
        "current": {
            "temp_c": 25.0,
            "humidity": 65
        },
        "location": {
            "name": "Bogota"
        }
    }

    wa_expr = """{
        "temp_c": current.temp_c,
        "humidity": current.humidity,
        "city": location.name
    }"""

    meta = {"provider": "weatherapi"}
    wa_result = apply_transform_jmes(weatherapi_data, wa_expr, meta)
    assert wa_result["temp_c"] == 25.0
    assert wa_result["humidity"] == 65
    assert wa_result["city"] == "Bogota"


def test_transform_with_meta_injection():
    """Test that meta is accessible in transforms"""
    data = {"value": 100}
    meta = {"provider": "test-provider", "latency_ms": 150}

    expr = "{value: value, provider: meta.provider, latency: meta.latency_ms}"
    result = apply_transform_jmes(data, expr, meta)

    assert result["value"] == 100
    assert result["provider"] == "test-provider"
    assert result["latency"] == 150


def test_transform_invalid_expression_fails_open():
    """Test that invalid JMESPath fails open (returns original data)"""
    data = {"field": "value"}
    meta = {}

    # Invalid JMESPath expression
    expr = "this[is{invalid}]syntax"
    result = apply_transform_jmes(data, expr, meta)

    # Should return original data on error
    assert result == data


def test_transform_with_array_data():
    """Test transforms on non-dict data (wrapped in envelope)"""
    data = [1, 2, 3, 4, 5]
    meta = {"provider": "test"}

    expr = "data[0]"
    result = apply_transform_jmes(data, expr, meta)

    assert result == 1

