import os
import imageio
from IPython import embed

# You can generate gifs calling the following function from elsewhere or execute this python script directly
def gifNum(path):
	nums = [int(x.split('.')[0]) for x in os.listdir(path) if '.gif' in x]
	if len(nums)>0:
		return max(nums)+1
	return 0

def genGIF(path):
	images = []
	correct_files = []
	files = os.listdir(path)
	for filename in files:
		if '.png' in filename:
			correct_files.append(os.path.join(path,filename))
	correct_files.sort(key=lambda x: int(x.split('.')[4]))

	for file in correct_files:
		images.append(imageio.imread(file))


	gif_number = gifNum(path)
	imageio.mimsave(os.path.join(path,"{:03}.gif".format(gif_number)), images, fps=5)
	for f in os.listdir(path):
		if '.png' in f:
			os.remove(os.path.join(path, f))
