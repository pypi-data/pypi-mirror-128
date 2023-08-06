import seaborn

from dsmlbc6_ebruagbay.hi import hello
from dsmlbc6_ebruagbay.hi import hello4 #geçici bellek burası.. hellonun bulunduğu hi.py kalıcı bellekte bir değişiklik yapıldığında yeniden başlatılması gerekir.
hello()
hello4()

import seaborn as sns
df=sns.load_dataset("tips")

from dsmlbc6_ebruagbay.eda.eda import grab_col_names, check_dataframe
grab_col_names(df)
check_dataframe(df)

from dsmlbc6_ebruagbay.eda.eda import *
help(dsmlbc6_ebruagbay.eda.eda)

import dsmlbc6_ebruagbay
help(dsmlbc6_ebruagbay)

from dsmlbc6_ebruagbay.eda import eda
help(eda)

import pandas as pd
help(pd)
# PACKAGE CONTENTS
#     _config (package)
#     _libs (package)
#     _testing (package)
#     _typing
#     _version
#     api (package)
#     arrays (package)
#     compat (package)
#     conftest
#     core (package)
#     errors (package)
#     io (package)
#     plotting (package)
#     testing
#     tests (package)
#     tseries (package)
#     util (package)

help(pd.tseries)

