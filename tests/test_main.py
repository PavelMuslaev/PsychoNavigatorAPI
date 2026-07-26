from src.psycho_navigator.main import create_app


def test_create_app(settings):
    app = create_app(settings)

    assert app.title == "Test API"
    assert app.version == "3.0.0"
    assert app.debug is True
