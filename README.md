# template-portfolio

사진 포트폴리오 사이트 템플릿. 정적 HTML, CSS, JS만 쓴다. 빌드 단계가 없다.

- 첫 화면: 커서를 움직이면 사진이 한 장씩 나타난다. 모바일은 터치할 때마다 한 장.
- Works / About 메뉴, 시리즈 페이지, 촬영(photoshoot) 페이지, 에디토리얼 크레딧 박스
- 전체화면 뷰어, 인덱스(그리드), 프로젝트 PDF 내려받기
- 이름, 사진, 문구는 모두 자리 표시다. 플레이스홀더 사진은 `tools/make-placeholders.py`가 만든다.

## 열어 보기

```
python3 -m http.server 8000
```

`http://localhost:8000`을 연다.

## 바꿀 곳

| 파일 | 바꾸는 것 |
| --- | --- |
| `index.html` | 메타 태그(`<head>` 전체), 이름, 직함, 연락처, Works 메뉴, About 문구, 크레딧 박스, `<body data-owner data-role>` |
| `image-titles.js` | 사진마다 제목과 태그. 태그가 같은 사진이 `?page=태그` 페이지에 모인다 |
| `script.js` 위쪽 | `SERIES_CONFIG`(시리즈와 장수), `LANDING_FRONT/REST`(첫 화면 사진), `DELTA_SELECTION`(선별 페이지), `PHOTOSHOOT_TITLES`(촬영 페이지) |
| `mobile.js` | 모바일 정보 블록. `index.html`의 `.d-info`와 같은 내용으로 맞춘다 |
| `series-video.js` | 영상이 있는 촬영 페이지만 `SERIES_VIDEOS`에 적는다. 없으면 비워 둔다 |
| `log.js` | `LOG_ENDPOINT`가 비어 있으면 다운로드 기록을 보내지 않는다 |
| `site.webmanifest`, 아이콘, `og.jpg` | 이름과 이미지 교체 |
| `download/` | `PortfolioCV.zip`(CV와 포트폴리오), `Portfolio_end.pdf`(프로젝트 PDF의 마지막 장, 630 x 480 pt) 교체 |

`index.html`의 Works 메뉴 `href`(`?page=...`)는 `script.js`와 `image-titles.js`의 키와 같아야 한다.

## 사진

- 파일 이름: `<시리즈>-NN.avif`. 시리즈 이름은 영문 소문자와 숫자만 쓴다. 하이픈은 쓰지 않는다.
- 크기가 두 벌 필요하다: `img/`(긴 변 2000px)와 `img/web/`(긴 변 1400px).
- 변환: `python3 tools/make-web-images.py <사진 폴더>`. 입력 파일은 `alpha-01.jpg`처럼 이름이 이미 맞아야 한다. Pillow 11.3 이상이 필요하다.
- 플레이스홀더는 `img/` 아래 파일을 지우고 새 파일로 바꾸면 된다. 장수가 달라지면 `script.js`의 `SERIES_CONFIG`와 `image-titles.js`를 같이 고친다.

## 저장소와 용량

- GitHub Pages는 게시된 사이트가 1GB 이하여야 한다. 레포는 1GB 이하를 권장하고, 파일 100MiB 초과는 push가 막힌다.
- 원본(RAW, TIFF, 영상)은 이 레포에 넣지 않는다. 웹용 AVIF만 넣는다.
- 출처: docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits, docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github

## 알아둘 것

- 다운로드(PDF, 포트폴리오 zip) 전에 이메일을 입력받는다(`email-gate.js`). 입력한 이메일은 방문자 브라우저에만 저장되고, `log.js`에 주소를 넣어야 따로 기록된다. 이메일을 받지 않으려면 `index.html`에서 `email-gate.js`와 `log.js` 줄을 지운다.
- 프로젝트 PDF는 방문자 브라우저에서 만들어진다. 표지 글꼴(`fonts/`)은 영문, 숫자, 문장부호만 들어 있는 서브셋이라 한글 이름은 표지에 나오지 않는다.
- 화면 레이아웃은 PC 중심이다. 모바일은 `mobile.js`가 별도 화면을 만든다.

## 글꼴

`fonts/`의 Pretendard 서브셋은 SIL OFL 1.1 라이선스다. 출처: npm `pretendard` 패키지(package.json의 license 필드).
