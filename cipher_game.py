import os
import time
import sys
import random

class C:
    PURPLE  = "\033[38;5;141m"
    GOLD    = "\033[38;5;214m"
    GREEN   = "\033[38;5;114m"
    RED     = "\033[38;5;203m"
    MUTED   = "\033[38;5;245m"
    WHITE   = "\033[38;5;253m"
    BOLD    = "\033[1m"
    DIM     = "\033[2m"
    RESET   = "\033[0m"
    CLEAR   = "\033c"

def p(text=""):
    """Print with reset at end."""
    print(text + C.RESET)

def slow(text, delay=0.018, color=""):
    """Typewriter effect for dramatic reveals."""
    for ch in text:
        sys.stdout.write(color + ch + C.RESET)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def divider(char="─", color=C.MUTED):
    p(color + char * 54)

def header():
    p(C.PURPLE + C.BOLD + """
   ██████╗  ██████╗ ████████╗ █████╗   ██████╗ ██████╗ ██████╗ ███████╗
   ██╔══██╗██╔═══██╗╚══██╔══╝██╔══██╗ ██╔════╝██╔═══██╗██╔══██╗██╔════╝
   ██████╔╝██║   ██║   ██║   ███████║ ██║     ██║   ██║██║  ██║█████╗ 
   ██╔══██╗██║   ██║   ██║   ██╔══██║ ██║     ██║   ██║██║  ██║██╔══╝
   ██║  ██║╚██████╔╝   ██║   ██║  ██║ ╚██████╗╚██████╔╝██████╔╝███████╗
   ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝""")
    p(C.GOLD   + "               C I P H E R   O P E R A T I V E")
    divider()


def encrypt(text, shift):
    """
    E(x) = (x + n) % 26
    Uppercase and lowercase handled separately.
    Non-alpha characters pass through unchanged.
    """
    result = []
    shift  = shift % 26
    for char in text:
        if char.isupper():
            result.append(chr((ord(char) - 65 + shift) % 26 + 65))
        elif char.islower():
            result.append(chr((ord(char) - 97 + shift) % 26 + 97))
        else:
            result.append(char)
    return "".join(result)

def decrypt(text, shift):
    """
    D(x) = (x - n) % 26
    Symmetric: same key locks and unlocks.
    """
    return encrypt(text, -shift)

def show_step_trace(char, shift, mode="encrypt"):
    """
    Shows the algorithm working step by step — exactly as the
    slides describe (ASCII → position → shift → modulo → output).
    """
    if not char.isalpha():
        p(C.MUTED + f"  '{char}'  →  non-alpha, passed through unchanged")
        return

    base     = 65 if char.isupper() else 97
    x        = ord(char) - base
    n        = shift % 26 if mode == "encrypt" else (-shift) % 26
    shifted  = (x + n) % 26
    result   = chr(shifted + base)

    p(C.MUTED  + f"  '{char}'"
      + C.MUTED  + f"  →  ord={C.WHITE}{ord(char)}{C.MUTED}"
      + f"  →  pos={C.WHITE}{x}{C.MUTED}"
      + f"  →  ({x} + {n}) % 26 = {C.WHITE}{shifted}{C.MUTED}"
      + f"  →  '{C.PURPLE}{result}{C.MUTED}'")

