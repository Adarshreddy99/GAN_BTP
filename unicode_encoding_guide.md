# Unicode and Character Encoding: A Comprehensive Guide
## Focus on UTF-8, UTF-16, and Telugu Script Processing

---

## Table of Contents

1. [Introduction to Character Encoding](#1-introduction-to-character-encoding)
2. [Unicode Standard Overview](#2-unicode-standard-overview)
3. [Unicode Code Points and Character Assignment](#3-unicode-code-points-and-character-assignment)
4. [UTF-8 Encoding](#4-utf-8-encoding)
5. [UTF-16 Encoding](#5-utf-16-encoding)
6. [Endianness and Byte Order](#6-endianness-and-byte-order)
7. [Telugu Script in Unicode](#7-telugu-script-in-unicode)
8. [Conversion Algorithms](#8-conversion-algorithms)
9. [Operating System and Machine-Level Processing](#9-operating-system-and-machine-level-processing)
10. [Implementation Considerations](#10-implementation-considerations)

---

## 1. Introduction to Character Encoding

### 1.1 What is Character Encoding?

Character encoding is a systematic method of representing characters (letters, numbers, symbols) as numerical values that computers can process and store. At the fundamental level, computers only understand binary data (0s and 1s), so every character must be mapped to a unique numerical code.

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

**Extended ASCII and Code Pages**
- 8-bit encoding (256 characters)
- Different code pages for different languages
- Problem: Same byte value represents different characters in different code pages
- No universal standard for multilingual text

**Unicode Solution**
- Universal character set
- Single encoding standard for all world's writing systems
- Over 149,000 characters from 161 scripts (as of Unicode 15.0)
- Consistent representation across platforms and languages

---

## 2. Unicode Standard Overview

### 2.1 Unicode Design Principles

Unicode follows these fundamental principles:

1. **Universal Repertoire**: Coverage of all characters from all writing systems
2. **Efficiency**: Compact encoding for common characters
3. **Uniformity**: Fixed-width code points in the abstract character set
4. **Unambiguous**: Each code point has exactly one meaning

### 2.2 Unicode Architecture

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

### 2.3 Unicode Planes

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

**Important Reserved Ranges**:
- **U+D800 to U+DFFF**: Surrogate pairs (used only in UTF-16, not valid characters)
- **U+FDD0 to U+FDEF**: Non-characters
- **U+FFFE and U+FFFF**: Non-characters in each plane

---

## 3. Unicode Code Points and Character Assignment

### 3.1 Code Point Structure

A Unicode code point is written in the format **U+XXXX** (for BMP) or **U+XXXXX** (for supplementary planes), where X represents a hexadecimal digit.

Examples:
- U+0041: Latin Capital Letter A
- U+0C05: Telugu Letter A (అ)
- U+1F600: Grinning Face Emoji (😀)

### 3.2 How Unicode Mappings are Decided

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

### 3.3 Character Properties Table Example

| Code Point | Character | Name | Category | Script |
|------------|-----------|------|----------|--------|
| U+0041 | A | LATIN CAPITAL LETTER A | Uppercase Letter | Latin |
| U+0C05 | అ | TELUGU LETTER A | Letter | Telugu |
| U+0C4D | ్ | TELUGU SIGN VIRAMA | Mark, Nonspacing | Telugu |

---

## 4. UTF-8 Encoding

### 4.1 UTF-8 Design Principles

UTF-8 (8-bit Unicode Transformation Format) is a variable-length encoding:

**Key Properties**:
1. **Variable Length**: 1 to 4 bytes per character
2. **ASCII Compatibility**: First 128 characters (U+0000 to U+007F) are identical to ASCII
3. **Self-Synchronizing**: Can detect character boundaries without scanning from the beginning
4. **Efficient**: Compact for Latin scripts, reasonable for all scripts

### 4.2 UTF-8 Encoding Structure

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

### 4.3 UTF-8 Encoding Algorithm

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

### 4.4 UTF-8 Decoding Algorithm

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

### 4.5 UTF-8 Example: Telugu Character "అ" (U+0C05)

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

---

## 5. UTF-16 Encoding

### 5.1 UTF-16 Design Principles

UTF-16 (16-bit Unicode Transformation Format) is a variable-length encoding using 16-bit code units:

**Key Properties**:
1. **Variable Length**: 2 or 4 bytes per character
2. **Efficient for BMP**: Single 16-bit unit for most common characters
3. **Surrogate Pairs**: Two 16-bit units for characters beyond BMP
4. **Widely Used**: Internal representation in Windows, Java, JavaScript

### 5.2 UTF-16 Encoding Structure

```
Code Point Range         | Code Units | Representation
-------------------------|------------|------------------
U+0000   to U+D7FF       | 1          | Direct mapping
U+D800   to U+DFFF       | Invalid    | Reserved for surrogates
U+E000   to U+FFFF       | 1          | Direct mapping
U+10000  to U+10FFFF     | 2          | Surrogate pair
```

### 5.3 Basic Multilingual Plane (BMP) Encoding

For code points U+0000 to U+FFFF (excluding U+D800 to U+DFFF):
- **Direct Mapping**: Code point value = UTF-16 code unit value
- **Example**: U+0C05 (Telugu అ) → UTF-16: 0x0C05

### 5.4 Surrogate Pairs for Supplementary Planes

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

**Surrogate Ranges**:
- **High Surrogates**: 0xD800 to 0xDBFF (1,024 values)
- **Low Surrogates**: 0xDC00 to 0xDFFF (1,024 values)
- **Total Combinations**: 1,024 × 1,024 = 1,048,576 code points

### 5.5 UTF-16 Encoding Algorithm

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

### 5.6 UTF-16 Decoding Algorithm

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

### 5.7 UTF-16 Example: Emoji "😀" (U+1F600)

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

---

## 6. Endianness and Byte Order

### 6.1 Understanding Endianness

Endianness refers to the order in which bytes are stored in memory for multi-byte data types.

**Origin**: The term comes from Jonathan Swift's "Gulliver's Travels" (1726), referring to which end of an egg should be cracked first.

### 6.2 Big-Endian vs Little-Endian

```
Consider the 32-bit number: 0x12345678

Memory Address:    0x00    0x01    0x02    0x03
Big-Endian:        0x12    0x34    0x56    0x78
Little-Endian:     0x78    0x56    0x34    0x12

Most Significant Byte (MSB): 0x12
Least Significant Byte (LSB): 0x78
```

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

### 6.3 Endianness in UTF-16

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

### 6.4 Byte Order Mark (BOM)

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

**Important Notes**:
- UTF-8 BOM is **optional** and **not recommended** (breaks ASCII compatibility)
- UTF-16 and UTF-32 BOMs are **recommended** for disambiguation
- If no BOM: UTF-16 defaults to **big-endian** per RFC 2781
- BOM should **not** be displayed as a visible character

### 6.5 UTF-16 with Endianness Example

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

### 6.6 Why UTF-8 Doesn't Need Endianness

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

## 7. Telugu Script in Unicode

### 7.1 Telugu Unicode Block

**Range**: U+0C00 to U+0C7F (128 code points)
**Plane**: Basic Multilingual Plane (BMP)
**Script**: Telugu

The Telugu Unicode block contains:
- Independent vowels (స్వరాలు)
- Consonants (హల్లులు)
- Dependent vowel signs (gunintamulu)
- Virama/Halant (combining character)
- Special symbols and digits

### 7.2 Telugu Character Categories

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

### 7.3 Sample Telugu Character Encodings

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

### 7.4 Complex Telugu Character Formation

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

### 7.5 Telugu Text Rendering Process

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

## 8. Conversion Algorithms

### 8.1 Unicode to UTF-8 Conversion (Complete)

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

### 8.2 UTF-8 to Unicode Conversion (Complete)

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

### 8.3 Unicode to UTF-16 Conversion (Complete)

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

### 8.4 UTF-16 to Unicode Conversion (Complete)

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

### 8.5 UTF-8 to UTF-16 Direct Conversion

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

### 8.6 UTF-16 to UTF-8 Direct Conversion

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

---

## 9. Operating System and Machine-Level Processing

### 9.1 How the OS Handles Character Encoding

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

### 9.2 Operating System Specific Behavior

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

### 9.3 Memory Representation

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

### 9.4 Font Rendering Pipeline

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

### 9.5 Processor-Level Byte Handling

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

### 9.6 System Call Examples

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

## 10. Implementation Considerations

### 10.1 String Representation in Memory

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

### 10.2 Character Boundary Detection

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

### 10.3 Validation

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

### 10.4 Performance Considerations

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

### 10.5 Error Handling Strategies

**Replacement Character**:
```
Invalid sequence → U+FFFD (�) REPLACEMENT CHARACTER
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

1. **Unicode** provides a universal character repertoire with consistent code point assignments
2. **UTF-8** is byte-oriented, ASCII-compatible, and the de facto standard for text interchange
3. **UTF-16** is efficient for BMP characters but requires surrogate pairs for supplementary planes
4. **Endianness** matters for multi-byte encodings (UTF-16, UTF-32) but not for UTF-8
5. **Telugu script** (U+0C00-U+0C7F) is in the BMP and requires 3 bytes in UTF-8, 2 bytes in UTF-16
6. **Conversion algorithms** between encodings follow well-defined mathematical transformations
7. **Operating systems** handle encodings differently (Windows: UTF-16, Linux/macOS: UTF-8)

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
