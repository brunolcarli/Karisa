import discord
from pygicord import Paginator
from discord.ext import commands
from request_api import buscar_dados
from settings import API_KEY

bot = commands.Bot(command_prefix='~>')

@bot.event
async def on_ready():
  print('Estou online!')

@bot.command(aliases=["pic", "photo"])
##Retorna a foto do dia publicada pela NASA
async def picture(ctx):
  daily_picture = buscar_dados("https://api.nasa.gov/planetary/apod?api_key={}".format(API_KEY))
  url = daily_picture['url']
  embed = discord.Embed(color=0x1E1E1E, type='rich')
  if('copyright' in daily_picture):
    embed.add_field(name="Autor", value=daily_picture['copyright'], inline=False)
  embed.add_field(name="Titulo", value=daily_picture['title'], inline=False)
  embed.set_image(url = url)
  print(len(daily_picture['explanation']))
  if(len(daily_picture['explanation']) in daily_picture < 1024):
    embed.add_field(name="Descrição", value=daily_picture['explanation'], inline=False)
  else:
    embed.add_field(name="Descrição", value="Infelizmente não posso enviar mais de 1024 caracteres nesse embed, para acompanhar a descrição tente pesquisar o título desta foto no google.", inline=False)
  await ctx.send('', embed=embed)

#Cria as páginas de esteróides
def get_pages():
    listar_asteroides = buscar_dados("https://api.nasa.gov/neo/rest/v1/neo/browse?api_key={}".format(API_KEY))
    asteroides = listar_asteroides['near_earth_objects']
    pages = []
    for asteroide in asteroides:
      embed = discord.Embed(color=0x1E1E1E, type='rich')
      embed.add_field(name="Id", value=asteroide[f'id'], inline=False)
      embed.add_field(name="Nome", value=asteroide[f'name'], inline=False)
      embed.set_footer(text="Para mais informações use ~>search id")
      pages.append(embed)
    return pages

#Lista todos os asteroides em um embed
@bot.command(aliases=["listar", "asteroides"])
async def neo_asteroides(ctx):
  paginator = Paginator(pages=get_pages())
  await paginator.start(ctx)

#Retorna informações de asteróides monitorados pela NASA pelo ID
@bot.command(aliases=["procurar", "search", "neo"])
async def neoWs(ctx, id_asteroide):
  id_asteroide = id_asteroide
  asteroide = buscar_dados("https://api.nasa.gov/neo/rest/v1/neo/{}?api_key={}".format(id_asteroide, API_KEY))
  embed = discord.Embed(color=0x1E1E1E, type='rich')
  embed.add_field(name="Id", value=asteroide['id'], inline=False)
  embed.add_field(name="Nome", value=asteroide['name'], inline=False)
  embed.add_field(name="Potencialmente Perigoso?", value=asteroide['is_potentially_hazardous_asteroid'], inline=False)
  embed.add_field(name="Magnitude", value=asteroide['absolute_magnitude_h'], inline=False)
  embed.add_field(name="Mais informações", value=asteroide['nasa_jpl_url'], inline=False)
  await ctx.send('Informações do asteroide', embed=embed)