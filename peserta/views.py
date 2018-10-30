from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Pendaftaran, Profail, Kehadiran
from penganjur.models import Aktiviti
from django.contrib.auth.decorators import login_required, user_passes_test
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.db.models import Count, Sum, Q, Case, Value, When, IntegerField
# from datetime import datetime
import datetime

# Aktiviti JSON list filtering
# @user_passes_test(grp_penganjur)
class senarai_blmdaftar_json(BaseDatatableView):
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
        # return Aktiviti.objects.all().exclude(pendaftaran__user=self.request.user)
        # return Aktiviti.objects.filter(mula__gte=datetime.date.today()).exclude(pendaftaran__user=self.request.user)
        # return Aktiviti.objects.filter(akhir__lte=datetime.date.today()).exclude(pendaftaran__user=self.request.user)

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
            status = ''
            if Pendaftaran.objects.filter(pk=int(qs[i].pk),user=self.request.user):
              status = 'Telah daftar'
            else:
              # if qs[i].mula > datetime.date.today():
              # if qs[i].mula > datetime.datetime.now():
              # if qs[i].mula > datetime.now():
              if Aktiviti.objects.filter(pk=int(qs[i].pk),tutup__gte=datetime.date.today()):
                status = 'Dibuka'
              else:
                status = 'Ditutup'
            json_data.append([
                i+1,
                qs[i].mula.strftime("%d-%m-%Y %H:%S"),
                qs[i].akhir.strftime("%d-%m-%Y %H:%S"),
                qs[i].tajuk,
                qs[i].tempat,
                qs[i].penganjur,
                reverse_lazy('home'),
                reverse_lazy('home'),
                reverse_lazy('home'),
                status,
            ])

        return json_data