from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse

from django.core.exceptions import ValidationError

from .models import *
from .forms import *

from datetime import datetime, timedelta


def homepage(request):
    print(Auction.objects.all())

    # Filter by auctions happening right now
    auctions_now = Auction.objects.filter(auctionstart__lt=datetime.now(),auctionend__gt=datetime.now())
    for auction in auctions_now:
        print(auction)

    # Filter by auctions scheduled at most a week from now
    week_range = datetime.now() + timedelta(days=7)
    auctions_soon = Auction.objects.filter(auctionstart__lt=week_range).exclude(auctionstart__lte=datetime.now())
    for auction in auctions_soon:  #
        print(auction)    

    context = {
        'auctions_now': auctions_now,
        'auctions_soon': auctions_soon,
    }

    return render(request, "boodlesite/templates/index.html",context)    

def auction(request, pk):

    # Current auction ID
    auction = Auction.objects.get(pk=pk)
    # Item for auction
    auction_item = auction.itemid
    # Auction bids
    auction_bids = AuctionBid.objects.filter(auctionid=pk).order_by('-bidtime')

    highest_bid = auction_item.floorprice

    if auction_bids:
        highest_bid = auction_bids[0].amount

    form = PlaceBidForm(initial={'auctionid':auction})
    if request.method == 'POST':
        form = PlaceBidForm(request.POST,initial={'auctionid':auction})
        if form.is_valid():
            try:
                amount = form.cleaned_data['amount']
                new_bid = AuctionBid(amount=amount,bidtime=datetime.now(),auctionid=auction)
                new_bid.save()
                return redirect(f"/auction/{pk}")
            except:
                pass


    context = {
        'item_name':auction_item.itemname,
        'item_specs': auction_item.itemspecs,
        'auction_bids' : auction_bids,
        'item_floor_price': auction_item.floorprice,
        'highest_bid': highest_bid,
        'auction_end':  auction.auctionend,
        'form' : form,
    }

    if auction.auctionend < datetime.now():
        return HttpResponse("This auction has already passed.")
    elif auction.auctionstart > datetime.now():
        #return HttpResponse("This auction has not yet started.")
        return render(request, "boodlesite/templates/error404/notstarted_error404.html")
    else:
        return render(request, "boodlesite/templates/auction.html",context)    

def error404(request):
    return render(request, "boodlesite/templates/error404/notstarted_error404.html")

def tempstore(request): # temp view

    #### Access to store 1 [ edit accordingly when it becomes accessible thru a user ] ####
    current_store = Store.objects.get(storeid=1)

    context = {
        'current_store':current_store #### used for navbar, access to store 1

    }

    return render(request, "boodlesite/templates/tempstore.html", context)

def mystore(request, pk):

    #### Access to store 1 [ edit accordingly when it becomes accessible thru a user ] ####
    # pk is storeid
    current_store = Store.objects.get(pk=pk)
    store_items = Item.objects.filter(storeid=pk)

    all_auctions = Auction.objects.all()

    form = DeleteItemForm()

    if request.method == "POST":
        form = DeleteItemForm(request.POST)
        if form.is_valid():
            item_id = form.cleaned_data['itemid']
            current_item = Item.objects.get(itemid=item_id)
            for auction in all_auctions:
                if auction.itemid == current_item:
                    Auction.objects.filter(itemid=item_id).delete()
                    
            Item.objects.get(itemid=item_id).delete()

            return redirect('storeid', pk=pk)

    context = {
        'current_store':current_store,
        'store_items':store_items,
        'form':form
  
    }

    return render(request, "boodlesite/templates/store.html", context)

def addItem(request, pk):

    # Current Store, pk here is the storeid
    current_store = Store.objects.get(pk=pk)

    form = AddItemForm(initial={'storeid':current_store})

    if request.method == 'POST':
        form = AddItemForm(request.POST,initial={'storeid':current_store})
        if form.is_valid():
            form.save()
            return redirect('storeid', pk=pk)

    context = {
        'form':form,
        'current_store': current_store # access to store 1
    }

    return render(request, "boodlesite/templates/additem.html", context)

def editItem(request, pk):

    item = Item.objects.get(itemid=pk)
    current_store = item.storeid.storeid
    form = AddItemForm(instance=item)

    if request.method == 'POST':
        form = AddItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('storeid', pk=current_store)

    context = {
        'form':form,
    }

    return render(request, "boodlesite/templates/additem.html", context)

def startAuction(request, pk):

    # pk is store id
    current_store = Store.objects.get(pk=pk)
    store_id = current_store.storeid
    # get items under this store
    store_items = Item.objects.filter(storeid=pk)

    # temp: all auctions
    all_auctions = Auction.objects.all()

    form = StartAuctionForm(initial={'auctionstart':datetime.now()})

    if request.method == 'POST':
        form = StartAuctionForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                info = form.cleaned_data['info']
                starttime = form.cleaned_data['auctionstart']
                endtime = form.cleaned_data['auctionend']
                current_item = form.cleaned_data['itemid']
                new_auction = Auction(title=title, info=info, auctionstart=starttime, auctionend=endtime, itemid=current_item)
                new_auction.save()
                return redirect(f"/startauction/{pk}")
            except:
                pass

    context = {
        'current_store':current_store,
        'store_items': store_items,
        'all_auctions':all_auctions,
        'form':form
    }

    return render(request, "boodlesite/templates/startauction.html", context)
