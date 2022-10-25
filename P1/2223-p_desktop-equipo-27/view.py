from __future__ import annotations
from typing import Protocol
import subprocess
import gettext

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

_ = gettext.gettext
N_ = gettext.ngettext

# ===============================Clase para la comunicación con el presenter===============================

class ViewHandler(Protocol):
    def on_search_clicked(widget) -> None: pass
    def on_button_clicked(widget, path) -> None: pass
    def on_showHelp_clicked(widget) -> None: pass
    def on_sendComments_clicked(widget) -> None: pass
    def on_about_clicked(widget) -> None: pass
    def on_openNew_clicked(widget) -> None: pass
    def on_closeApp_clicked(widget) -> None: pass
    def on_darkMode_clicked(widget) -> None: pass
    def on_clearMode_clicked(widget) -> None: pass
    def on_filter_clicked(widget) -> None: pass
    def on_messageDialogButton_clicked(widget) -> None: pass
    def on_filterButton_clicked(widget) -> None: pass
class View:

    run_on_main_thread = GLib.idle_add

    # ================================CONSTRUCTOR================================
    def __init__(self):
        self.handler = None
        self.commandList = []
        self.separatorList = []

    # ================================DEFINICIONES PARA LA ACTIVACIÓN================================
    def on_activate(self):
        self.build()
        self.execute()

    def execute(self):
        # MUESTA LA VENTANA
        self.window.connect("destroy", Gtk.main_quit)
        self.show_all()
        self.hideFilter()
        Gtk.main()

    def set_handler(self, handler: ViewHandler) -> None:
        self.handler = handler

    # ================================CONSTRUCTOR DEL DISEÑO================================
    def build(self):

        # ================================VENTANA PRINCIPAL================================
        self.window = Gtk.ApplicationWindow(
            title=_("Cheat.sh Searcher"),
            default_height=500,
            default_width=1000,
        )
        self.window.connect("destroy", Gtk.main_quit)

        # ================================Creación de Boxes================================
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # BOX PRINCIPAL
        self.secondaryBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # BOX PARA EL MENU BAR
        self.searchBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # BOX PARTE IZQUIERDA
        self.answerBox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # BOX PARTE DERECHA
        self.searchBarBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)  # BOX PARA LA BUSQUEDA JUNTO CON EL SPINNER
        self.boxScrollWinL = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # BOX PARA LOS BUSQUEDA DE COMANDOS MANUAL
        self.boxScrollWinR = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)  # BOX PARA LA RESPUESTA DE LA BÚSQUEDA
        self.commandBox = Gtk.Box(
            orientation=Gtk.Orientation.VERTICAL)  # BOX PARA LOS COMANDOS ENCONTRADOS DEL SCROLLED WINDOW
        self.filterBox = Gtk.Box(orientation = Gtk.Orientation.HORIZONTAL)    #BOX PARA EL FILTRO


        # ================================Barra de Búsqueda===============================
        self.searchBar = Gtk.SearchEntry()
        self.searchBar.set_placeholder_text(_("Search..."))
        self.searchBar.connect("activate", self.handler.on_search_clicked)

        # ================================Entry para el filtrado===============================
        self.entry = Gtk.Entry()
        self.entry.set_placeholder_text(_("Filter the command... (Example: ls -a)"))
        self.entry.connect("activate", self.handler.on_filter_clicked)
        self.filterButton = Gtk.Button(label=_("Clear"))
        self.filterButton.connect("clicked", self.handler.on_filterButton_clicked)

        # ================================Nombre de la APP================================
        self.image = Gtk.Image()
        self.image.set_from_file("./Cheat.png")

        # ================================Separators===============================
        self.separator1 = Gtk.Separator()
        self.separator2 = Gtk.Separator()
        self.separator1.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.separator2.set_orientation(Gtk.Orientation.VERTICAL)

        # ================================Scroll Bar===============================
        self.scrollBar = Gtk.Scrollbar(orientation=Gtk.Orientation.VERTICAL)

        # ================================Spinner===============================
        self.spinner = Gtk.Spinner()

        # ==================================Menu=================================
        self.menuBar = Gtk.MenuBar()
        file_menu = Gtk.Menu()
        help_menu = Gtk.Menu()
        ver_menu = Gtk.Menu()
        file_menu_dropdown = Gtk.MenuItem(_("File"))
        help_menu_dropdown = Gtk.MenuItem(_("Help"))
        ver_menu_dropdown = Gtk.MenuItem(_("View"))

        # File menu items
        file_new = Gtk.MenuItem(_("New Window"))
        file_close = Gtk.MenuItem(_("Close"))

        # Help menu items
        help_new = Gtk.MenuItem(_("See Help"))
        help_comm = Gtk.MenuItem(_("Send comments"))
        help_about = Gtk.MenuItem(_("About Cheat.sh"))

        # Ver menu items
        see_clear = Gtk.MenuItem(_("Light Mode"))
        see_dark = Gtk.MenuItem(_("Dark Mode"))

        # Dropdowns
        file_menu_dropdown.set_submenu(file_menu)
        help_menu_dropdown.set_submenu(help_menu)
        ver_menu_dropdown.set_submenu(ver_menu)

        # Add menu items
        file_menu.append(file_new)
        file_menu.append(file_close)

        # Add menu items
        help_menu.append(help_new)
        help_menu.append(help_comm)
        help_menu.append(help_about)

        # Add menu items
        ver_menu.append(see_clear)
        ver_menu.append(see_dark)

        # Add to main menu bar
        self.menuBar.append(file_menu_dropdown)
        self.menuBar.append(ver_menu_dropdown)
        self.menuBar.append(help_menu_dropdown)

        # Funcionalidades
        help_new.connect("activate", self.handler.on_showHelp_clicked)
        help_comm.connect("activate", self.handler.on_sendComments_clicked)
        help_about.connect("activate", self.handler.on_about_clicked)
        file_new.connect("activate", self.handler.on_openNew_clicked)
        file_close.connect("activate", self.handler.on_closeApp_clicked)
        see_clear.connect("activate", self.handler.on_clearMode_clicked)
        see_dark.connect("activate", self.handler.on_darkMode_clicked)

        # ================================Scrolled Window Búsqueda===============================
        self.scrolledWindow = Gtk.ScrolledWindow()
        self.scrolledWindow.add(self.boxScrollWinL)

        # ================================Scrolled Window Respuesta===============================
        self.scrolledWindow2 = Gtk.ScrolledWindow()
        self.scrolledWindow2.add(self.commandBox)

        # ================================Message Dialog===============================
        self.messageDialog = Gtk.MessageDialog(transient_for=self.window)
        button = self.messageDialog.add_button("_OK", Gtk.ResponseType.CLOSE)
        button.connect("clicked", self.handler.on_messageDialogButton_clicked)

        # ================================Treeeview===============================
        self.liststore = Gtk.ListStore(str, bool)
        self.suggestedCommands = ["pwd", "cd", "ls", "cat", "cp", "mv", "mkdir", "rmdir",
                                  "rm", "touch", "locate", "find", "grep", "sudo",
                                  "df", "du", "head", "tail", "diff", "tar", "chmod", "chown",
                                  "jobs", "kill", "ping", "wget", "uname", "top", "history",
                                  "man", "echo", "zip", "hostname", "useradd"]

        for i in self.suggestedCommands:
            self.liststore.append([i, False])

        self.treeView = Gtk.TreeView(model=self.liststore)
        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn(_("Popular commands"), renderer_text, text=0)
        self.treeView.append_column(column_text)

        self.renderer_radio = Gtk.CellRendererToggle()
        self.renderer_radio.set_radio(True)
        iter = self.liststore.get_iter_first()
        self.liststore.set_value(iter, 1, False)
        self.renderer_radio.connect("toggled", self.handler.on_button_clicked)
        treeviewcolumn = Gtk.TreeViewColumn("")
        treeviewcolumn.pack_start(self.renderer_radio, False)
        treeviewcolumn.add_attribute(self.renderer_radio, "active", 1)
        self.treeView.append_column(treeviewcolumn)

        # ================================Creación del diseño===============================

        # Creación del Box de los posibles comandos (Izquierda)
        self.boxScrollWinL.pack_start(self.treeView, expand=False, fill=False, padding=0)

        # Creación del Box de la barra de busqueda
        self.searchBarBox.pack_start(self.searchBar, expand=False, fill=True, padding=10)
        self.searchBarBox.pack_start(self.spinner, expand=False, fill=False, padding=10)

        # Creación del Box para el filtrado de los comandos encontrados
        self.filterBox.pack_start(self.entry, expand=True, fill=True, padding=0)
        self.filterBox.pack_start(self.filterButton, expand=False, fill=False, padding=0)

        # Creación del Box de la información del comando encontrado (Derecha)
        self.boxScrollWinR.pack_start(self.filterBox, expand=False, fill=False, padding=0)
        self.boxScrollWinR.pack_start(self.scrolledWindow2, expand=True, fill=True, padding=10)

        # Parte izquierda
        self.searchBox.pack_start(self.searchBarBox, expand=False, fill=False, padding=10)
        self.searchBox.pack_start(self.separator2, expand=False, fill=False, padding=10)
        self.searchBox.pack_start(self.scrolledWindow, expand=True, fill=True, padding=10)

        # Parte derecha
        self.answerBox.pack_start(self.image, expand=False, fill=False, padding=10)
        self.answerBox.pack_start(self.boxScrollWinR, expand=True, fill=True, padding=10)

        # Box secundario
        self.secondaryBox.pack_start(self.searchBox, expand=False, fill=True, padding=10)
        self.secondaryBox.pack_start(self.separator1, expand=False, fill=True, padding=10)
        self.secondaryBox.pack_start(self.answerBox, expand=True, fill=True, padding=10)

        # Box principal
        self.box.pack_start(self.menuBar, expand=False, fill=True, padding=0)
        self.box.pack_start(self.secondaryBox, expand=True, fill=True, padding=10)
        self.window.add(self.box)

    # ================================Funcionalidades Menu===============================
    # Menu Archivo
    def openNew(self):
        subprocess.call("python3 cheatSh.py", shell=True)

    def closeApp(self):
        Gtk.main_quit()

    # Menu View
    def darkMode(self):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", True)

    def clearMode(self):
        settings = Gtk.Settings.get_default()
        settings.set_property("gtk-application-prefer-dark-theme", False)

    # ================================Comando del SearchBar===============================
    def getSearchCommand(self):
        return self.searchBar.get_text()

    def clearSearchBar(self):
        self.searchBar.set_text("")

    # ================================Funcionalidades spinner===============================
    def show_working_searchBar(self):
        self.buttonClean()
        self.spinner.start()
        self.searchBar.set_sensitive(False)
        self.treeView.set_sensitive(False)

    def hide_working_searchBar(self):
        self.spinner.stop()
        self.searchBar.set_sensitive(True)
        self.treeView.set_sensitive(True)

    def show_working_button(self, path):
        self.buttonClean()
        self.spinner.start()
        self.liststore[path][1] = True
        self.searchBar.set_sensitive(False)
        self.treeView.set_sensitive(False)

    def hide_working_button(self):
        self.spinner.stop()
        self.searchBar.set_sensitive(True)
        self.treeView.set_sensitive(True)


    # ================================Funcionalidades Entry===============================
    def getFilterCommand(self):
        return self.entry.get_text()

    def filterCommand(self, command):
        cont = 0

        for widget in self.commandList:

            command2 = f' {command}'
            if self.separatorList:
                if not widget.get_label().startswith(command) and not widget.get_label().startswith(command2):
                    widget.hide()
                    self.separatorList[cont].hide()

            cont += 1

    def showFilter(self):
        self.entry.show()
        self.filterButton.show()

    def hideFilter(self):
        self.entry.hide()
        self.filterButton.hide()

    def clearFilter(self):
        self.window.show_all()
        self.entry.set_text("")

    # ================================Funcionalidades Buttons===============================
    def buttonClean(self):
        for i in range(34):
            self.liststore[i][1] = False

    # ================================Errores Encontrados===============================
    def infoApp(self, title: str, secondary: str) -> None:
        self.messageDialog.set_title(title)
        self.messageDialog.format_secondary_text(secondary)
        self.messageDialog.run()

    # ================================Creación de Widgets================================
    def createLabel(self, text: str) -> None:
        label1 = Gtk.Label(
            label=text,
            halign=Gtk.Align.START
        )
        self.commandList.append(label1)
        self.commandBox.pack_start(label1, expand=False, fill=False, padding=10)
        label1.show()

    def createExpanders(self, command: str, description: str):

        expander1 = Gtk.Expander(label=command)
        label1 = Gtk.Label(
            label=description,
            halign=Gtk.Align.START
        )
        expander1.add(label1)
        self.commandList.append(expander1)
        self.commandBox.pack_start(expander1, expand=False, fill=False, padding=10)

    def createSeparators(self):
        separator = Gtk.Separator()
        separator.set_orientation(Gtk.Orientation.HORIZONTAL)
        self.separatorList.append(separator)
        self.commandBox.pack_start(separator, expand=False, fill=False, padding=10)

    # ================================Gestión de widgets================================
    def closeWindow(self):
        self.messageDialog.hide()

    def closeWidgets(self):
        for widget in self.commandList:
            widget.destroy()

        self.commandList = []
        for separator in self.separatorList:
            separator.destroy()

        self.separatorList = []

    def show_all(self):
        self.window.show_all()


    def updateView(self, controller: bool, text):

        self.closeWidgets()
        self.hideFilter()

        if controller:
            if text.startswith("/*\n * 404"):  # EN CASO DE ERROR
                self.infoApp(_("ERROR 404 NOT FOUND"), text)
            else:  # EN CASO DE COMANDO COMPUESTO O COMANDO NO ENCONTRADO
                self.createLabel(text)

        else:
            if text == "NoRed":     # EN CASO DE NO TENER CONEXIÓN AL SERVIDOR
                self.infoApp(_("ERROR: NO INTERNET CONNECTION"), _("NO CONNECTION"))
            else:   # EN CASO DE QUE LA FUNCIÓN SEA CORRECTA
                for i, r in enumerate(text, start=0):
                    if not text[i].commands == "":
                        self.createExpanders(text[i].commands, text[i].description)
                    else:
                        self.createLabel(text[i].description)

                    self.createSeparators()

                self.show_all()
