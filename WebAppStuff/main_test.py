import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()

    r = client.get('/')
