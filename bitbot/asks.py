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
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "label": "პირადი ნომერი",
        "title": "თქვენი პირადი ნომერი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "label": "თელეფონის ნომერი",
        "title": "თქვენი ტელეფონის ნომერი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "label": "ელ.ფოსტის მისამართი",
        "title": "თქვენი ელ.ფოსტის მისამართი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "label": "შერჩეული პროგრამა",
        "title": "შერჩეული პროგრამის დასახელება?",
        "description": "აირჩიეთ შერჩეული პროგრამის დასახელება",
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
        "label": "ქვითარი",
        "title": "ატვირთეთ ქვითრის ფაილი",
        "description": None,
        "input_type": InputType.Attachment
    }
]
