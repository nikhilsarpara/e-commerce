from category.models import *


def menu_link(request):
    link = Category.objects.all()
    return dict({'links':link})