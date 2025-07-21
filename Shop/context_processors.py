from . models import Categories


def Greenery_Category(request):
    cat = Categories.objects.all()
    return dict(cat=cat)

