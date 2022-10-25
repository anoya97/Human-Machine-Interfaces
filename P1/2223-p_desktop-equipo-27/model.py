from __future__ import annotations
import cheathelper
import webbrowser


class ModelCheat:

    # ======================Se comunica con el helper para obtener el Sheet del comando=================================
    def get_cheetsheet(self, comando: str):
        return cheathelper.get_cheatsheet(comando)

    # =========================Se comunica con la fucnión aux para obtener el string====================================
    def get_cheetsheet_as_string(self, comando: str):     # ANTIGUO AUXILIAR
        return cheathelper.takeText(comando)

        # =========================================LLamar al modelo para paginas web========================================
    def commentsModel(self):
        webbrowser.open(
            "https://twitter.com/intent/follow?original_referer=https%3A%2F%2Fcheat.sh%2F&ref_src=twsrc%5Etfw%7Ctwcamp%5Ebuttonembed%7Ctwterm%5Efollow%7Ctwgr%5Eigor_chubin&region=follow_link&screen_name=igor_chubin")

