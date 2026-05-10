# translation.py

import os, posixpath

from qgis.PyQt.QtCore import (
    QCoreApplication,
    QSettings,
    QTranslator,
    QT_VERSION_STR
)

def setup_translation(plugin_dir, plugin_name):

    locale = QSettings().value('locale/userLocale')[0:2]

    qt_major = QT_VERSION_STR.split('.')[0]

    locale_path = posixpath.join(
        plugin_dir,
        'i18n',
        f'qt{qt_major}',
        f'{plugin_name}_{locale}.qm'
    )

    if not os.path.exists(locale_path):
        return None

    translator = QTranslator()

    if translator.load(locale_path):
        QCoreApplication.installTranslator(translator)
        return translator

    return None