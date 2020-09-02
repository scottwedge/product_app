from django.contrib.auth import get_user_model
import pytest
from graphql_jwt.testcases import JSONWebTokenTestCase
from backend.Apps.user.models import User


#? Testing creation of a user with minimum fields required
@pytest.fixture
def create_user(db):
    def make_user(**kwargs):
        return User.objects.create(**kwargs)
    return make_user

def test_fixture_create_user(create_user):
    user = create_user(username='foo', password='bar')
    assert user.is_authenticated is True



#? Testing user authentication with jwt
class UsersTests(JSONWebTokenTestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='test')
        self.client.authenticate(self.user)

    def test_get_user(self):
        query = '''
        query GetUser($username: String!) {
            user(username: $username) {
                id
            }
        }'''

        variable_values = {
            'username': self.user.username,
        }

        self.client.execute(query, variable_values)

