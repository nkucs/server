from .models import CaseStatus, ProblemSubmissionCase, ProblemSubmission
from django.contrib import admin


admin.site.register(CaseStatus)
admin.site.register(ProblemSubmission)
admin.site.register(ProblemSubmissionCase)

