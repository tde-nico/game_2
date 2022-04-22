from ursina import *


grounds = []

def generate_ground_from_file(map_file):
    with open('modules\\maps\\' + map_file + '.txt','r') as map_data:
        ground_datas = map_data.read()
        for ground in ground_datas.strip('\n').split('\n'):
            datas = ground.split(' ')
            grounds.append(Entity(
                model = 'cube',
                color = color.rgb(int(datas[5]),int(datas[6]),int(datas[7])),
                x = float(datas[0]),
                y = float(datas[1]),
                scale = (float(datas[2]), float(datas[3]), float(datas[4])),
                collider = 'box'))
    return grounds, ground_datas


def generate_ground_from_data(map_data):
    for ground in map_data:
        datas = ground.split(' ')
        grounds.append(Entity(
            model = 'cube',
            color = color.rgb(int(datas[5]),int(datas[6]),int(datas[7])),
            x = float(datas[0]),
            y = float(datas[1]),
            scale = (float(datas[2]), float(datas[3]), float(datas[4])),
            collider = 'box'))
    return grounds


def generate_entities_from_data(entities_data, direct_generation=False):
    if not direct_generation:
        entities = []
        for entity in entities_data:
            datas = entity.split(' ')
            entities.append(Entity(
                model = 'cube',
                color = color.rgb(int(datas[5]),int(datas[6]),int(datas[7])),
                x = float(datas[0]),
                y = float(datas[1]),
                scale = (float(datas[2]), float(datas[3]), float(datas[4])),
                collider = 'box'))
        return entities
    else:
        return Entity(
                model = 'cube',
                color = color.rgb(int(entities_data[5]),int(entities_data[6]),int(entities_data[7])),
                x = float(entities_data[0]),
                y = float(entities_data[1]),
                scale = (float(entities_data[2]), float(entities_data[3]), float(entities_data[4])),
                collider = 'box')


def watch_entities(entities, entities_data):
    new_entity = 0
    for entity in range(len(entities_data)):
        datas = entities_data[entity].split(' ')
        if len(datas) == 8:
            entities.append(generate_entities_from_data(datas, direct_generation=True))
            new_entity += 1
        else:
            if not int(datas[2]):
                entities[entity-new_entity].disable()
                entities[entity-new_entity] = 0
            else:
                entities[entity-new_entity].x = float(datas[0])
                entities[entity-new_entity].y = float(datas[1])
        
    for entity in entities:
        if entity == 0:
            entities.remove(entity)
    return entities



def list_maps():
    import os
    maps = []
    for map_ in os.listdir('modules\\maps'):
        maps.append(map_[:-4])
    return maps




