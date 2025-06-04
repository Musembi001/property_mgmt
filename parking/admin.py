from django.contrib import admin
from .models import ParkingSlot, ParkingAssignment

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'location', 'is_active')
    search_fields = ('slot_number', 'location')
    list_filter = ('is_active',)

@admin.register(ParkingAssignment)
class ParkingAssignmentAdmin(admin.ModelAdmin):
    list_display = ('slot', 'user', 'assigned_at', 'valid_until', 'is_active')
    search_fields = ('slot__slot_number', 'user__username')
    list_filter = ('is_active',)
