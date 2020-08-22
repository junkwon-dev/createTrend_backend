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

## API



## 사용된 도구

* [Django](https://www.djangoproject.com/) - 웹 프레임워크(앱 서버)
* [Django rest framework](https://www.django-rest-framework.org/) - 웹 REST 프레임워크
* [Docker](https://www.docker.com/) - 의존성 관리 프로그램
* [Nginx](https://www.nginx.com/) - 웹 서버
* [Gunicorn](https://gunicorn.org/) - 웹, 앱서버 통신 인터페이스



## 라이센스

 [the 3-clause BSD license 1](https://github.com/django/django/blob/master/the 3-clause BSD license 1)