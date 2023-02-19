import argparse
from md_pack.markdown_index import OrderNumber


def main():
    parser = argparse.ArgumentParser(description="markdown typesetting")
    parser.add_argument('-i', '--inplace', default=0)
    parser.add_argument('-c', '--contents', default=0)
    parser.add_argument('-f', '--filepath', default='')
    args = parser.parse_args()
    if args.filepath:
        OrderNumber().main(args.filepath, args.inplace == '1', args.contents == '1')
    else:
        print('args invalid')


if __name__ == '__main__':
    main()
