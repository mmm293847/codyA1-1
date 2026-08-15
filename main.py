import json


# =========================
# 프롬프트 불러오기
# =========================
def load_prompts():
    try:
        with open("prompts.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# =========================
# 프롬프트 저장하기
# =========================
def save_prompts(prompts):
    with open("prompts.json", "w", encoding="utf-8") as file:
        json.dump(
            prompts,
            file,
            ensure_ascii=False,
            indent=4
        )


# =========================
# 프롬프트 추가
# =========================
def add_prompt(prompts):
    print("\n========== 프롬프트 추가 ==========\n")

    title = input("제목: ").strip()
    category = input("카테고리: ").strip()
    keywords_input = input("키워드 (쉼표로 구분): ").strip()

    keywords = [
        keyword.strip()
        for keyword in keywords_input.split(",")
        if keyword.strip()
    ]

    print("\n프롬프트 내용을 입력하세요.")
    print("입력을 끝내려면 빈 줄에서 Enter를 누르세요.\n")

    content_lines = []

    while True:
        line = input("> ")

        if line == "":
            break

        content_lines.append(line)

    content = "\n".join(content_lines)

    # 새로운 ID 생성
    new_id = max(
        [prompt["id"] for prompt in prompts],
        default=0
    ) + 1

    new_prompt = {
        "id": new_id,
        "title": title,
        "content": content,
        "category": category,
        "keywords": keywords,
        "favorite": False
    }

    prompts.append(new_prompt)

    # JSON 파일에 저장
    save_prompts(prompts)

    print("\n✅ 프롬프트가 추가되었습니다!")


# =========================
# 메인 메뉴
# =========================
def main():
    prompts = load_prompts()

    while True:
        print("\n==============================")
        print("      프롬프트 관리 프로그램")
        print("==============================")
        print("1. 프롬프트 추가")
        print("2. 프롬프트 목록")
        print("3. 프롬프트 검색")
        print("4. 카테고리별 보기")
        print("5. 즐겨찾기")
        print("6. 프롬프트 수정")
        print("7. 프롬프트 삭제")
        print("0. 종료")
        print("==============================")

        choice = input("선택: ")

        if choice == "1":
            add_prompt(prompts)

        elif choice == "2":
            print("\n현재 저장된 프롬프트:")
            print(prompts)

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다.")


# 프로그램 시작
if __name__ == "__main__":
    main()
