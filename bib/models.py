from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
from idprovider.models import IdProvider
from vocabs.models import SkosConcept
from places.models import Place


class Person(IdProvider):
    """Eine Person, zum Beispiel die Verfasserin eines Werks."""
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    person_gnd = models.CharField(max_length=100, blank=True, null=True)

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_persons')

    def get_next(self):
        next = Person.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Person.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def get_absolute_url(self):
        return reverse('browsing:person_detail', kwargs={'pk': self.id})

    def __str__(self):
        return "{}, {}".format(self.last_name, self.first_name)


class Book(models.Model):
    zoterokey = models.CharField(primary_key=True, max_length=100, blank=True)
    item_type = models.CharField(max_length=100, blank=True, null=True)
    author = models.CharField(
        max_length=250, blank=True, null=True,
        verbose_name="Author Name fetched from Zotero"
    )
    book_author = models.ManyToManyField(Person, blank=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    siglum = models.CharField(
        verbose_name="Sigle", max_length=500, blank=True, null=True,
        help_text="Geben Sie hier die Sigle des publizierten Werks ein")
    publication_title = models.CharField(max_length=100, blank=True, null=True)
    short_title = models.CharField(max_length=500, blank=True, null=True)
    publication_year = models.IntegerField(blank=True, null=True)
    pub_place = models.ManyToManyField(Place, blank=True)
    book_gnd = models.CharField(max_length=500, blank=True, null=True)
    item_type = models.CharField(
        max_length=500, blank=True, null=True, verbose_name="type fetched from Zotero"
    )
    book_type = models.ManyToManyField(SkosConcept, blank=True)

    def get_zotero_url(self):
        "Returns the objects URL pointing to its Zotero entry"
        try:
            base = "https://www.zotero.org/{}/".format(settings.Z_ID_TYPE)
            url = "{}{}/peter_handke_stage_texts/items/itemKey/{}".format(
                base, settings.Z_ID, self.zoterokey
            )
            return url
        except AttributeError:
            return "please provide Zotero settings"

    def __str__(self):
        return "{}, {}".format(self.author, self.title)


class Work(IdProvider):
    "Some Description would be nice"
    work_author = models.ManyToManyField(
        Person, blank=True, related_name="has_work_created",
        verbose_name="Autor")
    work_translator = models.ManyToManyField(
        Person, blank=True, related_name="has_work_translated",
        verbose_name="Übersetzer"
    )
    title = models.CharField(
        verbose_name="Titel", max_length=500, blank=True, null=True,
        help_text="Geben Sie hier den Titel des publizierten Werks ein")
    alt_title = models.ManyToManyField(
        SkosConcept, blank=True, related_name="is_work_alt_title")
    creation_start_date = models.DateField(blank=True, null=True)
    creation_end_date = models.DateField(blank=True, null=True)
    start_date_sure = models.BooleanField(default=True)
    end_date_sure = models.BooleanField(default=True)
    creation_place = models.ManyToManyField(Place, blank=True)
    creation_place_sure = models.BooleanField(default=True)
    published_in = models.ManyToManyField(Book, blank=True, related_name="publication_of_work")
    work_type = models.ManyToManyField(SkosConcept, blank=True)
    main_language = models.ForeignKey(
        SkosConcept, null=True, blank=True, related_name="language_of_work")
    has_translation = models.ForeignKey(
        'self', blank=True, null=True, related_name="is_translation_of"
    )

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_works')

    def get_next(self):
        next = Work.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Work.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    def __str__(self):
        return "Work: {}".format(self.title)

    def get_absolute_url(self):
        return reverse('browsing:work_detail', kwargs={'pk': self.id})


class Speaker(IdProvider):
    name = models.CharField(max_length=500, blank=True, null=True)
    definition = models.CharField(max_length=500, blank=True, null=True)
    alt_name = models.ManyToManyField(SkosConcept, blank=True)

    def __str__(self):
        return "Speaker: {}".format(self.name)


class Quote(IdProvider):
    """Provides the context of quotes"""
    book_source = models.ForeignKey(Book, blank=True, null=True, related_name="has_quotes")
    startpage = models.IntegerField(blank=True)
    endpage = models.IntegerField(blank=True)
    text = models.TextField(blank=True)
    quote_type = models.ManyToManyField(SkosConcept, blank=True)
    part_of = models.ManyToManyField('self', blank=True)
    auto_trans = models.ManyToManyField('self', blank=True)

    def get_next(self):
        next = Quote.objects.filter(id__gt=self.id)
        if next:
            return next.first().id
        return False

    def get_prev(self):
        prev = Quote.objects.filter(id__lt=self.id).order_by('-id')
        if prev:
            return prev.first().id
        return False

    @classmethod
    def get_listview_url(self):
        return reverse('browsing:browse_quotes')

    def __str__(self):
        return "{}".format(self.text)

    def get_absolute_url(self):
        return reverse('browsing:quote_detail', kwargs={'pk': self.id})


class PartOfQuote(IdProvider):
    """A class modeling quotes"""
    text = models.CharField(blank=True, max_length=500)
    part_of = models.ForeignKey(Quote, blank=True, null=True, related_name="has_chunks")
    source = models.ForeignKey(Work, blank=True, null=True)
    follows = models.ForeignKey('self', blank=True, null=True, related_name='has_follower')
    translates = models.ManyToManyField('self', blank=True, related_name='has_translation')
    correct_translation_sure = models.BooleanField(default=True)
    language = models.ForeignKey(SkosConcept, blank=True, null=True, related_name='quote_language')
    partofquote_type = models.ManyToManyField(SkosConcept, blank=True, related_name='quote_type')
    speaker = models.ManyToManyField(Speaker, blank=True)

    def __str__(self):
        return "{} - {}".format(self.id, self.text)
