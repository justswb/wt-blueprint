# 레포 작업 규칙

## 브랜치·워크트리
- 기능 작업: 상위 feat 브랜치(예: `feat/feature`) 아래에 단계별 하위 브랜치
- 레포 공통 작업(CI 등): `main`에서 브랜치
- `.worktrees/`는 git 추적 안 함

## 위임
- 메인 세션은 계획, 위임, PR 감시만. 나머지(파일 수정, git·PR 작업, 리뷰 대응)는 전부 `.worktrees/` 워크트리에서 저렴한 하위 모델 subagent에 위임
- 위임 결과는 검토 안 함. CI와 PR 리뷰로 확인
- 위임 작업 내용은 대화에서 설명 안 함. PR 본문에 기록

## PR·stack
- 작업이 끝나면 PR 올리고, 리뷰 기다리지 않고 다음 작업 시작
- 의존 작업: `gh stack`으로 한 줄 stack. trunk는 상위 feat 브랜치(`gh stack init --base <feat 브랜치>`). 순서는 PR 본문에 안 적음
- 독립 작업: 상위 feat 브랜치에서 분기, feat 대상 일반 PR
- 의존이 갈라지면 하나만 stack에 넣고, 나머지는 앞 작업 merge 후 feat에서 시작
- 첫 하위 PR merge 후 feat → `main` PR을 draft로 생성(stack 밖). 마지막 하위 PR merge 후 ready
- 레포 공통 작업: stack 없이 `main` 대상 PR
- 브랜치 동기화는 merge. stack은 예외로 `gh stack sync`/`rebase` 사용(rebase, `--force-with-lease` push 허용). 그 외 rebase·강제 push는 사용자 허용 시에만

## 커밋
- author·committer 모두 실제 작업한 모델(예: `Claude Haiku 5.5 <noreply@anthropic.com>`)
- `Co-Authored-By` 안 넣음
- 기존 커밋의 author·committer는 안 고침

## PR 감시·리뷰 대응
- PR을 올리면 바로 Monitor로 3분마다 열린 PR 전체 확인: 사용자의 새 리뷰·코멘트·댓글(`🤖 Claude:` 답글 제외), merge·close, CI 실패
- Monitor 만료 시 재시작. 열린 PR이 없으면 종료
- 리뷰·코멘트·댓글이 오면 그 PR을 구현한 subagent를 다시 불러 대응(없으면 새 subagent). 사용자에게 따로 안 알림
- 수정했으면 해당 스레드에 수정 커밋 링크 답글
- 답글은 `🤖 Claude:`로 시작

## 도구 문서
- README 도구 목록: 이름, 버전, 용도, 라이선스만. 설치 관련 내용은 응답으로 안내
