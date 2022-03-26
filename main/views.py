from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *

from datetime import datetime, timedelta


def homepage(request):
    print(Auction.objects.all())

    # Filter by auctions happening right now
    auctions_now = Auction.objects.filter(auctionstart__lt=datetime.now(),auctionend__gt=datetime.now())
    for auction in auctions_now:  #
        print(auction)

    # Filter by auctions scheduled at most a week from now
    week_range = datetime.now() + timedelta(days=7)
    auctions_soon = Auction.objects.filter(auctionstart__lt=week_range).exclude(auctionstart__lte=datetime.now())
    for auction in auctions_soon:  #
        print(auction)    

    context = {
        'auctions_now': auctions_now,
        'auctions_soon': auctions_soon
    }

    return render(request, "boodlesite/templates/index.html",context)    

def auction(request, pk):
    # Current auction ID
    auction = Auction.objects.get(pk=pk)
    auction_bid = AuctionBid.objects.filter(auctionid=pk)

    auction_item = auction.itemid

    context = {
        'item_name':auction_item.itemname,
        'item_specs': auction_item.itemspecs,
        'item_bid' : auction_bid.amount,
        'item_floor_price': auction_item.floorprice
        # need to make floor price object here
    }

    if auction.auctionend < datetime.now():
        return HttpResponse("This auction has already passed.")
    elif auction.auctionstart > datetime.now():
        return HttpResponse("This auction has not yet started.")
    else:
        return render(request, "boodlesite/templates/auction.html",context)    
