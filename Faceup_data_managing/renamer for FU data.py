import os

folder = r'F:\Faceup\Faceup data\Set2_May17\Faceupdata\Inverted_39544'
Lighting = {'diffuse': 'diffuse', 'semidiff': 'semidiffuse', 'silh': 'Silhouette'}
for file in os.listdir(folder):
    old_filepath = os.path.join(folder, file)
    file_number = str(file)[(len(file) - 7):(len(file) - 4)]
    camera_number = file[9:12]

    lighting_name = file[13:(len(file) - 13)]

    if lighting_name == 'silh':
        view_angle = ''
    elif camera_number == '000':
        view_angle = '40'
    else:
        view_angle = '0'

    new_filename = 'Inverted_' + Lighting[lighting_name] + view_angle + '-' + file_number + '.png'

    print (file_number, camera_number, lighting_name, new_filename)

    new_path = os.path.join(folder, new_filename)

    # os.renames(old_filepath, new_path)
