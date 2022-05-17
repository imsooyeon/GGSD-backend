from django.http     import JsonResponse
from django.views    import View
from django.conf     import settings

from applies.models  import ProjectApplyStatus
from commons.models  import ImageType, TechnologyStack, Region, Position
from projects.models import ProjectCategory,ProgressStatus
from applies.models  import RequestStatus
from core.storage    import MyS3Client


class FileView(View):
    def post(self, request):
        file         = request.FILES['project_thumbnail']
        s3_client    = MyS3Client(settings.AWS_S3_ACCESS_KEY_ID, settings.AWS_S3_SECRET_ACCESS_KEY, settings.AWS_STORAGE_BUCKET_NAME)
        uploaded_url = s3_client.upload(file)
        return JsonResponse({"MESSAGE": "FILE_UPLOADED", "UPLOADED_URL":uploaded_url}, status=201)


class MetaDataView(View):
    def get(self, request):
        stacks            = TechnologyStack.objects.all()
        categories        = ProjectCategory.objects.all()
        regions           = Region.objects.all()
        positions         = Position.objects.all()
        apply_statuses    = ProjectApplyStatus.objects.all()
        image_types       = ImageType.objects.all()
        progress_statuses = ProgressStatus.objects.all()
        request_statuses  = RequestStatus.objects.all()

        results = [{
            "stacks": [{
                "id"   : stack.id,
                "title": stack.title
            } for stack in stacks],
            "categories": [{
                "id"   : category.id,
                "title": category.title
            } for category in categories],
            "regions" : [{
                "id"  : region.id,
                "district_name": region.district_name
            } for region in regions],
            "positions" : [{
                "id"  : position.id,
                "roll": position.roll
            } for position in positions],
            "apply_statuses": [{
                "id"  : apply_status.id,
                "type": apply_status.type
            } for apply_status in apply_statuses],
            "image_types": [{
                "id"   : image_type.id,
                "title": image_type.title
            } for image_type in image_types],
            "progress_statuses": [{
                "id"  : progress_status.id,
                "step": progress_status.step
            }for progress_status in progress_statuses],
            "request_statuses": [{
                "id"  : request_status.id,
                "type": request_status.type
            }for request_status in request_statuses]
        }]
        return JsonResponse({"results": results}, status=200)