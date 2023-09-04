from django.contrib.admin.apps import AdminConfig


class APIAdminConfig(AdminConfig):
    default_site = 'admin.TicketServiceAdminSite'
