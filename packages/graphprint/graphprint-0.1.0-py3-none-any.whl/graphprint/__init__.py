'''Takes a dictionary in the form {value: amount of value} and prints a graph'''

__version__ = "0.1.0"
__author__ = "Pie Thrower"

# TODO:
# Rework width resize to fit ranges not easily divisible by the width

def print_stats(stats, width, height):
    '''take statistics and print a graph'''
    keys = stats.keys()
    val_min = min(keys)
    val_max = max(keys)
    val_range = val_max - val_min

    data = {}

    # Resize data to correct width
    for value in stats:
        pos = round((value - val_min) / val_range * (width - 1))
        if pos in data:
            data[pos].append(stats[value])
        else:
            data[pos] = [stats[value]]
    for value in data:
        data[value] = sum(data[value]) / len(data[value])

    # Stretch to correct height
    data_max = max(data.values())
    for n in data:
        data[n] *= height / data_max

    # Print data
    print("=" * width)
    for y in reversed(range(height)):
        for x in range(width):
            if x in data and data[x] >= y:
                print("@", end="", flush=True)
            else:
                print(" ", end="", flush=True)
        print()
    print("=" * width)