# ── Level definitions ─────────────────────────────────────────────
#
# Each level increases BOTH shift complexity AND text complexity:
#   Levels 1-2  → small shift (1-5),  single word
#   Levels 3-4  → medium shift (6-12), short phrase
#   Levels 5-6  → large shift (13-19), full sentence
#   Levels 7-8  → very large shift (20-24), multi-clause sentence
#   Level  9    → random shift 1-25, boss round — paragraph
#   Level  10   → elite round — random shift, no hints at all
#
LEVELS = [
    # (level, shift, plaintext, hint_allowed, lives)
    (1,  3,  "PYTHON",
         "Shift each letter forward by 3 positions in the alphabet.",  3),

    (2,  5,  "SECURE",
         "A shift of 5 means A→F, B→G, C→H ...",                      3),

    (3,  8,  "HACK THE PLANET",
         "Spaces pass through. Focus only on the letters.",            3),

    (4,  11, "DATA IN TRANSIT",
         "Remember: after Z wraps back to A using modulo 26.",         2),

    (5,  13, "ENCRYPTION IS THE SHIELD",
         "Shift 13 is special — it is its own inverse (ROT13).",       2),

    (6,  17, "THE CAESAR CIPHER IS A LOCKBOX NOT A VAULT",
         "Large shift. Work letter by letter and stay patient.",        2),

    (7,  19, "CONFIDENTIALITY IS THE FIRST PRINCIPLE OF SECURITY",
         "Getting tough. Try decrypting one word at a time.",          2),

    (8,  22, "BEFORE YOU ENCRYPT YOU MUST VALIDATE THE INPUT",
         "Shift 22 — think of it as shifting BACK by 4.",              2),

    (9,  None, "THE KEY TO ALL CRYPTOGRAPHY IS MATHEMATICAL TRANSFORMATION AND LOGICAL PRECISION",
         "Boss round. Shift key is hidden — you must brute force it.", 2),

    (10, None, "ROTACODE SEES ALL OPERATIVES WHO MASTER THE ART OF THE SHIFT CIPHER EARN THEIR CLEARANCE",
         None,                                                          1),
]

# ── Scoring ───────────────────────────────────────────────────────

class Score:
    def __init__(self):
        self.total       = 0
        self.level_scores = []

    def add(self, level, attempts, time_taken, used_hint, used_trace):
        # Base points per level
        base  = level * 100
        # Time bonus — faster = more points (max 50 bonus)
        t_bonus = max(0, 50 - int(time_taken))
        # Penalties
        attempt_penalty = (attempts - 1) * 20
        hint_penalty    = 30 if used_hint  else 0
        trace_penalty   = 15 if used_trace else 0
        earned = max(0, base + t_bonus - attempt_penalty - hint_penalty - trace_penalty)
        self.total += earned
        self.level_scores.append({
            "level": level, "earned": earned, "base": base,
            "time": round(time_taken, 1), "attempts": attempts
        })
        return earned

    def rank(self):
        if   self.total >= 2500: return C.PURPLE + "CRYPTOGRAPHIC ELITE"
        elif self.total >= 1800: return C.GOLD   + "SENIOR OPERATIVE"
        elif self.total >= 1200: return C.GREEN  + "FIELD AGENT"
        elif self.total >= 600:  return C.WHITE  + "ANALYST"
        else:                    return C.MUTED  + "RECRUIT"

# ── Game screens ──────────────────────────────────────────────────

def intro_screen():
    clear()
    header()
    slow("\n  Incoming transmission ...\n", 0.03, C.GOLD)
    time.sleep(0.4)
    slow("  OPERATIVE. You have been selected for cipher training.", 0.02, C.WHITE)
    slow("  Your mission: decrypt intercepted ciphertext across", 0.02, C.WHITE)
    slow("  10 escalating levels of difficulty.\n", 0.02, C.WHITE)
    slow("  Each message was encrypted using the Caesar cipher —", 0.02, C.MUTED)
    slow("  a substitution cipher that shifts every letter by a", 0.02, C.MUTED)
    slow("  fixed key (n). Your job is to find the plaintext.\n", 0.02, C.MUTED)
    p(C.GOLD   + "  Formula:  " + C.WHITE + "E(x) = (x + n) % 26")
    p(C.GOLD   + "  Reverse:  " + C.WHITE + "D(x) = (x - n) % 26\n")
    divider()
    p(C.MUTED  + "  [H] Use hint  [T] Show step trace  [Q] Quit")
    divider()
    input(C.PURPLE + "\n  Press ENTER to begin your mission..." + C.RESET)

