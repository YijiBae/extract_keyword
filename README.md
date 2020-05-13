# extract_keyword
# Overview 

### Needs
우리나라 국내 최대 포털 사이트 네이버의 하루 평균 방문자수는 1,300만명, 1분에 약 9029명이 네이버에 방문한다.   
네이버 뉴스에 업데이트되는 뉴스 콘텐츠 수는 약 8000천여 건으로 많은 뉴스들이 나오게 된다.   
또한 많이 쏟아져나오는 뉴스 내용 중에서 가짜 뉴스들도 나오게 된다.    
그렇기에 콘텐츠 분석을 통해 정확한 키워드를 추출하는 것이 중요하다고 생각했다.
   
### Goals
특정 기간을 설정해 그 기간 동안의 핵심 키워드들을 보여주는 것이다.

------------

## TODO
- 네이버 뉴스 크롤링
  - 월별 크롤링
  - 일별 크롤링
  - 윤달 case 처리하기
- 크롤링 뉴스 전처리
  - 불필요한 데이터 제거하기 (링크, 뉴스사 등)
- 키워드 추출할 수 있는 기법 찾기
  - TF-IDF
  - 많이 언급된 단어 조사(ranking)
  
## Reference   
- 네이버기사 크롤링  
  - https://github.com/etilelab/webcrwling
  - http://blog.naver.com/luckperson7
  - http://yoonpunk.tistory.com/4  
- TF-IDF
  - http://blog.naver.com/vangarang/221072014624

