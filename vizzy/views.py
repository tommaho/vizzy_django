from django.shortcuts import render

# Create your views here.

def index(request):
    """Home page"""
    return render(request, 'vizzy/index.html')

def datasets(request):
    """Datasets page"""
    return render(request, 'vizzy/datasets.html')

def visualize(request):
    """Vizualization page"""
    return render(request, 'vizzy/visualize.html')