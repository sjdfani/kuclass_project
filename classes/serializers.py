from rest_framework import serializers
from django.db.models import Q
from .models import Class, RepeatChoose
from datetime import timedelta
from kuclass_project.settings import env
import uuid


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'


class CreateClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        exclude = ('uuid', 'user')

    def create(self, validated_data):
        request = self.context['request']
        unique_id = uuid.uuid4().hex
        if validated_data['repeat'] == RepeatChoose.ONE:
            obj = Class.objects.create(
                uuid=unique_id,
                user=request.user,
                lesson=validated_data['lesson'],
                start_time=validated_data['start_time'],
                end_time=validated_data['end_time'],
                date_of_day=validated_data['date_of_day'],
                repeat=validated_data['repeat'],
            )
        elif validated_data['repeat'] == RepeatChoose.ALL_WEEKS:
            current_date = validated_data['date_of_day']
            count_of_week = env('COUNT_OF_WEEKS', cast=int)
            for _ in range(count_of_week):  # means 16 week
                obj = Class.objects.create(
                    uuid=unique_id,
                    user=request.user,
                    lesson=validated_data['lesson'],
                    start_time=validated_data['start_time'],
                    end_time=validated_data['end_time'],
                    date_of_day=current_date,
                    repeat=validated_data['repeat'],
                )
                current_date += timedelta(days=7)
        elif validated_data['repeat'] == RepeatChoose.SEVERAL:
            list_of_dates = request.data.get('list_of_dates', [])
            list_of_dates.append(validated_data['date_of_day'])
            for item in list_of_dates:
                obj = Class.objects.create(
                    uuid=unique_id,
                    user=request.user,
                    lesson=validated_data['lesson'],
                    start_time=validated_data['start_time'],
                    end_time=validated_data['end_time'],
                    date_of_day=item,
                    repeat=validated_data['repeat'],
                )
        return obj


class DeleteClassSerializer(serializers.Serializer):
    unique_id = serializers.CharField(max_length=50)
    pk = serializers.IntegerField()
    repeat = serializers.CharField(max_length=9)

    def validate(self, attrs):
        request = self.context['request']
        lookup = Q(user=request.user) & Q(
            pk=attrs['pk']) & Q(uuid=attrs['unique_id'])
        if not Class.objects.filter(lookup).exists():
            raise serializers.ValidationError(
                'there is no class with your input information')
        return attrs

    def save(self, **kwargs):
        message = dict()
        user = self.context['request']
        unique_id = self.validated_data['unique_id']
        pk = self.validated_data['pk']
        repeat = self.validated_data['repeat']
        if repeat == RepeatChoose.ONE:
            obj = Class.objects.get(user=user, pk=pk)
            obj.delete()
            message['delete'] = f'object with pk={pk} was deleted'
        elif repeat == RepeatChoose.ALL_WEEKS:
            items = Class.objects.filter(user=user, uuid=unique_id)
            for i, obj in enumerate(items.iterator()):
                message[f'delete-{i+1}'] = f'object with pk={obj.pk} was deleted'
                obj.delete()
        return message
