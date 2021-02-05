# -*- coding: utf-8 -*-
import time
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from django.test import TransactionTestCase

import locations.testing_utils as locations_testing
import sows.testing_utils as sows_testing
import sows_events.utils as sows_events_testings
import piglets.testing_utils as piglets_testing
import staff.testing_utils as staff_testing

from sows.models import Gilt, Sow
from sows_events.models import SowFarrow, MarkAsGilt
from locations.models import WorkShop, SowAndPigletsCell, Location
from transactions.models import PigletsTransaction, SowTransaction
from tours.models import Tour

from workshopthree.serializers import SowMarkAsGiltSerializer


class WorkshopThreeSowsViewSetTest(APITestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()
        self.client = APIClient()
        self.user = staff_testing.create_employee()
        self.brig1 = User.objects.get(username='brigadir1')
        self.brig2 = User.objects.get(username='brigadir2')
        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws2 = Location.objects.get(workshop__number=2)

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

    def test_sow_farrow(self):
        self.client.force_authenticate(user=self.brig3)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7,
          'date': '2020-09-09T00:00' })

        self.assertEqual(response.data['sow']['id'], sow.pk)
        self.assertEqual(response.data['sow']['farm_id'], sow.farm_id)
        self.assertEqual('Тур 7' in response.data['sow']['tour'], True)
        self.assertEqual(response.data['sow']['status'], 'Опоросилась')
        self.assertEqual(response.data['farrow']['alive_quantity'], 10)
        self.assertEqual(response.data['farrow']['dead_quantity'], 1)
        self.assertEqual(response.data['farrow']['mummy_quantity'], 2)
        self.client.logout()

    def test_sow_farrow_401(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })
        self.assertEqual(response.status_code, 401)

    def test_sow_farrow_403(self):
        self.client.force_authenticate(user=self.brig1)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        response = self.client.post('/api/workshopthree/sows/%s/sow_farrow/' %
          sow.pk, {'alive_quantity': 10, 'dead_quantity': 1, 'mummy_quantity': 2, 'week': 7 })
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_mark_as_nurse_without_creating_piglets(self):
        self.client.force_authenticate(user=self.brig3)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk)
        sow.refresh_from_db()
        self.assertEqual(sow.status.title, 'Кормилица')
        self.assertEqual(response.data['message'], 'Свинья помечена как кормилица.')
        self.client.logout()

    def test_mark_as_nurse_without_creating_piglets_401(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk)
        self.assertEqual(response.status_code, 401)

    def test_mark_as_nurse_without_creating_piglets_403(self):
        self.client.force_authenticate(user=self.brig1)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_nurse/' % sow.pk)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_transfer_sow_and_piglets(self):
        self.client.force_authenticate(user=self.brig3)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        to_location = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]

        response = self.client.post('/api/workshopthree/sows/transfer_sow_and_piglets/',
            {'from_location': location, 'to_location': to_location})
        sow.refresh_from_db()

        self.assertEqual(response.data['message'],
            f"Свиноматка {sow.farm_id} и поросята №{farrow.piglets_group.id} перемещены.")
        self.client.logout()

    def test_transfer_sow_and_piglets_401(self):
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        to_location = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]

        response = self.client.post('/api/workshopthree/sows/transfer_sow_and_piglets/',
            {'from_location': location, 'to_location': to_location})
        self.assertEqual(response.status_code, 401)

    def test_transfer_sow_and_piglets_403(self):
        self.client.force_authenticate(user=self.brig1)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        to_location = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]

        response = self.client.post('/api/workshopthree/sows/transfer_sow_and_piglets/',
            {'from_location': location, 'to_location': to_location})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_transfer_sow_and_piglets_validate(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1.change_sow_current_location(location1)
        farrow1 = SowFarrow.objects.create_sow_farrow(sow=sow1, alive_quantity=10)

        sow2 = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1, week=7)
        location2 = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]
        sow2.change_sow_current_location(location2)

        response = self.client.post('/api/workshopthree/sows/transfer_sow_and_piglets/',
            {'from_location': location1, 'to_location': location2})
        sow1.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.client.logout()

    def test_move_to_permissions_200(self):
        self.client.force_authenticate(user=self.brig3)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1.change_sow_current_location(location1)
        response = self.client.post('/api/workshopthree/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_move_to_permissions_401(self):
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1.change_sow_current_location(location1)
        response = self.client.post('/api/workshopthree/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 401)

    def test_move_to_permissions_403(self):
        self.client.force_authenticate(user=self.brig1)
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1.change_sow_current_location(location1)
        response = self.client.post('/api/workshopthree/sows/%s/move_to/' % sow1.pk,
         {'location': self.loc_ws2})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_move_many_permissions_200(self):
        self.client.force_authenticate(user=self.brig3)
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.change_sow_current_location(location1)
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2.change_sow_current_location(location1)
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3.change_sow_current_location(location1)

        response = self.client.post('/api/workshopthree/sows/move_many/',
         {'to_location': self.loc_ws2, 'sows': [sow1.pk, sow2.pk, sow3.pk]})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_move_many_permissions_401(self):
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.change_sow_current_location(location1)
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2.change_sow_current_location(location1)
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3.change_sow_current_location(location1)

        response = self.client.post('/api/workshopthree/sows/move_many/',
         {'to_location': self.loc_ws2, 'sows': [sow1.pk, sow2.pk, sow3.pk]})
        self.assertEqual(response.status_code, 401)

    def test_move_many_permissions_403(self):
        self.client.force_authenticate(user=self.brig1)
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.change_sow_current_location(location1)
        sow2 = sows_testing.create_sow_and_put_in_workshop_one()
        sow2.change_sow_current_location(location1)
        sow3 = sows_testing.create_sow_and_put_in_workshop_one()
        sow3.change_sow_current_location(location1)

        response = self.client.post('/api/workshopthree/sows/move_many/',
         {'to_location': self.loc_ws2, 'sows': [sow1.pk, sow2.pk, sow3.pk]})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_culling_permissions_200(self):
        self.client.force_authenticate(user=self.brig3)
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.change_sow_current_location(location1)
        response = self.client.post('/api/workshopthree/sows/%s/culling/' % sow1.pk,
         {'culling_type': 'padej', 'reason': 'test', 'weight': 150})
        self.assertEqual(response.status_code, 200)
        self.client.logout()

    def test_culling_permissions_401(self):
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.change_sow_current_location(location1)
        response = self.client.post('/api/workshopthree/sows/%s/culling/' % sow1.pk,
         {'culling_type': 'padej', 'reason': 'test', 'weight': 150})
        self.assertEqual(response.status_code, 401)

    def test_culling_permissions_403(self):
        self.client.force_authenticate(user=self.brig5)
        location1 = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow1 = sows_testing.create_sow_and_put_in_workshop_one()
        sow1.change_sow_current_location(location1)
        response = self.client.post('/api/workshopthree/sows/%s/culling/' % sow1.pk,
         {'culling_type': 'padej', 'reason': 'test', 'weight': 150})
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_mark_as_gilt(self):
        self.client.force_authenticate(user=self.brig3)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1,
            week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)

        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow.pk,
         {'birth_id': 'A123'})
        self.assertEqual(response.status_code, 200)

        sow.alive = False
        sow.save()
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow.pk,
         {'birth_id': 'A124'})
        self.assertEqual(response.status_code, 200)
        
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow.pk,
         {'birth_id': 'A125', 'date': '2020-09-10'})
        self.assertEqual(response.status_code, 200)
        
        event = MarkAsGilt.objects.filter(gilt__birth_id='A125').first()
        self.assertEqual(event.date.day, 10)

        self.client.logout()


