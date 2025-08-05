import discord

def affinity_embed(affinity, username):
    print(f"Creating affinity embed for {username} with {len(affinity)} users")

    embed = discord.Embed(
        title=f"Affinity Results for {username}",
        color=discord.Color.green()
    )

    # Sort users by anime, manga, and total correlation
    anime_sorted = sorted(affinity, key=lambda x: x['anime_correlation'], reverse=True)
    manga_sorted = sorted(affinity, key=lambda x: x['manga_correlation'], reverse=True)
    total_sorted = sorted(affinity, key=lambda x: x['total_correlation'], reverse=True)

    # Build field values
    anime_field = ""
    for user in anime_sorted:
        anime_field += (
            f"{user['user'].capitalize()}: {user['anime_correlation'] * 100:.2f}% "
            f"({user['number_common_anime']})\n"
        )

    manga_field = ""
    for user in manga_sorted:
        manga_field += (
            f"{user['user'].capitalize()}: {user['manga_correlation'] * 100:.2f}% "
            f"({user['number_common_manga']})\n"
        )

    total_field = ""
    for user in total_sorted:
        total_field += (
            f"{user['user'].capitalize()}: {user['total_correlation'] * 100:.2f}% "
            f"({user['number_common_anime'] + user['number_common_manga']})\n"
        )

    # Add fields to embed
    embed.add_field(name="Anime Correlation", value=anime_field or "No data", inline=False)
    embed.add_field(name="Manga Correlation", value=manga_field or "No data", inline=False)
    embed.add_field(name="Total Correlation", value=total_field or "No data", inline=False)

    embed.set_footer(text="Affinity % (Number of common entries)")

    print(f"Affinity embed created for {username}")

    return embed