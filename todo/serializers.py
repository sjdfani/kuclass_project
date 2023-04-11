from rest_framework import serializers
from django.utils import timezone
from .models import Job, JobState


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class CreateJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ('user', 'complete_date',)

    def create(self, validated_data):
        user = self.context['request'].user
        return Job.objects.create(user=user, **validated_data)


class RetrieveUpdateDestroyJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ('user', 'complete_date')

    def update(self, instance, validated_data):
        state = validated_data.get('state', None)
        if state and state == JobState.DONE:
            instance.complete_date = timezone.now()
            instance.save()
        return super().update(instance, validated_data)
