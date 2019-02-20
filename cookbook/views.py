from django.views.generic.base import TemplateView

class HomeView(TemplateView):
    template_name = 'cookbook/index.html'

