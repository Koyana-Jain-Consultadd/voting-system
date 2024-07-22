from django.contrib import admin
from .models import *
from django import forms

class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_approved']
    list_filter = ['is_approved']
    actions = ['approve_users', 'reject_users']

    def approve_users(self, request, queryset):
        queryset.update(is_approved=True)

    def reject_users(self, request, queryset):
        queryset.delete()

class CandidatesForm(forms.ModelForm):
    class Meta:
        model = Candidates
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['party'].widget.choices = [(party.pk, party.p_name) for party in Parties.objects.all()]

class CandidatesAdmin(admin.ModelAdmin):
    form = CandidatesForm
    list_display = ['c_name', 'state', 'get_party_name']

    def get_party_name(self, obj):
        return obj.party.p_name

    get_party_name.short_description = 'Party'

class ElectionAdmin(admin.ModelAdmin):
    list_display=['e_name','e_date']

class PartiesAdmin(admin.ModelAdmin):
    list_display=['p_name','sym_name']

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['election'].widget.choices = [(election.pk, election.e_name) for election in Election.objects.all()]
        self.fields['candidate'].widget.choices = [(candidate.pk, candidate.c_name) for candidate in Candidates.objects.all()]

class ResultAdmin(admin.ModelAdmin):
    form = ResultForm
    list_display = ['election_name', 'candidate_name', 'votes']

    def election_name(self, obj):
        return obj.election.e_name

    def candidate_name(self, obj):
        return obj.candidate.c_name

    election_name.short_description = 'Election Name'
    candidate_name.short_description = 'Candidate Name'

admin.site.register(Result, ResultAdmin)
admin.site.register(Parties, PartiesAdmin)
admin.site.register(Election, ElectionAdmin)
admin.site.register(Candidates, CandidatesAdmin)
admin.site.register(User, UserAdmin)
