import sys
import numpy as np
import matplotlib.pyplot as plt

#Changes the values to get the NRZ-L coding
def encode_nrz_l(array):
    encoded = [not(x) for x in array]
    return encoded

#Encodes the array to get the NRZ-I code
def encode_nrzi(array):
    nrzi = [ array[0] ]
    for x in array[1:]:
        if x:
            nrzi.append(not(nrzi[-1]))
        else:
            nrzi.append(nrzi[-1])
    return nrzi
    
#AMI coding
def encode_ami(array):
    pulse = True #Decide to start with a positive pulse
    ami = []
    for x in array:
        if x:
            ami.append(1) if pulse else ami.append(-1)
            pulse = not(pulse)
        else:
            ami.append(0)
    return ami

#AMI coding  ##Just otherwise to ami
def encode_pseudoternary(array):
    pulse = True #Decide to start with a positive pulse
    pseudoternary = []
    for x in array:
        if not(x):
            pseudoternary.append(1) if pulse else pseudoternary.append(-1)
            pulse = not(pulse)
        else:
            pseudoternary.append(0)
    return pseudoternary
   
#MANCHESTER encode        
def encode_manchester(array):
    manchester = []
    for x in array:
        if x:
            manchester.append(0)
            manchester.append(1)
        else:
            manchester.append(1)
            manchester.append(0)
    return manchester

#DIFFERENCIAL MANCHESTER encode 
def encode_manchester_differencial(array):
    dif_manchester = []
    last = 0
    for x in array:
        if x:
            dif_manchester.append(1 if last == 1 else 0)
            dif_manchester.append(1 if last == 0 else 0)
            last = 1 if last == 0 else 0
        else:
            dif_manchester.append(1 if last == 0 else 0)
            dif_manchester.append(1 if last == 1 else 0)
           
    return dif_manchester
           

#B8ZS Binari 8 Zeros Substitution encode
def encode_b8zs(array):
    pulse = True #Decide to start with a positive pulse
    zeros = 0
    b8zs = []
    for x in array:
        if x:
            b8zs.append(1) if pulse else b8zs.append(-1)
            pulse = not(pulse)
            zeros = 0
        else:
            b8zs.append(0)
            zeros += 1
            if zeros >= 8:
                b8zs[-5] = 1 if not(pulse) else -1 #Equal to last pulse
                b8zs[-4] = 1 if pulse else -1
                b8zs[-2] = 1 if pulse else -1
                b8zs[-1] = 1 if not(pulse) else -1
                zeros = 0
    return b8zs    

#HDB3 High Density Bipolar 3 zeros
def encode_hdb3(array):
    pulse = True #Decide to start with a positive pulse
    zeros, ones = 0 , 0
    hdb3 = []    
    for x in array:
        if x:
            hdb3.append(1) if pulse else hdb3.append(-1)
            pulse = not(pulse)
            zeros = 0
            ones += 1
        else:
            hdb3.append(0)
            zeros += 1
            if zeros >= 4:
                if ones%2 == 0:
                    hdb3[-4] = 1 if pulse else -1
                    hdb3[-1] = 1 if pulse else -1
                    pulse = not(pulse)
                else:
                    hdb3[-1] = 1 if not(pulse) else -1
                zeros = 0
                ones = 0  
    return hdb3

#ASK Amplitud-shift key
def encode_ask(array):
    A = 1
    f = 1.5 #En realidad es la frecuencia de la senal portadora
    ask = []    
        
    x = np.arange(0,1,0.01)
    y = [] 
    for t in x: 
        y.append(A*np.cos( 2 * np.pi * f * t))
        
    for pos in array:
        if pos:
            ask.append(y)
        else:
            ask.append( [0]*100 )
    
    ask = np.array(ask)
    ask = ask.reshape(1, -1)[0]
    return ask

#FSK Frequency-shift key
def encode_fsk(array):
    A = 1
    f1 = 3 #En realidad es la frecuencia de la senal portadora 1
    f0 = 1 #La frequencia senal portadora para el 0
    fsk = []    
        
    x = np.arange(0,1,0.01)
    y1 = []
    y0 = []
    for t in x: 
        y1.append(A*np.cos( 2 * np.pi * f1 * t ))
        y0.append(A*np.cos( 2 * np.pi * f0 * t ))
        
    for pos in array:
        if pos:
            fsk.append(y1)
        else:
            fsk.append(y0)
    
    fsk = np.array(fsk)
    fsk = fsk.reshape(1, -1)[0]
    return fsk


#PSK Phase-shift key
def encode_psk(array):
    A = 1
    f = 1 #En realidad es la frecuencia de la senal portadora
    psk = []    
        
    x = np.arange(0,1,0.01)
    y1 = []
    y0 = []
    for t in x: 
        y1.append(A*np.cos( 2 * np.pi * f * t + np.pi))
        y0.append(A*np.cos( 2 * np.pi * f * t ))
        
    for pos in array:
        if pos:
            psk.append(y1)
        else:
            psk.append(y0)
    
    psk = np.array(psk)
    psk = psk.reshape(1, -1)[0]
    return psk    

