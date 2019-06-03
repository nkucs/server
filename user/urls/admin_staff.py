from django.conf.urls import url
from user.views.admin_staff import GetStaffListAPI, DeleteStaffAPI, GetStaffAPI


urlpatterns = [
    url(r'staff_list?$', GetStaffListAPI.as_view(), name="get_staff_list"),
    url(r'delete_staff?$', DeleteStaffAPI.as_view(), name="delete_staff"),
    url(r'staff_details?$', GetStaffAPI.as_view(), name="staff_details"),
]