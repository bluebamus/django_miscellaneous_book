import os
import sys
from pathlib import Path
import django
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_basic.settings.dev')
django.setup()

from orm_skills.models_ex.annotation_aggregation_like_excel_models import Product, OrderLog

# animal = Product.objects.create(name='동물동요', price=8200)
# pack = Product.objects.create(name='사운드북 패키지', price=38400)
# abc = Product.objects.create(name='ABC Activity', price=9900)

animal = Product.objects.get(name='동물동요')
pack = Product.objects.get(name='사운드북 패키지')
abc = Product.objects.get(name='ABC Activity')

import datetime
may1 = datetime.datetime(2016, 4, 1)
may2 = datetime.datetime(2016, 4, 2)
may3 = datetime.datetime(2016, 4, 3)

OrderLog.objects.bulk_create([
    OrderLog(created=may1, product=abc),
    OrderLog(created=may1, product=animal),
    OrderLog(created=may1, product=pack),
    OrderLog(created=may1, product=abc),
    OrderLog(created=may1, product=animal),
    OrderLog(created=may1, product=pack),
    OrderLog(created=may2, product=pack),
    OrderLog(created=may2, product=abc),
    OrderLog(created=may2, product=abc),
    OrderLog(created=may2, product=animal),
    OrderLog(created=may2, product=abc),
    OrderLog(created=may2, product=animal),
    OrderLog(created=may3, product=animal),
    OrderLog(created=may3, product=pack),
    OrderLog(created=may3, product=animal),
    OrderLog(created=may3, product=abc)
])