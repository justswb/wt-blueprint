# 레포 작업 규칙

## 브랜치·워크트리
- 기능 작업은 상위 feat 브랜치(예: `feat/feature`)에서 작업 단계별로 하위 브랜치를 나눠 진행한다.
- 레포 공통 작업(CI 등)은 `main`에서 별도 브랜치를 만든다.
- 메인 세션은 계획, 위임, PR 감시만 한다. 나머지 작업(파일 수정, git·PR 작업, 리뷰 대응 포함)은 모두 `.worktrees/` 아래 워크트리에서 저렴한 하위 모델 subagent에 위임한다.
- 위임 결과는 메인 세션이 검토하지 않고 CI와 PR 리뷰로 확인한다.
- `.worktrees/`는 git으로 추적하지 않는다.

## PR 순서·stack
- 각 작업이 끝나면 PR을 올리고, 리뷰를 기다리지 않고 다음 작업을 시작한다.
- 상위 feat 브랜치의 하위 작업 PR은 GitHub stacked PR(`gh stack`)로 한 줄로 쌓는다. stack의 trunk는 상위 feat 브랜치로 한다(`gh stack init --base <feat 브랜치>`). 서로 의존하지 않는 작업도 같은 stack에 순서대로 쌓는다.
- 각 PR의 base는 바로 아래 PR의 브랜치이고, 맨 아래 PR의 base는 상위 feat 브랜치다. 순서는 GitHub stack으로 보이므로 PR 본문에 따로 적지 않는다.
- 첫 하위 작업 PR이 상위 feat 브랜치에 merge되면 상위 feat 브랜치 → `main` PR을 draft로 연다. 이 PR은 stack에 넣지 않는다. 마지막 하위 작업 PR이 merge되면 ready로 바꾼다.
- 레포 공통 작업은 stack 없이 `main` 대상 PR로 올린다.
- stack 브랜치를 맞출 때는 `gh stack sync`나 `gh stack rebase`를 쓰고, 이때의 rebase와 `--force-with-lease` push는 허용한다. 그 밖에는 merge를 쓰고, rebase와 강제 push는 사용자가 허용한 경우에만 한다.

## 커밋 author·committer
- author는 실제로 작업한 모델로 지정한다. 예: `Claude Opus 5.5 <noreply@anthropic.com>`, `Claude Haiku 5.5 <noreply@anthropic.com>`
- committer도 author와 같은 모델로 지정한다.
- author를 모델로 지정했으므로 `Co-Authored-By` 줄은 넣지 않는다.
- 이미 만든 커밋의 author·committer는 고치지 않는다.

## PR 리뷰 대응
- PR을 올리면 따로 지시가 없어도 바로 감시를 건다(Monitor). 3분마다 열린 PR 전체를 확인한다.
  - 사용자가 단 새 리뷰, 리뷰 코멘트, 댓글. `🤖 Claude:`로 시작하는 내 답글은 제외한다.
  - PR이 merge되거나 닫혔는지
  - CI 실패
- Monitor가 만료되면 다시 건다. 열린 PR이 모두 merge되거나 닫히면 감시를 끝낸다.
- PR에 리뷰, 리뷰 코멘트, 댓글이 달리면 따로 지시가 없어도 그 PR을 구현한 subagent를 다시 불러 대응을 맡긴다. 그 subagent가 없으면 새 subagent에 맡긴다.
- PR 코멘트 대응은 사용자에게 따로 알리지 않는다.
- 리뷰 코멘트를 반영해 수정했으면 그 스레드에 수정 커밋 링크를 답글로 남긴다.
- 내가 다는 답글은 `🤖 Claude:`로 시작해서 사용자 댓글과 구분한다.
