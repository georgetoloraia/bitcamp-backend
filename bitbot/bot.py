import discord, copy, os

# Each "service channel" representation
channels = {}

# Custom types for questions
class InputType:
    Text = 0x1
    Choice = 0x2
    Attachment = 0x3

# Each "service channel" will be represented in the memmory in this format 
CHANNEL_TEMPLATE = {
    "user_id": None,
    "question": 0,     # Pointer to questions list
    "answers": {},     # List of answers
    "done": False,     # Finished answering questions
    "confirmed": False # Finished registration
}

class Client(discord.Client):
    def __init__(self, *, intents, questions, **options):
        super().__init__(intents=intents, **options)
        
        self.questions = questions
    
    # When the Discord bot is ready
    async def on_ready(self):
        print(f"[BitBot] Logged on as {self.user}!")
        
    # Proceed to the next question
    async def next_question(self, channel):
        channel_data = channels[channel.id]
        
        if channel_data["confirmed"]:
            await channel.send("დამთავრდა რეგისტრაცია")
            # Here we can save the registration data in our databse
            print("დამთავრდა რეგისტრაცია, პასუხები:", channel_data["answers"])
            return
        
        try:
            question = self.questions[channel_data["question"]]
        except IndexError:
            # If there was an IndexError, that means the last question
            # was answered, so we prompt for confirmation
            channel_data["done"] = True
            await self.prompt_confirm(channel)
            return
        
        # If its a text question
        if question["input_type"] == InputType.Text:
            await channel.send(question["title"])
            
        # If its a attachment question
        if question["input_type"] == InputType.Attachment:
            await channel.send(question["title"])
        
        # If its a choice question (buttons)
        if question["input_type"] == InputType.Choice:
            if "if_answer" in question:
                if not channel_data["answers"][question["if_answer"]["label"]] in question["if_answer"]["is_value"]:
                    channel_data["question"] += 1
                    await self.next_question(channel)
                    return
                
            question_embed = discord.Embed(
                title=question["title"],
                description=question["description"],
                color=0x7289DA
            )
            
            row = discord.ui.View()
            for choice in question["choices"]:
                row.add_item(
                    discord.ui.Button(style=discord.ButtonStyle.blurple, label=choice, custom_id=choice)
                )
            
            await channel.send(embed=question_embed, view=row)
    
    # Prompt for confirmation of answers
    async def prompt_confirm(self, channel):
        channel_data = channels[channel.id]
        answers = channel_data["answers"]
        
        answers_summary = []
        choices = []
        
        for answer in answers:
            answers_summary.append(
                f"**{answer}** - {answers[answer]}"
            )
            choices.append(
                f"შეცვალე {answer}"
            )
        
        confirm_embed = discord.Embed(
            title="სწორია ყველაფერი?",
            description="\n".join(answers_summary),
            color=0x7289DA
        )
        
        # This buttons have special keywords in their custom_id
        # Avoid using exact same keyword custom_id in actual choice questions
        
        row = discord.ui.View()
        row.add_item(
            discord.ui.Button(style=discord.ButtonStyle.green, label="დადასტურება", custom_id="CONFIRM")
        )
        for choice in choices:
            row.add_item(
                discord.ui.Button(style=discord.ButtonStyle.blurple, label=choice, custom_id=f"CHANGE_{choices.index(choice)}")
            )
        
        await channel.send(embed=confirm_embed, view=row)

    # Listen for new users joining the server
    async def on_member_join(self, member):
        channel = await member.guild.create_text_channel(f"{member.name}")
        
        await channel.set_permissions(
            member,
            overwrite=discord.PermissionOverwrite(view_channel=True, read_messages=True)
        )
        await channel.set_permissions(
            member.guild.default_role,
            overwrite=discord.PermissionOverwrite(read_messages=False)
        )
        
        await channel.send(f"{member.mention} კეთილი იყოს თქვენი ფეხი BitCamp-ში.")
        
        channels[channel.id] = copy.deepcopy(CHANNEL_TEMPLATE)
        channels[channel.id]["user_id"] = member.id
        
        await self.next_question(channel)

    # Listen for interactions (button click, checkboxes, etc)
    async def on_interaction(self, interaction):
        # If its a button click
        if interaction.data["component_type"] == 2:
            # Get the data of our "service channel"
            channel_data = channels[interaction.channel.id]
            
            # Check if the user who sent the interaction is the one we are serving in this channel
            # Check if the registration is over or not
            if interaction.user.id == channel_data["user_id"] and channel_data["confirmed"] == False:
                # Remove the buttons so that the user cannot click them again
                await interaction.message.edit(view=None)
                
                # Get the button ID
                custom_id = interaction.data["custom_id"]
                
                # If on confirmation stage, we check for CHANGE and CONFIRM buttons
                if channel_data["done"] and custom_id.split("_")[0] == "CHANGE":
                    channels[interaction.channel.id]["question"] = int(custom_id.split("_")[1])
                elif channel_data["done"] and custom_id == "CONFIRM":
                    channels[interaction.channel.id]["confirmed"] = True
                # If not on confirmation stage, we accept any buttons
                else:
                    question = self.questions[channel_data["question"]]
                
                    channels[interaction.channel.id]["answers"][question["label"]] = custom_id
                    channels[interaction.channel.id]["question"] += 1
                    
                    await interaction.response.send_message(
                        f"მოინიშნა **{custom_id}**."
                    )
                    
                # We proceed to the next question
                await self.next_question(interaction.channel)

    # Listen for messages on entire server
    async def on_message(self, message):
        # DEBUG #
        if message.channel.id == 1173695205266948136 and message.content == "test me" and message.author.id != 1173667963249897582:
            await message.channel.send(f"{message.author.mention} Ok")
            await self.on_member_join(message.author)
        # DEBUG #
        
        # Check if there was a message sent in one of the "service channels"
        if message.channel.id in channels:
            # Get the data of our "service channel"
            channel_data = channels[message.channel.id]
            
            # If the message author is the user we are serving
            if message.author.id == channel_data["user_id"] and channel_data["confirmed"] == False:
                question = self.questions[channel_data["question"]]
                
                # If we are waiting for a text input
                if question["input_type"] == InputType.Text:
                    channels[message.channel.id]["answers"][question["label"]] = message.content
                
                # If we are waiting for an attachment
                if question["input_type"] == InputType.Attachment:
                    if message.attachments:
                        attachment_url = message.attachments[0].url
                        channels[message.channel.id]["answers"][question["label"]] = attachment_url
                    else:
                        # Handle case where no attachment is provided
                        await message.channel.send("გთხოვთ ატვირთეთ ფაილი")
                        return
                    
                # If on confirmation stage
                if channel_data["done"]:
                    # We return to the last question
                    channels[message.channel.id]["question"] = len(self.questions)
                else:
                    channels[message.channel.id]["question"] += 1
                
                # We proceed to the next question
                await self.next_question(message.channel)

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = Client(
        intents=intents,
        
        # Questions list for testing
        # We will load this from the database
        questions=[
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
                    "front-end-vue",
                    "back-end-python",
                    "back-end-node",
                    "pro",
                    "kids"
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
    )
    
    client.run(os.environ["DISCORD_BOT_TOKEN"])

if __name__ == "__main__":
    main()