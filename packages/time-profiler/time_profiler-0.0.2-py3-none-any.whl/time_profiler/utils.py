def format_time(secs: float) -> str:
    secs %= 3600
    minutes = secs // 60
    secs %= 60
    seconds = secs

    if minutes > 0:
        return f"{minutes} min and {seconds} secs"

    return f"{seconds:.2f} secs"
