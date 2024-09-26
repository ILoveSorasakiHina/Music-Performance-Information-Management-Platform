from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from DataGovCRUD.models import ShowInfo


class ShowInfoDelete(LoginRequiredMixin, DeleteView):
    model = ShowInfo
    template_name = 'showinfo_confirm_delete.html'
    success_url = reverse_lazy('operation')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ShowInfo, pk=pk)


class ShowInfoUpdateView(LoginRequiredMixin, UpdateView):
    model = ShowInfo
    fields = [
        'event', 'time', 'end_time', 'on_sale', 'price', 'location'
    ]
    template_name = 'showinfo_form.html'
    success_url = reverse_lazy('showinfo_list')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(ShowInfo, pk=pk)
    