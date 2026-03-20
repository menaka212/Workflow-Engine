from rest_framework import serializers
from .models import Workflow, Step, Rule, Execution

class StepSerializer(serializers.ModelSerializer):
    class Meta:
        model = Step
        fields = '__all__'


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = '__all__'


class WorkflowSerializer(serializers.ModelSerializer):
    steps = StepSerializer(many=True, source='step_set', read_only=True)

    class Meta:
        model = Workflow
        fields = '__all__'


class ExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Execution
        fields = '__all__'