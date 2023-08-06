##############################
# 1. PyPi Hesabının Açılması
##############################


##############################
# 2. Proje Klasörü ve Virtual Env Oluşturma
##############################


##############################
# 3. Module, Package, Sub-Package Oluşturulması
##############################

Python'da .py uzantısı olan dosyalar modül olarak tanımlanır. İçerisinde bir çok fonksiyon, metod ve sınıf barındırır.
Paket ise modüllerin organize edildiği klasördür. Birçok python scriptinin bir arada tutulduğu dizindir.

Package  > Subpackage > Module

##############################
# 4. Diğer Proje Dosyalarının Eklenmesi
##############################

# requirements.txt (yaml da olabilir...bir projedeki gerekli versiyonların tutulduğu dosya)
# setup.cfg
# READNME.md
# LICENSE.md
# setup.py (source distribution için, paketleyip yayına hazır hale getirilmesini sağlayan dosyadır)

##############################
# 5. Projenin PyPI'a Yüklenmesi
##############################
 Terminalden "python setup.py sdist" bu kodu çalıştırdığımızda tar.gz PyPI'ın istediği formatta dosyalar oluşturulur..
            pip install twine            
            twine upload dist/*