def level_screen(lvl_data, score):
    level, shift, plaintext, hint, lives = lvl_data
    clear()
    header()

    # For boss/elite rounds shift is hidden
    is_boss  = (level == 9)
    is_elite = (level == 10)

    # Generate the ciphertext
    actual_shift = shift if shift is not None else random.randint(1, 25)
    ciphertext   = encrypt(plaintext, actual_shift)

    p(C.PURPLE + C.BOLD + f"\n  ◈ LEVEL {level} / 10")
    divider()

    # Difficulty indicators
    diff_label = (
        C.GREEN  + "EASY"    if level <= 2 else
        C.GOLD   + "MEDIUM"  if level <= 4 else
        C.GOLD   + "HARD"    if level <= 6 else
        C.RED    + "EXTREME" if level <= 8 else
        C.RED    + C.BOLD + "BOSS"
    )
    shift_display = (
        C.WHITE + str(actual_shift) if not (is_boss or is_elite)
        else C.RED + "UNKNOWN"
    )

    p(f"  Difficulty  {diff_label}")
    p(f"  Shift key   {shift_display}")
    p(f"  Lives       " + C.RED + "♥ " * lives)
    p(f"  Score       " + C.GOLD + str(score.total))
    divider()

    p(C.GOLD + "\n  INTERCEPTED CIPHERTEXT:\n")
    slow("  " + ciphertext, 0.025, C.WHITE)
    p()
    divider()

    if is_boss:
        p(C.MUTED + "  BOSS ROUND: Shift key is unknown.")
        p(C.MUTED + "  You must try shifts or use [T] trace to brute force.\n")
    if is_elite:
        p(C.RED + C.BOLD + "  ELITE ROUND: No hints. No traces. Shift hidden.")
        p(C.RED + "  This is the final test of your cipher mastery.\n")

    # Track state
    attempts    = 0
    used_hint   = False
    used_trace  = False
    start_time  = time.time()
    remaining   = lives

    while remaining > 0:
        try:
            raw = input(C.PURPLE + "  ▶ Your answer (or H/T/Q/B): " + C.WHITE).strip()
        except (EOFError, KeyboardInterrupt):
            p(C.MUTED + "\n  Mission aborted.")
            sys.exit()

        cmd = raw.upper()

        # ── Commands ──
        if cmd == "Q":
            p(C.MUTED + "\n  Standing down. Goodbye, operative.")
            sys.exit()

        if cmd == "B" and is_boss:
            # Brute force helper — shows all 25 possible decryptions
            p(C.MUTED + "\n  Running brute force across all 25 shifts...\n")
            for s in range(1, 26):
                attempt_decrypt = decrypt(ciphertext, s)
                p(C.MUTED + f"  Shift {str(s).rjust(2)}: " + C.WHITE + attempt_decrypt)
            p()
            used_hint = True
            continue

        if cmd == "H":
            if hint is None or is_elite:
                p(C.RED + "  No hints available at this level.")
            elif used_hint:
                p(C.MUTED + "  Hint already used.")
            else:
                used_hint = True
                p(C.GOLD + f"\n  HINT → {hint}\n")
            continue

        if cmd == "T":
            if is_elite:
                p(C.RED + "  Step trace disabled at elite level.")
                continue
            used_trace = True
            # Show the trace for the first 5 characters
            p(C.PURPLE + "\n  STEP TRACE — first 5 characters of ciphertext:\n")
            p(C.MUTED + "  char  ord  pos  formula              result")
            divider("·", C.MUTED)
            for ch in ciphertext[:5]:
                show_step_trace(ch, actual_shift, mode="decrypt")
            p()
            continue

        # ── Answer check ──
        attempts += 1
        guess = raw.upper()

        if guess == plaintext.upper():
            elapsed = time.time() - start_time
            earned  = score.add(level, attempts, elapsed, used_hint, used_trace)

            clear()
            header()
            slow(f"\n  ✓ CORRECT. Message decrypted.\n", 0.02, C.GREEN)
            p(C.WHITE  + f"  Plaintext  : " + C.GREEN + plaintext)
            p(C.WHITE  + f"  Shift used : " + C.PURPLE + str(actual_shift))
            p(C.WHITE  + f"  Attempts   : " + C.GOLD + str(attempts))
            p(C.WHITE  + f"  Time       : " + C.GOLD + f"{elapsed:.1f}s")
            p(C.WHITE  + f"  Points     : " + C.GOLD + f"+{earned}")
            p(C.WHITE  + f"  Total      : " + C.GOLD + str(score.total))

            # Show the full encryption / decryption display
            divider()
            p(C.MUTED + "\n  ── Algorithm breakdown ──\n")
            p(C.WHITE  + f"  Formula (encrypt): E(x) = (x + {actual_shift}) % 26")
            p(C.WHITE  + f"  Formula (decrypt): D(x) = (x - {actual_shift}) % 26\n")
            p(C.GOLD   + f"  Original  : " + C.WHITE + plaintext)
            p(C.GOLD   + f"  Encrypted : " + C.WHITE + ciphertext)
            p(C.GOLD   + f"  Decrypted : " + C.GREEN + plaintext)
            divider()

            input(C.PURPLE + "\n  Press ENTER for next level..." + C.RESET)
            return True  # level passed

        else:
            remaining -= 1
            if remaining > 0:
                p(C.RED + f"\n  ✗ Wrong. Lives remaining: " + "♥ " * remaining)
                p(C.MUTED + f"  You said: {C.WHITE}{guess}")
                if not used_hint and hint and not is_elite:
                    p(C.MUTED + "  Type [H] for a hint or [T] for step trace.\n")
            else:
                # Out of lives
                elapsed = time.time() - start_time
                score.add(level, attempts, elapsed, used_hint, used_trace)
                clear()
                header()
                slow(f"\n  ✗ MISSION FAILED — Level {level}\n", 0.02, C.RED)
                p(C.WHITE  + f"  The answer was : " + C.GREEN + plaintext)
                p(C.WHITE  + f"  Shift used     : " + C.PURPLE + str(actual_shift))
                p(C.WHITE  + f"  Ciphertext     : " + C.WHITE + ciphertext)
                divider()
                p(C.MUTED + "\n  The encrypted form of that message was:")
                p(C.MUTED + "  Built using E(x) = (x + n) % 26 on each letter.\n")

                choice = input(C.GOLD + "  Retry this level? [Y/N]: " + C.WHITE).strip().upper()
                if choice == "Y":
                    return level_screen(lvl_data, score)  # retry
                return False  # give up

    return False

