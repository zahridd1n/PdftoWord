from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class File(models.Model):
    file = models.FileField(upload_to='file')


# @receiver(pre_delete, sender=File)
# def delete_file_with_user(sender, instance, **kwargs):
#     """funksiya UserImage modelidan rasmlarni o'chirgandan so'ng,
#     bu rasmlarni diskdan ham o'chiradi. """
#     if instance.file:
#         # Rasmi diskdan o'chirish
#         instance.file.delete(False)
