from django.contrib import admin


class TicketServiceAdminSite(admin.AdminSite):
    title_header = 'Ticket Service Admin'
    site_header = 'Ticket Service administration'
    index_title = 'Ticket Service site admin'
