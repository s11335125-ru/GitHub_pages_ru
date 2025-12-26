#!/usr/bin/env python3
# 1A2B (Bulls and Cows) 小遊戲 - 終端版
# 規則：
# - 目標是一個由 4 個不重複數字組成的數字（第一位不為 0）
# - A 表示數字與位置皆正確；B 表示數字正確但位置錯誤
# - 例如：目標 4271，猜 1234 → 1A2B（「2」位置對、1 和 4 在錯位）

import random
import sys
from typing import Tuple

DIGITS = "0123456789"


def generate_secret(length: int = 4, allow_leading_zero: bool = False) -> str:
	if not (2 <= length <= 10):
		raise ValueError("length 必須介於 2~10")
	digits = list(DIGITS)
	if not allow_leading_zero:
		first = random.choice(digits[1:])
		digits.remove(first)
		rest = random.sample(digits, length - 1)
		return first + "".join(rest)
	else:
		return "".join(random.sample(digits, length))


def score_guess(guess: str, secret: str) -> Tuple[int, int]:
	"""回傳 (A, B)"""
	a = sum(g == s for g, s in zip(guess, secret))
	b = sum(min(guess.count(d), secret.count(d)) for d in set(guess)) - a
	return a, b


def is_valid_guess(guess: str, length: int) -> Tuple[bool, str]:
	if len(guess) != length:
		return False, f"請輸入 {length} 位數字"
	if not guess.isdigit():
		return False, "只能輸入數字"
	if guess[0] == "0":
		return False, "第一位不能為 0"
	if len(set(guess)) != length:
		return False, "每個數字不得重複"
	return True, ""


def play_once(length: int = 4) -> None:
	secret = generate_secret(length)
	attempts = 0
	history = []  # (guess, a, b)

	print("\n===== 1A2B 猜數字遊戲 =====")
	print(f"目標：{length} 位不重複數字（第一位不為 0）")
	print("指令：輸入 'quit' 離開、'ans' 看答案（僅示範用途）、'his' 看歷史\n")

	while True:
		raw = input(f"請輸入你的猜測（{length} 位）：").strip()
		if not raw:
			continue
		if raw.lower() in {"quit", "exit"}:
			print("遊戲結束，再見！")
			sys.exit(0)
		if raw.lower() == "ans":
			print(f"[提示] 答案：{secret}")
			continue
		if raw.lower() == "his":
			if not history:
				print("尚無歷史紀錄。")
			else:
				print("歷史：")
				for i, (g, a, b) in enumerate(history, 1):
					print(f"  {i:02d}. {g} -> {a}A{b}B")
			continue

		ok, msg = is_valid_guess(raw, length)
		if not ok:
			print(f"輸入無效：{msg}")
			continue

		attempts += 1
		a, b = score_guess(raw, secret)
		history.append((raw, a, b))
		print(f"結果：{a}A{b}B")

		if a == length:
			print(f"恭喜答對！你共嘗試 {attempts} 次。")
			break


def main():
	print("歡迎來到 1A2B！")
	# 可自訂長度（預設 4）
	while True:
		try:
			choice = input("請輸入遊戲長度（2~10，直接 Enter 使用 4）：").strip()
			if choice == "":
				length = 4
			else:
				length = int(choice)
				if not (2 <= length <= 10):
					print("長度需介於 2~10。")
					continue
		except ValueError:
			print("請輸入數字。")
			continue

		play_once(length)

		again = input("還要再玩一次嗎？(y/n)：").strip().lower()
		if again not in {"y", "yes"}:
			print("感謝遊玩！")
			break


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("\n已中斷，歡迎下次再來！")   