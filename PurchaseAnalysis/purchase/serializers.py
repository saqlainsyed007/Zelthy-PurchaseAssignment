import calendar
from datetime import datetime

from rest_framework import serializers


def validate_date(field_name, date_string, date_format):
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        raise serializers.ValidationError({
            field_name: (
                f"Invalid date {date_string}. Must be of format {date_format}"
            )
        })

class PurchaseDataParamSerializer(serializers.Serializer):

    start_date = serializers.CharField()
    end_date = serializers.CharField()

    def validate_start_date(self, start_date):
        start_date = validate_date('start_date', start_date, "%Y-%m")
        start_date = start_date.replace(day=1)
        return start_date.date()

    def validate_end_date(self, end_date):
        end_date = validate_date('end_date', end_date, "%Y-%m")
        last_day = calendar.monthrange(end_date.year, end_date.month)[1]
        end_date = end_date.replace(day=last_day)
        return end_date.date()
