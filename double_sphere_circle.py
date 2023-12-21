import math
import time
# from numpy.linalg import matrix_rank

# from IPython.display import display, Math, Latex

# Destination for files:
DEST = '/Users/georgfrenck/sciebo/Math/Teaching/2023 WS/Softwarepraktikum/triangulations-of-surfaces/input/'

# size of the circles:
n=9  # points on small circles or number of "equators" for genus=0
m=8      # points on large circles or number of "meridians" for genus=0

# increase the genus of the surface
# only sensible if XXXXX
genus=0


# Size of the canvas:
scale=300


# number of decimal places
precision=0










r_big=3
r_small=1
index=0

delta_0=[]
delta_1=[]
delta_2=[]

# points_left=[0,1,n+1]
# m_half=math.floor(m/2)
# p_right=[(m_half-1)*n,m_half*n,  m_half*n + 1]
# print(p_left)
# print(p_right)

def create_delta_0 (num_n, num_m,num_g):
    global delta_0
    delta_0=[]

    for i in range(num_n):
        # outermost points are (-r_big-r_small,0,0) and (r_big+ r_small,0,0)
        # hence scaling to be smaller then scale/2
        scale_genus=1.1*num_g



        
        scale_temp=scale/(2*(r_big+r_small)*scale_genus)
        x=round(scale_temp*r_big +r_small*math.cos(2*math.pi*i/num_n)*scale_temp,precision)
        y=0
        z=round(r_small*math.sin(2*math.pi*i/num_n)*scale_temp,precision)
        if precision==0:
            x=int(x)
            y=int(y)
            z=int(z)
        delta_0.append([x,y,z])

    cos=[]
    sin=[]

    for i in range(num_m-1):
        cos.append(math.cos(2*math.pi*(i+1)/num_m))
        sin.append(math.sin(2*math.pi*(i+1)/num_m))

        for j in range(num_n):
            x=round(delta_0[j][0]*cos[i] - delta_0[j][1]*sin[i],precision)
            y=round(delta_0[j][0]*sin[i] - delta_0[j][1]*cos[i],precision)
            z=delta_0[j][2]   
            if precision==0:
                x=int(x)
                y=int(y)
                z=int(z)
            delta_0.append([x,y,z])

    for i in range(num_g):
        mid=-scale/2 + scale/(2*num_g) + i*scale/num_g
        for j in range(num_m*num_n):
            x_temp=round(delta_0[j][0]-mid,precision)
            if precision==0:
                x_temp=int(x_temp)
            delta_0.append([x_temp,delta_0[j][1],delta_0[j][2]])
    delta_0 = delta_0[num_m*num_n:]
    



def create_delta_1(num_n, num_m,num_g,p_left,p_right):
    global delta_1
    delta_1=[]

    # add small circles

    for i in range(num_m):
        for j in range(num_n):
            delta_1.append([num_n*(i) + j, num_n*(i) + (j + 1)%num_n])

    # add large circles

    for i in range(num_m):
        for j in range(num_n):
            delta_1.append([num_n*(i) + j, (num_n*(i) + (j + num_n))%(num_n*num_m)])
            delta_1.append([num_n*(i) + j, (num_n*(i) + num_n+(j +1)%num_n)%(num_n*num_m)])


    delta_1_temp_length=len(delta_1)


    for i in range(num_g-1):
        # add lines for further tori
        for k in range(delta_1_temp_length):
            delta_1.append([(i+1)*num_m*num_n + delta_1[k][0],(i+1)*num_m*num_n + delta_1[k][1]])
        
        # add simplices for gluing
        for j in range(3):
            delta_1.append([i*num_m*num_n + p_right[j],(i+1)*num_m*num_n + p_left[j]])
            delta_1.append([i*num_m*num_n + p_right[j],(i+1)*num_m*num_n + p_left[(j+2)%3]])

# Find 2 simplices comment if not absolutely necessary





