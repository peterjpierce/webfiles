from app import app

DATE_FORMAT = '%Y-%m-%d'


@app.template_filter('formatted_date')
def _format_datetime_filter(datetime_obj, fmt=DATE_FORMAT):
    formatted = '' if datetime_obj is None else datetime_obj.strftime(fmt)
    return formatted
