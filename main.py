import argparse
import sys

from calculator.service import CalculatorService
from calculator.storage import FileStorage


def get_service() -> CalculatorService:
    return CalculatorService(FileStorage("history.json"))


def main():
    parser = argparse.ArgumentParser(description="Calculator CLI")
    parser.add_argument(
        "--action",
        required=True,
        choices=["calculate", "get-history"],
        help="Action to perform",
    )
    parser.add_argument(
        "--operation",
        help="Operation in format: a,operation,b  e.g. 10,divide,2",
    )
    args = parser.parse_args()

    service = get_service()

    if args.action == "calculate":
        if not args.operation:
            print("Error: --operation is required for calculate action")
            print("Format: --operation=a,operation,b  e.g. --operation=10,divide,2")
            sys.exit(1)

        parts = args.operation.split(",")
        if len(parts) != 3:
            print("Error: --operation must be in format: a,operation,b")
            sys.exit(1)

        raw_a, raw_op, raw_b = parts
        try:
            result = service.calculate(raw_a, raw_b, raw_op)
            print(f"Result: {result.a} {result.operation.value} {result.b} = {result.result}")
            print(f"Duration: {result.duration_ms:.4f} ms")
        except (ValueError, ZeroDivisionError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    elif args.action == "get-history":
        entries = service.get_history()
        if not entries:
            print("No calculations found.")
            return
        print(f"{'ID':<38} {'Operation':<10} {'A':>8} {'B':>8} {'Result':>10}  Timestamp")
        print("-" * 90)
        for e in entries:
            print(f"{e.id:<38} {e.operation:<10} {e.a:>8} {e.b:>8} {e.result:>10}  {e.timestamp}")


if __name__ == "__main__":
    main()
