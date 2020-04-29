from django.test import TestCase, Client


# Create your tests here.

class TestCalls(TestCase):
    def test_call_view_deny_anonymous(self):
        response = self.client.get('/home/', follow=True)
        self.assertRedirects(response, '/login/')

# Create your tests here.
class JenkinsTest(TestCase):

    def test_JenkinsRunOne(self):
        self.assertEqual(1, 1)
        print("Test")

    def test_JenkinsRuntwo(self):
        self.assertEqual(1, 1)
        print("Test")
