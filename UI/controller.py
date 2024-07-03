import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0
        self._mediaUmidita = None
        self._sequenza = []

    def handle_umidita_media(self, e):
        self._mediaUmidita=self._model.get_umiditaMediaPerMese(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"L'umidità nel mese selezionato é:"))
        self._view.lst_result.controls.append(ft.Text(f"Genova: {self._mediaUmidita[2]:.4f}"))
        self._view.lst_result.controls.append(ft.Text(f"Milano: {self._mediaUmidita[1]:.4f}"))
        self._view.lst_result.controls.append(ft.Text(f"Torino: {self._mediaUmidita[0]:.4f}"))
        self._view.update_page()



    def handle_sequenza(self, e):
        self._view.lst_result.controls.clear()
        self._sequenza = self._model.calcola_sequenza(self._mese)
        self._view.lst_result.controls.append(ft.Text(f"La sequenza ottima ha costo {self._sequenza[0]} ed è:"))
        for i in self._sequenza[1]:
            self._view.lst_result.controls.append(ft.Text(i))
        self._view.update_page()

    def read_mese(self, e):
        self._mese = int(e.control.value)

