# 포크 Git 워크플로우

이 저장소는 포크 기반으로 관리한다.

- `origin`: 내 포크 저장소
- `upstream`: 부모 원본 저장소

핵심 원칙은 하나다.

- 부모 저장소 변경은 `upstream`에서 받는다.
- 내가 올리는 변경은 `origin`에만 push한다.

## 왜 이렇게 관리하나

포크 저장소는 원본 저장소를 직접 쓰는 공간이 아니라, 원본을 따라가면서 내 변경을 쌓는 공간이다. 그래서 업데이트는 `upstream`에서 가져오고, 배포나 백업은 `origin`에 올린다.

이 흐름을 지키면 아래가 명확해진다.

- 원본 최신 변경 반영: `upstream`
- 내 저장소 공개 상태 유지: `origin`
- 실수로 부모 저장소에 push 시도할 가능성 축소

## 기본 흐름

`main`을 부모 저장소 최신 상태에 맞출 때는 아래 순서를 쓴다.

```powershell
git fetch upstream --prune
git merge --ff-only upstream/main
git push origin main
```

의미는 다음과 같다.

1. `git fetch upstream --prune`
   부모 저장소의 최신 브랜치와 커밋 정보를 가져온다.

2. `git merge --ff-only upstream/main`
   현재 `main`을 부모 `main`으로 fast-forward 한다.
   로컬 커밋이 엇갈려 있으면 merge commit을 만들지 않고 실패하게 해서, 기준 브랜치를 깔끔하게 유지한다.

3. `git push origin main`
   반영된 결과를 내 포크 저장소에 올린다.

## 현재 브랜치 규칙

현재는 브랜치 역할을 아래처럼 고정해서 쓴다.

- `main`: `upstream/main`을 따라가는 기준 브랜치
- `gunkim`: 실제 개발과 문서 작업을 하는 브랜치

즉, `main`에서는 직접 개발하지 않는다. 부모 저장소 최신 변경을 안전하게 받아오는 용도로만 쓴다.

## 현재 운영 절차

부모 저장소 최신 변경을 반영할 때는 먼저 `main`을 업데이트한다.

```powershell
git switch main
git fetch upstream --prune
git merge --ff-only upstream/main
git push origin main
```

그 다음 실제 작업 브랜치인 `gunkim`으로 돌아가서 `main`을 합친다.

```powershell
git switch gunkim
git merge main
git push origin gunkim
```

이 흐름을 쓰면 기준선과 작업선이 분리된다.

- 부모 원본과 같은 코드 확인: `main`
- 실제 개발, 디버깅, 문서 작업: `gunkim`

## 일상 규칙

- plain `git push`의 대상은 항상 `origin`이라고 생각한다.
- 부모 저장소 최신화가 필요하면 먼저 `upstream`을 fetch한다.
- `main`은 가능한 한 정리된 기준 브랜치로 둔다.
- 실험이나 기능 작업은 별도 브랜치에서 하고, 필요하면 다시 `origin`에 push한다.

## 브랜치 작업 예시

현재 저장소에서는 보통 `gunkim`을 작업 브랜치로 쓴다.

```powershell
git switch main
git fetch upstream --prune
git merge --ff-only upstream/main
git push origin main

git switch gunkim
git merge main
git push origin gunkim
```

필요하면 `gunkim`에서 다시 기능 브랜치를 따로 파도 되지만, 기본 규칙은 `main`은 기준선, `gunkim`은 개발 브랜치다.

## push 관련 메모

권한이 없다면 `upstream`으로 push는 실패한다. 그 자체로 큰 문제는 아니지만, 평소 습관은 아래처럼 가져가는 편이 안전하다.

- 받는 쪽은 `upstream`
- 올리는 쪽은 `origin`

즉, 이 저장소에서는 "부모에서 받고, 내 포크에 올린다"가 기본 규칙이다.
