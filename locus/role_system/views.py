from django.http import HttpResponse
from rest_framework.views import APIView


class ResourceView(APIView):
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and any(self.request.user.roles.values_list('read_allowed', flat=True)):
            return HttpResponse("ALLOWED")
        else:
            return HttpResponse("DISALLOWED")

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and any(self.request.user.roles.values_list('write_allowed', flat=True)):
            return HttpResponse("ALLOWED")
        else:
            return HttpResponse("DISALLOWED")

    def delete(self, request, *args, **kwargs):
        if self.request.user.is_authenticated and any(self.request.user.roles.values_list('delete_allowed', flat=True)):
            return HttpResponse("ALLOWED")
        else:
            return HttpResponse("DISALLOWED")