def create_delta_2(prod_nm,num_g,p_left,p_right):
    global delta_2
    delta_2=[]
    # print(prod_nm*num_g)
    # print(len(delta_0))
    if num_g==0:
        for i in range(prod_nm):
            progress = round(100*i/(prod_nm))
            string_temp = '| '
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

    else:
        for i in range(prod_nm*num_g):
            progress = round(100*i/(prod_nm*num_g))
            string_temp = '|'
            for q in range(progress):
                string_temp = string_temp+'='
            for q in range(100-progress):
                string_temp = string_temp+' '
            string_temp = string_temp + '|'
            print(string_temp, end='\r')
            for j in range(prod_nm*num_g-i-1):
                for k in range(prod_nm*num_g-j-i-2):
                    a=i%(prod_nm*num_g)
                    b=(i+j+1)%(prod_nm*num_g)
                    c=(i+j+k+2)%(prod_nm*num_g)
                    if (delta_1.count([a,b])>0 or delta_1.count([b,a])>0) and (delta_1.count([a,c])>0 or delta_1.count([c,a])>0) and (delta_1.count([b,c])>0 or delta_1.count([c,b])>0):
                        if a>0 and c<(num_g-1)*prod_nm+p_right[2]:
                            if [a%(prod_nm),b%(prod_nm),c%(prod_nm)] != p_left and [a%(prod_nm),b%(prod_nm),c%(prod_nm)] != p_right:
                                delta_2.append([a,b,c])
                            # else:
                            #     print([a,b,c])
                        else:
                            delta_2.append([a,b,c])
                    

# Create sphere

def create_delta_0_sphere(num_equator, num_meridian):
    scale_half=round(scale/2,precision)
    if(precision==0):
        scale_half=int(scale_half)

    
    for h in range(2):
        for i in range(num_meridian):
            cos=math.cos(2*math.pi*(i+1)/num_meridian)
            sin=math.sin(2*math.pi*(i+1)/num_meridian)

            height_mid=0

            for j in range(num_equator):
                j_temp = 2*(j)-num_equator +1
                scale_temp=(scale/2)*math.cos((1/2)*math.pi*(j_temp)/(num_equator+1))
                height=scale/2*math.sin((1/2)*math.pi*(j_temp)/(num_equator+1))
                x=round(cos*scale_temp + (1-2*(h))*150,precision)
                y=round(sin*scale_temp,precision)
                z=height+height_mid
                if precision==0:
                    x=int(x)
                    y=int(y)
                    z=int(z)
                delta_0.append([x,y,z])  
        delta_0.append([(1-2*(h))*150,0,-scale_half])
        delta_0.append([(1-2*(h))*150,0,scale_half])


    for j in range(2*num_equator+1):
        cos=2
        sin=0
        j_temp = 2*(j)-num_equator +1
        scale_temp=(scale/2)*math.cos((1/2)*math.pi*(j_temp)/(num_equator+1))
        height=scale/2*math.sin((1/2)*math.pi*(j_temp)/(num_equator+1))
        x=round(cos*scale_temp,precision)
        z=height+height_mid
        if precision==0:
            x=int(x)
            y=0
            z=int(2*z)
        if  not z==0: delta_0.append([x,y,z])
    delta_0.append([0,0,2*scale_half])
    delta_0.append([0,0,-2*scale_half])

    global index
    delta_0.reverse()
    index=len(delta_0)-delta_0.index([0,0,0])-1
    delta_0.remove([0,0,0])
    delta_0.reverse()

    for a in delta_0:
        if delta_0.count(a)>1:  
            print(a)
            delta_0.reverse()
            delta_0.remove(a)
            delta_0.reverse()
            print(delta_0.index(a))
    


    
    # for i in range(num_meridian):
    #     cos=math.cos(2*math.pi*(i+1)/num_meridian)
    #     sin=math.sin(2*math.pi*(i+1)/num_meridian)
    #     scale_temp=(scale/2)*math.cos((1/2)*math.pi*(5-num_equator)/(num_equator+1))
    #     x=round(cos*scale_temp,precision)
    #     y=round(sin*scale_temp,precision)
    #     delta_0.reverse()
    #     delta_0.remove([x,y,0])
    #     delta_0.reverse()

