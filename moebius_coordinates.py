import math

# from IPython.display import display, Math, Latex

# Destination for files:
DEST = '/Users/georgfrenck/sciebo/Math/Teaching/2023 WS/Softwarepraktikum/triangulations-of-surfaces/input/'

# size of the circles:
n=6 # points on line
m=16 # points on circles


# Size of the canvas:
scale=600


# number of decimal places
precision=0










r_big=5    # radius of circle
r_small=1  # length of line

delta_0=[]
delta_1=[]
delta_2=[]

# points_left=[0,1,n+1]
# m_half=math.floor(m/2)
# p_right=[(m_half-1)*n,m_half*n,  m_half*n + 1]
# print(p_left)
# print(p_right)

def create_delta_0 (num_n, num_m):
    global delta_0
    delta_0=[]
    mid=[]

    for i in range(num_m):
        scale_temp=scale/(2*(r_big+r_small))
        x=round(scale_temp*math.cos(2*math.pi*i/num_m)*r_big)
        y=round(scale_temp*math.sin(2*math.pi*i/num_m)*r_big)
        mid.append([x,y,0])


    for i in range(num_n):
        # outermost points are (-r_big-r_small,0,0) and (r_big+ r_small,0,0)
        # hence scaling to be smaler then scale/2

        scale_temp=scale/(2*(r_big+r_small))
        
        if num_n>1: height=scale_temp*(-r_small+2*r_small*i/(num_n-1))
        if num_n==1: height=0
        x=round(scale_temp*r_big)
        y=0
        z=round(height,precision)
        if precision==0:
            x=int(x)
            y=int(y)
            z=int(z)
        delta_0.append([x,y,z])

    cos=[]
    sin=[]

    for i in range(num_m-1):
        cos=math.cos(math.pi*(i+1)/num_m)
        sin=math.sin(math.pi*(i+1)/num_m)
        norm=math.sqrt(mid[i+1][1]*mid[i+1][1] + mid[i+1][0]*mid[i+1][0])
        n_1=-mid[i+1][1]/norm
        n_2=mid[i+1][0]/norm


        matrix = [
            [n_1*n_1*(1-cos)+cos, n_1*n_2*(1-cos), n_2*sin],
            [n_1*n_2*(1-cos), n_2*n_2*(1-cos)+cos, -n_1*sin],
            [-n_2*sin, -n_1*sin, cos]
        ]

        

        for j in range(num_n):
            x_precise = (delta_0[j][0]-mid[0][0])*matrix[0][0] + (delta_0[j][1]-mid[0][1])*matrix[0][1] + (delta_0[j][2]-mid[0][2])*matrix[0][2] + mid[i+1][0]
            y_precise = (delta_0[j][0]-mid[0][0])*matrix[1][0] + (delta_0[j][1]-mid[0][1])*matrix[1][1] + (delta_0[j][2]-mid[0][2])*matrix[1][2] + mid[i+1][1]
            z_precise = (delta_0[j][0]-mid[0][0])*matrix[2][0] + (delta_0[j][1]-mid[0][1])*matrix[2][1] + (delta_0[j][2]-mid[0][2])*matrix[2][2] + mid[i+1][2]
            x=round(x_precise,precision)
            y=round(y_precise,precision)
            z=round(z_precise,precision)
            if precision==0:
                x=int(x)
                y=int(y)
                z=int(z)
            delta_0.append([x,y,z])



def create_delta_1(num_n, num_m):
    global delta_1
    delta_1=[]

    # add small circles

    for i in range(num_m):
        for j in range(num_n-1):
            delta_1.append([num_n*(i) + j, num_n*(i) + j + 1])
            delta_1.append([num_n*(i) + j, (num_n*(i) + j + num_n + 1)%(num_n*num_m)])

    # add large circles

    for i in range(num_m):
        for j in range(num_n):
            delta_1.append([num_n*(i) + j, (num_n*(i) + (j + num_n))%(num_n*num_m)])


# Find 2 simplices comment if not absolutely necessary

