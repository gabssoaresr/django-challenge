from django.http import JsonResponse
from .utils import Utils 


class GenerateMonthlyReportView:
    @classmethod
    def generate_report(cls, request):
        utils = Utils()
        report_file_path = utils.generate_report()
        s3_url = utils.upload_report_file_to_s3(report_file_path)

        return JsonResponse({'download_url': s3_url})
