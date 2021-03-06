from global_test_case import GlobalTestCase as TestCase, popit_load_data
from django.core.urlresolvers  import reverse
from django.core.urlresolvers import reverse as original_reverse
from ...models import WriteItInstance
from django.contrib.auth.models import User
from django.test.client import Client, RequestFactory
from ..views import WriteItInstanceUpdateView
from django.forms import ModelForm
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.translation import activate
from ..forms import WriteItInstanceBasicForm, WriteItInstanceAdvancedUpdateForm, \
                            WriteItInstanceCreateForm
from popit.models import Person
from django.forms.models import model_to_dict
from contactos.models import Contact
from contactos.forms import ContactCreateForm
from ..forms import NewAnswerNotificationTemplateForm, ConfirmationTemplateForm
from mailit.forms import MailitTemplateForm
from .user_section_views_tests  import UserSectionTestCase


class DeleteAnInstanceTestCase(UserSectionTestCase):
    def setUp(self):
        super(DeleteAnInstanceTestCase, self).setUp()
        self.writeitinstance = WriteItInstance.objects.all()[0]
        self.writeitinstance.owner = self.user
        self.writeitinstance.save()

    def test_delete_url(self):
        '''There is a url to delete a writeitinstance'''
        url = reverse('delete_an_instance', kwargs={'pk':self.writeitinstance.id})
        self.assertTrue(url)

    def test_get_to_url(self):
        '''Get the delete a WriteItInstance url returns a check if deleting'''
        instance_id = self.writeitinstance.id
        url = reverse('delete_an_instance', kwargs={'pk':instance_id})
        c = Client()
        c.login(username="fiera", password="feroz")
        response = c.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'nuntium/profiles/writeitinstance_check_delete.html')
        #It's not yet deleted
        self.assertTrue(WriteItInstance.objects.get(id=instance_id))


    def test_post_to_url(self):
        '''When I post to the URL then it deletes the writeitinstance'''
        instance_id = self.writeitinstance.id
        url = reverse('delete_an_instance', kwargs={'pk':instance_id})
        c = Client()
        c.login(username="fiera", password="feroz")
        response = c.post(url)
        # Now it should be deleted
        self.assertFalse(WriteItInstance.objects.filter(id=instance_id))


        your_instances_url = reverse('your-instances')
        self.assertRedirects(response, your_instances_url)


    def test_get_if_not_logged_in(self):
        '''If I'm not logged in I cannot get the writeit instance delete url'''
        instance_id = self.writeitinstance.id
        url = reverse('delete_an_instance', kwargs={'pk':instance_id})
        c = Client()
        # this line is intentionally commented so I can show that I'm not logged in
        # c.login(username="fiera", password="feroz")
        # this line is intentionally commented so I can show that I'm not logged in
        response = c.get(url)
        self.assertEquals(response.status_code, 404)


    def test_post_if_not_logged_in(self):
        '''If I'm not logged in I cannot post to the writeit instance delete url'''
        instance_id = self.writeitinstance.id
        url = reverse('delete_an_instance', kwargs={'pk':instance_id})
        c = Client()
        # this line is intentionally commented so I can show that I'm not logged in
        # c.login(username="fiera", password="feroz")
        # this line is intentionally commented so I can show that I'm not logged in
        response = c.post(url)
        self.assertEquals(response.status_code, 404)

