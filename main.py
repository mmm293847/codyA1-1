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
# 프롬프트 목록 보기
# =========================
def list_prompts(prompts):
    print("\n========== 📋 프롬프트 목록 ==========\n")

    # 프롬프트가 없는 경우
    if not prompts:
        print("❌ 저장된 프롬프트가 없습니다.")
        return

    print(f"총 {len(prompts)}개의 프롬프트가 저장되어 있습니다.\n")

    for prompt in prompts:
        favorite = "⭐ 즐겨찾기" if prompt["favorite"] else ""

        print("┌" + "─" * 58 + "┐")
        print(f"│ ID       : {prompt['id']}")
        print(f"│ 제목     : {prompt['title']} {favorite}")
        print(f"│ 카테고리 : {prompt['category']}")
        print(f"│ 키워드   : {', '.join(prompt['keywords'])}")
        print("├" + "─" * 58 + "┤")
        print("│ 내용")

        # 여러 줄로 작성된 프롬프트도 보기 좋게 출력
        for line in prompt["content"].split("\n"):
            print(f"│ {line}")

        print("└" + "─" * 58 + "┘")
        print()

# =========================
# 프롬프트 검색
# =========================
def search_prompts(prompts):
    print("\n========== 프롬프트 검색 ==========\n")

    keyword = input("검색어를 입력하세요: ").strip().lower()

    if not keyword:
        print("❌ 검색어를 입력해주세요.")
        return

    results = []

    for prompt in prompts:
        title = prompt["title"].lower()
        content = prompt["content"].lower()
        category = prompt["category"].lower()

        keywords = [
            k.lower()
            for k in prompt["keywords"]
        ]

        # 제목 / 내용 / 카테고리 / 키워드 검색
        if (
            keyword in title
            or keyword in content
            or keyword in category
            or any(keyword in k for k in keywords)
        ):
            results.append(prompt)

    if not results:
        print("\n❌ 검색 결과가 없습니다.")
        return

    print(f"\n🔍 검색 결과: {len(results)}개\n")

    for prompt in results:
        favorite = "⭐" if prompt["favorite"] else ""

        print("--------------------------------")
        print(f"ID       : {prompt['id']}")
        print(f"제목     : {prompt['title']} {favorite}")
        print(f"카테고리 : {prompt['category']}")
        print(f"키워드   : {', '.join(prompt['keywords'])}")
        print(f"내용     : {prompt['content']}")
        print("--------------------------------")


# =========================
# 카테고리별 프롬프트 보기
# =========================
def category_prompts(prompts):
    print("\n========== 카테고리별 보기 ==========\n")

    # 저장된 카테고리 가져오기
    categories = []

    for prompt in prompts:
        category = prompt["category"]

        if category not in categories:
            categories.append(category)

    # 프롬프트가 없는 경우
    if not categories:
        print("❌ 저장된 프롬프트가 없습니다.")
        return

    # 카테고리 목록 출력
    print("카테고리 목록")

    for i, category in enumerate(categories, start=1):
        print(f"{i}. {category}")

    print("0. 돌아가기")

    choice = input("\n카테고리를 선택하세요: ")

    # 뒤로가기
    if choice == "0":
        return

    # 숫자인지 확인
    if not choice.isdigit():
        print("❌ 잘못된 입력입니다.")
        return

    category_index = int(choice) - 1

    # 존재하는 카테고리인지 확인
    if category_index < 0 or category_index >= len(categories):
        print("❌ 존재하지 않는 카테고리입니다.")
        return

    selected_category = categories[category_index]

    print(f"\n========== [{selected_category}] 프롬프트 ==========\n")

    # 선택한 카테고리의 프롬프트만 출력
    found = False

    for prompt in prompts:
        if prompt["category"] == selected_category:
            found = True

            favorite = "⭐" if prompt["favorite"] else ""

            print("--------------------------------")
            print(f"ID       : {prompt['id']}")
            print(f"제목     : {prompt['title']} {favorite}")
            print(f"카테고리 : {prompt['category']}")
            print(f"키워드   : {', '.join(prompt['keywords'])}")
            print(f"내용     : {prompt['content']}")
            print("--------------------------------")

    if not found:
        print("❌ 해당 카테고리에 프롬프트가 없습니다.")


