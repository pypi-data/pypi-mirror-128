import argparse


def main() -> None:
    from ss_test.sample_size import get_sample_size

    parser = argparse.ArgumentParser(prog="ss-test", description="")

    parser.add_argument("--type", choices={"numeric", "boolean", "ratio"}, default="numeric", help="The type")
    parser.add_argument("--effect", default=20.0, type=float, help="The effect, should be a number/float")

    args = parser.parse_args()

    print("Welcome to test pacakage!")
    print("Calculating effect {} of metric type {}".format(args.effect, args.type))
    print("And Here's your secret result:", get_sample_size(float(args.effect)))


if __name__ == "__main__":
    main()