class MarksAsGiltListViewTest(APITestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()
        self.client = APIClient()
        self.user = staff_testing.create_employee()
        self.brig1 = User.objects.get(username='brigadir1')
        self.brig2 = User.objects.get(username='brigadir2')
        self.brig3 = User.objects.get(username='brigadir3')
        self.brig4 = User.objects.get(username='brigadir4')
        self.brig5 = User.objects.get(username='brigadir5')

        self.loc_ws1 = Location.objects.get(workshop__number=1)
        self.loc_ws2 = Location.objects.get(workshop__number=2)

        self.loc_ws3 = Location.objects.get(workshop__number=3)
        self.loc_ws3_sec1 = Location.objects.get(section__workshop__number=3, section__number=1)
        self.loc_ws3_sec2 = Location.objects.get(section__workshop__number=3, section__number=2)

    def test_mark_as_gilt_list(self):
        self.client.force_authenticate(user=self.brig3)
        sow = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1,
            week=7)
        location = Location.objects.filter(sowAndPigletsCell__isnull=False).first()
        sow.change_sow_current_location(location)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)

        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow.pk,
         {'birth_id': 'A123', 'date': '2020-09-11'})
        
        sow.alive = False
        sow.save()
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow.pk,
         {'birth_id': 'A124', 'date': '2020-09-21'})
              
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow.pk,
         {'birth_id': 'A125', 'date': '2020-09-10'})

        sow2 = sows_testing.create_sow_seminated_usouded_ws3_section(section_number=1,
            week=7)
        location2 = Location.objects.filter(sowAndPigletsCell__isnull=False)[1]
        sow2.change_sow_current_location(location2)
        farrow2 = SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        response = self.client.post('/api/workshopthree/sows/%s/mark_as_gilt/' % sow2.pk,
         {'birth_id': 'A126', 'date': '2020-10-10'})

        response = self.client.get('/api/workshopthree/reports/mark_as_gilts_journal/')
        self.assertEqual(response.data['results'][0]['farm_id'], sow2.farm_id)
        self.assertEqual(response.data['results'][0]['gilt_list'][0], 'A126')

        self.client.logout()


