from interface_common import (
    parse_ascii_banner,
    print_ascii_banner,
    quit_program,
    clear_screen,
    to_previous_menu,
    display,  # InterfaceDisplay instance to format given data from facade
)
import os


def prompt_time_management():
    banner = os.path.join(os.path.dirname(__file__), "banners/tm.txt")
    print_ascii_banner(parse_ascii_banner(banner))
    return input(
        """0: Return to mode menu
1: Make a note
2: Set a task and completion goal
3: Print notes and tasks
4: Complete tasks
5: Print overdue tasks
6: Print SCRUM notes
7: Quit
"""
    )


def run_menu_loop_tm(facade):
    while True:
        choice = prompt_time_management()
        map_choice_to_function(choice, facade)


def map_choice_to_function(choice, facade):
    if choice == "0":
        to_previous_menu(facade)
    elif choice == "1":
        make_a_note(facade)
    elif choice == "2":
        set_a_task(facade)
    elif choice == "3":
        print_contents(facade)
    elif choice == "4":
        complete_task(facade)
    elif choice == "5":
        print_overdue_tasks(facade)
    elif choice == "6":
        print_scrum_notes(facade)
    elif choice == "7":
        quit_program(facade)
    else:
        print("Choice not recognized.")


def make_a_note(facade):
    clear_screen()
    print("0 to cancel\n")
    note = input("Make a note: ")
    if note == "0":
        clear_screen()
        run_menu_loop_tm(facade)
    else:
        facade.update_table_with_note(note)
        clear_screen()


def set_a_task(facade):
    clear_screen()
    print("0 to cancel\n")
    note = input("Set a task: ")
    if note == "0":
        clear_screen()
        run_menu_loop_tm(facade)
    else:
        days_until_completion = input("Set number of days to complete: ")
        facade.update_table_with_task(note, days_until_completion)
        clear_screen()


def print_contents(facade):
    clear_screen()
    table_rows = display.display_all_items(facade)
    if len(table_rows) == 0:
        return
    else:
        for row in table_rows:
            print(row)
        print(2 * "\n")


def complete_task(facade, first_run=True):
    clear_screen()
    print("0 to cancel\n")
    if first_run:
        task_input = input("Enter space delimited task IDs for completion: ")
    else:
        task_input = input("One or more task IDs not found. Please try again: ")

    task_ids = split_tasks(task_input)

    if task_ids[0] == "0":
        clear_screen()
        run_menu_loop_tm(facade)
    elif are_valid_tasks(task_ids, facade.get_all_ids()):
        for task_id in task_ids:
            facade.update_completion(task_id)
        clear_screen()
    else:
        complete_task(facade, False)


# TODO :: CHECK FOR ALREADY COMPLETE TASKS USING DEFINED TASK SCHEMA
def are_valid_tasks(tasks_to_complete, valid_task_ids):
    valid_tasks = []
    invalid_tasks = []
    for task_id in tasks_to_complete:
        if task_id.isdigit() and (int(task_id) in valid_task_ids):
            valid_tasks.append(task_id)
        else:
            invalid_tasks.append(task_id)
    if invalid_tasks:
        return False
    else:
        return True


def split_tasks(input_tasks):
    return input_tasks.split()


def print_overdue_tasks(facade):
    clear_screen()
    table_rows = display.display_overdue_items(facade)
    for row in table_rows:
        print(row)


def print_scrum_notes(facade):
    clear_screen()
    banner = os.path.join(os.path.dirname(__file__), "banners/scrum.txt")
    print_ascii_banner(parse_ascii_banner(banner))
    table_rows = display.display_last_days_items(facade)
    for row in table_rows:
        print(row)
