from .models import Lab, LabSubmission, LabProblem, LabSubmissionProblemSubmission, Attachment
from django.contrib import admin


admin.site.register(Lab)
admin.site.register(LabProblem)
admin.site.register(LabSubmissionProblemSubmission)
admin.site.register(LabSubmission)
admin.site.register(Attachment)

