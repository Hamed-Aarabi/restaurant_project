from contact_us.models import ContactUs


def contact_us(request):
    contact = ContactUs.objects.all().last()
    return {'contact':contact}