def create_delta_1_sphere(num_equator, num_meridian):
    global index
    prod_temp=num_equator*num_meridian
    for h in range(2):
        # print(len(delta_0))
        h_mult=(num_equator*num_meridian)+2
        # print(h_mult)
        for j in range(num_meridian):
            for i in range(num_equator):
                if h==0:
                    delta_1.append([i+j*num_equator,(i+j*num_equator+num_equator)%prod_temp])
                    if i<num_equator-1:
                        delta_1.append([i+j*num_equator,(i+j*num_equator+1)%prod_temp])
                        delta_1.append([i+j*num_equator,(i+j*num_equator+1+num_equator)%prod_temp])
                if h==1:
                    if j<num_meridian-2 or (j==num_meridian-2 and i<(num_equator)/2-1):
                        delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator)%prod_temp+h_mult])
                        if i<num_equator-1:
                            delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+1)%prod_temp+h_mult])
                            if (i+j*num_equator+1+num_equator)%prod_temp+h_mult==141:
                                delta_1.append([i+j*num_equator+h_mult,31])
                            else:
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+1+num_equator)%prod_temp+h_mult]) 
                    elif j==num_meridian-2:
                        if i+j*num_equator+num_equator-1+h_mult==140:
                            delta_1.append([i+j*num_equator+h_mult,31])
                        else:
                            delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator-1)%prod_temp+h_mult])
                        if i<num_equator-1:
                            if (i+j*num_equator+1+num_equator)%prod_temp+h_mult==141:
                                delta_1.append([i+j*num_equator+h_mult,31])
                            else:
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+1)%prod_temp+h_mult])
                            delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator)%prod_temp+h_mult]) 
                    else:
                        if i<=2:
                            if (i+j*num_equator+num_equator)%prod_temp+h_mult==141:
                                delta_1.append([i+j*num_equator+h_mult,31])
                            else:
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator)%prod_temp+h_mult])
                            if i<num_equator-1:
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+1)%prod_temp+h_mult])
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator+1)%prod_temp+h_mult])
                        elif i>=4 and i<=num_equator-3:
                            delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator+1)%prod_temp+h_mult])
                            if i<num_equator-1:
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+1)%prod_temp+h_mult])
                                delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator+2)%prod_temp+h_mult]) 
        delta_1.append([31,140])                            
        delta_1.append([31,141])                            
        delta_1.append([31,78])                            
        delta_1.append([31,79])                            
        delta_1.append([140,77])                            
        delta_1.append([140,78])                            
        delta_1.append([144,82])                            
                            # delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator)%prod_temp+h_mult])
                            # if i<num_equator-1:
                            #     delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+1)%prod_temp+h_mult])
                            #     delta_1.append([i+j*num_equator+h_mult,(i+j*num_equator+num_equator+1)%prod_temp+h_mult]) 

    for j in range(num_meridian):
        h_mult=(num_equator*num_meridian)+2
        delta_1.append([j*num_equator,h_mult-2])
        delta_1.append([num_equator*(j+1)-1,h_mult-1])
        delta_1.append([j*(num_equator)+h_mult,len(delta_0)-2*num_equator-2])
        if j<num_meridian-1: delta_1.append([(num_equator)*(j+1)+h_mult-1,len(delta_0)-2*num_equator-1])
    delta_1.append([144,146])    
    delta_1.append([147,148])    
    delta_1.append([148,149])    
    delta_1.append([149,150])    
    delta_1.append([150,67])    
    delta_1.append([151,67])    

    for j in range(num_equator-1):
        delta_1.append([151+j,151+j+1])

         
    delta_1.append([159,105])    
    delta_1.append([160,105])    
    delta_1.append([160,161])    
    delta_1.append([160,161])    
    delta_1.append([161,162])       
    delta_1.append([162,163])    
    delta_1.append([163,164])    
    delta_1.append([164,147])    

    for j in delta_1:
        if delta_1.count(j)>1:
            delta_1.remove(j)

    



# Print points for plotting in grapher:

