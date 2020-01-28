# -*- coding: utf-8 -*-

from locations.models import Location

def reset_to_suporos():
	for location in Location.objects.filter(sowAndPigletsCell__section__number=4):
		sow = location.sow_set.all().first()
		if sow and sow.tour:
			sow.sowfarrow_set.all().filter(tour=sow.tour).delete()
			sow.change_status_to('Супорос 35')

			location.piglets.all().delete()

