from rest_framework import serializers
from django.db.models import Q
from .models import Class, RepeatChoose
from datetime import timedelta
from kuclass_project.settings import env
import uuid
from lessons.serializers import LessonSerializer


class ClassSerializer(serializers.ModelSerializer):
    lesson = LessonSerializer(read_only=True)

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
        if not Class.objects.filter(lookup, status=True).exists():
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
            obj = Class.objects.get(user=user, pk=pk, status=True)
            obj.delete()
            message['delete'] = f'object with pk={pk} was deleted'
        else:
            items = Class.objects.filter(
                user=user, uuid=unique_id, status=True)
            for i, obj in enumerate(items.iterator()):
                message[f'delete-{i+1}'] = f'object with pk={obj.pk} was deleted'
                obj.delete()
        return message


class UpdateClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        exclude = ('uuid', 'user', 'status', 'repeat')


class UpdateMultiClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        exclude = ('uuid', 'user', 'status', 'repeat')

    def validate(self, attrs):
        request = self.context['request']
        pk = self.context['pk']
        if not Class.objects.filter(user=request.user, pk=pk, status=True).exists():
            return serializers.ValidationError('there is no class with your information')
        return attrs

    def update(self, instance, validated_data, repeat: str):
        if repeat == RepeatChoose.ONE:
            instance.lesson = validated_data.get('lesson', instance.lesson)
            instance.start_time = validated_data.get(
                'start_time', instance.start_time)
            instance.end_time = validated_data.get(
                'end_time', instance.end_time)
            instance.date_of_day = validated_data.get(
                'date_of_day', instance.date_of_day)
            instance.save()
        else:
            request = self.context['request']
            items = Class.objects.filter(
                user=request.user, uuid=instance.uuid, status=True)
            for obj in items.iterator():
                obj.lesson = validated_data.get('lesson', obj.lesson)
                obj.start_time = validated_data.get(
                    'start_time', obj.start_time)
                obj.end_time = validated_data.get(
                    'end_time', obj.end_time)
                obj.date_of_day = validated_data.get(
                    'date_of_day', obj.date_of_day)
                obj.save()
        return instance

    def save(self, pk: int, repeat: str, **kwargs):
        request = self.context['request']
        obj = Class.objects.get(user=request.user, pk=pk, status=True)
        self.update(obj, self.validated_data, repeat)
