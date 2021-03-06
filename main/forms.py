from datetime import datetime
from tracemalloc import start
from django import forms
from django.forms import (ModelForm, 
    TextInput, Textarea, widgets, MultiWidget)
from django.utils.translation import gettext_lazy as _
from .models import *

from django.utils import timezone 
import datetime, pytz

from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.admin import widgets

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
    
class PlaceBidForm(forms.ModelForm):
    class Meta:
        model = AuctionBid
        fields = ['amount', 'userid', 'auctionid']
        widgets = {'auctionid': forms.HiddenInput(), 
            'userid': forms.HiddenInput()
        }

    def clean(self):
        super().clean()
        form_amount = self.cleaned_data.get('amount')
        auction = self.cleaned_data.get('auctionid')

        auction_item = Item.objects.get(auction=auction)
        auction_bids = AuctionBid.objects.filter(auctionid=auction)
        
        if not auction_bids:
            highest_bid = auction_item.floorprice
            if form_amount < highest_bid:
                raise ValidationError('Please enter an amount greater than or equal to the floorprice.')
        else:
            highest_bid = auction_bids.latest('bidtime').amount
            if form_amount <= highest_bid:
                raise ValidationError('Please enter an amount higher than the current highest bid.')

class AddItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['itemname','itemspecs','floorprice','storeid']
        widgets = {'storeid': forms.HiddenInput()}

        labels = {
            'itemname': _('Item Name'),
            'itemspecs': _('Item Description'),
            'floorprice': _('Floor Price')
        }

class DeleteItemForm(forms.Form):
        itemid = forms.IntegerField()
        widgets = {'itemid': forms.HiddenInput()}

class StartAuctionForm(forms.ModelForm):

    # the widget is supposed to have a pop up but not showing, keeping here bc it separates date and time nicely
    # auctionstart = forms.SplitDateTimeField(widget=AdminSplitDateTime())
    # auctionend = forms.SplitDateTimeField(widget=AdminSplitDateTime())

    auctionstart = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
    auctionend = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

    class Meta:
        model = Auction
        fields = '__all__'

        labels = {
            'title': _('Auction Title'),
            'info': _('Auction Description'),
            'auctionstart': _('Starting time'),
            'auctionend': _('Closing time'),
            'itemid': _('Item up for auction')
        }

    def clean(self):
        
        super().clean()
        print(self.cleaned_data)
        end_time = self.cleaned_data.get('auctionend')
        start_time = self.cleaned_data.get('auctionstart')
        current_date = timezone.now()
        auctioned_item = self.cleaned_data['itemid']
            
        auctions = Auction.objects.all()

        if start_time > end_time:
            raise ValidationError('Start date should be before end date.')
        elif start_time < current_date or end_time < current_date:
            raise ValidationError('Date cannot be in the past.')
        else:  
            for auc in auctions:
                if auc.itemid == auctioned_item:
                    raise ValidationError('Auction Already Exists, pick another Item')

class CreateStoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['storename', 'storedesc', 'userid']
        widgets = {'userid': forms.HiddenInput()}

        labels = {
            'storename': _('Store Name'),
            'storedesc': _('Store Description')
        }

class editBoodleUserForm(forms.ModelForm):
    
    class Meta:
        model = AuthUser 
        fields = ['username', 'id']
        widgets = {'id': forms.HiddenInput()}

        labels = {
            'username': _('User Name')
        }

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']