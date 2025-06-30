from django.utils.timezone import now


def get_time_ago(post_time):
    delta = now() - post_time
    days = delta.days
    seconds = delta.seconds

    if days >= 30:
        months = days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    elif days >= 1:
        return f"{days} day{'s' if days > 1 else ''} ago"
    else:
        hours = seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
