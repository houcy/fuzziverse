from django.db import models
from django.utils import timezone
import uuid

class Application(models.Model):
    name = models.CharField(max_length=1024, unique=True)
    url = models.CharField(max_length=1024, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    __repr__ = __str__

class Report(models.Model):
    title = models.CharField(max_length=1024)
    url = models.CharField(max_length=1024)
    app = models.ForeignKey(Application)

    def __str__(self):
        return self.url
    __repr__ = __str__

class FuzzingAttempt(models.Model):
    app = models.ForeignKey(Application)
    created = models.DateTimeField(default=timezone.now)
    fuzzer_stats = models.TextField(verbose_name='fuzzer_stats contents')
    notes = models.TextField(verbose_name='Notes (version, patches, extra '
                             'environment setup like LD_PRELOAD):')

    # http://stackoverflow.com/a/1737078/1091116
    def save(self, *args, **kwargs):
        if not self.id:
            self.created = timezone.now()
        return super(FuzzingAttempt, self).save(*args, **kwargs)

def upload_path_handler(instance, filename):
    return 'static/%s' % uuid.uuid4()

class InputTestCase(models.Model):
    the_file = models.FileField(upload_to=upload_path_handler)
    attempt = models.ForeignKey(FuzzingAttempt)