# =========================
# 즐겨찾기
# =========================
def favorite_prompts(prompts):
    while True:
        print("\n========== ⭐ 즐겨찾기 ==========")
        print("1. 즐겨찾기 목록")
        print("2. 즐겨찾기 추가/해제")
        print("0. 돌아가기")

        choice = input("\n선택: ")

        # -------------------------
        # 1. 즐겨찾기 목록
        # -------------------------
        if choice == "1":
            favorites = [
                prompt
                for prompt in prompts
                if prompt["favorite"]
            ]

            if not favorites:
                print("\n⭐ 즐겨찾기에 등록된 프롬프트가 없습니다.")
                continue

            print(f"\n⭐ 즐겨찾기: {len(favorites)}개\n")

            for prompt in favorites:
                print("--------------------------------")
                print(f"ID       : {prompt['id']}")
                print(f"제목     : {prompt['title']} ⭐")
                print(f"카테고리 : {prompt['category']}")
                print(f"키워드   : {', '.join(prompt['keywords'])}")
                print(f"내용     : {prompt['content']}")
                print("--------------------------------")

        # -------------------------
        # 2. 즐겨찾기 추가/해제
        # -------------------------
        elif choice == "2":

            if not prompts:
                print("\n❌ 저장된 프롬프트가 없습니다.")
                continue

            print("\n========== 프롬프트 목록 ==========\n")

            for prompt in prompts:
                favorite = "⭐" if prompt["favorite"] else ""

                print(
                    f"{prompt['id']}. "
                    f"{prompt['title']} "
                    f"{favorite}"
                )

            try:
                prompt_id = int(
                    input("\n즐겨찾기 변경할 프롬프트 ID: ")
                )
            except ValueError:
                print("❌ 숫자를 입력해주세요.")
                continue

            selected_prompt = None

            for prompt in prompts:
                if prompt["id"] == prompt_id:
                    selected_prompt = prompt
                    break

            if selected_prompt is None:
                print("❌ 해당 ID의 프롬프트가 없습니다.")
                continue

            selected_prompt["favorite"] = not selected_prompt["favorite"]

            save_prompts(prompts)

            if selected_prompt["favorite"]:
                print(
                    f"\n⭐ '{selected_prompt['title']}' "
                    "프롬프트를 즐겨찾기에 추가했습니다."
                )
            else:
                print(
                    f"\n☆ '{selected_prompt['title']}' "
                    "프롬프트를 즐겨찾기에서 해제했습니다."
                )

        # -------------------------
        # 0. 돌아가기
        # -------------------------
        elif choice == "0":
            break

        else:
            print("❌ 잘못된 입력입니다.")


