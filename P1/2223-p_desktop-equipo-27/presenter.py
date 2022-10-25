from model import ModelCheat
from view import View
from typing import Optional
from time import sleep
from threading import Thread
import gettext


_ = gettext.gettext
N_ = gettext.ngettext

class CheatPresenter:

    def __init__(self, model: Optional[ModelCheat] = None, view: Optional[View] = None):
        self.model = model or ModelCheat()
        self.view = view or View()


    def run(self):
        self.view.set_handler(self)
        self.view.on_activate()

    # ===================================OBTENCIÓN DE INFORMACIÓN DEL SERVIDOR===================================
    def get_cheetsheet(self, comando: str):
        text = self.model.get_cheetsheet(comando)
        return text

    def get_cheetsheet_as_string(self, comando: str):
        text = self.model.get_cheetsheet_as_string(comando)
        return text

    # ================================FUNCIONALIDADES CLICKED================================
    # Funcionalidades SearchBar
    def on_search_clicked(self, widget):
        t = Thread(target=self.do_searchCommand_searchBar, daemon=True)
        t.start()

    def do_searchCommand_searchBar(self):
        command = self.view.getSearchCommand()
        View.run_on_main_thread(self.view.show_working_searchBar)
        self.searchCommand(command)
        View.run_on_main_thread(self.view.hide_working_searchBar)

    # Funcionalidades TreeView
    def on_button_clicked(self, widget, path):
        self.view.clearSearchBar()
        t = Thread(target=self.do_searchCommand_button, args=(path,), daemon=True)
        t.start()

    def do_searchCommand_button(self, path):
        command = self.view.liststore[path][0]
        View.run_on_main_thread(self.view.show_working_button, path)
        self.searchCommand(command)
        View.run_on_main_thread(self.view.hide_working_button)


    # Funcionalidades Menú
    def on_openNew_clicked(self, widget):
        self.view.openNew()

    def on_closeApp_clicked(self, widget):
        self.view.closeApp()

    def on_showHelp_clicked(self, widget):
        self.view.infoApp(_("HELP CHEAT.SH SEARCHER"), _("cheat.sh\n\n"
                                                         "This application allows a simple search for different commands and their uses.\n"
                                                         "Our application displays a search bar on the side by means of which searches "
                                                         "will appear on the right hand side. In addition, it implements a selection of "
                                                         "suggested commands that can be selected by simply clicking on them.\n"
                                                         "Once the results are displayed, there is another search bar on top of the results, "
                                                         "so that the desired command can be filtered.\n"
                                                         "At the top, there is a toolbar with different options, such as opening a new window or closing the current window, among others.\n"))

    def on_sendComments_clicked(self, widget):
        self.model.commentsModel()

    def on_about_clicked(self, widget):
        self.view.infoApp(_("ABOUT CHEAT.SH SEARCHER"), _("cheat.sh\n\n"
                                                         "Cheat.sh searcher is a GUI for the web www.cheat.sh which includes:\n"
                                                         " · A simple user interface.\n"
                                                         " · Coverage on more than 56 programming languages, several DBMSes, and more than 1000 most important UNIX/Linux commands.\n"
                                                         " · Provides access to the best community driven cheat sheets repositories in the world, on par with StackOverflow.\n"
                                                         " · Supports a special stealth mode where it can be used fully invisibly without ever touching a key and making sounds.\n"
                                                         " . On top of all that we offer 2 different ways on how you search your information: with a search bar and suggested commands.\n"
                                                         " . Created by Raúl Fernánadez del Blanco,Armando Martínes Poya, Brais González Piñeiro\n"))

    def on_clearMode_clicked(self, widget):
        self.view.clearMode()

    def on_darkMode_clicked(self, widget):
        self.view.darkMode()

    # ================================Funcionalidades Filter===============================

    def on_filter_clicked(self, widget):
        command = self.view.getFilterCommand()
        self.view.show_all()
        self.view.filterCommand(command)

    def on_filterButton_clicked(self, widget):
        self.view.clearFilter()
    # ================================Funcionalidades MessageDialog===============================

    def on_messageDialogButton_clicked(self, widget):
        self.view.closeWindow()


    # ================================Funcionalidades SearchBar===============================
    def searchCommand(self, command):

        sleep(1)
        searchedCommands = self.get_cheetsheet(command)

        if command:
            if not searchedCommands or searchedCommands[0][0] == "*/":
                text = self.get_cheetsheet_as_string(command)
                View.run_on_main_thread(self.view.updateView, True, text)
            else:
                View.run_on_main_thread(self.view.updateView, False, searchedCommands)
        else:
            View.run_on_main_thread(self.view.closeWidgets)
            View.run_on_main_thread(self.view.hideFilter)