import logging

from django.db import models
from uuslug import uuslug

logger = logging.getLogger("django-slug-model-mixin")


class SlugModelMixin(models.Model):
    slugged_field = "title"  # 'title or name or what ever
    slug_unique = True  # 'title or name or what ever
    force_slugify = False

    slug = (
        models.SlugField()
    )  # eliminato unique=True x la questione della preview e del linguaggio...

    class Meta:
        abstract = True
        # unique_together = ('slug',)

    def prepare_slug(self):
        if not self.slug:
            _slugged_field = getattr(self, self.slugged_field)
            self.slug = uuslug(_slugged_field, instance=self)
        else:
            self.slug = uuslug(self.slug, instance=self)

    def save(self, *args, **kwargs):
        self.prepare_slug()
        super(SlugModelMixin, self).save(*args, **kwargs)
