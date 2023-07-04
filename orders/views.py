from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Order


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Спасибо за заказ!'

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(initiator=self.request.user, status=0)
        order.update_after_payment()
        return super(SuccessTemplateView, self).get(request, *args, **kwargs)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Order

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['title'] = f'Заказ #{self.object.id}'
        return context


class OrdersCreateView(TitleMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_success')
    title = 'Оформление заказа'

    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrdersCreateView, self).form_valid(form)


class OrderListView(TitleMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Заказы'
    queryset = Order.objects.all()
    ordering = ('-id')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)
