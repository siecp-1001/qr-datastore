from io import BytesIO
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import FormView
import qrcode
from django.core.files.base import ContentFile

from . import models
from . import forms
import logging
from django.contrib.auth import login ,authenticate
from django.contrib import messages
# offer users a way to add, change, and remove their addresses
from django .views.generic.edit import FormView,CreateView,UpdateView,DeleteView
from django .views.generic.edit import (
     FormView,
     CreateView,
     UpdateView,
     DeleteView,
    )
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.template.loader import get_template
from django.urls import reverse_lazy
# Create your views here.

def home(request):
    return render(request, "home.html", {})
logger= logging.getLogger(__name__)

class signupview(FormView):
    template_name="signup.html"
    form_class=forms.Usercreationform
    def get_success_url(self) :
        redirect_to=self.request.GET.get("next","")
        return redirect_to
    def form_valid(self, form) :
        response=super().form_valid(form)
        form.save()
        email=form.cleaned_data.get("email")
        raw_password=form.cleaned_data.get("password1")
        logger.info(
            "new signup for email =%s through signupview",email
        )
        user=authenticate(email=email,password=raw_password)
        login(self.request,user)
       
        return response
    



class productlistview(ListView):
    template_name="pages/product_list.html"
    model = models.product
    paginate_by=7
    context_object_name="products"
    def  get_queryset(self):
      return models.product.objects.all()[:7]  
    




class notelistview(LoginRequiredMixin,ListView):
    model=models.notes
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    
class notecreateview(LoginRequiredMixin,CreateView):
    model=models.notes
    fields=[
        "NOTE",
        "date",
    ]  
    success_url= reverse_lazy("search:notes_list")
    def form_valid(self, form) :
         obj=form.save(commit=False)
         obj.user=self.request.user
         obj.save()
         return super().form_valid(form)    
    

class noteupdateview(LoginRequiredMixin,UpdateView):
    model=models.notes 
    fields=[
        "NOTE",
        "date",
     ]  
    success_url=reverse_lazy("search:notes_list")  
    def get_queryset(self) :
        return self.model.objects.filter(user=self.request.user)   

    
class NoteqrView(LoginRequiredMixin, CreateView):
    model = models.notes 
    fields = [
        "NOTE",
        "date",
    ]  
    success_url = reverse_lazy("search:notes_list")

    def form_valid(self, form):
        # Save the note object
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()

        # Generate QR code for the note's data
        qr_data = f"Note ID: {obj.id}\nNote: {obj.NOTE}\nDate: {obj.date}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save QR code image to BytesIO buffer
        img_byte_array = BytesIO()
        img.save(img_byte_array)

        # Attach the QR code image to the note object (optional)
        obj.qr_code.save(f'qrcode_{obj.id}.png', ContentFile(img_byte_array.getvalue()))

        return super().form_valid(form)

class notedeleteview(LoginRequiredMixin,DeleteView):
    model=models.notes
    success_url=reverse_lazy("search:notes_list")
    def get_queryset(self) :
        return self.model.objects.filter(user=self.request.user)
        