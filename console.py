#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""
import cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
import shlex


class HBNBCommand(cmd.Cmd):
    """Defines command interpreter class"""
    prompt = "(hbnb) "

    __models = {"BaseModel": BaseModel,
                "User": User,
                "State": State,
                "City": City,
                "Amenity": Amenity,
                "Place": Place,
                "Review": Review}

    def do_EOF(self, line):
        """Handle EOF"""
        print("")
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Disable repetition of last command when enter key is used"""
        pass

    def do_create(self, line):
        """Creates a new instance of BaseModel, saves it (to the JSON file)
        and prints the id"""
        arg = line.split()

        if len(arg) < 1:
            print("** class name missing **")
            return
        elif arg[0] not in self.__models.keys():
            print("** class doesn't exist **")
            return
        else:
            class_string = arg[0]
            for key, value in self.__models.items():
                if class_string == key:
                    newModel = value()
            storage.new(newModel)
            storage.save()
            print(newModel.id)

    def do_show(self, line):
        """Prints the string representation of an instance
        based on the class name and id"""
        arg = line.split()

        if len(arg) < 1:
            print("** class name missing **")
            return
        elif arg[0] not in self.__models.keys():
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:
            print('** instance id missing **')
            return
        class_string = arg[0]
        model_dict = storage.all()
        model_info = f"{class_string}.{arg[1]}"
        # checkid = model_dict.find(f"{modelName}.{baseid}")
        if model_info not in model_dict:
            print("** no instance found **")
        else:
            obj = model_dict[model_info]
            print(obj)

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""
        arg = line.split()

        if len(arg) < 1:
            print("** class name missing **")
            return
        elif arg[0] not in self.__models.keys():
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:
            print("** instance id missing **")
            return
        class_name = arg[0]
        model_info = f"{class_name}.{arg[1]}"
        model_dict = storage.all()
        checkdict = model_dict.pop(model_info, None)
        if not checkdict:
            print("** no instance found **")
        else:
            storage.save()

    def do_all(self, line):
        """Prints all string representation of all
        instances based or not on the class name"""
        args = line.split()
        if args and args[0] not in self.__models:
            print("** class doesn't exist **")
        else:
            objects = storage.all()
            objlist = []
            if args:
                for obj in objects.values():
                    if type(obj) == self.__models[args[0]]:
                        objlist.append(str(obj))
            else:
                for obj in objects.values():
                    objlist.append(str(obj))
            print(objlist)

    def do_update(self, line):
        """Updates an instance based on the class name
        and id by adding or updating attribute"""
        arg = shlex.split(line)
        if len(arg) < 1:
            print("** class name missing **")
            return
        elif arg[0] not in self.__models.keys():
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:
            print("** instance id missing **")
            return
        elif len(arg) < 3:
            print("** attribute name missing **")
            return
        elif len(arg) < 4:
            print("** value missing **")
            return
        class_string = arg[0]
        class_id = arg[1]
        attribute_name = arg[2]
        try:
            attribute_value = int(arg[3])
        except Exception:
            try:
                attribute_value = float(arg[3])
            except Exception:
                attribute_value = str(arg[3]).strip('\'"')
        objects = storage.all()

        model_info = f"{class_string}.{class_id}"
        if model_info not in objects:
            print("** no instance found **")
        else:
            obj = objects[model_info]
            setattr(obj, attribute_name, attribute_value)

            obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
