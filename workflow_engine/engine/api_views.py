from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Workflow, Step, Rule, Execution
from .serializers import *
from .services import execute_workflow

# WORKFLOW CRUD

@api_view(['GET'])
def get_workflows(request):
    workflows = Workflow.objects.all()
    return Response(WorkflowSerializer(workflows, many=True).data)


@api_view(['POST'])
def create_workflow_api(request):
    serializer = WorkflowSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


# EXECUTE

@api_view(['POST'])
def execute_api(request, workflow_id):
    workflow = Workflow.objects.get(id=workflow_id)
    execution = execute_workflow(workflow, request.data)

    return Response({
        "execution_id": execution.id,
        "status": execution.status,
        "logs": execution.logs
    })


# GET EXECUTION

@api_view(['GET'])
def execution_status(request, execution_id):
    execution = Execution.objects.get(id=execution_id)
    return Response(ExecutionSerializer(execution).data)

@api_view(['POST'])
def approve_step(request, execution_id):
    execution = Execution.objects.get(id=execution_id)
    step = execution.current_step

    decision = request.data.get("decision")  # approve / reject

    data = execution.data.copy()
    data["decision"] = decision

    # 🔥 Evaluate rules directly (no get_next_step)
    rules = step.rules.all().order_by('priority')
    next_step = None

    step_log = {
        "step_name": step.name,
        "step_type": step.step_type,
        "decision": decision,
        "evaluated_rules": [],
        "selected_next_step": None,
        "status": "completed"
    }

    for rule in rules:
        if rule.condition == "DEFAULT":
            next_step = rule.next_step
            step_log["selected_next_step"] = next_step.name if next_step else None
            break

        try:
            result = eval(rule.condition.replace("&&", "and").replace("||", "or"), {}, data)

            step_log["evaluated_rules"].append({
                "rule": rule.condition,
                "result": result
            })

            if result:
                next_step = rule.next_step
                step_log["selected_next_step"] = next_step.name
                break

        except Exception as e:
            step_log["error"] = str(e)

    # 🔥 Save log
    execution.logs.append(step_log)

    # 🔥 Move to next step
    execution.current_step = next_step

    if not next_step:
        execution.status = "completed"
    else:
        execution.status = "in_progress"

    execution.save()

    return Response({
        "status": execution.status,
        "next_step": next_step.name if next_step else None
    })

