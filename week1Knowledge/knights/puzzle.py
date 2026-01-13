from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # TODO
    # Base Constraint: A is a Knight if and only if A is not a Knave
    Biconditional(AKnight, Not(AKnave)),

    # A's Statement: "I am both a knight and a knave"
    # A is a Knight if and only if that statement is true
    Biconditional(AKnight, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # TODO
    # Base Constraints
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),

    # A's Statement: "We are both knaves"
    # A is a Knight if and only if (A is a Knave AND B is a Knave)
    Biconditional(AKnight, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # TODO
    # Base Constraints
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),

    # A's Statement: "We are the same kind"
    # This means: (A is Knight AND B is Knight) OR (A is Knave AND B is Knave)
    Biconditional(AKnight, Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave)
    )),

    # B's Statement: "We are of different kinds"
    # This means: (A is Knight AND B is Knave) OR (A is Knave AND B is Knight)
    Biconditional(BKnight, Or(
        And(AKnight, BKnave),
        And(AKnave, BKnight)
    ))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # TODO
    # Base Constraints
    Biconditional(AKnight, Not(AKnave)),
    Biconditional(BKnight, Not(BKnave)),
    Biconditional(CKnight, Not(CKnave)),

    # B says "A said 'I am a knave'."
    # 1. A says "I am a knave": Biconditional(AKnight, AKnave)
    #    (This checks if A's type matches the statement "I am a Knave")
    # 2. B says that: Biconditional(BKnight, ...)
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),

    # B says "C is a knave."
    Biconditional(BKnight, CKnave),

    # C says "A is a knight."
    Biconditional(CKnight, AKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
