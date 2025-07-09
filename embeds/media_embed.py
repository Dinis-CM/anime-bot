import discord

async def send_media_message(interaction, media_search_results, users_search_results, media_type):

    embed = discord.Embed(
        title=media_search_results['title']['english'] or media_search_results['title']['romaji'],
        url=f"https://anilist.co/{media_type.lower()}/{media_search_results['id']}",
        description=media_search_results['description'][:4096],  # Discord embed desc limit
        color=discord.Color.purple()
    )
    embed.set_thumbnail(url=media_search_results['coverImage']['large'])

    #Titles
    embed.add_field(name="English", value=media_search_results['title']['english'], inline=True)
    embed.add_field(name="Romaji", value=media_search_results['title']['romaji'], inline=True)
    embed.add_field(name="Native", value=media_search_results['title']['native'], inline=True)

    print("2")

    #Status
    embed.add_field(name="Format", value=media_search_results['format'], inline=True)
    embed.add_field(name="Status", value=media_search_results['status'], inline=True)
    embed.add_field(name="Source", value=media_search_results['source'], inline=True)

    #Dates
    embed.add_field(name="Start Date", value=f"{media_search_results['startDate']['year']:04d}-{media_search_results['startDate']['month']:02d}-{media_search_results['startDate']['day']:02d}", inline=True)
    end_date = media_search_results.get('endDate', {})
    if end_date.get('year'):
        end_date_str = f"{end_date['year']:04d}-{end_date['month']:02d}-{end_date['day']:02d}"
    else:
        end_date_str = "Ongoing"
    embed.add_field(name="End Date", value=end_date_str, inline=True)

    #Media specific fields
    if media_type == "anime":
        embed.add_field(name="Season", value=f"{media_search_results['season']} {media_search_results['seasonYear']}", inline=True)
        embed.add_field(name="Episodes", value=media_search_results['episodes'], inline=True)
    elif media_type == "manga":
        embed.add_field(name="Chapters", value=media_search_results.get('chapters', 'N/A'), inline=True)
        embed.add_field(name="Volumes", value=media_search_results.get('volumes', 'N/A'), inline=True)

    #Statistics
    embed.add_field(name="Average Score", value=f"{media_search_results['averageScore']}", inline=True)
    embed.add_field(name="Genres", value=', '.join(media_search_results['genres']), inline=False)
    
    # Users' media details
    status_types = {}
    for user in users_search_results:
        if user['status'] == 'PLANNING' or user['status'] == 'NOT IN LIST':
            display_name = f"{user['username']}  | "
        elif user['status'] == 'COMPLETED': 
            display_name = f"{user['username']} {'**'+str(user['score'])+'**' if user['score']!=0 else ''}  | "
        else:
            display_name = f"{user['username']} [{user['progress']}] {'**'+str(user['score'])+'**' if user['score']!=0 else ''} | "
        if user['status'] not in status_types:
            status_types[user['status']] = []
        status_types[user['status']].append(display_name)

    for status in status_types:
        embed.add_field(name=f"{status.capitalize()}:", value=' '.join(status_types[status]), inline=False)

    await interaction.followup.send(embed=embed)



