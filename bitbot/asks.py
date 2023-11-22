# asks.py
# Discord bot's conversation configuration
# Configure what the Discord bot asks the user

# Custom types for questions
class InputType:
    Text = 0x1
    Choice = 0x2
    Attachment = 0x3

QUESTIONS = [
    {
        "label": "სახელი და გვარი",
        "title": "თქვენი სახელი და გვარი?",
        "description": None,
        "input_type": InputType.Text
    },
    {
        "label": "პირადი ნომერი",
        "title": "თქვენი პირადი ნომერი?",
        "description": None,
        "input_type": InputType.Text
    },
    {
        "label": "თელეფონის ნომერი",
        "title": "თქვენი ტელეფონის ნომერი?",
        "description": None,
        "input_type": InputType.Text
    },
    {
        "label": "ელ.ფოსტის მისამართი",
        "title": "თქვენი ელ.ფოსტის მისამართი?",
        "description": None,
        "input_type": InputType.Text
    },
    {
        "label": "შერჩეული პროგრამა",
        "title": "შეარჩიეთ სასურველი სასწავლო პროგრამა",
        "description":
            "მომსახიურების ტიპების და ფასების ჩამონათვალს იხილავთ ამ ბმულზე: https://bitcamp.ge/programs/about/pricing\n\n"
            "თუ გაქვთ ფასდაკლების/Promo კოდი, გთხოვთ ამ ჩათში მოგვწეროთ და შეგეძლებათ ფასდაკლებით სარგებლობა.",
        "input_type": InputType.Choice,
        "choices": [
            "front-end-react",
            # "front-end-vue",
            "back-end-python",
            "back-end-node",
            "pro",
            # "kids"
        ]
    },
    {
        "label": "შერჩეული პაკეტი",
        
        "if_answer": {
            "label": "შერჩეული პროგრამა",
            "is_value": ["front-end-react", "back-end-python", "back-end-node"]
        },
        
        "title": "აირჩიეთ პაკეტი",
        "description": "აირჩიეთ შერჩეული პროგრამის პაკეტი",
        "input_type": InputType.Choice,
        "choices": [
            "საერთო სამენტორო მომსახურება",
            "პირადი მენტორის აყვანა"
        ]
    },
    {
        "label": "",
        "title": "სწავლის საფასურის ჩარიცხვა",
        "description":
            "თქვენს მიერ შერჩეული მომსახურებისა და ტარიფის მიხედვით ჩარიცხეთ საფასური ქვემოთ მოცემული მონაცემების გამოყენებით.\n\n"
            "ანგარიში: `GE75TB7003815365100012`\n"
            "მიმღები: `ოთარ ზაკალაშვილი`\n"
            "დანიშნულება: თქვენი სახელი და გვარი",
        "input_type": None
    },
    {
        "label": "ქვითარი",
        "title": "ატვირთეთ ქვითრის ფაილი",
        "description": None,
        "input_type": InputType.Attachment
    }
]
