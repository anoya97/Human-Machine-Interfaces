from view import View
from model import ModelCheat
from presenter import CheatPresenter
import gettext
import locale
from pathlib import Path


if __name__ == '__main__':
    mytextdomain = 'cheatSh'
    locale.setlocale(locale.LC_ALL, '')
    LOCALE_DIR = Path(__file__).parent / "locale"
    locale.bindtextdomain('cheatSh', LOCALE_DIR)
    gettext.bindtextdomain('cheatSh', LOCALE_DIR)
    gettext.textdomain('cheatSh')

    CheatPresenter(
        model=ModelCheat(),
        view=View()
    ).run()

