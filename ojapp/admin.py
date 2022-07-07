from django.contrib import admin
from ojapp.models import Problem,Solution,Testcases,Score

# Register your models here.
admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(Testcases)
admin.site.register(Score)