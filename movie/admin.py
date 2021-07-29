from django.contrib import admin
from .models import Movie, Score, Comment
# from .models import TestMovie, Testmodel, Entry, Color, Testmodel2
from import_export import resources
from import_export.admin import ImportExportMixin

# class MovieResource(resources.ModelResource):
    # class Meta:
        # model = Movie
        # import_id_fields = ('id',)
        # exclude = ('id',)
		
class MovieAdmin(ImportExportMixin, admin.ModelAdmin):
	# resource_class = MovieResource
	pass

# class ScoreResource(resources.ModelResource):
    # class Meta:
        # model = Score
        # import_id_fields = ('code',)
        # exclude = ('id',)
		
class ScoreAdmin(ImportExportMixin, admin.ModelAdmin):
	# resource_class = ScoreResource
	pass
	
# Register your models here.
admin.site.register(Movie, MovieAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Comment)
# admin.site.register(TestMovie)
# admin.site.register(Entry)
# admin.site.register(Color)
# admin.site.register(Testmodel)
# admin.site.register(Testmodel2)

