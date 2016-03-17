import os
import shutil

root_dir = '/Users/johan/Desktop/'
dir_name = 'apa'


dest_dir = os.path.join(root_dir, dir_name)


if not os.path.isdir(dest_dir):
	os.mkdir(dest_dir)

#print('dir exists delete!')
#shutil.rmtree(dest_dir)


src = '/Users/johan/Desktop/Faktura1014.pdf'

ext = 'pdf'
new_name = '16_12_23_apple_itunes.{}'.format(ext)


if os.path.isfile(os.path.join(dest_dir, new_name)):
	print('File exists. Overwrite?')

dst = os.path.join(dest_dir, new_name)
shutil.copy(src, dst)
	