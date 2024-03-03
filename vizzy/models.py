from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class DataSet(models.Model):
    """Container for uploaded and converted data files."""
    name = models.CharField(max_length=200)
    column_count = models.IntegerField()
    columns = models.TextField()
    row_count = models.BigIntegerField()
    data = models.BinaryField()
    date_added = models.DateTimeField(auto_now_add=True)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        """Describe the dataset model."""
        return f"{self.name}, {self.column_count} columns and {self.row_count} rows."
    