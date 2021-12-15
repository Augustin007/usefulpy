'''
preparing for new lighting system
'''
from ... import mathematics as math

testing = False

def light(L, p, n, t):
    h_raw = L-p
    h = abs(h_raw)
    d = abs((h_raw/h)-n)
    if d > math.sqrt(2)/2:
        return 0
    if testing:
        print(d, h)
    return light_square(h, d, t)

def light_square(h, d, t):
    square = 4*(t**2)
    d_cos, d_sin = cos_and_sin(d)
    offset_x = t*d_sin
    offset_z = t*d_cos
    t_off = math.hypot(t, offset_z)
    A_t = math.hypot(h+offset_x, t_off)
    A_b = math.hypot(h-offset_x, t_off)
    s1 = math.quaternion(0, (h+offset_x)/A_t, offset_z/A_t, t/A_t) #top left
    s2 = math.quaternion(0, (h-offset_x)/A_b, -offset_z/A_b, t/A_b) # top right
    s3 = math.quaternion(0, (h-offset_x)/A_b, -offset_z/A_b, -t/A_b) # bottom right
    s4 = math.quaternion(0, (h+offset_x)/A_t, offset_z/A_t, -t/A_t) #bottom left
    if testing:
        print()
        print(f'1: {s1}',f'2: {s2}', f'3: {s3}', f'4: {s4}', sep = '\n')
        print(abs(s1), abs(s2), abs(s3), abs(s4))

    if testing:
        print()
        print(abs(s1-s4), abs(s2-s3), abs(s1-s3))

        ##print(abs(s1))
    # Working up to here. I think.
    δ_cos, δ_sin = cos_and_sin(abs(s1-s3))
    α_cos, α_sin = cos_and_sin(abs(s1-s4))
    β_cos, β_sin = cos_and_sin(abs(s3-s4))
    γ_cos, γ_sin = cos_and_sin(abs(s2-s3))

    if testing:
        print()
        print('δ:', δ_cos, δ_sin)
        print('α:', α_cos, α_sin)
        print('β:', β_cos, β_sin)
        print('γ:', γ_cos, γ_sin)
    
    #Just discovered a bug with nmath inverse trigfuncs
    A_cos_numer = δ_cos-α_cos*β_cos
    A_cos_denom = α_sin*β_sin
    B_cos_numer =δ_cos-γ_cos*β_cos
    B_cos_denom = γ_sin*β_sin
    A_cos = A_cos_numer/A_cos_denom
    B_cos = B_cos_numer/B_cos_denom

    if testing:
        print()
        print(A_cos, B_cos)
    
    A = math.acos(A_cos)
    B = math.acos(B_cos)
    if testing:
        print()
        print(f'A and B: {A}, {B}')
    # with approximately 1.7374629934615633, (this is made from an imprecise
    # version of the calculation) as both the A and B values for
    # light(math.quaternion(0), math.quaternion(0, 2), math.quaternion(0, -1), 1)
    s_poly = 2*A + 2*B - math.tau
    #calculated value
    if testing:
        print()
        print('Function:', s_poly)
        #imprecise approximation
        print('Approx:', square_heron_points(s1, s2, s3, s4))
        print()
    return s_poly/square

def cos_and_sin(n):
    cos_val = 1-(n**2)/2
    sin_val = math.sqrt(1-cos_val**2)
    return cos_val, sin_val

def square_heron_points(a, b, c, d):
    a_, b_, c_, d_, h_= abs(a-b), abs(b-c), abs(c-d), abs(d-a), abs(b-d)
    t1=math.Heron(a_, b_, h_)
    t2 = math.Heron(c_, d_, h_)
    return t1+t2

def test(n=0):
    return light(math.quaternion(0), math.quaternion(0, 2), math.quaternion(0, -1, n).normal(), 1)

if __name__ == '__main__':
    testing =True
    print('test1:')
    print(test())
    print()
    print('test2:')
    print(test(1))
    print()
    print('test3:')
    print(test(3))
    print()
