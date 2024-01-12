from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from panel import *
import sqlite3
import sys

# Arayüz İşlemleri
#--------------------------------------------------------------------------------------------
uygulama = QApplication(sys.argv)
pencere = QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(pencere)
pencere.show()

# Veritabanı işlemleri
#---------------------------------------------------------------------------------------------
baglanti = sqlite3.connect("kayit.db")
islem = baglanti.cursor()

# Tablo oluşturulması ve commit işlemi
islem.execute("CREATE TABLE IF NOT EXISTS Kayit (Ad text, Soyad text, Okul text)")
baglanti.commit()

ui.tbl1.setHorizontalHeaderLabels(("Ad","Soyad","Okul"))
def kayit_ekle():
    Ad = ui.lne1.text()
    Soyad = ui.lne2.text()
    Okul = ui.cmb1.currentText()

    # Check if all fields are filled
    if not Ad or not Soyad or not Okul:
        QMessageBox.warning(pencere, "Uyarı", "Tüm alanları doldurun!", QMessageBox.Ok)
        return

    try:
        ekle = "INSERT INTO Kayit(Ad,Soyad,Okul) VALUES (?,?,?)"
        islem.execute(ekle, (Ad, Soyad, Okul))
        baglanti.commit()

        # Show a pop-up message when the record is added
        QMessageBox.information(pencere, "Kayıt Eklendi", "Kayıt başarıyla eklendi!", QMessageBox.Ok)

        # Clear the input fields
        ui.lne1.clear()
        ui.lne2.clear()
        ui.cmb1.setCurrentIndex(0)  # Set the combo box to the first item (assuming it's an appropriate default)

        kayit_listele()

    except Exception as e:
        # Show an error pop-up message if the record cannot be added
        QMessageBox.critical(pencere, "Hata", f"Kayıt Eklenemedi: {str(e)}", QMessageBox.Ok)

def kayit_listele():
    ui.tbl1.clear()
    ui.tbl1.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    ui.tbl1.setHorizontalHeaderLabels(("Ad" ,"Soyad","Okul")) 
    sorgu = "SELECT * FROM Kayit"
    islem.execute(sorgu)


    for indexSatir,kayitNumarasi in enumerate(islem):
        for IndexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tbl1.setItem(indexSatir,IndexSutun,QTableWidgetItem(str(kayitSutun)))


def kayit_sil():
    sil_mesaj = QMessageBox.question(pencere, "Silme Onayı", "Silmek İstediğinize Emin Misiniz?", 
                                     QMessageBox.Yes | QMessageBox.No)

    if sil_mesaj == QMessageBox.Yes:
        secilen_kayit = ui.tbl1.selectedItems()
        
        if secilen_kayit:
            silinecek_kayit = secilen_kayit[0].text()
            sorgu = "DELETE FROM Kayit WHERE Ad = ?"

            try:
                islem.execute(sorgu, (silinecek_kayit,))
                baglanti.commit()
                ui.statusbar.showMessage("Kayıt Silindi", 10000)
                kayit_listele()
            except Exception as e:
                ui.statusbar.showMessage(f"Kayıt Silinemedi: {str(e)}", 10000)
        else:
            ui.statusbar.showMessage("Silinecek bir kayıt seçiniz.", 10000)
    else:
        ui.statusbar.showMessage("İşlem İptal Edildi", 10000)


def Okula_göre_listele():
    listelenecek_Okul = ui.cmb2.currentText()
    sorgu = "select * From Kayit where Okul = ?"
    islem.execute(sorgu,(listelenecek_Okul,))
    ui.tbl1.clear()
    ui.tbl1.setHorizontalHeaderLabels(("Ad" ,"Soyad","Okul")) 
    for indexSatir,kayitNumarasi in enumerate(islem):
        for IndexSutun,kayitSutun in enumerate(kayitNumarasi):
            ui.tbl1.setItem(indexSatir,IndexSutun,QTableWidgetItem(str(kayitSutun)))



# Butonlar
#------------------------------------------------------------------
         
ui.btn1.clicked.connect(kayit_ekle)
ui.btn2.clicked.connect(kayit_sil)
ui.btn3.clicked.connect(Okula_göre_listele)

kayit_listele()


sys.exit(uygulama.exec_())
