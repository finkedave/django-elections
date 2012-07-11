from django.conf import settings
from django.db.models import Q
DEFAULT_SETTINGS = {
    'TEST_DATA_ONLY': False,
    'FTP_USER': 'anonymous',
    'FTP_PASSWORD': '',
    'FTP_HOST': '',
    'DOWNLOAD_PATHS': [],
    'DEST_PATH': '/tmp/election/',
    'IMAGE_MODEL': None,
    'IMAGE_STORAGE': settings.DEFAULT_FILE_STORAGE,
    'MAP_RESULTS_DEST': '',
    'HOT_RACE_RELATION_MODELS': [],
}

USER_SETTINGS = DEFAULT_SETTINGS.copy()
USER_SETTINGS.update(getattr(settings, 'ELECTIONS_SETTINGS', {}))
globals().update(USER_SETTINGS)
HOT_RACE_RELATIONS = [Q(app_label=al, model=m) for al, m in [x.rsplit('.', 1) for x in HOT_RACE_RELATION_MODELS]]