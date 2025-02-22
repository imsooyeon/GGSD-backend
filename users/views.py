import json, jwt, requests, enum

from tkinter import image_types
from commons.models import Image

from django.http  import JsonResponse
from django.db    import transaction
from django.conf  import settings
from django.views import View

from users.models   import User
from commons.models import Image

class ImageType(enum.Enum):
    BANNER            = 1
    PROJECT_THUMBNAIL = 2
    PROJECT_DETAIL    = 3
    STACK             = 4
    USER_PROFILE      = 5

class KakaoLoginView(View):        
    def get(self, request):        
        try:
            kakao_token   = request.headers.get('Authorization', None)
            requests_url  = "https://kapi.kakao.com/v2/user/me"
            user_account  = requests.get(requests_url, headers = {'Authorization': f'Bearer {kakao_token}'}).json()
            
            kakao_id  = user_account['id']
            email     = user_account['kakao_account']['email']
            name      = user_account['kakao_account']['profile']['nickname']
            image_url = user_account['kakao_account']['profile']['profile_image_url']
            
            if User.objects.filter(email = email):
                user         = User.objects.get(email = email)
                access_token = jwt.encode({"id" : user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
                
                return JsonResponse({'message' : 'SUCCESS', 'access_token' : access_token}, status=200)
            
            with transaction.atomic():
                
                new_user = User.objects.create(
                    kakao_id = kakao_id,
                    email    = email,
                    name     = name
                )
                new_user_image = Image.objects.create(
                    user_id       = new_user.id,
                    image_url     = image_url,
                    image_type_id = ImageType.USER_PROFILE.value
                )
            
            access_token = jwt.encode({"id" : new_user.id}, settings.SECRET_KEY, algorithm = settings.ALGORITHM)
            
            result = {
                'kakao_id'     : new_user.kakao_id,
                'name'         : new_user.name,
                'profile_url'  : new_user_image.image_url,
                'access_token' : access_token,
                "batch"        : new_user.batch
            }
            
            return JsonResponse({'message' : 'SUCCESS',
                                 'result'  : result
                                }, status=200)
            
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status = 400)