import discord

def media_embed(media_query, user_query, media_type):
    print(f"[DEBUG] Creating embed for media_type: {media_type}")
    print(f"[DEBUG] Media Query ID: {media_query.get('id')}")
    print(f"[DEBUG] Media Query Title: {media_query['title']}")

    embed = discord.Embed(
        title=media_query['title']['english'] or media_query['title']['romaji'],
        url=f"https://anilist.co/{media_type.lower()}/{media_query['id']}",
        description=media_query['description'][:4096],  # Discord embed desc limit
        color=discord.Color.purple()
    )
    print(f"[DEBUG] Embed created with title: {embed.title}")

    embed.set_thumbnail(url=media_query['coverImage']['large'])
    print(f"[DEBUG] Thumbnail set: {media_query['coverImage']['large']}")

    # Titles
    embed.add_field(name="English", value=media_query['title']['english'], inline=True)
    embed.add_field(name="Romaji", value=media_query['title']['romaji'], inline=True)
    embed.add_field(name="Native", value=media_query['title']['native'], inline=True)
    print(f"[DEBUG] Added title fields")

    # Status
    embed.add_field(name="Format", value=media_query['format'], inline=True)
    embed.add_field(name="Status", value=media_query['status'], inline=True)
    embed.add_field(name="Source", value=media_query['source'], inline=True)
    print(f"[DEBUG] Added status fields")

    # Dates
    start_date_str = f"{media_query['startDate']['year']:04d}-{media_query['startDate']['month']:02d}-{media_query['startDate']['day']:02d}"
    embed.add_field(name="Start Date", value=start_date_str, inline=True)
    print(f"[DEBUG] Start Date: {start_date_str}")

    end_date = media_query.get('endDate', {})
    if end_date.get('year'):
        end_date_str = f"{end_date['year']:04d}-{end_date['month']:02d}-{end_date['day']:02d}"
    else:
        end_date_str = "Ongoing"
    embed.add_field(name="End Date", value=end_date_str, inline=True)
    print(f"[DEBUG] End Date: {end_date_str}")

    # Media specific fields
    if media_type == "anime":
        embed.add_field(name="Season", value=f"{media_query['season']} {media_query['seasonYear']}", inline=True)
        embed.add_field(name="Episodes", value=media_query['episodes'], inline=True)
        print(f"[DEBUG] Added anime-specific fields")
    elif media_type == "manga":
        embed.add_field(name="Chapters", value=media_query.get('chapters', 'N/A'), inline=True)
        embed.add_field(name="Volumes", value=media_query.get('volumes', 'N/A'), inline=True)
        print(f"[DEBUG] Added manga-specific fields")

    # Statistics
    embed.add_field(name="Average Score", value=f"{media_query['averageScore']}", inline=True)
    embed.add_field(name="Genres", value=', '.join(media_query['genres']), inline=False)
    print(f"[DEBUG] Added statistics fields")

    # Users' media details
    status_types = {'CURRENT': [], 'COMPLETED': [], 'PAUSED': [], 'DROPPED': [], 'PLANNING': [], 'NOT IN LIST': []}
    print(f"[DEBUG] Sorting user_query by username")
    user_query = sorted(user_query, key=lambda user: user['username'].lower())
    for user in user_query:
        print(f"[DEBUG] Processing user: {user['username']} with status: {user['status']}")
        if user['status'] == 'PLANNING' or user['status'] == 'NOT IN LIST':
            display_name = f"{user['username']}"
        elif user['status'] == 'COMPLETED': 
            display_name = f"{user['username']} {'**'+str(user['score'])+'**' if user['score']!=0 else ''}"
        else:
            display_name = f"{user['username']} [{user['progress']}] {'**'+str(user['score'])+'**' if user['score']!=0 else ''}"
        status_types[user['status']].append(display_name)

    for status in status_types:
        if status_types[status]:
            value = ' | '.join(status_types[status])
            embed.add_field(name=f"{status.capitalize()}:", value=value, inline=False)
            print(f"[DEBUG] Added field for status {status}: {value}")

    print(f"[DEBUG] Embed construction complete")
    return embed
