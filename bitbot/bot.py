import discord, copy, os

channels = {}

class InputType:
    Text = 1
    Choice = 2

CHANNEL_TEMPLATE = {
    "user_id": None,
    "question": 0,
    "answers": None
}

ANSWERS = [
    {
        "label": "სახელი და გვარი",
        "value": None
    },
    {
        "label": "პირადი ნომერი",
        "value": None
    },
    {
        "label": "თელეფონის ნომერი",
        "value": None
    },
    {
        "label": "ელ.ფოსტის მისამართი",
        "value": None
    },
    {
        "label": "შერჩეული პროგრამის დასახელება",
        "value": None
    },
]

QUESTIONS = [
    {
        "title": "თქვენი სახელი და გვარი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "title": "თქვენი პირადი ნომერი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "title": "თქვენი ტელეფონის ნომერი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
        "title": "თქვენი ელ.ფოსტის მისამართი?",
        "description": None,
        "input_type": InputType.Text,
        "choices": None
    },
    {
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
    }
]

class Client(discord.Client):
    async def on_ready(self):
        print(f"[BitBot] Logged on as {self.user}!")
        
    async def next_question(self, channel):
        channel_data = channels[channel.id]
        
        try:
            question = QUESTIONS[channel_data["question"]]
        except IndexError:
            await self.prompt_confirm(channel)
            return False
        
        if question["input_type"] == InputType.Text:
            await channel.send(question["title"])
        
        if question["input_type"] == InputType.Choice:
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
    
    async def prompt_confirm(self, channel):
        channel_data = channels[channel.id]
        answers = channel_data["answers"]
        
        answers_summary = []
        choices = []
        
        for answer in answers:
            answers_summary.append(
                f"**{answer['label']}** - {answer['value']}"
            )
            choices.append(
                f"შეცვალე {answer['label']}"
            )
        
        confirm_embed = discord.Embed(
            title="სწორია ყველაფერი?",
            description="\n".join(answers_summary),
            color=0x7289DA
        )
        
        row = discord.ui.View()
        row.add_item(
            discord.ui.Button(style=discord.ButtonStyle.green, label="დადასტურება", custom_id="confirm")
        )
        for choice in choices:
            row.add_item(
                discord.ui.Button(style=discord.ButtonStyle.blurple, label=choice, custom_id=choice)
            )
        
        await channel.send(embed=confirm_embed, view=row)

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
        channels[channel.id]["answers"] = copy.deepcopy(ANSWERS)
        
        await self.next_question(channel)

    async def on_interaction(self, interaction):
        if interaction.data["component_type"] == 2:
            channel_data = channels[interaction.channel.id]
            
            if interaction.user.id == channel_data["user_id"]:
                await interaction.message.edit(view=None)
                    
                custom_id = interaction.data["custom_id"]
                question = channel_data["question"]
                
                channels[interaction.channel.id]["answers"][question]["value"] = custom_id
                channels[interaction.channel.id]["question"] += 1
                
                await interaction.response.send_message(
                    f"მოინიშნა **{custom_id}**."
                )
                
                await self.next_question(interaction.channel)

    async def on_message(self, message):
        # DEBUG #
        if message.channel.id == 1173695205266948136 and message.content == "test me" and message.author.id != 1173667963249897582:
            await message.channel.send(f"{message.author.mention} Ok")
            await self.on_member_join(message.author)
        # DEBUG #
        
        if message.channel.id in channels:
            channel_data = channels[message.channel.id]
            
            if message.author.id == channel_data["user_id"]:
                question = QUESTIONS[channel_data["question"]]
                
                if question["input_type"] == InputType.Text:
                    channels[message.channel.id]["answers"][channel_data["question"]]["value"] = message.content
                    channels[message.channel.id]["question"] += 1
                    
                    await self.next_question(message.channel)

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = Client(intents=intents)
    client.run(os.environ["DISCORD_BOT_TOKEN"])

if __name__ == "__main__":
    main()