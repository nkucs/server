from django.conf.urls import url
from user.views.admin_staff import GetStaffListAPI, DeleteStaffAPI, GetStaffAPI,CreateStaffAPI,GetOneStaffAPI,UpdateStaffAPI


urlpatterns = [
    url(r'staff_list?$', GetStaffListAPI.as_view(), name="get_staff_list"),
    url(r'delete_staff?$', DeleteStaffAPI.as_view(), name="delete_staff"),
    url(r'staff_details?$', GetStaffAPI.as_view(), name="staff_details"),

    url(r'staff_create/?$', CreateStaffAPI.as_view(), name="staff_create"),
    url(r'staff_get/?$', GetOneStaffAPI.as_view(), name="staff_get"),
    url(r'staff_update/?$', UpdateStaffAPI.as_view(), name="staff_update"),
]