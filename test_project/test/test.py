def parse_fsm(text):
    state = "START"
    buffer = []

    for char in text:
        if state == "START":
            if char == "\\":
                state = "Escape"
            elif char == '"':
                state = "Final"
                break
            else:
                buffer.append(char)
                state = "Content"

        elif state == "Content":
            if char == "\\":
                state = "Escape"
            elif char == '"':
                state = "Final"
                break
            else:
                buffer.append(char)

        elif state == "Escape":
            buffer.append(char)
            state = "Content"

    return "".join(buffer), state


def run_tests():
    test_cases = ["hello\"", "hello", "Final"]
    for tes in test_cases:
        print(parse_fsm(tes))

if __name__ == "__main__":
    run_tests()