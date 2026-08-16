#! /usr/bin/python

def php_serialize_strings(values):
    result = [f"a:{len(values)}:{{"]

    for i, value in enumerate(values):
        encoded = value.encode("utf-8")
        result.append(
            f'i:{i};s:{len(encoded)}:"{value}";'
        )

    result.append("}")
    return "".join(result)


# d = php_serialize_strings([
#     "PROPOSITION 039 - ESTABLISHES ADDITIONAL VOTER IDENTIFICATION AND CITIZENSHIP VERIFICATION REQUIREMENTS. INITIATIVE CONSTITUTIONAL AMENDMENT.",
#     "2026-11-03",
#     "2025",
# ])

d = php_serialize_strings([
    "PROPOSITION 039%",
    "2026-11-03",
])

print(d)
