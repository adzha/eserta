from django.shortcuts import render
from django.contrib.auth.signals import user_logged_out, user_logged_in
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Aktiviti
from .forms import AktivitiForm, JemputanForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField
from datetime import datetime
from django.core.exceptions import PermissionDenied

# Only user in group penganjur can use this views
def grp_penganjur(user):
    if user.groups.filter(name__in=['esertaPenganjur']):
        return user.groups.filter(name__in=['esertaPenganjur'])
    else:
        # Hantar mesej ke laman 404.html
        raise PermissionDenied("Anda tidak mempunyai akses ke fungsi ini!")

# Main eSERTA Homepage.
def home(request):
	return render(request,'penganjur/home.html')

# Add Aktiviti
@login_required(login_url='/accounts/login/')
@user_passes_test(grp_penganjur)
def aktiviti_new(request):

    if request.method == "POST":
        # The purpose of copy is to change the value of date type input
        # This is to avoid immutable error
        # source : https://stackoverflow.com/questions/18930234/django-modifying-the-request-object
        request.POST = request.POST.copy()
        form = AktivitiForm(request.POST)
        
        # remove "T" from date type input and put it back to the form again
        mydate,mytime = form.data['mula'].split('T')
        form.data['mula'] = datetime.strptime(mydate + ' ' + mytime, '%Y-%m-%d %H:%M')
        mydate,mytime = form.data['akhir'].split('T')
        form.data['akhir'] = datetime.strptime(mydate + ' ' + mytime, '%Y-%m-%d %H:%M')

        if form.is_valid():
            aktiviti = form.save(commit=False)
            aktiviti.save()
            messages.success(request, "Aktiviti dengan ID : " + str(aktiviti.pk) + " telah berjaya dicipta! ")
            return redirect(reverse_lazy('aktiviti_detail',kwargs={'pk': aktiviti.pk }))
        else:
            # remove "T" from date type input and put it back to the form again
            form.data['mula'] = form.data['mula'].strftime('%Y-%m-%dT%H:%M')
            form.data['akhir'] = form.data['akhir'].strftime('%Y-%m-%dT%H:%M')
    else:
        form = AktivitiForm()
    return render(request, 'penganjur/aktiviti_new.html', {'form': form})

# Updating Aktiviti
@login_required(login_url='/accounts/login/')
@user_passes_test(grp_penganjur)
def aktiviti_edit(request,pk):

    aktiviti = get_object_or_404(Aktiviti, pk=pk)
    if request.method == "POST":
        request.POST = request.POST.copy()
        form = AktivitiForm(request.POST,instance=aktiviti)
        # remove "T" from date type input and put it back to the form again
        mydate,mytime = form.data['mula'].split('T')
        form.data['mula'] = datetime.strptime(mydate + ' ' + mytime , '%Y-%m-%d %H:%M')
        mydate,mytime = form.data['akhir'].split('T')
        form.data['akhir'] = datetime.strptime(mydate + ' ' + mytime, '%Y-%m-%d %H:%M')
        
        if form.is_valid():
            aktiviti = form.save(commit=False)
            aktiviti.save()
            messages.success(request, "Aktiviti dengan ID: " + str(aktiviti.pk) + " telah berjaya dikemaskini! ")
            return redirect(reverse_lazy('aktiviti_detail',kwargs={'pk': aktiviti.pk }))
        else:
            form.data['mula'] = aktiviti.mula.strftime('%Y-%m-%dT%H:%M')
            form.data['akhir'] = aktiviti.akhir.strftime('%Y-%m-%dT%H:%M')
    else:
        # Use strftime to change to input type='date' value format
        aktiviti.mula = aktiviti.mula.strftime('%Y-%m-%dT%H:%M')
        aktiviti.akhir = aktiviti.akhir.strftime('%Y-%m-%dT%H:%M')
        form = AktivitiForm(instance=aktiviti)
    return render(request, 'penganjur/aktiviti_edit.html', {'form': form})

# Removing Aktiviti
@login_required(login_url='/accounts/login/')
@user_passes_test(grp_penganjur)
def aktiviti_remove(request,pk):

    aktiviti = get_object_or_404(Aktiviti, pk=pk)
    if request.method == "POST":
        if request.POST.get("submit_yes", ""):
            pk = aktiviti.pk
            aktiviti.delete()
            messages.success(request, "Aktiviti dengan ID: " + str(pk) + " telah berjaya dihapuskan! ")
            return redirect(reverse_lazy('aktiviti_home'))

    return render(request, 'penganjur/aktiviti_confirm_delete.html', {'aktiviti': aktiviti, 'pk':pk})

