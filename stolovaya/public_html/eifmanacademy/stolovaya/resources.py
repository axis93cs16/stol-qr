from import_export import resources
from .models import stolovaya

class CommentResource(resources.ModelResource):
    class Meta:
        model = stolovaya
