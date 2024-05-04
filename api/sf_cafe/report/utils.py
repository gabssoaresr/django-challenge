import shutil
import os
import tempfile
from externals.s3_bucket.storage import CustomS3Boto3Storage
from pyreportjasper import PyReportJasper
from platform import python_version


class Utils:
    def __init__(self) -> None:
        self.s3_connector = CustomS3Boto3Storage()

    def generate_report(self):
        input_file_path = "/usr/src/app/api/sf_cafe/report/jrxml/report.jrxml"

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            output_file = temp_file.name

        jasper = PyReportJasper()
        data_source = {
            'driver': 'postgres',
            'username': os.getenv('POSTGRES_USER'),
            'password': os.getenv('POSTGRES_PASSWORD'),
            'host': os.getenv('POSTGRES_HOST'),
            'database': os.getenv('POSTGRES_DB'),
            'port': os.getenv('POSTGRES_PORT'),
            'jdbc_driver': 'org.postgresql.Driver',
        }

        jasper.config(
            input_file_path,
            output_file,
            output_formats=["pdf",],
            parameters={'python_version': python_version()},
            db_connection=data_source,
            locale='pt_BR'
        )

        jasper.process_report()

        return output_file
    
    def upload_report_file_to_s3(self, file_path: str):
        file_name = os.path.basename(file_path)

        self.s3_connector.upload_file(file_path, file_name)
        os.unlink(file_path)

        return self.s3_connector.get_download_url(file_name)
