import random
import numpy as np
import torch

def setSeed(manualSeed):
	np.random.seed(manualSeed)
	random.seed(manualSeed)
	torch.manual_seed(manualSeed)
	torch.cuda.manual_seed(manualSeed)
	torch.cuda.manual_seed_all(manualSeed)

	torch.backends.cudnn.enabled = False
	torch.backends.cudnn.benchmark = False
	torch.backends.cudnn.deterministic = True
