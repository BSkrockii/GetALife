from django.test import TestCase


# Create your tests here.

class TestCalls(TestCase):
    def test_call_view_deny_anonymous(self):
        response = self.client.get('/home/', follow=True)
        self.assertRedirects(response, '/login/')