from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

from .forms import DataSetForm
from .models import DataSet
import pandas as pd
import bleach
import pickle

# Create your views here.

def index(request):
    """Home page"""
    return render(request, 'vizzy/index.html')


def create(request):
    """Create dataset page"""

    if request.method != 'POST':
        
        form = DataSetForm()

    else: # a submit has occurred

        form = DataSetForm(request.POST, request.FILES)
        file = request.FILES['file_upload']   

        if form.is_valid() and file.size < settings.MAX_FILE_SIZE:

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
                # owner = "tommaho"
            )

            messages.add_message(request
                                 , messages.SUCCESS
                                 , 'File successfully uploaded.'
                                 , extra_tags='alert alert-success')
            
            
            return redirect('vizzy:datasets')
        else: 

            messages.add_message(request
                                 , messages.SUCCESS
                                 , 'File upload failed. Must be a valid CSV file under 2MB.'
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