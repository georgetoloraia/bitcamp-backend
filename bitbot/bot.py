import discord, os

QUESTIONS = [
    "თქვენი სახელი და გვარი?",
    "პირადი ნომერი?",
    "ტელეფონის ნომერი?",
    "ელ.ფოსტის მისამართი?",
    "შერჩეული პროგრამის დასახელება?"
]

channels = {}

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[BitBot] Logged on as {self.user}!")
        
    async def on_member_join(self, member):
        new_channel = await member.guild.create_text_channel(f"{member.name}")
        
        overwrite = discord.PermissionOverwrite(view_channel=True, read_messages=True)
        await new_channel.set_permissions(member, overwrite=overwrite)
        
        overwrite_everyone = discord.PermissionOverwrite(read_messages=False)
        await new_channel.set_permissions(member.guild.default_role, overwrite=overwrite_everyone)

        await new_channel.send(f"{member.mention} კეთილი იყოს თქვენი ფეხი BitCamp-ში.")

        channels[new_channel.id] = {
            "user_id": member.id,
            "question": 0,
            "answers": []
        }
        await new_channel.send(QUESTIONS[channels[new_channel.id]["question"]])
        channels[new_channel.id]["question"] += 1

    async def on_select_option(self, interaction):
        print(interaction)

    async def on_interaction(self, interaction):
        if interaction.data["component_type"] == 2:
            custom_id = interaction.data["custom_id"]
            choice = {"yes": True, "no": False}[custom_id.split("_")[0]]
            if interaction.user.id == channels[interaction.channel.id]["user_id"]:
                if choice == True:
                    await interaction.response.send_message(
                        "ანუ ყველაფერი სწორადაა."
                    )
                if choice == False:
                    await interaction.response.send_message(
                        "თავიდან ვცადოთ მაშინ."
                    )
                    channels[interaction.channel.id]["question"] = 0
                    await interaction.channel.send(QUESTIONS[channels[interaction.channel.id]["question"]])
                    channels[interaction.channel.id]["question"] += 1

    async def on_message(self, message):
        if message.channel.id in channels:
            channel_data = channels[message.channel.id]
            if channel_data["user_id"] == message.author.id:
                if len(channel_data["answers"]) < len(QUESTIONS):
                    channel_data["answers"].append(message.content)

                if channel_data["question"] < len(QUESTIONS):
                    await message.channel.send(QUESTIONS[channel_data["question"]])
                    channel_data["question"] += 1
                else:
                    question_embed = discord.Embed(
                        title="სწორია ყველაფერი?",
                        description=(
                            f"**სახელი და გვარი:** {channel_data['answers'][0]}\n"
                            f"**პირადი ნომერი:** {channel_data['answers'][1]}\n"
                            f"**ტელეფონის ნომერი:** {channel_data['answers'][2]}\n"
                            f"**ელ.ფოსტის მისამართი:** {channel_data['answers'][3]}\n"
                            f"**შერჩეული პროგრამის დასახელება:** {channel_data['answers'][4]}\n"
                        ),
                        color=0x7289DA
                    )

                    buttons = [
                        discord.ui.Button(style=discord.ButtonStyle.primary, label="კი", custom_id=f"yes_{channels[message.channel.id]['question']}"),
                        discord.ui.Button(style=discord.ButtonStyle.primary, label="არა", custom_id=f"no_{channels[message.channel.id]['question']}")
                    ]

                    row = discord.ui.View()
                    row.add_item(buttons[0])
                    row.add_item(buttons[1])

                    await message.channel.send(embed=question_embed, view=row)

def main():
    global on_button_click
    
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = MyClient(intents=intents)
    client.run(os.environ["DISCORD_BOT_TOKEN"])

if __name__ == "__main__":
    main()