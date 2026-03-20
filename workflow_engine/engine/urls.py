from django.urls import path
from . import views
from .api_views import *
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('workflows/', views.workflow_list, name='workflow_list'),
    path('create/', views.create_workflow, name='create_workflow'),
    path('step/<uuid:workflow_id>/', views.add_step, name='add_step'),
    path('rule/<uuid:step_id>/', views.add_rule, name='add_rule'),
    path('execute/<uuid:workflow_id>/', views.execute, name='execute'),
    path('logs/<uuid:execution_id>/', views.logs, name='logs'),
    path('api/workflows/', get_workflows),
    path('api/workflows/create/', create_workflow_api),
    path('api/execute/<uuid:workflow_id>/', execute_api),
    path('api/execution/<uuid:execution_id>/', execution_status),
    path('builder/<uuid:workflow_id>/', views.builder, name='builder'),
    path('graph/<uuid:workflow_id>/', views.graph, name='graph'),
    path('save-step/', views.save_step, name='save_step'),
    path('graph/<uuid:workflow_id>/', views.graph, name='graph'),
    path('edit-step/<uuid:step_id>/', views.edit_step),
    path('delete-step/<uuid:step_id>/', views.delete_step),
    path('delete-rule/<uuid:rule_id>/', views.delete_rule),
    path('edit-rule/<uuid:rule_id>/', views.edit_rule),
]