def print_for_grapher(num_n,num_m,num_g):
    start = time.time()
    points_left=[0,1,num_n+1]
    m_half=math.floor(num_m/2)
    points_right=[(m_half-1)*num_m,m_half*num_m,  m_half*num_m + 1]
    if num_g>=1:
        create_delta_0(num_n,num_m,num_g)
        string=''
        count=0
        for i in delta_0:
            for a in i:
                string= string + '{} '.format(a)
            string+="\n"
        # print(string.replace('.',','))
        title='{}grapher_surface_genus_{}_circle_{}_{}.txt'.format(DEST,num_g,num_n,num_m)
        f=open(title,'w')
        f.write(string.replace('.',','))
        if num_g>=2:
            title='{}grapher_surface_genus_{}_circle_{}_{}_gluing.txt'.format(DEST,num_g,num_n,num_m)
            f=open(title,'w')
            gluing_points=[]
            for k in range(num_g):
                for p in points_left:
                    gluing_points.append(delta_0[p+k*num_m*num_n])
                for p in points_right:
                    gluing_points.append(delta_0[p+k*num_m*num_n])
            gluing_string=''
            for q in gluing_points:
                for a in q:
                    gluing_string= gluing_string + '{} '.format(a)
                gluing_string+="\n"
            f.write(gluing_string.replace('.',','))
    if num_g==0:
        create_delta_0_sphere(num_n,num_m)
        title='{}grapher_double_sphere_{}_{}.txt'.format(DEST,num_n,num_m)
        f=open(title,'w')
        string=''
        count=0
        for i in delta_0:
            for a in i:
                string= string + '{} '.format(a)
            string+="\n"
        f.write(string.replace('.',','))
    end=time.time()
    # print((end-start)/60)


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

def create_and_print(points_on_small_circle,points_on_large_circle,genus_of_surface):


    start = time.time()
    points_left=[0,1,points_on_small_circle+1]
    m_half=math.floor(points_on_large_circle/2)
    points_right=[(m_half-1)*points_on_small_circle,m_half*points_on_small_circle,  m_half*points_on_small_circle + 1]
    # print(points_left)
    # print(points_right)

    if genus_of_surface>=1:
        create_delta_0(points_on_small_circle,points_on_large_circle,genus_of_surface)
        create_delta_1(points_on_small_circle,points_on_large_circle,genus_of_surface,points_left,points_right)
        create_delta_2(points_on_small_circle*points_on_large_circle, genus_of_surface,points_left,points_right)

    if genus_of_surface==0:
        create_delta_0_sphere(points_on_small_circle,points_on_large_circle)
        create_delta_1_sphere(points_on_small_circle,points_on_large_circle)
        create_delta_2(len(delta_0),0,0,0)
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

    title='{}doube_sphere_circle.txt'.format(DEST,genus_of_surface,points_on_small_circle,points_on_large_circle)
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


    end = time.time()
    time_taken=end-start
    time_taken_minutes = math.floor(time_taken/60)
    time_taken_seconds = math.floor(time_taken%60)

    print()
    print('The data for a triangulation on the surface of genus {} with {} 0-simplices, {} 1-simplices and {} 2-simplices has been created in \n {}'.format(genus_of_surface,len(delta_0),len(delta_1),len(delta_2),title))
    print()
    print('Observe, that the Euler-Characteristic is given by {} which also equals 2-2g=2-2*{}={}.'.format(len(delta_0)-len(delta_1)+len(delta_2),genus_of_surface,2-2*genus_of_surface))
    print()
    print('By the way, this took {} minutes and {} seconds.'.format(time_taken_minutes,time_taken_seconds))
    print()
    print()



# create_and_print(8,8,2)
# create_and_print(8,8,3)
# create_and_print(8,8,4)

# create_and_print(8,12,2)
# create_and_print(8,12,3)
# create_and_print(8,12,4)


# create_and_print(8,16,2)
# create_and_print(8,16,3)
# create_and_print(8,16,4)

# create_and_print(10,12,2)
# create_and_print(10,12,3)
# create_and_print(10,12,4)

# create_and_print(10,14,2)
# create_and_print(10,14,3)
# create_and_print(10,14,4)

# create_and_print(10,16,2)
# create_and_print(10,16,3)
# create_and_print(10,16,4)

# create_and_print(12,20,1)



create_and_print(n,m,genus)
# print_for_grapher(n,m,genus)
# print_delta_1()