from global_test_case import GlobalTestCase as TestCase
from django.utils.unittest import skip
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.utils.translation import ugettext as _
from contactos.models import Contact, ContactType
from nuntium.models import Message, WriteItInstance, OutboundMessage, MessageRecord, Confirmation
from popit.models import Person, ApiInstance
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import slugify
from django.core import mail
import datetime


class TestMessages(TestCase):

    def setUp(self):
        super(TestMessages,self).setUp()
        self.writeitinstance1 = WriteItInstance.objects.all()[0]
        self.person1 = Person.objects.all()[0]
        self.person2 = Person.objects.all()[1]


    def test_create_message(self):
        message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Fiera es una perra feroz', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])
        self.assertTrue(message)
        self.assertEquals(message.content, "Content 1")
        self.assertEquals(message.subject, "Fiera es una perra feroz")
        self.assertEquals(message.writeitinstance, self.writeitinstance1)
        self.assertEquals(message.slug, slugify(message.subject))
        self.assertTrue(message.public)


    def test_update_a_message_does_not_need_persons(self):
        message1 = Message.objects.all()[0]

        previous_people = message1.people

        message1.slug = 'a-new-slug1'

        message1.save()

        self.assertEquals(message1.people, previous_people)


    def test_message_has_a_permalink(self):
        message1 = Message.objects.all()[0]
        expected_url = reverse('message_detail', kwargs={'slug':message1.slug})

        self.assertEquals(expected_url, message1.get_absolute_url())





    def test_two_messages_with_the_same_subject_but_different_slug(self):
        message1 = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Same subject hey', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])

        message2 = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Same subject hey', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])

        message3 = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Same subject hey', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])


        self.assertEquals(message1.slug, slugify(message1.subject))
        self.assertEquals(message2.slug, slugify(message2.subject)+"-2")
        self.assertEquals(message3.slug, slugify(message3.subject)+"-3")


    def test_a_person_with_two_contacts_method_people(self):
        contact = Contact.objects.create(person=self.person1
            , value=u"another@contact.cl"
            , contact_type=self.person1.contact_set.all()[0].contact_type)
        
        message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Same subject hey', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])


        self.assertEquals(message.people, [self.person1])


    def test_resave_a_message_should_not_change_slug(self):
        #There are a lot of good solutions for this problem but this
        #is the easyest one
        message1 = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Same subject hey', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])
        previous_slug = message1.slug
        #message1 now has a slug
        message1.subject = 'Some other subject and stuff'
        message1.save()

        self.assertEquals(message1.slug, previous_slug)


    def test_a_message_has_a_people_property(self):
        message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Same subject hey', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1, self.person2])

        self.assertEquals(message.people, [self.person1, self.person2])


    def test_message_unicode(self):
        message = Message.objects.create(content = 'Content 1', author_name='Felipe', author_email="falvarez@votainteligente.cl", subject='Subject 1', writeitinstance= self.writeitinstance1, persons = [self.person1])

        self.assertEquals(message.__unicode__(), _('%(subject)s at %(instance)s') % {
            'subject':message.subject,
            'instance':self.writeitinstance1.name
            })

    def test_outboundmessage_create_without_manager(self):
        message = Message(content = 'Content 1', author_name='Felipe', author_email="falvarez@votainteligente.cl", subject='Subject 1', writeitinstance= self.writeitinstance1, persons = [self.person1])
        message.save()

        
        self.assertEquals(message.outboundmessage_set.count(), 1)


    def test_it_creates_outbound_messages_only_once(self):
        message = Message.objects.create(content = 'Content 1', author_name='Felipe', author_email="falvarez@votainteligente.cl", subject='Subject 1', writeitinstance= self.writeitinstance1, persons = [self.person1])
        message.save()

        self.assertEquals(OutboundMessage.objects.filter(message=message).count(), 1)

    def test_it_raises_typeerror_when_no_contacts_are_present(self):
        with self.assertRaises(TypeError):
            Message.objects.create(content = 'Content 1', author_name='Felipe', author_email="falvarez@votainteligente.cl", subject='Subject 1', writeitinstance= self.writeitinstance1)

    def test_message_set_new_outbound_messages_to_ready(self):
        message = Message.objects.create(content = 'Content 1', author_name='Felipe', author_email="falvarez@votainteligente.cl", subject='Subject 1', writeitinstance= self.writeitinstance1, persons = [self.person1])

        message.recently_confirmated()

        outbound_message_to_pedro = OutboundMessage.objects.filter(message=message)[0]
        self.assertEquals(outbound_message_to_pedro.status, 'ready')




