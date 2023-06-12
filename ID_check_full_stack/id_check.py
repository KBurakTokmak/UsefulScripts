def id_check(id):
    error_message="None"
    if(not id.isnumeric()):#ID need to be all numbers
        error_message="ID is not all numbers"
        return (False,error_message)
    if(len(id)!=11):#id needs to be 11 numbers
        error_message="ID is not 11 Digits"
        return (False,error_message)
    if(int(id[0]==0)):#first element cant be 0
        error_message="First number of id cant be 0(zero)"
        return (False,error_message)
    check=(int(id[0])+int(id[2])+int(id[4])+int(id[6])+int(id[8]))*7-(int(id[1])+int(id[3])+int(id[5])+int(id[7]))
    check=check%10
    if(int(id[9])!=check):#(1+3+5+9)*7-(2+4+6+8) mod10 of this value needs to be equal to 10th
        error_message="4th math protocol failed , ID not valid"
        return (False,error_message)
    sum=0
    for x in range(0,10):
        sum+=int(id[x])
    if((sum%10)!=int(id[10])):#mod10 of sum of first 10 elements needs to be equal to 11th element
        error_message="5th math protocol failed, ID not valid"
        return (False,error_message)
    error_message="No error has been recieved"
    
    return (True,error_message)