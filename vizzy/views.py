from django.shortcuts import render, redirect
from .forms import DataSetForm
from .models import DataSet
import pandas as pd

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

            DataSet.objects.create(
                name = "test", # form.file_name,
                column_count = len(dataframe.columns),
                columns = ', '.join(dataframe.columns),
                row_count = len(dataframe),
                data = dataframe.to_json(),
                # owner = "tommaho"
            )


            return redirect('vizzy:visualize')
        else: 
            errors = form.errors

            return render(request, 'vizzy/create.html', {'form': form, 'errors': errors})

        

    context = {'form': form}
    return render(request, 'vizzy/create.html', context)



def datasets(request):
    """Datasets page"""
    return render(request, 'vizzy/datasets.html')

def visualize(request):
    """Vizualization page"""
    return render(request, 'vizzy/visualize.html')