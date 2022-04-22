from ursina import *
from modules import Player
from modules import Bullet
from modules import Ground
from modules import Server
from modules import Client


#------------------------------ WINDOW SETTINGS ------------------------------#


window_x = window.fullscreen_size[0]-100
window_y = window.fullscreen_size[1]-100

window.borderless = False
window.size = (window_x, window_y)


app = Ursina()
window.color = color.rgb(170,170,170)


camera.orthographic = True
fov = 30
camera.fov = fov


#------------------------------ START SERVER ------------------------------#


function = 0
grounds = []
players = []
servers = []
extra_player = ''

def start_server():
    play_button.disable()
    room_button.disable()
    
    global function
    global grounds
    global players
    global server
    global extra_player

    maps = Ground.list_maps()
    my_x = -15
    my_y = 0
    options_data =[]

    with open('options.txt','r') as options:
        for option in options.readlines():
            options_data.append(option.strip('\n'))

    server_ip = options_data[0]
    port = int(options_data[1])
    new_player_number = int(options_data[2])
    my_skin = (int(options_data[3].split(' ')[0]), int(options_data[3].split(' ')[1]), int(options_data[3].split(' ')[2]))
    map_number = int(options_data[4])

    
    players = [Player.Player(x=my_x, y=my_y, paint=(my_skin[0],my_skin[1],my_skin[2]))]
    players_datas = str(my_x)+' '+str(my_y)+' 2 2 1 '+str(my_skin[0])+' '+str(my_skin[1])+' '+str(my_skin[2])+'\n'
    grounds, ground_datas = Ground.generate_ground_from_file(maps[map_number])
    
    
    print(server_ip, port, new_player_number)

    for new_player in range(new_player_number):
        servers.append(Server.Server(server_ip, port - new_player))
        skin_color = servers[new_player].reliable_recive().split(' ')
        servers[new_player].reliable_send(ground_datas)
        new_player_x = -my_x+my_x*(new_player+1)
        new_player_y = 0
        players.append(Player.Player(x=new_player_x, y=new_player_y, paint=(int(skin_color[0]),int(skin_color[1]),int(skin_color[2]))))
        players_datas += str(new_player_x)+' '+str(new_player_y)+' 2 2 1 '+str(skin_color[0])+' '+str(skin_color[1])+' '+str(skin_color[2])+'\n'
        
    for server in servers:
        server.reliable_send(players_datas)
        
    function = 1


#------------------------------ PLAY LOOP ------------------------------#


def play():
    entities_data = ''
    my_keystrokes = str(held_keys['a'])+str(held_keys['d'])+str(held_keys['k'])+str(held_keys['left shift'])+str(held_keys['space'])+str(held_keys['escape'])
    keys = [my_keystrokes]

    for server in range(len(servers)):
        keystrokes = servers[server].reliable_recive()
        if keystrokes[-1] == '1':
            servers[server].connection.close()
            servers[server] = 0
        else:
            keys.append(keystrokes)

    for server in range(len(servers)):
        if servers[server] == 0:
            players[server+1].entity.disable()
            players.pop(server+1)
    for server in servers:
        if server == 0:
            servers.remove(server)
            
    for player_num in range(len(players)):
        player = players[player_num]
        player.ground = False
        for ground in grounds:
            if player.entity.intersects(ground).hit:
                player.ground = ground

        player.move(int(keys[player_num][1]), int(keys[player_num][0]), int(keys[player_num][4]))
        
        if int(keys[player_num][3]) and player.left_dashes > 0:
            player.dash()
        if int(keys[player_num][2]) and player.left_bullets > 0:
            shot, shot_data = player.shoot()
            bullets.append(shot)
            entities_data+=str(shot_data[0])+' '+str(shot_data[1])+' '+str(shot_data[2][0])+' '+str(shot_data[2][1])+' '+str(shot_data[2][2])+' '+str(shot_data[3][0])+' '+str(shot_data[3][1])+' '+str(shot_data[3][2])+'\n'
        if (player.entity.y < (-fov/2 -3)) or (player.entity.x > (fov + 1)) or (player.entity.x < (-fov + 1)):
            player.respawn()


    for bullet_num in range(len(bullets)):
        bullet = bullets[bullet_num]
        if bullet == 0 :
            continue
        elif (bullet.entity.y < (-fov/2 -3)) or (bullet.entity.x > (fov + 1)) or (bullet.entity.x < (-fov + 1)) or bullet.hits <= 0:
            bullets[bullet_num].entity.disable()
            bullets[bullet_num] = 0
        else:
            for ground in grounds:
                if ground.intersects(bullet.entity).hit:
                    bullet.gravity = -bullet.initial_gravity
                    bullet.entity.y = ground.y + ground.scale_y/2 +.2
                    invoke(setattr, bullet, 'gravity', bullet.initial_gravity, delay=(bullet.gravity))
                    bullet.hits -= 1
            bullet.move()
            for player in players:
                if player.entity.intersects(bullet.entity).hit:
                    player.respawn(hitted=True)

                    
    for player in players:
        entities_data += str(player.entity.x) + ' ' + str(player.entity.y) + ' 1\n'
    for bullet in bullets:
        if bullet == 0: 
            entities_data += '0 0 0\n'
        else: 
            entities_data += str(bullet.entity.x) + ' ' + str(bullet.entity.y) + ' 1\n'
    entities_data.strip('\n')
    for server in servers:
        server.reliable_send(entities_data)

    for bullet in bullets:
        if bullet == 0:
            bullets.remove(bullet)


