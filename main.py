from dolphin_memory_engine import read_word, read_byte, hook, read_bytes

ADDR_WORD_SCORE = int("0x804D0440", 16)
ADDR_BYTE_ATTACK = int("0x804D0433", 16)
ADDR_BYTE_LEVEL = int("0x804D042F", 16)
ADDR_BYTE_HP = int("0x804D0437", 16)
ADDR_HALFWORD_COIN = int("0x804D0446", 16)


def main():
    hook()
    print("reading...")
    score = read_bytes(ADDR_WORD_SCORE, 4)
    atk = read_byte(ADDR_BYTE_ATTACK)
    lvl = read_byte(ADDR_BYTE_LEVEL)
    hp = read_byte(ADDR_BYTE_HP)
    coin = read_bytes(ADDR_HALFWORD_COIN, 2)
    print({
        "score": int.from_bytes(score),
        "coin": int.from_bytes(coin),
        "atk": atk,
        "lvl": lvl,
        "hp": hp,
    })
    return 0


if __name__ == "__main__":
    main()
