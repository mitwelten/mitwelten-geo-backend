import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--version", help="show program version", action="store_true")
parser.add_argument("-d", "--demo", help="run with demo data", action="store_true")
parser.add_argument("-l", "--log", help="", action="store_true")

if __name__ == "__main__":
    args = parser.parse_args()

    if args.version:
        print("0.0.0")

    if args.demo:
        print("Running with demo data")
        #check for demo data
