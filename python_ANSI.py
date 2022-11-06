import time, sys, random

"""
Tutorial
https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html
run it with Console not from IDE integration!
"""


def loading1():
    """
    shows loading progress as percentage in one line
    :return:
    """
    print("Loading...")
    for i in range(0, 100):
        time.sleep(0.005)
        sys.stdout.write(u"\u001b[1000D" + str(i + 1) + "%")  # move cursor of terminal 1000 chars to the left
        sys.stdout.flush()


def loading2(count):
    """
    shows loading progress as [###]
    :param count:
    :return:
    """
    all_progress = [0] * count
    sys.stdout.write("\n" * count)  # Make sure we have space to draw the bars
    while any(x < 100 for x in all_progress):
        time.sleep(0.001)
        # Randomly increment one of our progress values
        unfinished = [(i, v) for (i, v) in enumerate(all_progress) if v < 100]
        index, _ = random.choice(unfinished)
        all_progress[index] += 1

        # Draw the progress bars
        sys.stdout.write(u"\u001b[1000D")  # Move left
        sys.stdout.write(u"\u001b[" + str(count) + "A")  # Move up
        for progress in all_progress:
            width = int(progress / 4)
            print("[" + "#" * width + " " * (25 - width) + "]")


loading1()
loading2(4)
