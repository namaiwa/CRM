from django import conf


def app_discover():
    for app in conf.settings.INSTALLED_APPS:
        try:
            exec('import %s.superadmin'% app)
        except ImportError:
            pass
