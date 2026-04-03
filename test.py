def all_chars():
    """a-z, A-Z, 한글 음절(가~힣) 순서로 모든 문자를 yield한다."""
    for c in range(ord('a'), ord('z') + 1):
        yield chr(c)
    for c in range(ord('A'), ord('Z') + 1):
        yield chr(c)
    for c in range(0xAC00, 0xD7A4):  # 가(U+AC00) ~ 힣(U+D7A3), 11172자
        yield chr(c)


if __name__ == "__main__":
    for ch in all_chars():
        print(ch, end=' ')
    print()
