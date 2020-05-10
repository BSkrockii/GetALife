from django.test import TestCase, Client
from django.contrib.auth.models import User

# Create your tests here.

class TestCalls(TestCase):
    def setUp(self):
        user = User.objects.create(username='temporary', email='temporary@gmail.com', is_active=True)
        user.set_password('temporary')
        user.save()

    def test_home_redirect_login(self):
        response = self.client.get('/home/', follow=True)
        self.assertRedirects(response, '/login/')

    def test_home_grant_authenticated(self):
        c = Client()
        c.login(username='temporary', password='temporary')
        response = c.get('/home/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'life/dashboard.html')  

    def test_index_goes_to_index(self):
        c = Client()
        response = c.get('/index/', follow=True)
        self.assertTemplateUsed(response, 'life/index.html')    

    def test_index_redirect_to_dashboard(self):
        c = Client()
        c.login(username='temporary', password='temporary')
        response = c.get('/index/', follow=True)
        self.assertRedirects(response, '/dashboard/')  

    def test_finance_render_template(self):
        response = self.client.get('/finance/', follow=True)
        self.assertTemplateUsed(response, 'life/finance.html') 

    def test_cost_render_template(self):
        response = self.client.get('/cost/', follow=True)
        self.assertTemplateUsed(response, 'life/cost.html') 

    def test_pay_render_template(self):
        response = self.client.get('/pay/', follow=True)
        self.assertTemplateUsed(response, 'life/pay.html') 
    
    def test_dashboard_render_template_authenticated(self):
        c = Client()
        c.login(username='temporary', password='temporary')
        response = c.get('/dashboard/', follow=True)
        self.assertTemplateUsed(response, 'life/dashboard.html') 
    
    def test_dashboard_redirect_unauthenticated_user(self):
        response = self.client.get('/dashboard/', follow=True)
        self.assertRedirects(response, '/login/')

    def test_login_redirect_authenticated_user(self):
        c = Client()
        c.login(username='temporary', password='temporary')
        response = c.get('/login/', follow=True)
        self.assertRedirects(response, '/dashboard/')

    def test_login_template_unauthenticated_user(self):
        response = self.client.get('/login/', follow=True)
        self.assertTemplateUsed(response, 'life/login.html')

    def test_faq_template(self):
        response = self.client.get('/faq/', follow=True)
        self.assertTemplateUsed(response, 'life/faq.html')

    def test_about_template(self):
        response = self.client.get('/about/', follow=True)
        self.assertTemplateUsed(response, 'life/about.html')

    def test_signOut_template(self):
        response = self.client.get('/signOut/', follow=True)
        self.assertRedirects(response, '/login/')

    def test_error_400_template(self):
        response = self.client.get('/error_400/', follow=True)
        self.assertTemplateUsed(response, 'life/error_404.html')

    def test_error_403_template(self):
        response = self.client.get('/error_403/', follow=True)
        self.assertTemplateUsed(response, 'life/error_404.html')

    def test_error_404_template(self):
        response = self.client.get('/error_404/', follow=True)
        self.assertTemplateUsed(response, 'life/error_404.html')

    def test_error_500_template(self):
        response = self.client.get('/error_500/', follow=True)
        self.assertTemplateUsed(response, 'life/error_404.html')

    def test_calendarFt_authenticated_template(self):
        c = Client()
        c.login(username='temporary', password='temporary')
        response = c.get('/calendarFt/', follow=True)
        self.assertTemplateUsed(response, 'life/calendarFt.html')

    def test_calendarFt_authenticated_redirect(self):
        response = self.client.get('/calendarFt/', follow=True)
        self.assertRedirects(response, '/login/')

'''
class UnAuthenticatedCallTests(TestCase):
    # setup client
    # Create User 
    def setup():
    
    # Check index/
    def indexTest():

    # Check finance/
    def financeTest():

    # Check cost/
    def cost():

    # Check pay/
    def pay():

    # Check dashboard/
    def dashboard():
    
    # Check login
    # get, then post and check if logged in.  
    # Then, remove all cookies
    def login():

    # Check Failed login
    # get, then post with wrong credentials
    # If logged in, fail test and remove cookies
    def failedLogin():

    # check faq
    def faq():

    #check about
    def about():

    # Check singout
    def signOut():

    # Check if an error.
    # Must create bad request
    def error400():

    # Try to access some authE only url
    # # Home, dashboard
    def error403():
    
    # Try a url that doesnt exist
    def error404():

    # Iternal error...
    # just access error 500 url
    def error500():

    # Must go to login.
    def calenderFt():

    #needs to check authentication.
    def event():
    

class AuthenticatedCallTest(TestCase):
    # Create user
    # Create 2 events
    def setup():
    
    # Should get redirected to dashboard
    def index():

    # Check if it is using dashboard.html
    def dashboard():

    # Check when is unAuthE, and check body to be login.html
    def unauthELogin():

    # Check Login and check if its going to dashboard
    def login():

    # Login and login again to see if its redirected
    def loginRedirection():

    # Check GET and see if we get body
    def registerGET():

    # Check POST to see if we get a session token (logged in)
    def registerPOST():

    # Login and check if we grab events
    def event():

    # Check it events get saved
    def saveEvent():

    # Check if events gets deleted
    def deleteEvent():

    
class restfulApi():
    # Create 2 user
    # Create 2 budget Account
    # Link 1 user to BudgetAccount 1 & 2
    # link 1 user to BudgetAccount 2 only
    # create Budget Income and link to BA 1
    def setup():

    # Check if can change a property in BudgetAccount
    # User must be authenticated in order to do so.
    def setBudgetAccount():

    # login to 1 user with link BA 2
    # Check if get gets 2 BA
    def getOneBudgetAccount():

    # login to 1 user with link BA 1
    # Check if can get 1 BA
    def getTwoBudgetAccount():

    # create budgetAccount 3
    # Add User to BA 3
    # Login to user
    # Check if can access BA 3
    def addUserToBudget():

    # Check if it can change property
    def setBudgetIncome():

    # Check if it can get BI
    def getBudgetIncome():


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
'''