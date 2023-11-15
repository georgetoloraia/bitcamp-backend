import discord, os

QUESTIONS: list = [
    "თქვენი სახელი და გვარი?",
    "პირადი ნომერი?",
    "ტელეფონის ნომერი?",
    "ელ.ფოსტის მისამართი?",
    "შერჩეული პროგრამის დასახელება?"
]

channels: dict = {}
client: discord.Client = None

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

    async def on_message(self, message):
        print("Works")
        
        if message.channel.id in channels:
            channel_data = channels[message.channel.id]
            if channel_data["user_id"] == message.author.id:
                if len(channel_data["answers"]) < len(QUESTIONS):
                    channel_data["answers"].append(message.content)

                if channel_data["question"] < len(QUESTIONS):
                    await message.channel.send(QUESTIONS[channel_data["question"]])
                    channel_data["question"] += 1
                else:
                    await message.channel.send(
                        f"**სახელი და გვარი:** {channel_data['answers'][0]}\n"
                        f"**პირადი ნომერი:** {channel_data['answers'][1]}\n"
                        f"**ტელეფონის ნომერი:** {channel_data['answers'][2]}\n"
                        f"**ელ.ფოსტის მისამართი:** {channel_data['answers'][3]}\n"
                        f"**შერჩეული პროგრამის დასახელება:** {channel_data['answers'][4]}\n\n"
                        "სწორია ყველაფერი?"
                    )

def main():
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    client = MyClient(intents=intents)
    client.run(os.environ["DISCORD_BOT_TOKEN"])

if __name__ == "__main__":
    main()