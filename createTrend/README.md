# 프로젝트 제목

한 문단 정도의 프로젝트 설명입니다.

Create Trend서비스의 정보를 제공해주는 API입니다.



### 시작하기에 앞서

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



## 시작하기

이 지침을 따르시면 로컬 컴퓨터에서 개발과 테스트를 위한 프로젝트 사본을 실행시킬 수 있습니다. 배포하기 항목을 확인하여 실제 시스템에 프로젝트를 배포하는 방법을 알아보세요.

1. cd ./muna-4/createtrend/
2. sudo docker-compose up -d --build django



### 설치하기

Django

## 테스트 실행하기

이 시스템을 위한 자동화된 테스트를 실행하는 방법을 적어주세요.

### End-to-End 테스트

이 단위 테스트가 테스트하는 항목을 설명하고 테스트를 하는 이유를 적어주세요.

```
예시도 재공하세요
```

### 코딩 스타일 테스트

이 단위 테스트가 테스트하는 항목을 설명하고 테스트를 하는 이유를 적어주세요.

```
예시도 재공하세요
```


## 배포

추가로 실제 시스템에 배포하는 방법을 노트해 두세요.

## 사용된 도구

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - 웹 프레임워크
* [Maven](https://maven.apache.org/) - 의존성 관리 프로그램
* [ROME](https://rometools.github.io/rome/) - RSS 피드 생성기.

## 버전 관리

[SemVer](http://semver.org/) (을)를 사용하여 버전을 관리합니다. 자세한 방법은 레포지토리의 [테그(tags)](https://github.com/your/project/tags)를 확인해 주십시오.

## 저자

* **Billie Thompson** - *초기작* - [PurpleBooth](https://github.com/PurpleBooth)
* **Taeuk Kang** - *한국어 번역* - [GitHub](https://github.com/taeukme) / [Keybase](https://keybase.io/taeuk)


[기여자 목록](https://github.com/your/project/contributors)을 확인하여 이 프로젝트에 참가하신 분들을 보실 수 있습니다.

## 라이센스

이 프로젝트는 MIT 허가서를 사용합니다 - [LICENSE.md](LICENSE.md) 파일에서 자세히 알아보세요.

## 감사 인사

* 본인의 코드가 사용된 분께 경의를 표합니다
* 영감
* 기타 등등...

---

위 템플렛의 영문 원본은 [여기](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)에서 확인하실 수 있습니다.
오타는 Comment (댓글) 로 남겨주시면 수정해드리겠습니다.