import discord
import re

def media_embed(media_query, user_query, media_type):
    print(f"[DEBUG] Creating embed for media_type: {media_type}")
    clean_description = re.sub(r'<[^>]+>', '', media_query['description'][:4096])

    embed = discord.Embed(
        title=media_query['title']['english'] or media_query['title']['romaji'],
        url=f"https://anilist.co/{media_type.lower()}/{media_query['id']}",
        description=f"*{clean_description}*",  
        color=discord.Color.purple()
    )
    print("[DEBUG] Embed created")

    embed.set_thumbnail(url=media_query['coverImage']['large'])
    
    # Titles
    embed.add_field(name="English", value=media_query['title']['english'], inline=True)
    embed.add_field(name="Romaji", value=media_query['title']['romaji'], inline=True)
    embed.add_field(name="Native", value=media_query['title']['native'], inline=True)
    
    # Status
    embed.add_field(name="Format", value=media_query['format'], inline=True)
    embed.add_field(name="Status", value=media_query['status'], inline=True)
    embed.add_field(name="Source", value=media_query['source'], inline=True)
    
    # Dates
    start_date = media_query.get('startDate', {})
    year = start_date.get('year')
    month = start_date.get('month')
    day = start_date.get('day')
    if year and month and day:
        start_date_str = f"{year:04d}-{month:02d}-{day:02d}"
    else:
        start_date_str = "Unknown"
    embed.add_field(name="Start Date", value=start_date_str, inline=True)
    
    end_date = media_query.get('endDate', {})
    year = end_date.get('year')
    month = end_date.get('month')
    day = end_date.get('day')
    if year and month and day:
        end_date_str = f"{year:04d}-{month:02d}-{day:02d}"
    else:
        end_date_str = "Ongoing"
    embed.add_field(name="End Date", value=end_date_str, inline=True)
    
    # Media specific fields
    if media_type == "anime":
        embed.add_field(name="Season", value=f"{media_query['season']} {media_query['seasonYear']}", inline=True)
        embed.add_field(name="Episodes", value=media_query['episodes'], inline=True)
        
    elif media_type == "manga":
        embed.add_field(name="Chapters", value=media_query.get('chapters', 'N/A'), inline=True)
        embed.add_field(name="Volumes", value=media_query.get('volumes', 'N/A'), inline=True)


    # Statistics
    embed.add_field(name="Average Score", value=f"{media_query['averageScore']}", inline=True)
    embed.add_field(name="Genres", value=', '.join(media_query['genres']), inline=False)


    # Users' media details
    status_types = {'CURRENT': [], 'REPEATING':[], 'COMPLETED': [], 'PAUSED': [], 'DROPPED': [], 'PLANNING': [], 'NOT IN LIST': []}
    print(f"[DEBUG] Sorting user_query by username")
    
    # Sort users into status buckets first
    for user in user_query:
        status = user['status']
        print(f"[DEBUG] Processing user: {user['username']} with status: {status}")
        if status == 'PLANNING' or status == 'NOT IN LIST':
            display_name = f"{user['username']}"
        elif status == 'COMPLETED':
            display_name = f"{user['username']} {'**'+str(user['score'])+'**' if user['score']!=0 else ''}"
        else:
            display_name = f"{user['username']} [{user['progress']}] {'**'+str(user['score'])+'**' if user['score']!=0 else ''}"
        status_types[status].append((user, display_name))

    # Sort each status bucket as requested
    for status in status_types:
        users_display = status_types[status]
        if status in ['PLANNING', 'NOT IN LIST']:
            # Sort alphabetically
            users_display.sort(key=lambda tup: tup[0]['username'].lower())
        elif status == 'COMPLETED':
            # Sort by score high to low, then alphabetically
            users_display.sort(key=lambda tup: (-tup[0]['score'], tup[0]['username'].lower()))
        else:
            # Sort by progress high to low, then alphabetically
            users_display.sort(key=lambda tup: (-tup[0]['progress'], -tup[0]['score'], tup[0]['username'].lower()))
        # Replace with just display names
        status_types[status] = [tup[1] for tup in users_display]

    for status in status_types:
        if status_types[status]:
            value = ' | '.join(status_types[status])
            embed.add_field(name=f"{status.capitalize()}:", value=value, inline=False)
            print(f"[DEBUG] Added field for status {status}: {value}")

    print(f"[DEBUG] Embed construction complete")
    return embed
