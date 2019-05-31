from rest_framework.views import APIView
from rest_framework.response import Response

import workshops.testing_utils as workshops_testing
import pigs.testing_utils as pigs_testing


class CreateWorkshopsView(APIView):
    # authentication_classes = (authentication.TokenAuthentication,)
    # permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        workshops_testing.create_workshops_sections_and_cells()
        pigs_testing.create_statuses()
        return Response({'msg': 'success'})