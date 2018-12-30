import numpy as np

def generate_with_seed(model, seed, max_len):
    
    if len(seed) == 0:
        seed = b'\x00'
    
    x = np.zeros((1, len(seed)), dtype='uint8')
    for num, i in enumerate(seed): x[0][num] = i
    output = seed
    choice = None
    
    while len(output) < max_len:
        
        out = model.predict(x)[0][-1]
        
        if  len(output)-len(seed) < 2:
            out[0] = 0
            out /= np.sum(out)
            
        choice = np.random.choice(256, p=out)
        
        if choice == 0:
            break
        
        output += bytes([choice])
        
        x = np.zeros((1, 1), dtype='uint8')
        x[0][0] = choice

    if output[0] == 0:
        output = output[1:]

    return output
    


