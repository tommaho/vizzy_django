"""Custom file validators."""
from django.core.exceptions import ValidationError
import os
import magic

def has_csv_extension(arg):
    extension = os.path.splitext(arg.name)[1]
    if extension.lower() != '.csv':
        raise ValidationError('File does not have a .csv extension.')
    
def has_valid_encoding(arg):
    try:
        content = arg.read().decode('utf-8')
    
    except UnicodeDecodeError:

        raise ValidationError('File does not use UTF-8 encoding.')
    arg.seek(0)



def has_correct_mime_type(buffer):
    mime_type = magic.from_buffer(buffer.read(1024), mime=True)
    if mime_type != 'text/csv':
        raise ValidationError("The uploaded file is not a CSV.")
    buffer.seek(0)