# List Aktiviti with datatables JSON.
@login_required(login_url='/accounts/login/')
@user_passes_test(grp_penganjur)
def aktiviti_home(request):
  return render(request,'penganjur/aktiviti_home.html')

# Aktiviti detail
@login_required(login_url='/accounts/login/')
@user_passes_test(grp_penganjur)
def aktiviti_detail(request,pk):
    aktiviti = get_object_or_404(Aktiviti, pk=pk)
    return render(request, 'penganjur/aktiviti_detail.html', {'aktiviti': aktiviti})

# Penganjur Dashboard / Home with datatables JSON.
def penganjur_home(request):
  return render(request,'penganjur/penganjur_home.html')

# Aktiviti JSON list filtering
# @user_passes_test(grp_penganjur)
class aktiviti_json(BaseDatatableView):
    # Columns to be displayed in datatables 

    # define the columns that will be returned
    # columns = ['number', 'user', 'state', 'created', 'modified']
    columns = ['mula','akhir','tajuk', 'tempat','penganjur']

    # define column names that will be used in sorting
    # order is important and should be same as order of columns
    # displayed by datatables. For non sortable columns use empty
    # value like ''
    # order_columns = ['number', 'user', 'state', '', '']
    order_columns = ['mula','akhir','tajuk', 'tempat','penganjur']


    # Get initial records of Aktivit
    def get_initial_queryset(self):
        return Aktiviti.objects.all()

    # Filtering Aktiviti records from initial records
    def filter_queryset(self, qs):

        # Getting advanced filtering indicators for dataTables 1.10.13
        search = self.request.GET.get(u'search[value]', "")
        iSortCol_0 = self.request.GET.get(u'order[0][column]', "") # Column number 0,1,2,3,4
        sSortDir_0 = self.request.GET.get(u'order[0][dir]', "") # asc, desc
        
        # Choose which column to sort
        if iSortCol_0 == '1':
          sortcol = 'mula'
        elif iSortCol_0 == '2':
          sortcol = 'akhir'
        elif iSortCol_0 == '3':
          sortcol = 'tajuk'
        elif iSortCol_0 == '4':
          sortcol = 'tempat'
        elif iSortCol_0 == '5':
          sortcol = 'penganjur'  
        else:
          sortcol = 'mula'


        # Choose which sorting direction : asc or desc
        if sSortDir_0 == 'asc':
          sortdir = ''
        else:
          sortdir = '-'

        # Filtering if search value is key-in
        if search:
          # Initial Q parameter value
          qs_params = None

          # Filtering other fields
          q = Q(tempat__icontains=search)|Q(tajuk__icontains=search)|Q(penganjur__icontains=search)
          qs_params = qs_params | q if qs_params else q
   
          # Completed Q queryset
          qs = qs.filter(qs_params)

        # return qs
        return qs.order_by(sortdir + sortcol)
        

    def prepare_results(self, qs):
        # prepare list with output column data
        # queryset is already paginated here
        # json_data = {}
        json_data = []

        for i in range(len(qs)):
            json_data.append([
                i+1,
                qs[i].mula.strftime("%d-%m-%Y %H:%S"),
                qs[i].akhir.strftime("%d-%m-%Y %H:%S"),
                qs[i].tajuk,
                qs[i].tempat,
                qs[i].penganjur,
                reverse_lazy('aktiviti_edit',kwargs={'pk':qs[i].pk}),
                reverse_lazy('aktiviti_remove',kwargs={'pk':qs[i].pk}),
                reverse_lazy('aktiviti_detail',kwargs={'pk':qs[i].pk}),
            ])

        return json_data

# Sending successful logout messages
def show_message_logout(sender, user, request, **kwargs):
    messages.info(request, 'Anda telah berjaya keluar!')

# Sending successful login messages
def show_message_login(sender, user, request, **kwargs):
    messages.info(request, 'Anda telah berjaya login. Selamat datang ' + str(user) + ' !')
    print(user)

user_logged_out.connect(show_message_logout)
user_logged_in.connect(show_message_login)

# Hantar jemputan
@login_required(login_url='/accounts/login/') 
def aktiviti_jemput(request,pk):
    aktiviti = get_object_or_404(Aktiviti, pk=pk)
    if request.method == "POST":
        if form.is_valid():
            messages.success(request, "Jemputan telah dihantar kepada emel : " + str(aktiviti.pk) + " ! ")
            return redirect(reverse_lazy('aktiviti_detail',kwargs={'pk': aktiviti.pk }))
    else:
        form = JemputanForm()
    return render(request,'penganjur/aktiviti_jemput.html',{ 'aktiviti' : aktiviti , 'form': form })