from dolphin_memory_engine import hook, read_bytes, write_bytes, is_hooked

ADDR_WORD_SCORE = int("0x804D0440", 16)
ADDR_BYTE_ATTACK = int("0x804D0433", 16)
ADDR_BYTE_LEVEL = int("0x804D042F", 16)
ADDR_BYTE_HP = int("0x804D0437", 16)
ADDR_BYTE_MAX_HP = int("0x804D043B", 16)
ADDR_HALFWORD_COIN = int("0x804D0446", 16)


def get_stats():
    if not is_hooked():
        hook()
    score = int.from_bytes(read_bytes(ADDR_WORD_SCORE, 4))
    atk = int.from_bytes(read_bytes(ADDR_BYTE_ATTACK, 1))
    lvl = int.from_bytes(read_bytes(ADDR_BYTE_LEVEL, 1))
    hp = int.from_bytes(read_bytes(ADDR_BYTE_HP, 1))
    maxhp = int.from_bytes(read_bytes(ADDR_BYTE_MAX_HP, 1))
    coin = int.from_bytes(read_bytes(ADDR_HALFWORD_COIN, 2))
    return {
        "score": score,
        "coin": coin,
        "atk": atk,
        "lvl": lvl,
        "hp": hp,
        "maxhp": maxhp
    }

def write_stats(stats):
    write_score(stats["score"])
    write_coin(stats["coin"])
    write_atk(stats["atk"])
    write_level(stats["lvl"])
    write_hp(stats["hp"])
    write_max_hp(stats["maxhp"])


def write_score(score):
    if not is_hooked():
        hook()
    write_bytes(ADDR_WORD_SCORE, score.to_bytes(4))


def write_atk(atk):
    if not is_hooked():
        hook()
    write_bytes(ADDR_BYTE_ATTACK, atk.to_bytes(1))


def write_level(level):
    if not is_hooked():
        hook()
    write_bytes(ADDR_BYTE_LEVEL, level.to_bytes(1))


def write_hp(hp):
    if not is_hooked():
        hook()
    write_bytes(ADDR_BYTE_HP, hp.to_bytes(1))

def write_max_hp(maxhp):
    if not is_hooked():
        hook()
    write_bytes(ADDR_BYTE_MAX_HP, maxhp.to_bytes(1))


def write_coin(coin):
    if not is_hooked():
        hook()
    write_bytes(ADDR_HALFWORD_COIN, coin.to_bytes(2))


def main():
    while True:
        print(get_stats())


if __name__ == "__main__":
    main()
