# RotaCode — Cipher Operative

A terminal-based Caesar cipher game built in Python. Intercept encrypted transmissions and decrypt them across 10 escalating levels — before you run out of lives.

Built as **Project 2** of the DecodeLabs Cybersecurity Internship (Batch 2026).

---

## Demo

![RotaCode gameplay](assets/demo.gif)

---

## How to Run

**Requirements:** Python 3.6+  — no third-party libraries needed.

```bash
git clone https://github.com/YOUR_USERNAME/rotacode.git
cd rotacode
python cipher_game.py
```

> **Windows users:** the colored terminal output works best in Windows Terminal or VS Code's integrated terminal.

---

## Gameplay

You are a **Cipher Operative**. Each level presents an intercepted ciphertext encrypted with the Caesar cipher. Your job is to decrypt it and submit the plaintext.

| Command | Action |
|---------|--------|
| Type your answer | Submit a decryption attempt |
| `H` | Request a hint (-30 pts) |
| `T` | Show step-by-step trace for first 5 chars (-15 pts) |
| `B` | Brute-force all 25 shifts (Boss level only) |
| `Q` | Quit the game |

### Level Structure

| Levels | Difficulty | Shift Key | Lives |
|--------|------------|-----------|-------|
| 1 – 2  | Easy       | 3, 5      | 3     |
| 3 – 4  | Medium     | 8, 11     | 3     |
| 5 – 6  | Hard       | 13, 17    | 2     |
| 7 – 8  | Extreme    | 19, 22    | 2     |
| 9      | Boss       | Hidden    | 2     |
| 10     | Elite      | Hidden, no hints | 1 |

### Scoring

```
Score = (Level × 100) + Time Bonus − Attempt Penalty − Hint/Trace Penalty
```

| Factor | Effect |
|--------|--------|
| Speed  | Up to +50 bonus points |
| Wrong answer | −20 pts per attempt |
| Used hint | −30 pts |
| Used trace | −15 pts |

### Operative Ranks

| Score | Rank |
|-------|------|
| 2500+ | Cryptographic Elite |
| 1800+ | Senior Operative |
| 1200+ | Field Agent |
| 600+  | Analyst |
| <600  | Recruit |

---

## How the Cipher Works

The Caesar cipher shifts every letter in the alphabet by a fixed key `n`.

**Encryption:**
```
E(x) = (x + n) % 26
```

**Decryption:**
```
D(x) = (x - n) % 26
```

Where `x` is the 0-based position of the letter (A=0, B=1 ... Z=25).

**Example with shift 3:**
```
A → D    (0 + 3) % 26 = 3
Y → B    (24 + 3) % 26 = 1
Z → C    (25 + 3) % 26 = 2
```

Non-alphabetic characters (spaces, punctuation) pass through unchanged.

---

## Project Structure

```
rotacode/
├── cipher_game.py   # Main game — all logic lives here
├── assets/
│   └── demo.gif     # Gameplay preview
├── .gitignore
└── README.md
```

---

## Key Concepts Practiced

- Caesar cipher encryption & decryption logic
- Modular arithmetic (`% 26`) for alphabet wrapping
- ASCII manipulation using `ord()` and `chr()`
- Handling edge cases (spaces, punctuation, case sensitivity)
- Terminal UI with ANSI color codes
- Object-oriented scoring system

---

## Part of the DecodeLabs Cybersecurity Internship

This project is **Project 2: Basic Encryption & Decryption** from the DecodeLabs Industrial Training Kit (Batch 2026). The goal is to master the fundamentals of data confidentiality through hands-on implementation.

---

*"Master the logic of the shift, and you master the foundation of the shield."*
