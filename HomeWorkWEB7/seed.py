import argparse
from confa.models import Grade, Teacher, Student, Group, Subject
from confa.db import session


def create(args, model):
    if model == Teacher or Student:
        model = model(fullname=args.name)
    else:
        model = model(name=args.name)
    session.add(model)
    session.commit()
    print(f" in model '{model}' '{args.name}' created successfully.")


def list(args, model):
    models = session.query(model).all()
    for model in models:
        print(f"ID: {model.id}, Name: {args.name}")


def update(args, model):
    model = session.query(model).filter_by(id=args.id).first()
    if model == Teacher or Student:
        name = model.fullname
    else:
        name = model.name
    if model:
        name = args.name
        session.commit()
        print(f"{model} with ID {args.id} updated successfully.")
    else:
        print(f"{model} with ID {args.id} not found.")


def remove(args, model):
    model = session.query(model).filter_by(id=args.id).first()
    if model:
        session.delete(model)
        session.commit()
        print(f"{model} with ID {args.id} removed successfully.")
    else:
        print(f"{model} with ID {args.id} not found.")


def main():
    parser = argparse.ArgumentParser(description="CRUD operations with the database.")
    parser.add_argument(
        "--action",
        "-a",
        choices=["create", "list", "update", "remove"],
        required=True,
        help="CRUD action: create, list, update, or remove.",
    )
    parser.add_argument(
        "--model",
        "-m",
        choices=["Teacher", "Group", "Grade", "Student", "Subject"],
        required=True,
        help="Model to perform CRUD operations on: Grade, Teacher, Student, Group, Subject.",
    )
    parser.add_argument(
        "--id", type=int, help="ID of the record for update or removal."
    )
    parser.add_argument("--name", "-n", type=str, help="Name for creation or update.")

    args = parser.parse_args()

    model_classes = {
        "Grade": Grade,
        "Teacher": Teacher,
        "Subject": Subject,
        "Student": Student,
        "Group": Group,
    }

    model = model_classes.get(args.model)
    if model is None:
        print("Invalid model.")
        return

    if args.action == "create":
        create(args, model)
    elif args.action == "list":
        list(args, model)
    elif args.action == "update":
        update(args, model)
    elif args.action == "remove":
        remove(args, model)
    else:
        print("Invalid action or model.")


if __name__ == "__main__":
    main()
