

# import json
# from pydantic import BaseModel, TypeAdapter, ConfigDict
# class Base(BaseModel):
#     prompt: str

# def main():
#     data = ["test3", "test2", "te\\\\st1"]
#     basemodels: list[Base] = list()
#     for prompt in data:
#         basemodels.append(Base(prompt=prompt))
#     ss = TypeAdapter(list[Base])
#     with open("test.json", 'w') as f:
#         jso = ss.dump_json(basemodels).decode("utf-8")

    
# if __name__ == "__main__":
#     main()
import json

# Python string fih quote f-l-bdāya
my_regex = '\"[aeiouAEIOU]'

# Mlli kat-ḥawwlo l-JSON:
json_data = json.dumps({"pattern": my_regex})


print(json_data)
# L-natija f-l-file JSON: {"pattern": " \"[aeiouAEIOU]"}