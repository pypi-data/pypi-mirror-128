import numpy as np
import reikna.cluda as cluda
from reikna.cluda import functions, dtypes
from reikna.cluda.tempalloc import ZeroOffsetManager

import pyopencl as cl

dtype = np.complex64
api = cluda.ocl_api()
thr = api.Thread.create(0)

#This is working
input_1 = np.ones((200,200)).astype(np.complex64)
i1 = thr.empty_like(input_1)
i1.conj()

#This is not working
temp_manager = ZeroOffsetManager(thr, pack_on_alloc=True, pack_on_free=True)
a1 = temp_manager.array([200,200], np.complex64)

buf = cl.Buffer(thr._context, cl.mem_flags.READ_WRITE, 320000)
a1.base_data = buf

a1.conj()
