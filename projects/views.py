import json

from enum import Enum

from django.http     import JsonResponse
from django.views    import View
from django.db       import transaction

from projects.models import Project, ProjectStack
from applies.models  import ProjectApply, ProjectApplyStack
from commons.models  import Image
from users.models    import User
from core.utils      import login_required


class ApplyStatusType(Enum):
    applicant = 1
    creator   = 2


class ProgressStatus(Enum):
    before_start = 1
    in_progress  = 2
    done         = 3


class ImageType(Enum):
    banner           = 1
    project_thumbnail= 2
    project_detail   = 3
    stack            = 4
    user_profile     = 5


class ProjectEnrollmentView(View):
    @login_required
    def post(self, request):
        user_id = request.user.id

        data    = json.loads(request.body)

        title                     = data["title"]
        start_recruit             = data["start_recruit"]
        end_recruit               = data["end_recruit"]
        start_project             = data["start_project"]
        end_project               = data["end_project"]
        description               = data["description"]
        front_vacancy             = data["front_vacancy"]
        back_vacancy              = data["back_vacancy"]
        is_online                 = data.get("is_online", 0)
        progress_status_id        = data.get("progress_status_id", ProgressStatus.before_start.value)
        project_category_id       = data["project_category_id"]
        region_id                 = data["region_id"]
        project_stacks_ids        = data["project_stacks_ids"]
        project_apply_position_id = data["project_apply_position_id"]
        apply_stacks_ids          = data["apply_stacks_ids"]
        image_url                 = data["image_url"]
        is_private                = data["is_private"]

        with transaction.atomic():
            new_project = Project.objects.create(
                title                =title,
                start_recruit        =start_recruit,
                end_recruit          =end_recruit,
                start_project        =start_project,
                end_project          =end_project,
                description          =description,
                front_vacancy        =front_vacancy,
                back_vacancy         =back_vacancy,
                is_online            =is_online,
                project_category_id  =project_category_id,
                region_id            =region_id,
                progress_status_id   =progress_status_id,
            )

            [ProjectStack.objects.create(
                project_id         =new_project.id,
                technology_stack_id=project_stack_id
            ) for project_stack_id in project_stacks_ids]

            new_project_apply = ProjectApply.objects.create(
                project_id             =new_project.id,
                position_id            =project_apply_position_id,
                project_apply_status_id=ApplyStatusType.creator.value,
                user_id                =user_id
            )

            [ProjectApplyStack.objects.create(
                project_apply_id   =new_project_apply.id,
                technology_stack_id=apply_stack_id
            ) for apply_stack_id in apply_stacks_ids]

            creator_portfolio            = User.objects.get(id=user_id).portfolio
            creator_portfolio.is_private = is_private
            creator_portfolio.save()

            Image.objects.create(
                project_id   =new_project.id,
                image_url    = image_url,
                image_type_id=ImageType.project_thumbnail.value
            )
            results=[{
                "project" :{
                    "id": new_project.id
                }
            }]
        return JsonResponse({"MESSAGE": "PROJECT_CREATED", "results":results}, status=201)

    @login_required
    def get(self, request):
        user_id=request.user.id
        creator_portfolio = User.objects.get(id=user_id).portfolio

        results=[{
            "is_private": creator_portfolio.is_private
        }]
        return JsonResponse({"results": results}, status=200)

