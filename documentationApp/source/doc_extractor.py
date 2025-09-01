import inspect
from typing import Optional


class MethodDoc:
    def __init__(self, name: str, docstring: Optional[str]):
        self.name = name
        self.docstring = docstring

    def __repr__(self):
        return f"MethodDoc(name={self.name!r})"


class ClassDoc:
    def __init__(self, name: str, docstring: Optional[str], methods: list[MethodDoc]):
        self.name = name
        self.docstring = docstring
        self.methods = methods

    def __repr__(self):
        return f"ClassDoc(name={self.name!r}, methods={self.methods!r})"


class FunctionDoc:
    def __init__(self, name: str, docstring: Optional[str]):
        self.name = name
        self.docstring = docstring

    def __repr__(self):
        return f"FunctionDoc(name={self.name!r})"


class ModuleDoc:
    def __init__(self, module):
        self.module = module
        self.module_docstring = inspect.getdoc(module)
        self.functions = self._extract_functions()
        self.classes = self._extract_classes()

    def _extract_functions(self) -> list[FunctionDoc]:
        return [
            FunctionDoc(name, inspect.getdoc(func))
            for name, func in inspect.getmembers(self.module, inspect.isfunction)
            if func.__module__ == self.module.__name__
        ]

    def _extract_classes(self) -> list[ClassDoc]:
        class_docs = []

        for cls_name, cls_obj in inspect.getmembers(self.module, inspect.isclass):
            if cls_obj.__module__ != self.module.__name__:
                continue

            class_doc = inspect.getdoc(cls_obj)
            method_docs = []

            for attr_name, attr_value in cls_obj.__dict__.items():
                if isinstance(attr_value, (classmethod, staticmethod)):
                    func = attr_value.__func__
                elif inspect.isfunction(attr_value):
                    func = attr_value
                else:
                    continue

                if func.__module__ == self.module.__name__:
                    method_docs.append(MethodDoc(attr_name, inspect.getdoc(func)))

            class_docs.append(ClassDoc(cls_name, class_doc, method_docs))

        return class_docs

    def __repr__(self):
        return f"ModuleDoc(functions={self.functions!r}, classes={self.classes!r})"
