from datetime import datetime


def booking_dates(constant: list, temporary: list, validated_data: dict, user_id: int) -> bool:
    start_date = validated_data['start_date']
    end_date = validated_data['end_date']
    is_temporary = validated_data['temporary']
    if constant:
        return False

    for booking in temporary:
        booked_from = datetime.strptime(booking['booked_from'], '%Y-%m-%d %H:%M:%S%z')
        booked_to = datetime.strptime(booking['booked_to'], '%Y-%m-%d %H:%M:%S%z')
        if booked_from <= end_date or booked_to >= start_date:
            if booking['user_id'] != user_id or is_temporary:
                return False
    return True
