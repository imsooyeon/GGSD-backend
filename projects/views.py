import datetime

from enum import Enum

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Prefetch

from projects.models  import Project, ProjectStack
from commons.models   import Image
from core.utils       import login_required


class ImageType(Enum):
    BANNER            = 1
    PROJECT_THUMBNAIL = 2
    PROJECT_DETAIL    = 3
    STACK             = 4
    USER_PROFILE      = 5


class ProjectsListView(View):
    @login_required
    def get(self, request):
        user_id         = request.user.id

        order_condition = request.GET.get("sort", "default_sort")
        search          = request.GET.get("search", None)
        region_id       = request.GET.get("region_id", None)
        apply_status_id = request.GET.get("apply_status_id", None)
        start_recruit   = request.GET.get("start_recruit", None)
        end_recruit     = request.GET.get("end_recruit", None)
        stack_ids_q     = request.GET.getlist("stack_ids", None)
        category_ids_q  = request.GET.getlist("category_ids", None)
        offset          = int(request.GET.get("offset", 0))
        limit           = int(request.GET.get("limit", 10))

        q = Q()

        page_title = None

        if search:
            q &= Q(title__icontains=search) \
                 | Q(description__icontains=search) \
                 | Q(region__district_name__icontains=search) \
                 | Q(projectstack__technology_stack__title__icontains=search)
            page_title = f"{search}\"에 대한 검색결과"

        if region_id:
            q &= Q(region_id=region_id)

        if stack_ids_q:
            q &= Q(projectstack__technology_stack_id__in=stack_ids_q)

        if category_ids_q:
            q &= Q(project_categories_id__in=category_ids_q)

        if apply_status_id:
            q &= Q(projectapply__project_apply_status_id=apply_status_id) \
                 & Q(projectapply__user_id=user_id)

        if start_recruit:
            q &= Q(start_recruit__lte=start_recruit)

        if end_recruit:
            q &= Q(end_recruit__gte=end_recruit)

        if order_condition == "deadline":
            q &= Q(end_recruit__lte=datetime.datetime.now() + datetime.timedelta(days=3)) \
                 & Q(end_recruit__gte=datetime.datetime.now())

        if order_condition == "recent_created":
            q &= Q(created_at__lte=datetime.datetime.now()) \
                 & Q(created_at__gte=datetime.datetime.now() - datetime.timedelta(days=3))

        order = {
            "default_sort"  : "-created_at",
            "recent_created": "-created_at",
            "deadline"      : "-end_recruit"
        }

        projects = Project.objects \
               .select_related("project_category") \
               .prefetch_related(
                    Prefetch("image_set", queryset=Image.objects.filter(image_type=ImageType.PROJECT_THUMBNAIL.value),
                             to_attr="thumbnails"),
                    Prefetch("projectstack_set", queryset=ProjectStack.objects.select_related("technology_stack"),
                             to_attr="project_stacks")) \
               .filter(q) \
               .order_by(order[order_condition]) \
               [offset:offset + limit]

        results = []

        for project in projects:
            thumbnail        = [thumbnail.image_url for thumbnail in project.thumbnails]
            project_stack_qs = [project_stack for project_stack in project.project_stacks]

            project_stacks = [{
                "id"   : project_stack.technology_stack.id,
                "title": project_stack.technology_stack.title,
                "color": project_stack.technology_stack.color
            } for project_stack in project_stack_qs]

            results.append({
                "today"      : datetime.date.today(),
                "end_recruit": project.end_recruit,
                "created_at" : project.created_at,
                "sort"       : order,
                "page_title" : page_title,
                "project_id" : project.id,
                "category"   : project.project_category.title,
                "title"      : project.title,
                "thumbnail"  : thumbnail,
                "stacks"     : project_stacks
            })
        return JsonResponse({"results": results}, status=200)