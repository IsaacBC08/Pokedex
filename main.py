import flet as ft
import aiohttp
import asyncio
import pygame as pg

pokemon_actual = 0

async def main(page: ft.Page):
    alto = 640
    ancho = 360
    page.window_width = ancho
    page.window_height = alto 
    page.window_resizable = True
    page.padding = 0
    page.fonts = {
        "zpix": "https://github.com/SolidZORO/zpix-pixel-font/releases/download/v3.1.8/zpix.ttf"
    }
    page.theme = ft.Theme(font_family="zpix")
    async def peticion(url):
        async with aiohttp.ClientSession() as sesion:
            async with sesion.get(url) as response:
                return await response.json()
            

    async def cambiar(e : ft.ContainerTapEvent):
        global pokemon_actual
        if e.control == flecha_superior:
            pokemon_actual += 1
        else:
            pokemon_actual -=1
        numero = (pokemon_actual % 1024 ) + 1
        resultado = await peticion(f"https://pokeapi.co/api/v2/pokemon/{numero}")
        datos = f"Numero:{numero}\nNombre: {resultado['name']}"
        datos += f"\n\nPeso: {resultado['height']} Lbs"
        texto.value = datos
        
        texto.value = datos    
        sprite_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{numero}.png"
        imagen.src = sprite_url
        select = pg.mixer.Sound("select.mp3")
        pg.mixer.Sound.play(select)
        await page.update_async()
    async def blink():
        while True:
            await asyncio.sleep(0.5)
            luz_azul.bgcolor = ft.colors.BLUE_100
            await page.update_async()
            await asyncio.sleep(0.4)
            luz_azul.bgcolor = ft.colors.BLUE
            await page.update_async()
            
    luz_azul = ft.Container(width=40, height=40,bgcolor=ft.colors.WHITE,border_radius=50)
    boton_azul = ft.Stack([
        luz_azul,
        ft.Container(width=30, height=30,top=5, left=5, bgcolor=ft.colors.BLUE,border_radius=50)
        
        ])
    
    items_superior = [
        ft.Container(boton_azul, width=40, height=40),
        ft.Container(width=20, height=20,border_radius=25, bgcolor=ft.colors.RED_100),
        ft.Container(width=20, height=20,border_radius=25, bgcolor=ft.colors.YELLOW),
        ft.Container(width=20, height=20,border_radius=25, bgcolor=ft.colors.GREEN),
    ]
    sprite_url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png"
    imagen = ft.Image(
        src=sprite_url,
        scale= 6,
        width= 25,
        height= 25,
        top= 175 / 2,
        left= 275 / 2 
        )
    stack_central = ft.Stack([
        ft.Container(width=300, height=200, bgcolor=ft.colors.WHITE, border_radius=50),
        ft.Container(width=275, height=175, bgcolor=ft.colors.BLACK, top=12.5, left=12.5, border_radius=50),
        imagen
    ])
    
    triangulo = ft.canvas.Canvas([
        ft.canvas.Path([
            ft.canvas.Path.MoveTo(20,0),
            ft.canvas.Path.LineTo(0,25),
            ft.canvas.Path.LineTo(40,25)], 
            paint=ft.Paint(
                style=ft.PaintingStyle.FILL,))],
            width=40, height=25)
        
    flecha_superior = ft.Container(triangulo, width=40,height=25, on_click=cambiar)
    flechas = ft.Column([
        flecha_superior,
        ft.Container(triangulo, rotate=ft.Rotate(angle=3.14159),width=40,height=25, on_click=cambiar)
    ])

    texto = ft.Text(value="...",color=ft.colors.BLACK, size=16)

    items_inferior = [
        ft.Container(width=25,  ),        
        ft.Container(texto,padding=10, width=200, height=150, bgcolor=ft.colors.GREEN_500, border_radius=20),
        ft.Container(width=10), 
        ft.Container(flechas, width=40, height=60),
    
    ]


    superior = ft.Container(content=ft.Row(items_superior),width=300, height=40, margin=ft.margin.only(top=20))
    centro = ft.Container(content=stack_central, width=300, height=200, margin=ft.margin.only(top=20), alignment=ft.alignment.center)
    inferior = ft.Container(content=ft.Row(items_inferior), width=300, height=200, margin=ft.margin.only(top=40))

    col = ft.Column(spacing=0, controls=[
        superior,
        centro,
        inferior
    ])
    contenedor = ft.Container(col, width=360, height=640,bgcolor=ft.colors.RED_500, alignment=ft.alignment.top_center )

    await page.add_async(contenedor)
    pg.init()
    pg.mixer.init()
    sonido_fondo = pg.mixer.Sound("main_theme.mp3")
    pg.mixer.Sound.play(sonido_fondo, -1)
    await blink()
ft.app(target=main)
