from django.contrib import admin
from .models import Workflow, Step, Rule, Execution
admin.site.register(Workflow)
admin.site.register(Step)       
admin.site.register(Rule)
admin.site.register(Execution)  

# Register your models here.
