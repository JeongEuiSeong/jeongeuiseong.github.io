# jeongeuiseong.github.io

다람 가계부의 개발자 웹사이트. GitHub Pages 사용자 사이트로 올린다.

| 주소 | 파일 | 쓰는 곳 |
|---|---|---|
| `/` | `index.html` | App Store Connect **마케팅 URL** (AdMob이 이 도메인에서 app-ads.txt를 찾는다) |
| `/app-ads.txt` | `app-ads.txt` | AdMob 앱 인증 |
| `/daram/` | `daram/index.html` | 앱 소개 |
| `/daram/privacy/` | `daram/privacy/index.html` | **개인정보 처리방침 URL** (한국어) |
| `/daram/privacy/en/` | `daram/privacy/en/index.html` | 영어 개인정보 처리방침 |
| `/daram/support/` | `daram/support/index.html` | **지원 URL** |

## 올리기 전에 할 일

1. 출시 후 `daram/index.html`의 주석으로 둔 App Store 링크를 채운다.

## 올리는 법 (처음 한 번)

1. GitHub에서 **공개(Public)** 저장소를 `jeongeuiseong.github.io` 이름으로 만든다. 이름이 정확히 이것이어야 루트 주소로 올라간다.
2. 이 폴더에서:
   ```bash
   git add -A
   git commit -m "사이트 첫 게시"
   git remote add origin https://github.com/JeongEuiSeong/jeongeuiseong.github.io.git
   git push -u origin main
   ```
3. 저장소 Settings > Pages에서 Source가 `Deploy from a branch`, 브랜치 `main` / `/(root)`인지 확인한다.
4. 몇 분 뒤 `https://jeongeuiseong.github.io/app-ads.txt`가 열리는지 확인한다.

## 개인정보 처리방침 고치기

원본은 다람 저장소의 `docs/appstore/privacy-policy-ko.md`, `privacy-policy-en.md`다. 원본을 고친 뒤:

```bash
python3 scripts/build_privacy.py ../daram
```

`daram/privacy/` 아래 HTML은 이 스크립트가 만든다. 직접 고치지 않는다.

## 주의

- 공개 저장소다. 앱 소스, `sample/`(실제 금융 데이터), 스크린샷 원본 등은 넣지 않는다.
- `.nojekyll`이 있어 GitHub이 Jekyll로 변환하지 않고 파일을 그대로 올린다.
