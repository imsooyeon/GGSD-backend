# 개고수덜 (GGSD) 
개고수덜 ("개발자들의 고민과 수고를 덜어주는" 사이트)

## 프로젝트 개요

- 개발자들끼리의 프로젝트 매칭 사이트를 기획했습니다 <개발자들의 고민과 수고를 덜어주기 위하여!>
- 기존의 비지니스 로직을 모방하는, 사이트 클로닝 프로젝트가 아닙니다
- 기획부터 개발까지, 팀원들과 스크럼 방식의 소통으로 프로젝트를 진행했습니다
- 2주에 구현 가능한 기능들로만 간추려 진행했습니다

## 프로젝트 참여 기간 및 인원

2022.05.09 ~ 2022.05.20 (12일)

[프론트엔드](https://github.com/wecode-bootcamp-korea/32-2nd-GGSD-frontend)
- 정덕우
- 최승이
- 이하영
- 이희준

[백엔드](https://github.com/wecode-bootcamp-korea/32-2nd-GGSD-backend)
- [지기성](https://github.com/jiggyjiggy)
- [임수연](https://github.com/imsooyeon)

---

## 기술 스택
<img alt="Python" src="https://user-images.githubusercontent.com/78680486/158049036-4c7371ab-443d-4db9-baa0-6877a4528034.svg"> <img alt="Django" src="https://user-images.githubusercontent.com/78680486/158049032-6368747a-c353-491c-8d22-63cdc1c525b1.svg"> <img alt="MySQL" src="https://user-images.githubusercontent.com/78680486/158049035-1b7122ad-cc99-477c-8d94-98ce48944d92.svg"> <img alt="Git" src="https://user-images.githubusercontent.com/78680486/158049033-6a7836e9-da4a-4333-8f80-ea7972b2f922.svg"> <img alt="AWS" src="https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon%20aws&logoColor=black">

## 협업 툴
<img alt="Github" src="https://user-images.githubusercontent.com/78680486/158049034-cc1a893a-bc48-463f-811d-72e57853121d.svg"> <img alt="Trello" src="https://user-images.githubusercontent.com/78680486/158049038-9c0dd825-e9c8-4e9d-aa60-f66deb56178d.svg"> <img alt="Slack" src="https://user-images.githubusercontent.com/78680486/158049039-55093258-f377-468f-bcf0-d4e7474b7e84.svg">

---

# 기획과 구현

## 특기 할만한 기획

- meta data view
  ```
  - front 와 back의 소통에 있어서 인간 의존성을 줄이고자 meta data view를 시도해봤습니다 
  - 돌이켜보면 해당 view가 meta data라는 이름을 갖는 것에 대해서는 틀리다는 생각이 들지만, 해당 시도는 옳았다고 생각합니다
  ```
  <img width="1246" alt="meta data view" src="https://user-images.githubusercontent.com/89971435/169652820-5c771cf7-dc0f-47d5-94a7-07211917fba8.png">


### ERD 

- GGSD ERD (essential_version)
  ```
  - 2주 안에 구현 가능 할 기능에 대해서만 축소한 ERD 입니다
  - 최대한 정규화를 해봤습니다
  - Many to Many 관계가 많았습니다
  - 필터링 시, 자주 사용될 관계에 대해 미리 예측해보고 model class들을 구성했습니다
  ```
  ![GGDS_essential](https://user-images.githubusercontent.com/48621061/169649714-24baf931-d6e9-4fff-9a7d-d3001fdcb56f.png)

---

## 특기 할만한 구현 기능

1. 카카오 소셜 로그인
2. 무한 스크롤 및 페이지네이션
3. 필터링
    - 3-1. 스택 필터링
    - 3-2. 기간 필터링
4. ORM 최적화
5. transaction 적용
6. S3를 이용한 이미지 업로드
7. EC2, RDS를 이용한 배포

- 카카오 소셜 로그인 
  ```
  - 카카오 공식 자료를 통해 소셜 로그인을 구현하였습니다
  - 공유에 대한 개발자의 문화에 깊이 공감할 수 있던 순간이였습니다.
  - REST 를 왜 쓰는지에 대한, 개발에 있어서 Semantic web을 위한 규칙의 정립의 중요성을 느낄 수 있던 순간이였습니다.
  ```
  
- 무한 스크롤 및 페이지네이션
  ```
  - 일부로 쿼리파라미터로 구현했다는 점에서 특기 할만 하다 할 수 있을 것 같습니다
  - HTTP 의 Range 헤더를 활용한다면 프론트에서 깔끔한 요청이 가능합니다, 또한 미리 정의된 header를 사용하는 것이 의미론적 사용법을 통일 할 수 있다는 장점이 있을 수 있습니다
  - 하지만 본 프로젝트에서 추후 북마크를 지원 할 계획도 갖고 있었기에 쿼리 파라미터로써 구현했습니다 (Range 헤더를 활용한 페이지네이션은 북마크를 할 수 없다)
  ```
  
- 필터링 

  ```
  - 아래의 두 필터링을 구현하면서 공식문서의 중요성을 더욱 깨우쳤습니다
  - 구체적으로 말하자면, 해당 기능을 제공하는지에 대한 확실한 숙지가 선행되어야 유연한 구현이 가능하다는 것을 깨우쳤습니다.
  - 스택 필터링에서는 제공하지 않는 기능으로 해결하려해서, 기간 필터링에서는 제공하는 기능으로 해결하려하지 않아서 꽤나 bloker로써 작용했습니다
  ```

  - 스택 필터링 
    ```
    - 다중 선택에 있어서, 선택 조건을 반드시 포함하는 필터링을 구현하였습니다
    - django의 field lookup 에서 __in 은 조건 중 하나만이라도 존재한다면 필터링을 하였기에 
    - django_mysql (library) 로 DB를 가공하고, annotate로 묶은 다음 python으로 입력값을 가공한뒤 __contains로 구현할 수 있었습니다
    ```
    ![django_mysql lib](https://user-images.githubusercontent.com/89971435/169655092-dbd5d7c3-ca6c-4818-9736-a7bd7447786c.png)

    <img width="543" alt="Q join" src="https://user-images.githubusercontent.com/89971435/169653332-350c18ea-505e-4920-ade6-938cc1ad6870.png">
    <img width="743" alt="annotate" src="https://user-images.githubusercontent.com/89971435/169653333-5c8863d8-9707-415f-887e-1c70c373303b.png">
  
  - 기간 필터링
    ```
    - 지금 보면 굉장히 쉬운 문제를 어렵게 해결하려 했던 부분입니다
    - F객체를 활용해 DB에서 호출시 가공해서 처리하려 시도했습니다
    - 하지만 비교의 자료형이 달랐고, 비교가 쉽지 않아서 꽤 고생했습니다
    - 하지만 django의 field lookup을 활용하면 매우 간단히 해결 할 수 있었습니다
    ```
    ![기간 필터링 ](https://user-images.githubusercontent.com/89971435/169656867-715e1d2c-1948-4fc1-be54-adfab344d58e.png)
  
- ORM 최적화 (select_related, profetch_related, Prefetch)
  ```
  - 본 프로젝트에선 Many to Many 관계가 특히나 많고, 해당 관계 속에서 필터링이 적용됩니다 (ex. 스택을 이용한 프로젝트 필터링) 
  - 따라서 백엔드 서버 자체에서 DB hit 관점에서의 최적화가 필요했고, ORM 최적화 했습니다
  - 추후 네트워크 관점에서 최적화를 시도하는것이 가장 시급한 목표입니다
  ```
  ![ORM 최적화](https://user-images.githubusercontent.com/89971435/169654779-438ced91-0494-4bcd-8336-d4d0a779d9a2.png)
  <img width="1036" alt="최적화 후 쿼리 수" src="https://user-images.githubusercontent.com/89971435/169654848-540666ad-b5ca-4c4e-a878-973d4e14e7fd.png">
  
- data 생성 시, transaction 적용
  ```
  - 이미지 업로드와 5개의 테이블이 엮여있는 관계에서 데이터를 생성하기에, 프로그램 run time 중 오류로 인해 데이터의 원자성이 깨질 상황에 대해 자연스럽게 생각해보게 됐습니다
  - 따라서 atomic 을 적용해봤습니다
  ```
  ![transaction](https://user-images.githubusercontent.com/89971435/169655305-69c10baa-3828-4577-89e0-e3b207553013.png)

- S3를 이용한 이미지 업로드
  ```
  - 과거 프로젝트 진행 시 로컬 환경의 이미지의 직접 업로드의 궁금증이 들었습니다
  - 따라서 본 프로젝트에선 로컬의 resource를 직접 활용해 보고자 했습니다
  ```
  <img width="700" alt="S3 사용 이유" src="https://user-images.githubusercontent.com/89971435/169653649-1ca7947a-8e45-4883-9413-dbe107ccce05.png">

  ```
  - 클래스화를 통해 객체 프로그래밍을 적용해 동작하도록 구현했습니다
  ```
  ![S3 업로드 클래스](https://user-images.githubusercontent.com/89971435/169653624-822799e0-93ad-47e0-898c-ae772e49b32a.png)

- EC2, RDS를 이용한 배포
  ```
  - EC2 를 사용하면서 지속적인 runserver 를 위해 gunicorn 사용했습니다
  ```
  <img width="1268" alt="gunicorn" src="https://user-images.githubusercontent.com/89971435/169652599-e0afad4b-4217-45d7-9ba9-f60daabcdda4.png">

---

### 주요 기능 시연 영상

1. 카카오 소셜 로그인 
2. 무한 스크롤
3. 필터링
    - 3-1. 스택 필터링
    - 3-2. 기간 필터링
4. S3를 이용한 이미지 업로드

- 카카오 소셜 로그인 

  https://user-images.githubusercontent.com/89971435/169651190-1c640235-459f-4f94-a70a-bf6787517553.mp4

- 무한 스크롤

  https://user-images.githubusercontent.com/89971435/169651442-cd3c936f-557d-45e0-8824-4e3d7299dd5e.mp4

- 필터링

  - 스택 필터링

    https://user-images.githubusercontent.com/89971435/169651559-761c4fbf-7366-4f86-8fbf-5cb3bae5f148.mp4

  - 기간 필터링

    https://user-images.githubusercontent.com/89971435/169656606-0f992180-f3c6-4b3c-9716-1e4f78ab60be.mp4


- S3를 이용한 이미지 업로드

  https://user-images.githubusercontent.com/89971435/169652441-c835bd6f-794b-4bb8-ba7c-2ff2385a79c6.mp4

  https://user-images.githubusercontent.com/89971435/169652443-f9254c07-77df-4f4f-a490-7a1b8b2c896d.mp4
  
