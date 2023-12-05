# asks.py
# Discord bot's conversation configuration
# Configure what the Discord bot asks the user

from content import models

# Custom types for questions
class InputType:
    Text = 0x1
    Choice = 0x2
    Attachment = 0x3

# Todo: Write documentation for this configuration
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
            program.title for program in models.Program.objects.all()
        ]
    }
]

# This is where it gets complicated
for program in models.Program.objects.all():
    # Here we basically generate a service choice question for each program
    QUESTIONS.append(
        {
            "label": "შერჩეული პაკეტი",
            
            "if_answer": {
                "label": "შერჩეული პროგრამა",
                "is_value": [program.title]
            },
            
            "title": "აირჩიეთ პაკეტი",
            "description": "აირჩიეთ შერჩეული პროგრამის პაკეტი",
            "input_type": InputType.Choice,
            "choices": [
                service.title for service in program.services.all()
            ]
        }
    )
    
    # And here we check if any service has mentors
    for service in program.services.all():
        # If the service has more than 0 mentors then we prompt the user
        # to choose one
        if len(service.mentors.all()) >= 1:
            QUESTIONS.append(
                {
                    "label": "აყვანილი მენტორი",
                    
                    "if_answer": {
                        "label": "შერჩეული პაკეტი",
                        "is_value": [service.title]
                    },
                    
                    "title": "აიყვანეთ მენტორი",
                    "description": "აიყვანეთ პირადი მენტორი",
                    "input_type": InputType.Choice,
                    "choices": [
                        mentor.fullname for mentor in service.mentors.all()
                    ]
                }
            )
