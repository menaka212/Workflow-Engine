from .models import Execution


# =========================
# CONDITION EVALUATION
# =========================
def evaluate_condition(condition, data):
    try:
        condition = condition.replace("&&", "and").replace("||", "or")

        for key, value in data.items():
            if isinstance(value, str):
                condition = condition.replace(key, f"'{value}'")
            else:
                condition = condition.replace(key, str(value))

        return eval(condition)
    except Exception:
        return False


# =========================
# GET NEXT STEP (FIXED)
# =========================
def get_next_step(step, data):
    rules = step.rules.all().order_by('priority')

    default_step = None

    for rule in rules:
        if rule.condition == "DEFAULT":
            default_step = rule.next_step
            continue

        if evaluate_condition(rule.condition, data):
            return rule.next_step

    return default_step


# =========================
# EXECUTE WORKFLOW
# =========================
def execute_workflow(workflow, input_data):

    # 🔥 Ensure start step exists FIRST
    step = workflow.start_step

    if not step:
        step = workflow.step_set.order_by('order').first()
        workflow.start_step = step
        workflow.save()

    # 🔥 Fail safe
    if not step:
        return Execution.objects.create(
            workflow=workflow,
            workflow_version=workflow.version,
            status='failed',
            data=input_data,
            current_step=None,
            logs=[{"error": "No steps found"}]
        )

    # ✅ NOW create execution
    execution = Execution.objects.create(
        workflow=workflow,
        workflow_version=workflow.version,
        status='in_progress',
        data=input_data,
        current_step=step,
        logs=[]
    )

    while step:

        step_log = {
            "step_name": step.name,
            "step_type": step.step_type,
            "evaluated_rules": [],
            "selected_next_step": None,
            "status": "pending"
        }

        # =========================
        # APPROVAL STEP
        # =========================
        if step.step_type == "approval":
            execution.status = "pending"
            execution.current_step = step

            step_log["status"] = "waiting_for_approval"

            execution.logs = execution.logs + [step_log]
            execution.save()

            return execution

        # =========================
        # RULE EVALUATION
        # =========================
        rules = step.rules.all().order_by('priority')

        next_step = None
        default_step = None

        for rule in rules:

            if rule.condition == "DEFAULT":
                default_step = rule.next_step
                continue

            result = evaluate_condition(rule.condition, input_data)

            step_log["evaluated_rules"].append({
                "rule": rule.condition,
                "result": result
            })

            if result:
                next_step = rule.next_step
                break

        # fallback
        if not next_step:
            next_step = default_step

        # =========================
        # LOG DECISION
        # =========================
        step_log["selected_next_step"] = (
            next_step.name if next_step else "END"
        )
        step_log["status"] = "completed"

        execution.logs = execution.logs + [step_log]
        execution.save()

        step = next_step

    # =========================
    # COMPLETE
    # =========================
    execution.status = 'completed'
    execution.current_step = None
    execution.save()

    return execution