from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, ListView, DetailView, DeleteView, UpdateView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from DataGovCRUD.models import Event, ShowInfo


class AllEventsView(ListView):
    queryset = Event.objects.all().prefetch_related('master_unit', 'sub_unit', 'support_unit', 'other_unit').order_by("-hit_rate",)
    template_name = 'event_list.html'
    paginate_by = 20


class EventsDetailView(DetailView):
    model = Event
    template_name = 'event_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        showinfos = ShowInfo.objects.filter(event=self.object).select_related('location')
        context['showinfos'] = showinfos
        return context


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('operation')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Event, pk=pk)


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    fields = [
        'version', 'uid', 'title', 'category', 'description', 'image_url',
        'web_sale', 'source_web_promote', 'comment', 'edit_modify_date',
        'source_web_name', 'start_date', 'end_date', 'hit_rate', 'show_unit',
        'discount_info', 'description_filter_html', 'master_unit', 'sub_unit',
        'support_unit', 'other_unit'
    ]
    template_name = 'event_form.html'
    success_url = reverse_lazy('operation_page')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Event, pk=pk)