def create_delta_2(prod_nm):
    global delta_2
    delta_2=[]
    for i in range(prod_nm):
        progress = round(100*i/(prod_nm))
        string_temp = '|'
        for q in range(progress):
            string_temp = string_temp+'='
        for q in range(100-progress):
            string_temp = string_temp+' '
        string_temp = string_temp + '|'
        print(string_temp, end='\r')
        for j in range(prod_nm-i-1):
            for k in range(prod_nm-j-i-2):
                a=i%(prod_nm)
                b=(i+j+1)%(prod_nm)
                c=(i+j+k+2)%(prod_nm)
                if (delta_1.count([a,b])>0 or delta_1.count([b,a])>0) and (delta_1.count([a,c])>0 or delta_1.count([c,a])>0) and (delta_1.count([b,c])>0 or delta_1.count([c,b])>0):
                    delta_2.append([a,b,c])
                    





# Print points for plotting in grapher:

def print_for_grapher(num_n,num_m):
    create_delta_0(num_n,num_m)
    string=''
    count=0
    for i in delta_0:
        for a in i:
            string= string + '{} '.format(a)
        string+="\n"
    # print(string.replace('.',','))
    title='{}moebiusband_{}_{}.txt'.format(DEST,num_n,num_m)
    f=open(title,'w')
    f.write(string.replace('.',','))
    f=open(title,'w')

# Print 0-simplices

def print_delta_0():
    print('delta_0=[')
    for a in delta_0:
        print('{},'.format(a))
    print(']')
    print('')


# # Print 1-simplices

def print_delta_1():
    print('delta_1=[')
    for a in delta_1:
        print('{},'.format(a))
    print(']')
    print('')


# # Print 2-simplices

def print_delta_2():
    print('delta_2=[')
    for a in delta_2:
        print('{},'.format(a))
    print(']')



# create_delta_0(n,m)

def create_and_print(points_on_fiber_line,number_of_fibers):

    create_delta_0(points_on_fiber_line,number_of_fibers)
    create_delta_1(points_on_fiber_line,number_of_fibers)
    create_delta_2(points_on_fiber_line*number_of_fibers)

    # The following only works for n,m<=10 or so, otherwise the terminal erases stuff.
    # print()
    # print()
    # print('Here are the data for a triangulation on the torus with {} 0-simplices, {} 1-simplices and {} 2-simplices'.format(len(delta_0),len(delta_1),len(delta_2)))
    # print()
    # print()
    # print_delta_0()
    # print()
    # print_delta_1()
    # print()
    # print_delta_2()
    # print()
    # print()
    # print('This was the data for a triangulation on the torus with {} 0-simplices, {} 1-simplices and {} 2-simplices'.format(len(delta_0),len(delta_1),len(delta_2)))
    # print()
    # print()

    title='{}moebiusband_{}_{}.txt'.format(DEST,points_on_fiber_line,number_of_fibers)
    f=open(title,'w')
    str_delta_0='delta_0=[\n '
    for a in delta_0:
        str_delta_0=str_delta_0+'{},\n '.format(a)
    str_delta_0=str_delta_0+']\n'

    str_delta_1='delta_1=[\n '
    for a in delta_1:
        str_delta_1=str_delta_1+'{},\n '.format(a)
    str_delta_1=str_delta_1+']\n'

    str_delta_2='delta_2=[\n '
    for a in delta_2:
        str_delta_2=str_delta_2+'{},\n '.format(a)
    str_delta_2=str_delta_2+']\n'
    f.write('{}\n\n{}\n\n{}'.format(str_delta_0,str_delta_1,str_delta_2))

    print()
    print('The data for a triangulation of the Moebius band with {} 0-simplices, {} 1-simplices and {} 2-simplices has been created in {}'.format(len(delta_0),len(delta_1),len(delta_2),f))
    print()
    print('Observe, that the Euler-Characteristic is given by {}'.format(len(delta_0)-len(delta_1)+len(delta_2)))
    print()
    print()




create_and_print(n,m)
print_for_grapher(n,m)

# create_and_print(8,8,2)
# create_and_print(8,8,3)
# create_and_print(8,8,4)

# create_and_print(8,12,2)
# create_and_print(8,12,3)
# create_and_print(8,12,4)


# create_and_print(8,16,2)
# create_and_print(8,16,3)
# create_and_print(8,16,4)
