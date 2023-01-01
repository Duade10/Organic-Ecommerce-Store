from django import forms
from . import models


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone",
            "address_line_1",
            "address_line_2",
            "country",
            "state",
            "city",
            "order_note",
            "payment_method",
        ]

    def clean_order_note(self):
        data = self.cleaned_data.get("order_note")
        print(data)
        if len(data) > 100:
            raise forms.ValidationError("Order Note is longer 100 characters")
        return data

    def save(self, *args, **kwargs):
        order = super().save(commit=False)
        order = models.Order()
        order.first_name = self.cleaned_data.get("first_name", None)
        order.last_name = self.cleaned_data.get("last_name", None)
        order.email = self.cleaned_data.get("email", None)
        order.phone = self.cleaned_data.get("phone", None)
        order.address_line_1 = self.cleaned_data.get("address_line_1", None)
        order.address_line_2 = self.cleaned_data.get("address_line_2", None)
        order.country = self.cleaned_data.get("country", None)
        order.state = self.cleaned_data.get("state", None)
        order.city = self.cleaned_data.get("city", None)
        order.order_note = self.cleaned_data.get("order_note", None)
        order.payment_method = self.cleaned_data.get("payment_method", None)
        order.save()
        return order
