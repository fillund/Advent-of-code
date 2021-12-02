


def count_increase(inputs: list[str]):
    ints = [int(a) for a in inputs]
    pairs = list(zip(ints[:-1], ints[1:]))
    count = 0
    for pair in pairs:
        if pair[1] > pair[0]:
            count = count + 1
    return count

def count_sliding_window(inputs: list[str]):
    ints = [int(a) for a in inputs]
    triplets = list(zip(ints[:-2], ints[1:-1], ints[2:]))
    sums = [sum(t) for t in triplets]
    count = 0
    prev = sums[0]
    for s in sums[1:]:
        if s > prev:
            count = count + 1
        prev = s
    return count

if __name__ == "__main__":

    with open("2021\Day1.txt") as f:
        data = f.readlines()
        count = count_increase(data)

        print(f"Increases: {count}")
        
        count = count_sliding_window(data)
        print(f"Increases: {count}")

