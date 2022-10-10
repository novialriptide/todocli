import json
import datetime
from typing import List

dt = datetime.datetime.now()
date_str = datetime.date.today().strftime("%m/%d/%Y")


def validate_tasks():
    config = json.load(open("data/config.json", "r"))
    data = json.load(open("data/save.json", "r"))
    previous_tasks = json.load(open("data/previous_tasks.json", "r"))
    if config["last_opened_day"] != date_str:
        previous_tasks["previous_tasks"][config["last_opened_day"]] = data["current_tasks"]
        data["current_tasks"] = []
        add_tasks(config["tasks"])
        config["last_opened_day"] = date_str
    
        for i, t in enumerate(config["tasks"]):
            if t["delete_queue"]:
                del config["tasks"][i]

    json.dump(data, open("data/save.json", "w"), indent=4)
    json.dump(config, open("data/config.json", "w"), indent=4)
    json.dump(previous_tasks, open("data/previous_tasks.json", "w"), indent=4)


def user_complete_task(index: int, completed: bool):
    config = json.load(open("data/config.json", "r"))
    data = json.load(open("data/save.json", "r"))
    data["current_tasks"][index]["completed"] = completed
    
    for i, t in enumerate(config["tasks"]):
        if t["delete_on_complete"] and t["desc"] == data["current_tasks"][index]["desc"]:
            config["tasks"][i]["delete_queue"] = data["current_tasks"][index]["completed"]

    json.dump(data, open("data/save.json", "w"), indent=4)
    json.dump(config, open("data/config.json", "w"), indent=4)


def user_add_task(desc: str):
    data = json.load(open("data/save.json", "r"))
    task = {"completed": False, "desc": desc}
    data["current_tasks"].append(task)
    json.dump(data, open("data/save.json", "w"), indent=4)


def add_tasks(tasks: List[dict]) -> bool:
    data = json.load(open("data/save.json", "r"))
    config = json.load(open("data/config.json", "r"))
    current_tasks = []
    for i in range(len(tasks)):
        if config["tasks"][i]["active_days"][dt.strftime("%A").lower()]:
            task = {"completed": False, "desc": config["tasks"][i]["desc"]}
            current_tasks.append(task)

    data["current_tasks"] = []
    data["current_tasks"] = current_tasks
    json.dump(data, open("data/save.json", "w"), indent=4)


def config_add_task(desc: str, delete_on_complete=False):
    config = json.load(open("data/config.json", "r"))
    build = {
        "desc": desc,
        "enabled": True,
        "delete_on_complete": delete_on_complete,
        "delete_queue": False,
        "active_days": {
            "sunday": True,
            "monday": True,
            "tuesday": True,
            "wednesday": True,
            "thursday": True,
            "friday": True,
            "saturday": True,
        },
    }
    config["tasks"].append(build)

    json.dump(config, open("data/config.json", "w"), indent=4)


def render_template() -> str:
    data = json.load(open("data/save.json", "r"))
    config = json.load(open("data/config.json", "r"))
    username = config["username"]
    date = None
    time_str = None
    temperature = None
    weather = None
    current_tasks = data["current_tasks"]
    config_tasks = config["tasks"]

    rendered_tasks = []
    for i, t in enumerate(current_tasks):
        marker = "x" if t["completed"] else " "
        desc = t["desc"]
        line = f"= {i} [{marker}] {desc}"
        rendered_tasks.append(line)
    rendered_tasks = "\n".join(rendered_tasks)

    lines = [
        f"[BORDER]",
        f"| Welcome, {username}",
        f"[BORDER]",
        f"# Tasks for Today",
        f"[BORDER]",
        f"{rendered_tasks}",
        f"[BORDER]",
    ]

    divider_length = 0
    for x in lines:
        max_length = len(max(x.split("\n")))
        if max_length > divider_length:
            divider_length = max_length

    divider = divider_length * "="

    for i, x in enumerate(lines):
        if x == "[BORDER]":
            lines[i] = divider

    for l in lines:
        print(l)