# =========================
# 프롬프트 수정
# =========================
def edit_prompt(prompts):
    print("\n========== 프롬프트 수정 ==========\n")

    if not prompts:
        print("❌ 저장된 프롬프트가 없습니다.")
        return

    # 프롬프트 목록
    print("현재 프롬프트 목록\n")

    for prompt in prompts:
        favorite = "⭐" if prompt["favorite"] else ""

        print(
            f"ID: {prompt['id']} | "
            f"제목: {prompt['title']} {favorite}"
        )

    # 수정할 ID
    try:
        prompt_id = int(
            input("\n수정할 프롬프트 ID: ")
        )
    except ValueError:
        print("❌ 숫자를 입력해주세요.")
        return

    # 프롬프트 찾기
    selected_prompt = None

    for prompt in prompts:
        if prompt["id"] == prompt_id:
            selected_prompt = prompt
            break

    if selected_prompt is None:
        print("❌ 해당 ID의 프롬프트가 없습니다.")
        return

    # 현재 정보
    print("\n========== 현재 프롬프트 ==========\n")
    print(f"제목     : {selected_prompt['title']}")
    print(f"카테고리 : {selected_prompt['category']}")
    print(f"키워드   : {', '.join(selected_prompt['keywords'])}")
    print(f"내용     :\n{selected_prompt['content']}")

    print("\n--------------------------------")
    print("수정하지 않을 항목은 Enter를 누르세요.")
    print("--------------------------------\n")

    # 제목
    new_title = input(
        f"제목 [{selected_prompt['title']}]: "
    ).strip()

    if new_title:
        selected_prompt["title"] = new_title

    # 카테고리
    new_category = input(
        f"카테고리 [{selected_prompt['category']}]: "
    ).strip()

    if new_category:
        selected_prompt["category"] = new_category

    # 키워드
    current_keywords = ", ".join(
        selected_prompt["keywords"]
    )

    new_keywords_input = input(
        f"키워드 [{current_keywords}]: "
    ).strip()

    if new_keywords_input:
        selected_prompt["keywords"] = [
            keyword.strip()
            for keyword in new_keywords_input.split(",")
            if keyword.strip()
        ]

    # 내용
    print("\n프롬프트 내용을 수정하세요.")
    print("기존 내용을 유지하려면 첫 줄에서 Enter를 누르세요.")
    print("입력을 끝내려면 빈 줄에서 Enter를 누르세요.\n")

    print("----- 현재 내용 -----")
    print(selected_prompt["content"])
    print("--------------------\n")

    content_lines = []

    first_line = input("> ")

    if first_line == "":
        new_content = selected_prompt["content"]

    else:
        content_lines.append(first_line)

        while True:
            line = input("> ")

            if line == "":
                break

            content_lines.append(line)

        new_content = "\n".join(content_lines)

    selected_prompt["content"] = new_content

    # 저장
    save_prompts(prompts)

    print("\n✅ 프롬프트가 수정되었습니다!")

# =========================
# 프롬프트 삭제
# =========================
def delete_prompt(prompts):
    print("\n========== 프롬프트 삭제 ==========\n")

    if not prompts:
        print("❌ 저장된 프롬프트가 없습니다.")
        return

    # 현재 프롬프트 목록 출력
    print("현재 프롬프트 목록\n")

    for prompt in prompts:
        favorite = "⭐" if prompt["favorite"] else ""

        print(
            f"ID: {prompt['id']} | "
            f"제목: {prompt['title']} "
            f"{favorite}"
        )

    # 삭제할 ID 입력
    try:
        prompt_id = int(
            input("\n삭제할 프롬프트 ID: ")
        )
    except ValueError:
        print("❌ 숫자를 입력해주세요.")
        return

    # 삭제할 프롬프트 찾기
    selected_prompt = None

    for prompt in prompts:
        if prompt["id"] == prompt_id:
            selected_prompt = prompt
            break

    # 해당 ID가 없는 경우
    if selected_prompt is None:
        print("❌ 해당 ID의 프롬프트가 없습니다.")
        return

    # 삭제할 프롬프트 정보 출력
    print("\n========== 삭제할 프롬프트 ==========\n")
    print(f"ID       : {selected_prompt['id']}")
    print(f"제목     : {selected_prompt['title']}")
    print(f"카테고리 : {selected_prompt['category']}")
    print(f"키워드   : {', '.join(selected_prompt['keywords'])}")
    print(f"내용     : {selected_prompt['content']}")

    # 삭제 확인
    confirm = input(
        "\n정말 삭제하시겠습니까? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("\n❌ 삭제를 취소했습니다.")
        return

    # 프롬프트 삭제
    prompts.remove(selected_prompt)

    # JSON 파일 저장
    save_prompts(prompts)

    print(
        f"\n✅ '{selected_prompt['title']}' "
        "프롬프트가 삭제되었습니다."
    )

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
          list_prompts(prompts)

        elif choice == "3":
            search_prompts(prompts)

        elif choice == "4":
            category_prompts(prompts)

        elif choice == "5":
            favorite_prompts(prompts)

        elif choice == "6":
            edit_prompt(prompts)

        elif choice == "7":
            delete_prompt(prompts)

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("❌ 잘못된 입력입니다.")


# =========================
# 프로그램 시작
# =========================
if __name__ == "__main__":
    main()
