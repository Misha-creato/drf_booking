

def booking_dates(constant: list, temporary: list, validated_data: dict, user_id: int) -> bool:
    start_date = validated_data['start_date']
    end_date = validated_data['end_date']
    if constant:
        return False

    for booking in temporary:
        if booking['booked_from'] < end_date or booking['booked_to'] > start_date:
            if booking['user_id'] != user_id:
                return False
    return True
