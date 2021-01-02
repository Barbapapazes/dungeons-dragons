import xml.etree.ElementTree as ET
import os
from random import randint
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



def fusion_two_map(map1,map2,out,direction):      # direction prend la valeur right or down (c'est pour savoir comment on place la map 1 par rapport a la deuxieme)
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





    out_xml(out,str(widthF),str(heightF),data_groundF,data_wallF,listObjF)

    
    



def generate_map(height,width,out='../map_generated.tmx'):
    list_10 = ['LD','LR','LDR']
    list_11 = ['LT','TRDL','LDR','LTR','LTD']
    list_00 = ['RD']
    list_01 = ['TD','TR','TRD']
    
    endw_10 = ['LD']
    endw_11 = ['LT']
    endw_00 = ['D']
    endw_01 = ['TD']

    endh_10 = ['LR']
    endh_11 = ['LT','LR','LTR']
    endh_00 = ['R']
    endh_01 = ['TR']

    list_R1 = ['LR','RD','TR','TRDL','R','LDR','LTR']
    list_D1 = ['LD','RD','TD','TRDL','D','LDR','LTD','TRD']
    
    ligneUP = list(x-x for x in range(width))
    ligneCUR_R = list(x-x for x in range(width))
    ligneCUR_D = list(x-x for x in range(width))
    
    os.chdir('./preset')

    dir = './S/'
    listDir = os.listdir(dir)
    
    dirChild = listDir[randint(0,len(listDir)-1)]
    dir = dir + dirChild +'/'

    if dirChild == 'R':
        ligneCUR_R[0] = 1
    elif dirChild == 'D':
        ligneCUR_D[0] = 1

    listDir = os.listdir(dir)
    map1Select = dir +listDir[randint(0,len(listDir)-1)]
    #END INITIALISATION 

    for k in range(height):
        if k == 0:
            init= 1
        else:
            init=0

        for i in range(width-init):
            
            
            if ligneCUR_R[i] == 1 and ligneUP[i] == 0:
                list_cur = list_10   
            elif ligneCUR_R[i] == 1 and ligneUP[i] == 1:
                list_cur = list_11  
            elif ligneCUR_R[i] == 0 and ligneUP[i] == 0:
                list_cur = list_00
            elif ligneCUR_R[i] == 0 and ligneUP[i] == 1:
                list_cur = list_01

            if i== width-1:
                if ligneCUR_R[i] == 1 and ligneUP[i] == 0:
                    list_cur = endw_10   
                elif ligneCUR_R[i] == 1 and ligneUP[i] == 1:
                    list_cur = endw_11  
                elif ligneCUR_R[i] == 0 and ligneUP[i] == 0:
                    list_cur = endw_00
                elif ligneCUR_R[i] == 0 and ligneUP[i] == 1:
                    list_cur = endw_01

            if k== height-1:
                if ligneCUR_R[i] == 1 and ligneUP[i] == 0:
                    list_cur = endh_10   
                elif ligneCUR_R[i] == 1 and ligneUP[i] == 1:
                    list_cur = endh_11  
                elif ligneCUR_R[i] == 0 and ligneUP[i] == 0:
                    list_cur = endh_00
                elif ligneCUR_R[i] == 0 and ligneUP[i] == 1:
                    list_cur = endh_01

            if k == height-1 and i == width - 1:
                list_cur = ['WALL']

            dirMap = list_cur[randint(0,len(list_cur)-1)]
            dir = './' + dirMap + '/'
            listMap = os.listdir(dir)
            
            
            if i != width-1:
                if dirMap in list_R1:
                    ligneCUR_R[i+1] = 1
                
            if dirMap in list_D1:
                ligneCUR_D[i] = 1

            if i == 0 and k!=0:
                map1Select = dir + listMap[randint(0,len(listMap)-1)]
            else:

                map2Select = dir + listMap[randint(0,len(listMap)-1)]
                
                fusion_two_map(map1Select,map2Select,'./GENERATED/ligne'+str(k)+'.tmx','right')
                map1Select = './GENERATED/ligne'+str(k)+'.tmx'

   
        ligneUP = ligneCUR_D
        ligneCUR_R = list(x-x for x in range(width))
        ligneCUR_D = list(x-x for x in range(width))
        



    map1Select='./GENERATED/ligne0.tmx'

    for k in range(1,height):
        #print(k,'  ',height)
        if k != height-1:
            fusion_two_map(map1Select,'./GENERATED/ligne'+str(k)+'.tmx','./GENERATED/Untildown.tmx','down')
            map1Select='./GENERATED/Untildown.tmx'
        else:
            fusion_two_map(map1Select,'./GENERATED/ligne'+str(k)+'.tmx',out,'down')






