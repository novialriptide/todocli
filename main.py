from colorama import Fore, Back
from todocli.utils import *
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", type=str)
    parser.add_argument("--doc", action="store_true")  # delete on complete
    parser.add_argument("-t", "--today", action="store_true")  # delete on complete

    parser.add_argument("-c", "--complete", type=int)
    parser.add_argument("-u", "--uncomplete", type=int)

    parser.add_argument("-p", "--print", action="store_true")

    return parser.parse_args()


def main():
    validate_tasks()
    args = parse_args()

    data = json.load(open("data/save.json", "r"))
    config = json.load(open("data/config.json", "r"))

    if "current_tasks" not in data or data["current_tasks"] == []:
        add_tasks(config["tasks"])

    data = json.load(open("data/save.json", "r"))

    if args.add:
        for s in data["current_tasks"] + config["tasks"]:
            if s["desc"] == args.add:
                print("Cannot add duplicate task")
                return
            
        if args.today:
            user_add_task(args.add)
            render_template()
            return

        config_add_task(args.add, delete_on_complete=args.doc)
        user_add_task(args.add)
        render_template()

    elif args.print:
        render_template()

    elif args.complete is not None:
        user_complete_task(args.complete, True)
        render_template()

    elif args.uncomplete is not None:
        user_complete_task(args.uncomplete, False)
        render_template()

    else:
        pass


if __name__ == "__main__":
    main()
