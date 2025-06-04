from django.db import models
from leases.models import Lease

PAYMENT_METHODS = [
    ('mpesa', 'M-PESA'),
    ('bank', 'Bank Transfer'),
    ('airtel', 'Airtel Money'),
    ('tkash', 'T-Kash'),
    ('manual', 'Manual'),
]

class Payment(models.Model):
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('paid', 'Paid')])
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='mpesa')
    reference = models.CharField(max_length=100, blank=True)
    proof = models.FileField(upload_to='payment_proofs/', blank=True, null=True)

    def __str__(self):
        return f"{self.get_method_display()} {self.amount} on {self.date}"