#Plots the functions in a sinusoidal form
def plot_sinusoidal(model,array, encoded):
    step = len(array)/float(len(encoded))
    print len(array), len(encoded), step
    x = np.arange(0,len(array), step)
    xticks = np.arange(0,len(array)+1) 
    
    #PLOTS
    plt.subplot(211)
    plt.xlim(0, len(array))
    plt.ylim(-0.5, 1.5)
    
    plt.ylabel('Value')
    plt.title('Original')
    
    array = [int(z) for z in array]
    for i in range(len(array)):
        plt.text(i+0.4, 1.2, array[i])
    
    plt.grid()
    plt.xticks(xticks)    
    plt.step(xticks, [array[0]]+array)    
    
    #The silusoidal plots
    plt.subplot(212)
    plt.xlim(0, len(array))
    plt.ylim(-1.5, 1.5)
    
    plt.ylabel('Value')
    plt.title(model)
    
    for i in range(len(array)):
            plt.text(i+0.4, 1.2, array[i])    
    
    plt.plot(x, encoded)
    plt.grid()
    plt.xticks(xticks)
    plt.show()        


def plot_binary(model, array, encoded):
    if model == 'manchester' or model == 'differential-manchester':
        x = np.arange(0,len(array)+0.5, 0.5)
        x2 = np.arange(0,len(array)+1)
    else:
        x = np.arange(0,len(encoded)+1)
        x2 = x
    
    #PLOTS
    plt.subplot(211)
    plt.xlim(0, len(array))
    plt.ylim(-0.5, 1.5)
    
    plt.ylabel('Value')
    plt.title('Original')
    
    array = [int(z) for z in array]
    for i in range(len(array)):
        plt.text(i+0.4, 1.2, array[i])
    
    plt.grid()
    plt.xticks(x2)    
    plt.step(x2, [array[0]]+array)
    
    
    #We need add the first number twice to see properly on plot
    plt.subplot(212)
    plt.xlim(0, len(array))
    plt.ylim(-1.5, 1.5)
    
    plt.ylabel('Value')
    plt.title(model)
    
    for i in range(len(array)):
            plt.text(i+0.4, 1.2, array[i])    
    
    plt.grid()
    plt.xticks(x2)        
    plt.step(x, [encoded[0]]+encoded)
    plt.show()    


def encode(args):
    array = args['sequence']
    model = args['model']
    encoded = [0, 0];
    print array
    print model
    
    if model == 'nrz-l':
        encoded = encode_nrz_l(array)
        plot_binary(model, array, encoded)
    elif model == 'nrzi':
        encoded = encode_nrzi(array)
        plot_binary(model, array, encoded)
    elif model == 'bipolar-ami':
        encoded = encode_ami(array)
        plot_binary(model, array, encoded)
    elif model == 'pseudoternary':
        encoded = encode_pseudoternary(array)
        plot_binary(model, array, encoded)
    elif model == 'manchester':
        encoded = encode_manchester(array)
        plot_binary(model, array, encoded)
    elif model == 'differential-manchester': 
        encoded = encode_manchester_differencial(array)
        plot_binary(model, array, encoded)        
    elif model == 'b8zs':
        encoded = encode_b8zs(array)
        plot_binary(model, array, encoded)
    elif model == 'hdb3':
        encoded = encode_hdb3(array)
        plot_binary(model, array, encoded)
    elif model == 'ask':
        encoded = encode_ask(array)
        plot_sinusoidal(model, array, encoded)
    elif model == 'fsk':
        encoded = encode_fsk(array)
        plot_sinusoidal(model, array, encoded)
    elif model == 'psk':
        encoded = encode_psk(array)
        plot_sinusoidal(model, array, encoded)
    else:
        pass



def default(str):
    return str +'\n'+' [Default: %default]'

def readCommand( argv ):
    """
    Processes the command used to run pacman from the command line.
    """
    from optparse import OptionParser
    usageStr = """
    USAGE:      python code.py <options>
    """
    parser = OptionParser(usageStr)

    parser.add_option('-b', '--binarySequence', dest='binarySequence',
                      help=default('the BINARY SEQUENCE to encode'), default='random')

    parser.add_option('-m', '--model', dest='model',
                      help=default('Codification MODEL used: \n\n\
                      "nrz-l" Nonreturn to Zero-Level \n\
                      "nrzi" Nonreturn to Zero Inverted \n\
                      "bipolar-ami" 0:no-signal 1:level-changes(+to-) \n\
                      "pseudoternary" 0:level-changes(+to-) 1:no-signal \n\
                      "manchester" 0:high-to-low 1:low-to-high \n\
                      "differential-manchester" 0:transition-at-first 1:no-t \n\
                      "b8zs" Bipolar with 8 Zeros Substitution \n\
                      "hdb3" High Density Bipolar 3 zeros \n\
                      "ask" Amplitude-shift keying \n\
                      "fsk" Frequency-shift keying \n\
                      "psk" Phase-shift keying \n'), default='nrz-l')


    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()    

    #Get the sequence
    args['sequence'] = options.binarySequence
    if args['sequence'] == 'random':
        if not(options.model == 'b8zs' or options.model == 'hdb3'):
            #Creates a random binary array, we use bool to easy manipulate.
            rand = np.random.randint(2, size=(10,))
            args['sequence'] = [bool(x) for x in rand] 
        else:
            #Semi random for b8zs and hdb3 to get a 8zs sequence at first
            rand = np.random.randint(2, size=(5,))
            args['sequence'] = [True, True, False, False, False, False, False, False, False, False] + [bool(x) for x in rand] 
    else:
        args['sequence'] = [False if e=="0" else True for e in options.binarySequence ]
    
    #Gets the model of modulation/encode
    args['model'] = options.model
            
    return args

if __name__ == '__main__':
    """
    Main function called when code.py is run
    from the comand line:
    > python code.py


    """
    args = readCommand( sys.argv[1:] ) # Get game components based on input
    encode(args) #Operate with the options introduced

    pass