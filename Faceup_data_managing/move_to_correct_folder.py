import os

folder = r'F:\Faceup\Faceup data\Set2_May17\Faceupdata\Inverted_39542'

for item in os.listdir(folder):
    full_path = os.path.join(folder, item)
    Newpath = ''
    if os.path.isfile(full_path):
        Light_type = item[9:(len(item) - 8)]
        print(Light_type)
        if Light_type == 'diffuse0':
            Newpath = os.path.join(folder, 'Inverted_Diffuse0', item)
        elif Light_type == 'diffuse40':
            Newpath = os.path.join(folder, 'Inverted_Diffuse40', item)
        elif Light_type == 'semidiffuse0':
            Newpath = os.path.join(folder, 'Inverted_semidiffuse0', item)
        elif Light_type == 'semidiffuse40':
            Newpath = os.path.join(folder, 'Inverted_semidiffuse40', item)
        elif Light_type == 'Silhouette':
            Newpath = os.path.join(folder, 'Inverted_silhouette', item)

        os.renames(full_path, Newpath)
