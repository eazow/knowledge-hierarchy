import pandas as pd


def get_phones_by_credit_code():
    phones_by_credit_code = {}
    reader = pd.ExcelFile("students.xls")
    sheet_names = reader.sheet_names
    for i, _ in enumerate(sheet_names):
        df = reader.parse(sheet_name=sheet_names[i])

        for _, row in df.iterrows():
            phones_by_credit_code[row["证件号码"]] = row["联系电话"]

    return phones_by_credit_code


def add_phone_col():
    phones_by_credit_code = get_phones_by_credit_code()

    with pd.ExcelWriter("核酸学生名册_电话.xls") as writer:
        excel_reader = pd.ExcelFile("核酸学生名册.xls")
        sheet_names = excel_reader.sheet_names
        for i, sheet_name in enumerate(sheet_names):
            df = excel_reader.parse(sheet_name=sheet_names[i])

            for _, row in df.iterrows():
                df["联系电话"] = df["证件号码"].map(lambda x: phones_by_credit_code.get(x, ""))

            df.to_excel(writer, sheet_name=sheet_name, index=False)

        writer.save()


if __name__ == "__main__":
    add_phone_col()
