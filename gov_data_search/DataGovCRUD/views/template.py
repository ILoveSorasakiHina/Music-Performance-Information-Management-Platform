from django.views.generic import TemplateView


class OperationPageView(TemplateView):
    template_name = 'operation.html'


class HomePageView(TemplateView):
    template_name = 'home.html'