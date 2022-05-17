from enum import Enum

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Prefetch

from projects.models  import Project, ProjectStack
from applies.models   import ProjectApply
from commons.models   import Image

from core.utils       import login_required


class ApplyStatusType(Enum):
    applicant = 1
    creator   = 2


class PositionRoll(Enum):
    back_end = 1
    front_end = 2


class ImageType(Enum):
    banner=1
    project_thumbnail=2
    project_detail=3
    stack=4
    user_profile =5


class RequestType(Enum):
    request = 1
    deny = 2
    confirm = 3


class ProjectDetailView(View):
    def get(self, request, project_id):
        project = Project.objects \
            .select_related("region", "project_category") \
            .prefetch_related(
            Prefetch("projectstack_set",
                     queryset=ProjectStack.objects.select_related("technology_stack"),
                     to_attr="project_stacks"),
            Prefetch("projectapply_set",
                     queryset=ProjectApply.objects.select_related("user", "user__portfolio").filter(
                         project_apply_status=ApplyStatusType.creator.value),
                     to_attr="creators_apply"),
            Prefetch("projectapply_set",
                     queryset=ProjectApply.objects.select_related("user").filter(
                         project_apply_status=ApplyStatusType.applicant.value),
                     to_attr="applicants_apply"),
            Prefetch("image_set",
                     queryset=Image.objects.filter(image_type=ImageType.project_thumbnail.value),
                     to_attr="thumbnails")) \
            .get(id=project_id)

        creators_apply = ProjectApply.objects \
            .select_related("project_apply_status").filter(project_id=project.id,
                                                           project_apply_status=ApplyStatusType.creator.value)

        applicants_apply_ = ProjectApply.objects \
            .select_related("project_apply_status").filter(project_id=project.id,
                                                           project_apply_status=ApplyStatusType.applicant.value)

        back_fixed  = 0
        front_fixed = 0

        for creator_apply in creators_apply:
            if creator_apply.position_id == PositionRoll.back_end.value:
                back_fixed += 1
            if creator_apply.position_id == PositionRoll.front_end.value:
                front_fixed += 1

        for applicant_apply in applicants_apply_:
            if applicant_apply.project_apply_status.requeststatus_set.get(
                    id=RequestType.confirm.value) and applicant_apply.position_id == PositionRoll.back_end.value:
                back_fixed += 1
            if applicant_apply.project_apply_status.requeststatus_set.get(
                    id=RequestType.confirm.value) and applicant_apply.position_id == PositionRoll.front_end.value:
                front_fixed += 1

        thumbnail = [thumbnail.image_url for thumbnail in project.thumbnails]

        results = [
            {
                "project": {
                    "title"         : project.title,
                    "front_vacancy" : project.front_vacancy,
                    "back_vacancy"  : project.back_vacancy,
                    "front_fixed"   : front_fixed,
                    "back_fixed"    : back_fixed,
                    "start_recruit" : project.start_recruit,
                    "end_recruit"   : project.end_recruit,
                    "start_project" : project.start_project,
                    "end_project"   : project.end_project,
                    "region"        : project.region.district_name if project.region else None,
                    "is_online"     : project.is_online,
                    "description"   : project.description,
                    "thumbnail"     : thumbnail,
                    "category"      : project.project_category.title,
                    "project_stacks": [{
                        "stack_id": project_stack.technology_stack.id,
                        "title"   : project_stack.technology_stack.title,
                        "color"   : project_stack.technology_stack.color
                    } for project_stack in project.project_stacks],
                    "creators": [{
                        "id"        : creator_apply.user.id,
                        "name"      : creator_apply.user.name,
                        "position"  : creator_apply.position.roll,
                        "github_url": creator_apply.user.github_repo_url,
                        "portfolio" : [{
                            "file_url"  : None if creator_apply.user.portfolio.is_private else creator_apply.user.portfolio.file_url,
                            "is_private": creator_apply.user.portfolio.is_private
                        }]
                    } for creator_apply in project.creators_apply],
                    "applicants": [{
                        "id"            : applicant_apply.user.id,
                        "name"          : applicant_apply.user.name,
                        "position"      : applicant_apply.position.roll,
                        "apply_status"  : applicant_apply.project_apply_status.type,
                        "request_status": applicant_apply.project_apply_status.type,
                        "github_url"    : applicant_apply.user.github_repo_url
                    } for applicant_apply in project.applicants_apply]
                }
            }
        ]
        return JsonResponse({"results": results}, status=200)
