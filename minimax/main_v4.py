import time
start_time=time.time()
def sort_common_list_desc(cp):
    n=len(cp)
    for i in range(0,n-1):
        for j in range(0,n-i-1):
            c1=sum([int(k) for k in cp[j][-7:]])
            c2=sum([int(k) for k in cp[j+1][-7:]])

            # print c1,c2
            if c1<c2:
                temp=cp[j]
                cp[j]=cp[j+1]
                cp[j+1]=temp
    return cp

def get_possible_moves(state,current_list):
    temp=[]
    for item in current_list:
        f=0
        for ele in state:
            if item==ele[0]:
                f=1
        if f==0:
            temp.append(item)
    return temp

def find_difference_between_list(list1,state_list):
    temp=[]
    for f_ele in list1:
        f=0
        for s_ele in state_list:
            if f_ele==s_ele[0]:
                f=1
        if f==0:
          temp.append(f_ele)
    return temp

def maxmax(state,player,sp,lp,result):

    best_sscore=None
    best_lscore=None
    if len(state)==len(sp):
        print 'inside base condition'
        print 'state=',state
        sscore=state[len(state)-1][1]
        lscore=state[len(state)-1][2]
        print 'sscore=',sscore
        print 'lscore=',lscore
        result.append([sscore,lscore])
        print "result=",result
        return result
    else:

                st1=get_possible_moves(state,sp)
                st2=get_possible_moves(state,cp)

                if player=='lahsa':
                    st2 = get_possible_moves(state, lp)
                    if st2==[]:
                        result=maxmax(state,'spla',sp,lp,result)
                    else:
                        for i in range(0,len(st2)):
                            # top_node = state[len( state ) - 1][0]
                            top_sscore = state[len( state ) - 1][1]
                            top_lscore = state[len( state ) - 1][2]
                            prev_lscore=top_lscore
                            cur_score=list(int(x) for x in st2[i][-7:])
                            lahsa_score=list(sum(x) for x in zip(prev_lscore,cur_score))
                            state.append([st2[i],top_sscore,lahsa_score,'lahsa'])
                            result=maxmax(state,'spla',sp,lp,result)

                        remove = state.pop()

                else:
                    st1 = get_possible_moves( state, sp )
                    for j in range(0,len(st1)):
                        top_sscore = state[len( state ) - 1][1]
                        top_lscore = state[len( state ) - 1][2]
                        prev_lscore=top_lscore
                        prev_sscore=top_sscore
                        cur_score = list( int( x ) for x in st1[j][-7:] )
                        spla_score = list( sum( x ) for x in zip( prev_sscore, cur_score ))
                        state.append([st1[j],spla_score,top_lscore,'spla'])
                        result=maxmax(state,'lahsa',sp,lp,result)

                    remove=state.pop()



                return result


fd=open('anirudh_input.txt','r')
b=int(fd.readline().rstrip())
p=int(fd.readline().strip())
nol=int(fd.readline().strip())
lahsa_added=[]
for i in range(0,nol):
    lahsa_added.append(fd.readline().rstrip())
nos=int(fd.readline().rstrip())
spla_added=[]
for i in range(0,nos):
    spla_added.append(fd.readline().rstrip())

noa=int(fd.readline().rstrip())
cp=[]
sp=[]
lp=[]
tp=[]
onlylp=[]
onlysp=[]
for i in range(0,noa):
    entry=fd.readline().rstrip()
    # print entry
    tp.append(entry)
    if entry[0:5] not in spla_added and entry[0:5] not in lahsa_added:

        gender=entry[5:6]
        age=int(entry[6:9])
        pets=entry[9:10]
        medical=entry[10:11]
        car=entry[11:12]
        licence=entry[12:13]
        if gender=='F' and pets=='N' and age>17 and medical=='N' and car=='Y' and licence=='Y':
            cp.append(entry)
        elif gender=='F' and pets=='N' and age>17:
            onlylp.append(entry)
        elif medical=='N' and car=='Y' and licence=='Y':
            onlysp.append(entry)



sp=cp+onlysp
lp=cp+onlylp

print 'lahsa_added=',lahsa_added
print 'spla_added=',spla_added
# print 'cp=',cp


# sp=sort_common_list_desc(sp)
# lp=sort_common_list_desc(lp)

print 'lp=',lp
print 'sp=',sp
print 'tp=',tp

# print 'after sorting cp=',cp



total_bed_rm=7*b
total_park_rm=7*p
beds_remaining=[b,b,b,b,b,b,b]
park_remaining=[p,p,p,p,p,p,p]

beds_so_far=[0]*7
park_so_far=[0]*7
for entry in tp:
    id=entry[0:5]
    if id in lahsa_added:
        days=list(entry[-7:])
        for i in range(0,7):
            beds_so_far[i]=beds_so_far[i]+int(days[i])

    elif id in spla_added:
        days=list(entry[-7:])
        for i in range(0,7):
            park_so_far[i]=park_so_far[i]+int(days[i])

print "park_so_far=",park_so_far
print "beds_so_far=",beds_so_far


max_score=None
best_move=None
global_max=None
for i in range(0,len(sp)):
    print '*********main loop****',i
    state=[]
    result=[]
    cur_park_so_far_spla=[0]*7
    for day in range(0,7):
        cur_park_so_far_spla[day]=park_so_far[day]+int(list(sp[i][-7:])[day])
    state.append([sp[i],cur_park_so_far_spla,beds_so_far,'spla'])
    print state
    # result.append([cur_park_so_far_spla,beds_so_far])
    # localsscore,locallscore=maxmax(state,'lahsa',cp)
    result=maxmax(state,'lahsa',sp,lp,result)
    # print "result=", result
    local_max_sscore = None
    local_max_lscore=None
    for s_l_score in result:
        sscore_list = s_l_score[0]
        lscore_list = s_l_score[1]
        local_sscore = sum(sscore_list)
        local_lscore = sum(lscore_list)
        if local_max_sscore < local_sscore:
            local_max_sscore = local_sscore
        if local_max_lscore < local_lscore:
            local_max_lscore=local_lscore

    print "cur_move=",sp[i]
    print "local_max_sscore=", local_max_sscore
    print "local_max_lscore=", local_max_lscore
    print "global_max_b=",global_max
    if global_max<local_max_sscore:
        # print 'inside global max if'
        global_max=local_max_sscore
        best_move=sp[i]

    elif global_max==local_max_sscore:

        old_id=int(best_move[0:5])
        cur_id=int(sp[i][0:5])
        print "inside global and local equal"
        print "cur_id=",cur_id
        print "old_id=",old_id
        if cur_id<old_id:
            best_move=sp[i]


print 'best_move=',best_move
print 'time taken=',time.time() - start_time


