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

# every def, put variable Client() (ex: c = Client())

# for csrf, c = Client(enforce_csrf_checks=True)
# can have HTTP_USER_AGENTS HTTP_USER_AGENT=''
# 


#self.client.session, self.client.cookies


# response = c.post(url, { data})
    # follow=True, allows to go thru redirects
    # content_type = 'application/json'  Can also do json.dumps()
# response.status_code

# response = c.get(url)
# response.content

# cannot test cors directly

# theres delete

# theres login

# theres logout

#IS STATEFUL.  KEEPS COOKIES.

# Response:
    #client, content (body), context

    #json()
    # request

    # status_code

    # templates

    #


#SimpleTestCase
    # tests exceptions, warnings, render and error treatments
    # Verify templates

    #2 urls are equal


# TestCase
    # def setUpTestData
        #sets up dataa

    #Everything must be setup inside the methods


# SimpleTestCase.assertContains(response,text, count, status_code, msgprefix, html = False)
# SimpleTestCase.assertNotContains(response,text, count, status_code, msgprefix, html = False
# SimpleTestCase.assertTemplateUsed(response,text, count, status_code, msgprefix, html = False
# SimpleTestCase.assertJSONEqual(raw, expected)
# SimpleTestCase.assertJSONNotEqual(raw, expected)




# Rest framework
    # APIRequestFactory(enforce_csrf_checks=True)
        #has .get, post, put, patch, delete
        

    # from rest_framework.test import force_authenticate
    #  force_authenticate(request, user=None, token=None)

    # from rest_framework.test import RequestsClient
    # requestsClient
    # Tests the service interface

    #lient = RequestsClient()

# Obtain a CSRF token.
# response = client.get('http://testserver/homepage/')
# assert response.status_code == 200
# csrftoken = response.cookies['csrftoken']

# # Interact with the API.
# response = client.post('http://testserver/organisations/', json={
#     'name': 'MegaCorp',
#     'status': 'active'
# }, headers={'X-CSRFToken': csrftoken})
# assert response.status_code == 200