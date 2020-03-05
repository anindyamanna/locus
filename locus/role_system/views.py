from rest_framework.response import Response
from rest_framework.views import APIView

from role_system.models import Resource


class CheckAccess(APIView):
    def get(self, request, *args, **kwargs):
        resource_id = int(kwargs['resource_id'])
        action_id = int(kwargs['action_id'])
        allowed = False
        for role in self.request.user.roles.all():
            for action_resource_pair in role.action_resource_pairs.all():
                if action_resource_pair.action_id == action_id and action_resource_pair.resource_id == resource_id:
                    allowed = True
                    break
            if allowed:
                break
        resp = {"ALLOWED": allowed}
        if allowed:
            resource = Resource.objects.get(id=resource_id)
            resp['resource_name'] = resource.resource_name
            resp['resource_desc'] = resource.resource_desc
        return Response(resp)