#------------------------------ ENTER ROOM  ------------------------------#


entities = []
client = 0

def enter_room():
    play_button.disable()
    room_button.disable()
    
    global function
    global grounds
    global players
    global client
    global entities

    options_data =[]

    with open('options.txt','r') as options:
        for option in options.readlines():
            options_data.append(option.strip('\n'))
        
    server_ip = options_data[0]
    port = int(options_data[1])
    my_skin = options_data[3]
    
    
    client = Client.Client(server_ip.strip('\n'), int(port))
    client.reliable_send(my_skin)
    get_grounds = client.reliable_recive().split('\n')
    Ground.generate_ground_from_data(get_grounds)
    get_entities = client.reliable_recive().strip('\n').split('\n')
    entities = Ground.generate_entities_from_data(get_entities)

    function = 2


#------------------------------ ROOM LOOP ------------------------------#


def room():
    global entities
    
    keystrokes = str(held_keys['a'])+str(held_keys['d'])+str(held_keys['k'])+str(held_keys['left shift'])+str(held_keys['space'])+str(held_keys['escape'])
    client.reliable_send(keystrokes)
    if keystrokes[-1] == '1':
        client.connection.close()
        exit(0)
    
    get_entities_data = client.reliable_recive().strip('\n').split('\n')
    entities = Ground.watch_entities(entities, get_entities_data)


#------------------------------ MENU LOOP ------------------------------#


my_ip = "192.168.1.230"

play_button = Button(scale=(.5, .25), text='Play', x=0,y=.3)
play_button.on_mouse_enter = Func(setattr, play_button, 'text', my_ip)
play_button.on_mouse_exit = Func(setattr, play_button, 'text', 'Play')

room_button = Button(scale=(.5, .25), text='Enter Room', x=0,y=0)
room_button.on_mouse_enter = Func(setattr, room_button, 'text', my_ip)
room_button.on_mouse_exit = Func(setattr, room_button, 'text', 'Enter Room')

play_button.on_click = start_server
room_button.on_click = enter_room

def menu():
    pass


#------------------------------ UPDATE LOOP ------------------------------#


functions = [menu, play, room]
bullets = []
def update():
    functions[function]()
    
        
#------------------------------ CONTROLS ------------------------------#


input_handler.bind('w', 'space')


#------------------------------ GAMEPAD CONTROLS ------------------------------#


input_handler.bind('gamepad a', 'space')
input_handler.bind('gamepad dpad up', 'space')
input_handler.bind('gamepad dpad left', 'a')
input_handler.bind('gamepad dpad right', 'd')
input_handler.bind('gamepad b', 'left shift')
input_handler.bind('gamepad x', 'k')

#input_handler.bind('gamepad dpad down', 's')
#input_handler.bind('gamepad y', 'l')
#input_handler.bind('gamepad left stick', 'space')


#------------------------------ RUN ------------------------------#


app.run()







