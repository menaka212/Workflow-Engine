from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
import json

from .models import Workflow, Step, Rule, Execution
from .forms import WorkflowForm
from .services import execute_workflow


# =========================
# WORKFLOW LIST + SEARCH
# =========================
def workflow_list(request):
    query = request.GET.get('q')
    workflows = Workflow.objects.all()

    if query:
        workflows = workflows.filter(Q(name__icontains=query))

    return render(request, 'workflow_list.html', {
        'workflows': workflows
    })


# =========================
# CREATE WORKFLOW
# =========================
def create_workflow(request):
    form = WorkflowForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('workflow_list')

    return render(request, 'workflow_form.html', {'form': form})


# =========================
# ADD STEP
# =========================
def add_step(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)

    if request.method == "POST":
        Step.objects.create(
            workflow=workflow,
            name=request.POST['name'],
            step_type=request.POST['step_type'],
            order=int(request.POST['order']),
            metadata=request.POST.get('metadata', '{}')
        )

        return redirect(f'/step/{workflow.id}/')  # 🔥 FIX

    return render(request, 'step_form.html', {'workflow': workflow})


# =========================
# ADD RULE
# =========================
def add_rule(request, step_id):
    step = get_object_or_404(Step, id=step_id)

    if request.method == "POST":
        Rule.objects.create(
            step=step,
            condition=request.POST['condition'],
            priority=int(request.POST['priority']),
            next_step_id=request.POST['next_step']
        )

        return redirect(f'/step/{step.workflow.id}/')  # 🔥 FIX

    return render(request, 'rule_form.html', {'step': step})


# =========================
# DASHBOARD
# =========================
def dashboard(request):
    workflows = Workflow.objects.all()
    executions = Execution.objects.all()

    return render(request, 'dashboard.html', {
        'workflows': workflows,
        'executions': executions
    })


# =========================
# EXECUTE WORKFLOW
# =========================
def execute(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)

    if request.method == "POST":
        data = {}

        for key in workflow.input_schema.keys():
            value = request.POST.get(key)

            # convert numbers
            if value.isdigit():
                value = int(value)

            data[key] = value

        execution = execute_workflow(workflow, data)
        return redirect('logs', execution.id)

    return render(request, 'execute.html', {
        'workflow': workflow
    })


# =========================
# EXECUTION LOGS
# =========================
from django.shortcuts import render, get_object_or_404
from .models import Execution

def logs(request, execution_id):
    execution = get_object_or_404(Execution, id=execution_id)

    return render(request, 'logs.html', {
        'execution': execution
    })


# =========================
# BUILDER (DRAG UI)
# =========================
def builder(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)
    steps = Step.objects.filter(workflow=workflow).order_by('order')

    return render(request, 'builder.html', {
        'workflow': workflow,
        'steps': steps
    })


# =========================
# SAVE STEP (AJAX)
# =========================
def save_step(request):
    if request.method == "POST":
        data = json.loads(request.body)

        step = Step.objects.create(
            workflow_id=data['workflow_id'],
            name=data['name'],
            step_type=data['type'],
            order=data['order']
        )

        return JsonResponse({"status": "saved", "id": str(step.id)})


# =========================
# GRAPH / OVERVIEW
# =========================
def graph(request, workflow_id):
    workflow = get_object_or_404(Workflow, id=workflow_id)

    # 🔥 FIX ORDER ISSUE
    steps = workflow.step_set.all().order_by('order')

    return render(request, "graph.html", {
        "workflow": workflow,
        "steps": steps
    })


# =========================
# EDIT STEP
# =========================
def edit_step(request, step_id):
    step = get_object_or_404(Step, id=step_id)

    if request.method == "POST":
        step.name = request.POST['name']
        step.step_type = request.POST['step_type']
        step.order = int(request.POST['order'])
        step.save()

        return redirect(f'/step/{step.workflow.id}/')

    return render(request, 'edit_step.html', {'step': step})


# =========================
# DELETE STEP
# =========================
def delete_step(request, step_id):
    step = get_object_or_404(Step, id=step_id)
    workflow_id = step.workflow.id
    step.delete()

    return redirect(f'/step/{workflow_id}/')


# =========================
# EDIT RULE
# =========================
def edit_rule(request, rule_id):
    rule = get_object_or_404(Rule, id=rule_id)

    if request.method == "POST":
        rule.condition = request.POST['condition']
        rule.priority = int(request.POST['priority'])
        rule.next_step_id = request.POST['next_step']
        rule.save()

        return redirect(f'/step/{rule.step.workflow.id}/')

    return render(request, 'edit_rule.html', {'rule': rule})


# =========================
# DELETE RULE
# =========================
def delete_rule(request, rule_id):
    rule = get_object_or_404(Rule, id=rule_id)
    workflow_id = rule.step.workflow.id
    rule.delete()

    return redirect(f'/step/{workflow_id}/')