class SowMarksAsGiltSerializerTest(TransactionTestCase):
    def setUp(self):
        locations_testing.create_workshops_sections_and_cells()
        sows_testing.create_statuses()
        sows_events_testings.create_types()
        piglets_testing.create_piglets_statuses()
        staff_testing.create_svinbin_users()
        
    def test_serializer_queries(self):
        cells = Location.objects.filter(sowAndPigletsCell__isnull=False)
        sow = sows_testing.create_sow_with_semination_usound(cells[0], 1)
        farrow = SowFarrow.objects.create_sow_farrow(sow=sow, alive_quantity=10)
        piglets = farrow.piglets_group
        gilt1 = Gilt.objects.create_gilt(birth_id='1a', mother_sow_farm_id=sow.farm_id,
             piglets=piglets)
        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt1)
        gilt2 = Gilt.objects.create_gilt(birth_id='2a', mother_sow_farm_id=sow.farm_id,
             piglets=piglets)
        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt2)

        sow2 = sows_testing.create_sow_with_semination_usound(cells[1], 1)
        farrow2 = SowFarrow.objects.create_sow_farrow(sow=sow2, alive_quantity=10)
        piglets2 = farrow2.piglets_group
        gilt3 = Gilt.objects.create_gilt(birth_id='3a', mother_sow_farm_id=sow2.farm_id,
             piglets=piglets2)
        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt3)
        gilt4 = Gilt.objects.create_gilt(birth_id='4a', mother_sow_farm_id=sow2.farm_id,
             piglets=piglets2)
        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt4)

        sow3 = sows_testing.create_sow_with_semination_usound(cells[2], 1)
        farrow3 = SowFarrow.objects.create_sow_farrow(sow=sow3, alive_quantity=10)
        piglets3 = farrow3.piglets_group
        gilt5 = Gilt.objects.create_gilt(birth_id='5a', mother_sow_farm_id=sow3.farm_id,
             piglets=piglets3)
        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt5)
        gilt6 = Gilt.objects.create_gilt(birth_id='6a', mother_sow_farm_id=sow3.farm_id,
             piglets=piglets3)
        MarkAsGilt.objects.create_init_gilt_event(gilt=gilt6)

        mag_qs = MarkAsGilt.objects.all().select_related('gilt', 'sow', 'tour') \
            .order_by('-date')

        sows_pk_list = mag_qs.values_list('sow__pk', flat=True)

        sows_qs = Sow.objects.get_queryset_with_not_alive() \
            .filter(pk__in=sows_pk_list) \
            .add_mark_as_gilt_last_date_and_last_tour() \
            .order_by('-last_date_mark')

        with self.assertNumQueries(1):
            serializer = SowMarkAsGiltSerializer(sows_qs, many=True)
            serializer.data
