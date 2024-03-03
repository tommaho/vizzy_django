from django.shortcuts import render, redirect
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
        
        if form.is_valid():

            file = request.FILES['file_upload']
            dataframe = pd.read_csv(file, encoding='utf-8')

            # this will be a performance killer for large datasets
            dataframe = dataframe.map(lambda x: bleach.clean(x) if isinstance(x, str) else x)


            column_names = dataframe.columns.tolist()

            DataSet.objects.create(
                name = form.cleaned_data['file_name'],
                column_count = len(dataframe.columns),
                columns = column_names,
                row_count = len(dataframe),
                data = pickle.dumps(dataframe) # dataframe.to_json(),
                # owner = "tommaho"
            )


            return redirect('vizzy:datasets')
        else: 
            errors = form.errors

            return render(request, 'vizzy/create.html', {'form': form, 'errors': errors})

        

    context = {'form': form}
    return render(request, 'vizzy/create.html', context)


def datasets(request):
    """Datasets page"""
    datasets = DataSet.objects.order_by('date_added')
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