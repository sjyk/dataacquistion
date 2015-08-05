import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/formoptimization/') # Path to the project directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(__file__))+'/includes/')

from django.core.management import setup_environ
import settings
setup_environ(settings)