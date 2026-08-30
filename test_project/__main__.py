from src.parser.schema.SchemaFunDefn import SchemaFunDefn
from src.parser.schema.SchemaPrompt import SchemaPromte


class A:
    @staticmethod
    def test_scheam() -> None:
        print(SchemaPromte(age='12'))
        print(SchemaFunDefn(age=12))

if __name__ == "__main__":
    ss = A()
    print("Sss")
    ss.test_scheam()
