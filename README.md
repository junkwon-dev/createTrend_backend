# CreateTrend backend

Create Trend 서비스의 정보를 제공해주는 API입니다.



### 시작하기에 앞서

Django REST framework로 제작한 CreateTrend서비스의 API로 PostgreSQL Database와 연동되어있습니다. 

이 프로그램을 사용하려면 자신의 IP가 CreateTrend 서버의 PostgreSQL 포트 인바운드 규칙에 추가되어야 합니다. 



## 시작하기

### 설치하기

1. Docker 설치
2. Docker-compose 설치

```bash
$ sudo apt update
$ sudo apt install apt-transport-https ca-certificates curl software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
$ sudo apt update
$ apt-cache policy docker-ce
$ sudo apt install docker-ce
```

```bash
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```



Docker로 구성된 서버에 Dockerfile,Docker-compose로 모든것을 정리해놓았습니다. 바로 실행할 수 있습니다.




## 배포

1. cd ./muna-4/createtrend/
2. sudo docker-compose up -d --build django

![result](https://user-images.githubusercontent.com/48988862/90956224-76214600-e4bf-11ea-88c9-9d7784bb8117.png)

## EXAMPLE

### 회원 API

![image-20201111134649774](https://user-images.githubusercontent.com/48988862/98775638-e1c8de80-2430-11eb-82b9-dfd43395f4ae.png)

![image-20201111134707760](https://user-images.githubusercontent.com/48988862/98775718-045af780-2431-11eb-8a42-cd5a75ebb6f7.png)

![image-20201111134723843](https://user-images.githubusercontent.com/48988862/98775748-1341aa00-2431-11eb-9d0f-6f3484727271.png)

### 전체 채널 API

![image-20201111134755646](https://user-images.githubusercontent.com/48988862/98775760-1ccb1200-2431-11eb-9821-3c483872baaf.png)

![image-20201111134804086](https://user-images.githubusercontent.com/48988862/98775783-23f22000-2431-11eb-868b-482faf40c763.png)

### 키워드 검색 API

![image-20201111134813497](https://user-images.githubusercontent.com/48988862/98775806-2d7b8800-2431-11eb-88bb-436d4682a523.png)

### 채널 정보/기간 내 정보 API

![image-20201111134836748](https://user-images.githubusercontent.com/48988862/98775825-35d3c300-2431-11eb-979f-8c6464bbc3cf.png)

![image-20201111134854006](https://user-images.githubusercontent.com/48988862/98775839-3d936780-2431-11eb-9876-6416ed9bbfd5.png)

![image-20201111134901897](https://user-images.githubusercontent.com/48988862/98775851-44ba7580-2431-11eb-940b-dcb06582edf3.png)

### 비디오 상세정보 API

![image-20201111134935149](https://user-images.githubusercontent.com/48988862/98775873-4dab4700-2431-11eb-85cd-728b7022d103.png)

### 조회수 예측 API

![image-20201111135025263](https://user-images.githubusercontent.com/48988862/98775890-54d25500-2431-11eb-903a-f694379009f6.png)

![image-20201111135035036](https://user-images.githubusercontent.com/48988862/98775910-5b60cc80-2431-11eb-8e23-8887f9610e98.png)

![image-20201111135043301](https://user-images.githubusercontent.com/48988862/98775925-61ef4400-2431-11eb-9e66-b7d94927b5ad.png)

## How it Works

### Common

- Model - 각 장고 프로세스가 PostgreSQL에서 데이터를 가져올 때 참조하는 모듈입니다. 
- Serializer - 객체를 직렬화(JSON)할때 참조하는 모듈입니다. 
- functions - views.py에서 사용하는 함수를 관리해주는 모듈입니다.
- urls - URI를 관리해주는 모듈입니다.
- Django rest framework - Django를 rest api framework로 활용할 수 있게 해주는 라이브러리입니다.
- ELASTICSEARCH_DSL - 각 Django process가 Elasticsearch와 연결되어 Django에서 Elasticsearch 데이터를 객체화하여 사용할 수 있게 해줍니다.

### accounts

- 회원가입, 로그인, 로그아웃, 회원정보 업데이트를 담당하는 Application입니다.

- knox(django third-party auth app) - 토큰 위주의 Authorization library입니다.
- 회원가입, 로그인 시 토큰이 발행됩니다.
- 해당 토큰을 가지고 인증 요청할 시 유저가 인증됩니다.
- 발행한 토큰의 유효기간은 하루입니다.

### Analyze_Channel

- 인기, 영상화 TOP10 키워드, 키워드에 대한 상세 정보, 추천 영상을 제공해주는 Application입니다.

- 인기, 영상화 TOP10을 Elasticsearch에 질의 후 가공하여 제공합니다. (collection 모듈을 사용하여 최빈 10개의 키워드 추출)
- 해당 키워드들의 상세 정보를 Elasticsearch에 질의 후 가공하여 제공합니다.

### Search_Keyword

- 키워드 검색 시 해당 키워드의 상세 정보를 제공해주는 Application입니다.
- 워드맵, 해당 키워드의 인기,영상화 추이, 관련 키워드 TOP10 등을  Elasticsearch에 질의 후 가공하여 제공합니다.

### Search_StarYoutuber

- 채널검색, 채널 상세 정보, 기간별 상세정보를 제공해주는 Application입니다.
- 해당 어플리케이션의 시나리오는 검색 -> 상세정보 -> 기간별 상세정보 입니다.
- 채널에 대한 각종 정보를 PostgreSQL에 질의 후 제공합니다.

### Video_Detail

- 영상에 대한 상세 정보를 제공해주는 Application입니다.
- 해당되는 영상의 정보를 PostgreSQL에 질의 후 가공하여 제공합니다.

### Views_Predict

- 영상에 대한 조회수를 예측하는 Application입니다.

- 해당 어플리케이션의 시나리오는 원하는 컨텐츠 검색 -> 추천되는 썸네일과 제목 체크하기 -> 구독자수 입력하기 -> 예측해보기입니다.

- 해당되는 영상의 정보와 채널의 정보를 Elasticsearch에 먼저 질의하고, 해당 정보를 이용하여 PostgreSQL에 다시 질의합니다.

- AI Server와 통신할 때 RabbitMQ 대용량 메시지 큐를 활용합니다.

- 데이터의 흐름은 다음과 같습니다. 

  >  __데이터 요청 -> 큐 생성 -> 메시지 업로드 -> AI server에서 Listen하다가 메시지 받음 -> 처리 후 메시지 업로드 -> Django에서 데이터 받음 -> Response 제공__ 

## Create Trend Server Architecture

### 전체 구성

![image](https://user-images.githubusercontent.com/48988862/98776375-2739db80-2432-11eb-9d43-89d166679015.png)

### Docker를 활용한 서버 설계

![image](https://user-images.githubusercontent.com/48988862/98776549-7b44c000-2432-11eb-87c3-14982c01909b.png)

>  장고, 엘라스틱서치 등 중요 기능을 담당하는 부분은 삼중화를 통해 서버의 안정성을 확보하였고, 후에 Scale out에 용이하게 설계하였습니다.

### CreateTrend Docker 네트워크 환경

![image](https://user-images.githubusercontent.com/48988862/98776613-a0d1c980-2432-11eb-9b61-0b29d135e834.png)

> CreateTrend 서버의 네트워크 환경입니다. 

## Built With

* [Django](https://www.djangoproject.com/) - 웹 프레임워크(앱 서버)
* [Django rest framework](https://www.django-rest-framework.org/) - 웹 REST 프레임워크
* [Docker](https://www.docker.com/) - 의존성 관리 프로그램
* [Nginx](https://www.nginx.com/) - 웹 서버
* [Gunicorn](https://gunicorn.org/) - 웹, 앱서버 통신 인터페이스
* [django-elasticsearch-dsl](https://django-elasticsearch-dsl.readthedocs.io/en/latest/index.html) - 장고-엘라스틱서치간 모델 관리 및 사용 라이브러리  
* [knox](https://github.com/James1345/django-rest-knox) -토큰 기반 회원 인증 시스템 라이브러리


## Author
__권준 (dydqja1013@naver.com)__

## 라이센스

[the 3-clause BSD license 1](https://opensource.org/licenses/BSD-3-Clause) - Django, Nginx

[MIT License](https://github.com/James1345/django-rest-knox/blob/develop/LICENSE) - knox

[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0) - elasticsearch-dsl, Docker







