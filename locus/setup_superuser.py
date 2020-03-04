import django
# from django.conf import settings
django.setup()
# settings.configure()


from role_system.models import CustomUser
u = CustomUser.objects.get(username='anindya')
u.set_password('locus123')
u.save()