def results_screen(score, levels_cleared):
    clear()
    header()
    slow("\n  Transmission closing. Compiling operative report...\n", 0.03, C.GOLD)
    time.sleep(0.5)

    divider()
    p(C.PURPLE + C.BOLD + "  MISSION DEBRIEF")
    divider()
    p(C.WHITE  + f"  Levels cleared : " + C.GOLD + f"{levels_cleared} / 10")
    p(C.WHITE  + f"  Total score    : " + C.GOLD + str(score.total))
    p(C.WHITE  + f"  Operative rank : " + score.rank())
    divider()

    p(C.MUTED + "\n  ── Level breakdown ──\n")
    for s in score.level_scores:
        bar = "█" * min(20, s["earned"] // 20)
        p(C.MUTED + f"  Lv {str(s['level']).rjust(2)}  "
          + C.PURPLE + f"{bar:<20}  "
          + C.GOLD + f"{str(s['earned']).rjust(4)} pts  "
          + C.MUTED + f"{s['attempts']} attempt(s)  {s['time']}s")

    divider()


# ── Main ──────────────────────────────────────────────────────────

def main():
    intro_screen()
    score          = Score()
    levels_cleared = 0

    for lvl_data in LEVELS:
        passed = level_screen(lvl_data, score)
        if passed:
            levels_cleared += 1
        # Even if they fail they see the next level (they lose points not progress)

    results_screen(score, levels_cleared)

if __name__ == "__main__":
    main()
