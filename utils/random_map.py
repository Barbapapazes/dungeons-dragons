import xml.etree.ElementTree as ET
import os
#from config.random import MAP,IMAGE,TILE

os.chdir('./assets/map_random/')

def out_xml(out,width,height,data_Ground,data_Wall,data_Object):


    MAP = {'version': '1.4', 'tiledversion': '1.4.2', 'orientation': 'orthogonal', 'renderorder': 'right-down',
    'width': '0', 'height': '0', 'tilewidth': '64', 'tileheight': '64', 'infinite': '0', 'nextlayerid': '4', 'nextobjectid': '11'}

    TILE = {'firstgid': '1', 'name': 'tile_dungeons', 'tilewidth': '64', 'tileheight': '64', 'tilecount': '18', 'columns': '3'} 

    IMAGE = {'source': '../img/tile_dungeons.png', 'trans': 'ff00ff', 'width': '192', 'height': '384'}

    LAYER_G = {'id': '1', 'name': 'Ground', 'width': '0', 'height': '0'}

    LAYER_W = {'id': '2', 'name': 'Wall', 'width': '0', 'height': '0'}

    DATA = {'encoding': 'csv'}

    OBJ = {'id': '3', 'name': 'Obstacles'}

    MAP["width"] = width
    LAYER_G["width"] = width
    LAYER_W["width"] = width
    MAP["height"] = height
    LAYER_G["height"] = height
    LAYER_W["height"] = height

    map = ET.Element('map')
    tileset = ET.SubElement(map,'tileset')
    image = ET.SubElement(tileset,'image')
    layerG = ET.SubElement(map,'layer')
    dataG =ET.SubElement(layerG,'data')
    layerW = ET.SubElement(map,'layer')
    dataW =ET.SubElement(layerW,'data')
    objectgroup = ET.SubElement(map,'objectgroup')



    for key,val in MAP.items():
        map.set(key,val)

    for key,val in TILE.items():
        tileset.set(key,val)

    for key,val in IMAGE.items():
        image.set(key,val)

    for key,val in LAYER_G.items():
        layerG.set(key,val)
    
    for key,val in LAYER_W.items():
        layerW.set(key,val)

    for key,val in DATA.items():
        dataG.set(key,val)
        dataW.set(key,val)

    dataG.text = data_Ground
    dataW.text = data_Wall

    for key,val in OBJ.items():
        objectgroup.set(key,val)

    for dictObj in data_Object:
        obj = ET.SubElement(objectgroup,'object')
        for key,val in dictObj.items():
            obj.set(key,val)
    
    tree =ET.ElementTree(map)
    tree.write(out)



def fusion_two_map(map1,map2,direction):      # direction prend la valeur right or down (c'est pour savoir comment on place la map 1 par rapport a la deuxieme)
    id_obj=2

    tree1= ET.parse(map1)
    tree2= ET.parse(map2)

    arbo1 = tree1.getroot()
    arbo2 = tree2.getroot()

    width1 = int(arbo1.attrib.get("width"))
    height1 = int(arbo1.attrib.get("height"))
    data_ground1 = arbo1[1][0].text
    dataAnySlash_ground1 = data_ground1.replace('\n','')
    listdata_ground1 = dataAnySlash_ground1.split(',')
    data_wall1 = arbo1[2][0].text
    dataAnySlash_wall1 = data_wall1.replace('\n','')
    listdata_wall1 = dataAnySlash_wall1.split(',')

    listObj1= []
    for obj in arbo1[3]:
        listObj1.append(obj.attrib)
        id_obj += 1

    

    width2 = int(arbo2.attrib.get("width"))
    height2 = int(arbo2.attrib.get("height"))
    data_ground2 = arbo2[1][0].text
    dataAnySlash_ground2 = data_ground2.replace('\n','')
    listdata_ground2 = dataAnySlash_ground2.split(',')
    data_wall2 = arbo2[2][0].text
    dataAnySlash_wall2 = data_wall2.replace('\n','')
    listdata_wall2 = dataAnySlash_wall2.split(',')

    listObj2= []
    for obj in arbo2[3]:
        listObj2.append(obj.attrib)

    
    listdata_groundF=['\n']
    listdata_wallF=['\n']
    
    if direction == "right":
        widthF = width1 + width2
        heightF = max(height1,height2)

        for h in range(heightF):

            for w1 in range(width1):
                listdata_groundF.append(listdata_ground1[w1+h*width1])
                listdata_groundF.append(',')

                listdata_wallF.append(listdata_wall1[w1+h*width1])
                listdata_wallF.append(',')

            for w2 in range(width2):
                listdata_groundF.append(listdata_ground2[w2+h*width2])
                listdata_wallF.append(listdata_wall2[w2+h*width2])
                if (h!=heightF-1 or w2 != width2-1):   
                    listdata_groundF.append(',')
                    listdata_wallF.append(',')

            listdata_groundF.append('\n')
            listdata_wallF.append('\n')

        for obj in listObj2:
            obj['x'] =  str(float(obj['x']) + width1*64)
            obj['id'] = str(id_obj)
            id_obj += 1



    if direction == "down":
        widthF = max(width1,width2)
        heightF = height1 + height2
        i=1

        for M1 in range(width1*height1):
            listdata_groundF.append(listdata_ground1[M1])
            listdata_groundF.append(',')

            listdata_wallF.append(listdata_wall1[M1])
            listdata_wallF.append(',')

            if i == width1:
                listdata_groundF.append('\n')
                listdata_wallF.append('\n')
                i=0
            i+=1

        for M2 in range(width2*height2):
            listdata_groundF.append(listdata_ground2[M2])

            listdata_wallF.append(listdata_wall2[M2])

            if(M2 != width2*height2 -1):
                listdata_groundF.append(',')
                listdata_wallF.append(',')
            if i == width2:
                listdata_groundF.append('\n')
                listdata_wallF.append('\n')
                i=0
            i+=1


        listdata_groundF.append('\n')
        listdata_wallF.append('\n')

        for obj in listObj2:
            obj['y'] =  str(float(obj['y']) + height1*64)
            obj['id'] = str(id_obj)
            id_obj += 1



    data_groundF = "".join(listdata_groundF)
    data_wallF= "".join(listdata_wallF)
    listObjF=listObj1 + listObj2





    out_xml('out2.tmx',str(widthF),str(heightF),data_groundF,data_wallF,listObjF)

    
    

fusion_two_map('out.tmx','out1.tmx','down')

