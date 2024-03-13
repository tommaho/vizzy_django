from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404


from .forms import DataSetForm
from .models import DataSet
import pandas as pd
import bleach
import pickle

# Create your views here.

def index(request):
    """Home page"""
    return render(request, 'vizzy/index.html')

@login_required
def create(request):
    """Create dataset page"""

    if request.method != 'POST':
        
        form = DataSetForm()

    else:

        form = DataSetForm(request.POST, request.FILES)
        file = request.FILES['file_upload']   

        if form.is_valid():

            dataframe = pd.read_csv(file, encoding='utf-8')

            # this will be a performance killer for large datasets
            dataframe = dataframe.map(lambda x: bleach.clean(x) if isinstance(x, str) else x)

            column_names = dataframe.columns.tolist()

            DataSet.objects.create(
                name = form.cleaned_data['file_name'],
                column_count = len(dataframe.columns),
                columns = column_names,
                row_count = len(dataframe),
                data = pickle.dumps(dataframe)
            )

            messages.add_message(request
                                 , messages.SUCCESS
                                 , 'File successfully uploaded.'
                                 , extra_tags='alert alert-success')
            
            
            return redirect('vizzy:datasets')
        else: 
             
            # if not size_ok:
            #    form.add_error(None, 'File too large.')


            errors = form.errors.get('file_upload', None)
            
      
            messages.add_message(request
                                 , messages.SUCCESS
                                 , f'File upload failed. Must be a valid CSV file under 2MB. <br><br>Errors: {errors}'
                                 , extra_tags='alert alert-danger')           
            
            form = DataSetForm()   # reset form 

        

    context = {'form': form}
    return render(request, 'vizzy/create.html', context)


def datasets(request):
    """Datasets page"""
    datasets = DataSet.objects.order_by('-date_added')
    context = {'datasets': datasets}
    return render(request, 'vizzy/datasets.html', context)


def visualize(request, dataset_id):
    """Visualization page"""

    dataset = DataSet.objects.get(id=dataset_id)
    
    datatable = pickle.loads(dataset.data).to_html(index=False
                                       , classes='table table-bordered table-striped'
                                       , table_id='data_table')
    
    context = {'dataset_name': dataset.name, 'datatable': datatable}

    return render(request, 'vizzy/visualize.html', context)


def err_handler(request, e=None):
    return render(request, 'vizzy/err.html')