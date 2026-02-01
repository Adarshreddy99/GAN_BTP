# Unicode and Character Encoding: A Comprehensive Guide
## Focus on UTF-8, UTF-16, and Telugu Script Processing

---

## Table of Contents

1. [Introduction to Character Encoding](#1-introduction-to-character-encoding)
2. [Number Systems: Binary, Octal, Decimal, and Hexadecimal](#2-number-systems-binary-octal-decimal-and-hexadecimal)
3. [Unicode Standard Overview](#3-unicode-standard-overview)
4. [Unicode Code Points and Character Assignment](#4-unicode-code-points-and-character-assignment)
5. [UTF-8 Encoding](#5-utf-8-encoding)
6. [UTF-16 Encoding](#6-utf-16-encoding)
7. [Endianness and Byte Order](#7-endianness-and-byte-order)
8. [Telugu Script in Unicode](#8-telugu-script-in-unicode)
9. [Conversion Algorithms](#9-conversion-algorithms)
10. [Operating System and Machine-Level Processing](#10-operating-system-and-machine-level-processing)
11. [Implementation Considerations](#11-implementation-considerations)

---

## 1. Introduction to Character Encoding

### 1.1 What is Character Encoding?

Character encoding is a systematic method of representing characters (letters, numbers, symbols) as numerical values that computers can process and store. At the fundamental level, computers only understand binary data (0s and 1s), so every character must be mapped to a unique numerical code.

Think of it this way: imagine you want to send a secret message to a friend, but instead of using words, you agree that every letter in the alphabet will be replaced by a number. "A" becomes 1, "B" becomes 2, and so on. Character encoding is exactly that kind of agreed-upon mapping — except it is done between humans and computers, and it covers not just English letters but every writing system on Earth.

### 1.2 Evolution of Character Encoding

```
ASCII (1963)
    ↓
Extended ASCII / Code Pages (1980s)
    ↓
Unicode (1991)
    ↓
UTF-8 (1993), UTF-16 (1996), UTF-32
```

**ASCII (American Standard Code for Information Interchange)**
- 7-bit encoding
- Represents 128 characters (0-127)
- Covers English letters, digits, and basic symbols
- Limitation: Cannot represent non-English scripts

Why only 7 bits? A single byte has 8 bits, but ASCII intentionally uses only 7. The 8th bit was reserved for parity checking (error detection) in early communication systems. This gives 2^7 = 128 unique codes.

**Extended ASCII and Code Pages**
- 8-bit encoding (256 characters)
- Different code pages for different languages
- Problem: Same byte value represents different characters in different code pages
- No universal standard for multilingual text

The code page problem is serious. For example, byte value 0xE0 represents "à" in ISO 8859-1 (Western European), but it represents "а" (Cyrillic a) in Windows-1251. If you open a Russian text file using a Western European code page, you get gibberish. This is why a universal standard was needed.

**Unicode Solution**
- Universal character set
- Single encoding standard for all world's writing systems
- Over 149,000 characters from 161 scripts (as of Unicode 15.0)
- Consistent representation across platforms and languages

---

## 2. Number Systems: Binary, Octal, Decimal, and Hexadecimal

Before diving into encoding details, it is essential to firmly understand how numbers are represented in different bases, because encoding values are written and manipulated in binary, octal, decimal, and hexadecimal constantly throughout this entire document.

### 2.1 What Is a Number Base (Radix)?

A number base (or radix) determines how many unique digit symbols are used and what positional value each digit carries. In base-N, each digit position represents a power of N, starting from N^0 (ones place) on the right and increasing leftward.

**General formula for a number in base N:**

```
Number = d_k × N^k + d_(k-1) × N^(k-1) + ... + d_1 × N^1 + d_0 × N^0

Where:
  d_i  = the digit at position i
  N    = the base
  k    = the index of the leftmost digit
```

### 2.2 Binary (Base 2)

Binary uses only two digits: **0** and **1**. Computers use binary because electronic circuits have two natural states — on (1) and off (0). Every piece of data a computer stores or processes is ultimately a sequence of binary digits called **bits**.

**Key terminology:**
- **Bit**: A single binary digit (0 or 1)
- **Nibble**: 4 bits (can represent 0–15, or 0x0–0xF)
- **Byte**: 8 bits (can represent 0–255, or 0x00–0xFF)

**Dry Run: Converting Decimal 53 to Binary**

```
Goal: 53 (decimal) → ? (binary)
Method: Repeatedly divide by 2, collect remainders bottom-to-top.

  53 ÷ 2 = 26  remainder 1   ← least significant bit (rightmost)
  26 ÷ 2 = 13  remainder 0
  13 ÷ 2 =  6  remainder 1
   6 ÷ 2 =  3  remainder 0
   3 ÷ 2 =  1  remainder 1
   1 ÷ 2 =  0  remainder 1   ← most significant bit (leftmost)

Read remainders bottom-to-top: 110101

Verification: 1×2^5 + 1×2^4 + 0×2^3 + 1×2^2 + 0×2^1 + 1×2^0
            = 32 + 16 + 0 + 4 + 0 + 1
            = 53 ✓
```

**Dry Run: Converting Binary 10110 to Decimal**

```
Binary: 1  0  1  1  0
Power:  4  3  2  1  0   (exponents of 2, right to left)

= 1×2^4 + 0×2^3 + 1×2^2 + 1×2^1 + 0×2^0
= 16    + 0     + 4     + 2     + 0
= 22 (decimal)
```

### 2.3 Octal (Base 8)

Octal uses digits **0 through 7**. It was historically popular in computing because a byte (8 bits) can be split into groups of 3 bits neatly (with one bit left over), and each group of 3 bits maps to exactly one octal digit. Octal is still used in file permissions on Unix/Linux systems (e.g., `chmod 755`).

**Each octal digit represents exactly 3 binary bits:**

```
Octal Digit │ Binary
────────────┼────────
    0       │  000
    1       │  001
    2       │  010
    3       │  011
    4       │  100
    5       │  101
    6       │  110
    7       │  111
```

**Dry Run: Converting Decimal 219 to Octal**

```
Method: Repeatedly divide by 8, collect remainders bottom-to-top.

  219 ÷ 8 = 27  remainder 3   ← least significant digit
   27 ÷ 8 =  3  remainder 3
    3 ÷ 8 =  0  remainder 3   ← most significant digit

Read remainders bottom-to-top: 333 (octal)

Verification: 3×8^2 + 3×8^1 + 3×8^0
            = 3×64 + 3×8  + 3×1
            = 192  + 24   + 3
            = 219 ✓
```

**Dry Run: Converting Octal 752 to Decimal**

```
Octal: 7  5  2
Power: 2  1  0   (exponents of 8)

= 7×8^2 + 5×8^1 + 2×8^0
= 7×64  + 5×8   + 2×1
= 448   + 40    + 2
= 490 (decimal)
```

**Dry Run: Converting Octal 333 to Binary (shortcut method)**

```
Replace each octal digit with its 3-bit binary equivalent:
  3 → 011
  3 → 011
  3 → 011

Result: 011 011 011 → 11011011 (drop leading zero)

Verification: 11011011 binary
= 128+64+0+16+8+0+2+1 = 219 ✓ (matches our earlier result)
```

**Octal and Unicode:** Octal is relevant to encoding because it appears frequently in C/C++ string literals. For instance, the UTF-8 bytes for Telugu "అ" (0xE0 0xB0 0x85) can be written in C as `"\340\260\205"` — those are octal escape sequences.

```
0xE0 = 224 decimal. Convert to octal:
  224 ÷ 8 = 28 remainder 0
   28 ÷ 8 =  3 remainder 4
    3 ÷ 8 =  0 remainder 3
  → 340 (octal)  ✓  (matches \340)

0xB0 = 176 decimal. Convert to octal:
  176 ÷ 8 = 22 remainder 0
   22 ÷ 8 =  2 remainder 6
    2 ÷ 8 =  0 remainder 2
  → 260 (octal)  ✓  (matches \260)

0x85 = 133 decimal. Convert to octal:
  133 ÷ 8 = 16 remainder 5
   16 ÷ 8 =  2 remainder 0
    2 ÷ 8 =  0 remainder 2
  → 205 (octal)  ✓  (matches \205)
```

### 2.4 Decimal (Base 10)

Decimal is the number system humans use in everyday life, using digits **0 through 9**. In the context of computing and encoding, decimal values serve as the "human-friendly" reference point. Every Unicode code point has a decimal equivalent, and understanding how to convert between decimal and other bases is a fundamental skill.

**Dry Run: Converting Decimal 3077 — the decimal value of U+0C05 (Telugu "అ") — into all other bases**

```
Decimal 3077 → Binary:
  3077 ÷ 2 = 1538 r 1
  1538 ÷ 2 =  769 r 0
   769 ÷ 2 =  384 r 1
   384 ÷ 2 =  192 r 0
   192 ÷ 2 =   96 r 0
    96 ÷ 2 =   48 r 0
    48 ÷ 2 =   24 r 0
    24 ÷ 2 =   12 r 0
    12 ÷ 2 =    6 r 0
     6 ÷ 2 =    3 r 0
     3 ÷ 2 =    1 r 1
     1 ÷ 2 =    0 r 1

  Read bottom-to-top: 110000000101 (binary)

Decimal 3077 → Octal:
  3077 ÷ 8 = 384 r 5
   384 ÷ 8 =  48 r 0
    48 ÷ 8 =   6 r 0
     6 ÷ 8 =   0 r 6

  Read bottom-to-top: 6005 (octal)

Decimal 3077 → Hexadecimal:
  3077 ÷ 16 = 192 r 5    → digit: 5
   192 ÷ 16 =  12 r 0    → digit: 0
    12 ÷ 16 =   0 r 12   → digit: C

  Read bottom-to-top: C05 (hex) → written as 0C05 with leading zero

Summary for U+0C05 (అ):
  Decimal:     3077
  Binary:      0000 1100 0000 0101
  Octal:       6005
  Hexadecimal: 0C05
```

### 2.5 Hexadecimal (Base 16)

Hexadecimal (hex) uses digits **0–9 and A–F** (where A=10, B=11, C=12, D=13, E=14, F=15). Hexadecimal is the single most important number system for understanding character encoding because:

1. Each hex digit represents exactly **4 binary bits** (one nibble)
2. A byte (8 bits) is always exactly **2 hex digits**
3. Unicode code points are written in hex (e.g., U+0C05)
4. Memory addresses, byte values, and bitmasks are all expressed in hex

**Hex-to-Binary quick reference (memorize this table):**

```
Hex │ Binary    Hex │ Binary
────┼──────    ────┼──────
 0  │ 0000      8  │ 1000
 1  │ 0001      9  │ 1001
 2  │ 0010      A  │ 1010
 3  │ 0011      B  │ 1011
 4  │ 0100      C  │ 1100
 5  │ 0101      D  │ 1101
 6  │ 0110      E  │ 1110
 7  │ 0111      F  │ 1111
```

**Dry Run: Converting Decimal 255 to Hexadecimal**

```
  255 ÷ 16 = 15  remainder 15  → digit: F
   15 ÷ 16 =  0  remainder 15  → digit: F

Result: FF (hex)

Verification: F×16^1 + F×16^0 = 15×16 + 15×1 = 240 + 15 = 255 ✓
```

**Dry Run: Converting Hex 0xE0 to Decimal and Binary**

```
Hex: E  0
     ↓  ↓
Dec: E×16^1 + 0×16^0 = 14×16 + 0 = 224 (decimal)

Bin: E    →  1110
     0    →  0000
     Result: 11100000 (binary)

Verification: 128+64+32+0+0+0+0+0 = 224 ✓
```

**Dry Run: Converting Hex 0xB0 to Decimal and Binary**

```
Hex: B  0
Dec: B×16 + 0×1 = 11×16 + 0 = 176 (decimal)
Bin: B → 1011, 0 → 0000 → 10110000

Verification: 128+0+32+16+0+0+0+0 = 176 ✓
```

**Dry Run: Converting Hex 0x85 to Decimal and Binary**

```
Hex: 8  5
Dec: 8×16 + 5×1 = 128 + 5 = 133 (decimal)
Bin: 8 → 1000, 5 → 0101 → 10000101

Verification: 128+0+0+0+0+4+0+1 = 133 ✓
```

### 2.6 Converting Between Bases — Summary of Methods

```
┌─────────────────────────────────────────────────────────────┐
│               Base Conversion Cheat Sheet                   │
├─────────────────────────────────────────────────────────────┤
│  FROM Decimal TO any base:                                  │
│    → Repeatedly divide by the target base                   │
│    → Collect remainders (bottom-to-top = the answer)        │
│                                                             │
│  FROM any base TO Decimal:                                  │
│    → Multiply each digit by base^(position)                 │
│    → Sum all the products                                   │
│                                                             │
│  Binary ↔ Hex  (fastest shortcut):                          │
│    → Group binary digits into nibbles (4 bits)              │
│    → Each nibble maps directly to one hex digit             │
│                                                             │
│  Binary ↔ Octal (shortcut):                                 │
│    → Group binary digits into triplets (3 bits)             │
│    → Each triplet maps directly to one octal digit          │
│                                                             │
│  Hex ↔ Octal (no direct shortcut):                          │
│    → Convert through binary or decimal as intermediate      │
└─────────────────────────────────────────────────────────────┘
```

### 2.7 How These Bases Connect to Unicode Encoding

The reason all four bases matter in this document:

- **Binary** is what actually lives in memory. Every byte is 8 binary bits. The UTF-8 encoding algorithm works by packing code point bits into specific binary patterns (like `1110xxxx 10xxxxxx 10xxxxxx`). You must be comfortable reading and writing binary to understand these patterns.

- **Octal** appears in C/C++ character literals (e.g., `"\340\260\205"` for Telugu "అ" in UTF-8) and in Unix file permissions. When you see a backslash followed by three digits in a string literal, those are octal escape codes.

- **Decimal** is the human-readable reference. Unicode charts often list the decimal value alongside the hex code point. For instance, Telugu "అ" is code point U+0C05, which equals decimal 3077.

- **Hexadecimal** is the native language of encoding. Code points (U+0C05), byte values (0xE0), bitmasks (0x3F), and memory addresses are all written in hex. Two hex digits always equal one byte exactly, which makes hex the most natural way to express byte-level data.

---

## 3. Unicode Standard Overview

### 3.1 Unicode Design Principles

Unicode follows these fundamental principles:

1. **Universal Repertoire**: Coverage of all characters from all writing systems
2. **Efficiency**: Compact encoding for common characters
3. **Uniformity**: Fixed-width code points in the abstract character set
4. **Unambiguous**: Each code point has exactly one meaning

### 3.2 Unicode Architecture

```
┌─────────────────────────────────────────┐
│      Abstract Character Repertoire      │
│    (Code Points U+0000 to U+10FFFF)     │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│         Character Properties            │
│   (Name, Category, Scripts, etc.)       │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Encoding Forms (UTF)              │
│    UTF-8, UTF-16, UTF-32                │
└─────────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────────┐
│       Encoding Schemes                  │
│   (Byte Order: BE, LE)                  │
└─────────────────────────────────────────┘
```

An important distinction: **Unicode code points** are abstract identifiers. They are not bytes stored on disk. The encoding forms (UTF-8, UTF-16, UTF-32) are the concrete byte sequences that represent those code points in memory and on storage media. A single code point can have different byte representations depending on which encoding you use.

### 3.3 Unicode Planes

Unicode code space is divided into 17 planes, each containing 65,536 (2^16) code points:

| Plane | Range | Name | Usage |
|-------|-------|------|-------|
| 0 | U+0000 to U+FFFF | Basic Multilingual Plane (BMP) | Most common characters from all scripts |
| 1 | U+10000 to U+1FFFF | Supplementary Multilingual Plane (SMP) | Historic scripts, symbols, emoji |
| 2 | U+20000 to U+2FFFF | Supplementary Ideographic Plane (SIP) | CJK ideographs |
| 3-13 | U+30000 to U+DFFFF | Unassigned | Reserved for future use |
| 14 | U+E0000 to U+EFFFF | Supplementary Special-purpose Plane (SSP) | Tags and variation selectors |
| 15-16 | U+F0000 to U+10FFFF | Private Use Areas | Application-specific characters |

**Total Unicode Code Space**: 1,114,112 code points (U+0000 to U+10FFFF)

Why 1,114,112? Let us verify: 17 planes × 65,536 code points per plane = 1,114,112. And 65,536 = 2^16 because each plane spans exactly 16 bits of address space.

**Important Reserved Ranges**:
- **U+D800 to U+DFFF**: Surrogate pairs (used only in UTF-16, not valid characters)
- **U+FDD0 to U+FDEF**: Non-characters
- **U+FFFE and U+FFFF**: Non-characters in each plane

---

## 4. Unicode Code Points and Character Assignment

### 4.1 Code Point Structure

A Unicode code point is written in the format **U+XXXX** (for BMP) or **U+XXXXX** (for supplementary planes), where X represents a hexadecimal digit.

The "U+" prefix is a convention that tells you "this is a Unicode code point, and the number that follows is in hexadecimal." It is not part of the number itself — it is just a label.

Examples:
- U+0041: Latin Capital Letter A
- U+0C05: Telugu Letter A (అ)
- U+1F600: Grinning Face Emoji (😀)

**Breaking down U+0C05 in all bases:**

```
Notation:  U+0C05
Hex:       0C05
Decimal:   0×16^3 + C×16^2 + 0×16^1 + 5×16^0
         = 0 + 12×256 + 0 + 5
         = 3077
Binary:    0000 1100 0000 0101
Octal:     6005
```

### 4.2 How Unicode Mappings are Decided

The Unicode Consortium follows a rigorous process:

1. **Script Encoding Proposals**: Submitted by experts, governments, or organizations
2. **Review Process**: Technical review by Unicode Technical Committee (UTC)
3. **Character Properties**: Each character is assigned properties:
   - Name (immutable once assigned)
   - General Category (Letter, Mark, Number, Punctuation, Symbol, Separator, Other)
   - Script (Latin, Telugu, Arabic, etc.)
   - Bidirectional class (for text direction)
   - Combining class (for diacritics)
   - Case mapping (uppercase/lowercase)

4. **Stability Policy**: Once a code point is assigned, it never changes
5. **Allocation Strategy**: Related characters are grouped in blocks

### 4.3 Character Properties Table Example

| Code Point | Character | Name | Category | Script |
|------------|-----------|------|----------|--------|
| U+0041 | A | LATIN CAPITAL LETTER A | Uppercase Letter | Latin |
| U+0C05 | అ | TELUGU LETTER A | Letter | Telugu |
| U+0C4D | ్ | TELUGU SIGN VIRAMA | Mark, Nonspacing | Telugu |

---

## 5. UTF-8 Encoding

### 5.1 UTF-8 Design Principles

UTF-8 (8-bit Unicode Transformation Format) is a variable-length encoding:

**Key Properties**:
1. **Variable Length**: 1 to 4 bytes per character
2. **ASCII Compatibility**: First 128 characters (U+0000 to U+007F) are identical to ASCII
3. **Self-Synchronizing**: Can detect character boundaries without scanning from the beginning
4. **Efficient**: Compact for Latin scripts, reasonable for all scripts

### 5.2 UTF-8 Encoding Structure

UTF-8 uses a prefix code system where the first bits of each byte indicate its role:

```
Code Point Range         | Byte 1    | Byte 2    | Byte 3    | Byte 4
-------------------------|-----------|-----------|-----------|----------
U+0000   to U+007F       | 0xxxxxxx  |           |           |
U+0080   to U+07FF       | 110xxxxx  | 10xxxxxx  |           |
U+0800   to U+FFFF       | 1110xxxx  | 10xxxxxx  | 10xxxxxx  |
U+10000  to U+10FFFF     | 11110xxx  | 10xxxxxx  | 10xxxxxx  | 10xxxxxx
```

**Bit Patterns**:
- **0xxxxxxx**: Single-byte character (ASCII)
- **110xxxxx**: Start of 2-byte sequence
- **1110xxxx**: Start of 3-byte sequence
- **11110xxx**: Start of 4-byte sequence
- **10xxxxxx**: Continuation byte

**Why this pattern works (self-synchronizing property):** If you land randomly in the middle of a multi-byte UTF-8 sequence, you will see bytes starting with `10`. You know these are continuation bytes and not the start of any character. You can simply skip forward until you find a byte that does NOT start with `10`, and that is the start of the next character. No other encoding has this property.

**How many payload bits does each byte type carry?**

```
Byte type     | Total bits | Header bits | Payload bits
──────────────┼────────────┼─────────────┼─────────────
0xxxxxxx      |     8      |      1      |      7
110xxxxx      |     8      |      3      |      5
1110xxxx      |     8      |      4      |      4
11110xxx      |     8      |      5      |      3
10xxxxxx      |     8      |      2      |      6

So total payload bits per sequence:
  1-byte: 7 bits  → can encode 0 to 127           (2^7  - 1 = 127)
  2-byte: 5+6 = 11 bits → up to 2047             (2^11 - 1 = 2047)
  3-byte: 4+6+6 = 16 bits → up to 65535          (2^16 - 1 = 65535)
  4-byte: 3+6+6+6 = 21 bits → up to 2097151     (but capped at 1114111 = U+10FFFF)
```

### 5.3 UTF-8 Encoding Algorithm

**Algorithm: Unicode Code Point → UTF-8**

```
Input: Unicode code point U (integer value)
Output: Byte sequence in UTF-8

FUNCTION unicode_to_utf8(U):
    IF U >= 0x00000000 AND U <= 0x0000007F:
        // 1-byte sequence
        byte1 = U
        RETURN [byte1]
    
    ELSE IF U >= 0x00000080 AND U <= 0x000007FF:
        // 2-byte sequence
        byte1 = 0xC0 | (U >> 6)           // 110xxxxx
        byte2 = 0x80 | (U & 0x3F)         // 10xxxxxx
        RETURN [byte1, byte2]
    
    ELSE IF U >= 0x00000800 AND U <= 0x0000FFFF:
        // 3-byte sequence (check for surrogates)
        IF U >= 0xD800 AND U <= 0xDFFF:
            ERROR: "Surrogate code points are invalid"
        
        byte1 = 0xE0 | (U >> 12)          // 1110xxxx
        byte2 = 0x80 | ((U >> 6) & 0x3F)  // 10xxxxxx
        byte3 = 0x80 | (U & 0x3F)         // 10xxxxxx
        RETURN [byte1, byte2, byte3]
    
    ELSE IF U >= 0x00010000 AND U <= 0x0010FFFF:
        // 4-byte sequence
        byte1 = 0xF0 | (U >> 18)          // 11110xxx
        byte2 = 0x80 | ((U >> 12) & 0x3F) // 10xxxxxx
        byte3 = 0x80 | ((U >> 6) & 0x3F)  // 10xxxxxx
        byte4 = 0x80 | (U & 0x3F)         // 10xxxxxx
        RETURN [byte1, byte2, byte3, byte4]
    
    ELSE:
        ERROR: "Invalid Unicode code point"
END FUNCTION
```

**Understanding the bitwise operations used in the algorithm:**

The two key operators are the **right shift** (`>>`) and the **bitwise OR** (`|`), along with the **bitwise AND** (`&`):

- `U >> n` shifts all bits of U to the right by n positions, effectively dividing U by 2^n and discarding the remainder. This extracts the upper bits.
- `U & mask` keeps only the bits where the mask has a 1. For example, `U & 0x3F` (mask = `00111111`) keeps only the lowest 6 bits.
- `prefix | data` combines the fixed header pattern with the payload bits. For example, `0xE0 | (U >> 12)` combines header `11100000` with the top 4 payload bits.

### 5.4 UTF-8 Decoding Algorithm

**Algorithm: UTF-8 → Unicode Code Point**

```
Input: Byte sequence (array of bytes)
Output: Unicode code point U

FUNCTION utf8_to_unicode(bytes, position):
    byte1 = bytes[position]
    
    // 1-byte sequence (ASCII)
    IF (byte1 & 0x80) == 0x00:
        U = byte1
        RETURN (U, 1)  // Return code point and bytes consumed
    
    // 2-byte sequence
    ELSE IF (byte1 & 0xE0) == 0xC0:
        IF position + 1 >= length(bytes):
            ERROR: "Incomplete UTF-8 sequence"
        
        byte2 = bytes[position + 1]
        IF (byte2 & 0xC0) != 0x80:
            ERROR: "Invalid continuation byte"
        
        U = ((byte1 & 0x1F) << 6) | (byte2 & 0x3F)
        
        // Check for overlong encoding
        IF U < 0x80:
            ERROR: "Overlong encoding"
        
        RETURN (U, 2)
    
    // 3-byte sequence
    ELSE IF (byte1 & 0xF0) == 0xE0:
        IF position + 2 >= length(bytes):
            ERROR: "Incomplete UTF-8 sequence"
        
        byte2 = bytes[position + 1]
        byte3 = bytes[position + 2]
        
        IF (byte2 & 0xC0) != 0x80 OR (byte3 & 0xC0) != 0x80:
            ERROR: "Invalid continuation byte"
        
        U = ((byte1 & 0x0F) << 12) | ((byte2 & 0x3F) << 6) | (byte3 & 0x3F)
        
        // Check for overlong encoding and surrogates
        IF U < 0x800:
            ERROR: "Overlong encoding"
        IF U >= 0xD800 AND U <= 0xDFFF:
            ERROR: "UTF-8 encoded surrogate"
        
        RETURN (U, 3)
    
    // 4-byte sequence
    ELSE IF (byte1 & 0xF8) == 0xF0:
        IF position + 3 >= length(bytes):
            ERROR: "Incomplete UTF-8 sequence"
        
        byte2 = bytes[position + 1]
        byte3 = bytes[position + 2]
        byte4 = bytes[position + 3]
        
        IF (byte2 & 0xC0) != 0x80 OR (byte3 & 0xC0) != 0x80 OR (byte4 & 0xC0) != 0x80:
            ERROR: "Invalid continuation byte"
        
        U = ((byte1 & 0x07) << 18) | ((byte2 & 0x3F) << 12) | 
            ((byte3 & 0x3F) << 6) | (byte4 & 0x3F)
        
        // Check for overlong encoding and valid range
        IF U < 0x10000:
            ERROR: "Overlong encoding"
        IF U > 0x10FFFF:
            ERROR: "Code point out of Unicode range"
        
        RETURN (U, 4)
    
    ELSE:
        ERROR: "Invalid UTF-8 start byte"
END FUNCTION
```

**What is an "overlong encoding"?** It is when you use more bytes than necessary to encode a code point. For example, the character "A" (U+0041) can be encoded in 1 byte as `01000001`. But you could also illegally encode it in 2 bytes as `11000001 10000001`, which decodes to the same value. This is forbidden because it would create two different byte sequences for the same character, breaking the "unambiguous" guarantee. The overlong checks in the algorithm prevent this.

### 5.5 UTF-8 Example: Telugu Character "అ" (U+0C05)

```
Code Point: U+0C05 (decimal: 3077)

Step 1: Determine byte count
3077 is in range 0x0800 to 0xFFFF → 3-byte sequence

Step 2: Extract bits
U+0C05 = 0000 1100 0000 0101 (binary)
         aaaa bbbbbb cccccc (group into 4, 6, 6 bits)
         0000 110000 000101

Step 3: Create UTF-8 bytes
Byte 1: 1110aaaa = 11100000 = 0xE0
Byte 2: 10bbbbbb = 10110000 = 0xB0
Byte 3: 10cccccc = 10000101 = 0x85

Result: 0xE0 0xB0 0x85 (3 bytes in UTF-8)
```

**Verification**:
```
Decode: 
Byte 1: 11100000 → header bits (1110), data bits (0000)
Byte 2: 10110000 → header bits (10), data bits (110000)
Byte 3: 10000101 → header bits (10), data bits (000101)

Combine: 0000 110000 000101 = 0000 1100 0000 0101 = 0x0C05 ✓
```

**Full dry run with all number bases for "అ" (U+0C05):**

```
Code Point: U+0C05
├── Decimal:     3077
├── Binary:      0000 1100 0000 0101
├── Octal:       6005
└── Hexadecimal: 0C05

UTF-8 Bytes (each shown in all bases):
  Byte 1: 0xE0
  ├── Hex:     E0
  ├── Decimal: 224
  ├── Binary:  1110 0000
  └── Octal:   340

  Byte 2: 0xB0
  ├── Hex:     B0
  ├── Decimal: 176
  ├── Binary:  1011 0000
  └── Octal:   260

  Byte 3: 0x85
  ├── Hex:     85
  ├── Decimal: 133
  ├── Binary:  1000 0101
  └── Octal:   205

  In C string literal (octal escapes): "\340\260\205"
  In C string literal (hex escapes):   "\xE0\xB0\x85"
```

### 5.6 Additional UTF-8 Encoding Dry Runs

**Dry Run 1: Latin Letter "A" (U+0041) — 1-byte case**

```
Code Point: U+0041 (decimal: 65)
Range check: 65 is in 0x00–0x7F → 1-byte sequence

Binary: 0100 0001
Pattern: 0xxxxxxx → just use the byte as-is

Byte 1: 0100 0001 = 0x41

Result: [0x41]

All bases:
  Code Point: Hex 0041, Dec 65, Bin 01000001, Oct 101
  UTF-8 Byte: Hex 41,   Dec 65, Bin 01000001, Oct 101

  Note: For ASCII, the code point value IS the UTF-8 byte. They are identical.
```

**Dry Run 2: Euro Sign "€" (U+20AC) — 3-byte case**

```
Code Point: U+20AC (decimal: 8364)
Range check: 8364 is in 0x0800–0xFFFF → 3-byte sequence

Binary of 0x20AC:
  2 → 0010
  0 → 0000
  A → 1010
  C → 1100
  Full: 0010 0000 1010 1100

Group into 4-6-6 bits:
  0010 000010 101100

Byte 1: 1110 0010 = 0xE2
Byte 2: 10 000010 = 0x82
Byte 3: 10 101100 = 0xAC

Result: [0xE2, 0x82, 0xAC]

Verification (decode back):
  Strip headers: 0010 | 000010 | 101100
  Combine:       0010 0000 1010 1100 = 0x20AC ✓

All bases for each byte:
  Byte 1 (0xE2): Dec 226, Bin 11100010, Oct 342
  Byte 2 (0x82): Dec 130, Bin 10000010, Oct 202
  Byte 3 (0xAC): Dec 172, Bin 10101100, Oct 254
```

**Dry Run 3: Devanagari "क" (U+0915) — another 3-byte case, different script**

```
Code Point: U+0915 (decimal: 2325)
Range check: 2325 is in 0x0800–0xFFFF → 3-byte sequence

Binary of 0x0915:
  0 → 0000
  9 → 1001
  1 → 0001
  5 → 0101
  Full: 0000 1001 0001 0101

Group into 4-6-6 bits:
  0000 100100 010101

Byte 1: 1110 0000 = 0xE0
Byte 2: 10 100100 = 0xA4
Byte 3: 10 010101 = 0x95

Result: [0xE0, 0xA4, 0x95]

Verification:
  Strip headers: 0000 | 100100 | 010101
  Combine:       0000 1001 0001 0101 = 0x0915 ✓
```

**Dry Run 4: Emoji "😀" (U+1F600) — 4-byte case**

```
Code Point: U+1F600 (decimal: 128512)
Range check: 128512 is in 0x10000–0x10FFFF → 4-byte sequence

Binary of 0x1F600:
  1 → 0001
  F → 1111
  6 → 0110
  0 → 0000
  0 → 0000
  Full: 0 0001 1111 0110 0000 0000 (pad to 21 bits)
      = 000 011111 011000 000000

Group into 3-6-6-6 bits:
  000 011111 011000 000000

Byte 1: 11110 000 = 0xF0
Byte 2: 10 011111 = 0x9F
Byte 3: 10 011000 = 0x98
Byte 4: 10 000000 = 0x80

Result: [0xF0, 0x9F, 0x98, 0x80]

Verification:
  Strip headers: 000 | 011111 | 011000 | 000000
  Combine:       000 011111 011000 000000
               = 0 0001 1111 0110 0000 0000 = 0x1F600 ✓

All bases for each byte:
  Byte 1 (0xF0): Dec 240, Bin 11110000, Oct 360
  Byte 2 (0x9F): Dec 159, Bin 10011111, Oct 237
  Byte 3 (0x98): Dec 152, Bin 10011000, Oct 230
  Byte 4 (0x80): Dec 128, Bin 10000000, Oct 200
```

**Dry Run 5: Telugu Vowel Sign "ు" (U+0C41) — 3-byte case**

```
Code Point: U+0C41 (decimal: 3137)
Range check: 3137 is in 0x0800–0xFFFF → 3-byte sequence

Binary of 0x0C41:
  0 → 0000
  C → 1100
  4 → 0100
  1 → 0001
  Full: 0000 1100 0100 0001

Group into 4-6-6 bits:
  0000 110001 000001

Byte 1: 1110 0000 = 0xE0
Byte 2: 10 110001 = 0xB1
Byte 3: 10 000001 = 0x81

Result: [0xE0, 0xB1, 0x81]

Verification:
  Strip headers: 0000 | 110001 | 000001
  Combine:       0000 1100 0100 0001 = 0x0C41 ✓

All bases:
  Byte 1 (0xE0): Dec 224, Bin 11100000, Oct 340
  Byte 2 (0xB1): Dec 177, Bin 10110001, Oct 261
  Byte 3 (0x81): Dec 129, Bin 10000001, Oct 201
```

**Dry Run 6: Telugu Virama "్" (U+0C4D) — 3-byte case**

```
Code Point: U+0C4D (decimal: 3149)
Range check: 3149 is in 0x0800–0xFFFF → 3-byte sequence

Binary of 0x0C4D:
  0 → 0000
  C → 1100
  4 → 0100
  D → 1101
  Full: 0000 1100 0100 1101

Group into 4-6-6 bits:
  0000 110001 001101

Byte 1: 1110 0000 = 0xE0
Byte 2: 10 110001 = 0xB1
Byte 3: 10 001101 = 0x8D

Result: [0xE0, 0xB1, 0x8D]

Verification:
  Strip headers: 0000 | 110001 | 001101
  Combine:       0000 1100 0100 1101 = 0x0C4D ✓
```

**Dry Run 7: Latin Small Letter "é" (U+00E9) — 2-byte case**

```
Code Point: U+00E9 (decimal: 233)
Range check: 233 is in 0x0080–0x07FF → 2-byte sequence

Binary of 0x00E9:
  E → 1110
  9 → 1001
  Full (11 bits): 000 1110 1001

Group into 5-6 bits:
  00011 101001

Byte 1: 110 00011 = 0xC3
Byte 2: 10 101001 = 0xA9

Result: [0xC3, 0xA9]

Verification:
  Strip headers: 00011 | 101001
  Combine:       00011 101001 = 0000 1110 1001 = 0xE9 ✓

All bases:
  Byte 1 (0xC3): Dec 195, Bin 11000011, Oct 303
  Byte 2 (0xA9): Dec 169, Bin 10101001, Oct 251
```

---

## 6. UTF-16 Encoding

### 6.1 UTF-16 Design Principles

UTF-16 (16-bit Unicode Transformation Format) is a variable-length encoding using 16-bit code units:

**Key Properties**:
1. **Variable Length**: 2 or 4 bytes per character
2. **Efficient for BMP**: Single 16-bit unit for most common characters
3. **Surrogate Pairs**: Two 16-bit units for characters beyond BMP
4. **Widely Used**: Internal representation in Windows, Java, JavaScript

### 6.2 UTF-16 Encoding Structure

```
Code Point Range         | Code Units | Representation
-------------------------|------------|------------------
U+0000   to U+D7FF       | 1          | Direct mapping
U+D800   to U+DFFF       | Invalid    | Reserved for surrogates
U+E000   to U+FFFF       | 1          | Direct mapping
U+10000  to U+10FFFF     | 2          | Surrogate pair
```

### 6.3 Basic Multilingual Plane (BMP) Encoding

For code points U+0000 to U+FFFF (excluding U+D800 to U+DFFF):
- **Direct Mapping**: Code point value = UTF-16 code unit value
- **Example**: U+0C05 (Telugu అ) → UTF-16: 0x0C05

This is the simplest possible encoding: the 16-bit code unit is just the code point number itself. No transformation is needed.

### 6.4 Surrogate Pairs for Supplementary Planes

For code points U+10000 to U+10FFFF:

**Surrogate Pair Formula**:
```
Code Point U (U >= 0x10000):

Step 1: Subtract 0x10000 from U
    U' = U - 0x10000

Step 2: Split U' into high 10 bits and low 10 bits
    High10 = (U' >> 10) & 0x3FF
    Low10  = U' & 0x3FF

Step 3: Create surrogate pair
    HighSurrogate = 0xD800 + High10  (range: 0xD800-0xDBFF)
    LowSurrogate  = 0xDC00 + Low10   (range: 0xDC00-0xDFFF)

Result: [HighSurrogate, LowSurrogate]
```

**Why subtract 0x10000?** The supplementary planes start at U+10000. By subtracting 0x10000, we get a value starting from 0. This adjusted value (U') ranges from 0 to 0xFFFFF (20 bits). We then split those 20 bits into two 10-bit halves, each of which fits into the 10 available bits in a surrogate code unit.

**Why 10 bits each?** The high surrogate range is 0xD800–0xDBFF, which spans exactly 1024 values (0x400 = 2^10). The low surrogate range is 0xDC00–0xDFFF, also 1024 values. So each surrogate carries 10 bits of payload.

**Surrogate Ranges**:
- **High Surrogates**: 0xD800 to 0xDBFF (1,024 values)
- **Low Surrogates**: 0xDC00 to 0xDFFF (1,024 values)
- **Total Combinations**: 1,024 × 1,024 = 1,048,576 code points

### 6.5 UTF-16 Encoding Algorithm

**Algorithm: Unicode Code Point → UTF-16**

```
Input: Unicode code point U
Output: UTF-16 code unit(s)

FUNCTION unicode_to_utf16(U):
    // BMP characters (excluding surrogates)
    IF U >= 0x0000 AND U <= 0xD7FF:
        RETURN [U]
    
    ELSE IF U >= 0xE000 AND U <= 0xFFFF:
        RETURN [U]
    
    // Surrogate range (invalid)
    ELSE IF U >= 0xD800 AND U <= 0xDFFF:
        ERROR: "Surrogate code points cannot be encoded"
    
    // Supplementary planes
    ELSE IF U >= 0x10000 AND U <= 0x10FFFF:
        // Subtract 0x10000
        U_prime = U - 0x10000
        
        // Extract high and low 10 bits
        high10 = (U_prime >> 10) & 0x3FF
        low10  = U_prime & 0x3FF
        
        // Create surrogate pair
        high_surrogate = 0xD800 | high10
        low_surrogate  = 0xDC00 | low10
        
        RETURN [high_surrogate, low_surrogate]
    
    ELSE:
        ERROR: "Invalid Unicode code point"
END FUNCTION
```

### 6.6 UTF-16 Decoding Algorithm

**Algorithm: UTF-16 → Unicode Code Point**

```
Input: UTF-16 code units array, position
Output: Unicode code point U

FUNCTION utf16_to_unicode(code_units, position):
    unit1 = code_units[position]
    
    // BMP character (not a surrogate)
    IF unit1 < 0xD800 OR unit1 > 0xDFFF:
        RETURN (unit1, 1)  // Return code point and units consumed
    
    // High surrogate (start of pair)
    ELSE IF unit1 >= 0xD800 AND unit1 <= 0xDBFF:
        IF position + 1 >= length(code_units):
            ERROR: "Incomplete surrogate pair"
        
        unit2 = code_units[position + 1]
        
        // Verify low surrogate
        IF unit2 < 0xDC00 OR unit2 > 0xDFFF:
            ERROR: "Invalid surrogate pair"
        
        // Decode surrogate pair
        high10 = unit1 - 0xD800
        low10  = unit2 - 0xDC00
        
        U = 0x10000 + (high10 << 10) + low10
        
        RETURN (U, 2)
    
    // Low surrogate (invalid without high surrogate)
    ELSE:
        ERROR: "Unpaired low surrogate"
END FUNCTION
```

### 6.7 UTF-16 Example: Emoji "😀" (U+1F600)

```
Code Point: U+1F600 (decimal: 128,512)

Step 1: This is in supplementary plane (U > 0xFFFF)

Step 2: Subtract 0x10000
U' = 0x1F600 - 0x10000 = 0x0F600 (decimal: 62,976)

Step 3: Convert to binary
0x0F600 = 0000 1111 0110 0000 0000 (20 bits)

Step 4: Split into high 10 bits and low 10 bits
High10 = 00 0011 1101 = 0x03D
Low10  = 10 0000 0000 = 0x200

Step 5: Create surrogates
High Surrogate = 0xD800 + 0x03D = 0xD83D
Low Surrogate  = 0xDC00 + 0x200 = 0xDE00

Result: 0xD83D 0xDE00 (surrogate pair)
```

**Verification**:
```
Decode:
High: 0xD83D - 0xD800 = 0x03D
Low:  0xDE00 - 0xDC00 = 0x200

Combine: (0x03D << 10) + 0x200 = 0x0F600
Add base: 0x0F600 + 0x10000 = 0x1F600 ✓
```

### 6.8 Additional UTF-16 Dry Runs

**Dry Run 1: Telugu "అ" (U+0C05) — BMP direct mapping**

```
Code Point: U+0C05 (decimal: 3077)
Range check: 0x0C05 < 0xD800 → BMP, direct mapping

UTF-16 code unit: 0x0C05 (same as code point)

In bytes:
  Big-Endian (UTF-16BE):    0C 05
  Little-Endian (UTF-16LE): 05 0C

All bases for the code unit 0x0C05:
  Hex:     0C05
  Decimal: 3077
  Binary:  0000 1100 0000 0101
  Octal:   6005

No surrogate pair needed — BMP characters map directly.
```

**Dry Run 2: Musical Symbol "𝄞" (U+1D11E) — surrogate pair case**

```
Code Point: U+1D11E (decimal: 119070)
Range check: 0x1D11E > 0xFFFF → supplementary plane, needs surrogate pair

Step 1: U' = 0x1D11E - 0x10000 = 0x0D11E (decimal: 53534)

Step 2: Convert U' to binary (20 bits):
  0x0D11E:
  0 → 0000
  D → 1101
  1 → 0001
  1 → 0001
  E → 1110
  Full: 0000 1101 0001 0001 1110
  As 20 bits: 00 0011 0100 0100 0111 10

  Wait — let us be more careful:
  0x0D11E = 0×16^4 + D×16^3 + 1×16^2 + 1×16^1 + E×16^0
          = 0 + 13×4096 + 1×256 + 1×16 + 14
          = 53248 + 256 + 16 + 14 = 53534

  53534 in binary (divide by 2 repeatedly):
  53534 → 26767 r0 → 13383 r1 → 6691 r1 → 3345 r1 → 1672 r1
  1672 → 836 r0 → 418 r0 → 209 r0 → 104 r1 → 52 r0
  52 → 26 r0 → 13 r0 → 6 r1 → 3 r0 → 1 r1 → 0 r1

  Read bottom-to-top: 1101 0001 0001 1110
  Pad to 20 bits:     00 0011 0100 0100 0111 10

  Actually, let us use the hex-to-binary shortcut:
  0 → 0000
  D → 1101
  1 → 0001
  1 → 0001
  E → 1110
  Concatenate: 0000 1101 0001 0001 1110 (20 bits)

Step 3: Split into high 10 and low 10:
  High 10: 00 0011 0100 = 0x034 (decimal: 52)
  Low 10:  01 0001 1110 = 0x11E (decimal: 286)

Step 4: Create surrogates:
  High Surrogate = 0xD800 + 0x034 = 0xD834
  Low Surrogate  = 0xDC00 + 0x11E = 0xDD1E

Result: [0xD834, 0xDD1E]

Verification:
  High: 0xD834 - 0xD800 = 0x034
  Low:  0xDD1E - 0xDC00 = 0x11E
  Combine: (0x034 << 10) + 0x11E = 0xD000 + 0x11E = 0xD11E
  Add base: 0xD11E + 0x10000 = 0x1D11E ✓

In bytes (Big-Endian): D8 34 DD 1E
In bytes (Little-Endian): 34 D8 1E DD
```

**Dry Run 3: Supplementary Ideograph (U+20000) — first character in SIP**

```
Code Point: U+20000 (decimal: 131072)
Range check: 0x20000 > 0xFFFF → surrogate pair needed

Step 1: U' = 0x20000 - 0x10000 = 0x10000 (decimal: 65536)

Step 2: Binary of 0x10000 (20 bits):
  1 → 0001, 0 → 0000, 0 → 0000, 0 → 0000, 0 → 0000
  → 0001 0000 0000 0000 0000 (20 bits)

Step 3: Split into high 10 and low 10:
  High 10: 00 0100 0000 = 0x040 (decimal: 64)
  Low 10:  00 0000 0000 = 0x000 (decimal: 0)

Step 4: Create surrogates:
  High Surrogate = 0xD800 + 0x040 = 0xD840
  Low Surrogate  = 0xDC00 + 0x000 = 0xDC00

Result: [0xD840, 0xDC00]

Verification:
  High: 0xD840 - 0xD800 = 0x040
  Low:  0xDC00 - 0xDC00 = 0x000
  Combine: (0x040 << 10) + 0x000 = 0x10000
  Add base: 0x10000 + 0x10000 = 0x20000 ✓
```

**Dry Run 4: Last valid Unicode code point (U+10FFFF)**

```
Code Point: U+10FFFF (decimal: 1114111)
Range check: > 0xFFFF → surrogate pair needed

Step 1: U' = 0x10FFFF - 0x10000 = 0x0FFFFF (decimal: 1048575)

Step 2: Binary of 0x0FFFFF (20 bits):
  0 → 0000, F → 1111, F → 1111, F → 1111, F → 1111
  → 0000 1111 1111 1111 1111 (20 bits)
  As 20 bits: 11 1111 1111 1111 1111

  Actually: 0x0FFFFF = 0×16^4 + F×16^3 + F×16^2 + F×16^1 + F×16^0
  In binary nibbles: 0000 1111 1111 1111 1111
  Take the lower 20 bits: 1111 1111 1111 1111 1111

Step 3: Split into high 10 and low 10:
  High 10: 11 1111 1111 = 0x3FF (decimal: 1023)
  Low 10:  11 1111 1111 = 0x3FF (decimal: 1023)

Step 4: Create surrogates:
  High Surrogate = 0xD800 + 0x3FF = 0xDBFF  ← maximum high surrogate
  Low Surrogate  = 0xDC00 + 0x3FF = 0xDFFF  ← maximum low surrogate

Result: [0xDBFF, 0xDFFF]

This confirms: the surrogate ranges 0xD800–0xDBFF and 0xDC00–0xDFFF
are fully utilized, and 1024 × 1024 = 1,048,576 supplementary
code points can be encoded.

Verification:
  High: 0xDBFF - 0xD800 = 0x3FF
  Low:  0xDFFF - 0xDC00 = 0x3FF
  Combine: (0x3FF << 10) + 0x3FF = 0xFFC00 + 0x3FF = 0xFFFFF
  Add base: 0xFFFFF + 0x10000 = 0x10FFFF ✓
```

---

## 7. Endianness and Byte Order

### 7.1 Understanding Endianness

Endianness refers to the order in which bytes are stored in memory for multi-byte data types.

**Origin**: The term comes from Jonathan Swift's "Gulliver's Travels" (1726), referring to which end of an egg should be cracked first.

### 7.2 Big-Endian vs Little-Endian

```
Consider the 32-bit number: 0x12345678

Memory Address:    0x00    0x01    0x02    0x03
Big-Endian:        0x12    0x34    0x56    0x78
Little-Endian:     0x78    0x56    0x34    0x12

Most Significant Byte (MSB): 0x12
Least Significant Byte (LSB): 0x78
```

A helpful way to remember: **Big-Endian** stores the **B**ig end (most significant byte) first, at the lowest memory address. **Little-Endian** stores the **L**ittle end (least significant byte) first.

**Big-Endian** (Network Byte Order):
- Most significant byte stored at lowest address
- "Natural" reading order (left to right)
- Used by: Network protocols, Motorola, SPARC, PowerPC
- Example: 0x1234 → Memory[0]=0x12, Memory[1]=0x34

**Little-Endian**:
- Least significant byte stored at lowest address
- "Reversed" reading order
- Used by: x86, x86-64 (Intel/AMD), ARM (configurable)
- Example: 0x1234 → Memory[0]=0x34, Memory[1]=0x12

**Dry Run: Storing 0x0C05 (Telugu "అ") in memory under both endiannesses**

```
Value: 0x0C05 (16-bit)
High byte: 0x0C
Low byte:  0x05

Big-Endian layout (starting at address 0x2000):
  Address 0x2000: 0x0C  ← high byte first
  Address 0x2001: 0x05  ← low byte second
  Read left-to-right as hex: 0C 05 → 0x0C05 ✓

Little-Endian layout (starting at address 0x2000):
  Address 0x2000: 0x05  ← low byte first
  Address 0x2001: 0x0C  ← high byte second
  Read left-to-right as hex: 05 0C → looks like 0x050C, but
  the CPU knows to interpret it as 0x0C05 ✓
```

### 7.3 Endianness in UTF-16

UTF-16 uses 16-bit (2-byte) code units, so byte order matters.

**Example: Telugu "అ" (U+0C05)**

```
Code Point: U+0C05
Binary: 0000 1100 0000 0101
Hex: 0x0C 0x05

Big-Endian (UTF-16BE):
Memory[0] = 0x0C (higher byte first)
Memory[1] = 0x05

Little-Endian (UTF-16LE):
Memory[0] = 0x05 (lower byte first)
Memory[1] = 0x0C
```

### 7.4 Byte Order Mark (BOM)

The **Byte Order Mark** (U+FEFF) is a special Unicode character used to:
1. Indicate the encoding scheme (UTF-8, UTF-16, UTF-32)
2. Specify byte order (big-endian or little-endian)

**BOM Values**:

| Encoding | BOM Bytes | Hex |
|----------|-----------|-----|
| UTF-8 | EF BB BF | 0xEFBBBF |
| UTF-16 BE | FE FF | 0xFEFF |
| UTF-16 LE | FF FE | 0xFFFE |
| UTF-32 BE | 00 00 FE FF | 0x0000FEFF |
| UTF-32 LE | FF FE 00 00 | 0xFFFE0000 |

**Why does the BOM look different in BE vs LE?** The BOM character is always U+FEFF. In Big-Endian, it is stored as bytes `FE FF` (high byte first). In Little-Endian, it is stored as bytes `FF FE` (low byte first). So if you see `FF FE` at the start of a file, you know it is Little-Endian. If you see `FE FF`, it is Big-Endian. The byte order itself tells you the byte order — that is the clever trick.

**BOM Detection Algorithm**:

```
Input: First 2-4 bytes of file
Output: Encoding and byte order

FUNCTION detect_bom(bytes):
    // Check UTF-8 BOM (3 bytes)
    IF bytes[0:3] == [0xEF, 0xBB, 0xBF]:
        RETURN ("UTF-8", None, 3)
    
    // Check UTF-32 (4 bytes needed)
    IF length(bytes) >= 4:
        IF bytes[0:4] == [0x00, 0x00, 0xFE, 0xFF]:
            RETURN ("UTF-32", "BE", 4)
        IF bytes[0:4] == [0xFF, 0xFE, 0x00, 0x00]:
            RETURN ("UTF-32", "LE", 4)
    
    // Check UTF-16 (2 bytes)
    IF bytes[0:2] == [0xFE, 0xFF]:
        RETURN ("UTF-16", "BE", 2)
    IF bytes[0:2] == [0xFF, 0xFE]:
        RETURN ("UTF-16", "LE", 2)
    
    // No BOM detected
    RETURN (None, None, 0)
END FUNCTION
```

**Dry Run of BOM Detection:**

```
Example 1: File starts with bytes [0xFF, 0xFE, 0x05, 0x0C, ...]

  Check UTF-8 BOM: [0xFF, 0xFE, 0x05] ≠ [0xEF, 0xBB, 0xBF] → No
  Check UTF-32 LE: [0xFF, 0xFE, 0x05, 0x0C] ≠ [0xFF, 0xFE, 0x00, 0x00] → No
  Check UTF-32 BE: [0xFF, 0xFE, 0x05, 0x0C] ≠ [0x00, 0x00, 0xFE, 0xFF] → No
  Check UTF-16 BE: [0xFF, 0xFE] ≠ [0xFE, 0xFF] → No
  Check UTF-16 LE: [0xFF, 0xFE] == [0xFF, 0xFE] → YES!
  
  Result: ("UTF-16", "LE", 2)
  → Skip first 2 bytes (BOM), then read remaining as UTF-16LE.
  → Next bytes [0x05, 0x0C] in LE = code unit 0x0C05 = Telugu "అ"

Example 2: File starts with bytes [0xEF, 0xBB, 0xBF, 0xE0, 0xB0, 0x85, ...]

  Check UTF-8 BOM: [0xEF, 0xBB, 0xBF] == [0xEF, 0xBB, 0xBF] → YES!
  
  Result: ("UTF-8", None, 3)
  → Skip first 3 bytes (BOM), then read remaining as UTF-8.
  → Next bytes [0xE0, 0xB0, 0x85] = Telugu "అ" in UTF-8
```

**Important Notes**:
- UTF-8 BOM is **optional** and **not recommended** (breaks ASCII compatibility)
- UTF-16 and UTF-32 BOMs are **recommended** for disambiguation
- If no BOM: UTF-16 defaults to **big-endian** per RFC 2781
- BOM should **not** be displayed as a visible character

### 7.5 UTF-16 with Endianness Example

**Example: Telugu word "తెలుగు" (Telugu)**

```
Characters: త (U+0C24), ె (U+0C46), ల (U+0C32), ు (U+0C41), గ (U+0C17), ు (U+0C41)

UTF-16 Code Points:
0x0C24, 0x0C46, 0x0C32, 0x0C41, 0x0C17, 0x0C41

UTF-16BE (Big-Endian):
FE FF  0C 24  0C 46  0C 32  0C 41  0C 17  0C 41
^BOM   ^త     ^ె     ^ల     ^ు     ^గ     ^ు

UTF-16LE (Little-Endian):
FF FE  24 0C  46 0C  32 0C  41 0C  17 0C  41 0C
^BOM   ^త     ^ె     ^ల     ^ు     ^గ     ^ు
```

### 7.6 Why UTF-8 Doesn't Need Endianness

UTF-8 is byte-oriented:
- Each code unit is exactly 1 byte (8 bits)
- No ambiguity in byte order
- Multi-byte sequences are explicitly ordered by the encoding scheme
- UTF-8 BOM (if present) is only for encoding identification, not byte order

**Example: "అ" (U+0C05) in UTF-8**
```
UTF-8: E0 B0 85
This sequence is the SAME regardless of processor architecture
No ambiguity about which byte comes first
```

---

## 8. Telugu Script in Unicode

### 8.1 Telugu Unicode Block

**Range**: U+0C00 to U+0C7F (128 code points)
**Plane**: Basic Multilingual Plane (BMP)
**Script**: Telugu

The Telugu Unicode block contains:
- Independent vowels (స్వరాలు)
- Consonants (హల్లులు)
- Dependent vowel signs (gunintamulu)
- Virama/Halant (combining character)
- Special symbols and digits

### 8.2 Telugu Character Categories

```
┌─────────────────────────────────────────────────┐
│              Telugu Unicode Block               │
│               U+0C00 - U+0C7F                   │
├─────────────────────────────────────────────────┤
│ U+0C00-U+0C04 │ Combining Signs                │
│ U+0C05-U+0C14 │ Independent Vowels             │
│ U+0C15-U+0C39 │ Consonants                     │
│ U+0C3D        │ Sign Avagraha                  │
│ U+0C3E-U+0C4C │ Dependent Vowel Signs          │
│ U+0C4D        │ Sign Virama (halant)           │
│ U+0C55-U+0C56 │ Length Marks                   │
│ U+0C58-U+0C5A │ Additional Consonants          │
│ U+0C60-U+0C63 │ Vocalic R and L                │
│ U+0C66-U+0C6F │ Telugu Digits (0-9)            │
│ U+0C77-U+0C7F │ Signs and Symbols              │
└─────────────────────────────────────────────────┘
```

### 8.3 Sample Telugu Character Encodings

| Char | Unicode | Name | UTF-8 | UTF-16BE | UTF-16LE |
|------|---------|------|-------|----------|----------|
| అ | U+0C05 | TELUGU LETTER A | E0 B0 85 | 0C 05 | 05 0C |
| క | U+0C15 | TELUGU LETTER KA | E0 B0 95 | 0C 15 | 15 0C |
| త | U+0C24 | TELUGU LETTER TA | E0 B0 A4 | 0C 24 | 24 0C |
| న | U+0C28 | TELUGU LETTER NA | E0 B0 A8 | 0C 28 | 28 0C |
| మ | U+0C2E | TELUGU LETTER MA | E0 B0 AE | 0C 2E | 2E 0C |
| ్ | U+0C4D | TELUGU SIGN VIRAMA | E0 B1 8D | 0C 4D | 4D 0C |
| ా | U+0C3E | TELUGU VOWEL SIGN AA | E0 B0 BE | 0C 3E | 3E 0C |
| ి | U+0C3F | TELUGU VOWEL SIGN I | E0 B0 BF | 0C 3F | 3F 0C |
| ు | U+0C41 | TELUGU VOWEL SIGN U | E0 B1 81 | 0C 41 | 41 0C |
| ౦ | U+0C66 | TELUGU DIGIT ZERO | E0 B1 A6 | 0C 66 | 66 0C |
| ౯ | U+0C6F | TELUGU DIGIT NINE | E0 B1 AF | 0C 6F | 6F 0C |

**Extended encoding table with all number bases:**

| Char | Unicode | Decimal | Binary | Octal | UTF-8 Bytes | UTF-8 Octal Escapes |
|------|---------|---------|--------|-------|-------------|---------------------|
| అ | U+0C05 | 3077 | 0000 1100 0000 0101 | 6005 | E0 B0 85 | \340\260\205 |
| ఆ | U+0C06 | 3078 | 0000 1100 0000 0110 | 6006 | E0 B0 86 | \340\260\206 |
| ఇ | U+0C07 | 3079 | 0000 1100 0000 0111 | 6007 | E0 B0 87 | \340\260\207 |
| ఈ | U+0C08 | 3080 | 0000 1100 0000 1000 | 6010 | E0 B0 88 | \340\260\210 |
| ఉ | U+0C09 | 3081 | 0000 1100 0000 1001 | 6011 | E0 B0 89 | \340\260\211 |
| ఊ | U+0C0A | 3082 | 0000 1100 0000 1010 | 6012 | E0 B0 8A | \340\260\212 |
| క | U+0C15 | 3093 | 0000 1100 0001 0101 | 6025 | E0 B0 95 | \340\260\225 |
| ఖ | U+0C16 | 3094 | 0000 1100 0001 0110 | 6026 | E0 B0 96 | \340\260\226 |
| గ | U+0C17 | 3095 | 0000 1100 0001 0111 | 6027 | E0 B0 97 | \340\260\227 |
| ఘ | U+0C18 | 3096 | 0000 1100 0001 1000 | 6030 | E0 B0 98 | \340\260\230 |
| ఙ | U+0C19 | 3097 | 0000 1100 0001 1001 | 6031 | E0 B0 99 | \340\260\231 |
| ై | U+0C48 | 3144 | 0000 1100 0100 1000 | 6110 | E0 B1 88 | \340\261\210 |
| ్ | U+0C4D | 3149 | 0000 1100 0100 1101 | 6115 | E0 B1 8D | \340\261\215 |
| ౦ | U+0C66 | 3174 | 0000 1100 0110 0110 | 6146 | E0 B1 A6 | \340\261\246 |
| ౧ | U+0C67 | 3175 | 0000 1100 0110 0111 | 6147 | E0 B1 A7 | \340\261\247 |
| ౨ | U+0C68 | 3176 | 0000 1100 0110 1000 | 6150 | E0 B1 A8 | \340\261\250 |
| ౯ | U+0C6F | 3183 | 0000 1100 0110 1111 | 6157 | E0 B1 AF | \340\261\257 |

### 8.4 Complex Telugu Character Formation

Telugu is an **abugida** (alphasyllabary) where consonant-vowel sequences combine:

**Example: "కా" (kā)**
```
Base: క (ka) = U+0C15
Vowel Sign: ా (AA) = U+0C3E
Rendered: కా

Storage:
- Code Points: U+0C15 U+0C3E (2 code points)
- UTF-8: E0 B0 95 E0 B0 BE (6 bytes)
- UTF-16BE: 0C 15 0C 3E (4 bytes)
```

**Example: "క్త" (kta with virama)**
```
Consonant 1: క (ka) = U+0C15
Virama: ్ = U+0C4D
Consonant 2: త (ta) = U+0C24

Storage:
- Code Points: U+0C15 U+0C4D U+0C24 (3 code points)
- UTF-8: E0 B0 95 E0 B1 8D E0 B0 A4 (9 bytes)
- UTF-16BE: 0C 15 0C 4D 0C 24 (6 bytes)
```

**Detailed byte-level breakdown of "కా":**

```
Character 1: క (U+0C15)
  Code point binary: 0000 1100 0001 0101
  UTF-8 grouping:    0000 | 110000 | 010101
  Byte 1: 1110 0000 = 0xE0 (Dec 224, Oct 340)
  Byte 2: 10 110000 = 0xB0 (Dec 176, Oct 260)
  Byte 3: 10 010101 = 0x95 (Dec 149, Oct 225)

Character 2: ా (U+0C3E)
  Code point binary: 0000 1100 0011 1110
  UTF-8 grouping:    0000 | 110000 | 111110
  Byte 4: 1110 0000 = 0xE0 (Dec 224, Oct 340)
  Byte 5: 10 110000 = 0xB0 (Dec 176, Oct 260)
  Byte 6: 10 111110 = 0xBE (Dec 190, Oct 276)

Complete UTF-8 byte stream: E0 B0 95 E0 B0 BE
In octal escapes: \340\260\225\340\260\276
In decimal bytes: 224 176 149 224 176 190
```

### 8.5 Telugu Text Rendering Process

```
┌─────────────────────┐
│   Unicode Input     │
│   (Code Points)     │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Normalization      │
│  (NFC, NFD, etc.)   │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Script Shaping     │
│  (OpenType/AAT)     │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Glyph Selection    │
│  (Font Tables)      │
└──────────┬──────────┘
           │
           ↓
┌─────────────────────┐
│  Rendering          │
│  (Screen/Print)     │
└─────────────────────┘
```

**Key Points**:
1. **Unicode**: Stores logical order of characters
2. **Shaping**: Combines characters into ligatures
3. **Font**: Provides visual glyphs
4. **Rendering**: Displays on screen

---

## 9. Conversion Algorithms

### 9.1 Unicode to UTF-8 Conversion (Complete)

```python
def unicode_to_utf8(codepoint):
    """
    Convert Unicode code point to UTF-8 byte sequence.
    
    Args:
        codepoint: Integer Unicode code point (0x0 to 0x10FFFF)
    
    Returns:
        List of bytes representing UTF-8 encoding
    
    Raises:
        ValueError: If code point is invalid
    """
    
    # Validate code point range
    if codepoint < 0 or codepoint > 0x10FFFF:
        raise ValueError(f"Code point 0x{codepoint:X} out of valid range")
    
    # Check for surrogate range (invalid)
    if 0xD800 <= codepoint <= 0xDFFF:
        raise ValueError(f"Code point 0x{codepoint:X} is in surrogate range")
    
    # 1-byte sequence (ASCII)
    if codepoint <= 0x7F:
        return [codepoint]
    
    # 2-byte sequence
    elif codepoint <= 0x7FF:
        byte1 = 0xC0 | (codepoint >> 6)
        byte2 = 0x80 | (codepoint & 0x3F)
        return [byte1, byte2]
    
    # 3-byte sequence
    elif codepoint <= 0xFFFF:
        byte1 = 0xE0 | (codepoint >> 12)
        byte2 = 0x80 | ((codepoint >> 6) & 0x3F)
        byte3 = 0x80 | (codepoint & 0x3F)
        return [byte1, byte2, byte3]
    
    # 4-byte sequence
    else:  # codepoint <= 0x10FFFF
        byte1 = 0xF0 | (codepoint >> 18)
        byte2 = 0x80 | ((codepoint >> 12) & 0x3F)
        byte3 = 0x80 | ((codepoint >> 6) & 0x3F)
        byte4 = 0x80 | (codepoint & 0x3F)
        return [byte1, byte2, byte3, byte4]


# Example usage:
# Telugu అ (U+0C05)
utf8_bytes = unicode_to_utf8(0x0C05)
# Result: [0xE0, 0xB0, 0x85]
```

**Dry Run of unicode_to_utf8(0x0C05) — step by step through the code:**

```
Input: codepoint = 0x0C05 (decimal 3077)

Line: if codepoint < 0 or codepoint > 0x10FFFF
  → 3077 < 0? No. 3077 > 1114111? No. → Pass validation.

Line: if 0xD800 <= codepoint <= 0xDFFF
  → 55296 <= 3077? No. → Pass surrogate check.

Line: if codepoint <= 0x7F
  → 3077 <= 127? No. → Not 1-byte.

Line: elif codepoint <= 0x7FF
  → 3077 <= 2047? No. → Not 2-byte.

Line: elif codepoint <= 0xFFFF
  → 3077 <= 65535? Yes. → 3-byte sequence.

  byte1 = 0xE0 | (codepoint >> 12)
        = 0xE0 | (3077 >> 12)
        = 0xE0 | 0          (3077 in binary is 110000000101;
                              shifting right 12 gives 0000 = 0)
        Wait: 3077 = 0000 1100 0000 0101
              >> 12 shifts right 12 positions
              Result: 0000 0000 0000 0000 0000 → but we have 16 bits
              0000 1100 0000 0101 >> 12 = 0000 0000 0000 = 0x000... 
              Actually: 0000 1100 0000 0101 has bits at positions 10,11
              >> 12 means only bits at position 12+ survive
              Position 12 is bit index 12 (counting from 0 on right)
              Bit 12 = 0, Bit 11 = 1, Bit 10 = 1
              So >> 12 gives: 0000 (only the top 4 bits matter for a 16-bit value)
              0xE0 | 0x00 = 0xE0
        = 0xE0 ✓

  byte2 = 0x80 | ((codepoint >> 6) & 0x3F)
        = 0x80 | ((3077 >> 6) & 0x3F)
        3077 >> 6:
          3077 = 0000 1100 0000 0101
          >> 6 =      0000 0011 0000 = 0x30 (decimal 48)
        48 & 0x3F (keep low 6 bits):
          0x30 = 0011 0000
          0x3F = 0011 1111
          AND  = 0011 0000 = 0x30
        0x80 | 0x30 = 1000 0000 | 0011 0000 = 1011 0000 = 0xB0
        = 0xB0 ✓

  byte3 = 0x80 | (codepoint & 0x3F)
        = 0x80 | (3077 & 0x3F)
        3077 & 0x3F (keep low 6 bits):
          3077 = ...0000 0101
          0x3F =  0011 1111
          AND  =  0000 0101 = 0x05
        0x80 | 0x05 = 1000 0000 | 0000 0101 = 1000 0101 = 0x85
        = 0x85 ✓

  RETURN [0xE0, 0xB0, 0x85]
```

**Dry Run of unicode_to_utf8(0x41) — ASCII "A":**

```
Input: codepoint = 0x41 (decimal 65)

Validation: 65 is in valid range, not a surrogate. → Pass.

if codepoint <= 0x7F:
  → 65 <= 127? Yes. → 1-byte sequence.
  RETURN [65] = [0x41]

Output: [0x41]
That is it — ASCII characters pass through unchanged.
```

**Dry Run of unicode_to_utf8(0x00E9) — "é":**

```
Input: codepoint = 0x00E9 (decimal 233)

Validation: Pass.

if codepoint <= 0x7F:   → 233 <= 127? No.
elif codepoint <= 0x7FF: → 233 <= 2047? Yes. → 2-byte sequence.

  byte1 = 0xC0 | (233 >> 6)
        233 >> 6: 233 = 1110 1001, >> 6 = 0000 0011 = 3
        0xC0 | 3 = 1100 0000 | 0000 0011 = 1100 0011 = 0xC3
        = 0xC3 ✓

  byte2 = 0x80 | (233 & 0x3F)
        233 & 0x3F: 1110 1001 & 0011 1111 = 0010 1001 = 0x29 (decimal 41)
        0x80 | 0x29 = 1000 0000 | 0010 1001 = 1010 1001 = 0xA9
        = 0xA9 ✓

  RETURN [0xC3, 0xA9]
```

**Dry Run of unicode_to_utf8(0x1F600) — Emoji "😀":**

```
Input: codepoint = 0x1F600 (decimal 128512)

Validation: Pass.

if codepoint <= 0x7F:    → No.
elif codepoint <= 0x7FF: → No.
elif codepoint <= 0xFFFF:→ 128512 <= 65535? No.
else (4-byte):           → Yes.

  byte1 = 0xF0 | (128512 >> 18)
        128512 >> 18:
          128512 = 0001 1111 0110 0000 0000 0000 (in enough bits)
          Actually: 0x1F600 in binary = 1 1111 0110 0000 0000 0000
          >> 18: shifts right 18 positions
          Remaining: 000 (top 3 bits of the 21-bit value)
          0x1F600 = 0 0001 1111 0110 0000 0000 (21 bits)
          >> 18 = 000 = 0
        0xF0 | 0 = 0xF0
        = 0xF0 ✓

  byte2 = 0x80 | ((128512 >> 12) & 0x3F)
        128512 >> 12:
          0 0001 1111 0110 0000 0000 >> 12 = 0 0001 1111 0 = 0x1F (decimal 31)
        Wait, more carefully:
          21-bit value: 000 011111 011000 000000
          >> 12 means take bits 12-20: 000 011111 = 0x1F (31)
        31 & 0x3F = 31 (0x1F, already < 64)
        0x80 | 0x1F = 1000 0000 | 0001 1111 = 1001 1111 = 0x9F
        = 0x9F ✓

  byte3 = 0x80 | ((128512 >> 6) & 0x3F)
        >> 6 then & 0x3F extracts bits 6-11: 011000 = 0x18 (24)
        0x80 | 0x18 = 1000 0000 | 0001 1000 = 1001 1000 = 0x98
        = 0x98 ✓

  byte4 = 0x80 | (128512 & 0x3F)
        & 0x3F extracts bits 0-5: 000000 = 0x00
        0x80 | 0x00 = 1000 0000 = 0x80
        = 0x80 ✓

  RETURN [0xF0, 0x9F, 0x98, 0x80]
```

### 9.2 UTF-8 to Unicode Conversion (Complete)

```python
def utf8_to_unicode(byte_sequence, start_pos=0):
    """
    Convert UTF-8 byte sequence to Unicode code point.
    
    Args:
        byte_sequence: List of bytes
        start_pos: Starting position in byte sequence
    
    Returns:
        Tuple of (code_point, bytes_consumed)
    
    Raises:
        ValueError: If UTF-8 sequence is invalid
    """
    
    if start_pos >= len(byte_sequence):
        raise ValueError("Start position beyond sequence length")
    
    byte1 = byte_sequence[start_pos]
    
    # 1-byte sequence (0xxxxxxx)
    if (byte1 & 0x80) == 0:
        return (byte1, 1)
    
    # 2-byte sequence (110xxxxx 10xxxxxx)
    elif (byte1 & 0xE0) == 0xC0:
        if start_pos + 1 >= len(byte_sequence):
            raise ValueError("Incomplete 2-byte UTF-8 sequence")
        
        byte2 = byte_sequence[start_pos + 1]
        
        # Check continuation byte
        if (byte2 & 0xC0) != 0x80:
            raise ValueError("Invalid continuation byte in 2-byte sequence")
        
        codepoint = ((byte1 & 0x1F) << 6) | (byte2 & 0x3F)
        
        # Check for overlong encoding
        if codepoint < 0x80:
            raise ValueError("Overlong 2-byte encoding")
        
        return (codepoint, 2)
    
    # 3-byte sequence (1110xxxx 10xxxxxx 10xxxxxx)
    elif (byte1 & 0xF0) == 0xE0:
        if start_pos + 2 >= len(byte_sequence):
            raise ValueError("Incomplete 3-byte UTF-8 sequence")
        
        byte2 = byte_sequence[start_pos + 1]
        byte3 = byte_sequence[start_pos + 2]
        
        # Check continuation bytes
        if (byte2 & 0xC0) != 0x80 or (byte3 & 0xC0) != 0x80:
            raise ValueError("Invalid continuation byte in 3-byte sequence")
        
        codepoint = ((byte1 & 0x0F) << 12) | \
                   ((byte2 & 0x3F) << 6) | \
                   (byte3 & 0x3F)
        
        # Check for overlong encoding
        if codepoint < 0x800:
            raise ValueError("Overlong 3-byte encoding")
        
        # Check for surrogate range
        if 0xD800 <= codepoint <= 0xDFFF:
            raise ValueError("UTF-8 encoded surrogate code point")
        
        return (codepoint, 3)
    
    # 4-byte sequence (11110xxx 10xxxxxx 10xxxxxx 10xxxxxx)
    elif (byte1 & 0xF8) == 0xF0:
        if start_pos + 3 >= len(byte_sequence):
            raise ValueError("Incomplete 4-byte UTF-8 sequence")
        
        byte2 = byte_sequence[start_pos + 1]
        byte3 = byte_sequence[start_pos + 2]
        byte4 = byte_sequence[start_pos + 3]
        
        # Check continuation bytes
        if (byte2 & 0xC0) != 0x80 or \
           (byte3 & 0xC0) != 0x80 or \
           (byte4 & 0xC0) != 0x80:
            raise ValueError("Invalid continuation byte in 4-byte sequence")
        
        codepoint = ((byte1 & 0x07) << 18) | \
                   ((byte2 & 0x3F) << 12) | \
                   ((byte3 & 0x3F) << 6) | \
                   (byte4 & 0x3F)
        
        # Check for overlong encoding
        if codepoint < 0x10000:
            raise ValueError("Overlong 4-byte encoding")
        
        # Check for valid Unicode range
        if codepoint > 0x10FFFF:
            raise ValueError("Code point exceeds Unicode maximum")
        
        return (codepoint, 4)
    
    else:
        raise ValueError(f"Invalid UTF-8 start byte: 0x{byte1:02X}")


# Example usage:
# UTF-8 bytes for Telugu అ: E0 B0 85
utf8_bytes = [0xE0, 0xB0, 0x85]
codepoint, consumed = utf8_to_unicode(utf8_bytes, 0)
# Result: codepoint = 0x0C05, consumed = 3
```

**Dry Run of utf8_to_unicode([0xE0, 0xB0, 0x85], 0):**

```
Input: byte_sequence = [0xE0, 0xB0, 0x85], start_pos = 0

byte1 = 0xE0 = 1110 0000

Check: (byte1 & 0x80) == 0?
  0xE0 & 0x80 = 1110 0000 & 1000 0000 = 1000 0000 = 0x80
  0x80 == 0? No. → Not 1-byte.

Check: (byte1 & 0xE0) == 0xC0?
  0xE0 & 0xE0 = 1110 0000 & 1110 0000 = 1110 0000 = 0xE0
  0xE0 == 0xC0? No. → Not 2-byte.

Check: (byte1 & 0xF0) == 0xE0?
  0xE0 & 0xF0 = 1110 0000 & 1111 0000 = 1110 0000 = 0xE0
  0xE0 == 0xE0? Yes! → 3-byte sequence.

  start_pos + 2 = 2. Length = 3. 2 >= 3? No. → Enough bytes.

  byte2 = 0xB0 = 1011 0000
  byte3 = 0x85 = 1000 0101

  Check continuation bytes:
    byte2 & 0xC0 = 1011 0000 & 1100 0000 = 1000 0000 = 0x80. Equals 0x80? Yes ✓
    byte3 & 0xC0 = 1000 0101 & 1100 0000 = 1000 0000 = 0x80. Equals 0x80? Yes ✓

  Compute codepoint:
    (byte1 & 0x0F) = 0xE0 & 0x0F = 1110 0000 & 0000 1111 = 0000 0000 = 0x00
    << 12: 0x00 << 12 = 0x0000

    (byte2 & 0x3F) = 0xB0 & 0x3F = 1011 0000 & 0011 1111 = 0011 0000 = 0x30
    << 6: 0x30 << 6 = 0x0C00

    (byte3 & 0x3F) = 0x85 & 0x3F = 1000 0101 & 0011 1111 = 0000 0101 = 0x05

    codepoint = 0x0000 | 0x0C00 | 0x05 = 0x0C05

  Overlong check: 0x0C05 < 0x800? No. → Pass.
  Surrogate check: 0xD800 <= 0x0C05 <= 0xDFFF? No. → Pass.

  RETURN (0x0C05, 3)

Output: codepoint = 0x0C05 (decimal 3077), bytes consumed = 3
```

**Dry Run of utf8_to_unicode([0xC3, 0xA9], 0) — decoding "é":**

```
Input: byte_sequence = [0xC3, 0xA9], start_pos = 0

byte1 = 0xC3 = 1100 0011

Check: (byte1 & 0x80) == 0? → 0xC3 & 0x80 = 0x80. No.
Check: (byte1 & 0xE0) == 0xC0?
  0xC3 & 0xE0 = 1100 0011 & 1110 0000 = 1100 0000 = 0xC0. Yes! → 2-byte.

  byte2 = 0xA9 = 1010 1001

  Continuation check: 0xA9 & 0xC0 = 1010 1001 & 1100 0000 = 1000 0000 = 0x80 ✓

  codepoint = ((0xC3 & 0x1F) << 6) | (0xA9 & 0x3F)
            = (0x03 << 6) | 0x29
            = 0xC0 | 0x29
            = 0x00E9

  Overlong check: 0xE9 < 0x80? No. → Pass.

  RETURN (0x00E9, 2)

Output: codepoint = 0x00E9 (decimal 233, "é"), bytes consumed = 2
```

**Dry Run of utf8_to_unicode([0xF0, 0x9F, 0x98, 0x80], 0) — decoding "😀":**

```
Input: byte_sequence = [0xF0, 0x9F, 0x98, 0x80], start_pos = 0

byte1 = 0xF0 = 1111 0000

Check: (byte1 & 0x80) == 0? No.
Check: (byte1 & 0xE0) == 0xC0? 0xF0 & 0xE0 = 0xE0 ≠ 0xC0. No.
Check: (byte1 & 0xF0) == 0xE0? 0xF0 & 0xF0 = 0xF0 ≠ 0xE0. No.
Check: (byte1 & 0xF8) == 0xF0? 0xF0 & 0xF8 = 1111 0000 & 1111 1000 = 1111 0000 = 0xF0. Yes! → 4-byte.

  byte2 = 0x9F, byte3 = 0x98, byte4 = 0x80
  All continuation checks pass (each & 0xC0 = 0x80) ✓

  codepoint = ((0xF0 & 0x07) << 18) | ((0x9F & 0x3F) << 12) |
              ((0x98 & 0x3F) << 6) | (0x80 & 0x3F)

  0xF0 & 0x07 = 0x00 → << 18 = 0x00000
  0x9F & 0x3F = 0x1F → << 12 = 0x1F000
  0x98 & 0x3F = 0x18 → <<  6 = 0x00600
  0x80 & 0x3F = 0x00 →        0x00000

  codepoint = 0x00000 | 0x1F000 | 0x00600 | 0x00000 = 0x1F600

  Overlong check: 0x1F600 < 0x10000? No. → Pass.
  Range check: 0x1F600 > 0x10FFFF? No. → Pass.

  RETURN (0x1F600, 4)

Output: codepoint = 0x1F600 (decimal 128512, "😀"), bytes consumed = 4
```

### 9.3 Unicode to UTF-16 Conversion (Complete)

```python
def unicode_to_utf16(codepoint, byte_order='BE'):
    """
    Convert Unicode code point to UTF-16 byte sequence.
    
    Args:
        codepoint: Integer Unicode code point
        byte_order: 'BE' for big-endian, 'LE' for little-endian
    
    Returns:
        List of bytes representing UTF-16 encoding
    
    Raises:
        ValueError: If code point is invalid
    """
    
    # Validate code point
    if codepoint < 0 or codepoint > 0x10FFFF:
        raise ValueError(f"Code point 0x{codepoint:X} out of valid range")
    
    # Surrogate range is invalid
    if 0xD800 <= codepoint <= 0xDFFF:
        raise ValueError(f"Cannot encode surrogate code point 0x{codepoint:X}")
    
    # BMP characters (direct encoding)
    if codepoint <= 0xFFFF:
        if byte_order == 'BE':
            byte1 = (codepoint >> 8) & 0xFF
            byte2 = codepoint & 0xFF
            return [byte1, byte2]
        else:  # LE
            byte1 = codepoint & 0xFF
            byte2 = (codepoint >> 8) & 0xFF
            return [byte1, byte2]
    
    # Supplementary planes (surrogate pairs)
    else:
        # Subtract 0x10000
        adjusted = codepoint - 0x10000
        
        # Extract high and low 10 bits
        high10 = (adjusted >> 10) & 0x3FF
        low10 = adjusted & 0x3FF
        
        # Create surrogates
        high_surrogate = 0xD800 + high10
        low_surrogate = 0xDC00 + low10
        
        if byte_order == 'BE':
            bytes_result = [
                (high_surrogate >> 8) & 0xFF,
                high_surrogate & 0xFF,
                (low_surrogate >> 8) & 0xFF,
                low_surrogate & 0xFF
            ]
        else:  # LE
            bytes_result = [
                high_surrogate & 0xFF,
                (high_surrogate >> 8) & 0xFF,
                low_surrogate & 0xFF,
                (low_surrogate >> 8) & 0xFF
            ]
        
        return bytes_result


# Example usage:
# Telugu అ (U+0C05)
utf16_be = unicode_to_utf16(0x0C05, 'BE')
# Result: [0x0C, 0x05]

utf16_le = unicode_to_utf16(0x0C05, 'LE')
# Result: [0x05, 0x0C]

# Emoji 😀 (U+1F600)
emoji_utf16_be = unicode_to_utf16(0x1F600, 'BE')
# Result: [0xD8, 0x3D, 0xDE, 0x00]
```

**Dry Run of unicode_to_utf16(0x0C05, 'BE'):**

```
Input: codepoint = 0x0C05, byte_order = 'BE'

Validation: 0x0C05 is valid, not in surrogate range. → Pass.

if codepoint <= 0xFFFF: → 0x0C05 <= 0xFFFF? Yes. → BMP direct encoding.

  byte_order == 'BE':
    byte1 = (0x0C05 >> 8) & 0xFF
          = 0x0C & 0xFF = 0x0C
    byte2 = 0x0C05 & 0xFF = 0x05

  RETURN [0x0C, 0x05]

Output: [0x0C, 0x05] — high byte first, then low byte.
```

**Dry Run of unicode_to_utf16(0x0C05, 'LE'):**

```
Input: codepoint = 0x0C05, byte_order = 'LE'

BMP path (same check as above).

  byte_order == 'LE':
    byte1 = 0x0C05 & 0xFF = 0x05
    byte2 = (0x0C05 >> 8) & 0xFF = 0x0C

  RETURN [0x05, 0x0C]

Output: [0x05, 0x0C] — low byte first, then high byte.
```

**Dry Run of unicode_to_utf16(0x1F600, 'BE') — Emoji surrogate pair:**

```
Input: codepoint = 0x1F600, byte_order = 'BE'

Validation: Pass.

if codepoint <= 0xFFFF: → 0x1F600 <= 0xFFFF? No. → Surrogate pair path.

  adjusted = 0x1F600 - 0x10000 = 0x0F600

  high10 = (0x0F600 >> 10) & 0x3FF
         = 0x0F600 >> 10:
           0x0F600 = 0000 1111 0110 0000 0000 (binary, 20 bits)
           >> 10:    0000 0011 1101 = 0x03D (decimal 61)
         0x03D & 0x3FF = 0x03D (already < 1024)

  low10 = 0x0F600 & 0x3FF
        = 0000 1111 0110 0000 0000 & 0000 0011 1111 1111
        = 0000 0010 0000 0000 = 0x200 (decimal 512)

  high_surrogate = 0xD800 + 0x03D = 0xD83D
  low_surrogate  = 0xDC00 + 0x200 = 0xDE00

  byte_order == 'BE':
    bytes_result = [
        (0xD83D >> 8) & 0xFF = 0xD8,
        0xD83D & 0xFF        = 0x3D,
        (0xDE00 >> 8) & 0xFF = 0xDE,
        0xDE00 & 0xFF        = 0x00
    ]

  RETURN [0xD8, 0x3D, 0xDE, 0x00]
```

### 9.4 UTF-16 to Unicode Conversion (Complete)

```python
def utf16_to_unicode(byte_sequence, start_pos=0, byte_order='BE'):
    """
    Convert UTF-16 byte sequence to Unicode code point.
    
    Args:
        byte_sequence: List of bytes
        start_pos: Starting position
        byte_order: 'BE' for big-endian, 'LE' for little-endian
    
    Returns:
        Tuple of (code_point, bytes_consumed)
    
    Raises:
        ValueError: If UTF-16 sequence is invalid
    """
    
    if start_pos + 1 >= len(byte_sequence):
        raise ValueError("Incomplete UTF-16 sequence")
    
    # Read first code unit
    if byte_order == 'BE':
        unit1 = (byte_sequence[start_pos] << 8) | byte_sequence[start_pos + 1]
    else:  # LE
        unit1 = byte_sequence[start_pos] | (byte_sequence[start_pos + 1] << 8)
    
    # BMP character (not a surrogate)
    if unit1 < 0xD800 or unit1 > 0xDFFF:
        return (unit1, 2)
    
    # High surrogate (start of pair)
    elif 0xD800 <= unit1 <= 0xDBFF:
        if start_pos + 3 >= len(byte_sequence):
            raise ValueError("Incomplete surrogate pair")
        
        # Read second code unit
        if byte_order == 'BE':
            unit2 = (byte_sequence[start_pos + 2] << 8) | \
                    byte_sequence[start_pos + 3]
        else:  # LE
            unit2 = byte_sequence[start_pos + 2] | \
                    (byte_sequence[start_pos + 3] << 8)
        
        # Verify low surrogate
        if unit2 < 0xDC00 or unit2 > 0xDFFF:
            raise ValueError("Invalid surrogate pair")
        
        # Decode surrogate pair
        high10 = unit1 - 0xD800
        low10 = unit2 - 0xDC00
        
        codepoint = 0x10000 + (high10 << 10) + low10
        
        return (codepoint, 4)
    
    # Low surrogate without high surrogate
    else:
        raise ValueError("Unpaired low surrogate")


# Example usage:
# UTF-16BE for Telugu అ: 0C 05
utf16_bytes_be = [0x0C, 0x05]
codepoint, consumed = utf16_to_unicode(utf16_bytes_be, 0, 'BE')
# Result: codepoint = 0x0C05, consumed = 2

# UTF-16LE for Telugu అ: 05 0C
utf16_bytes_le = [0x05, 0x0C]
codepoint, consumed = utf16_to_unicode(utf16_bytes_le, 0, 'LE')
# Result: codepoint = 0x0C05, consumed = 2
```

**Dry Run of utf16_to_unicode([0x0C, 0x05], 0, 'BE'):**

```
Input: byte_sequence = [0x0C, 0x05], start_pos = 0, byte_order = 'BE'

start_pos + 1 = 1. len = 2. 1 >= 2? No. → Enough bytes.

byte_order == 'BE':
  unit1 = (0x0C << 8) | 0x05
        = 0x0C00 | 0x05
        = 0x0C05

Is unit1 < 0xD800 or > 0xDFFF?
  0x0C05 < 0xD800? Yes. → BMP character.

RETURN (0x0C05, 2)

Output: codepoint = 0x0C05, bytes consumed = 2
```

**Dry Run of utf16_to_unicode([0x05, 0x0C], 0, 'LE'):**

```
Input: byte_sequence = [0x05, 0x0C], start_pos = 0, byte_order = 'LE'

byte_order == 'LE':
  unit1 = 0x05 | (0x0C << 8)
        = 0x05 | 0x0C00
        = 0x0C05

BMP check: 0x0C05 < 0xD800? Yes. → BMP character.

RETURN (0x0C05, 2)

Output: Same result regardless of byte order — the algorithm correctly
        reassembles the code unit from LE byte layout.
```

**Dry Run of utf16_to_unicode([0xD8, 0x3D, 0xDE, 0x00], 0, 'BE') — decoding emoji surrogate pair:**

```
Input: byte_sequence = [0xD8, 0x3D, 0xDE, 0x00], start_pos = 0, byte_order = 'BE'

unit1 = (0xD8 << 8) | 0x3D = 0xD800 | 0x003D = 0xD83D

Is unit1 < 0xD800 or > 0xDFFF? 0xD83D is in range 0xD800–0xDFFF. → No, it is a surrogate.

Is 0xD800 <= unit1 <= 0xDBFF? 0xD800 <= 0xD83D <= 0xDBFF? Yes. → High surrogate.

  start_pos + 3 = 3. len = 4. 3 >= 4? No. → Enough bytes for pair.

  unit2 = (0xDE << 8) | 0x00 = 0xDE00

  Is 0xDC00 <= unit2 <= 0xDFFF? 0xDC00 <= 0xDE00 <= 0xDFFF? Yes. → Valid low surrogate.

  high10 = 0xD83D - 0xD800 = 0x003D (decimal 61)
  low10  = 0xDE00 - 0xDC00 = 0x0200 (decimal 512)

  codepoint = 0x10000 + (0x003D << 10) + 0x0200
            = 0x10000 + 0x0F400 + 0x0200
            = 0x10000 + 0x0F600
            = 0x1F600

RETURN (0x1F600, 4)

Output: codepoint = 0x1F600 (😀), bytes consumed = 4
```

### 9.5 UTF-8 to UTF-16 Direct Conversion

```python
def utf8_to_utf16(utf8_bytes, byte_order='BE', add_bom=False):
    """
    Convert UTF-8 byte sequence to UTF-16.
    
    Args:
        utf8_bytes: List of UTF-8 bytes
        byte_order: 'BE' or 'LE'
        add_bom: Whether to prepend BOM
    
    Returns:
        List of UTF-16 bytes
    """
    
    utf16_result = []
    
    # Add BOM if requested
    if add_bom:
        if byte_order == 'BE':
            utf16_result.extend([0xFE, 0xFF])
        else:
            utf16_result.extend([0xFF, 0xFE])
    
    # Process UTF-8 sequence
    pos = 0
    while pos < len(utf8_bytes):
        # Decode UTF-8 to code point
        codepoint, consumed = utf8_to_unicode(utf8_bytes, pos)
        
        # Encode code point to UTF-16
        utf16_bytes = unicode_to_utf16(codepoint, byte_order)
        utf16_result.extend(utf16_bytes)
        
        pos += consumed
    
    return utf16_result


# Example usage:
# UTF-8 for "అక" (two characters)
utf8_input = [0xE0, 0xB0, 0x85, 0xE0, 0xB0, 0x95]
utf16_output = utf8_to_utf16(utf8_input, 'BE', add_bom=True)
# Result: [0xFE, 0xFF, 0x0C, 0x05, 0x0C, 0x15]
#         BOM       అ          క
```

**Dry Run of utf8_to_utf16 for "అక" (BE, with BOM):**

```
Input: utf8_bytes = [0xE0, 0xB0, 0x85, 0xE0, 0xB0, 0x95]
       byte_order = 'BE', add_bom = True

Step 1: Add BOM (BE)
  utf16_result = [0xFE, 0xFF]

Step 2: Process loop

  Iteration 1: pos = 0
    utf8_to_unicode([0xE0, 0xB0, 0x85, ...], 0)
    → codepoint = 0x0C05, consumed = 3  (as we traced earlier)
    unicode_to_utf16(0x0C05, 'BE')
    → [0x0C, 0x05]
    utf16_result = [0xFE, 0xFF, 0x0C, 0x05]
    pos = 0 + 3 = 3

  Iteration 2: pos = 3
    utf8_to_unicode([..., 0xE0, 0xB0, 0x95], 3)
    → Decoding 0xE0 0xB0 0x95:
      byte1 = 0xE0 → 3-byte sequence
      byte2 = 0xB0, byte3 = 0x95
      codepoint = ((0xE0 & 0x0F) << 12) | ((0xB0 & 0x3F) << 6) | (0x95 & 0x3F)
               = (0x00 << 12) | (0x30 << 6) | 0x15
               = 0x0000 | 0x0C00 | 0x0015
               = 0x0C15
    → codepoint = 0x0C15, consumed = 3
    unicode_to_utf16(0x0C15, 'BE')
    → [0x0C, 0x15]
    utf16_result = [0xFE, 0xFF, 0x0C, 0x05, 0x0C, 0x15]
    pos = 3 + 3 = 6

  pos = 6, len = 6. Loop ends.

Output: [0xFE, 0xFF, 0x0C, 0x05, 0x0C, 0x15]
        ^^^^^^^^   ^^^^^^^^^   ^^^^^^^^^
         BOM(BE)    అ (BE)      క (BE)
```

### 9.6 UTF-16 to UTF-8 Direct Conversion

```python
def utf16_to_utf8(utf16_bytes, byte_order=None):
    """
    Convert UTF-16 byte sequence to UTF-8.
    
    Args:
        utf16_bytes: List of UTF-16 bytes
        byte_order: 'BE', 'LE', or None (auto-detect from BOM)
    
    Returns:
        List of UTF-8 bytes
    """
    
    # Auto-detect byte order from BOM
    if byte_order is None:
        if len(utf16_bytes) >= 2:
            if utf16_bytes[0] == 0xFE and utf16_bytes[1] == 0xFF:
                byte_order = 'BE'
                start_pos = 2  # Skip BOM
            elif utf16_bytes[0] == 0xFF and utf16_bytes[1] == 0xFE:
                byte_order = 'LE'
                start_pos = 2  # Skip BOM
            else:
                # Default to BE if no BOM
                byte_order = 'BE'
                start_pos = 0
        else:
            raise ValueError("UTF-16 sequence too short")
    else:
        start_pos = 0
    
    utf8_result = []
    pos = start_pos
    
    # Process UTF-16 sequence
    while pos < len(utf16_bytes):
        # Decode UTF-16 to code point
        codepoint, consumed = utf16_to_unicode(utf16_bytes, pos, byte_order)
        
        # Encode code point to UTF-8
        utf8_bytes = unicode_to_utf8(codepoint)
        utf8_result.extend(utf8_bytes)
        
        pos += consumed
    
    return utf8_result


# Example usage:
# UTF-16BE with BOM for "అక"
utf16_input = [0xFE, 0xFF, 0x0C, 0x05, 0x0C, 0x15]
utf8_output = utf16_to_utf8(utf16_input)
# Result: [0xE0, 0xB0, 0x85, 0xE0, 0xB0, 0x95]
```

**Dry Run of utf16_to_utf8 for UTF-16BE "అक" with BOM:**

```
Input: utf16_bytes = [0xFE, 0xFF, 0x0C, 0x05, 0x0C, 0x15], byte_order = None

Step 1: Auto-detect BOM
  utf16_bytes[0] = 0xFE, utf16_bytes[1] = 0xFF
  Matches [0xFE, 0xFF] → byte_order = 'BE', start_pos = 2

Step 2: Process loop

  Iteration 1: pos = 2
    utf16_to_unicode([..., 0x0C, 0x05, ...], 2, 'BE')
    → unit1 = (0x0C << 8) | 0x05 = 0x0C05
    → BMP character → return (0x0C05, 2)
    unicode_to_utf8(0x0C05)
    → [0xE0, 0xB0, 0x85] (as traced before)
    utf8_result = [0xE0, 0xB0, 0x85]
    pos = 2 + 2 = 4

  Iteration 2: pos = 4
    utf16_to_unicode([..., 0x0C, 0x15], 4, 'BE')
    → unit1 = (0x0C << 8) | 0x15 = 0x0C15
    → BMP character → return (0x0C15, 2)
    unicode_to_utf8(0x0C15)
    → 3-byte encoding for 0x0C15:
      byte1 = 0xE0 | (0x0C15 >> 12) = 0xE0 | 0 = 0xE0
      byte2 = 0x80 | ((0x0C15 >> 6) & 0x3F) = 0x80 | 0x30 = 0xB0
      byte3 = 0x80 | (0x0C15 & 0x3F) = 0x80 | 0x15 = 0x95
    → [0xE0, 0xB0, 0x95]
    utf8_result = [0xE0, 0xB0, 0x85, 0xE0, 0xB0, 0x95]
    pos = 4 + 2 = 6

  pos = 6, len = 6. Loop ends.

Output: [0xE0, 0xB0, 0x85, 0xE0, 0xB0, 0x95]
        ^^^^^^^^^^^^^^^   ^^^^^^^^^^^^^^^
         అ in UTF-8        క in UTF-8
```

---

## 10. Operating System and Machine-Level Processing

### 10.1 How the OS Handles Character Encoding

```
┌───────────────────────────────────────────────┐
│           Application Layer                   │
│  (User programs, text editors, browsers)      │
└───────────────┬───────────────────────────────┘
                │ Unicode API calls
                ↓
┌───────────────────────────────────────────────┐
│        Operating System Layer                 │
│  • Character encoding conversion              │
│  • Locale and language settings               │
│  • Font rendering subsystem                   │
└───────────────┬───────────────────────────────┘
                │ System calls
                ↓
┌───────────────────────────────────────────────┐
│           File System Layer                   │
│  • File names (UTF-8/UTF-16)                  │
│  • File content encoding metadata             │
└───────────────┬───────────────────────────────┘
                │ I/O operations
                ↓
┌───────────────────────────────────────────────┐
│         Hardware Layer                        │
│  • Disk storage (bytes)                       │
│  • Memory (endianness-dependent)              │
└───────────────────────────────────────────────┘
```

### 10.2 Operating System Specific Behavior

**Windows**:
- Internal representation: **UTF-16 LE**
- API: Wide character functions (wchar_t, 16-bit)
- File system (NTFS): UTF-16 for file names
- Console: Limited UTF-8 support (Code Page 65001)
- Registry: Stores strings in UTF-16

**Linux/Unix**:
- Internal representation: **UTF-8**
- API: Multi-byte character functions (char, 8-bit)
- File system: UTF-8 for file names (byte-oriented)
- Locale: LC_CTYPE determines encoding
- Modern distros: Default to UTF-8

**macOS**:
- Internal representation: **UTF-8**
- File system (APFS/HFS+): UTF-8 (normalized NFD)
- API: Supports both UTF-8 and UTF-16
- Core Foundation: CFString (abstract, multiple encodings)

### 10.3 Memory Representation

**Stack Example**: String "అ" in different systems

```
Windows (UTF-16LE):
Address  |  Value  |  Comment
---------|---------|----------
0x1000   |  0x05   |  Low byte
0x1001   |  0x0C   |  High byte
0x1002   |  0x00   |  Null terminator (low)
0x1003   |  0x00   |  Null terminator (high)

Linux (UTF-8):
Address  |  Value  |  Comment
---------|---------|----------
0x1000   |  0xE0   |  Byte 1
0x1001   |  0xB0   |  Byte 2
0x1002   |  0x85   |  Byte 3
0x1003   |  0x00   |  Null terminator
```

**Memory representation with all number bases for "అ":**

```
Windows (UTF-16LE):
Address  |  Hex  |  Dec  |  Bin       |  Oct  |  Role
---------|-------|-------|------------|-------|------------------
0x1000   |  05   |   5   | 0000 0101  |  005  |  Low byte of U+0C05
0x1001   |  0C   |  12   | 0000 1100  |  014  |  High byte of U+0C05
0x1002   |  00   |   0   | 0000 0000  |  000  |  Null terminator low
0x1003   |  00   |   0   | 0000 0000  |  000  |  Null terminator high

Linux (UTF-8):
Address  |  Hex  |  Dec  |  Bin       |  Oct  |  Role
---------|-------|-------|------------|-------|------------------
0x1000   |  E0   | 224   | 1110 0000  |  340  |  UTF-8 Byte 1 (3-byte start)
0x1001   |  B0   | 176   | 1011 0000  |  260  |  UTF-8 Byte 2 (continuation)
0x1002   |  85   | 133   | 1000 0101  |  205  |  UTF-8 Byte 3 (continuation)
0x1003   |  00   |   0   | 0000 0000  |  000  |  Null terminator
```

### 10.4 Font Rendering Pipeline

```
┌──────────────────────────────────────────┐
│  1. Text Input (Unicode code points)     │
│     U+0C05 U+0C15 U+0C24                 │
└────────────────┬─────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│  2. Text Shaping Engine                  │
│     • HarfBuzz, DirectWrite, CoreText    │
│     • Applies OpenType features          │
│     • Handles ligatures and positioning  │
└────────────────┬─────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│  3. Glyph Selection                      │
│     • Maps code points to glyph IDs      │
│     • Font: Noto Sans Telugu             │
│     • Glyph IDs: [125, 142, 167]         │
└────────────────┬─────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│  4. Rasterization                        │
│     • TrueType/OpenType outlines         │
│     • Anti-aliasing, hinting             │
│     • Pixel grid alignment               │
└────────────────┬─────────────────────────┘
                 │
                 ↓
┌──────────────────────────────────────────┐
│  5. Display                              │
│     • GPU/Screen rendering               │
│     • అకత displayed                     │
└──────────────────────────────────────────┘
```

### 10.5 Processor-Level Byte Handling

**Little-Endian System (x86)**:
```
UTF-16 value: 0x0C05 (అ)
Memory layout:
  [0x05] [0x0C]
   LSB    MSB

Read as 16-bit integer:
  Register: 0x0C05 ✓ (correct)
```

**Big-Endian System (Network)**:
```
UTF-16 value: 0x0C05 (అ)
Memory layout:
  [0x0C] [0x05]
   MSB    LSB

Read as 16-bit integer:
  Register: 0x0C05 ✓ (correct)
```

**Byte Swapping** (when transferring between systems):
```
// Little-endian to big-endian conversion
uint16_t value = 0x0C05;
uint16_t swapped = ((value & 0xFF) << 8) | ((value >> 8) & 0xFF);
// swapped = 0x050C

// Or use system functions:
// htons() - host to network short
// ntohs() - network to host short
```

**Dry Run of byte swap for 0x0C05:**

```
value = 0x0C05 = 0000 1100 0000 0101

Step 1: (value & 0xFF) extracts low byte
  0x0C05 & 0x00FF = 0x0005

Step 2: << 8 shifts it to high byte position
  0x0005 << 8 = 0x0500

Step 3: (value >> 8) shifts high byte to low position
  0x0C05 >> 8 = 0x000C

Step 4: & 0xFF masks to keep only one byte
  0x000C & 0xFF = 0x0C

Step 5: OR the two together
  0x0500 | 0x000C = 0x050C

Result: 0x050C — the bytes are swapped.
This is what Little-Endian memory looks like when read as a raw
16-bit value on a Big-Endian system (or vice versa).
```

### 10.6 System Call Examples

**Linux - Write UTF-8 to file**:
```c
#include <stdio.h>
#include <string.h>

int main() {
    FILE *fp = fopen("telugu.txt", "w");
    
    // UTF-8 bytes for "అ"
    unsigned char utf8[] = {0xE0, 0xB0, 0x85, 0x00};
    
    fwrite(utf8, 1, 3, fp);
    fclose(fp);
    
    return 0;
}

// File content (hex): E0 B0 85
```

**Windows - Write UTF-16 to file**:
```c
#include <windows.h>

int main() {
    HANDLE hFile = CreateFileW(L"telugu.txt",
                               GENERIC_WRITE,
                               0, NULL,
                               CREATE_ALWAYS,
                               FILE_ATTRIBUTE_NORMAL,
                               NULL);
    
    // UTF-16LE for "అ"
    wchar_t text[] = {0x0C05, 0x0000};
    DWORD written;
    
    WriteFile(hFile, text, 2, &written, NULL);
    CloseHandle(hFile);
    
    return 0;
}

// File content (hex): 05 0C (little-endian)
```

---

## 11. Implementation Considerations

### 11.1 String Representation in Memory

**Structure for Unicode String**:
```c
typedef struct {
    uint32_t *codepoints;    // Array of code points
    size_t length;           // Number of code points
    size_t capacity;         // Allocated capacity
} UnicodeString;

typedef struct {
    uint8_t *bytes;          // UTF-8 byte array
    size_t byte_length;      // Number of bytes
    size_t char_count;       // Number of characters (cached)
} UTF8String;

typedef struct {
    uint16_t *units;         // UTF-16 code units
    size_t unit_length;      // Number of 16-bit units
    size_t char_count;       // Number of characters
    enum {BE, LE} byte_order;
} UTF16String;
```

### 11.2 Character Boundary Detection

**UTF-8 Character Boundary**:
```c
bool is_utf8_char_start(uint8_t byte) {
    // Start bytes: 0xxxxxxx, 110xxxxx, 1110xxxx, 11110xxx
    // Not: 10xxxxxx (continuation byte)
    return (byte & 0xC0) != 0x80;
}

size_t utf8_char_length(uint8_t first_byte) {
    if ((first_byte & 0x80) == 0x00) return 1;  // 0xxxxxxx
    if ((first_byte & 0xE0) == 0xC0) return 2;  // 110xxxxx
    if ((first_byte & 0xF0) == 0xE0) return 3;  // 1110xxxx
    if ((first_byte & 0xF8) == 0xF0) return 4;  // 11110xxx
    return 0;  // Invalid
}
```

**Dry Run of utf8_char_length for various bytes:**

```
Input: 0xE0 (first byte of "అ")
  (0xE0 & 0x80) == 0x00? → 0x80 == 0x00? No.
  (0xE0 & 0xE0) == 0xC0? → 0xE0 == 0xC0? No.
  (0xE0 & 0xF0) == 0xE0? → 0xE0 == 0xE0? Yes! → return 3. ✓

Input: 0xF0 (first byte of emoji)
  (0xF0 & 0x80) == 0x00? No.
  (0xF0 & 0xE0) == 0xC0? → 0xE0 == 0xC0? No.
  (0xF0 & 0xF0) == 0xE0? → 0xF0 == 0xE0? No.
  (0xF0 & 0xF8) == 0xF0? → 0xF0 == 0xF0? Yes! → return 4. ✓

Input: 0xB0 (continuation byte — middle of "అ")
  (0xB0 & 0x80) == 0x00? → 0x80 == 0x00? No.
  (0xB0 & 0xE0) == 0xC0? → 0xA0 == 0xC0? No.
  (0xB0 & 0xF0) == 0xE0? → 0xB0 == 0xE0? No.
  (0xB0 & 0xF8) == 0xF0? → 0xB0 == 0xF0? No.
  → return 0 (Invalid as start byte — it is a continuation byte). ✓

Input: 0x41 (ASCII "A")
  (0x41 & 0x80) == 0x00? → 0x00 == 0x00? Yes! → return 1. ✓

Input: 0xC3 (first byte of "é")
  (0xC3 & 0x80) == 0x00? No.
  (0xC3 & 0xE0) == 0xC0? → 0xC0 == 0xC0? Yes! → return 2. ✓
```

**UTF-16 Character Boundary**:
```c
bool is_utf16_high_surrogate(uint16_t unit) {
    return (unit >= 0xD800) && (unit <= 0xDBFF);
}

bool is_utf16_low_surrogate(uint16_t unit) {
    return (unit >= 0xDC00) && (unit <= 0xDFFF);
}

size_t utf16_char_length(uint16_t first_unit) {
    if (is_utf16_high_surrogate(first_unit)) {
        return 2;  // Surrogate pair
    } else if (is_utf16_low_surrogate(first_unit)) {
        return 0;  // Error: unpaired low surrogate
    } else {
        return 1;  // BMP character
    }
}
```

### 11.3 Validation

**UTF-8 Validation**:
```python
def validate_utf8(byte_sequence):
    """
    Validate UTF-8 byte sequence.
    
    Returns: True if valid, False otherwise
    """
    pos = 0
    while pos < len(byte_sequence):
        byte = byte_sequence[pos]
        
        # Determine expected sequence length
        if (byte & 0x80) == 0:
            char_len = 1
        elif (byte & 0xE0) == 0xC0:
            char_len = 2
        elif (byte & 0xF0) == 0xE0:
            char_len = 3
        elif (byte & 0xF8) == 0xF0:
            char_len = 4
        else:
            return False  # Invalid start byte
        
        # Check for enough bytes
        if pos + char_len > len(byte_sequence):
            return False
        
        # Validate continuation bytes
        for i in range(1, char_len):
            if (byte_sequence[pos + i] & 0xC0) != 0x80:
                return False
        
        # Check for overlong encoding
        if char_len == 2:
            value = ((byte & 0x1F) << 6) | (byte_sequence[pos + 1] & 0x3F)
            if value < 0x80:
                return False
        elif char_len == 3:
            value = ((byte & 0x0F) << 12) | \
                   ((byte_sequence[pos + 1] & 0x3F) << 6) | \
                   (byte_sequence[pos + 2] & 0x3F)
            if value < 0x800:
                return False
            # Check surrogate range
            if 0xD800 <= value <= 0xDFFF:
                return False
        elif char_len == 4:
            value = ((byte & 0x07) << 18) | \
                   ((byte_sequence[pos + 1] & 0x3F) << 12) | \
                   ((byte_sequence[pos + 2] & 0x3F) << 6) | \
                   (byte_sequence[pos + 3] & 0x3F)
            if value < 0x10000 or value > 0x10FFFF:
                return False
        
        pos += char_len
    
    return True
```

**Dry Run of validate_utf8 for valid input [0xE0, 0xB0, 0x85, 0x41]:**

```
Input: [0xE0, 0xB0, 0x85, 0x41]  (Telugu "అ" followed by ASCII "A")

pos = 0, byte = 0xE0
  (0xE0 & 0x80) == 0? No.
  (0xE0 & 0xE0) == 0xC0? No.
  (0xE0 & 0xF0) == 0xE0? Yes. → char_len = 3

  pos + char_len = 0 + 3 = 3. len = 4. 3 > 4? No. → Enough bytes.

  Continuation check:
    i=1: byte_sequence[1] & 0xC0 = 0xB0 & 0xC0 = 0x80. == 0x80? Yes ✓
    i=2: byte_sequence[2] & 0xC0 = 0x85 & 0xC0 = 0x80. == 0x80? Yes ✓

  Overlong check (char_len == 3):
    value = ((0xE0 & 0x0F) << 12) | ((0xB0 & 0x3F) << 6) | (0x85 & 0x3F)
          = (0x00 << 12) | (0x30 << 6) | 0x05
          = 0 | 0x0C00 | 0x05 = 0x0C05
    0x0C05 < 0x800? No. → Pass.
    0xD800 <= 0x0C05 <= 0xDFFF? No. → Pass.

  pos = 0 + 3 = 3

pos = 3, byte = 0x41
  (0x41 & 0x80) == 0? → 0x00 == 0? Yes. → char_len = 1

  pos + 1 = 4. len = 4. 4 > 4? No. → OK.
  No continuation bytes to check.
  No overlong check for 1-byte.

  pos = 3 + 1 = 4

pos = 4. 4 < 4? No. Loop ends.

Return True ✓
```

**Dry Run of validate_utf8 for INVALID input [0xE0, 0xB0, 0x41]:**

```
Input: [0xE0, 0xB0, 0x41]  (broken sequence — 0x41 is not a continuation byte)

pos = 0, byte = 0xE0 → char_len = 3

  pos + 3 = 3. len = 3. 3 > 3? No. → Enough bytes.

  Continuation check:
    i=1: byte_sequence[1] & 0xC0 = 0xB0 & 0xC0 = 0x80. == 0x80? Yes ✓
    i=2: byte_sequence[2] & 0xC0 = 0x41 & 0xC0 = 0x40. == 0x80? No! ✗

  Return False ← Invalid: third byte is not a continuation byte.
```

### 11.4 Performance Considerations

**Memory Efficiency**:

| Encoding | Telugu Text | English Text | Emoji |
|----------|-------------|--------------|-------|
| UTF-8 | 3 bytes/char | 1 byte/char | 4 bytes/char |
| UTF-16 | 2 bytes/char | 2 bytes/char | 4 bytes/char |
| UTF-32 | 4 bytes/char | 4 bytes/char | 4 bytes/char |

**Processing Speed**:
- **UTF-8**: Variable-length, requires sequential processing, ASCII-compatible
- **UTF-16**: Mostly fixed-width (BMP), random access for BMP, Windows-native
- **UTF-32**: Fixed-width, true random access, memory-intensive

**Recommendation for Telugu**:
- **Storage/Network**: UTF-8 (3 bytes per character, standard)
- **Internal Processing**: UTF-32 or code point arrays (fast indexing)
- **Windows APIs**: UTF-16 (required for native APIs)

### 11.5 Error Handling Strategies

**Replacement Character**:
```
Invalid sequence → U+FFFD (REPLACEMENT CHARACTER)
```

**Error Handling Modes**:
1. **Strict**: Reject any invalid sequence
2. **Replace**: Insert U+FFFD for invalid sequences
3. **Ignore**: Skip invalid sequences
4. **Lossy**: Best-effort conversion

**Example Implementation**:
```python
def utf8_decode_with_errors(bytes, error_mode='replace'):
    """
    Decode UTF-8 with error handling.
    
    error_mode: 'strict', 'replace', 'ignore'
    """
    result = []
    pos = 0
    
    while pos < len(bytes):
        try:
            codepoint, consumed = utf8_to_unicode(bytes, pos)
            result.append(codepoint)
            pos += consumed
        except ValueError:
            if error_mode == 'strict':
                raise
            elif error_mode == 'replace':
                result.append(0xFFFD)  # Replacement character
                pos += 1
            elif error_mode == 'ignore':
                pos += 1
    
    return result
```

---

## Conclusion

This document has covered the fundamental aspects of Unicode and character encoding with specific focus on UTF-8 and UTF-16 transformations. The key takeaways are:

1. **Number bases** (binary, octal, decimal, hexadecimal) are the foundation of all encoding work. Binary is what computers store; hex is how humans read byte values; octal appears in C string literals; decimal is the human reference point.
2. **Unicode** provides a universal character repertoire with consistent code point assignments
3. **UTF-8** is byte-oriented, ASCII-compatible, and the de facto standard for text interchange
4. **UTF-16** is efficient for BMP characters but requires surrogate pairs for supplementary planes
5. **Endianness** matters for multi-byte encodings (UTF-16, UTF-32) but not for UTF-8
6. **Telugu script** (U+0C00-U+0C7F) is in the BMP and requires 3 bytes in UTF-8, 2 bytes in UTF-16
7. **Conversion algorithms** between encodings follow well-defined mathematical transformations
8. **Operating systems** handle encodings differently (Windows: UTF-16, Linux/macOS: UTF-8)

For text processing applications in Telugu or any multilingual context, understanding these encoding schemes is essential for:
- Correct storage and retrieval
- Accurate string operations
- Cross-platform compatibility
- Efficient memory usage
- Proper rendering and display

The algorithms provided in this document form the foundation for implementing custom text processing tools without relying on existing libraries, enabling direct control over encoding operations for specialized applications such as grammar checking, spell correction, and string matching at the byte level.

---

## References

1. The Unicode Standard, Version 15.0, Unicode Consortium
2. RFC 3629 - UTF-8, a transformation format of ISO 10646
3. RFC 2781 - UTF-16, an encoding of ISO 10646
4. Telugu Unicode Block Chart (U+0C00-U+0C7F)
5. Unicode Technical Report #17: Character Encoding Model
6. UTF-8 and Unicode FAQ, Unicode.org
7. IETF Standards on character encoding
8. ISO/IEC 10646 Universal Character Set
