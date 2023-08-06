import sys
from queue import Queue

from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot

from gb_21_11.finder import Finder
from gb_21_11.finder_ui import Ui_FinderForm


class FinderMonitor(QObject):
    """
    Класс-монитор, принимающий результаты поиска из очереди результатов
    Данный класс будет помещён в отдельный поток QThread
    """
    gotData = pyqtSignal(tuple)
    finished = pyqtSignal(int)

    def __init__(self, parent, urls, text):
        super().__init__()
        self.parent = parent
        self.urls = urls
        self.text = text
        self.res_queue = Queue()
        self.finder = Finder(self.text, self.res_queue)

    def search_text(self):
        """
        Запуск поиска.
        Поиск будет выполняться в отдельном потоке
        """
        self.finder.search_in_urls(self.urls)
        # Текущая функция будет:
        #    - принимать результаты из очереди;
        #    - создавать сигналы для взаимодействия с GUI
        while True:
            data = self.res_queue.get()
            if data is None:
                break
            self.gotData.emit(data)
            self.res_queue.task_done()  # ?

        self.res_queue.task_done()
        self.finished.emit(0)

    def stop(self):
        self.finder.stop_search()


class ProgressDialog(QtWidgets.QDialog):
    """ Класс GUI-формы 'Поисковика' """

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_FinderForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.start_search)
        self.ui.pushButton_2.clicked.connect(self.stop_search)
        self.monitor = None
        self.is_active = False
        self.progress = 0
        self.progress_inc = 1
        self.thread = None

    @pyqtSlot(tuple)
    def update_results(self, data):
        """ Отображение результатов поиска """
        self.ui.plainTextEdit.appendPlainText(f"++ {data[0]} ++")
        for text in data[1]:
            self.ui.plainTextEdit.appendPlainText(f" {text}")
        self.ui.plainTextEdit.appendPlainText("")

    @pyqtSlot()
    def update_progress(self):
        self.progress += self.progress_inc
        self.ui.progressBar.setValue(int(self.progress))

    def stop_search(self):
        if self.monitor is not None:
            self.is_active = False
            self.monitor.stop()

    def finished(self):
        self.is_active = False
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.setEnabled(True)

    def start_search(self):
        if not self.is_active:
            self.ui.plainTextEdit.clear()
            self.is_active = True
            urls = self.ui.plainTextEdit_2.toPlainText().split("\n")
            text = self.ui.lineEdit.text()

            self.progress = 0
            self.progress_inc = 100 / len(urls)

            self.monitor = FinderMonitor(self, urls, text)
            self.monitor.gotData.connect(self.update_results)
            self.monitor.gotData.connect(self.update_progress)

            self.thread = QThread()
            self.monitor.moveToThread(self.thread)

            self.ui.pushButton_2.setEnabled(True)
            self.ui.pushButton.setEnabled(False)

            # slots and signals
            self.thread.started.connect(self.monitor.search_text)
            # self.ui.pushButton_2.clicked.connect(self.monitor.stop)

            self.monitor.finished.connect(self.thread.quit)
            self.monitor.finished.connect(self.finished)

            self.thread.start()


def main():
    app = QtWidgets.QApplication(sys.argv)

    progress = ProgressDialog()
    progress.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())