class MessageDetailView(TestCase):
    def setUp(self):
        super(MessageDetailView,self).setUp()
        self.writeitinstance1 = WriteItInstance.objects.all()[0]
        self.person1 = Person.objects.all()[0]
        self.message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Subject 1', 
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])
        Confirmation.objects.create(message=self.message, confirmated_at = datetime.datetime.now())


    def test_get_message_detail_page(self):
        #I'm kind of feeling like I need 
        #something like rspec or cucumber
        
        url = reverse('message_detail', kwargs={'slug':self.message.slug})
        self.assertTrue(url)

        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.context['message'], self.message)



class PrivateMessagesTestCase(TestCase):
    def setUp(self):
        super(PrivateMessagesTestCase,self).setUp()
        self.writeitinstance1 = WriteItInstance.objects.all()[0]
        self.person1 = Person.objects.all()[0]
        self.private_message = Message.objects.create(content = 'Content 1', 
            author_name='Felipe', 
            author_email="falvarez@votainteligente.cl", 
            subject='Subject 1', 
            public=False,
            writeitinstance= self.writeitinstance1, 
            persons = [self.person1])
        self.confirmation = Confirmation.objects.create(message=self.private_message)
        

    

    def test_private_messages_confirmation_created_move_from_new_to_needs_moderation(self):
        self.private_message.recently_confirmated()
        outbound_message_to_pedro = OutboundMessage.objects.get(message=self.private_message)
        self.assertEquals(outbound_message_to_pedro.status, 'needmodera')

    def test_outbound_messages_of_a_confirmed_message_are_waiting_for_moderation(self):
        #I need to do a get to the confirmation url
        url = reverse('confirm', kwargs={
            'slug':self.confirmation.key
            })
        response = self.client.get(url)
        #this works proven somewhere else
        outbound_message_to_pedro = OutboundMessage.objects.get(message=self.private_message)
        self.assertEquals(outbound_message_to_pedro.status, 'needmodera')

    def test_when_moderation_needed_a_mail_for_its_owner_is_sent(self):
        self.private_message.recently_confirmated()
        #There should be two 
        #One is created for confirmation
        #The other one is created for the moderation thing
        self.assertEquals(len(mail.outbox),2)
        moderation_mail = mail.outbox[1]
        #it is sent to the owner of the instance
        self.assertEquals(moderation_mail.to[0], self.private_message.writeitinstance.owner.email)
        self.assertTrue(self.private_message.content in moderation_mail.body)
        self.assertTrue(self.private_message.subject in moderation_mail.body)
        self.assertTrue(self.private_message.author_name in moderation_mail.body)
        self.assertTrue(self.private_message.author_email in moderation_mail.body)

    def test_message_send_moderation_message(self):
        self.private_message.send_moderation_mail()

        self.assertEquals(len(mail.outbox),2)
        moderation_mail = mail.outbox[1]
        self.assertEquals(moderation_mail.to[0], self.private_message.writeitinstance.owner.email)
        self.assertTrue(self.private_message.content in moderation_mail.body)
        self.assertTrue(self.private_message.subject in moderation_mail.body)
        self.assertTrue(self.private_message.author_name in moderation_mail.body)
        self.assertTrue(self.private_message.author_email in moderation_mail.body)
        self.assertTrue(self.person1.name in moderation_mail.body)











    





