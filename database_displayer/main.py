import math
from pathlib import Path
import matplotlib.pyplot as plt

input_question = "Please give the path to the data file: "
parsing_error = "Could not parse path format"
# if none given, defaults to "1-3"
ignore_lines = "1-3, 999-1002, 89-72, 30-31"

# return an array of numbers corresponding to the ignore-lines ranges
def process_ignorance(raw_ignore):
    # enter (empty string) for defaults [1-3]
    if not raw_ignore:
        return [1, 2, 3]
    raw_ignore_split = raw_ignore.replace(" ", "").split(",")
    ranges = []
    processed_numbers = []
    # separate ranges and individual numbers
    for i in range(len(raw_ignore_split)):
        # range
        if "-" in raw_ignore_split[i]:
            ranges.append(raw_ignore_split[i])
        # individual number
        else:
            try:
                number = int(eval(raw_ignore_split[i]))
                assert(number > 0)
                processed_numbers.append(number)
            except:
                # not a valid integer
                print("Could not ignore line '" + str(raw_ignore_split[i]) + "', " + "number not understood")
    # split ranges from [[a, b], [c-d]] to [a, b, c, d] for evaluation purposes 
    for j in range(len(ranges)):
        pair = ranges[j].split("-")
        try:
            # check that range values are positive integers
            first = int(eval(pair[0]))
            assert(first > 0)
            second = int(eval(pair[1]))
            assert(second > 0)
            if first < second:
                # increment from first to second
                for k in range(0, second - first + 1):
                    processed_numbers.append(first + k)
            # if user gives a pair backwards, such as [10-5], read it as [5-10]
            elif first > second:
                for k in range(0, first - second + 1):
                    processed_numbers.append(second + k)
            # interpret ranges [a-a] as individual number a
            else:
                processed_numbers.append(first)
        except:
            # if ignore_lines isn't interpreted correctly, return defaults
            print("Range " + str(pair) + " could not be understood, not ignoring those lines.")
        
        # delete duplicates
        processed_numbers = list(dict.fromkeys(processed_numbers))
    return processed_numbers

# parse input for file location
def input_asker(q):
    try:
        p = Path(input(q))
        # the is_file() method breaks python terminal termination with ctrl + C
        if p.exists() and p.is_file():
            return p
        else:
            print("Given path does not exist")
            return input_asker(q)
    except:
        print(parsing_error)
        return input_asker(q)

# returns P(t) values
def logpower(voltage,current):
    return math.log(voltage * current)

def main(question):
    print("Please give the numbers of the lines you wish to ignore, enter for defaults,")
    ignore = process_ignorance(input("program supports individual numbers and ranges, format example: a, b-f, k-p, q, r, ... etc : "))
    path = input_asker(question)
    f = open(path, "r")
    # save file lines to list
    lines = f.read().splitlines()
    count = 0
    # pop the elements out of the lines array that correspond to the ignore line numbers
    for i in range(len(ignore)):
        # -1 because VSCode lines start counting from 1 but lines[] elements starts from 0
        if ignore[i] - 1 - count < len(lines):
            lines.pop(ignore[i] - 1 - count)
            # lines[] array decreases for each iteration of the loop, so must shrink the ignored line numbers by the iteration count to keep correspondence between the indexes
            count += 1

    processed_lines = []
    for i in range(len(lines)):
        line = lines[i].replace(" ", "").split(",")
        # both values aren't empty strings
        if len(line) > 1:
            if line[0] and line[1]:
                processed_lines.append(line)
                # prints
                print(line)
                print("-----------")
    print("Ignored lines: " + str(ignore))
    print("-----------")
    print("Data: " + str(processed_lines))
    print("-----------")

    times = []
    logs = []
    # create time and p(t) lists
    for i in range(len(processed_lines)):
        times.append(i / 25000)
        try:
            voltage = eval(processed_lines[i][0])
            current = eval(processed_lines[i][1])
            p = logpower(voltage, current)
            logs.append(p)
        except:
            pass

    # graph formatting
    plt.figure()
    plt.title('Log of current * voltage over time graph')
    plt.xlabel('Time (s)')
    plt.ylabel('P(t) = Log(V(t)*I(t))')
    plt.plot(times, logs, c='b') 
    plt.show()

    main(question)

main(input_question)