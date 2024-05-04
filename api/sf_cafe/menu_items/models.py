from django.db import models
from externals.s3_bucket.storage import CustomS3Boto3Storage

class MenuItem(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    photo_path = models.CharField(max_length=100, blank=True, null=True)
    ingredients = models.TextField()
    nutritional_information = models.TextField()

    def save_price(self, price_float):
        if price_float:
            self.price = int(price_float * 100)

    def get_price_float(self):
        if self.price:
            return float(self.price) / 100

    def get_photo_path_download_url(self):
        if not self.photo_path:
            return ''
        
        storage = CustomS3Boto3Storage()
        url = storage.get_download_url(self.photo_path)
        return url
        
    def upload_photo_to_s3(self, photo_file):
        storage = CustomS3Boto3Storage()
        split_filename = photo_file.name.split(".")
        extension = split_filename[-1]
        file_name = storage.generate_random_filename_string(extension)
        key = f'menu-items/{file_name}'
        storage.upload_fileobj(photo_file, key)

        return key
    
    def save(self, *args, **kwargs):
        if self.price is not None:
            self.save_price(self.price)
        
        if hasattr(self, 'new_photo'):
            path = self.upload_photo_to_s3(self.new_photo)
            del self.new_photo
            self.photo_path = path

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.photo_path:
            storage = CustomS3Boto3Storage()
            storage.delete_object(self.photo_path)
        super().delete(*args, **kwargs)

    
    def __str__(self):
        return self.name
