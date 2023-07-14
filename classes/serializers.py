from rest_framework import serializers
from .models import Class, RepeatChoose
import uuid
from datetime import timedelta
from kuclass_project.settings import env


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
