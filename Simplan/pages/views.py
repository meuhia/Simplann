# coding: utf-8
from Simplan.utils import render_template


def home(request):
    '''
    Display the home page with last topics added
    '''
    return render_template('pages/home.html', {
    })

def about(request):
    '''
    Display many informations about the website
    '''
    return render_template('pages/about.html')
