"""Custom file validators."""
from django.core.exceptions import ValidationError
from django.conf import settings
import os
import magic
import csv

def is_correctly_sized(arg):

    try:
        if arg.size >= settings.MAX_FILE_SIZE:
            raise ValidationError(f'File is too large: {arg.size / (1024 * 1024):.2f} MB attempted. ')
    
    except ValidationError:
        raise

    except Exception:
        raise ValidationError('General exception in is_correctly_sized')



def has_csv_extension(arg):
    try:
        extension = os.path.splitext(arg.name)[1]
        if extension.lower() != '.csv':
            raise ValidationError('File does not have a .csv extension.')
    
    except ValidationError:
        raise
    
    except Exception:
        raise ValidationError('General exception in has_csv_extension')


def has_valid_encoding(arg):

    try:
        content = arg.read().decode('utf-8')
    
    except UnicodeDecodeError:
        raise ValidationError('File does not use UTF-8 encoding.')
    
    except Exception:
        raise ValidationError('General exception in has_valid_encoding')
 
    arg.seek(0)



def has_correct_mime_type(arg):
    try:
        mime_type = magic.from_buffer(arg.read(1024), mime=True)
        if mime_type != 'text/csv':
            raise ValidationError("The uploaded file is not a valid CSV.")

    except ValidationError:
        raise

    except Exception:
        raise ValidationError('General exception in has_valid_encoding')
    
    arg.seek(0)


def is_well_formed_csv(arg):
    try:
        content = arg.read().decode('utf-8')
        csv.reader(content.splitlines())

    except Exception:
        raise ValidationError('File does not appear to be valid csv')

    arg.seek(0)