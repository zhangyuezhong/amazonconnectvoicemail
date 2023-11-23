def convert_time_to_seconds(input_time):
    if input_time is None:
        raise ValueError("Invalid input format")

    time_mapping = {
        'second': 1,
        'seconds': 1,
        'minute': 60,
        'minutes': 60,
        'hour': 3600,
        'hours': 3600,
        'day': 86400,
        'days': 86400,
        'week': 604800,
        'weeks': 604800,
        'month': 2592000,
        'months': 2592000,
        'year': 31536000,
        'years': 31536000,
    }

    parts = input_time.split()

    if len(parts) >= 2:  # Only consider the first two words
        try:
            # Strip leading and trailing whitespace
            numeric_value = int(parts[0].strip())
            # Strip leading and trailing whitespace
            time_unit = parts[1].lower().strip()

            if time_unit in time_mapping:
                return numeric_value * time_mapping[time_unit]
            else:
                raise ValueError(f"Unrecognized time unit: {time_unit}")
        except ValueError:
            raise ValueError("Invalid numeric value")
    else:
        raise ValueError("Invalid input format")
