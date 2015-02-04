from haystack import indexes
from main.models import Title

class TitleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='id')
    def get_model(self):
        return Title


