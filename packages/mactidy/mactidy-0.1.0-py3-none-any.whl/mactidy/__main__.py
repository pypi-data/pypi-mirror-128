import argparse

from mactidy.main import print_hi

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Location to run")
    args = parser.parse_args()
    print_hi(args.path or "/Users/Work/Downloads")
